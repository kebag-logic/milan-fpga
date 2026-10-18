`default_nettype none
module KL_srp_domain (
	clk_i,
	rst_n,
	link_up_i,
	rxdom_valid_i,
	rxdom_class_id_i,
	rxdom_prio_i,
	rxdom_vid_i,
	rxdom_nov_i,
	rxdom_lv_i,
	periodic_tick_i,
	leaveall_tick_i,
	tx_tick_i,
	dom_ev_valid_o,
	dom_ev_event_o,
	dom_ev_value_o,
	dom_ev_ready_i,
	evt_domain_change_o,
	class_a_prio_o,
	class_a_vid_o,
	adopted_o
);
	reg _sv2v_0;
	parameter [7:0] DEF_PRIO_P = 8'd3;
	parameter [15:0] DEF_VID_P = 16'd2;
	input wire clk_i;
	input wire rst_n;
	input wire link_up_i;
	input wire rxdom_valid_i;
	input wire [7:0] rxdom_class_id_i;
	input wire [7:0] rxdom_prio_i;
	input wire [15:0] rxdom_vid_i;
	input wire [12:0] rxdom_nov_i;
	input wire rxdom_lv_i;
	input wire periodic_tick_i;
	input wire leaveall_tick_i;
	input wire tx_tick_i;
	output wire dom_ev_valid_o;
	output wire [2:0] dom_ev_event_o;
	output wire [31:0] dom_ev_value_o;
	input wire dom_ev_ready_i;
	output reg evt_domain_change_o;
	output wire [2:0] class_a_prio_o;
	output wire [11:0] class_a_vid_o;
	output wire adopted_o;
	localparam [7:0] CLASS_A_ID_C = 8'd6;
	localparam [2:0] EV_NEW_C = 3'd0;
	localparam [2:0] EV_JOININ_C = 3'd1;
	localparam [2:0] EV_JOINMT_C = 3'd3;
	localparam [2:0] EV_LV_C = 3'd5;
	reg [7:0] decl_prio_r;
	reg [15:0] decl_vid_r;
	reg adopted_r;
	reg declared_r;
	reg link_q_r;
	reg q0_valid_r;
	reg q1_valid_r;
	reg [2:0] q0_ev_r;
	reg [2:0] q1_ev_r;
	reg [31:0] q0_val_r;
	reg [31:0] q1_val_r;
	reg rx_pend_v_r;
	reg [7:0] rx_pend_prio_r;
	reg [15:0] rx_pend_vid_r;
	reg rejoin_pend_r;
	reg rxla_pend_r;
	reg reg_in_r;
	reg pend_in_r;
	wire covers6_w;
	wire [7:0] surf_prio_w;
	wire link_rise_w;
	wire link_fall_w;
	wire q_empty_w;
	wire rx_is_decl_w;
	wire rx_is_pend_w;
	reg reg_in_nx_w;
	reg pend_in_nx_w;
	assign covers6_w = (rxdom_class_id_i <= CLASS_A_ID_C) && (({6'd0, rxdom_class_id_i} + {1'b0, rxdom_nov_i}) > 14'd6);
	assign surf_prio_w = rxdom_prio_i + (CLASS_A_ID_C - rxdom_class_id_i);
	assign link_rise_w = link_up_i && !link_q_r;
	assign link_fall_w = !link_up_i && link_q_r;
	assign q_empty_w = !q0_valid_r && !q1_valid_r;
	assign rx_is_decl_w = (declared_r && covers6_w) && ({surf_prio_w, rxdom_vid_i} == {decl_prio_r, decl_vid_r});
	assign rx_is_pend_w = ((declared_r && covers6_w) && rx_pend_v_r) && ({surf_prio_w, rxdom_vid_i} == {rx_pend_prio_r, rx_pend_vid_r});
	always @(*) begin : registrar_next
		if (_sv2v_0)
			;
		reg_in_nx_w = reg_in_r;
		pend_in_nx_w = pend_in_r;
		if (leaveall_tick_i && declared_r) begin
			reg_in_nx_w = 1'b0;
			pend_in_nx_w = 1'b0;
		end
		if (rxdom_valid_i && rx_is_decl_w)
			reg_in_nx_w = 1'b1;
		if (rxdom_valid_i && rx_is_pend_w)
			pend_in_nx_w = 1'b1;
		if (rxdom_lv_i && rx_is_decl_w)
			reg_in_nx_w = 1'b0;
		if (rxdom_lv_i && rx_is_pend_w)
			pend_in_nx_w = 1'b0;
	end
	always @(posedge clk_i) begin : domain_sm
		if (!rst_n) begin
			decl_prio_r <= DEF_PRIO_P;
			decl_vid_r <= DEF_VID_P;
			adopted_r <= 1'b0;
			declared_r <= 1'b0;
			link_q_r <= 1'b0;
			q0_valid_r <= 1'b0;
			q1_valid_r <= 1'b0;
			q0_ev_r <= 3'd0;
			q1_ev_r <= 3'd0;
			q0_val_r <= 32'd0;
			q1_val_r <= 32'd0;
			rx_pend_v_r <= 1'b0;
			rx_pend_prio_r <= 8'd0;
			rx_pend_vid_r <= 16'd0;
			rejoin_pend_r <= 1'b0;
			rxla_pend_r <= 1'b0;
			reg_in_r <= 1'b0;
			pend_in_r <= 1'b0;
			evt_domain_change_o <= 1'b0;
		end
		else begin
			evt_domain_change_o <= 1'b0;
			link_q_r <= link_up_i;
			reg_in_r <= reg_in_nx_w;
			pend_in_r <= pend_in_nx_w;
			if (q0_valid_r && dom_ev_ready_i) begin
				q0_valid_r <= q1_valid_r;
				q0_ev_r <= q1_ev_r;
				q0_val_r <= q1_val_r;
				q1_valid_r <= 1'b0;
			end
			if (((rxdom_valid_i && declared_r) && covers6_w) && ({surf_prio_w, rxdom_vid_i} != {decl_prio_r, decl_vid_r})) begin
				rx_pend_prio_r <= surf_prio_w;
				rx_pend_vid_r <= rxdom_vid_i;
				rx_pend_v_r <= 1'b1;
				pend_in_r <= 1'b1;
			end
			if ((periodic_tick_i || (leaveall_tick_i && tx_tick_i)) && declared_r)
				rejoin_pend_r <= 1'b1;
			if ((leaveall_tick_i && !tx_tick_i) && declared_r)
				rxla_pend_r <= 1'b1;
			if (tx_tick_i && rxla_pend_r) begin
				rxla_pend_r <= 1'b0;
				rejoin_pend_r <= 1'b1;
			end
			if (link_fall_w) begin
				if (adopted_r)
					evt_domain_change_o <= 1'b1;
				decl_prio_r <= DEF_PRIO_P;
				decl_vid_r <= DEF_VID_P;
				adopted_r <= 1'b0;
				declared_r <= 1'b0;
				q0_valid_r <= 1'b0;
				q1_valid_r <= 1'b0;
				rx_pend_v_r <= 1'b0;
				rejoin_pend_r <= 1'b0;
				rxla_pend_r <= 1'b0;
				reg_in_r <= 1'b0;
				pend_in_r <= 1'b0;
			end
			else if (link_rise_w) begin
				q0_valid_r <= 1'b1;
				q0_ev_r <= EV_NEW_C;
				q0_val_r <= {CLASS_A_ID_C, DEF_PRIO_P, DEF_VID_P};
				declared_r <= 1'b1;
				reg_in_r <= 1'b0;
				pend_in_r <= 1'b0;
			end
			else if (rx_pend_v_r && q_empty_w) begin
				q0_valid_r <= 1'b1;
				q0_ev_r <= EV_LV_C;
				q0_val_r <= {CLASS_A_ID_C, decl_prio_r, decl_vid_r};
				q1_valid_r <= 1'b1;
				q1_ev_r <= EV_NEW_C;
				q1_val_r <= {CLASS_A_ID_C, rx_pend_prio_r, rx_pend_vid_r};
				decl_prio_r <= rx_pend_prio_r;
				decl_vid_r <= rx_pend_vid_r;
				reg_in_r <= pend_in_nx_w;
				adopted_r <= 1'b1;
				rx_pend_v_r <= 1'b0;
				evt_domain_change_o <= 1'b1;
			end
			else if ((rejoin_pend_r && declared_r) && q_empty_w) begin
				q0_valid_r <= 1'b1;
				q0_ev_r <= (reg_in_r ? EV_JOININ_C : EV_JOINMT_C);
				q0_val_r <= {CLASS_A_ID_C, decl_prio_r, decl_vid_r};
				rejoin_pend_r <= 1'b0;
			end
		end
	end
	assign dom_ev_valid_o = q0_valid_r;
	assign dom_ev_event_o = q0_ev_r;
	assign dom_ev_value_o = q0_val_r;
	assign class_a_prio_o = decl_prio_r[2:0];
	assign class_a_vid_o = decl_vid_r[11:0];
	assign adopted_o = adopted_r;
	initial _sv2v_0 = 0;
endmodule
`default_nettype wire

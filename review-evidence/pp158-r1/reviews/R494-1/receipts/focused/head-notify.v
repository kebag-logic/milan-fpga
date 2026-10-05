`default_nettype none
`default_nettype wire
`default_nettype none
module KL_aecp_notify (
	clk_i,
	rst_n,
	rgy_req_i,
	rgy_state_i,
	rgy_op_i,
	rgy_eid_i,
	rgy_mac_i,
	rgy_tl_i,
	rgy_data_o,
	rgy_wait_o,
	ev_stri_in_i,
	ev_stri_out_i,
	ev_avb_i,
	ev_asp_i,
	ev_amap_i,
	ev_amap_remove_i,
	ev_amap_type_i,
	ev_amap_index_i,
	ev_amap_count_i,
	ev_amap_excl_eid_i,
	ev_ctr_i,
	ev_ctr_type_i,
	ev_ctr_index_i,
	ev_cmd_i,
	ev_cmd_class_i,
	ev_cmd_type_i,
	ev_cmd_index_i,
	ev_cmd_arg0_i,
	ev_cmd_arg1_i,
	ev_cmd_excl_eid_i,
	identify_button_i,
	identify_index_i,
	rx_cmd_valid_i,
	rx_cmd_eid_i,
	rx_cmd_mac_i,
	prng_draw_req_o,
	prng_draw_kind_o,
	prng_draw_busy_i,
	prng_draw_valid_i,
	prng_draw_ms_i,
	ca_valid_o,
	ca_owner_o,
	ca_ctlr_eid_o,
	ca_mac_o,
	ca_ready_i,
	ca_cancel_valid_o,
	ca_cancel_owner_o,
	ca_rsp_valid_i,
	ca_rsp_owner_i,
	ca_fail_valid_i,
	ca_fail_owner_i,
	uns_valid_o,
	uns_kind_o,
	uns_desc_type_o,
	uns_desc_index_o,
	uns_ctlr_eid_o,
	uns_mac_o,
	uns_seq_o,
	uns_amap_remove_o,
	uns_amap_count_o,
	uns_arg0_o,
	uns_arg1_o,
	uns_done_i,
	uns_tx_busy_i,
	amap_busy_o,
	lock_held_o,
	lock_ctlr_o,
	tmr_arm_valid_o,
	tmr_arm_cancel_o,
	tmr_arm_slot_o,
	tmr_arm_owner_o,
	tmr_arm_deadline_ms_o,
	now_ms_i,
	tmr_exp_valid_i,
	tmr_exp_slot_i,
	tmr_exp_owner_i,
	mon_arm_valid_o,
	mon_arm_cancel_o,
	mon_arm_slot_o,
	mon_arm_owner_o,
	mon_arm_deadline_ms_o,
	dbg_reg_cnt_o,
	dbg_uns_cnt_o,
	dbg_coalesce_o
);
	reg _sv2v_0;
	parameter [31:0] N_CTRL_P = 16;
	parameter [31:0] N_STREAM_IN_P = 8;
	parameter [31:0] N_STREAM_OUT_P = 8;
	parameter [31:0] TL_TIMEOUT_MS_P = 300000;
	parameter [31:0] LOCK_TIMEOUT_MS_P = 60000;
	parameter [31:0] TMR_SLOTS_P = 89;
	parameter [31:0] TMR_REGMON_BASE_P = 25;
	parameter [31:0] TMR_LOCK_SLOT_P = 61;
	parameter [31:0] TMR_IDENT_SLOT_P = 62;
	parameter [0:0] EN_IDENTIFY_NOTIF_P = 1'b0;
	localparam [31:0] TMR_AW_C = (TMR_SLOTS_P > 1 ? $clog2(TMR_SLOTS_P) : 1);
	localparam [31:0] CIX_W_C = (N_CTRL_P > 1 ? $clog2(N_CTRL_P) : 1);
	localparam [31:0] SIX_W_C = (N_STREAM_IN_P > 1 ? $clog2(N_STREAM_IN_P) : 1);
	localparam [31:0] SOX_W_C = (N_STREAM_OUT_P > 1 ? $clog2(N_STREAM_OUT_P) : 1);
	input wire clk_i;
	input wire rst_n;
	input wire rgy_req_i;
	input wire rgy_state_i;
	input wire [1:0] rgy_op_i;
	input wire [63:0] rgy_eid_i;
	input wire [47:0] rgy_mac_i;
	input wire rgy_tl_i;
	output wire [63:0] rgy_data_o;
	output wire rgy_wait_o;
	input wire [N_STREAM_IN_P - 1:0] ev_stri_in_i;
	input wire [N_STREAM_OUT_P - 1:0] ev_stri_out_i;
	input wire ev_avb_i;
	input wire ev_asp_i;
	input wire ev_amap_i;
	input wire ev_amap_remove_i;
	input wire [15:0] ev_amap_type_i;
	input wire [15:0] ev_amap_index_i;
	input wire [15:0] ev_amap_count_i;
	input wire [63:0] ev_amap_excl_eid_i;
	input wire ev_ctr_i;
	input wire [15:0] ev_ctr_type_i;
	input wire [15:0] ev_ctr_index_i;
	input wire ev_cmd_i;
	input wire [3:0] ev_cmd_class_i;
	input wire [15:0] ev_cmd_type_i;
	input wire [15:0] ev_cmd_index_i;
	input wire [15:0] ev_cmd_arg0_i;
	input wire [15:0] ev_cmd_arg1_i;
	input wire [63:0] ev_cmd_excl_eid_i;
	input wire identify_button_i;
	input wire [15:0] identify_index_i;
	input wire rx_cmd_valid_i;
	input wire [63:0] rx_cmd_eid_i;
	input wire [47:0] rx_cmd_mac_i;
	output reg prng_draw_req_o;
	output wire [2:0] prng_draw_kind_o;
	input wire prng_draw_busy_i;
	input wire prng_draw_valid_i;
	input wire [15:0] prng_draw_ms_i;
	output reg ca_valid_o;
	output reg [3:0] ca_owner_o;
	output reg [63:0] ca_ctlr_eid_o;
	output reg [47:0] ca_mac_o;
	input wire ca_ready_i;
	output reg ca_cancel_valid_o;
	output reg [3:0] ca_cancel_owner_o;
	input wire ca_rsp_valid_i;
	input wire [3:0] ca_rsp_owner_i;
	input wire ca_fail_valid_i;
	input wire [3:0] ca_fail_owner_i;
	output wire uns_valid_o;
	output wire [3:0] uns_kind_o;
	output wire [15:0] uns_desc_type_o;
	output wire [15:0] uns_desc_index_o;
	output wire [63:0] uns_ctlr_eid_o;
	output wire [47:0] uns_mac_o;
	output wire [15:0] uns_seq_o;
	output wire uns_amap_remove_o;
	output wire [15:0] uns_amap_count_o;
	output wire [15:0] uns_arg0_o;
	output wire [15:0] uns_arg1_o;
	input wire uns_done_i;
	input wire uns_tx_busy_i;
	output wire amap_busy_o;
	output wire lock_held_o;
	output wire [63:0] lock_ctlr_o;
	output reg tmr_arm_valid_o;
	output reg tmr_arm_cancel_o;
	output reg [TMR_AW_C - 1:0] tmr_arm_slot_o;
	localparam [31:0] pp_pkg_PP_TIMER_OWNER_W_C = 8;
	output reg [7:0] tmr_arm_owner_o;
	output reg [31:0] tmr_arm_deadline_ms_o;
	input wire [31:0] now_ms_i;
	input wire tmr_exp_valid_i;
	input wire [TMR_AW_C - 1:0] tmr_exp_slot_i;
	input wire [7:0] tmr_exp_owner_i;
	output reg mon_arm_valid_o;
	output reg mon_arm_cancel_o;
	output reg [TMR_AW_C - 1:0] mon_arm_slot_o;
	output reg [7:0] mon_arm_owner_o;
	output reg [31:0] mon_arm_deadline_ms_o;
	output reg [7:0] dbg_reg_cnt_o;
	output wire [15:0] dbg_uns_cnt_o;
	output wire [7:0] dbg_coalesce_o;
	(* ram_style = "distributed" *) reg [127:0] rows_r [0:N_CTRL_P - 1];
	reg [N_CTRL_P - 1:0] valid_r;
	reg [N_CTRL_P - 1:0] tl_r;
	reg [N_CTRL_P - 1:0] pend_r;
	reg [CIX_W_C - 1:0] rd_ix_w;
	wire [127:0] row_w;
	wire [63:0] row_eid_w;
	wire [47:0] row_mac_w;
	wire [15:0] row_seq_w;
	assign row_w = rows_r[rd_ix_w];
	assign row_eid_w = row_w[127:64];
	assign row_mac_w = row_w[63:16];
	assign row_seq_w = row_w[15:0];
	reg wr_en_r;
	reg [CIX_W_C - 1:0] wr_ix_r;
	reg [127:0] wr_row_r;
	always @(posedge clk_i) begin : row_write
		if (wr_en_r)
			rows_r[wr_ix_r] <= wr_row_r;
	end
	reg lk_held_r;
	reg [63:0] lk_ctlr_r;
	assign lock_held_o = lk_held_r;
	assign lock_ctlr_o = lk_ctlr_r;
	reg [N_STREAM_IN_P - 1:0] pe_sin_r;
	reg [N_STREAM_OUT_P - 1:0] pe_sout_r;
	reg pe_avb_r;
	reg pe_asp_r;
	reg pe_lock_r;
	reg pe_amap_r;
	reg amap_remove_r;
	reg [15:0] amap_type_r;
	reg [15:0] amap_index_r;
	reg [15:0] amap_count_r;
	reg [63:0] amap_excl_r;
	reg [63:0] lockx_eid_r;
	reg lockx_v_r;
	localparam [31:0] CMDQ_N_C = 16;
	reg [3:0] cmdq_class_r [0:15];
	reg [15:0] cmdq_type_r [0:15];
	reg [15:0] cmdq_index_r [0:15];
	reg [15:0] cmdq_arg0_r [0:15];
	reg [15:0] cmdq_arg1_r [0:15];
	reg [63:0] cmdq_excl_r [0:15];
	reg [3:0] cmdq_wr_r;
	reg [3:0] cmdq_rd_r;
	reg [4:0] cmdq_count_r;
	reg [15:0] cmdq_drop_r;
	wire cmd_class_ok_w;
	wire cmd_push_w;
	localparam [31:0] N_CTR_DESC_C = (N_STREAM_IN_P + N_STREAM_OUT_P) + 2;
	localparam [31:0] CTX_W_C = (N_CTR_DESC_C > 1 ? $clog2(N_CTR_DESC_C) : 1);
	localparam [15:0] DT_STREAM_INPUT_C = 16'h0005;
	localparam [15:0] DT_STREAM_OUTPUT_C = 16'h0006;
	localparam [15:0] DT_AVB_INTERFACE_C = 16'h0009;
	localparam [15:0] DT_CLOCK_DOMAIN_C = 16'h0024;
	reg [N_CTR_DESC_C - 1:0] ctr_dirty_r;
	reg [N_CTR_DESC_C - 1:0] ctr_pend_r;
	reg [N_CTR_DESC_C - 1:0] ctr_sent_r;
	reg [31:0] ctr_last_r [0:N_CTR_DESC_C - 1];
	reg ctr_ev_ok_w;
	reg [CTX_W_C - 1:0] ctr_ev_ix_w;
	reg [N_CTRL_P - 1:0] mon_draw_pend_r;
	reg [N_CTRL_P - 1:0] ca_pend_r;
	reg [N_CTRL_P - 1:0] ca_probe_r;
	reg mon_draw_wait_r;
	reg [CIX_W_C - 1:0] mon_draw_ix_r;
	reg mon_pick_ok_w;
	reg ca_pick_ok_w;
	reg ca_cancel_ok_w;
	reg [CIX_W_C - 1:0] mon_pick_ix_w;
	reg [CIX_W_C - 1:0] ca_pick_ix_w;
	reg [CIX_W_C - 1:0] ca_cancel_ix_w;
	reg [N_CTRL_P - 1:0] rx_cmd_hit_w;
	reg dh_v_r;
	reg [63:0] dh_eid_r;
	reg [47:0] dh_mac_r;
	reg [15:0] dh_seq_r;
	reg [3:0] n_st_r;
	reg req_done_r;
	reg [CIX_W_C - 1:0] wk_ix_r;
	reg wk_match_r;
	reg [CIX_W_C - 1:0] wk_match_ix_r;
	reg [15:0] wk_match_seq_r;
	reg wk_free_r;
	reg [CIX_W_C - 1:0] wk_free_ix_r;
	reg [63:0] hold_eid_r;
	reg [47:0] hold_mac_r;
	reg [15:0] hold_seq_r;
	reg op_tl_r;
	reg op_dereg_r;
	reg [1:0] result_r;
	reg result_q_r;
	reg em_active_r;
	reg [3:0] em_kind_r;
	reg [15:0] em_dt_r;
	reg [15:0] em_di_r;
	reg [15:0] em_arg0_r;
	reg [15:0] em_arg1_r;
	reg [63:0] em_excl_r;
	reg em_excl_v_r;
	reg em_amap_remove_r;
	reg [15:0] em_amap_count_r;
	reg em_dh_r;
	reg em_cmd_r;
	reg [CIX_W_C - 1:0] em_ix_r;
	reg [CTX_W_C - 1:0] em_ctr_ix_r;
	reg [15:0] uns_cnt_r;
	reg [7:0] coalesce_r;
	wire [31:0] deadline_w;
	assign deadline_w = now_ms_i + (rgy_req_i && rgy_op_i[1] ? LOCK_TIMEOUT_MS_P : TL_TIMEOUT_MS_P);
	wire rgy_new_w;
	assign rgy_new_w = rgy_req_i && !req_done_r;
	wire lk_is_holder_w;
	assign lk_is_holder_w = lk_held_r && (lk_ctlr_r == rgy_eid_i);
	wire lk_denied_w;
	assign lk_denied_w = lk_held_r && !lk_is_holder_w;
	wire wk_hit_w;
	assign wk_hit_w = (valid_r[wk_ix_r] && (row_eid_w == hold_eid_r)) && (row_mac_w == hold_mac_r);
	wire em_skip_w;
	assign em_skip_w = !valid_r[wk_ix_r] || (em_excl_v_r && (row_eid_w == em_excl_r));
	function automatic [31:0] sv2v_cast_32;
		input reg [31:0] inp;
		sv2v_cast_32 = inp;
	endfunction
	function automatic [CTX_W_C - 1:0] sv2v_cast_FA169;
		input reg [CTX_W_C - 1:0] inp;
		sv2v_cast_FA169 = inp;
	endfunction
	always @(*) begin : counter_event_map
		if (_sv2v_0)
			;
		ctr_ev_ok_w = 1'b0;
		ctr_ev_ix_w = 1'sb0;
		if ((ev_ctr_type_i == DT_STREAM_INPUT_C) && (sv2v_cast_32(ev_ctr_index_i) < N_STREAM_IN_P)) begin
			ctr_ev_ok_w = 1'b1;
			ctr_ev_ix_w = sv2v_cast_FA169(ev_ctr_index_i);
		end
		else if ((ev_ctr_type_i == DT_STREAM_OUTPUT_C) && (sv2v_cast_32(ev_ctr_index_i) < N_STREAM_OUT_P)) begin
			ctr_ev_ok_w = 1'b1;
			ctr_ev_ix_w = sv2v_cast_FA169(N_STREAM_IN_P + sv2v_cast_32(ev_ctr_index_i));
		end
		else if ((ev_ctr_type_i == DT_AVB_INTERFACE_C) && (ev_ctr_index_i == 16'd0)) begin
			ctr_ev_ok_w = 1'b1;
			ctr_ev_ix_w = sv2v_cast_FA169(N_STREAM_IN_P + N_STREAM_OUT_P);
		end
		else if ((ev_ctr_type_i == DT_CLOCK_DOMAIN_C) && (ev_ctr_index_i == 16'd0)) begin
			ctr_ev_ok_w = 1'b1;
			ctr_ev_ix_w = sv2v_cast_FA169((N_STREAM_IN_P + N_STREAM_OUT_P) + 1);
		end
	end
	assign cmd_class_ok_w = |{ev_cmd_class_i == 4'd1, ev_cmd_class_i == 4'd2, ev_cmd_class_i == 4'd3, ev_cmd_class_i == 4'd4, ev_cmd_class_i == 4'd5, ev_cmd_class_i == 4'd7, ev_cmd_class_i == 4'd8, ev_cmd_class_i == 4'd9};
	function automatic [4:0] sv2v_cast_5;
		input reg [4:0] inp;
		sv2v_cast_5 = inp;
	endfunction
	assign cmd_push_w = (ev_cmd_i && cmd_class_ok_w) && (cmdq_count_r < sv2v_cast_5(CMDQ_N_C));
	function automatic signed [CIX_W_C - 1:0] sv2v_cast_17814_signed;
		input reg signed [CIX_W_C - 1:0] inp;
		sv2v_cast_17814_signed = inp;
	endfunction
	function automatic signed [31:0] sv2v_cast_32_signed;
		input reg signed [31:0] inp;
		sv2v_cast_32_signed = inp;
	endfunction
	always @(*) begin : monitor_pick
		if (_sv2v_0)
			;
		mon_pick_ok_w = 1'b0;
		mon_pick_ix_w = 1'sb0;
		ca_pick_ok_w = 1'b0;
		ca_pick_ix_w = 1'sb0;
		ca_cancel_ok_w = 1'b0;
		ca_cancel_ix_w = 1'sb0;
		begin : sv2v_autoblock_1
			reg signed [31:0] i;
			for (i = sv2v_cast_32_signed(N_CTRL_P) - 1; i >= 0; i = i - 1)
				begin
					if ((mon_draw_pend_r[i] && valid_r[i]) && !ca_probe_r[i]) begin
						mon_pick_ok_w = 1'b1;
						mon_pick_ix_w = sv2v_cast_17814_signed(i);
					end
					if (((ca_pend_r[i] && valid_r[i]) && !ca_probe_r[i]) && !rx_cmd_hit_w[i]) begin
						ca_pick_ok_w = 1'b1;
						ca_pick_ix_w = sv2v_cast_17814_signed(i);
					end
					if (rx_cmd_hit_w[i] && ca_probe_r[i]) begin
						ca_cancel_ok_w = 1'b1;
						ca_cancel_ix_w = sv2v_cast_17814_signed(i);
					end
				end
		end
	end
	localparam [31:0] IXC_W_C = 6;
	localparam [31:0] N_IXC_C = 19;
	wire [(N_IXC_C * IXC_W_C) - 1:0] ix_key_w;
	wire [(N_IXC_C * IXC_W_C) - 1:0] ix_row_w;
	wire [127:0] ix_wr_row_w;
	reg ix_clr_r;
	reg ix_set_r;
	wire ix_busy_w;
	wire ix_own_w;
	wire [N_CTRL_P - 1:0] ix_hit_w;
	assign ix_wr_row_w = rows_r[wr_ix_r];
	function automatic [(N_IXC_C * 32'd6) - 1:0] sv2v_cast_E0530;
		input reg [(N_IXC_C * 32'd6) - 1:0] inp;
		sv2v_cast_E0530 = inp;
	endfunction
	assign ix_key_w = sv2v_cast_E0530({rx_cmd_eid_i, rx_cmd_mac_i});
	assign ix_row_w = sv2v_cast_E0530(ix_wr_row_w[127:16]);
	assign ix_busy_w = ix_clr_r || ix_set_r;
	assign ix_own_w = ix_wr_row_w[127:16] == {rx_cmd_eid_i, rx_cmd_mac_i};
	genvar _gv_i_1;
	generate
		for (_gv_i_1 = 0; _gv_i_1 < N_CTRL_P; _gv_i_1 = _gv_i_1 + 1) begin : g_ix_row
			localparam i = _gv_i_1;
			wire [18:0] ch_w;
			genvar _gv_j_1;
			for (_gv_j_1 = 0; _gv_j_1 < N_IXC_C; _gv_j_1 = _gv_j_1 + 1) begin : g_ix_chunk
				localparam j = _gv_j_1;
				(* ram_style = "distributed" *) reg mem_r [0:63];
				initial begin : sv2v_autoblock_2
					reg signed [31:0] a;
					for (a = 0; a < 64; a = a + 1)
						mem_r[a] = 1'b0;
				end
				always @(posedge clk_i) begin : ix_write
					if (ix_busy_w && (wr_ix_r == sv2v_cast_17814_signed(i)))
						mem_r[ix_row_w[j * IXC_W_C+:IXC_W_C]] <= ix_set_r;
				end
				assign ch_w[j] = mem_r[ix_key_w[j * IXC_W_C+:IXC_W_C]];
			end
			assign ix_hit_w[i] = &ch_w;
		end
	endgenerate
	function automatic [CIX_W_C - 1:0] sv2v_cast_17814;
		input reg [CIX_W_C - 1:0] inp;
		sv2v_cast_17814 = inp;
	endfunction
	always @(*) begin : command_registry_hit
		if (_sv2v_0)
			;
		rx_cmd_hit_w = 1'sb0;
		begin : sv2v_autoblock_3
			reg [31:0] i;
			for (i = 0; i < N_CTRL_P; i = i + 1)
				rx_cmd_hit_w[i] = (rx_cmd_valid_i && valid_r[i]) && (ix_busy_w && (wr_ix_r == sv2v_cast_17814(i)) ? ix_own_w : ix_hit_w[i]);
		end
	end
	reg pd_any_w;
	reg [CIX_W_C - 1:0] pd_ix_w;
	function automatic [3:0] sv2v_cast_4;
		input reg [3:0] inp;
		sv2v_cast_4 = inp;
	endfunction
	always @(*) begin : ca_request
		if (_sv2v_0)
			;
		ca_valid_o = ca_pick_ok_w;
		ca_owner_o = sv2v_cast_4(ca_pick_ix_w);
		ca_ctlr_eid_o = rows_r[ca_pick_ix_w][127:64];
		ca_mac_o = rows_r[ca_pick_ix_w][63:16];
		ca_cancel_valid_o = ca_cancel_ok_w || ((n_st_r == 4'd4) && ca_probe_r[pd_ix_w]);
		ca_cancel_owner_o = ((n_st_r == 4'd4) && ca_probe_r[pd_ix_w] ? sv2v_cast_4(pd_ix_w) : sv2v_cast_4(ca_cancel_ix_w));
	end
	reg pick_any_w;
	reg [3:0] pick_kind_w;
	reg [15:0] pick_dt_w;
	reg [15:0] pick_di_w;
	reg [15:0] pick_arg0_w;
	reg [15:0] pick_arg1_w;
	reg pick_cmd_w;
	reg [CTX_W_C - 1:0] pick_ctr_ix_w;
	localparam [3:0] pp_pkg_PP_UNS_AMAP_C = 4'd5;
	localparam [3:0] pp_pkg_PP_UNS_ASP_C = 4'd4;
	localparam [3:0] pp_pkg_PP_UNS_AVB_C = 4'd3;
	localparam [3:0] pp_pkg_PP_UNS_CFG_C = 4'd9;
	localparam [3:0] pp_pkg_PP_UNS_CLKS_C = 4'd13;
	localparam [3:0] pp_pkg_PP_UNS_CTRL_C = 4'd12;
	localparam [3:0] pp_pkg_PP_UNS_CTRS_C = 4'd6;
	localparam [3:0] pp_pkg_PP_UNS_DEREG_C = 4'd0;
	localparam [3:0] pp_pkg_PP_UNS_LOCK_C = 4'd1;
	localparam [3:0] pp_pkg_PP_UNS_NAME_C = 4'd8;
	localparam [3:0] pp_pkg_PP_UNS_SFMT_C = 4'd10;
	localparam [3:0] pp_pkg_PP_UNS_SINFO_C = 4'd11;
	localparam [3:0] pp_pkg_PP_UNS_SRATE_C = 4'd7;
	localparam [3:0] pp_pkg_PP_UNS_STRI_C = 4'd2;
	localparam [3:0] pp_pkg_PP_UNS_STRM_C = 4'd14;
	function automatic [15:0] sv2v_cast_16;
		input reg [15:0] inp;
		sv2v_cast_16 = inp;
	endfunction
	always @(*) begin : emit_pick
		if (_sv2v_0)
			;
		pick_any_w = 1'b1;
		pick_kind_w = pp_pkg_PP_UNS_LOCK_C;
		pick_dt_w = 16'h0000;
		pick_di_w = 16'd0;
		pick_arg0_w = 16'd0;
		pick_arg1_w = 16'd0;
		pick_cmd_w = 1'b0;
		pick_ctr_ix_w = 1'sb0;
		if (pe_lock_r)
			pick_kind_w = pp_pkg_PP_UNS_LOCK_C;
		else if (cmdq_count_r != 5'd0) begin
			pick_cmd_w = 1'b1;
			pick_dt_w = cmdq_type_r[cmdq_rd_r];
			pick_di_w = cmdq_index_r[cmdq_rd_r];
			pick_arg0_w = cmdq_arg0_r[cmdq_rd_r];
			pick_arg1_w = cmdq_arg1_r[cmdq_rd_r];
			(* full_case, parallel_case *)
			case (cmdq_class_r[cmdq_rd_r])
				4'd1: pick_kind_w = pp_pkg_PP_UNS_CFG_C;
				4'd2: pick_kind_w = pp_pkg_PP_UNS_SFMT_C;
				4'd3: pick_kind_w = pp_pkg_PP_UNS_SINFO_C;
				4'd4: pick_kind_w = pp_pkg_PP_UNS_CTRL_C;
				4'd5: pick_kind_w = pp_pkg_PP_UNS_SRATE_C;
				4'd7: pick_kind_w = pp_pkg_PP_UNS_NAME_C;
				4'd8: pick_kind_w = pp_pkg_PP_UNS_CLKS_C;
				4'd9: pick_kind_w = pp_pkg_PP_UNS_STRM_C;
				default: pick_kind_w = pp_pkg_PP_UNS_DEREG_C;
			endcase
		end
		else if (pe_amap_r) begin
			pick_kind_w = pp_pkg_PP_UNS_AMAP_C;
			pick_dt_w = amap_type_r;
			pick_di_w = amap_index_r;
		end
		else if (pe_avb_r) begin
			pick_kind_w = pp_pkg_PP_UNS_AVB_C;
			pick_dt_w = 16'h0009;
		end
		else if (pe_asp_r) begin
			pick_kind_w = pp_pkg_PP_UNS_ASP_C;
			pick_dt_w = 16'h0009;
		end
		else begin
			pick_any_w = 1'b0;
			begin : sv2v_autoblock_4
				reg [31:0] c;
				for (c = 0; c < N_CTR_DESC_C; c = c + 1)
					if (!pick_any_w && ctr_pend_r[c]) begin
						pick_any_w = 1'b1;
						pick_kind_w = pp_pkg_PP_UNS_CTRS_C;
						pick_ctr_ix_w = sv2v_cast_FA169(c);
						if (c < N_STREAM_IN_P) begin
							pick_dt_w = DT_STREAM_INPUT_C;
							pick_di_w = sv2v_cast_16(c);
						end
						else if (c < (N_STREAM_IN_P + N_STREAM_OUT_P)) begin
							pick_dt_w = DT_STREAM_OUTPUT_C;
							pick_di_w = sv2v_cast_16(c - N_STREAM_IN_P);
						end
						else if (c == (N_STREAM_IN_P + N_STREAM_OUT_P)) begin
							pick_dt_w = DT_AVB_INTERFACE_C;
							pick_di_w = 16'd0;
						end
						else begin
							pick_dt_w = DT_CLOCK_DOMAIN_C;
							pick_di_w = 16'd0;
						end
					end
			end
			begin : sv2v_autoblock_5
				reg [31:0] s;
				for (s = 0; s < N_STREAM_IN_P; s = s + 1)
					if (!pick_any_w && pe_sin_r[s]) begin
						pick_any_w = 1'b1;
						pick_kind_w = pp_pkg_PP_UNS_STRI_C;
						pick_dt_w = 16'h0005;
						pick_di_w = sv2v_cast_16(s);
					end
			end
			begin : sv2v_autoblock_6
				reg [31:0] s;
				for (s = 0; s < N_STREAM_OUT_P; s = s + 1)
					if (!pick_any_w && pe_sout_r[s]) begin
						pick_any_w = 1'b1;
						pick_kind_w = pp_pkg_PP_UNS_STRI_C;
						pick_dt_w = 16'h0006;
						pick_di_w = sv2v_cast_16(s);
					end
			end
		end
	end
	wire exp_row_w;
	wire exp_lock_w;
	wire exp_mon_w;
	wire [CIX_W_C - 1:0] exp_ix_w;
	assign exp_ix_w = tmr_exp_owner_i[CIX_W_C - 1:0];
	localparam [7:0] pp_pkg_PP_OWN_NTFY_C = 8'ha0;
	function automatic [TMR_AW_C - 1:0] sv2v_cast_5A563;
		input reg [TMR_AW_C - 1:0] inp;
		sv2v_cast_5A563 = inp;
	endfunction
	assign exp_row_w = (tmr_exp_valid_i && (tmr_exp_owner_i[7:CIX_W_C] == pp_pkg_PP_OWN_NTFY_C[7:CIX_W_C])) && (tmr_exp_slot_i == sv2v_cast_5A563(TMR_REGMON_BASE_P + sv2v_cast_32(exp_ix_w)));
	localparam [7:0] pp_pkg_PP_OWN_LOCK_C = 8'hb0;
	assign exp_lock_w = (tmr_exp_valid_i && (tmr_exp_owner_i == pp_pkg_PP_OWN_LOCK_C)) && (tmr_exp_slot_i == sv2v_cast_5A563(TMR_LOCK_SLOT_P));
	localparam [7:0] pp_pkg_PP_OWN_CMON_C = 8'hd0;
	assign exp_mon_w = (tmr_exp_valid_i && (tmr_exp_owner_i[7:CIX_W_C] == pp_pkg_PP_OWN_CMON_C[7:CIX_W_C])) && (tmr_exp_slot_i == sv2v_cast_5A563((TMR_REGMON_BASE_P + N_CTRL_P) + sv2v_cast_32(exp_ix_w)));
	always @(*) begin : pend_pick
		if (_sv2v_0)
			;
		pd_any_w = 1'b0;
		pd_ix_w = 1'sb0;
		begin : sv2v_autoblock_7
			reg signed [31:0] i;
			for (i = sv2v_cast_32_signed(N_CTRL_P) - 1; i >= 0; i = i - 1)
				if (pend_r[i]) begin
					pd_any_w = 1'b1;
					pd_ix_w = sv2v_cast_17814_signed(i);
				end
		end
	end
	always @(*) begin : read_mux
		if (_sv2v_0)
			;
		(* full_case, parallel_case *)
		case (n_st_r)
			4'd4: rd_ix_w = pd_ix_w;
			default: rd_ix_w = wk_ix_r;
		endcase
	end
	assign rgy_wait_o = n_st_r != 4'd3;
	assign rgy_data_o = (result_q_r ? (lk_held_r ? lk_ctlr_r : 64'd0) : {62'd0, result_r});
	localparam [31:0] IDENT_BURST_MS_C = 150;
	localparam [31:0] IDENT_REARM_MS_C = 1000;
	localparam [15:0] DT_CONTROL_C = 16'h001a;
	wire id_own_w;
	wire id_arm_gnt_w;
	wire [TMR_AW_C - 1:0] id_arm_slot_w;
	wire [7:0] id_arm_owner_w;
	wire [31:0] id_arm_deadline_w;
	wire core_done_w;
	wire core_arm_w;
	assign core_arm_w = (n_st_r == 4'd2) || ((n_st_r == 4'd0) && rgy_new_w);
	localparam [63:0] pp_pkg_PP_IDENT_CTLR_EID_C = 64'h90e0f0fffe010001;
	localparam [47:0] pp_pkg_PP_IDENT_MCAST_MAC_C = 48'h91e0f0010001;
	localparam [7:0] pp_pkg_PP_OWN_IDENT_C = 8'hb1;
	localparam [3:0] pp_pkg_PP_UNS_IDENT_C = 4'd15;
	generate
		if (EN_IDENTIFY_NOTIF_P) begin : gen_ident
			localparam [1:0] I_WAIT = 2'd0;
			localparam [1:0] I_SEND = 2'd1;
			localparam [1:0] I_GAP = 2'd2;
			localparam [1:0] I_HOLD = 2'd3;
			reg [1:0] i_st_r;
			(* ASYNC_REG = "TRUE" *) reg btn_q1_r;
			(* ASYNC_REG = "TRUE" *) reg btn_q2_r;
			reg job_r;
			reg own_r;
			reg left_r;
			reg [1:0] ix_r;
			reg [15:0] seq_r;
			reg [31:0] t0_r;
			reg gen_r;
			reg rel_r;
			reg prs_r;
			reg fired_r;
			reg gap_r;
			reg armb_r;
			reg armr_r;
			wire exp_b_w;
			wire exp_r_w;
			wire done_w;
			wire dep_w;
			wire [7:0] rearm_owner_w;
			assign rearm_owner_w = (pp_pkg_PP_OWN_IDENT_C + 8'd1) + {7'd0, gen_r};
			assign exp_b_w = (tmr_exp_valid_i && (tmr_exp_owner_i == pp_pkg_PP_OWN_IDENT_C)) && (tmr_exp_slot_i == sv2v_cast_5A563(TMR_IDENT_SLOT_P));
			assign exp_r_w = (tmr_exp_valid_i && (tmr_exp_owner_i == rearm_owner_w)) && (tmr_exp_slot_i == sv2v_cast_5A563(TMR_IDENT_SLOT_P + 1));
			assign done_w = own_r && uns_done_i;
			assign dep_w = (done_w || left_r) && !uns_tx_busy_i;
			assign id_own_w = own_r;
			assign core_done_w = uns_done_i && !own_r;
			assign id_arm_gnt_w = (armb_r || armr_r) && !core_arm_w;
			assign id_arm_slot_w = (armb_r ? sv2v_cast_5A563(TMR_IDENT_SLOT_P) : sv2v_cast_5A563(TMR_IDENT_SLOT_P + 1));
			assign id_arm_owner_w = (armb_r ? pp_pkg_PP_OWN_IDENT_C : rearm_owner_w);
			assign id_arm_deadline_w = (armb_r ? now_ms_i + sv2v_cast_32(151) : t0_r + IDENT_REARM_MS_C);
			assign uns_valid_o = own_r || (n_st_r == 4'd6);
			assign uns_kind_o = (own_r ? pp_pkg_PP_UNS_IDENT_C : em_kind_r);
			assign uns_desc_type_o = (own_r ? DT_CONTROL_C : em_dt_r);
			assign uns_desc_index_o = (own_r ? identify_index_i : em_di_r);
			assign uns_ctlr_eid_o = (own_r ? pp_pkg_PP_IDENT_CTLR_EID_C : hold_eid_r);
			assign uns_mac_o = (own_r ? pp_pkg_PP_IDENT_MCAST_MAC_C : hold_mac_r);
			assign uns_seq_o = (own_r ? seq_r : hold_seq_r);
			always @(posedge clk_i) begin : identify_sequencer
				if (!rst_n) begin
					i_st_r <= I_WAIT;
					btn_q1_r <= 1'b0;
					btn_q2_r <= 1'b0;
					job_r <= 1'b0;
					own_r <= 1'b0;
					left_r <= 1'b0;
					ix_r <= 2'd0;
					seq_r <= 16'd0;
					t0_r <= 32'd0;
					gen_r <= 1'b0;
					rel_r <= 1'b0;
					prs_r <= 1'b0;
					fired_r <= 1'b0;
					gap_r <= 1'b0;
					armb_r <= 1'b0;
					armr_r <= 1'b0;
				end
				else begin
					btn_q1_r <= identify_button_i;
					btn_q2_r <= btn_q1_r;
					if (id_arm_gnt_w) begin
						if (armb_r)
							armb_r <= 1'b0;
						else
							armr_r <= 1'b0;
					end
					if ((job_r && !own_r) && (n_st_r != 4'd6))
						own_r <= 1'b1;
					if (done_w) begin
						own_r <= 1'b0;
						job_r <= 1'b0;
					end
					if (dep_w)
						left_r <= 1'b0;
					else if (done_w)
						left_r <= 1'b1;
					if (exp_b_w)
						gap_r <= 1'b0;
					if (exp_r_w && (i_st_r != I_WAIT))
						fired_r <= 1'b1;
					if ((btn_q2_r && rel_r) && (i_st_r != I_WAIT))
						prs_r <= 1'b1;
					(* full_case, parallel_case *)
					case (i_st_r)
						I_WAIT: begin
							if (btn_q2_r && gap_r)
								prs_r <= 1'b1;
							if ((btn_q2_r || prs_r) && !gap_r) begin
								job_r <= 1'b1;
								ix_r <= 2'd0;
								rel_r <= 1'b0;
								prs_r <= 1'b0;
								i_st_r <= I_SEND;
							end
						end
						I_SEND: begin
							if (!btn_q2_r)
								rel_r <= 1'b1;
							if (dep_w) begin
								armb_r <= 1'b1;
								gap_r <= 1'b1;
								if (ix_r == 2'd0) begin
									t0_r <= now_ms_i + 32'd1;
									gen_r <= !gen_r;
									fired_r <= 1'b0;
									armr_r <= 1'b1;
									ix_r <= 2'd1;
									i_st_r <= I_GAP;
								end
								else if (ix_r == 2'd1) begin
									ix_r <= 2'd2;
									i_st_r <= I_GAP;
								end
								else begin
									seq_r <= seq_r + 16'd1;
									i_st_r <= I_HOLD;
								end
							end
						end
						I_GAP: begin
							if (!btn_q2_r)
								rel_r <= 1'b1;
							if (exp_b_w) begin
								job_r <= 1'b1;
								i_st_r <= I_SEND;
							end
						end
						I_HOLD:
							if (!btn_q2_r)
								i_st_r <= I_WAIT;
							else if (((rel_r || fired_r) || exp_r_w) && !gap_r) begin
								job_r <= 1'b1;
								ix_r <= 2'd0;
								rel_r <= 1'b0;
								prs_r <= 1'b0;
								i_st_r <= I_SEND;
							end
						default: i_st_r <= I_WAIT;
					endcase
				end
			end
		end
		else begin : gen_no_ident
			assign id_own_w = 1'b0;
			assign id_arm_gnt_w = 1'b0;
			assign id_arm_slot_w = 1'sb0;
			assign id_arm_owner_w = 1'sb0;
			assign id_arm_deadline_w = 32'd0;
			assign core_done_w = uns_done_i;
			assign uns_valid_o = n_st_r == 4'd6;
			assign uns_kind_o = em_kind_r;
			assign uns_desc_type_o = em_dt_r;
			assign uns_desc_index_o = em_di_r;
			assign uns_ctlr_eid_o = hold_eid_r;
			assign uns_mac_o = hold_mac_r;
			assign uns_seq_o = hold_seq_r;
		end
	endgenerate
	assign uns_amap_remove_o = em_amap_remove_r;
	assign uns_amap_count_o = em_amap_count_r;
	assign uns_arg0_o = em_arg0_r;
	assign uns_arg1_o = em_arg1_r;
	assign amap_busy_o = (((((((((dh_v_r || em_active_r) || pe_lock_r) || pe_amap_r) || pe_avb_r) || pe_asp_r) || |pe_sin_r) || |pe_sout_r) || (cmdq_count_r != 5'd0)) || |ctr_pend_r) || id_own_w;
	assign prng_draw_kind_o = 3'd4;
	assign dbg_uns_cnt_o = uns_cnt_r;
	assign dbg_coalesce_o = coalesce_r;
	always @(*) begin : reg_count
		if (_sv2v_0)
			;
		dbg_reg_cnt_o = 8'd0;
		begin : sv2v_autoblock_8
			reg [31:0] i;
			for (i = 0; i < N_CTRL_P; i = i + 1)
				dbg_reg_cnt_o = dbg_reg_cnt_o + {7'd0, valid_r[i]};
		end
	end
	always @(posedge clk_i) begin : notify_core
		if (!rst_n) begin
			n_st_r <= 4'd0;
			valid_r <= 1'sb0;
			tl_r <= 1'sb0;
			pend_r <= 1'sb0;
			lk_held_r <= 1'b0;
			lk_ctlr_r <= 64'd0;
			pe_sin_r <= 1'sb0;
			pe_sout_r <= 1'sb0;
			pe_avb_r <= 1'b0;
			pe_asp_r <= 1'b0;
			pe_lock_r <= 1'b0;
			pe_amap_r <= 1'b0;
			cmdq_wr_r <= 4'd0;
			cmdq_rd_r <= 4'd0;
			cmdq_count_r <= 5'd0;
			cmdq_drop_r <= 16'd0;
			ctr_dirty_r <= 1'sb0;
			ctr_pend_r <= 1'sb0;
			ctr_sent_r <= 1'sb0;
			mon_draw_pend_r <= 1'sb0;
			ca_pend_r <= 1'sb0;
			ca_probe_r <= 1'sb0;
			mon_draw_wait_r <= 1'b0;
			mon_draw_ix_r <= 1'sb0;
			prng_draw_req_o <= 1'b0;
			mon_arm_valid_o <= 1'b0;
			mon_arm_cancel_o <= 1'b0;
			mon_arm_slot_o <= 1'sb0;
			mon_arm_owner_o <= 1'sb0;
			mon_arm_deadline_ms_o <= 32'd0;
			amap_remove_r <= 1'b0;
			amap_type_r <= 16'd0;
			amap_index_r <= 16'd0;
			amap_count_r <= 16'd0;
			amap_excl_r <= 64'd0;
			lockx_eid_r <= 64'd0;
			lockx_v_r <= 1'b0;
			dh_v_r <= 1'b0;
			dh_eid_r <= 64'd0;
			dh_mac_r <= 48'd0;
			dh_seq_r <= 16'd0;
			req_done_r <= 1'b0;
			wk_ix_r <= 1'sb0;
			wk_match_r <= 1'b0;
			wk_match_ix_r <= 1'sb0;
			wk_match_seq_r <= 16'd0;
			wk_free_r <= 1'b0;
			wk_free_ix_r <= 1'sb0;
			hold_eid_r <= 64'd0;
			hold_mac_r <= 48'd0;
			hold_seq_r <= 16'd0;
			op_tl_r <= 1'b0;
			op_dereg_r <= 1'b0;
			result_r <= 2'd0;
			result_q_r <= 1'b0;
			em_active_r <= 1'b0;
			em_kind_r <= 4'd0;
			em_dt_r <= 16'd0;
			em_di_r <= 16'd0;
			em_arg0_r <= 16'd0;
			em_arg1_r <= 16'd0;
			em_excl_r <= 64'd0;
			em_excl_v_r <= 1'b0;
			em_amap_remove_r <= 1'b0;
			em_amap_count_r <= 16'd0;
			em_dh_r <= 1'b0;
			em_cmd_r <= 1'b0;
			em_ix_r <= 1'sb0;
			em_ctr_ix_r <= 1'sb0;
			uns_cnt_r <= 16'd0;
			coalesce_r <= 8'd0;
			wr_en_r <= 1'b0;
			wr_ix_r <= 1'sb0;
			wr_row_r <= 1'sb0;
			ix_clr_r <= 1'b0;
			ix_set_r <= 1'b0;
			tmr_arm_valid_o <= 1'b0;
			tmr_arm_cancel_o <= 1'b0;
			tmr_arm_slot_o <= 1'sb0;
			tmr_arm_owner_o <= 1'sb0;
			tmr_arm_deadline_ms_o <= 32'd0;
		end
		else begin
			wr_en_r <= 1'b0;
			ix_clr_r <= 1'b0;
			ix_set_r <= ix_clr_r;
			tmr_arm_valid_o <= 1'b0;
			prng_draw_req_o <= 1'b0;
			mon_arm_valid_o <= 1'b0;
			if (!rgy_req_i)
				req_done_r <= 1'b0;
			begin : sv2v_autoblock_9
				reg [31:0] s;
				for (s = 0; s < N_STREAM_IN_P; s = s + 1)
					if (ev_stri_in_i[s])
						pe_sin_r[s] <= 1'b1;
			end
			begin : sv2v_autoblock_10
				reg [31:0] s;
				for (s = 0; s < N_STREAM_OUT_P; s = s + 1)
					if (ev_stri_out_i[s])
						pe_sout_r[s] <= 1'b1;
			end
			if (ev_avb_i)
				pe_avb_r <= 1'b1;
			if (ev_asp_i)
				pe_asp_r <= 1'b1;
			if (ev_amap_i) begin
				pe_amap_r <= 1'b1;
				amap_remove_r <= ev_amap_remove_i;
				amap_type_r <= ev_amap_type_i;
				amap_index_r <= ev_amap_index_i;
				amap_count_r <= ev_amap_count_i;
				amap_excl_r <= ev_amap_excl_eid_i;
			end
			if (ev_cmd_i && cmd_class_ok_w) begin
				if (cmd_push_w) begin
					cmdq_class_r[cmdq_wr_r] <= ev_cmd_class_i;
					cmdq_type_r[cmdq_wr_r] <= ev_cmd_type_i;
					cmdq_index_r[cmdq_wr_r] <= ev_cmd_index_i;
					cmdq_arg0_r[cmdq_wr_r] <= ev_cmd_arg0_i;
					cmdq_arg1_r[cmdq_wr_r] <= ev_cmd_arg1_i;
					cmdq_excl_r[cmdq_wr_r] <= ev_cmd_excl_eid_i;
					cmdq_wr_r <= cmdq_wr_r + 4'd1;
					cmdq_count_r <= cmdq_count_r + 5'd1;
				end
				else if (cmdq_drop_r != 16'hffff)
					cmdq_drop_r <= cmdq_drop_r + 16'd1;
			end
			if (ev_ctr_i && ctr_ev_ok_w)
				ctr_dirty_r[ctr_ev_ix_w] <= 1'b1;
			begin : sv2v_autoblock_11
				reg [31:0] c;
				for (c = 0; c < N_CTR_DESC_C; c = c + 1)
					if ((ctr_dirty_r[c] && !ctr_pend_r[c]) && (!ctr_sent_r[c] || ((now_ms_i - ctr_last_r[c]) >= 32'd1000))) begin
						ctr_dirty_r[c] <= 1'b0;
						ctr_pend_r[c] <= 1'b1;
					end
			end
			begin : sv2v_autoblock_12
				reg [31:0] i;
				for (i = 0; i < N_CTRL_P; i = i + 1)
					if (rx_cmd_hit_w[i]) begin
						mon_draw_pend_r[i] <= 1'b1;
						ca_pend_r[i] <= 1'b0;
						ca_probe_r[i] <= 1'b0;
					end
			end
			if (((((exp_mon_w && valid_r[exp_ix_w]) && !ca_probe_r[exp_ix_w]) && !mon_draw_pend_r[exp_ix_w]) && !rx_cmd_hit_w[exp_ix_w]) && !(mon_draw_wait_r && (mon_draw_ix_r == exp_ix_w)))
				ca_pend_r[exp_ix_w] <= 1'b1;
			if (ca_valid_o && ca_ready_i) begin
				ca_pend_r[ca_pick_ix_w] <= 1'b0;
				ca_probe_r[ca_pick_ix_w] <= 1'b1;
			end
			if (((ca_rsp_valid_i && (sv2v_cast_32(ca_rsp_owner_i) < N_CTRL_P)) && !rx_cmd_hit_w[ca_rsp_owner_i]) && valid_r[ca_rsp_owner_i]) begin
				ca_probe_r[ca_rsp_owner_i] <= 1'b0;
				mon_draw_pend_r[ca_rsp_owner_i] <= 1'b1;
			end
			if (((ca_fail_valid_i && (sv2v_cast_32(ca_fail_owner_i) < N_CTRL_P)) && !rx_cmd_hit_w[ca_fail_owner_i]) && valid_r[ca_fail_owner_i]) begin
				ca_probe_r[ca_fail_owner_i] <= 1'b0;
				pend_r[ca_fail_owner_i] <= 1'b1;
			end
			if ((!mon_draw_wait_r && mon_pick_ok_w) && !prng_draw_busy_i) begin
				prng_draw_req_o <= 1'b1;
				mon_draw_wait_r <= 1'b1;
				mon_draw_ix_r <= mon_pick_ix_w;
				mon_draw_pend_r[mon_pick_ix_w] <= 1'b0;
			end
			if (mon_draw_wait_r && prng_draw_valid_i) begin
				mon_draw_wait_r <= 1'b0;
				mon_arm_valid_o <= 1'b1;
				mon_arm_cancel_o <= 1'b0;
				mon_arm_slot_o <= sv2v_cast_5A563((TMR_REGMON_BASE_P + N_CTRL_P) + sv2v_cast_32(mon_draw_ix_r));
				mon_arm_owner_o <= pp_pkg_PP_OWN_CMON_C | {{pp_pkg_PP_TIMER_OWNER_W_C - CIX_W_C {1'b0}}, mon_draw_ix_r};
				mon_arm_deadline_ms_o <= now_ms_i + sv2v_cast_32(prng_draw_ms_i);
			end
			if ((exp_row_w && valid_r[exp_ix_w]) && tl_r[exp_ix_w])
				pend_r[exp_ix_w] <= 1'b1;
			if (exp_lock_w && lk_held_r) begin
				lk_held_r <= 1'b0;
				lk_ctlr_r <= 64'd0;
				if (pe_lock_r) begin
					lockx_v_r <= 1'b0;
					if (coalesce_r != 8'hff)
						coalesce_r <= coalesce_r + 8'd1;
				end
				else begin
					pe_lock_r <= 1'b1;
					lockx_v_r <= 1'b0;
				end
			end
			if (id_arm_gnt_w) begin
				tmr_arm_valid_o <= 1'b1;
				tmr_arm_cancel_o <= 1'b0;
				tmr_arm_slot_o <= id_arm_slot_w;
				tmr_arm_owner_o <= id_arm_owner_w;
				tmr_arm_deadline_ms_o <= id_arm_deadline_w;
			end
			(* full_case, parallel_case *)
			case (n_st_r)
				4'd0: begin
					wk_ix_r <= 1'sb0;
					wk_match_r <= 1'b0;
					wk_free_r <= 1'b0;
					if (rgy_new_w) begin
						req_done_r <= 1'b1;
						result_q_r <= rgy_state_i;
						if (rgy_state_i)
							n_st_r <= 4'd3;
						else if (rgy_op_i[1]) begin
							if (lk_denied_w)
								result_r <= 2'd1;
							else if (!rgy_op_i[0]) begin
								result_r <= {!lk_held_r, 1'b0};
								lk_held_r <= 1'b1;
								lk_ctlr_r <= rgy_eid_i;
								tmr_arm_valid_o <= 1'b1;
								tmr_arm_cancel_o <= 1'b0;
								tmr_arm_slot_o <= sv2v_cast_5A563(TMR_LOCK_SLOT_P);
								tmr_arm_owner_o <= pp_pkg_PP_OWN_LOCK_C;
								tmr_arm_deadline_ms_o <= deadline_w;
								if (!lk_held_r) begin
									pe_lock_r <= 1'b1;
									lockx_eid_r <= rgy_eid_i;
									lockx_v_r <= 1'b1;
								end
							end
							else begin
								result_r <= {lk_held_r, 1'b0};
								if (lk_held_r) begin
									lk_held_r <= 1'b0;
									lk_ctlr_r <= 64'd0;
									tmr_arm_valid_o <= 1'b1;
									tmr_arm_cancel_o <= 1'b1;
									tmr_arm_slot_o <= sv2v_cast_5A563(TMR_LOCK_SLOT_P);
									tmr_arm_owner_o <= pp_pkg_PP_OWN_LOCK_C;
									tmr_arm_deadline_ms_o <= 32'd0;
									pe_lock_r <= 1'b1;
									lockx_eid_r <= rgy_eid_i;
									lockx_v_r <= 1'b1;
								end
							end
							n_st_r <= 4'd3;
						end
						else begin
							hold_eid_r <= rgy_eid_i;
							hold_mac_r <= rgy_mac_i;
							op_tl_r <= rgy_tl_i;
							op_dereg_r <= rgy_op_i[0];
							n_st_r <= 4'd1;
						end
					end
					else if (pd_any_w && !dh_v_r)
						n_st_r <= 4'd4;
					else if ((dh_v_r || em_active_r) || pick_any_w) begin
						if (dh_v_r && !em_active_r) begin
							em_kind_r <= pp_pkg_PP_UNS_DEREG_C;
							em_dt_r <= 16'd0;
							em_di_r <= 16'd0;
							em_arg0_r <= 16'd0;
							em_arg1_r <= 16'd0;
							em_dh_r <= 1'b1;
							em_cmd_r <= 1'b0;
							hold_eid_r <= dh_eid_r;
							hold_mac_r <= dh_mac_r;
							hold_seq_r <= dh_seq_r;
							n_st_r <= 4'd6;
						end
						else begin
							if (!em_active_r) begin
								em_active_r <= 1'b1;
								em_kind_r <= pick_kind_w;
								em_dt_r <= pick_dt_w;
								em_di_r <= pick_di_w;
								em_arg0_r <= pick_arg0_w;
								em_arg1_r <= pick_arg1_w;
								em_cmd_r <= pick_cmd_w;
								em_ix_r <= 1'sb0;
								if (pick_kind_w == pp_pkg_PP_UNS_LOCK_C) begin
									em_excl_r <= lockx_eid_r;
									em_excl_v_r <= lockx_v_r;
									pe_lock_r <= 1'b0;
								end
								else if (pick_kind_w == pp_pkg_PP_UNS_AMAP_C) begin
									em_excl_r <= amap_excl_r;
									em_excl_v_r <= 1'b1;
									em_amap_remove_r <= amap_remove_r;
									em_amap_count_r <= amap_count_r;
									pe_amap_r <= 1'b0;
								end
								else if (pick_cmd_w) begin
									em_excl_r <= cmdq_excl_r[cmdq_rd_r];
									em_excl_v_r <= 1'b1;
									cmdq_rd_r <= cmdq_rd_r + 4'd1;
									if (cmd_push_w)
										cmdq_count_r <= cmdq_count_r;
									else
										cmdq_count_r <= cmdq_count_r - 5'd1;
								end
								else if (pick_kind_w == pp_pkg_PP_UNS_CTRS_C) begin
									em_excl_v_r <= 1'b0;
									em_ctr_ix_r <= pick_ctr_ix_w;
									ctr_pend_r[pick_ctr_ix_w] <= 1'b0;
									ctr_sent_r[pick_ctr_ix_w] <= 1'b1;
									ctr_last_r[pick_ctr_ix_w] <= now_ms_i;
								end
								else begin
									em_excl_v_r <= 1'b0;
									if (pick_kind_w == pp_pkg_PP_UNS_AVB_C)
										pe_avb_r <= 1'b0;
									else if (pick_kind_w == pp_pkg_PP_UNS_ASP_C)
										pe_asp_r <= 1'b0;
									else if (pick_dt_w == 16'h0005)
										pe_sin_r[pick_di_w[SIX_W_C - 1:0]] <= 1'b0;
									else
										pe_sout_r[pick_di_w[SOX_W_C - 1:0]] <= 1'b0;
								end
								wk_ix_r <= 1'sb0;
							end
							else
								wk_ix_r <= em_ix_r;
							em_dh_r <= 1'b0;
							n_st_r <= 4'd5;
						end
					end
				end
				4'd1: begin
					if (wk_hit_w && !wk_match_r) begin
						wk_match_r <= 1'b1;
						wk_match_ix_r <= wk_ix_r;
						wk_match_seq_r <= row_seq_w;
					end
					if (!valid_r[wk_ix_r] && !wk_free_r) begin
						wk_free_r <= 1'b1;
						wk_free_ix_r <= wk_ix_r;
					end
					if (wk_ix_r == sv2v_cast_17814(N_CTRL_P - 1))
						n_st_r <= 4'd2;
					else
						wk_ix_r <= wk_ix_r + sv2v_cast_17814_signed(1);
				end
				4'd2: begin
					if (op_dereg_r) begin
						result_r <= 2'd0;
						if (wk_match_r) begin
							valid_r[wk_match_ix_r] <= 1'b0;
							tl_r[wk_match_ix_r] <= 1'b0;
							pend_r[wk_match_ix_r] <= 1'b0;
							tmr_arm_valid_o <= 1'b1;
							tmr_arm_cancel_o <= 1'b1;
							tmr_arm_slot_o <= sv2v_cast_5A563(TMR_REGMON_BASE_P + sv2v_cast_32(wk_match_ix_r));
							tmr_arm_owner_o <= pp_pkg_PP_OWN_NTFY_C | {{pp_pkg_PP_TIMER_OWNER_W_C - CIX_W_C {1'b0}}, wk_match_ix_r};
							tmr_arm_deadline_ms_o <= 32'd0;
							mon_draw_pend_r[wk_match_ix_r] <= 1'b0;
							ca_pend_r[wk_match_ix_r] <= 1'b0;
							ca_probe_r[wk_match_ix_r] <= 1'b0;
							if (mon_draw_wait_r && (mon_draw_ix_r == wk_match_ix_r))
								mon_draw_wait_r <= 1'b0;
							mon_arm_valid_o <= 1'b1;
							mon_arm_cancel_o <= 1'b1;
							mon_arm_slot_o <= sv2v_cast_5A563((TMR_REGMON_BASE_P + N_CTRL_P) + sv2v_cast_32(wk_match_ix_r));
							mon_arm_owner_o <= pp_pkg_PP_OWN_CMON_C | {{pp_pkg_PP_TIMER_OWNER_W_C - CIX_W_C {1'b0}}, wk_match_ix_r};
							mon_arm_deadline_ms_o <= 32'd0;
						end
					end
					else if (wk_match_r || wk_free_r) begin
						result_r <= 2'd0;
						wr_en_r <= 1'b1;
						ix_clr_r <= 1'b1;
						wr_ix_r <= (wk_match_r ? wk_match_ix_r : wk_free_ix_r);
						wr_row_r <= {hold_eid_r, hold_mac_r, (wk_match_r ? wk_match_seq_r : 16'd0)};
						valid_r[(wk_match_r ? wk_match_ix_r : wk_free_ix_r)] <= 1'b1;
						tl_r[(wk_match_r ? wk_match_ix_r : wk_free_ix_r)] <= op_tl_r;
						pend_r[(wk_match_r ? wk_match_ix_r : wk_free_ix_r)] <= 1'b0;
						mon_draw_pend_r[(wk_match_r ? wk_match_ix_r : wk_free_ix_r)] <= 1'b1;
						ca_pend_r[(wk_match_r ? wk_match_ix_r : wk_free_ix_r)] <= 1'b0;
						ca_probe_r[(wk_match_r ? wk_match_ix_r : wk_free_ix_r)] <= 1'b0;
						tmr_arm_valid_o <= 1'b1;
						tmr_arm_cancel_o <= !op_tl_r;
						tmr_arm_slot_o <= sv2v_cast_5A563(TMR_REGMON_BASE_P + sv2v_cast_32((wk_match_r ? wk_match_ix_r : wk_free_ix_r)));
						tmr_arm_owner_o <= pp_pkg_PP_OWN_NTFY_C | {{pp_pkg_PP_TIMER_OWNER_W_C - CIX_W_C {1'b0}}, (wk_match_r ? wk_match_ix_r : wk_free_ix_r)};
						tmr_arm_deadline_ms_o <= deadline_w;
					end
					else
						result_r <= 2'd1;
					n_st_r <= 4'd3;
				end
				4'd3:
					if (!rgy_req_i)
						n_st_r <= 4'd0;
				4'd4: begin
					dh_v_r <= 1'b1;
					dh_eid_r <= row_eid_w;
					dh_mac_r <= row_mac_w;
					dh_seq_r <= row_seq_w;
					valid_r[pd_ix_w] <= 1'b0;
					tl_r[pd_ix_w] <= 1'b0;
					pend_r[pd_ix_w] <= 1'b0;
					mon_draw_pend_r[pd_ix_w] <= 1'b0;
					ca_pend_r[pd_ix_w] <= 1'b0;
					ca_probe_r[pd_ix_w] <= 1'b0;
					if (mon_draw_wait_r && (mon_draw_ix_r == pd_ix_w))
						mon_draw_wait_r <= 1'b0;
					mon_arm_valid_o <= 1'b1;
					mon_arm_cancel_o <= 1'b1;
					mon_arm_slot_o <= sv2v_cast_5A563((TMR_REGMON_BASE_P + N_CTRL_P) + sv2v_cast_32(pd_ix_w));
					mon_arm_owner_o <= pp_pkg_PP_OWN_CMON_C | {{pp_pkg_PP_TIMER_OWNER_W_C - CIX_W_C {1'b0}}, pd_ix_w};
					mon_arm_deadline_ms_o <= 32'd0;
					n_st_r <= 4'd0;
				end
				4'd5:
					if ((em_ix_r >= sv2v_cast_17814(N_CTRL_P - 1)) && em_skip_w) begin
						em_active_r <= 1'b0;
						n_st_r <= 4'd0;
					end
					else if (em_skip_w) begin
						em_ix_r <= em_ix_r + sv2v_cast_17814_signed(1);
						wk_ix_r <= em_ix_r + sv2v_cast_17814_signed(1);
					end
					else begin
						hold_eid_r <= row_eid_w;
						hold_mac_r <= row_mac_w;
						hold_seq_r <= row_seq_w;
						n_st_r <= 4'd6;
					end
				4'd6: begin
					if (em_kind_r == pp_pkg_PP_UNS_CTRS_C)
						ctr_last_r[em_ctr_ix_r] <= now_ms_i;
					if (core_done_w)
						n_st_r <= 4'd7;
					else if (rgy_new_w)
						n_st_r <= 4'd0;
				end
				4'd7: begin
					if (uns_cnt_r != 16'hffff)
						uns_cnt_r <= uns_cnt_r + 16'd1;
					if (em_dh_r)
						dh_v_r <= 1'b0;
					else begin
						wr_en_r <= 1'b1;
						wr_ix_r <= em_ix_r;
						wr_row_r <= {hold_eid_r, hold_mac_r, hold_seq_r + 16'd1};
						if (em_ix_r == sv2v_cast_17814(N_CTRL_P - 1))
							em_active_r <= 1'b0;
						else
							em_ix_r <= em_ix_r + sv2v_cast_17814_signed(1);
					end
					n_st_r <= 4'd0;
				end
				default: n_st_r <= 4'd0;
			endcase
		end
	end
	initial _sv2v_0 = 0;
endmodule
`default_nettype wire

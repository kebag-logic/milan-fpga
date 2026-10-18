`default_nettype none
`default_nettype wire
`default_nettype none
`default_nettype wire
`default_nettype none
`default_nettype wire
`default_nettype none
`default_nettype wire
`default_nettype none
`default_nettype wire
`default_nettype none
module KL_pp_event_router (
	clk_i,
	rst_n,
	src_strobe_i,
	src_payload_i,
	evt_valid_o,
	evt_src_o,
	evt_payload_o,
	evt_lost_o,
	evt_ack_i,
	lost_src_i,
	lost_count_o
);
	reg _sv2v_0;
	parameter [31:0] N_SRC_P = 16;
	parameter [31:0] PAYLOAD_W_P = 16;
	localparam [31:0] SRC_W_C = (N_SRC_P > 32'd1 ? $clog2(N_SRC_P) : 32'd1);
	input wire clk_i;
	input wire rst_n;
	input wire [N_SRC_P - 1:0] src_strobe_i;
	input wire [(N_SRC_P * PAYLOAD_W_P) - 1:0] src_payload_i;
	output wire evt_valid_o;
	output wire [SRC_W_C - 1:0] evt_src_o;
	output wire [PAYLOAD_W_P - 1:0] evt_payload_o;
	output wire evt_lost_o;
	input wire evt_ack_i;
	input wire [SRC_W_C - 1:0] lost_src_i;
	output wire [7:0] lost_count_o;
	localparam [7:0] LOST_MAX_C = 8'hff;
	reg [N_SRC_P - 1:0] pending_r;
	reg [N_SRC_P - 1:0] coalesced_r;
	reg [PAYLOAD_W_P - 1:0] payload_r [0:N_SRC_P - 1];
	reg [7:0] lost_cnt_r [0:N_SRC_P - 1];
	reg valid_r;
	reg [SRC_W_C - 1:0] sel_r;
	reg [SRC_W_C - 1:0] ptr_r;
	wire deliver_w;
	assign deliver_w = valid_r && evt_ack_i;
	reg [N_SRC_P - 1:0] delivered_w;
	always @(*) begin : delivered_vec
		if (_sv2v_0)
			;
		delivered_w = 1'sb0;
		if (deliver_w)
			delivered_w[sel_r] = 1'b1;
	end
	function automatic [SRC_W_C - 1:0] sv2v_cast_14954;
		input reg [SRC_W_C - 1:0] inp;
		sv2v_cast_14954 = inp;
	endfunction
	function automatic signed [SRC_W_C - 1:0] sv2v_cast_14954_signed;
		input reg signed [SRC_W_C - 1:0] inp;
		sv2v_cast_14954_signed = inp;
	endfunction
	function automatic [SRC_W_C - 1:0] rr_next;
		input reg [SRC_W_C - 1:0] s;
		rr_next = (s == sv2v_cast_14954(N_SRC_P - 32'd1) ? {SRC_W_C {1'sb0}} : s + sv2v_cast_14954_signed(1));
	endfunction
	reg [N_SRC_P - 1:0] pend_after_w;
	always @(*) begin : pend_after
		if (_sv2v_0)
			;
		pend_after_w = pending_r;
		if (deliver_w)
			pend_after_w[sel_r] = 1'b0;
	end
	wire [SRC_W_C - 1:0] base_w;
	assign base_w = (deliver_w ? rr_next(sel_r) : ptr_r);
	reg gnt_found_w;
	reg [SRC_W_C - 1:0] gnt_src_w;
	function automatic [31:0] sv2v_cast_32;
		input reg [31:0] inp;
		sv2v_cast_32 = inp;
	endfunction
	always @(*) begin : rr_scan
		if (_sv2v_0)
			;
		gnt_found_w = 1'b0;
		gnt_src_w = 1'sb0;
		begin : sv2v_autoblock_1
			reg [31:0] k;
			for (k = 0; k < N_SRC_P; k = k + 1)
				begin : sv2v_autoblock_2
					reg [31:0] idx;
					idx = sv2v_cast_32(base_w) + k;
					if (idx >= N_SRC_P)
						idx = idx - N_SRC_P;
					if (!gnt_found_w && pend_after_w[idx[SRC_W_C - 1:0]]) begin
						gnt_found_w = 1'b1;
						gnt_src_w = idx[SRC_W_C - 1:0];
					end
				end
		end
	end
	always @(posedge clk_i) begin : evt_state
		if (!rst_n) begin
			pending_r <= 1'sb0;
			coalesced_r <= 1'sb0;
			valid_r <= 1'b0;
			sel_r <= 1'sb0;
			ptr_r <= 1'sb0;
			begin : sv2v_autoblock_3
				reg [31:0] s;
				for (s = 0; s < N_SRC_P; s = s + 1)
					begin
						payload_r[s] <= 1'sb0;
						lost_cnt_r[s] <= 8'd0;
					end
			end
		end
		else begin
			begin : sv2v_autoblock_4
				reg [31:0] s;
				for (s = 0; s < N_SRC_P; s = s + 1)
					if (src_strobe_i[s]) begin
						if (!pending_r[s] || delivered_w[s]) begin
							pending_r[s] <= 1'b1;
							payload_r[s] <= src_payload_i[s * PAYLOAD_W_P+:PAYLOAD_W_P];
							coalesced_r[s] <= 1'b0;
						end
						else begin
							coalesced_r[s] <= 1'b1;
							if (lost_cnt_r[s] != LOST_MAX_C)
								lost_cnt_r[s] <= lost_cnt_r[s] + 8'd1;
						end
					end
					else if (delivered_w[s]) begin
						pending_r[s] <= 1'b0;
						coalesced_r[s] <= 1'b0;
					end
			end
			if (deliver_w || !valid_r) begin
				valid_r <= gnt_found_w;
				if (gnt_found_w)
					sel_r <= gnt_src_w;
			end
			if (deliver_w)
				ptr_r <= rr_next(sel_r);
		end
	end
	assign evt_valid_o = valid_r;
	assign evt_src_o = sel_r;
	assign evt_payload_o = payload_r[sel_r];
	assign evt_lost_o = valid_r && coalesced_r[sel_r];
	assign lost_count_o = lost_cnt_r[lost_src_i];
	initial _sv2v_0 = 0;
endmodule
`default_nettype wire

`resetall
`default_nettype none
module axis_fifo (
	clk,
	rst,
	s_axis_tdata,
	s_axis_tkeep,
	s_axis_tvalid,
	s_axis_tready,
	s_axis_tlast,
	s_axis_tid,
	s_axis_tdest,
	s_axis_tuser,
	m_axis_tdata,
	m_axis_tkeep,
	m_axis_tvalid,
	m_axis_tready,
	m_axis_tlast,
	m_axis_tid,
	m_axis_tdest,
	m_axis_tuser,
	pause_req,
	pause_ack,
	status_depth,
	status_depth_commit,
	status_overflow,
	status_bad_frame,
	status_good_frame
);
	parameter DEPTH = 4096;
	parameter DATA_WIDTH = 8;
	parameter KEEP_ENABLE = DATA_WIDTH > 8;
	parameter KEEP_WIDTH = (DATA_WIDTH + 7) / 8;
	parameter LAST_ENABLE = 1;
	parameter ID_ENABLE = 0;
	parameter ID_WIDTH = 8;
	parameter DEST_ENABLE = 0;
	parameter DEST_WIDTH = 8;
	parameter USER_ENABLE = 1;
	parameter USER_WIDTH = 1;
	parameter RAM_PIPELINE = 1;
	parameter OUTPUT_FIFO_ENABLE = 0;
	parameter FRAME_FIFO = 0;
	parameter USER_BAD_FRAME_VALUE = 1'b1;
	parameter USER_BAD_FRAME_MASK = 1'b1;
	parameter DROP_OVERSIZE_FRAME = FRAME_FIFO;
	parameter DROP_BAD_FRAME = 0;
	parameter DROP_WHEN_FULL = 0;
	parameter MARK_WHEN_FULL = 0;
	parameter PAUSE_ENABLE = 0;
	parameter FRAME_PAUSE = FRAME_FIFO;
	input wire clk;
	input wire rst;
	input wire [DATA_WIDTH - 1:0] s_axis_tdata;
	input wire [KEEP_WIDTH - 1:0] s_axis_tkeep;
	input wire s_axis_tvalid;
	output wire s_axis_tready;
	input wire s_axis_tlast;
	input wire [ID_WIDTH - 1:0] s_axis_tid;
	input wire [DEST_WIDTH - 1:0] s_axis_tdest;
	input wire [USER_WIDTH - 1:0] s_axis_tuser;
	output wire [DATA_WIDTH - 1:0] m_axis_tdata;
	output wire [KEEP_WIDTH - 1:0] m_axis_tkeep;
	output wire m_axis_tvalid;
	input wire m_axis_tready;
	output wire m_axis_tlast;
	output wire [ID_WIDTH - 1:0] m_axis_tid;
	output wire [DEST_WIDTH - 1:0] m_axis_tdest;
	output wire [USER_WIDTH - 1:0] m_axis_tuser;
	input wire pause_req;
	output wire pause_ack;
	output wire [$clog2(DEPTH):0] status_depth;
	output wire [$clog2(DEPTH):0] status_depth_commit;
	output wire status_overflow;
	output wire status_bad_frame;
	output wire status_good_frame;
	parameter ADDR_WIDTH = (KEEP_ENABLE && (KEEP_WIDTH > 1) ? $clog2(DEPTH / KEEP_WIDTH) : $clog2(DEPTH));
	parameter CL_KEEP_WDITH = $clog2(KEEP_WIDTH);
	parameter OUTPUT_FIFO_ADDR_WIDTH = (RAM_PIPELINE < 2 ? 3 : $clog2((RAM_PIPELINE * 2) + 7));
	initial begin
		if (FRAME_FIFO && !LAST_ENABLE) begin
			$display("Error [%0t] $VALIDATION_STORAGE/reviews/r247-520-r1/third_party/verilog-axis/rtl/axis_fifo.v:145:9 - axis_fifo.<unnamed_block>.<unnamed_block>\n msg: ", $time, "Error: FRAME_FIFO set requires LAST_ENABLE set (instance %m)");
			$finish;
		end
		if (DROP_OVERSIZE_FRAME && !FRAME_FIFO) begin
			$display("Error [%0t] $VALIDATION_STORAGE/reviews/r247-520-r1/third_party/verilog-axis/rtl/axis_fifo.v:150:9 - axis_fifo.<unnamed_block>.<unnamed_block>\n msg: ", $time, "Error: DROP_OVERSIZE_FRAME set requires FRAME_FIFO set (instance %m)");
			$finish;
		end
		if (DROP_BAD_FRAME && !(FRAME_FIFO && DROP_OVERSIZE_FRAME)) begin
			$display("Error [%0t] $VALIDATION_STORAGE/reviews/r247-520-r1/third_party/verilog-axis/rtl/axis_fifo.v:155:9 - axis_fifo.<unnamed_block>.<unnamed_block>\n msg: ", $time, "Error: DROP_BAD_FRAME set requires FRAME_FIFO and DROP_OVERSIZE_FRAME set (instance %m)");
			$finish;
		end
		if (DROP_WHEN_FULL && !(FRAME_FIFO && DROP_OVERSIZE_FRAME)) begin
			$display("Error [%0t] $VALIDATION_STORAGE/reviews/r247-520-r1/third_party/verilog-axis/rtl/axis_fifo.v:160:9 - axis_fifo.<unnamed_block>.<unnamed_block>\n msg: ", $time, "Error: DROP_WHEN_FULL set requires FRAME_FIFO and DROP_OVERSIZE_FRAME set (instance %m)");
			$finish;
		end
		if ((DROP_BAD_FRAME || MARK_WHEN_FULL) && ((USER_BAD_FRAME_MASK & {USER_WIDTH {1'b1}}) == 0)) begin
			$display("Error [%0t] $VALIDATION_STORAGE/reviews/r247-520-r1/third_party/verilog-axis/rtl/axis_fifo.v:165:9 - axis_fifo.<unnamed_block>.<unnamed_block>\n msg: ", $time, "Error: Invalid USER_BAD_FRAME_MASK value (instance %m)");
			$finish;
		end
		if (MARK_WHEN_FULL && FRAME_FIFO) begin
			$display("Error [%0t] $VALIDATION_STORAGE/reviews/r247-520-r1/third_party/verilog-axis/rtl/axis_fifo.v:170:9 - axis_fifo.<unnamed_block>.<unnamed_block>\n msg: ", $time, "Error: MARK_WHEN_FULL is not compatible with FRAME_FIFO (instance %m)");
			$finish;
		end
		if (MARK_WHEN_FULL && !LAST_ENABLE) begin
			$display("Error [%0t] $VALIDATION_STORAGE/reviews/r247-520-r1/third_party/verilog-axis/rtl/axis_fifo.v:175:9 - axis_fifo.<unnamed_block>.<unnamed_block>\n msg: ", $time, "Error: MARK_WHEN_FULL set requires LAST_ENABLE set (instance %m)");
			$finish;
		end
	end
	localparam KEEP_OFFSET = DATA_WIDTH;
	localparam LAST_OFFSET = KEEP_OFFSET + (KEEP_ENABLE ? KEEP_WIDTH : 0);
	localparam ID_OFFSET = LAST_OFFSET + (LAST_ENABLE ? 1 : 0);
	localparam DEST_OFFSET = ID_OFFSET + (ID_ENABLE ? ID_WIDTH : 0);
	localparam USER_OFFSET = DEST_OFFSET + (DEST_ENABLE ? DEST_WIDTH : 0);
	localparam WIDTH = USER_OFFSET + (USER_ENABLE ? USER_WIDTH : 0);
	reg [ADDR_WIDTH:0] wr_ptr_reg = {ADDR_WIDTH + 1 {1'b0}};
	reg [ADDR_WIDTH:0] wr_ptr_commit_reg = {ADDR_WIDTH + 1 {1'b0}};
	reg [ADDR_WIDTH:0] rd_ptr_reg = {ADDR_WIDTH + 1 {1'b0}};
	(* ramstyle = "no_rw_check" *) reg [WIDTH - 1:0] mem [(2 ** ADDR_WIDTH) - 1:0];
	reg mem_read_data_valid_reg = 1'b0;
	(* shreg_extract = "no" *) reg [WIDTH - 1:0] m_axis_pipe_reg [RAM_PIPELINE + 0:0];
	reg [RAM_PIPELINE + 0:0] m_axis_tvalid_pipe_reg = 0;
	wire full = wr_ptr_reg == (rd_ptr_reg ^ {1'b1, {ADDR_WIDTH {1'b0}}});
	wire empty = wr_ptr_commit_reg == rd_ptr_reg;
	wire full_wr = wr_ptr_reg == (wr_ptr_commit_reg ^ {1'b1, {ADDR_WIDTH {1'b0}}});
	reg s_frame_reg = 1'b0;
	reg drop_frame_reg = 1'b0;
	reg mark_frame_reg = 1'b0;
	reg send_frame_reg = 1'b0;
	reg [ADDR_WIDTH:0] depth_reg = 0;
	reg [ADDR_WIDTH:0] depth_commit_reg = 0;
	reg overflow_reg = 1'b0;
	reg bad_frame_reg = 1'b0;
	reg good_frame_reg = 1'b0;
	assign s_axis_tready = (FRAME_FIFO ? (!full || (full_wr && DROP_OVERSIZE_FRAME)) || DROP_WHEN_FULL : !full || MARK_WHEN_FULL);
	wire [WIDTH - 1:0] s_axis;
	assign s_axis[DATA_WIDTH - 1:0] = s_axis_tdata;
	generate
		if (KEEP_ENABLE) begin : genblk1
			assign s_axis[KEEP_OFFSET+:KEEP_WIDTH] = s_axis_tkeep;
		end
		if (LAST_ENABLE) begin : genblk2
			assign s_axis[LAST_OFFSET] = s_axis_tlast | mark_frame_reg;
		end
		if (ID_ENABLE) begin : genblk3
			assign s_axis[ID_OFFSET+:ID_WIDTH] = s_axis_tid;
		end
		if (DEST_ENABLE) begin : genblk4
			assign s_axis[DEST_OFFSET+:DEST_WIDTH] = s_axis_tdest;
		end
		if (USER_ENABLE) begin : genblk5
			assign s_axis[USER_OFFSET+:USER_WIDTH] = (mark_frame_reg ? USER_BAD_FRAME_VALUE : s_axis_tuser);
		end
	endgenerate
	wire [WIDTH - 1:0] m_axis = m_axis_pipe_reg[RAM_PIPELINE + 0];
	wire m_axis_tready_pipe;
	wire m_axis_tvalid_pipe = m_axis_tvalid_pipe_reg[RAM_PIPELINE + 0];
	wire [DATA_WIDTH - 1:0] m_axis_tdata_pipe = m_axis[DATA_WIDTH - 1:0];
	wire [KEEP_WIDTH - 1:0] m_axis_tkeep_pipe = (KEEP_ENABLE ? m_axis[KEEP_OFFSET+:KEEP_WIDTH] : {KEEP_WIDTH {1'b1}});
	wire m_axis_tlast_pipe = (LAST_ENABLE ? m_axis[LAST_OFFSET] : 1'b1);
	wire [ID_WIDTH - 1:0] m_axis_tid_pipe = (ID_ENABLE ? m_axis[ID_OFFSET+:ID_WIDTH] : {ID_WIDTH {1'b0}});
	wire [DEST_WIDTH - 1:0] m_axis_tdest_pipe = (DEST_ENABLE ? m_axis[DEST_OFFSET+:DEST_WIDTH] : {DEST_WIDTH {1'b0}});
	wire [USER_WIDTH - 1:0] m_axis_tuser_pipe = (USER_ENABLE ? m_axis[USER_OFFSET+:USER_WIDTH] : {USER_WIDTH {1'b0}});
	wire m_axis_tready_out;
	wire m_axis_tvalid_out;
	wire [DATA_WIDTH - 1:0] m_axis_tdata_out;
	wire [KEEP_WIDTH - 1:0] m_axis_tkeep_out;
	wire m_axis_tlast_out;
	wire [ID_WIDTH - 1:0] m_axis_tid_out;
	wire [DEST_WIDTH - 1:0] m_axis_tdest_out;
	wire [USER_WIDTH - 1:0] m_axis_tuser_out;
	wire pipe_ready;
	assign status_depth = (KEEP_ENABLE && (KEEP_WIDTH > 1) ? {depth_reg, {CL_KEEP_WDITH {1'b0}}} : depth_reg);
	assign status_depth_commit = (KEEP_ENABLE && (KEEP_WIDTH > 1) ? {depth_commit_reg, {CL_KEEP_WDITH {1'b0}}} : depth_commit_reg);
	assign status_overflow = overflow_reg;
	assign status_bad_frame = bad_frame_reg;
	assign status_good_frame = good_frame_reg;
	always @(posedge clk) begin
		overflow_reg <= 1'b0;
		bad_frame_reg <= 1'b0;
		good_frame_reg <= 1'b0;
		if ((s_axis_tready && s_axis_tvalid) && LAST_ENABLE)
			s_frame_reg <= !s_axis_tlast;
		if (FRAME_FIFO) begin
			if (s_axis_tready && s_axis_tvalid) begin
				if (((full && DROP_WHEN_FULL) || (full_wr && DROP_OVERSIZE_FRAME)) || drop_frame_reg) begin
					drop_frame_reg <= 1'b1;
					if (s_axis_tlast) begin
						wr_ptr_reg <= wr_ptr_commit_reg;
						drop_frame_reg <= 1'b0;
						overflow_reg <= 1'b1;
					end
				end
				else begin
					mem[wr_ptr_reg[ADDR_WIDTH - 1:0]] <= s_axis;
					wr_ptr_reg <= wr_ptr_reg + 1;
					if (s_axis_tlast || (!DROP_OVERSIZE_FRAME && (full_wr || send_frame_reg))) begin
						send_frame_reg <= !s_axis_tlast;
						if ((s_axis_tlast && DROP_BAD_FRAME) && (USER_BAD_FRAME_MASK & ~(s_axis_tuser ^ USER_BAD_FRAME_VALUE))) begin
							wr_ptr_reg <= wr_ptr_commit_reg;
							bad_frame_reg <= 1'b1;
						end
						else begin
							wr_ptr_commit_reg <= wr_ptr_reg + 1;
							good_frame_reg <= s_axis_tlast;
						end
					end
				end
			end
			else if ((s_axis_tvalid && full_wr) && !DROP_OVERSIZE_FRAME) begin
				send_frame_reg <= 1'b1;
				wr_ptr_commit_reg <= wr_ptr_reg;
			end
		end
		else if (s_axis_tready && s_axis_tvalid) begin
			if (drop_frame_reg && MARK_WHEN_FULL) begin
				if (s_axis_tlast) begin
					if (!full && mark_frame_reg) begin
						mark_frame_reg <= 1'b0;
						mem[wr_ptr_reg[ADDR_WIDTH - 1:0]] <= s_axis;
						wr_ptr_reg <= wr_ptr_reg + 1;
						wr_ptr_commit_reg <= wr_ptr_reg + 1;
					end
					drop_frame_reg <= 1'b0;
					overflow_reg <= 1'b1;
				end
			end
			else if ((full || mark_frame_reg) && MARK_WHEN_FULL) begin
				drop_frame_reg <= 1'b1;
				mark_frame_reg <= mark_frame_reg || s_frame_reg;
				if (s_axis_tlast) begin
					drop_frame_reg <= 1'b0;
					overflow_reg <= 1'b1;
				end
			end
			else begin
				mem[wr_ptr_reg[ADDR_WIDTH - 1:0]] <= s_axis;
				wr_ptr_reg <= wr_ptr_reg + 1;
				wr_ptr_commit_reg <= wr_ptr_reg + 1;
			end
		end
		else if (((!full && !drop_frame_reg) && mark_frame_reg) && MARK_WHEN_FULL) begin
			mark_frame_reg <= 1'b0;
			mem[wr_ptr_reg[ADDR_WIDTH - 1:0]] <= s_axis;
			wr_ptr_reg <= wr_ptr_reg + 1;
			wr_ptr_commit_reg <= wr_ptr_reg + 1;
		end
		if (rst) begin
			wr_ptr_reg <= {ADDR_WIDTH + 1 {1'b0}};
			wr_ptr_commit_reg <= {ADDR_WIDTH + 1 {1'b0}};
			s_frame_reg <= 1'b0;
			drop_frame_reg <= 1'b0;
			mark_frame_reg <= 1'b0;
			send_frame_reg <= 1'b0;
			overflow_reg <= 1'b0;
			bad_frame_reg <= 1'b0;
			good_frame_reg <= 1'b0;
		end
	end
	always @(posedge clk) begin
		depth_reg <= wr_ptr_reg - rd_ptr_reg;
		depth_commit_reg <= wr_ptr_commit_reg - rd_ptr_reg;
	end
	integer j;
	always @(posedge clk) begin
		if (m_axis_tready_pipe)
			m_axis_tvalid_pipe_reg[RAM_PIPELINE + 0] <= 1'b0;
		for (j = RAM_PIPELINE + 0; j > 0; j = j - 1)
			if (m_axis_tready_pipe || (~m_axis_tvalid_pipe_reg >> j)) begin
				m_axis_tvalid_pipe_reg[j] <= m_axis_tvalid_pipe_reg[j - 1];
				m_axis_pipe_reg[j] <= m_axis_pipe_reg[j - 1];
				m_axis_tvalid_pipe_reg[j - 1] <= 1'b0;
			end
		if (m_axis_tready_pipe || ~m_axis_tvalid_pipe_reg) begin
			m_axis_tvalid_pipe_reg[0] <= 1'b0;
			m_axis_pipe_reg[0] <= mem[rd_ptr_reg[ADDR_WIDTH - 1:0]];
			if (!empty && pipe_ready) begin
				m_axis_tvalid_pipe_reg[0] <= 1'b1;
				rd_ptr_reg <= rd_ptr_reg + 1;
			end
		end
		if (rst) begin
			rd_ptr_reg <= {ADDR_WIDTH + 1 {1'b0}};
			m_axis_tvalid_pipe_reg <= 0;
		end
	end
	generate
		if (!OUTPUT_FIFO_ENABLE) begin : genblk6
			assign pipe_ready = 1'b1;
			assign m_axis_tready_pipe = m_axis_tready_out;
			assign m_axis_tvalid_out = m_axis_tvalid_pipe;
			assign m_axis_tdata_out = m_axis_tdata_pipe;
			assign m_axis_tkeep_out = m_axis_tkeep_pipe;
			assign m_axis_tlast_out = m_axis_tlast_pipe;
			assign m_axis_tid_out = m_axis_tid_pipe;
			assign m_axis_tdest_out = m_axis_tdest_pipe;
			assign m_axis_tuser_out = m_axis_tuser_pipe;
		end
		else begin : output_fifo
			reg [DATA_WIDTH - 1:0] m_axis_tdata_reg = {DATA_WIDTH {1'b0}};
			reg [KEEP_WIDTH - 1:0] m_axis_tkeep_reg = {KEEP_WIDTH {1'b0}};
			reg m_axis_tvalid_reg = 1'b0;
			reg m_axis_tlast_reg = 1'b0;
			reg [ID_WIDTH - 1:0] m_axis_tid_reg = {ID_WIDTH {1'b0}};
			reg [DEST_WIDTH - 1:0] m_axis_tdest_reg = {DEST_WIDTH {1'b0}};
			reg [USER_WIDTH - 1:0] m_axis_tuser_reg = {USER_WIDTH {1'b0}};
			reg [OUTPUT_FIFO_ADDR_WIDTH + 0:0] out_fifo_wr_ptr_reg = 0;
			reg [OUTPUT_FIFO_ADDR_WIDTH + 0:0] out_fifo_rd_ptr_reg = 0;
			reg out_fifo_half_full_reg = 1'b0;
			wire out_fifo_full = out_fifo_wr_ptr_reg == (out_fifo_rd_ptr_reg ^ {1'b1, {OUTPUT_FIFO_ADDR_WIDTH {1'b0}}});
			wire out_fifo_empty = out_fifo_wr_ptr_reg == out_fifo_rd_ptr_reg;
			(* ram_style = "distributed", ramstyle = "no_rw_check, mlab" *) reg [DATA_WIDTH - 1:0] out_fifo_tdata [(2 ** OUTPUT_FIFO_ADDR_WIDTH) - 1:0];
			(* ram_style = "distributed", ramstyle = "no_rw_check, mlab" *) reg [KEEP_WIDTH - 1:0] out_fifo_tkeep [(2 ** OUTPUT_FIFO_ADDR_WIDTH) - 1:0];
			(* ram_style = "distributed", ramstyle = "no_rw_check, mlab" *) reg out_fifo_tlast [(2 ** OUTPUT_FIFO_ADDR_WIDTH) - 1:0];
			(* ram_style = "distributed", ramstyle = "no_rw_check, mlab" *) reg [ID_WIDTH - 1:0] out_fifo_tid [(2 ** OUTPUT_FIFO_ADDR_WIDTH) - 1:0];
			(* ram_style = "distributed", ramstyle = "no_rw_check, mlab" *) reg [DEST_WIDTH - 1:0] out_fifo_tdest [(2 ** OUTPUT_FIFO_ADDR_WIDTH) - 1:0];
			(* ram_style = "distributed", ramstyle = "no_rw_check, mlab" *) reg [USER_WIDTH - 1:0] out_fifo_tuser [(2 ** OUTPUT_FIFO_ADDR_WIDTH) - 1:0];
			assign pipe_ready = !out_fifo_half_full_reg;
			assign m_axis_tready_pipe = 1'b1;
			assign m_axis_tdata_out = m_axis_tdata_reg;
			assign m_axis_tkeep_out = (KEEP_ENABLE ? m_axis_tkeep_reg : {KEEP_WIDTH {1'b1}});
			assign m_axis_tvalid_out = m_axis_tvalid_reg;
			assign m_axis_tlast_out = (LAST_ENABLE ? m_axis_tlast_reg : 1'b1);
			assign m_axis_tid_out = (ID_ENABLE ? m_axis_tid_reg : {ID_WIDTH {1'b0}});
			assign m_axis_tdest_out = (DEST_ENABLE ? m_axis_tdest_reg : {DEST_WIDTH {1'b0}});
			assign m_axis_tuser_out = (USER_ENABLE ? m_axis_tuser_reg : {USER_WIDTH {1'b0}});
			always @(posedge clk) begin
				m_axis_tvalid_reg <= m_axis_tvalid_reg && !m_axis_tready_out;
				out_fifo_half_full_reg <= $unsigned(out_fifo_wr_ptr_reg - out_fifo_rd_ptr_reg) >= (2 ** (OUTPUT_FIFO_ADDR_WIDTH - 1));
				if (!out_fifo_full && m_axis_tvalid_pipe) begin
					out_fifo_tdata[out_fifo_wr_ptr_reg[OUTPUT_FIFO_ADDR_WIDTH - 1:0]] <= m_axis_tdata_pipe;
					out_fifo_tkeep[out_fifo_wr_ptr_reg[OUTPUT_FIFO_ADDR_WIDTH - 1:0]] <= m_axis_tkeep_pipe;
					out_fifo_tlast[out_fifo_wr_ptr_reg[OUTPUT_FIFO_ADDR_WIDTH - 1:0]] <= m_axis_tlast_pipe;
					out_fifo_tid[out_fifo_wr_ptr_reg[OUTPUT_FIFO_ADDR_WIDTH - 1:0]] <= m_axis_tid_pipe;
					out_fifo_tdest[out_fifo_wr_ptr_reg[OUTPUT_FIFO_ADDR_WIDTH - 1:0]] <= m_axis_tdest_pipe;
					out_fifo_tuser[out_fifo_wr_ptr_reg[OUTPUT_FIFO_ADDR_WIDTH - 1:0]] <= m_axis_tuser_pipe;
					out_fifo_wr_ptr_reg <= out_fifo_wr_ptr_reg + 1;
				end
				if (!out_fifo_empty && (!m_axis_tvalid_reg || m_axis_tready_out)) begin
					m_axis_tdata_reg <= out_fifo_tdata[out_fifo_rd_ptr_reg[OUTPUT_FIFO_ADDR_WIDTH - 1:0]];
					m_axis_tkeep_reg <= out_fifo_tkeep[out_fifo_rd_ptr_reg[OUTPUT_FIFO_ADDR_WIDTH - 1:0]];
					m_axis_tvalid_reg <= 1'b1;
					m_axis_tlast_reg <= out_fifo_tlast[out_fifo_rd_ptr_reg[OUTPUT_FIFO_ADDR_WIDTH - 1:0]];
					m_axis_tid_reg <= out_fifo_tid[out_fifo_rd_ptr_reg[OUTPUT_FIFO_ADDR_WIDTH - 1:0]];
					m_axis_tdest_reg <= out_fifo_tdest[out_fifo_rd_ptr_reg[OUTPUT_FIFO_ADDR_WIDTH - 1:0]];
					m_axis_tuser_reg <= out_fifo_tuser[out_fifo_rd_ptr_reg[OUTPUT_FIFO_ADDR_WIDTH - 1:0]];
					out_fifo_rd_ptr_reg <= out_fifo_rd_ptr_reg + 1;
				end
				if (rst) begin
					out_fifo_wr_ptr_reg <= 0;
					out_fifo_rd_ptr_reg <= 0;
					m_axis_tvalid_reg <= 1'b0;
				end
			end
		end
		if (PAUSE_ENABLE) begin : pause
			reg pause_reg = 1'b0;
			reg pause_frame_reg = 1'b0;
			assign m_axis_tready_out = m_axis_tready && !pause_reg;
			assign m_axis_tvalid = m_axis_tvalid_out && !pause_reg;
			assign m_axis_tdata = m_axis_tdata_out;
			assign m_axis_tkeep = m_axis_tkeep_out;
			assign m_axis_tlast = m_axis_tlast_out;
			assign m_axis_tid = m_axis_tid_out;
			assign m_axis_tdest = m_axis_tdest_out;
			assign m_axis_tuser = m_axis_tuser_out;
			assign pause_ack = pause_reg;
			always @(posedge clk) begin
				if (FRAME_PAUSE) begin
					if (pause_reg)
						pause_reg <= pause_req;
					else if (m_axis_tvalid_out) begin
						pause_frame_reg <= 1'b1;
						if (m_axis_tready && m_axis_tlast) begin
							pause_frame_reg <= 1'b0;
							pause_reg <= pause_req;
						end
					end
					else if (!pause_frame_reg)
						pause_reg <= pause_req;
				end
				else
					pause_reg <= pause_req;
				if (rst) begin
					pause_frame_reg <= 1'b0;
					pause_reg <= 1'b0;
				end
			end
		end
		else begin : genblk7
			assign m_axis_tready_out = m_axis_tready;
			assign m_axis_tvalid = m_axis_tvalid_out;
			assign m_axis_tdata = m_axis_tdata_out;
			assign m_axis_tkeep = m_axis_tkeep_out;
			assign m_axis_tlast = m_axis_tlast_out;
			assign m_axis_tid = m_axis_tid_out;
			assign m_axis_tdest = m_axis_tdest_out;
			assign m_axis_tuser = m_axis_tuser_out;
			assign pause_ack = 1'b0;
		end
	endgenerate
endmodule
`resetall
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
module KL_acmp_nvm_shadow (
	clk_i,
	rst_n,
	tick_i,
	restore_go_i,
	restore_busy_o,
	restore_done_o,
	restore_fail_o,
	restore_blank_o,
	alarm_o,
	cap_wr_i,
	cap_sink_i,
	cap_rec_i,
	pre_valid_o,
	pre_sink_o,
	pre_talker_eid_o,
	pre_talker_uid_o,
	pre_ctlr_eid_o,
	pre_sw_o,
	pre_started_o,
	pre_ready_i,
	nvm_req_o,
	nvm_we_o,
	nvm_record_id_o,
	nvm_wvalid_o,
	nvm_wready_i,
	nvm_wdata_o,
	nvm_rvalid_i,
	nvm_rready_o,
	nvm_rdata_i,
	nvm_busy_i,
	nvm_done_i,
	nvm_err_i,
	dbg_dirty_o,
	dbg_valid_o,
	dbg_touched_o
);
	reg _sv2v_0;
	parameter [31:0] N_SINKS_P = 8;
	parameter [7:0] REC_ID_BASE_P = 8'h20;
	parameter [7:0] LAYOUT_VER_P = 8'h02;
	parameter [31:0] DEB_TICKS_P = 500;
	parameter [31:0] RETRY_MAX_P = 2;
	localparam [31:0] SINK_W_C = (N_SINKS_P > 1 ? $clog2(N_SINKS_P) : 1);
	input wire clk_i;
	input wire rst_n;
	input wire tick_i;
	input wire restore_go_i;
	output wire restore_busy_o;
	output wire restore_done_o;
	output wire restore_fail_o;
	output wire restore_blank_o;
	output wire alarm_o;
	input wire cap_wr_i;
	input wire [SINK_W_C - 1:0] cap_sink_i;
	localparam [31:0] pp_acmp_pkg_ACMP_REC_W_C = 384;
	input wire [383:0] cap_rec_i;
	output wire pre_valid_o;
	output wire [15:0] pre_sink_o;
	output wire [63:0] pre_talker_eid_o;
	output wire [15:0] pre_talker_uid_o;
	output wire [63:0] pre_ctlr_eid_o;
	output wire pre_sw_o;
	output wire pre_started_o;
	input wire pre_ready_i;
	output reg nvm_req_o;
	output reg nvm_we_o;
	output reg [7:0] nvm_record_id_o;
	output wire nvm_wvalid_o;
	input wire nvm_wready_i;
	output wire [7:0] nvm_wdata_o;
	input wire nvm_rvalid_i;
	output wire nvm_rready_o;
	input wire [7:0] nvm_rdata_i;
	input wire nvm_busy_i;
	input wire nvm_done_i;
	input wire nvm_err_i;
	output wire [N_SINKS_P - 1:0] dbg_dirty_o;
	output wire [N_SINKS_P - 1:0] dbg_valid_o;
	output wire [N_SINKS_P - 1:0] dbg_touched_o;
	localparam [7:0] MAGIC_HI_C = 8'h17;
	localparam [7:0] MAGIC_LO_C = 8'h22;
	localparam [31:0] PL_BYTES_C = 20;
	function automatic [15:0] sv2v_cast_16;
		input reg [15:0] inp;
		sv2v_cast_16 = inp;
	endfunction
	localparam [15:0] PLEN_C = sv2v_cast_16(PL_BYTES_C);
	localparam [31:0] SHW_W_C = 146;
	reg [3:0] hs_r;
	reg [SINK_W_C:0] init_cnt_r;
	reg go_pend_r;
	reg [145:0] shw_ram_r [0:N_SINKS_P - 1];
	reg [145:0] shw_rdata_r;
	wire rd_en_w;
	wire [SINK_W_C - 1:0] rd_addr_w;
	wire wr_en_w;
	wire [SINK_W_C - 1:0] wr_addr_w;
	wire [145:0] wr_data_w;
	always @(posedge clk_i) begin : shw_ram_wr
		if (wr_en_w)
			shw_ram_r[wr_addr_w] <= wr_data_w;
	end
	always @(posedge clk_i) begin : shw_ram_rd
		if (rd_en_w)
			shw_rdata_r <= shw_ram_r[rd_addr_w];
	end
	reg byp_v_r;
	reg [SINK_W_C - 1:0] byp_sink_r;
	reg [145:0] byp_data_r;
	always @(posedge clk_i) begin : byp_ff
		if (!rst_n) begin
			byp_v_r <= 1'b0;
			byp_sink_r <= 1'sb0;
			byp_data_r <= 1'sb0;
		end
		else begin
			byp_v_r <= wr_en_w;
			byp_sink_r <= wr_addr_w;
			byp_data_r <= wr_data_w;
		end
	end
	reg [N_SINKS_P - 1:0] valid_r;
	reg [N_SINKS_P - 1:0] dirty_r;
	reg [N_SINKS_P - 1:0] touched_r;
	wire [383:0] cap_rec_w;
	reg [145:0] cap_proj_w;
	wire cap_vld_w;
	wire cap_active_w;
	function automatic [383:0] sv2v_cast_384;
		input reg [383:0] inp;
		sv2v_cast_384 = inp;
	endfunction
	assign cap_rec_w = sv2v_cast_384(cap_rec_i);
	assign cap_vld_w = cap_rec_w[11];
	assign cap_active_w = cap_wr_i && (hs_r != 4'd0);
	always @(*) begin : cap_proj
		if (_sv2v_0)
			;
		cap_proj_w[145] = cap_rec_w[12];
		cap_proj_w[144] = cap_rec_w[13];
		cap_proj_w[143-:16] = cap_rec_w[111-:16];
		cap_proj_w[127-:64] = cap_rec_w[95-:64];
		cap_proj_w[63-:64] = cap_rec_w[191-:64];
	end
	reg c1_v_r;
	reg [SINK_W_C - 1:0] c1_sink_r;
	reg [145:0] c1_proj_r;
	reg c1_vld_r;
	always @(posedge clk_i) begin : cap_stage
		if (!rst_n) begin
			c1_v_r <= 1'b0;
			c1_sink_r <= 1'sb0;
			c1_proj_r <= 1'sb0;
			c1_vld_r <= 1'b0;
		end
		else begin
			c1_v_r <= cap_active_w;
			c1_sink_r <= cap_sink_i;
			c1_proj_r <= cap_proj_w;
			c1_vld_r <= cap_vld_w;
		end
	end
	wire [145:0] cmp_data_w;
	wire c1_diff_w;
	wire c1_wr_w;
	assign cmp_data_w = (byp_v_r && (byp_sink_r == c1_sink_r) ? byp_data_r : shw_rdata_r);
	function automatic [145:0] sv2v_cast_D0A1A;
		input reg [145:0] inp;
		sv2v_cast_D0A1A = inp;
	endfunction
	assign c1_diff_w = (sv2v_cast_D0A1A(c1_proj_r) != cmp_data_w) || (c1_vld_r != valid_r[c1_sink_r]);
	assign c1_wr_w = c1_v_r && c1_diff_w;
	wire go_take_w;
	wire rest_span_w;
	assign go_take_w = (hs_r == 4'd1) && (restore_go_i || go_pend_r);
	assign rest_span_w = (((((go_take_w || (hs_r == 4'd2)) || (hs_r == 4'd3)) || (hs_r == 4'd4)) || (hs_r == 4'd5)) || (hs_r == 4'd6)) || (hs_r == 4'd7);
	reg [SINK_W_C - 1:0] rs_k_r;
	reg [16:0] rbcnt_r;
	reg [7:0] rver_r;
	reg [7:0] rrid_r;
	reg [15:0] rplen_r;
	reg [15:0] rcrc_rx_r;
	reg [15:0] rcrc_acc_r;
	reg rvld_q_r;
	reg rstarted_q_r;
	reg rsw_q_r;
	reg [15:0] ruid_q_r;
	reg [63:0] rtk_q_r;
	reg [63:0] rctlr_q_r;
	wire [16:0] rexp_total_w;
	wire rrec_ok_w;
	function automatic [16:0] sv2v_cast_17;
		input reg [16:0] inp;
		sv2v_cast_17 = inp;
	endfunction
	assign rexp_total_w = 17'd8 + sv2v_cast_17(rplen_r);
	assign rrec_ok_w = (((rver_r == LAYOUT_VER_P) && (rrid_r == nvm_record_id_o)) && (rplen_r == PLEN_C)) && (rcrc_acc_r == rcrc_rx_r);
	reg [SINK_W_C - 1:0] rp_k_r;
	reg [145:0] rp_fields_r;
	reg [SINK_W_C - 1:0] fl_sink_r;
	reg [145:0] fl_fields_r;
	reg fl_vld_r;
	reg [15:0] fl_crc_r;
	reg [4:0] fl_cidx_r;
	reg [4:0] fl_sidx_r;
	reg [31:0] fl_retry_r;
	reg fl_taint_r;
	reg fl_any_w;
	reg [SINK_W_C - 1:0] fl_pick_w;
	function automatic [SINK_W_C - 1:0] sv2v_cast_86716;
		input reg [SINK_W_C - 1:0] inp;
		sv2v_cast_86716 = inp;
	endfunction
	always @(*) begin : dirty_pick
		if (_sv2v_0)
			;
		fl_any_w = 1'b0;
		fl_pick_w = 1'sb0;
		begin : sv2v_autoblock_1
			reg [31:0] i;
			for (i = 0; i < N_SINKS_P; i = i + 1)
				if (!fl_any_w && dirty_r[i]) begin
					fl_any_w = 1'b1;
					fl_pick_w = sv2v_cast_86716(i);
				end
		end
	end
	reg deb_open_r;
	reg [31:0] deb_cnt_r;
	reg fl_arm_r;
	always @(posedge clk_i) begin : debounce_ff
		if (!rst_n) begin
			deb_open_r <= 1'b0;
			deb_cnt_r <= 32'd0;
			fl_arm_r <= 1'b0;
		end
		else begin
			if (c1_wr_w && !deb_open_r) begin
				deb_open_r <= 1'b1;
				deb_cnt_r <= DEB_TICKS_P;
			end
			else if (deb_open_r && tick_i) begin
				if (deb_cnt_r <= 32'd1) begin
					deb_open_r <= 1'b0;
					fl_arm_r <= 1'b1;
				end
				else
					deb_cnt_r <= deb_cnt_r - 32'd1;
			end
			if (((hs_r == 4'd9) && fl_arm_r) && !fl_any_w)
				fl_arm_r <= 1'b0;
		end
	end
	function automatic [15:0] crc16_f;
		input reg [15:0] c;
		input reg [7:0] d;
		reg [15:0] x;
		begin
			x = c ^ {d, 8'h00};
			begin : sv2v_autoblock_2
				reg [31:0] i;
				for (i = 0; i < 8; i = i + 1)
					x = (x[15] ? (x << 1) ^ 16'h1021 : x << 1);
			end
			crc16_f = x;
		end
	endfunction
	function automatic [145:0] sv2v_cast_146;
		input reg [145:0] inp;
		sv2v_cast_146 = inp;
	endfunction
	function automatic [31:0] sv2v_cast_32;
		input reg [31:0] inp;
		sv2v_cast_32 = inp;
	endfunction
	function automatic [7:0] fr_byte_f;
		input reg [145:0] fields;
		input reg vld;
		input reg [7:0] rid;
		input reg [15:0] crc;
		input reg [4:0] idx;
		reg [145:0] f;
		reg [7:0] b;
		begin
			f = sv2v_cast_146(fields);
			(* full_case, parallel_case *)
			case (idx)
				5'd0: b = MAGIC_HI_C;
				5'd1: b = MAGIC_LO_C;
				5'd2: b = LAYOUT_VER_P;
				5'd3: b = rid;
				5'd4: b = PLEN_C[15:8];
				5'd5: b = PLEN_C[7:0];
				5'd6: b = crc[15:8];
				5'd7: b = crc[7:0];
				5'd8: b = {5'd0, f[144], f[145], vld};
				5'd9: b = 8'd0;
				5'd10: b = f[143:136];
				5'd11: b = f[135:128];
				default:
					if (idx < 5'd20)
						b = f[64 + (8 * (32'd19 - sv2v_cast_32(idx)))+:8];
					else
						b = f[0 + (8 * (32'd27 - sv2v_cast_32(idx)))+:8];
			endcase
			fr_byte_f = b;
		end
	endfunction
	wire [4:0] fl_cbyte_w;
	assign fl_cbyte_w = (fl_cidx_r < 5'd6 ? fl_cidx_r : fl_cidx_r + 5'd2);
	wire fsm_rd_req_w;
	wire [SINK_W_C - 1:0] fsm_rd_addr_w;
	wire fsm_rd_gnt_w;
	assign fsm_rd_req_w = (hs_r == 4'd5) || (hs_r == 4'd10);
	assign fsm_rd_addr_w = (hs_r == 4'd5 ? rp_k_r : fl_sink_r);
	assign fsm_rd_gnt_w = fsm_rd_req_w && !cap_active_w;
	assign rd_en_w = cap_active_w || fsm_rd_req_w;
	assign rd_addr_w = (cap_active_w ? cap_sink_i : fsm_rd_addr_w);
	wire fsm_wr_req_w;
	wire [SINK_W_C - 1:0] fsm_wr_addr_w;
	wire [145:0] fsm_wr_data_w;
	wire fsm_wr_gnt_w;
	reg [145:0] rs_store_w;
	always @(*) begin : rs_store
		if (_sv2v_0)
			;
		rs_store_w[145] = rstarted_q_r;
		rs_store_w[144] = rsw_q_r;
		rs_store_w[143-:16] = ruid_q_r;
		rs_store_w[127-:64] = rtk_q_r;
		rs_store_w[63-:64] = rctlr_q_r;
	end
	function automatic [((SINK_W_C + 0) >= 0 ? SINK_W_C + 1 : 1 - (SINK_W_C + 0)) - 1:0] sv2v_cast_70DE6;
		input reg [((SINK_W_C + 0) >= 0 ? SINK_W_C + 1 : 1 - (SINK_W_C + 0)) - 1:0] inp;
		sv2v_cast_70DE6 = inp;
	endfunction
	assign fsm_wr_req_w = ((hs_r == 4'd0) && (init_cnt_r < sv2v_cast_70DE6(N_SINKS_P))) || ((hs_r == 4'd4) && !touched_r[rs_k_r]);
	assign fsm_wr_addr_w = (hs_r == 4'd0 ? init_cnt_r[SINK_W_C - 1:0] : rs_k_r);
	assign fsm_wr_data_w = (hs_r == 4'd0 ? {146 {1'sb0}} : sv2v_cast_D0A1A(rs_store_w));
	assign fsm_wr_gnt_w = fsm_wr_req_w && !c1_wr_w;
	assign wr_en_w = c1_wr_w || fsm_wr_req_w;
	assign wr_addr_w = (c1_wr_w ? c1_sink_r : fsm_wr_addr_w);
	assign wr_data_w = (c1_wr_w ? sv2v_cast_D0A1A(c1_proj_r) : fsm_wr_data_w);
	wire rs_torn_w;
	wire rs_empty_w;
	wire rs_complete_w;
	assign rs_torn_w = (hs_r == 4'd3) && ((nvm_err_i && (rbcnt_r != 17'd0)) || ((nvm_done_i && (rbcnt_r != 17'd0)) && ((rbcnt_r < 17'd8) || (rbcnt_r != rexp_total_w))));
	assign rs_empty_w = (hs_r == 4'd3) && ((nvm_err_i && (rbcnt_r == 17'd0)) || (nvm_done_i && (rbcnt_r == 17'd0)));
	assign rs_complete_w = (((hs_r == 4'd3) && nvm_done_i) && (rbcnt_r >= 17'd8)) && (rbcnt_r == rexp_total_w);
	wire fl_done_w;
	wire fl_err_w;
	wire fl_giveup_w;
	wire fl_active_w;
	assign fl_done_w = (hs_r == 4'd15) && nvm_done_i;
	assign fl_err_w = ((hs_r == 4'd15) || (hs_r == 4'd14)) && nvm_err_i;
	assign fl_giveup_w = fl_err_w && (fl_retry_r >= RETRY_MAX_P);
	assign fl_active_w = (((((hs_r == 4'd10) || (hs_r == 4'd11)) || (hs_r == 4'd12)) || (hs_r == 4'd13)) || (hs_r == 4'd14)) || (hs_r == 4'd15);
	always @(posedge clk_i) begin : fl_taint_ff
		if (!rst_n)
			fl_taint_r <= 1'b0;
		else if (((hs_r == 4'd9) && fl_arm_r) && fl_any_w)
			fl_taint_r <= 1'b0;
		else if ((c1_wr_w && fl_active_w) && (c1_sink_r == fl_sink_r))
			fl_taint_r <= 1'b1;
	end
	always @(posedge clk_i) begin : flags_ff
		if (!rst_n) begin
			valid_r <= 1'sb0;
			dirty_r <= 1'sb0;
			touched_r <= 1'sb0;
		end
		else begin
			if (go_take_w)
				touched_r <= 1'sb0;
			if (rs_torn_w) begin : sv2v_autoblock_3
				reg [31:0] i;
				for (i = 0; i < N_SINKS_P; i = i + 1)
					if (!touched_r[i])
						valid_r[i] <= 1'b0;
			end
			if ((hs_r == 4'd4) && fsm_wr_gnt_w)
				valid_r[rs_k_r] <= rvld_q_r;
			if ((rs_complete_w && !rrec_ok_w) && !touched_r[rs_k_r])
				valid_r[rs_k_r] <= 1'b0;
			if (rs_empty_w && !touched_r[rs_k_r])
				valid_r[rs_k_r] <= 1'b0;
			if ((fl_done_w && !fl_taint_r) || fl_giveup_w)
				dirty_r[fl_sink_r] <= 1'b0;
			if (c1_wr_w) begin
				valid_r[c1_sink_r] <= c1_vld_r;
				dirty_r[c1_sink_r] <= 1'b1;
				if (rest_span_w)
					touched_r[c1_sink_r] <= 1'b1;
			end
		end
	end
	reg alarm_r;
	always @(posedge clk_i) begin : alarm_ff
		if (!rst_n)
			alarm_r <= 1'b0;
		else if (fl_giveup_w)
			alarm_r <= 1'b1;
	end
	reg done_r;
	reg fail_r;
	reg any_rec_r;
	function automatic signed [((SINK_W_C + 0) >= 0 ? SINK_W_C + 1 : 1 - (SINK_W_C + 0)) - 1:0] sv2v_cast_70DE6_signed;
		input reg signed [((SINK_W_C + 0) >= 0 ? SINK_W_C + 1 : 1 - (SINK_W_C + 0)) - 1:0] inp;
		sv2v_cast_70DE6_signed = inp;
	endfunction
	function automatic [7:0] sv2v_cast_8;
		input reg [7:0] inp;
		sv2v_cast_8 = inp;
	endfunction
	function automatic signed [SINK_W_C - 1:0] sv2v_cast_86716_signed;
		input reg signed [SINK_W_C - 1:0] inp;
		sv2v_cast_86716_signed = inp;
	endfunction
	always @(posedge clk_i) begin : engine
		if (!rst_n) begin
			hs_r <= 4'd0;
			init_cnt_r <= 1'sb0;
			go_pend_r <= 1'b0;
			rs_k_r <= 1'sb0;
			rbcnt_r <= 17'd0;
			rver_r <= 8'd0;
			rrid_r <= 8'd0;
			rplen_r <= 16'd0;
			rcrc_rx_r <= 16'd0;
			rcrc_acc_r <= 16'd0;
			rvld_q_r <= 1'b0;
			rstarted_q_r <= 1'b0;
			rsw_q_r <= 1'b0;
			ruid_q_r <= 16'd0;
			rtk_q_r <= 64'd0;
			rctlr_q_r <= 64'd0;
			rp_k_r <= 1'sb0;
			rp_fields_r <= 1'sb0;
			fl_sink_r <= 1'sb0;
			fl_fields_r <= 1'sb0;
			fl_vld_r <= 1'b0;
			fl_crc_r <= 16'd0;
			fl_cidx_r <= 5'd0;
			fl_sidx_r <= 5'd0;
			fl_retry_r <= 32'd0;
			done_r <= 1'b0;
			fail_r <= 1'b0;
			any_rec_r <= 1'b0;
			nvm_req_o <= 1'b0;
			nvm_we_o <= 1'b0;
			nvm_record_id_o <= 8'd0;
		end
		else begin
			nvm_req_o <= 1'b0;
			if (restore_go_i && (hs_r == 4'd0))
				go_pend_r <= 1'b1;
			(* full_case, parallel_case *)
			case (hs_r)
				4'd0:
					if (init_cnt_r < sv2v_cast_70DE6(N_SINKS_P))
						init_cnt_r <= init_cnt_r + sv2v_cast_70DE6_signed(1);
					else
						hs_r <= 4'd1;
				4'd1:
					if (go_take_w) begin
						go_pend_r <= 1'b0;
						rs_k_r <= 1'sb0;
						any_rec_r <= 1'b0;
						hs_r <= 4'd2;
					end
				4'd2:
					if ((!nvm_busy_i && !nvm_done_i) && !nvm_err_i) begin
						nvm_req_o <= 1'b1;
						nvm_we_o <= 1'b0;
						nvm_record_id_o <= REC_ID_BASE_P + sv2v_cast_8(rs_k_r);
						rbcnt_r <= 17'd0;
						rcrc_acc_r <= 16'hffff;
						hs_r <= 4'd3;
					end
				4'd3: begin
					if (nvm_rvalid_i) begin
						if ((rbcnt_r != 17'd6) && (rbcnt_r != 17'd7))
							rcrc_acc_r <= crc16_f(rcrc_acc_r, nvm_rdata_i);
						if (rbcnt_r == 17'd2)
							rver_r <= nvm_rdata_i;
						else if (rbcnt_r == 17'd3)
							rrid_r <= nvm_rdata_i;
						else if (rbcnt_r == 17'd4)
							rplen_r <= {nvm_rdata_i, rplen_r[7:0]};
						else if (rbcnt_r == 17'd5)
							rplen_r <= {rplen_r[15:8], nvm_rdata_i};
						else if (rbcnt_r == 17'd6)
							rcrc_rx_r <= {nvm_rdata_i, rcrc_rx_r[7:0]};
						else if (rbcnt_r == 17'd7)
							rcrc_rx_r <= {rcrc_rx_r[15:8], nvm_rdata_i};
						else if (rbcnt_r == 17'd8) begin
							rvld_q_r <= nvm_rdata_i[0];
							rstarted_q_r <= nvm_rdata_i[1];
							rsw_q_r <= nvm_rdata_i[2];
						end
						else if ((rbcnt_r == 17'd10) || (rbcnt_r == 17'd11))
							ruid_q_r <= {ruid_q_r[7:0], nvm_rdata_i};
						else if ((rbcnt_r >= 17'd12) && (rbcnt_r < 17'd20))
							rtk_q_r <= {rtk_q_r[55:0], nvm_rdata_i};
						else if ((rbcnt_r >= 17'd20) && (rbcnt_r < 17'd28))
							rctlr_q_r <= {rctlr_q_r[55:0], nvm_rdata_i};
						rbcnt_r <= rbcnt_r + 17'd1;
					end
					if (rs_torn_w) begin
						fail_r <= 1'b1;
						done_r <= 1'b1;
						any_rec_r <= 1'b0;
						hs_r <= 4'd9;
					end
					else if (rs_empty_w || (rs_complete_w && !rrec_ok_w)) begin
						if (rs_k_r == sv2v_cast_86716(N_SINKS_P - 1)) begin
							rp_k_r <= 1'sb0;
							hs_r <= 4'd5;
						end
						else begin
							rs_k_r <= rs_k_r + sv2v_cast_86716_signed(1);
							hs_r <= 4'd2;
						end
					end
					else if (rs_complete_w) begin
						any_rec_r <= 1'b1;
						hs_r <= 4'd4;
					end
				end
				4'd4:
					if (fsm_wr_gnt_w || touched_r[rs_k_r]) begin
						if (rs_k_r == sv2v_cast_86716(N_SINKS_P - 1)) begin
							rp_k_r <= 1'sb0;
							hs_r <= 4'd5;
						end
						else begin
							rs_k_r <= rs_k_r + sv2v_cast_86716_signed(1);
							hs_r <= 4'd2;
						end
					end
				4'd5:
					if (!valid_r[rp_k_r] || touched_r[rp_k_r]) begin
						if (rp_k_r == sv2v_cast_86716(N_SINKS_P - 1))
							hs_r <= 4'd8;
						else
							rp_k_r <= rp_k_r + sv2v_cast_86716_signed(1);
					end
					else if (fsm_rd_gnt_w)
						hs_r <= 4'd6;
				4'd6: begin
					rp_fields_r <= sv2v_cast_146(shw_rdata_r);
					hs_r <= 4'd7;
				end
				4'd7:
					if (pre_ready_i || touched_r[rp_k_r]) begin
						if (rp_k_r == sv2v_cast_86716(N_SINKS_P - 1))
							hs_r <= 4'd8;
						else begin
							rp_k_r <= rp_k_r + sv2v_cast_86716_signed(1);
							hs_r <= 4'd5;
						end
					end
				4'd8: begin
					done_r <= 1'b1;
					hs_r <= 4'd9;
				end
				4'd9:
					if (fl_arm_r && fl_any_w) begin
						fl_sink_r <= fl_pick_w;
						fl_retry_r <= 32'd0;
						hs_r <= 4'd10;
					end
				4'd10:
					if (fsm_rd_gnt_w)
						hs_r <= 4'd11;
				4'd11: begin
					fl_fields_r <= sv2v_cast_146(shw_rdata_r);
					fl_vld_r <= valid_r[fl_sink_r];
					fl_crc_r <= 16'hffff;
					fl_cidx_r <= 5'd0;
					hs_r <= 4'd12;
				end
				4'd12: begin
					fl_crc_r <= crc16_f(fl_crc_r, fr_byte_f(sv2v_cast_D0A1A(fl_fields_r), fl_vld_r, REC_ID_BASE_P + sv2v_cast_8(fl_sink_r), 16'h0000, fl_cbyte_w));
					if (fl_cidx_r == 5'd25) begin
						fl_sidx_r <= 5'd0;
						hs_r <= 4'd13;
					end
					else
						fl_cidx_r <= fl_cidx_r + 5'd1;
				end
				4'd13:
					if ((!nvm_busy_i && !nvm_done_i) && !nvm_err_i) begin
						nvm_req_o <= 1'b1;
						nvm_we_o <= 1'b1;
						nvm_record_id_o <= REC_ID_BASE_P + sv2v_cast_8(fl_sink_r);
						hs_r <= 4'd14;
					end
				4'd14:
					if (nvm_err_i) begin
						if (fl_retry_r >= RETRY_MAX_P)
							hs_r <= 4'd9;
						else begin
							fl_retry_r <= fl_retry_r + 32'd1;
							hs_r <= 4'd10;
						end
					end
					else if (nvm_wready_i) begin
						if (fl_sidx_r == 5'd27)
							hs_r <= 4'd15;
						else
							fl_sidx_r <= fl_sidx_r + 5'd1;
					end
				4'd15:
					if (nvm_done_i)
						hs_r <= 4'd9;
					else if (nvm_err_i) begin
						if (fl_retry_r >= RETRY_MAX_P)
							hs_r <= 4'd9;
						else begin
							fl_retry_r <= fl_retry_r + 32'd1;
							hs_r <= 4'd10;
						end
					end
				default: hs_r <= 4'd9;
			endcase
		end
	end
	assign nvm_wvalid_o = hs_r == 4'd14;
	assign nvm_wdata_o = fr_byte_f(sv2v_cast_D0A1A(fl_fields_r), fl_vld_r, nvm_record_id_o, fl_crc_r, fl_sidx_r);
	assign nvm_rready_o = hs_r == 4'd3;
	assign pre_valid_o = (hs_r == 4'd7) && !touched_r[rp_k_r];
	assign pre_sink_o = sv2v_cast_16(sv2v_cast_32(rp_k_r));
	assign pre_talker_eid_o = rp_fields_r[127-:64];
	assign pre_talker_uid_o = rp_fields_r[143-:16];
	assign pre_ctlr_eid_o = rp_fields_r[63-:64];
	assign pre_sw_o = rp_fields_r[144];
	assign pre_started_o = rp_fields_r[145];
	assign restore_busy_o = ((((((hs_r == 4'd2) || (hs_r == 4'd3)) || (hs_r == 4'd4)) || (hs_r == 4'd5)) || (hs_r == 4'd6)) || (hs_r == 4'd7)) || (hs_r == 4'd8);
	assign restore_done_o = done_r;
	assign restore_fail_o = fail_r;
	assign restore_blank_o = done_r && !any_rec_r;
	assign alarm_o = alarm_r;
	assign dbg_dirty_o = dirty_r;
	assign dbg_valid_o = valid_r;
	assign dbg_touched_o = touched_r;
	initial _sv2v_0 = 0;
endmodule
`default_nettype wire
`default_nettype none
module KL_acmp_talker (
	clk_i,
	rst_n,
	own_entity_id_i,
	cfg_src_en_i,
	cfg_src_iface_i,
	cfg_stream_id_i,
	srp_lsn_reg_state_i,
	srp_class_vid_i,
	srp_pcp_change_i,
	txn_valid_i,
	txn_i,
	txn_ready_o,
	rxs_rd_slot_o,
	rxs_rd_addr_o,
	rxs_rd_en_o,
	rxs_rd_data_i,
	rxs_slot_len_i,
	rxs_free_o,
	rxs_free_slot_o,
	resp_valid_o,
	resp_msg_type_o,
	resp_status_o,
	resp_stream_id_o,
	resp_controller_eid_o,
	resp_talker_eid_o,
	resp_listener_eid_o,
	resp_talker_uid_o,
	resp_listener_uid_o,
	resp_dest_mac_o,
	resp_conn_count_o,
	resp_seq_id_o,
	resp_flags_o,
	resp_vlan_id_o,
	resp_if_index_o,
	maap_req_valid_o,
	maap_req_ready_i,
	maap_req_release_o,
	maap_req_src_o,
	maap_rsp_valid_i,
	maap_rsp_ok_i,
	maap_rsp_da_i,
	maap_conflict_valid_i,
	maap_conflict_src_i,
	maap_conflict_ack_o,
	declaring_o,
	gate_open_o,
	gate_close_o,
	gate_src_o,
	gate_stream_id_o,
	gate_da_o,
	gate_vlan_o,
	now_ms_i,
	tmr_arm_valid_o,
	tmr_arm_cancel_o,
	tmr_arm_slot_o,
	tmr_arm_owner_o,
	tmr_arm_deadline_ms_o,
	tmr_exp_valid_i,
	tmr_exp_slot_i,
	tmr_exp_owner_i,
	prng_draw_req_o,
	prng_draw_kind_o,
	prng_draw_busy_i,
	prng_draw_valid_i,
	prng_draw_ms_i
);
	reg _sv2v_0;
	parameter [31:0] N_STREAM_OUT_P = 8;
	parameter [31:0] RX_SLOTS_P = 4;
	parameter [31:0] RX_SLOT_BYTES_P = 576;
	localparam [31:0] pp_pkg_PP_CA_POOL_C = 4;
	localparam [31:0] pp_pkg_PP_N_CTRL_C = 16;
	localparam [31:0] pp_pkg_PP_N_IF_C = 1;
	localparam [31:0] pp_pkg_PP_N_STREAM_IN_C = 8;
	localparam [31:0] pp_pkg_PP_N_STREAM_OUT_C = 8;
	localparam [31:0] pp_pkg_PP_MAAP_SLOTS_C = 2;
	localparam [31:0] pp_pkg_PP_SINGLETON_SLOTS_C = 5;
	localparam [31:0] pp_pkg_PP_SRP_CAD_SLOTS_C = 7;
	function automatic [415:0] pp_pkg_pp_timer_map;
		input reg [31:0] n_if;
		input reg [31:0] si;
		input reg [31:0] so;
		input reg [31:0] n_ctrl;
		input reg [31:0] ca_pool;
		reg [415:0] m;
		begin
			m[415-:32] = 32'd0;
			m[383-:32] = m[415-:32] + n_if;
			m[351-:32] = m[383-:32] + si;
			m[319-:32] = m[351-:32] + si;
			m[287-:32] = m[319-:32] + so;
			m[255-:32] = m[287-:32] + ((32'd2 * n_ctrl) * n_if);
			m[223-:32] = m[255-:32] + ca_pool;
			m[191-:32] = m[223-:32] + pp_pkg_PP_SINGLETON_SLOTS_C;
			m[159-:32] = m[191-:32] + pp_pkg_PP_MAAP_SLOTS_C;
			m[127-:32] = m[159-:32];
			m[95-:32] = m[127-:32] + pp_pkg_PP_SRP_CAD_SLOTS_C;
			m[63-:32] = m[95-:32] + so;
			m[31-:32] = m[127-:32] + (((pp_pkg_PP_SRP_CAD_SLOTS_C + si) + so) * n_if);
			pp_pkg_pp_timer_map = m;
		end
	endfunction
	function automatic [31:0] pp_pkg_pp_timer_slots;
		input reg [31:0] n_if;
		input reg [31:0] si;
		input reg [31:0] so;
		input reg [31:0] n_ctrl;
		input reg [31:0] ca_pool;
		input reg en_srp;
		reg [415:0] m;
		begin
			m = pp_pkg_pp_timer_map(n_if, si, so, n_ctrl, ca_pool);
			pp_pkg_pp_timer_slots = (en_srp ? m[31-:32] : m[159-:32]);
		end
	endfunction
	localparam [31:0] pp_pkg_PP_TIMER_SLOTS_C = pp_pkg_pp_timer_slots(pp_pkg_PP_N_IF_C, pp_pkg_PP_N_STREAM_IN_C, pp_pkg_PP_N_STREAM_OUT_C, pp_pkg_PP_N_CTRL_C, pp_pkg_PP_CA_POOL_C, 1'b1);
	parameter [31:0] TMR_SLOTS_P = pp_pkg_PP_TIMER_SLOTS_C;
	parameter [31:0] TMR_SLOT_BASE_P = 17;
	parameter [31:0] TMR_OWNER_BASE_P = 32'h00000050;
	parameter [31:0] DAFRESH_MS_P = 15000;
	parameter [31:0] MAAP_ACCEPT_CYC_P = 1024;
	parameter [31:0] MAAP_RSP_MS_P = 32'd10000;
	localparam [31:0] SRC_W_C = (N_STREAM_OUT_P > 32'd1 ? $clog2(N_STREAM_OUT_P) : 32'd1);
	localparam [31:0] RXS_W_C = (RX_SLOTS_P > 32'd1 ? $clog2(RX_SLOTS_P) : 32'd1);
	localparam [31:0] RXA_W_C = $clog2(RX_SLOT_BYTES_P);
	localparam [31:0] RXL_W_C = $clog2(RX_SLOT_BYTES_P + 1);
	localparam [31:0] TMR_AW_C = (TMR_SLOTS_P > 32'd1 ? $clog2(TMR_SLOTS_P) : 32'd1);
	localparam [31:0] MTMO_W_C = (MAAP_ACCEPT_CYC_P > 32'd1 ? $clog2(MAAP_ACCEPT_CYC_P) : 32'd1);
	input wire clk_i;
	input wire rst_n;
	input wire [63:0] own_entity_id_i;
	input wire [N_STREAM_OUT_P - 1:0] cfg_src_en_i;
	input wire [(N_STREAM_OUT_P * 2) - 1:0] cfg_src_iface_i;
	input wire [(N_STREAM_OUT_P * 64) - 1:0] cfg_stream_id_i;
	input wire [(N_STREAM_OUT_P * 2) - 1:0] srp_lsn_reg_state_i;
	input wire [11:0] srp_class_vid_i;
	input wire srp_pcp_change_i;
	input wire txn_valid_i;
	localparam [31:0] pp_pkg_PP_TXN_W_C = 393;
	input wire [392:0] txn_i;
	output wire txn_ready_o;
	output wire [RXS_W_C - 1:0] rxs_rd_slot_o;
	output wire [RXA_W_C - 1:0] rxs_rd_addr_o;
	output wire rxs_rd_en_o;
	input wire [7:0] rxs_rd_data_i;
	input wire [RXL_W_C - 1:0] rxs_slot_len_i;
	output wire rxs_free_o;
	output wire [RXS_W_C - 1:0] rxs_free_slot_o;
	output reg resp_valid_o;
	output reg [3:0] resp_msg_type_o;
	output reg [4:0] resp_status_o;
	output reg [63:0] resp_stream_id_o;
	output reg [63:0] resp_controller_eid_o;
	output reg [63:0] resp_talker_eid_o;
	output reg [63:0] resp_listener_eid_o;
	output reg [15:0] resp_talker_uid_o;
	output reg [15:0] resp_listener_uid_o;
	output reg [47:0] resp_dest_mac_o;
	output reg [15:0] resp_conn_count_o;
	output reg [15:0] resp_seq_id_o;
	output reg [15:0] resp_flags_o;
	output reg [15:0] resp_vlan_id_o;
	output reg [1:0] resp_if_index_o;
	output wire maap_req_valid_o;
	input wire maap_req_ready_i;
	output wire maap_req_release_o;
	output wire [SRC_W_C - 1:0] maap_req_src_o;
	input wire maap_rsp_valid_i;
	input wire maap_rsp_ok_i;
	input wire [47:0] maap_rsp_da_i;
	input wire maap_conflict_valid_i;
	input wire [SRC_W_C - 1:0] maap_conflict_src_i;
	output wire maap_conflict_ack_o;
	output wire [N_STREAM_OUT_P - 1:0] declaring_o;
	output reg gate_open_o;
	output reg gate_close_o;
	output reg [SRC_W_C - 1:0] gate_src_o;
	output reg [63:0] gate_stream_id_o;
	output reg [47:0] gate_da_o;
	output reg [11:0] gate_vlan_o;
	input wire [31:0] now_ms_i;
	output reg tmr_arm_valid_o;
	output reg tmr_arm_cancel_o;
	output reg [TMR_AW_C - 1:0] tmr_arm_slot_o;
	localparam [31:0] pp_pkg_PP_TIMER_OWNER_W_C = 8;
	output reg [7:0] tmr_arm_owner_o;
	output reg [31:0] tmr_arm_deadline_ms_o;
	input wire tmr_exp_valid_i;
	input wire [TMR_AW_C - 1:0] tmr_exp_slot_i;
	input wire [7:0] tmr_exp_owner_i;
	output wire prng_draw_req_o;
	output wire [2:0] prng_draw_kind_o;
	input wire prng_draw_busy_i;
	input wire prng_draw_valid_i;
	input wire [15:0] prng_draw_ms_i;
	localparam [3:0] MT_PROBE_TX_C = 4'd0;
	localparam [3:0] MT_DISC_TX_C = 4'd2;
	localparam [3:0] MT_GTX_ST_C = 4'd4;
	localparam [3:0] MT_GTX_CN_C = 4'd12;
	localparam [4:0] ST_SUCCESS_C = 5'd0;
	localparam [4:0] ST_TALKER_UNKNOWN_C = 5'd2;
	localparam [4:0] ST_DEST_MAC_FAIL_C = 5'd3;
	localparam [4:0] ST_NOT_SUPPORTED_C = 5'd31;
	localparam [15:0] FLG_ECHO_MASK_C = 16'h000a;
	localparam [15:0] FLG_REG_FAILED_C = 16'h0040;
	localparam [1:0] GS_NO_DA_C = 2'd0;
	localparam [1:0] GS_DA_OK_C = 2'd1;
	localparam [1:0] GS_DECLARING_C = 2'd2;
	localparam [1:0] GS_BACKOFF_C = 2'd3;
	localparam [31:0] REC_W_C = 84;
	reg [83:0] rec_ram_r [0:N_STREAM_OUT_P - 1];
	reg [83:0] rec_q_r;
	reg rec_we_w;
	reg [SRC_W_C - 1:0] rec_waddr_w;
	reg [83:0] rec_wdata_w;
	reg rec_re_w;
	reg [SRC_W_C - 1:0] rec_raddr_w;
	always @(posedge clk_i) begin : rec_ram_write
		if (rec_we_w)
			rec_ram_r[rec_waddr_w] <= rec_wdata_w;
	end
	wire [83:0] rec_wdata_s;
	function automatic [83:0] sv2v_cast_84;
		input reg [83:0] inp;
		sv2v_cast_84 = inp;
	endfunction
	assign rec_wdata_s = sv2v_cast_84(rec_wdata_w);
	reg [N_STREAM_OUT_P - 1:0] declaring_r;
	always @(posedge clk_i) begin : declaring_mirror
		if (!rst_n)
			declaring_r <= 1'sb0;
		else if (rec_we_w)
			declaring_r[rec_waddr_w] <= rec_wdata_s[83-:2] == GS_DECLARING_C;
	end
	assign declaring_o = declaring_r;
	always @(posedge clk_i) begin : rec_ram_read
		if (rec_re_w)
			rec_q_r <= rec_ram_r[rec_raddr_w];
	end
	wire [83:0] rec_w;
	assign rec_w = sv2v_cast_84(rec_q_r);
	function automatic [31:0] sv2v_cast_32;
		input reg [31:0] inp;
		sv2v_cast_32 = inp;
	endfunction
	function automatic [1:0] src_iface_f;
		input reg [SRC_W_C - 1:0] s;
		src_iface_f = cfg_src_iface_i[sv2v_cast_32(s) * 2+:2];
	endfunction
	function automatic [63:0] src_sid_f;
		input reg [SRC_W_C - 1:0] s;
		src_sid_f = cfg_stream_id_i[sv2v_cast_32(s) * 64+:64];
	endfunction
	function automatic [1:0] sv2v_cast_2;
		input reg [1:0] inp;
		sv2v_cast_2 = inp;
	endfunction
	function automatic [1:0] lsn_state_f;
		input reg [SRC_W_C - 1:0] s;
		lsn_state_f = sv2v_cast_2(srp_lsn_reg_state_i[sv2v_cast_32(s) * 2+:2]);
	endfunction
	function automatic lsn_reg_f;
		input reg [SRC_W_C - 1:0] s;
		lsn_reg_f = lsn_state_f(s) != 2'd0;
	endfunction
	function automatic fresh_f;
		input reg [83:0] r;
		fresh_f = r[80] && ((now_ms_i - r[79-:32]) < DAFRESH_MS_P);
	endfunction
	function automatic signed [SRC_W_C - 1:0] sv2v_cast_14954_signed;
		input reg signed [SRC_W_C - 1:0] inp;
		sv2v_cast_14954_signed = inp;
	endfunction
	function automatic signed [31:0] sv2v_cast_32_signed;
		input reg signed [31:0] inp;
		sv2v_cast_32_signed = inp;
	endfunction
	function automatic [SRC_W_C - 1:0] ffs_f;
		input reg [N_STREAM_OUT_P - 1:0] v;
		begin
			ffs_f = 1'sb0;
			begin : sv2v_autoblock_1
				reg signed [31:0] i;
				for (i = sv2v_cast_32_signed(N_STREAM_OUT_P) - 1; i >= 0; i = i - 1)
					if (v[i])
						ffs_f = sv2v_cast_14954_signed(i);
			end
		end
	endfunction
	function automatic signed [RXA_W_C - 1:0] sv2v_cast_3BB6D_signed;
		input reg signed [RXA_W_C - 1:0] inp;
		sv2v_cast_3BB6D_signed = inp;
	endfunction
	function automatic [RXA_W_C - 1:0] pdu_off_f;
		input reg [3:0] ix;
		(* full_case, parallel_case *)
		case (ix)
			4'd0: pdu_off_f = sv2v_cast_3BB6D_signed(28);
			4'd1: pdu_off_f = sv2v_cast_3BB6D_signed(29);
			4'd2: pdu_off_f = sv2v_cast_3BB6D_signed(30);
			4'd3: pdu_off_f = sv2v_cast_3BB6D_signed(31);
			4'd4: pdu_off_f = sv2v_cast_3BB6D_signed(32);
			4'd5: pdu_off_f = sv2v_cast_3BB6D_signed(33);
			4'd6: pdu_off_f = sv2v_cast_3BB6D_signed(34);
			4'd7: pdu_off_f = sv2v_cast_3BB6D_signed(35);
			4'd8: pdu_off_f = sv2v_cast_3BB6D_signed(38);
			4'd9: pdu_off_f = sv2v_cast_3BB6D_signed(39);
			4'd10: pdu_off_f = sv2v_cast_3BB6D_signed(50);
			default: pdu_off_f = sv2v_cast_3BB6D_signed(51);
		endcase
	endfunction
	reg [N_STREAM_OUT_P - 1:0] pe_conflict_r;
	reg [N_STREAM_OUT_P - 1:0] pe_pcp_r;
	reg [N_STREAM_OUT_P - 1:0] pe_tmr_r;
	reg [N_STREAM_OUT_P - 1:0] pe_lsn_r;
	reg [N_STREAM_OUT_P - 1:0] pe_init_r;
	reg [N_STREAM_OUT_P - 1:0] pe_off_r;
	reg [N_STREAM_OUT_P - 1:0] pe_rel_r;
	reg [(N_STREAM_OUT_P * 2) - 1:0] lsn_q_r;
	reg [N_STREAM_OUT_P - 1:0] en_q_r;
	reg maap_busy_r;
	reg [SRC_W_C - 1:0] maap_src_r;
	reg maap_rel_r;
	reg [31:0] maap_t0_r;
	reg gp_valid_r;
	reg [SRC_W_C - 1:0] gp_src_r;
	reg [47:0] gp_da_r;
	localparam [31:0] MAAP_STALE_W_C = 2;
	reg [1:0] maap_stale_r;
	wire maap_stale_full_w;
	assign maap_stale_full_w = &maap_stale_r;
	wire maap_swallow_w;
	wire maap_rsp_live_w;
	wire maap_rsp_tmo_w;
	wire maap_accept_w;
	wire maap_avail_w;
	assign maap_avail_w = (!maap_busy_r && !gp_valid_r) && !maap_stale_full_w;
	wire exp_hit_w;
	wire [SRC_W_C - 1:0] exp_src_w;
	wire [31:0] exp_rel_w;
	assign exp_rel_w = {{32 - TMR_AW_C {1'b0}}, tmr_exp_slot_i} - TMR_SLOT_BASE_P;
	function automatic [7:0] sv2v_cast_4E301;
		input reg [7:0] inp;
		sv2v_cast_4E301 = inp;
	endfunction
	assign exp_hit_w = (tmr_exp_valid_i && (exp_rel_w < N_STREAM_OUT_P)) && (tmr_exp_owner_i == sv2v_cast_4E301(TMR_OWNER_BASE_P + exp_rel_w));
	assign exp_src_w = exp_rel_w[SRC_W_C - 1:0];
	assign maap_conflict_ack_o = maap_conflict_valid_i;
	reg [3:0] state_r;
	reg [2:0] ev_code_r;
	reg [SRC_W_C - 1:0] ev_src_r;
	reg [392:0] txn_r;
	reg [3:0] fetch_ix_r;
	reg [RXL_W_C - 1:0] slot_len_r;
	reg [63:0] pdu_leid_r;
	reg [15:0] pdu_luid_r;
	reg [15:0] pdu_flags_r;
	reg [31:0] arm_deadline_r;
	reg [SRC_W_C - 1:0] mreq_src_r;
	reg mreq_rel_r;
	reg [MTMO_W_C - 1:0] mreq_tmo_r;
	reg [SRC_W_C:0] init_ix_r;
	wire maap_tmo_w;
	function automatic [MTMO_W_C - 1:0] sv2v_cast_C0AA2;
		input reg [MTMO_W_C - 1:0] inp;
		sv2v_cast_C0AA2 = inp;
	endfunction
	assign maap_tmo_w = (state_r == 4'd10) && (mreq_tmo_r == sv2v_cast_C0AA2(MAAP_ACCEPT_CYC_P - 32'd1));
	assign maap_swallow_w = maap_rsp_valid_i && (maap_stale_r != {2 {1'sb0}});
	assign maap_rsp_live_w = (maap_rsp_valid_i && maap_busy_r) && !maap_swallow_w;
	assign maap_rsp_tmo_w = (maap_busy_r && !maap_rsp_live_w) && ((now_ms_i - maap_t0_r) >= MAAP_RSP_MS_P);
	assign maap_accept_w = (state_r == 4'd10) && maap_req_ready_i;
	reg [1:0] disp_kind_w;
	reg [2:0] disp_code_w;
	reg [SRC_W_C - 1:0] disp_src_w;
	always @(*) begin : dispatcher
		if (_sv2v_0)
			;
		disp_kind_w = 2'd0;
		disp_code_w = 3'd0;
		disp_src_w = 1'sb0;
		if (state_r == 4'd1) begin
			if (gp_valid_r) begin
				disp_kind_w = 2'd2;
				disp_code_w = 3'd0;
				disp_src_w = gp_src_r;
			end
			else if (txn_valid_i)
				disp_kind_w = 2'd1;
			else if (|pe_off_r) begin
				disp_kind_w = 2'd2;
				disp_code_w = 3'd1;
				disp_src_w = ffs_f(pe_off_r);
			end
			else if (|pe_conflict_r) begin
				disp_kind_w = 2'd2;
				disp_code_w = 3'd2;
				disp_src_w = ffs_f(pe_conflict_r);
			end
			else if (|pe_pcp_r) begin
				disp_kind_w = 2'd2;
				disp_code_w = 3'd3;
				disp_src_w = ffs_f(pe_pcp_r);
			end
			else if (|pe_tmr_r) begin
				disp_kind_w = 2'd2;
				disp_code_w = 3'd4;
				disp_src_w = ffs_f(pe_tmr_r);
			end
			else if (|pe_lsn_r) begin
				disp_kind_w = 2'd2;
				disp_code_w = 3'd5;
				disp_src_w = ffs_f(pe_lsn_r);
			end
			else if (|pe_rel_r) begin
				disp_kind_w = 2'd2;
				disp_code_w = 3'd7;
				disp_src_w = ffs_f(pe_rel_r);
			end
			else if (|pe_init_r) begin
				disp_kind_w = 2'd2;
				disp_code_w = 3'd6;
				disp_src_w = ffs_f(pe_init_r);
			end
		end
	end
	wire [392:0] txn_in_w;
	function automatic [392:0] sv2v_cast_393;
		input reg [392:0] inp;
		sv2v_cast_393 = inp;
	endfunction
	assign txn_in_w = sv2v_cast_393(txn_i);
	wire [15:0] uid16_w;
	wire [SRC_W_C - 1:0] tsrc_w;
	wire uid_valid_w;
	wire talker_cmd_w;
	wire iface_ok_w;
	wire ping_w;
	wire da_ok_w;
	wire slot_ok_w;
	wire needs_pdu_w;
	assign uid16_w = txn_r[75-:16];
	assign tsrc_w = uid16_w[SRC_W_C - 1:0];
	function automatic [15:0] sv2v_cast_16;
		input reg [15:0] inp;
		sv2v_cast_16 = inp;
	endfunction
	assign uid_valid_w = (uid16_w < sv2v_cast_16(N_STREAM_OUT_P)) && cfg_src_en_i[tsrc_w];
	assign talker_cmd_w = ((txn_r[356-:3] == 3'd1) && (txn_r[221-:64] == own_entity_id_i)) && ((((txn_r[353-:4] == MT_PROBE_TX_C) || (txn_r[353-:4] == MT_DISC_TX_C)) || (txn_r[353-:4] == MT_GTX_ST_C)) || (txn_r[353-:4] == MT_GTX_CN_C));
	assign iface_ok_w = src_iface_f(tsrc_w) == txn_r[390-:2];
	assign ping_w = ((talker_cmd_w && (txn_r[353-:4] == MT_PROBE_TX_C)) && uid_valid_w) && iface_ok_w;
	assign da_ok_w = rec_w[81] && !pe_conflict_r[tsrc_w];
	function automatic [2:0] sv2v_cast_3;
		input reg [2:0] inp;
		sv2v_cast_3 = inp;
	endfunction
	assign slot_ok_w = txn_r[59-:3] < sv2v_cast_3(RX_SLOTS_P);
	assign needs_pdu_w = (talker_cmd_w && slot_ok_w) && ((((txn_r[353-:4] == MT_PROBE_TX_C) && (!uid_valid_w || iface_ok_w)) || (txn_r[353-:4] == MT_DISC_TX_C)) || (txn_r[353-:4] == MT_GTX_CN_C));
	reg [83:0] txn_rec2_w;
	reg txn_open_w;
	reg txn_initset_w;
	always @(*) begin : txn_commit
		if (_sv2v_0)
			;
		txn_rec2_w = rec_w;
		txn_open_w = 1'b0;
		txn_initset_w = 1'b0;
		if (ping_w) begin
			txn_rec2_w[80] = 1'b1;
			txn_rec2_w[79-:32] = now_ms_i;
			if ((rec_w[83-:2] == GS_DA_OK_C) && da_ok_w) begin
				txn_rec2_w[83-:2] = GS_DECLARING_C;
				txn_open_w = 1'b1;
			end
			if (rec_w[83-:2] == GS_NO_DA_C)
				txn_initset_w = 1'b1;
		end
	end
	reg [83:0] ev_rec2_w;
	reg ev_we_w;
	reg ev_open_w;
	reg ev_close_w;
	reg ev_arm_fresh_w;
	reg ev_cancel_w;
	reg ev_initset_w;
	reg ev_relset_w;
	reg ev_to_draw_w;
	reg ev_to_maap_w;
	reg ev_maap_rel_w;
	reg ev_gate_w;
	reg ev_daok2_w;
	always @(maap_avail_w or rec_w[83-:2] or maap_avail_w or rec_w[83-:2] or ev_gate_w or rec_w[83-:2] or ev_gate_w or rec_w[83-:2] or ev_src_r or srp_lsn_reg_state_i or rec_w or now_ms_i or ev_daok2_w or ev_src_r or pe_conflict_r or rec_w[81] or ev_gate_w or rec_w[83-:2] or ev_src_r or srp_lsn_reg_state_i or rec_w or now_ms_i or ev_daok2_w or ev_src_r or pe_conflict_r or rec_w[81] or rec_w or now_ms_i or ev_gate_w or ev_src_r or srp_lsn_reg_state_i or rec_w or now_ms_i or ev_daok2_w or ev_src_r or pe_conflict_r or rec_w[81] or rec_w[83-:2] or rec_w[83-:2] or rec_w[83-:2] or rec_w[83-:2] or maap_avail_w or rec_w[81] or rec_w[81] or rec_w[83-:2] or ev_gate_w or ev_rec2_w[83-:2] or ev_src_r or srp_lsn_reg_state_i or ev_rec2_w or now_ms_i or ev_daok2_w or ev_src_r or pe_conflict_r or ev_rec2_w[81] or rec_w[83-:2] or gp_da_r or ev_code_r or rec_w or _sv2v_0) begin : ev_eval
		if (_sv2v_0)
			;
		ev_rec2_w = rec_w;
		ev_we_w = 1'b0;
		ev_open_w = 1'b0;
		ev_close_w = 1'b0;
		ev_arm_fresh_w = 1'b0;
		ev_cancel_w = 1'b0;
		ev_initset_w = 1'b0;
		ev_relset_w = 1'b0;
		ev_to_draw_w = 1'b0;
		ev_to_maap_w = 1'b0;
		ev_maap_rel_w = 1'b0;
		ev_daok2_w = 1'b0;
		ev_gate_w = 1'b0;
		(* full_case, parallel_case *)
		case (ev_code_r)
			3'd0: begin
				ev_rec2_w[47-:48] = gp_da_r;
				ev_rec2_w[81] = 1'b1;
				if (rec_w[83-:2] == GS_NO_DA_C)
					ev_rec2_w[83-:2] = GS_DA_OK_C;
				ev_we_w = 1'b1;
				ev_daok2_w = ev_rec2_w[81] && !pe_conflict_r[ev_src_r];
				ev_gate_w = ev_daok2_w && (fresh_f(ev_rec2_w) || lsn_reg_f(ev_src_r));
				if ((ev_rec2_w[83-:2] == GS_DA_OK_C) && ev_gate_w) begin
					ev_rec2_w[83-:2] = GS_DECLARING_C;
					ev_open_w = 1'b1;
				end
			end
			3'd1: begin
				if (rec_w[83-:2] == GS_DECLARING_C)
					ev_close_w = 1'b1;
				ev_rec2_w = {GS_NO_DA_C, 82'h000000000000000000000};
				ev_we_w = 1'b1;
				ev_cancel_w = 1'b1;
				ev_relset_w = rec_w[81];
				if (rec_w[81] && maap_avail_w) begin
					ev_to_maap_w = 1'b1;
					ev_maap_rel_w = 1'b1;
				end
			end
			3'd2: begin
				ev_rec2_w[81] = 1'b0;
				ev_we_w = 1'b1;
				if (rec_w[83-:2] == GS_DECLARING_C) begin
					ev_close_w = 1'b1;
					ev_rec2_w[83-:2] = GS_BACKOFF_C;
					ev_to_draw_w = 1'b1;
				end
				else if (rec_w[83-:2] == GS_DA_OK_C) begin
					ev_rec2_w[83-:2] = GS_NO_DA_C;
					ev_initset_w = 1'b1;
				end
			end
			3'd3:
				if (rec_w[83-:2] == GS_DECLARING_C) begin
					ev_close_w = 1'b1;
					ev_rec2_w[83-:2] = GS_BACKOFF_C;
					ev_we_w = 1'b1;
					ev_to_draw_w = 1'b1;
				end
			3'd4:
				if (rec_w[83-:2] == GS_BACKOFF_C) begin
					if (rec_w[81]) begin
						ev_rec2_w[83-:2] = GS_DA_OK_C;
						ev_we_w = 1'b1;
						ev_daok2_w = !pe_conflict_r[ev_src_r];
						ev_gate_w = ev_daok2_w && (fresh_f(rec_w) || lsn_reg_f(ev_src_r));
						if (ev_gate_w) begin
							ev_rec2_w[83-:2] = GS_DECLARING_C;
							ev_open_w = 1'b1;
						end
						if (fresh_f(rec_w))
							ev_arm_fresh_w = 1'b1;
					end
					else begin
						ev_rec2_w[83-:2] = GS_NO_DA_C;
						ev_we_w = 1'b1;
						ev_initset_w = 1'b1;
					end
				end
				else begin
					ev_daok2_w = rec_w[81] && !pe_conflict_r[ev_src_r];
					ev_gate_w = ev_daok2_w && (fresh_f(rec_w) || lsn_reg_f(ev_src_r));
					if ((rec_w[83-:2] == GS_DECLARING_C) && !ev_gate_w) begin
						ev_close_w = 1'b1;
						ev_rec2_w[83-:2] = GS_DA_OK_C;
						ev_we_w = 1'b1;
					end
				end
			3'd5: begin
				ev_daok2_w = rec_w[81] && !pe_conflict_r[ev_src_r];
				ev_gate_w = ev_daok2_w && (fresh_f(rec_w) || lsn_reg_f(ev_src_r));
				if ((rec_w[83-:2] == GS_DA_OK_C) && ev_gate_w) begin
					ev_rec2_w[83-:2] = GS_DECLARING_C;
					ev_open_w = 1'b1;
					ev_we_w = 1'b1;
				end
				else if ((rec_w[83-:2] == GS_DECLARING_C) && !ev_gate_w) begin
					ev_rec2_w[83-:2] = GS_DA_OK_C;
					ev_close_w = 1'b1;
					ev_we_w = 1'b1;
				end
				else if (rec_w[83-:2] == GS_NO_DA_C)
					ev_initset_w = 1'b1;
			end
			3'd7:
				if (maap_avail_w) begin
					ev_to_maap_w = 1'b1;
					ev_maap_rel_w = 1'b1;
				end
			default:
				if (rec_w[83-:2] == GS_NO_DA_C) begin
					if (maap_avail_w)
						ev_to_maap_w = 1'b1;
					else
						ev_initset_w = 1'b1;
				end
		endcase
	end
	function automatic [((SRC_W_C + 0) >= 0 ? SRC_W_C + 1 : 1 - (SRC_W_C + 0)) - 1:0] sv2v_cast_13314;
		input reg [((SRC_W_C + 0) >= 0 ? SRC_W_C + 1 : 1 - (SRC_W_C + 0)) - 1:0] inp;
		sv2v_cast_13314 = inp;
	endfunction
	function automatic signed [((SRC_W_C + 0) >= 0 ? SRC_W_C + 1 : 1 - (SRC_W_C + 0)) - 1:0] sv2v_cast_13314_signed;
		input reg signed [((SRC_W_C + 0) >= 0 ? SRC_W_C + 1 : 1 - (SRC_W_C + 0)) - 1:0] inp;
		sv2v_cast_13314_signed = inp;
	endfunction
	function automatic signed [MTMO_W_C - 1:0] sv2v_cast_C0AA2_signed;
		input reg signed [MTMO_W_C - 1:0] inp;
		sv2v_cast_C0AA2_signed = inp;
	endfunction
	always @(posedge clk_i) begin : walker
		if (!rst_n) begin
			state_r <= 4'd0;
			ev_code_r <= 3'd0;
			ev_src_r <= 1'sb0;
			txn_r <= sv2v_cast_393({pp_pkg_PP_TXN_W_C {1'b0}});
			fetch_ix_r <= 4'd0;
			slot_len_r <= 1'sb0;
			pdu_leid_r <= 64'd0;
			pdu_luid_r <= 16'd0;
			pdu_flags_r <= 16'd0;
			arm_deadline_r <= 32'd0;
			mreq_src_r <= 1'sb0;
			mreq_rel_r <= 1'b0;
			mreq_tmo_r <= 1'sb0;
			init_ix_r <= 1'sb0;
		end
		else
			(* full_case, parallel_case *)
			case (state_r)
				4'd0: begin
					if (init_ix_r == sv2v_cast_13314(N_STREAM_OUT_P - 32'd1))
						state_r <= 4'd1;
					init_ix_r <= init_ix_r + sv2v_cast_13314_signed(1);
				end
				4'd1:
					if (disp_kind_w == 2'd1) begin
						txn_r <= sv2v_cast_393(txn_i);
						pdu_leid_r <= 64'd0;
						pdu_luid_r <= 16'd0;
						pdu_flags_r <= 16'd0;
						fetch_ix_r <= 4'd0;
						state_r <= 4'd2;
					end
					else if (disp_kind_w == 2'd2) begin
						ev_code_r <= disp_code_w;
						ev_src_r <= disp_src_w;
						state_r <= 4'd5;
					end
				4'd2: state_r <= (needs_pdu_w ? 4'd3 : 4'd4);
				4'd3: begin
					if (fetch_ix_r == 4'd0)
						slot_len_r <= rxs_slot_len_i;
					if (fetch_ix_r != 4'd0) begin : capture
						reg [7:0] byte_w;
						byte_w = ({{RXL_W_C - RXA_W_C {1'b0}}, pdu_off_f(fetch_ix_r - 4'd1)} < slot_len_r ? rxs_rd_data_i : 8'h00);
						(* full_case, parallel_case *)
						case (fetch_ix_r)
							4'd1: pdu_leid_r[63:56] <= byte_w;
							4'd2: pdu_leid_r[55:48] <= byte_w;
							4'd3: pdu_leid_r[47:40] <= byte_w;
							4'd4: pdu_leid_r[39:32] <= byte_w;
							4'd5: pdu_leid_r[31:24] <= byte_w;
							4'd6: pdu_leid_r[23:16] <= byte_w;
							4'd7: pdu_leid_r[15:8] <= byte_w;
							4'd8: pdu_leid_r[7:0] <= byte_w;
							4'd9: pdu_luid_r[15:8] <= byte_w;
							4'd10: pdu_luid_r[7:0] <= byte_w;
							4'd11: pdu_flags_r[15:8] <= byte_w;
							default: pdu_flags_r[7:0] <= byte_w;
						endcase
					end
					if (fetch_ix_r == 4'd12)
						state_r <= 4'd4;
					else
						fetch_ix_r <= fetch_ix_r + 4'd1;
				end
				4'd4: state_r <= 4'd1;
				4'd5: state_r <= 4'd6;
				4'd6:
					if (ev_to_draw_w)
						state_r <= 4'd7;
					else if (ev_to_maap_w) begin
						mreq_src_r <= ev_src_r;
						mreq_rel_r <= ev_maap_rel_w;
						mreq_tmo_r <= 1'sb0;
						state_r <= 4'd10;
					end
					else
						state_r <= 4'd1;
				4'd7:
					if (!prng_draw_busy_i)
						state_r <= 4'd8;
				4'd8:
					if (prng_draw_valid_i) begin
						arm_deadline_r <= now_ms_i + {15'd0, prng_draw_ms_i, 1'b0};
						state_r <= 4'd9;
					end
				4'd9: state_r <= 4'd1;
				default: begin
					mreq_tmo_r <= mreq_tmo_r + sv2v_cast_C0AA2_signed(1);
					if (maap_req_ready_i || maap_tmo_w)
						state_r <= 4'd1;
				end
			endcase
	end
	function automatic signed [1:0] sv2v_cast_4138B_signed;
		input reg signed [1:0] inp;
		sv2v_cast_4138B_signed = inp;
	endfunction
	always @(posedge clk_i) begin : maap_track
		if (!rst_n) begin
			maap_busy_r <= 1'b0;
			maap_src_r <= 1'sb0;
			maap_rel_r <= 1'b0;
			maap_t0_r <= 32'd0;
			maap_stale_r <= 1'sb0;
			gp_valid_r <= 1'b0;
			gp_src_r <= 1'sb0;
			gp_da_r <= 48'd0;
		end
		else begin
			if (maap_accept_w) begin
				maap_busy_r <= 1'b1;
				maap_src_r <= mreq_src_r;
				maap_rel_r <= mreq_rel_r;
				maap_t0_r <= now_ms_i;
			end
			else if (maap_rsp_live_w || maap_rsp_tmo_w)
				maap_busy_r <= 1'b0;
			if ((maap_rsp_live_w && !maap_rel_r) && maap_rsp_ok_i) begin
				gp_valid_r <= 1'b1;
				gp_src_r <= maap_src_r;
				gp_da_r <= maap_rsp_da_i;
			end
			if (maap_rsp_tmo_w && !maap_swallow_w)
				maap_stale_r <= maap_stale_r + sv2v_cast_4138B_signed(1);
			else if (maap_swallow_w && !maap_rsp_tmo_w)
				maap_stale_r <= maap_stale_r - sv2v_cast_4138B_signed(1);
			if ((state_r == 4'd6) && (ev_code_r == 3'd0))
				gp_valid_r <= 1'b0;
		end
	end
	reg [N_STREAM_OUT_P - 1:0] set_conflict_w;
	reg [N_STREAM_OUT_P - 1:0] set_pcp_w;
	reg [N_STREAM_OUT_P - 1:0] set_tmr_w;
	reg [N_STREAM_OUT_P - 1:0] set_lsn_w;
	reg [N_STREAM_OUT_P - 1:0] set_init_w;
	reg [N_STREAM_OUT_P - 1:0] set_off_w;
	reg [N_STREAM_OUT_P - 1:0] set_rel_w;
	reg [N_STREAM_OUT_P - 1:0] clr_disp_w;
	reg [N_STREAM_OUT_P - 1:0] clr_relq_w;
	reg [N_STREAM_OUT_P - 1:0] clr_arm_w;
	wire [31:0] arm_rel_w;
	always @(*) begin : pe_sets
		if (_sv2v_0)
			;
		set_conflict_w = 1'sb0;
		set_pcp_w = 1'sb0;
		set_tmr_w = 1'sb0;
		set_lsn_w = 1'sb0;
		set_init_w = 1'sb0;
		set_off_w = 1'sb0;
		set_rel_w = 1'sb0;
		clr_disp_w = 1'sb0;
		clr_relq_w = 1'sb0;
		if (maap_conflict_valid_i)
			set_conflict_w[maap_conflict_src_i] = 1'b1;
		if (srp_pcp_change_i)
			set_pcp_w = cfg_src_en_i;
		if (exp_hit_w)
			set_tmr_w[exp_src_w] = 1'b1;
		begin : sv2v_autoblock_2
			reg signed [31:0] i;
			for (i = 0; i < sv2v_cast_32_signed(N_STREAM_OUT_P); i = i + 1)
				begin
					if (srp_lsn_reg_state_i[i * 2+:2] != lsn_q_r[i * 2+:2])
						set_lsn_w[i] = 1'b1;
					if (cfg_src_en_i[i] && !en_q_r[i])
						set_init_w[i] = 1'b1;
					if (!cfg_src_en_i[i] && en_q_r[i])
						set_off_w[i] = 1'b1;
				end
		end
		if ((state_r == 4'd4) && txn_initset_w)
			set_init_w[tsrc_w] = 1'b1;
		if ((state_r == 4'd6) && ev_initset_w)
			set_init_w[ev_src_r] = 1'b1;
		if ((state_r == 4'd6) && ev_relset_w)
			set_rel_w[ev_src_r] = 1'b1;
		if (maap_accept_w && mreq_rel_r)
			clr_relq_w[mreq_src_r] = 1'b1;
		if ((state_r == 4'd1) && (disp_kind_w == 2'd2))
			clr_disp_w[disp_src_w] = 1'b1;
	end
	assign arm_rel_w = {{32 - TMR_AW_C {1'b0}}, tmr_arm_slot_o} - TMR_SLOT_BASE_P;
	always @(*) begin : arm_clr
		if (_sv2v_0)
			;
		clr_arm_w = 1'sb0;
		if (tmr_arm_valid_o && (arm_rel_w < N_STREAM_OUT_P))
			clr_arm_w[arm_rel_w[SRC_W_C - 1:0]] = 1'b1;
	end
	always @(posedge clk_i) begin : pe_flags
		if (!rst_n) begin
			pe_conflict_r <= 1'sb0;
			pe_pcp_r <= 1'sb0;
			pe_tmr_r <= 1'sb0;
			pe_lsn_r <= 1'sb0;
			pe_init_r <= 1'sb0;
			pe_off_r <= 1'sb0;
			pe_rel_r <= 1'sb0;
			lsn_q_r <= 1'sb0;
			en_q_r <= 1'sb0;
		end
		else begin
			pe_conflict_r <= (pe_conflict_r & ~(disp_code_w == 3'd2 ? clr_disp_w : {N_STREAM_OUT_P {1'sb0}})) | set_conflict_w;
			pe_pcp_r <= (pe_pcp_r & ~(disp_code_w == 3'd3 ? clr_disp_w : {N_STREAM_OUT_P {1'sb0}})) | set_pcp_w;
			pe_tmr_r <= ((pe_tmr_r & ~(disp_code_w == 3'd4 ? clr_disp_w : {N_STREAM_OUT_P {1'sb0}})) & ~clr_arm_w) | set_tmr_w;
			pe_lsn_r <= (pe_lsn_r & ~(disp_code_w == 3'd5 ? clr_disp_w : {N_STREAM_OUT_P {1'sb0}})) | set_lsn_w;
			pe_init_r <= (pe_init_r & ~(disp_code_w == 3'd6 ? clr_disp_w : {N_STREAM_OUT_P {1'sb0}})) | set_init_w;
			pe_off_r <= (pe_off_r & ~(disp_code_w == 3'd1 ? clr_disp_w : {N_STREAM_OUT_P {1'sb0}})) | set_off_w;
			pe_rel_r <= (pe_rel_r & ~clr_relq_w) | set_rel_w;
			lsn_q_r <= srp_lsn_reg_state_i;
			en_q_r <= cfg_src_en_i;
		end
	end
	function automatic [83:0] sv2v_cast_33ED2;
		input reg [83:0] inp;
		sv2v_cast_33ED2 = inp;
	endfunction
	always @(*) begin : rec_ports
		if (_sv2v_0)
			;
		rec_re_w = 1'b0;
		rec_raddr_w = 1'sb0;
		rec_we_w = 1'b0;
		rec_waddr_w = 1'sb0;
		rec_wdata_w = 1'sb0;
		if (state_r == 4'd0) begin
			rec_we_w = 1'b1;
			rec_waddr_w = init_ix_r[SRC_W_C - 1:0];
			rec_wdata_w = sv2v_cast_33ED2({GS_NO_DA_C, 82'h000000000000000000000});
		end
		else if (state_r == 4'd1) begin
			if (disp_kind_w == 2'd1) begin
				rec_re_w = 1'b1;
				rec_raddr_w = txn_in_w[SRC_W_C + 59:60];
			end
			else if (disp_kind_w == 2'd2) begin
				rec_re_w = 1'b1;
				rec_raddr_w = disp_src_w;
			end
		end
		else if (state_r == 4'd4) begin
			if (ping_w) begin
				rec_we_w = 1'b1;
				rec_waddr_w = tsrc_w;
				rec_wdata_w = sv2v_cast_33ED2(txn_rec2_w);
			end
		end
		else if (state_r == 4'd6) begin
			if (ev_we_w) begin
				rec_we_w = 1'b1;
				rec_waddr_w = ev_src_r;
				rec_wdata_w = sv2v_cast_33ED2(ev_rec2_w);
			end
		end
	end
	wire rf_live_w;
	assign rf_live_w = lsn_state_f(tsrc_w) == 2'd1;
	always @(pdu_luid_r or pdu_leid_r or srp_class_vid_i or rec_w[47-:48] or da_ok_w or tsrc_w or cfg_stream_id_i or rf_live_w or uid_valid_w or pdu_luid_r or pdu_leid_r or srp_class_vid_i or rec_w[47-:48] or tsrc_w or cfg_stream_id_i or da_ok_w or pdu_flags_r or pdu_luid_r or pdu_leid_r or iface_ok_w or pdu_flags_r or pdu_luid_r or pdu_leid_r or uid_valid_w or txn_r[353-:4] or txn_r[390-:2] or txn_r[157-:16] or uid16_w or own_entity_id_i or txn_r[285-:64] or txn_r[353-:4] or talker_cmd_w or state_r or _sv2v_0) begin : respond
		if (_sv2v_0)
			;
		resp_valid_o = 1'b0;
		resp_msg_type_o = 4'd0;
		resp_status_o = ST_SUCCESS_C;
		resp_stream_id_o = 64'd0;
		resp_controller_eid_o = 64'd0;
		resp_talker_eid_o = 64'd0;
		resp_listener_eid_o = 64'd0;
		resp_talker_uid_o = 16'd0;
		resp_listener_uid_o = 16'd0;
		resp_dest_mac_o = 48'd0;
		resp_conn_count_o = 16'd0;
		resp_seq_id_o = 16'd0;
		resp_flags_o = 16'd0;
		resp_vlan_id_o = 16'd0;
		resp_if_index_o = 2'd0;
		if ((state_r == 4'd4) && talker_cmd_w) begin
			resp_msg_type_o = txn_r[353-:4] | 4'd1;
			resp_controller_eid_o = txn_r[285-:64];
			resp_talker_eid_o = own_entity_id_i;
			resp_talker_uid_o = uid16_w;
			resp_seq_id_o = txn_r[157-:16];
			resp_if_index_o = txn_r[390-:2];
			(* full_case, parallel_case *)
			case (txn_r[353-:4])
				MT_PROBE_TX_C:
					if (!uid_valid_w) begin
						resp_valid_o = 1'b1;
						resp_status_o = ST_TALKER_UNKNOWN_C;
						resp_listener_eid_o = pdu_leid_r;
						resp_listener_uid_o = pdu_luid_r;
						resp_flags_o = pdu_flags_r & FLG_ECHO_MASK_C;
					end
					else if (iface_ok_w) begin
						resp_valid_o = 1'b1;
						resp_listener_eid_o = pdu_leid_r;
						resp_listener_uid_o = pdu_luid_r;
						resp_flags_o = pdu_flags_r & FLG_ECHO_MASK_C;
						if (da_ok_w) begin
							resp_status_o = ST_SUCCESS_C;
							resp_stream_id_o = src_sid_f(tsrc_w);
							resp_dest_mac_o = rec_w[47-:48];
							resp_vlan_id_o = {4'd0, srp_class_vid_i};
						end
						else
							resp_status_o = ST_DEST_MAC_FAIL_C;
					end
				MT_DISC_TX_C: begin
					resp_valid_o = 1'b1;
					resp_status_o = ST_SUCCESS_C;
					resp_listener_eid_o = pdu_leid_r;
					resp_listener_uid_o = pdu_luid_r;
				end
				MT_GTX_ST_C: begin
					resp_valid_o = 1'b1;
					if (uid_valid_w) begin
						resp_status_o = ST_SUCCESS_C;
						resp_flags_o = (rf_live_w ? FLG_REG_FAILED_C : 16'd0);
						resp_stream_id_o = src_sid_f(tsrc_w);
						resp_dest_mac_o = (da_ok_w ? rec_w[47-:48] : 48'd0);
						resp_vlan_id_o = {4'd0, srp_class_vid_i};
					end
					else
						resp_status_o = ST_TALKER_UNKNOWN_C;
				end
				default: begin
					resp_valid_o = 1'b1;
					resp_status_o = ST_NOT_SUPPORTED_C;
					resp_listener_eid_o = pdu_leid_r;
					resp_listener_uid_o = pdu_luid_r;
				end
			endcase
		end
	end
	always @(srp_class_vid_i or ev_rec2_w[47-:48] or ev_src_r or cfg_stream_id_i or ev_src_r or ev_close_w or ev_open_w or state_r or srp_class_vid_i or rec_w[47-:48] or tsrc_w or cfg_stream_id_i or tsrc_w or txn_open_w or state_r or _sv2v_0) begin : gate_face
		if (_sv2v_0)
			;
		gate_open_o = 1'b0;
		gate_close_o = 1'b0;
		gate_src_o = 1'sb0;
		gate_stream_id_o = 64'd0;
		gate_da_o = 48'd0;
		gate_vlan_o = 12'd0;
		if (state_r == 4'd4) begin
			gate_open_o = txn_open_w;
			gate_src_o = tsrc_w;
			gate_stream_id_o = src_sid_f(tsrc_w);
			gate_da_o = rec_w[47-:48];
			gate_vlan_o = srp_class_vid_i;
		end
		else if (state_r == 4'd6) begin
			gate_open_o = ev_open_w;
			gate_close_o = ev_close_w;
			gate_src_o = ev_src_r;
			gate_stream_id_o = src_sid_f(ev_src_r);
			gate_da_o = ev_rec2_w[47-:48];
			gate_vlan_o = srp_class_vid_i;
		end
	end
	function automatic [TMR_AW_C - 1:0] sv2v_cast_5A563;
		input reg [TMR_AW_C - 1:0] inp;
		sv2v_cast_5A563 = inp;
	endfunction
	always @(*) begin : timer_face
		if (_sv2v_0)
			;
		tmr_arm_valid_o = 1'b0;
		tmr_arm_cancel_o = 1'b0;
		tmr_arm_slot_o = 1'sb0;
		tmr_arm_owner_o = 1'sb0;
		tmr_arm_deadline_ms_o = 32'd0;
		if (((state_r == 4'd4) && ping_w) && (rec_w[83-:2] != GS_BACKOFF_C)) begin
			tmr_arm_valid_o = 1'b1;
			tmr_arm_slot_o = sv2v_cast_5A563(TMR_SLOT_BASE_P + sv2v_cast_32(tsrc_w));
			tmr_arm_owner_o = sv2v_cast_4E301(TMR_OWNER_BASE_P + sv2v_cast_32(tsrc_w));
			tmr_arm_deadline_ms_o = now_ms_i + DAFRESH_MS_P;
		end
		else if (state_r == 4'd6) begin
			if (ev_arm_fresh_w) begin
				tmr_arm_valid_o = 1'b1;
				tmr_arm_slot_o = sv2v_cast_5A563(TMR_SLOT_BASE_P + sv2v_cast_32(ev_src_r));
				tmr_arm_owner_o = sv2v_cast_4E301(TMR_OWNER_BASE_P + sv2v_cast_32(ev_src_r));
				tmr_arm_deadline_ms_o = rec_w[79-:32] + DAFRESH_MS_P;
			end
			else if (ev_cancel_w) begin
				tmr_arm_valid_o = 1'b1;
				tmr_arm_cancel_o = 1'b1;
				tmr_arm_slot_o = sv2v_cast_5A563(TMR_SLOT_BASE_P + sv2v_cast_32(ev_src_r));
				tmr_arm_owner_o = sv2v_cast_4E301(TMR_OWNER_BASE_P + sv2v_cast_32(ev_src_r));
			end
		end
		else if (state_r == 4'd9) begin
			tmr_arm_valid_o = 1'b1;
			tmr_arm_slot_o = sv2v_cast_5A563(TMR_SLOT_BASE_P + sv2v_cast_32(ev_src_r));
			tmr_arm_owner_o = sv2v_cast_4E301(TMR_OWNER_BASE_P + sv2v_cast_32(ev_src_r));
			tmr_arm_deadline_ms_o = arm_deadline_r;
		end
	end
	assign rxs_rd_slot_o = txn_r[56 + RXS_W_C:57];
	assign rxs_rd_addr_o = pdu_off_f(fetch_ix_r);
	assign rxs_rd_en_o = (state_r == 4'd3) && (fetch_ix_r != 4'd12);
	assign rxs_free_o = (state_r == 4'd4) && slot_ok_w;
	assign rxs_free_slot_o = txn_r[56 + RXS_W_C:57];
	assign txn_ready_o = (state_r == 4'd1) && !gp_valid_r;
	assign maap_req_valid_o = state_r == 4'd10;
	assign maap_req_release_o = mreq_rel_r;
	assign maap_req_src_o = mreq_src_r;
	assign prng_draw_req_o = (state_r == 4'd7) && !prng_draw_busy_i;
	assign prng_draw_kind_o = 3'd3;
	initial _sv2v_0 = 0;
endmodule
`default_nettype wire
`default_nettype none
module KL_pp_acmp_listener (
	clk_i,
	rst_n,
	entity_id_i,
	txn_valid_i,
	txn_i,
	txn_ready_o,
	evt_tk_valid_i,
	evt_tk_kind_i,
	evt_tk_failed_i,
	evt_tk_sink_i,
	evt_tk_ready_o,
	pre_valid_i,
	pre_sink_i,
	pre_talker_eid_i,
	pre_talker_uid_i,
	pre_ctlr_eid_i,
	pre_sw_i,
	pre_started_i,
	pre_ready_o,
	strm_set_valid_i,
	strm_set_sink_i,
	strm_set_val_i,
	strm_set_ready_o,
	strm_set_error_o,
	strm_started_o,
	now_ms_i,
	tmr_arm_valid_o,
	tmr_arm_cancel_o,
	tmr_arm_slot_o,
	tmr_arm_owner_o,
	tmr_arm_deadline_ms_o,
	tmr_exp_valid_i,
	tmr_exp_slot_i,
	tmr_exp_owner_i,
	draw_req_o,
	draw_kind_o,
	draw_busy_i,
	draw_valid_i,
	draw_ms_i,
	rxs_rd_slot_o,
	rxs_rd_addr_o,
	rxs_rd_en_o,
	rxs_rd_data_i,
	rxs_free_o,
	rxs_free_slot_o,
	txs_alloc_req_o,
	txs_oversize_o,
	txs_alloc_gnt_i,
	txs_alloc_slot_i,
	txs_wr_slot_o,
	txs_wr_addr_o,
	txs_wr_valid_o,
	txs_wr_data_o,
	txs_wr_commit_o,
	txs_wr_len_o,
	txreq_valid_o,
	txreq_slot_o,
	lock_held_i,
	lock_ctlr_i,
	act_settle_o,
	act_settle_sid_o,
	act_settle_da_o,
	act_settle_vlan_o,
	act_teardown_o,
	act_disc_arm_o,
	act_disc_talker_eid_o,
	act_disc_disarm_o,
	act_nvm_o,
	act_nvm_set_o,
	act_notify_o,
	act_sink_o,
	dbg_busy_o,
	dbg_strq_drop_o,
	act_strt_chg_o,
	act_strt_cmd_chg_o,
	dbg_recwr_o,
	dbg_recwr_sink_o,
	dbg_recwr_rec_o
);
	reg _sv2v_0;
	parameter [31:0] N_SINKS_P = 8;
	parameter TROM_HEX_P = "ltn_rom.hex";
	parameter [31:0] RX_SLOTS_P = 4;
	parameter [31:0] RX_SLOT_BYTES_P = 576;
	parameter [31:0] TX_STD_SLOTS_P = 4;
	parameter [31:0] TX_OVERSIZE_BYTES_P = 1600;
	parameter [31:0] TMR_SLOT_AW_P = 7;
	parameter [31:0] TMR_BASE_SLOT_P = 9;
	parameter [31:0] TMR_OWNER_BASE_P = 32;
	parameter [31:0] STRM_TIMEOUT_CYC_P = 4096;
	localparam [31:0] SINK_W_C = (N_SINKS_P > 1 ? $clog2(N_SINKS_P) : 1);
	localparam [31:0] RXS_SLOT_W_C = (RX_SLOTS_P > 1 ? $clog2(RX_SLOTS_P) : 1);
	localparam [31:0] RXS_ADDR_W_C = $clog2(RX_SLOT_BYTES_P);
	localparam [31:0] TXS_SLOT_W_C = $clog2(TX_STD_SLOTS_P + 1);
	localparam [31:0] TXS_LEN_W_C = $clog2(TX_OVERSIZE_BYTES_P + 1);
	input wire clk_i;
	input wire rst_n;
	input wire [63:0] entity_id_i;
	input wire txn_valid_i;
	input wire [392:0] txn_i;
	output wire txn_ready_o;
	input wire evt_tk_valid_i;
	input wire [1:0] evt_tk_kind_i;
	input wire evt_tk_failed_i;
	input wire [15:0] evt_tk_sink_i;
	output wire evt_tk_ready_o;
	input wire pre_valid_i;
	input wire [15:0] pre_sink_i;
	input wire [63:0] pre_talker_eid_i;
	input wire [15:0] pre_talker_uid_i;
	input wire [63:0] pre_ctlr_eid_i;
	input wire pre_sw_i;
	input wire pre_started_i;
	output wire pre_ready_o;
	input wire strm_set_valid_i;
	input wire [15:0] strm_set_sink_i;
	input wire strm_set_val_i;
	output wire strm_set_ready_o;
	output wire strm_set_error_o;
	output reg [N_SINKS_P - 1:0] strm_started_o;
	input wire [31:0] now_ms_i;
	output reg tmr_arm_valid_o;
	output reg tmr_arm_cancel_o;
	output reg [TMR_SLOT_AW_P - 1:0] tmr_arm_slot_o;
	localparam [31:0] pp_pkg_PP_TIMER_OWNER_W_C = 8;
	output reg [7:0] tmr_arm_owner_o;
	output reg [31:0] tmr_arm_deadline_ms_o;
	input wire tmr_exp_valid_i;
	input wire [TMR_SLOT_AW_P - 1:0] tmr_exp_slot_i;
	input wire [7:0] tmr_exp_owner_i;
	output reg draw_req_o;
	output wire [2:0] draw_kind_o;
	input wire draw_busy_i;
	input wire draw_valid_i;
	input wire [15:0] draw_ms_i;
	output wire [RXS_SLOT_W_C - 1:0] rxs_rd_slot_o;
	output wire [RXS_ADDR_W_C - 1:0] rxs_rd_addr_o;
	output wire rxs_rd_en_o;
	input wire [7:0] rxs_rd_data_i;
	output reg rxs_free_o;
	output wire [RXS_SLOT_W_C - 1:0] rxs_free_slot_o;
	output reg txs_alloc_req_o;
	output wire txs_oversize_o;
	input wire txs_alloc_gnt_i;
	input wire [TXS_SLOT_W_C - 1:0] txs_alloc_slot_i;
	output wire [TXS_SLOT_W_C - 1:0] txs_wr_slot_o;
	output reg [TXS_LEN_W_C - 1:0] txs_wr_addr_o;
	output reg txs_wr_valid_o;
	output reg [7:0] txs_wr_data_o;
	output reg txs_wr_commit_o;
	output reg [TXS_LEN_W_C - 1:0] txs_wr_len_o;
	output reg txreq_valid_o;
	output wire [TXS_SLOT_W_C - 1:0] txreq_slot_o;
	input wire lock_held_i;
	input wire [63:0] lock_ctlr_i;
	output reg act_settle_o;
	output wire [63:0] act_settle_sid_o;
	output wire [47:0] act_settle_da_o;
	output wire [11:0] act_settle_vlan_o;
	output reg act_teardown_o;
	output reg act_disc_arm_o;
	output reg [63:0] act_disc_talker_eid_o;
	output reg act_disc_disarm_o;
	output reg act_nvm_o;
	output reg act_nvm_set_o;
	output reg act_notify_o;
	output wire [SINK_W_C - 1:0] act_sink_o;
	output wire dbg_busy_o;
	output wire [15:0] dbg_strq_drop_o;
	output reg act_strt_chg_o;
	output reg act_strt_cmd_chg_o;
	output wire dbg_recwr_o;
	output wire [SINK_W_C - 1:0] dbg_recwr_sink_o;
	localparam [31:0] pp_acmp_pkg_ACMP_REC_W_C = 384;
	output wire [383:0] dbg_recwr_rec_o;
	reg [4:0] xs_r;
	reg [SINK_W_C:0] init_cnt_r;
	reg src_txn_r;
	reg src_tmr_r;
	reg src_strq_r;
	reg [3:0] msg_x_r;
	reg [4:0] status_x_r;
	reg [63:0] ctlr_x_r;
	reg [15:0] seq_x_r;
	reg [15:0] uid16_r;
	reg [2:0] rxslot_r;
	reg [SINK_W_C - 1:0] sink_r;
	reg [1:0] tkkind_r;
	reg tkfail_r;
	reg errflow_r;
	reg [63:0] preL_talker_eid_r;
	reg [15:0] preL_talker_uid_r;
	reg [63:0] preL_ctlr_eid_r;
	reg preL_sw_r;
	reg preL_started_r;
	reg strtL_val_r;
	reg strq_pend_r;
	reg strq_busy_r;
	reg strq_done_r;
	reg strq_fail_r;
	localparam [31:0] STRQ_TMO_W_C = $clog2(STRM_TIMEOUT_CYC_P + 1);
	reg [STRQ_TMO_W_C - 1:0] strq_tmo_r;
	reg [15:0] strq_sink_r;
	reg strq_val_r;
	reg [15:0] dbg_strq_drop_r;
	reg strt_was_r;
	reg bnd_was_r;
	reg bind_act_r;
	initial begin : parameter_checks
		if (STRM_TIMEOUT_CYC_P == 0) begin
			$display("Fatal [%0t] $VALIDATION_STORAGE/reviews/r247-520-r1/protocol-processor/hdl/acmp/KL_pp_acmp_listener.sv:347:7 - KL_pp_acmp_listener.parameter_checks.<unnamed_block>\n msg: ", $time, "STRM_TIMEOUT_CYC_P must be greater than zero");
			$finish(1);
		end
	end
	reg [63:0] tk_eid_f_r;
	reg [15:0] tk_uid_f_r;
	reg [15:0] flags_f_r;
	reg [63:0] sid_f_r;
	reg [47:0] da_f_r;
	reg [15:0] vlan_f_r;
	reg [4:0] f_idx_r;
	reg [4:0] f_cap_idx_r;
	reg f_cap_v_r;
	reg [383:0] rec_r;
	reg [3:0] evt_r;
	reg [16:0] apend_r;
	reg [4:0] ord_r;
	reg cellmut_r;
	reg [2:0] bk_r;
	reg [3:0] bmsg_r;
	reg [4:0] bstat_r;
	reg [5:0] bidx_r;
	reg bwait_r;
	reg [TXS_SLOT_W_C - 1:0] bslot_r;
	reg [15:0] probe_ctr_r;
	reg draw_issued_r;
	reg [N_SINKS_P - 1:0] pendexp_r;
	reg [383:0] rec_ram_r [0:N_SINKS_P - 1];
	reg [383:0] rec_rdata_r;
	wire [383:0] rec_rd_w;
	wire [383:0] recwr_rec_w;
	wire recwr_en_w;
	wire [SINK_W_C - 1:0] recwr_addr_w;
	wire [383:0] recwr_data_w;
	reg [383:0] pre_rec_w;
	reg [383:0] wb_rec_w;
	always @(posedge clk_i) begin : rec_ram_wr
		if (recwr_en_w)
			rec_ram_r[recwr_addr_w] <= recwr_data_w;
	end
	always @(posedge clk_i) begin : rec_ram_rd
		rec_rdata_r <= rec_ram_r[sink_r];
	end
	localparam [31:0] pp_acmp_pkg_TROM_DEPTH_C = 128;
	localparam [31:0] pp_acmp_pkg_TROM_W_C = 32;
	reg [31:0] trom_r [0:127];
	reg [31:0] trom_rdata_r;
	reg [3:0] evt_w;
	wire probe_match_w;
	initial $readmemh(TROM_HEX_P, trom_r);
	always @(posedge clk_i) begin : trom_rd
		trom_rdata_r <= trom_r[{evt_w, rec_r[2-:3]}];
	end
	reg pend_any_w;
	reg [SINK_W_C - 1:0] pend_sink_w;
	function automatic [SINK_W_C - 1:0] sv2v_cast_86716;
		input reg [SINK_W_C - 1:0] inp;
		sv2v_cast_86716 = inp;
	endfunction
	always @(*) begin : pend_pick
		if (_sv2v_0)
			;
		pend_any_w = 1'b0;
		pend_sink_w = 1'sb0;
		begin : sv2v_autoblock_1
			reg [31:0] i;
			for (i = 0; i < N_SINKS_P; i = i + 1)
				if (!pend_any_w && pendexp_r[i]) begin
					pend_any_w = 1'b1;
					pend_sink_w = sv2v_cast_86716(i);
				end
		end
	end
	wire exp_hit_w;
	wire [SINK_W_C - 1:0] exp_sink_w;
	function automatic [31:0] sv2v_cast_32;
		input reg [31:0] inp;
		sv2v_cast_32 = inp;
	endfunction
	assign exp_hit_w = (tmr_exp_valid_i && (sv2v_cast_32(tmr_exp_owner_i) >= TMR_OWNER_BASE_P)) && (sv2v_cast_32(tmr_exp_owner_i) < (TMR_OWNER_BASE_P + N_SINKS_P));
	assign exp_sink_w = sv2v_cast_86716(sv2v_cast_32(tmr_exp_owner_i) - TMR_OWNER_BASE_P);
	wire txn_acmp_w;
	wire txn_msg_ok_w;
	wire txn_eid_ok_w;
	wire txn_uid_ok_w;
	wire txn_has_slot_w;
	assign txn_acmp_w = txn_i[356-:3] == 3'd1;
	localparam [3:0] pp_acmp_pkg_AMSG_BIND_RX_CMD_C = 4'd6;
	localparam [3:0] pp_acmp_pkg_AMSG_GET_RX_STATE_CMD_C = 4'd10;
	localparam [3:0] pp_acmp_pkg_AMSG_PROBE_TX_RESP_C = 4'd1;
	localparam [3:0] pp_acmp_pkg_AMSG_UNBIND_RX_CMD_C = 4'd8;
	assign txn_msg_ok_w = (((txn_i[353-:4] == pp_acmp_pkg_AMSG_PROBE_TX_RESP_C) || (txn_i[353-:4] == pp_acmp_pkg_AMSG_BIND_RX_CMD_C)) || (txn_i[353-:4] == pp_acmp_pkg_AMSG_UNBIND_RX_CMD_C)) || (txn_i[353-:4] == pp_acmp_pkg_AMSG_GET_RX_STATE_CMD_C);
	assign txn_eid_ok_w = txn_i[221-:64] == entity_id_i;
	assign txn_uid_ok_w = sv2v_cast_32(txn_i[75-:16]) < N_SINKS_P;
	localparam [2:0] pp_pkg_PP_SLOT_NULL_C = 3'd7;
	assign txn_has_slot_w = txn_i[59-:3] != pp_pkg_PP_SLOT_NULL_C;
	assign txn_ready_o = (xs_r == 5'd1) && !strq_pend_r;
	assign evt_tk_ready_o = (((xs_r == 5'd1) && !strq_pend_r) && !txn_valid_i) && !pend_any_w;
	assign strm_set_ready_o = strq_done_r;
	assign strm_set_error_o = strq_fail_r;
	assign pre_ready_o = ((((xs_r == 5'd1) && !strq_pend_r) && !txn_valid_i) && !pend_any_w) && !evt_tk_valid_i;
	wire slot_ok_w;
	wire [4:0] f_cnt_w;
	assign slot_ok_w = rxslot_r != pp_pkg_PP_SLOT_NULL_C;
	assign f_cnt_w = (msg_x_r == pp_acmp_pkg_AMSG_PROBE_TX_RESP_C ? 5'd28 : 5'd12);
	function automatic [9:0] sv2v_cast_10;
		input reg [9:0] inp;
		sv2v_cast_10 = inp;
	endfunction
	function automatic [RXS_ADDR_W_C - 1:0] sv2v_cast_E1968;
		input reg [RXS_ADDR_W_C - 1:0] inp;
		sv2v_cast_E1968 = inp;
	endfunction
	function automatic [RXS_ADDR_W_C - 1:0] fofs_f;
		input reg [4:0] i;
		reg [9:0] o;
		begin
			if (i < 5'd8)
				o = 10'd20 + sv2v_cast_10(i);
			else if (i < 5'd10)
				o = 10'd36 + sv2v_cast_10(i - 5'd8);
			else if (i < 5'd12)
				o = 10'd50 + sv2v_cast_10(i - 5'd10);
			else if (i < 5'd20)
				o = 10'd4 + sv2v_cast_10(i - 5'd12);
			else if (i < 5'd26)
				o = 10'd40 + sv2v_cast_10(i - 5'd20);
			else
				o = 10'd52 + sv2v_cast_10(i - 5'd26);
			fofs_f = sv2v_cast_E1968(o);
		end
	endfunction
	assign rxs_rd_en_o = ((xs_r == 5'd5) && slot_ok_w) && (f_idx_r < f_cnt_w);
	assign rxs_rd_addr_o = fofs_f(f_idx_r);
	assign rxs_rd_slot_o = rxslot_r[RXS_SLOT_W_C - 1:0];
	assign probe_match_w = (((ctlr_x_r == rec_r[191-:64]) && (tk_eid_f_r == rec_r[95-:64])) && (tk_uid_f_r == rec_r[111-:16])) && (seq_x_r == rec_r[127-:16]);
	localparam [4:0] pp_acmp_pkg_AST_SUCCESS_C = 5'd0;
	localparam [1:0] pp_acmp_pkg_TK_KIND_DEP_C = 2'd1;
	localparam [1:0] pp_acmp_pkg_TK_KIND_DISC_C = 2'd0;
	localparam [1:0] pp_acmp_pkg_TK_KIND_REG_C = 2'd2;
	always @(*) begin : classify
		if (_sv2v_0)
			;
		evt_w = 4'd7;
		if (src_txn_r)
			(* full_case, parallel_case *)
			case (msg_x_r)
				pp_acmp_pkg_AMSG_BIND_RX_CMD_C:
					if ((rec_r[11] && (tk_eid_f_r == rec_r[95-:64])) && (tk_uid_f_r == rec_r[111-:16]))
						evt_w = 4'd0;
					else
						evt_w = 4'd1;
				pp_acmp_pkg_AMSG_UNBIND_RX_CMD_C: evt_w = 4'd2;
				pp_acmp_pkg_AMSG_GET_RX_STATE_CMD_C: evt_w = 4'd3;
				default: evt_w = (status_x_r == pp_acmp_pkg_AST_SUCCESS_C ? 4'd4 : 4'd5);
			endcase
		else if (src_tmr_r)
			(* full_case, parallel_case *)
			case (rec_r[2-:3])
				3'd2: evt_w = 4'd6;
				3'd3: evt_w = 4'd7;
				3'd4: evt_w = 4'd7;
				3'd5: evt_w = 4'd8;
				3'd6: evt_w = 4'd9;
				default: evt_w = 4'd7;
			endcase
		else
			(* full_case, parallel_case *)
			case (tkkind_r)
				pp_acmp_pkg_TK_KIND_DISC_C: evt_w = 4'd10;
				pp_acmp_pkg_TK_KIND_DEP_C: evt_w = 4'd11;
				pp_acmp_pkg_TK_KIND_REG_C: evt_w = 4'd12;
				default: evt_w = 4'd13;
			endcase
	end
	wire rom_valid_w;
	wire rom_ign_w;
	wire rom_cond_w;
	wire [16:0] rom_acts_w;
	wire [2:0] rom_next_w;
	localparam [31:0] pp_acmp_pkg_TROM_VALID_B_C = 20;
	assign rom_valid_w = trom_rdata_r[pp_acmp_pkg_TROM_VALID_B_C];
	localparam [31:0] pp_acmp_pkg_TROM_IGN_B_C = 21;
	assign rom_ign_w = trom_rdata_r[pp_acmp_pkg_TROM_IGN_B_C];
	localparam [31:0] pp_acmp_pkg_TROM_COND_B_C = 22;
	assign rom_cond_w = trom_rdata_r[pp_acmp_pkg_TROM_COND_B_C];
	localparam [31:0] pp_acmp_pkg_TROM_ACT_LSB_C = 3;
	assign rom_acts_w = trom_rdata_r[pp_acmp_pkg_TROM_ACT_LSB_C+:17];
	localparam [31:0] pp_acmp_pkg_TROM_NEXT_LSB_C = 0;
	assign rom_next_w = trom_rdata_r[pp_acmp_pkg_TROM_NEXT_LSB_C+:3];
	reg [16:0] res_acts_w;
	reg [2:0] res_next_w;
	localparam [31:0] pp_acmp_pkg_ACT_A12_C = 11;
	localparam [31:0] pp_acmp_pkg_ACT_A17_C = 16;
	always @(*) begin : dagger
		if (_sv2v_0)
			;
		res_acts_w = rom_acts_w;
		res_next_w = rom_next_w;
		if (rom_cond_w && !rec_r[18]) begin
			res_next_w = 3'd1;
			res_acts_w[pp_acmp_pkg_ACT_A12_C] = 1'b0;
			res_acts_w[pp_acmp_pkg_ACT_A17_C] = 1'b1;
		end
	end
	wire lock_block_w;
	assign lock_block_w = lock_held_i && (lock_ctlr_i != ctlr_x_r);
	localparam [31:0] pp_acmp_pkg_ACT_A10_C = 9;
	localparam [31:0] pp_acmp_pkg_ACT_A11_C = 10;
	localparam [31:0] pp_acmp_pkg_ACT_A13_C = 12;
	localparam [31:0] pp_acmp_pkg_ACT_A14_C = 13;
	localparam [31:0] pp_acmp_pkg_ACT_A15_C = 14;
	localparam [31:0] pp_acmp_pkg_ACT_A16_C = 15;
	localparam [31:0] pp_acmp_pkg_ACT_A1_C = 0;
	localparam [31:0] pp_acmp_pkg_ACT_A2_C = 1;
	localparam [31:0] pp_acmp_pkg_ACT_A3_C = 2;
	localparam [31:0] pp_acmp_pkg_ACT_A4_C = 3;
	localparam [31:0] pp_acmp_pkg_ACT_A5_C = 4;
	localparam [31:0] pp_acmp_pkg_ACT_A6_C = 5;
	localparam [31:0] pp_acmp_pkg_ACT_A7_C = 6;
	localparam [31:0] pp_acmp_pkg_ACT_A8_C = 7;
	localparam [31:0] pp_acmp_pkg_ACT_A9_C = 8;
	function automatic [4:0] sv2v_cast_5;
		input reg [4:0] inp;
		sv2v_cast_5 = inp;
	endfunction
	function automatic [4:0] act_order_f;
		input reg [4:0] k;
		(* full_case, parallel_case *)
		case (k)
			5'd0: act_order_f = sv2v_cast_5(pp_acmp_pkg_ACT_A1_C);
			5'd1: act_order_f = sv2v_cast_5(pp_acmp_pkg_ACT_A11_C);
			5'd2: act_order_f = sv2v_cast_5(pp_acmp_pkg_ACT_A8_C);
			5'd3: act_order_f = sv2v_cast_5(pp_acmp_pkg_ACT_A9_C);
			5'd4: act_order_f = sv2v_cast_5(pp_acmp_pkg_ACT_A2_C);
			5'd5: act_order_f = sv2v_cast_5(pp_acmp_pkg_ACT_A6_C);
			5'd6: act_order_f = sv2v_cast_5(pp_acmp_pkg_ACT_A10_C);
			5'd7: act_order_f = sv2v_cast_5(pp_acmp_pkg_ACT_A12_C);
			5'd8: act_order_f = sv2v_cast_5(pp_acmp_pkg_ACT_A13_C);
			5'd9: act_order_f = sv2v_cast_5(pp_acmp_pkg_ACT_A14_C);
			5'd10: act_order_f = sv2v_cast_5(pp_acmp_pkg_ACT_A15_C);
			5'd11: act_order_f = sv2v_cast_5(pp_acmp_pkg_ACT_A16_C);
			5'd12: act_order_f = sv2v_cast_5(pp_acmp_pkg_ACT_A17_C);
			5'd13: act_order_f = sv2v_cast_5(pp_acmp_pkg_ACT_A3_C);
			5'd14: act_order_f = sv2v_cast_5(pp_acmp_pkg_ACT_A7_C);
			5'd15: act_order_f = sv2v_cast_5(pp_acmp_pkg_ACT_A4_C);
			default: act_order_f = sv2v_cast_5(pp_acmp_pkg_ACT_A5_C);
		endcase
	endfunction
	wire [4:0] cur_act_w;
	assign cur_act_w = act_order_f(ord_r);
	reg [3:0] b_msg_w;
	reg [4:0] b_status_w;
	reg [63:0] b_sid_w;
	reg [63:0] b_ctlr_w;
	reg [63:0] b_tkeid_w;
	reg [15:0] b_tkuid_w;
	reg [15:0] b_luid_w;
	reg [15:0] b_cc_w;
	reg [15:0] b_seq_w;
	reg [15:0] b_flags_w;
	reg [15:0] b_vlan_w;
	reg [47:0] b_da_w;
	wire [447:0] pdu_w;
	wire [7:0] pdu_byte_w;
	wire settled_w;
	wire rf_w;
	assign settled_w = (rec_r[2-:3] == 3'd6) || (rec_r[2-:3] == 3'd7);
	assign rf_w = (rec_r[2-:3] == 3'd7) && rec_r[16];
	localparam [15:0] pp_acmp_pkg_AFLG_FAST_CONNECT_C = 16'h0002;
	localparam [15:0] pp_acmp_pkg_AFLG_REG_FAILED_C = 16'h0040;
	localparam [15:0] pp_acmp_pkg_AFLG_STREAMING_WAIT_C = 16'h0008;
	localparam [3:0] pp_acmp_pkg_AMSG_BIND_RX_RESP_C = 4'd7;
	localparam [3:0] pp_acmp_pkg_AMSG_GET_RX_STATE_RESP_C = 4'd11;
	localparam [3:0] pp_acmp_pkg_AMSG_PROBE_TX_CMD_C = 4'd0;
	localparam [3:0] pp_acmp_pkg_AMSG_UNBIND_RX_RESP_C = 4'd9;
	function automatic [15:0] sv2v_cast_16;
		input reg [15:0] inp;
		sv2v_cast_16 = inp;
	endfunction
	always @(*) begin : bld_fields
		if (_sv2v_0)
			;
		b_msg_w = pp_acmp_pkg_AMSG_GET_RX_STATE_RESP_C;
		b_status_w = pp_acmp_pkg_AST_SUCCESS_C;
		b_sid_w = 64'd0;
		b_ctlr_w = ctlr_x_r;
		b_tkeid_w = 64'd0;
		b_tkuid_w = 16'd0;
		b_luid_w = uid16_r;
		b_da_w = 48'd0;
		b_cc_w = 16'd0;
		b_seq_w = seq_x_r;
		b_flags_w = 16'd0;
		b_vlan_w = 16'd0;
		(* full_case, parallel_case *)
		case (bk_r)
			3'd0: begin
				b_msg_w = bmsg_r;
				b_status_w = bstat_r;
				b_tkeid_w = tk_eid_f_r;
				b_tkuid_w = tk_uid_f_r;
			end
			3'd1: begin
				b_msg_w = pp_acmp_pkg_AMSG_BIND_RX_RESP_C;
				b_tkeid_w = tk_eid_f_r;
				b_tkuid_w = tk_uid_f_r;
				b_cc_w = 16'd1;
				b_flags_w = flags_f_r & pp_acmp_pkg_AFLG_STREAMING_WAIT_C;
			end
			3'd2: begin
				b_msg_w = pp_acmp_pkg_AMSG_UNBIND_RX_RESP_C;
				b_tkeid_w = tk_eid_f_r;
				b_tkuid_w = tk_uid_f_r;
			end
			3'd3: begin
				b_msg_w = pp_acmp_pkg_AMSG_GET_RX_STATE_RESP_C;
				b_tkeid_w = (rec_r[11] ? rec_r[95-:64] : 64'd0);
				b_tkuid_w = (rec_r[11] ? rec_r[111-:16] : 16'd0);
				b_cc_w = (rec_r[11] ? 16'd1 : 16'd0);
				b_flags_w = (rec_r[11] ? (pp_acmp_pkg_AFLG_FAST_CONNECT_C | (rec_r[13] ? pp_acmp_pkg_AFLG_STREAMING_WAIT_C : 16'd0)) | (rf_w ? pp_acmp_pkg_AFLG_REG_FAILED_C : 16'd0) : 16'd0);
				b_sid_w = (settled_w ? rec_r[255-:64] : 64'd0);
				b_da_w = (settled_w ? rec_r[303-:48] : 48'd0);
				b_vlan_w = (settled_w ? {4'd0, rec_r[315-:12]} : 16'd0);
			end
			default: begin
				b_msg_w = pp_acmp_pkg_AMSG_PROBE_TX_CMD_C;
				b_ctlr_w = rec_r[191-:64];
				b_tkeid_w = rec_r[95-:64];
				b_tkuid_w = rec_r[111-:16];
				b_luid_w = sv2v_cast_16(sv2v_cast_32(sink_r));
				b_seq_w = rec_r[127-:16];
				b_flags_w = pp_acmp_pkg_AFLG_FAST_CONNECT_C;
			end
		endcase
	end
	localparam [10:0] pp_acmp_pkg_ACMP_CDL_MILAN_C = 11'd44;
	assign pdu_w = {12'hfc0, b_msg_w, b_status_w, pp_acmp_pkg_ACMP_CDL_MILAN_C, b_sid_w, b_ctlr_w, b_tkeid_w, entity_id_i, b_tkuid_w, b_luid_w, b_da_w, b_cc_w, b_seq_w, b_flags_w, b_vlan_w, 16'h0000};
	assign pdu_byte_w = pdu_w[9'd440 - {bidx_r, 3'b000}+:8];
	localparam [2:0] pp_acmp_pkg_PB_PASSIVE_C = 3'd1;
	function automatic [7:0] sv2v_cast_8;
		input reg [7:0] inp;
		sv2v_cast_8 = inp;
	endfunction
	always @(*) begin : pre_rec
		if (_sv2v_0)
			;
		pre_rec_w = 1'sb0;
		pre_rec_w[2-:3] = 3'd1;
		pre_rec_w[5-:3] = pp_acmp_pkg_PB_PASSIVE_C;
		pre_rec_w[11] = 1'b1;
		pre_rec_w[13] = preL_sw_r;
		pre_rec_w[12] = preL_started_r;
		pre_rec_w[95-:64] = preL_talker_eid_r;
		pre_rec_w[111-:16] = preL_talker_uid_r;
		pre_rec_w[191-:64] = preL_ctlr_eid_r;
		pre_rec_w[367-:8] = sv2v_cast_8(TMR_BASE_SLOT_P + sv2v_cast_32(sink_r));
	end
	always @(*) begin : wb_rec
		if (_sv2v_0)
			;
		wb_rec_w = rec_r;
		wb_rec_w[367-:8] = sv2v_cast_8(TMR_BASE_SLOT_P + sv2v_cast_32(sink_r));
	end
	function automatic [((SINK_W_C + 0) >= 0 ? SINK_W_C + 1 : 1 - (SINK_W_C + 0)) - 1:0] sv2v_cast_70DE6;
		input reg [((SINK_W_C + 0) >= 0 ? SINK_W_C + 1 : 1 - (SINK_W_C + 0)) - 1:0] inp;
		sv2v_cast_70DE6 = inp;
	endfunction
	assign recwr_en_w = (((xs_r == 5'd0) && (init_cnt_r < sv2v_cast_70DE6(N_SINKS_P))) || (xs_r == 5'd2)) || (xs_r == 5'd15);
	function automatic [383:0] sv2v_cast_384;
		input reg [383:0] inp;
		sv2v_cast_384 = inp;
	endfunction
	assign rec_rd_w = sv2v_cast_384(rec_rdata_r);
	assign recwr_rec_w = sv2v_cast_384(recwr_data_w);
	assign recwr_addr_w = (xs_r == 5'd0 ? init_cnt_r[SINK_W_C - 1:0] : sink_r);
	function automatic [383:0] sv2v_cast_BA781;
		input reg [383:0] inp;
		sv2v_cast_BA781 = inp;
	endfunction
	assign recwr_data_w = (xs_r == 5'd0 ? {384 {1'sb0}} : (xs_r == 5'd2 ? sv2v_cast_BA781(pre_rec_w) : sv2v_cast_BA781(wb_rec_w)));
	always @(posedge clk_i) begin : started_mirror
		if (!rst_n)
			strm_started_o <= 1'sb0;
		else if (recwr_en_w)
			strm_started_o[recwr_addr_w] <= recwr_rec_w[12];
	end
	assign dbg_busy_o = xs_r != 5'd1;
	assign dbg_strq_drop_o = dbg_strq_drop_r;
	assign dbg_recwr_o = recwr_en_w;
	assign dbg_recwr_sink_o = recwr_addr_w;
	assign dbg_recwr_rec_o = recwr_data_w;
	localparam [2:0] pp_acmp_pkg_PRNG_KIND_ACMP_DELAY_C = 3'd0;
	assign draw_kind_o = pp_acmp_pkg_PRNG_KIND_ACMP_DELAY_C;
	assign txs_oversize_o = 1'b0;
	assign txs_wr_slot_o = bslot_r;
	assign txreq_slot_o = bslot_r;
	assign rxs_free_slot_o = rxslot_r[RXS_SLOT_W_C - 1:0];
	assign act_sink_o = sink_r;
	assign act_settle_sid_o = sid_f_r;
	assign act_settle_da_o = da_f_r;
	assign act_settle_vlan_o = vlan_f_r[11:0];
	wire pend_clr_a11_w;
	wire pend_clr_pop_w;
	assign pend_clr_a11_w = ((xs_r == 5'd8) && (cur_act_w == sv2v_cast_5(pp_acmp_pkg_ACT_A11_C))) && apend_r[pp_acmp_pkg_ACT_A11_C];
	assign pend_clr_pop_w = (((xs_r == 5'd1) && !strq_pend_r) && !txn_valid_i) && pend_any_w;
	always @(posedge clk_i) begin : pendexp
		if (!rst_n)
			pendexp_r <= 1'sb0;
		else begin
			if (exp_hit_w)
				pendexp_r[exp_sink_w] <= 1'b1;
			if (pend_clr_a11_w)
				pendexp_r[sink_r] <= 1'b0;
			if (pend_clr_pop_w)
				pendexp_r[pend_sink_w] <= 1'b0;
		end
	end
	localparam [31:0] pp_acmp_pkg_ACMP_PDU_BYTES_C = 56;
	localparam [4:0] pp_acmp_pkg_AST_CONTROLLER_NOT_AUTH_C = 5'd13;
	localparam [4:0] pp_acmp_pkg_AST_LISTENER_TALKER_TIMEOUT_C = 5'd7;
	localparam [4:0] pp_acmp_pkg_AST_LISTENER_UNKNOWN_ID_C = 5'd1;
	localparam [2:0] pp_acmp_pkg_PB_ACTIVE_C = 3'd2;
	localparam [2:0] pp_acmp_pkg_PB_COMPLETED_C = 3'd3;
	localparam [2:0] pp_acmp_pkg_PB_DISABLED_C = 3'd0;
	localparam [31:0] pp_acmp_pkg_T_ACMP_CMD_MS_C = 32'd200;
	localparam [31:0] pp_acmp_pkg_T_ACMP_NOTK_MS_C = 32'd10000;
	localparam [31:0] pp_acmp_pkg_T_ACMP_RETRY_MS_C = 32'd4000;
	function automatic signed [((SINK_W_C + 0) >= 0 ? SINK_W_C + 1 : 1 - (SINK_W_C + 0)) - 1:0] sv2v_cast_70DE6_signed;
		input reg signed [((SINK_W_C + 0) >= 0 ? SINK_W_C + 1 : 1 - (SINK_W_C + 0)) - 1:0] inp;
		sv2v_cast_70DE6_signed = inp;
	endfunction
	function automatic [TMR_SLOT_AW_P - 1:0] sv2v_cast_13ADE;
		input reg [TMR_SLOT_AW_P - 1:0] inp;
		sv2v_cast_13ADE = inp;
	endfunction
	function automatic [7:0] sv2v_cast_4E301;
		input reg [7:0] inp;
		sv2v_cast_4E301 = inp;
	endfunction
	function automatic [TXS_LEN_W_C - 1:0] sv2v_cast_EFC2D;
		input reg [TXS_LEN_W_C - 1:0] inp;
		sv2v_cast_EFC2D = inp;
	endfunction
	function automatic [5:0] sv2v_cast_6;
		input reg [5:0] inp;
		sv2v_cast_6 = inp;
	endfunction
	function automatic [STRQ_TMO_W_C - 1:0] sv2v_cast_84400;
		input reg [STRQ_TMO_W_C - 1:0] inp;
		sv2v_cast_84400 = inp;
	endfunction
	function automatic signed [STRQ_TMO_W_C - 1:0] sv2v_cast_84400_signed;
		input reg signed [STRQ_TMO_W_C - 1:0] inp;
		sv2v_cast_84400_signed = inp;
	endfunction
	always @(posedge clk_i) begin : engine
		if (!rst_n) begin
			xs_r <= 5'd0;
			init_cnt_r <= 1'sb0;
			src_txn_r <= 1'b0;
			src_tmr_r <= 1'b0;
			src_strq_r <= 1'b0;
			msg_x_r <= 4'd0;
			status_x_r <= 5'd0;
			ctlr_x_r <= 64'd0;
			seq_x_r <= 16'd0;
			uid16_r <= 16'd0;
			rxslot_r <= pp_pkg_PP_SLOT_NULL_C;
			sink_r <= 1'sb0;
			tkkind_r <= 2'd0;
			tkfail_r <= 1'b0;
			errflow_r <= 1'b0;
			preL_talker_eid_r <= 64'd0;
			preL_talker_uid_r <= 16'd0;
			preL_ctlr_eid_r <= 64'd0;
			preL_sw_r <= 1'b0;
			preL_started_r <= 1'b0;
			strtL_val_r <= 1'b0;
			strq_pend_r <= 1'b0;
			strq_busy_r <= 1'b0;
			strq_done_r <= 1'b0;
			strq_fail_r <= 1'b0;
			strq_tmo_r <= 1'sb0;
			strq_sink_r <= 16'd0;
			strq_val_r <= 1'b0;
			dbg_strq_drop_r <= 16'd0;
			strt_was_r <= 1'b0;
			bnd_was_r <= 1'b0;
			bind_act_r <= 1'b0;
			act_strt_chg_o <= 1'b0;
			act_strt_cmd_chg_o <= 1'b0;
			tk_eid_f_r <= 64'd0;
			tk_uid_f_r <= 16'd0;
			flags_f_r <= 16'd0;
			sid_f_r <= 64'd0;
			da_f_r <= 48'd0;
			vlan_f_r <= 16'd0;
			f_idx_r <= 5'd0;
			f_cap_idx_r <= 5'd0;
			f_cap_v_r <= 1'b0;
			rec_r <= 1'sb0;
			evt_r <= 4'd0;
			apend_r <= 17'd0;
			ord_r <= 5'd0;
			cellmut_r <= 1'b0;
			bk_r <= 3'd0;
			bmsg_r <= 4'd0;
			bstat_r <= 5'd0;
			bidx_r <= 6'd0;
			bslot_r <= 1'sb0;
			probe_ctr_r <= 16'd0;
			draw_issued_r <= 1'b0;
			tmr_arm_valid_o <= 1'b0;
			tmr_arm_cancel_o <= 1'b0;
			tmr_arm_slot_o <= 1'sb0;
			tmr_arm_owner_o <= 1'sb0;
			tmr_arm_deadline_ms_o <= 32'd0;
			draw_req_o <= 1'b0;
			txs_alloc_req_o <= 1'b0;
			txs_wr_addr_o <= 1'sb0;
			txs_wr_valid_o <= 1'b0;
			txs_wr_data_o <= 8'd0;
			txs_wr_commit_o <= 1'b0;
			txs_wr_len_o <= 1'sb0;
			txreq_valid_o <= 1'b0;
			rxs_free_o <= 1'b0;
			act_settle_o <= 1'b0;
			act_teardown_o <= 1'b0;
			act_disc_arm_o <= 1'b0;
			act_disc_talker_eid_o <= 64'd0;
			act_disc_disarm_o <= 1'b0;
			act_nvm_o <= 1'b0;
			act_nvm_set_o <= 1'b0;
			act_notify_o <= 1'b0;
		end
		else begin
			tmr_arm_valid_o <= 1'b0;
			tmr_arm_cancel_o <= 1'b0;
			draw_req_o <= 1'b0;
			txs_alloc_req_o <= 1'b0;
			txs_wr_valid_o <= 1'b0;
			txs_wr_commit_o <= 1'b0;
			txreq_valid_o <= 1'b0;
			rxs_free_o <= 1'b0;
			act_settle_o <= 1'b0;
			act_teardown_o <= 1'b0;
			act_disc_arm_o <= 1'b0;
			act_disc_disarm_o <= 1'b0;
			act_nvm_o <= 1'b0;
			act_notify_o <= 1'b0;
			act_strt_chg_o <= 1'b0;
			act_strt_cmd_chg_o <= 1'b0;
			f_cap_v_r <= 1'b0;
			(* full_case, parallel_case *)
			case (xs_r)
				5'd0:
					if (init_cnt_r < sv2v_cast_70DE6(N_SINKS_P))
						init_cnt_r <= init_cnt_r + sv2v_cast_70DE6_signed(1);
					else
						xs_r <= 5'd1;
				5'd1: begin
					bind_act_r <= 1'b0;
					errflow_r <= 1'b0;
					cellmut_r <= 1'b0;
					apend_r <= 17'd0;
					ord_r <= 5'd0;
					f_idx_r <= 5'd0;
					tk_eid_f_r <= 64'd0;
					tk_uid_f_r <= 16'd0;
					flags_f_r <= 16'd0;
					sid_f_r <= 64'd0;
					da_f_r <= 48'd0;
					vlan_f_r <= 16'd0;
					if (strq_pend_r) begin
						src_txn_r <= 1'b0;
						src_tmr_r <= 1'b0;
						src_strq_r <= 1'b1;
						rxslot_r <= pp_pkg_PP_SLOT_NULL_C;
						sink_r <= sv2v_cast_86716(strq_sink_r);
						strtL_val_r <= strq_val_r;
						strq_pend_r <= 1'b0;
						if (sv2v_cast_32(strq_sink_r) < N_SINKS_P)
							xs_r <= 5'd17;
						else begin
							dbg_strq_drop_r <= dbg_strq_drop_r + 16'd1;
							strq_done_r <= 1'b1;
							strq_fail_r <= 1'b1;
						end
					end
					else if (txn_valid_i) begin
						src_txn_r <= 1'b1;
						src_tmr_r <= 1'b0;
						src_strq_r <= 1'b0;
						msg_x_r <= txn_i[353-:4];
						status_x_r <= txn_i[349-:5];
						ctlr_x_r <= txn_i[285-:64];
						seq_x_r <= txn_i[157-:16];
						uid16_r <= txn_i[75-:16];
						rxslot_r <= txn_i[59-:3];
						sink_r <= sv2v_cast_86716(txn_i[75-:16]);
						if ((!txn_acmp_w || !txn_msg_ok_w) || !txn_eid_ok_w)
							xs_r <= 5'd16;
						else if (!txn_uid_ok_w) begin
							if (txn_i[353-:4] == pp_acmp_pkg_AMSG_PROBE_TX_RESP_C)
								xs_r <= 5'd16;
							else begin
								errflow_r <= 1'b1;
								bk_r <= 3'd0;
								bstat_r <= pp_acmp_pkg_AST_LISTENER_UNKNOWN_ID_C;
								bmsg_r <= txn_i[353-:4] + 4'd1;
								xs_r <= (txn_i[59-:3] != pp_pkg_PP_SLOT_NULL_C ? 5'd5 : 5'd10);
							end
						end
						else
							xs_r <= 5'd3;
					end
					else if (pend_any_w) begin
						src_txn_r <= 1'b0;
						src_tmr_r <= 1'b1;
						src_strq_r <= 1'b0;
						rxslot_r <= pp_pkg_PP_SLOT_NULL_C;
						sink_r <= pend_sink_w;
						xs_r <= 5'd3;
					end
					else if (evt_tk_valid_i) begin
						src_txn_r <= 1'b0;
						src_tmr_r <= 1'b0;
						src_strq_r <= 1'b0;
						rxslot_r <= pp_pkg_PP_SLOT_NULL_C;
						tkkind_r <= evt_tk_kind_i;
						tkfail_r <= evt_tk_failed_i;
						sink_r <= sv2v_cast_86716(evt_tk_sink_i);
						if (sv2v_cast_32(evt_tk_sink_i) < N_SINKS_P)
							xs_r <= 5'd3;
					end
					else if (pre_valid_i) begin
						src_strq_r <= 1'b0;
						sink_r <= sv2v_cast_86716(pre_sink_i);
						preL_talker_eid_r <= pre_talker_eid_i;
						preL_talker_uid_r <= pre_talker_uid_i;
						preL_ctlr_eid_r <= pre_ctlr_eid_i;
						preL_sw_r <= pre_sw_i;
						preL_started_r <= pre_started_i;
						if (sv2v_cast_32(pre_sink_i) < N_SINKS_P)
							xs_r <= 5'd2;
					end
				end
				5'd2: begin
					act_disc_arm_o <= 1'b1;
					act_disc_talker_eid_o <= preL_talker_eid_r;
					xs_r <= 5'd1;
				end
				5'd17: xs_r <= 5'd18;
				5'd18: begin
					rec_r <= rec_rd_w;
					strt_was_r <= rec_rd_w[12];
					bnd_was_r <= rec_rd_w[11];
					if (rec_rd_w[11] && (rec_rd_w[12] != strtL_val_r)) begin
						rec_r[12] <= strtL_val_r;
						cellmut_r <= 1'b1;
						xs_r <= 5'd15;
					end
					else begin
						strq_done_r <= 1'b1;
						strq_fail_r <= 1'b0;
						xs_r <= 5'd1;
					end
				end
				5'd3: xs_r <= 5'd4;
				5'd4: begin
					rec_r <= sv2v_cast_384(rec_rdata_r);
					strt_was_r <= rec_rd_w[12];
					bnd_was_r <= rec_rd_w[11];
					if ((src_txn_r && (msg_x_r != pp_acmp_pkg_AMSG_GET_RX_STATE_CMD_C)) && slot_ok_w)
						xs_r <= 5'd5;
					else
						xs_r <= 5'd6;
				end
				5'd5: begin
					if (slot_ok_w && (f_idx_r < f_cnt_w))
						f_idx_r <= f_idx_r + 5'd1;
					f_cap_v_r <= rxs_rd_en_o;
					f_cap_idx_r <= f_idx_r;
					if (f_cap_v_r) begin
						if (f_cap_idx_r < 5'd8)
							tk_eid_f_r <= {tk_eid_f_r[55:0], rxs_rd_data_i};
						else if (f_cap_idx_r < 5'd10)
							tk_uid_f_r <= {tk_uid_f_r[7:0], rxs_rd_data_i};
						else if (f_cap_idx_r < 5'd12)
							flags_f_r <= {flags_f_r[7:0], rxs_rd_data_i};
						else if (f_cap_idx_r < 5'd20)
							sid_f_r <= {sid_f_r[55:0], rxs_rd_data_i};
						else if (f_cap_idx_r < 5'd26)
							da_f_r <= {da_f_r[39:0], rxs_rd_data_i};
						else
							vlan_f_r <= {vlan_f_r[7:0], rxs_rd_data_i};
						if (f_cap_idx_r == (f_cnt_w - 5'd1))
							xs_r <= (errflow_r ? 5'd10 : 5'd6);
					end
					else if (!slot_ok_w)
						xs_r <= (errflow_r ? 5'd10 : 5'd6);
				end
				5'd6: begin
					evt_r <= evt_w;
					if ((src_txn_r && (msg_x_r == pp_acmp_pkg_AMSG_PROBE_TX_RESP_C)) && !probe_match_w)
						xs_r <= 5'd16;
					else
						xs_r <= 5'd7;
				end
				5'd7: begin
					if ((evt_r == 4'd10) && rom_valid_w)
						rec_r[18] <= 1'b1;
					if ((evt_r == 4'd11) && rom_valid_w)
						rec_r[18] <= 1'b0;
					if (((evt_r == 4'd12) && rom_valid_w) && !rom_ign_w) begin
						rec_r[17] <= 1'b1;
						rec_r[16] <= tkfail_r;
					end
					if (!rom_valid_w || rom_ign_w)
						xs_r <= 5'd15;
					else if (res_acts_w[pp_acmp_pkg_ACT_A1_C] && lock_block_w) begin
						errflow_r <= 1'b1;
						bk_r <= 3'd0;
						bstat_r <= pp_acmp_pkg_AST_CONTROLLER_NOT_AUTH_C;
						bmsg_r <= msg_x_r + 4'd1;
						xs_r <= 5'd10;
					end
					else begin
						rec_r[2-:3] <= res_next_w;
						apend_r <= res_acts_w & ~(17'd1 << pp_acmp_pkg_ACT_A1_C);
						ord_r <= 5'd0;
						xs_r <= 5'd8;
					end
				end
				5'd8:
					if (ord_r == 5'd17)
						xs_r <= 5'd15;
					else if (!apend_r[cur_act_w])
						ord_r <= ord_r + 5'd1;
					else begin
						ord_r <= ord_r + 5'd1;
						(* full_case, parallel_case *)
						case (cur_act_w)
							sv2v_cast_5(pp_acmp_pkg_ACT_A11_C): begin
								tmr_arm_valid_o <= 1'b1;
								tmr_arm_cancel_o <= 1'b1;
								tmr_arm_slot_o <= sv2v_cast_13ADE(TMR_BASE_SLOT_P + sv2v_cast_32(sink_r));
								tmr_arm_owner_o <= sv2v_cast_4E301(TMR_OWNER_BASE_P + sv2v_cast_32(sink_r));
							end
							sv2v_cast_5(pp_acmp_pkg_ACT_A8_C): begin
								act_teardown_o <= 1'b1;
								rec_r[255-:64] <= 64'd0;
								rec_r[303-:48] <= 48'd0;
								rec_r[315-:12] <= 12'd0;
								rec_r[17] <= 1'b0;
								rec_r[16-:2] <= 2'd0;
								cellmut_r <= 1'b1;
							end
							sv2v_cast_5(pp_acmp_pkg_ACT_A9_C): begin
								act_disc_disarm_o <= 1'b1;
								rec_r[18] <= 1'b0;
								cellmut_r <= 1'b1;
							end
							sv2v_cast_5(pp_acmp_pkg_ACT_A2_C): begin
								bind_act_r <= 1'b1;
								rec_r[95-:64] <= tk_eid_f_r;
								rec_r[111-:16] <= tk_uid_f_r;
								rec_r[191-:64] <= ctlr_x_r;
								rec_r[13] <= |(flags_f_r & pp_acmp_pkg_AFLG_STREAMING_WAIT_C);
								rec_r[12] <= ~|(flags_f_r & pp_acmp_pkg_AFLG_STREAMING_WAIT_C);
								rec_r[11] <= 1'b1;
								act_nvm_o <= 1'b1;
								act_nvm_set_o <= 1'b1;
								cellmut_r <= 1'b1;
							end
							sv2v_cast_5(pp_acmp_pkg_ACT_A6_C): begin
								rec_r[191-:64] <= ctlr_x_r;
								rec_r[13] <= |(flags_f_r & pp_acmp_pkg_AFLG_STREAMING_WAIT_C);
								rec_r[12] <= ~|(flags_f_r & pp_acmp_pkg_AFLG_STREAMING_WAIT_C);
								cellmut_r <= 1'b1;
							end
							sv2v_cast_5(pp_acmp_pkg_ACT_A10_C): begin
								rec_r[95-:64] <= 64'd0;
								rec_r[111-:16] <= 16'd0;
								rec_r[191-:64] <= 64'd0;
								rec_r[127-:16] <= 16'd0;
								rec_r[11] <= 1'b0;
								rec_r[13] <= 1'b0;
								rec_r[12] <= 1'b0;
								rec_r[14] <= 1'b0;
								rec_r[5-:3] <= pp_acmp_pkg_PB_DISABLED_C;
								rec_r[10-:5] <= 5'd0;
								act_nvm_o <= 1'b1;
								act_nvm_set_o <= 1'b0;
								cellmut_r <= 1'b1;
							end
							sv2v_cast_5(pp_acmp_pkg_ACT_A12_C): begin
								rec_r[5-:3] <= pp_acmp_pkg_PB_ACTIVE_C;
								rec_r[10-:5] <= 5'd0;
								cellmut_r <= 1'b1;
								draw_issued_r <= 1'b0;
								ord_r <= ord_r;
								xs_r <= 5'd9;
							end
							sv2v_cast_5(pp_acmp_pkg_ACT_A13_C): begin
								rec_r[14] <= 1'b1;
								cellmut_r <= 1'b1;
								bk_r <= 3'd4;
								ord_r <= ord_r;
								xs_r <= 5'd10;
							end
							sv2v_cast_5(pp_acmp_pkg_ACT_A14_C): begin
								tmr_arm_valid_o <= 1'b1;
								tmr_arm_cancel_o <= 1'b0;
								tmr_arm_slot_o <= sv2v_cast_13ADE(TMR_BASE_SLOT_P + sv2v_cast_32(sink_r));
								tmr_arm_owner_o <= sv2v_cast_4E301(TMR_OWNER_BASE_P + sv2v_cast_32(sink_r));
								tmr_arm_deadline_ms_o <= now_ms_i + pp_acmp_pkg_T_ACMP_RETRY_MS_C;
								rec_r[10-:5] <= (evt_r == 4'd5 ? status_x_r : pp_acmp_pkg_AST_LISTENER_TALKER_TIMEOUT_C);
								cellmut_r <= 1'b1;
							end
							sv2v_cast_5(pp_acmp_pkg_ACT_A15_C): begin
								rec_r[255-:64] <= sid_f_r;
								rec_r[303-:48] <= da_f_r;
								rec_r[315-:12] <= vlan_f_r[11:0];
								rec_r[15] <= 1'b1;
								rec_r[5-:3] <= pp_acmp_pkg_PB_COMPLETED_C;
								rec_r[10-:5] <= 5'd0;
								act_settle_o <= 1'b1;
								tmr_arm_valid_o <= 1'b1;
								tmr_arm_cancel_o <= 1'b0;
								tmr_arm_slot_o <= sv2v_cast_13ADE(TMR_BASE_SLOT_P + sv2v_cast_32(sink_r));
								tmr_arm_owner_o <= sv2v_cast_4E301(TMR_OWNER_BASE_P + sv2v_cast_32(sink_r));
								tmr_arm_deadline_ms_o <= now_ms_i + pp_acmp_pkg_T_ACMP_NOTK_MS_C;
								cellmut_r <= 1'b1;
							end
							sv2v_cast_5(pp_acmp_pkg_ACT_A16_C): begin
								bk_r <= 3'd3;
								ord_r <= ord_r;
								xs_r <= 5'd10;
							end
							sv2v_cast_5(pp_acmp_pkg_ACT_A17_C): begin
								rec_r[5-:3] <= pp_acmp_pkg_PB_PASSIVE_C;
								rec_r[10-:5] <= 5'd0;
								cellmut_r <= 1'b1;
							end
							sv2v_cast_5(pp_acmp_pkg_ACT_A3_C): begin
								bk_r <= 3'd1;
								ord_r <= ord_r;
								xs_r <= 5'd10;
							end
							sv2v_cast_5(pp_acmp_pkg_ACT_A7_C): begin
								bk_r <= 3'd2;
								ord_r <= ord_r;
								xs_r <= 5'd10;
							end
							sv2v_cast_5(pp_acmp_pkg_ACT_A4_C): begin
								act_disc_arm_o <= 1'b1;
								act_disc_talker_eid_o <= rec_r[95-:64];
								rec_r[5-:3] <= pp_acmp_pkg_PB_PASSIVE_C;
								cellmut_r <= 1'b1;
							end
							default: begin
								rec_r[127-:16] <= probe_ctr_r;
								probe_ctr_r <= probe_ctr_r + 16'd1;
								rec_r[14] <= 1'b0;
								rec_r[5-:3] <= pp_acmp_pkg_PB_ACTIVE_C;
								rec_r[10-:5] <= 5'd0;
								cellmut_r <= 1'b1;
								bk_r <= 3'd4;
								ord_r <= ord_r;
								xs_r <= 5'd10;
							end
						endcase
					end
				5'd9:
					if (draw_valid_i) begin
						tmr_arm_valid_o <= 1'b1;
						tmr_arm_cancel_o <= 1'b0;
						tmr_arm_slot_o <= sv2v_cast_13ADE(TMR_BASE_SLOT_P + sv2v_cast_32(sink_r));
						tmr_arm_owner_o <= sv2v_cast_4E301(TMR_OWNER_BASE_P + sv2v_cast_32(sink_r));
						tmr_arm_deadline_ms_o <= now_ms_i + sv2v_cast_32(draw_ms_i);
						draw_issued_r <= 1'b0;
						ord_r <= ord_r + 5'd1;
						xs_r <= 5'd8;
					end
					else if (!draw_issued_r && !draw_busy_i) begin
						draw_req_o <= 1'b1;
						draw_issued_r <= 1'b1;
					end
				5'd10: begin
					txs_alloc_req_o <= 1'b1;
					bwait_r <= 1'b0;
					xs_r <= 5'd11;
				end
				5'd11:
					if (txs_alloc_gnt_i) begin
						bslot_r <= txs_alloc_slot_i;
						bidx_r <= 6'd0;
						xs_r <= 5'd12;
					end
					else if (!bwait_r)
						bwait_r <= 1'b1;
					else
						xs_r <= 5'd10;
				5'd12: begin
					txs_wr_valid_o <= 1'b1;
					txs_wr_addr_o <= sv2v_cast_EFC2D(sv2v_cast_32(bidx_r));
					txs_wr_data_o <= pdu_byte_w;
					if (bidx_r == sv2v_cast_6(55))
						xs_r <= 5'd13;
					else
						bidx_r <= bidx_r + 6'd1;
				end
				5'd13: begin
					txs_wr_commit_o <= 1'b1;
					txs_wr_len_o <= sv2v_cast_EFC2D(pp_acmp_pkg_ACMP_PDU_BYTES_C);
					xs_r <= 5'd14;
				end
				5'd14: begin
					txreq_valid_o <= 1'b1;
					if (bk_r == 3'd4) begin
						tmr_arm_valid_o <= 1'b1;
						tmr_arm_cancel_o <= 1'b0;
						tmr_arm_slot_o <= sv2v_cast_13ADE(TMR_BASE_SLOT_P + sv2v_cast_32(sink_r));
						tmr_arm_owner_o <= sv2v_cast_4E301(TMR_OWNER_BASE_P + sv2v_cast_32(sink_r));
						tmr_arm_deadline_ms_o <= now_ms_i + pp_acmp_pkg_T_ACMP_CMD_MS_C;
					end
					if (errflow_r)
						xs_r <= 5'd16;
					else begin
						ord_r <= ord_r + 5'd1;
						xs_r <= 5'd8;
					end
				end
				5'd15: begin
					act_notify_o <= cellmut_r;
					act_strt_chg_o <= (((cellmut_r && bnd_was_r) && rec_r[11]) && !bind_act_r) && (rec_r[12] != strt_was_r);
					act_strt_cmd_chg_o <= ((((cellmut_r && bnd_was_r) && rec_r[11]) && !bind_act_r) && src_strq_r) && (rec_r[12] != strt_was_r);
					if (src_strq_r) begin
						strq_done_r <= 1'b1;
						strq_fail_r <= 1'b0;
					end
					xs_r <= 5'd16;
				end
				5'd16: begin
					if (src_txn_r && slot_ok_w)
						rxs_free_o <= 1'b1;
					xs_r <= 5'd1;
				end
				default: xs_r <= 5'd1;
			endcase
			if (strm_set_valid_i && strm_set_ready_o) begin
				strq_busy_r <= 1'b0;
				strq_done_r <= 1'b0;
				strq_fail_r <= 1'b0;
			end
			else if (strm_set_valid_i && !strq_busy_r) begin
				strq_pend_r <= 1'b1;
				strq_busy_r <= 1'b1;
				strq_done_r <= 1'b0;
				strq_fail_r <= 1'b0;
				strq_tmo_r <= 1'sb0;
				strq_sink_r <= strm_set_sink_i;
				strq_val_r <= strm_set_val_i;
			end
			if (strq_pend_r && (xs_r != 5'd1)) begin
				if (strq_tmo_r == sv2v_cast_84400(STRM_TIMEOUT_CYC_P - 1)) begin
					strq_pend_r <= 1'b0;
					strq_done_r <= 1'b1;
					strq_fail_r <= 1'b1;
				end
				else
					strq_tmo_r <= strq_tmo_r + sv2v_cast_84400_signed(1);
			end
			else if (!strq_pend_r)
				strq_tmo_r <= 1'sb0;
		end
	end
	initial _sv2v_0 = 0;
endmodule
`default_nettype wire
`default_nettype none
module KL_adp_engine (
	clk_i,
	rst_n,
	entity_enable_i,
	link_up_i,
	gm_change_i,
	gm_id_i,
	gptp_domain_i,
	entity_id_i,
	entity_model_id_i,
	own_mac_i,
	talker_sources_i,
	talker_caps_i,
	listener_sinks_i,
	listener_caps_i,
	current_cfg_i,
	identify_index_i,
	txn_valid_i,
	txn_i,
	txn_ready_o,
	rxs_rd_slot_o,
	rxs_rd_addr_o,
	rxs_rd_en_o,
	rxs_rd_data_i,
	rxs_free_o,
	rxs_free_slot_o,
	prng_draw_req_o,
	prng_draw_kind_o,
	prng_draw_busy_i,
	prng_draw_valid_i,
	prng_draw_ms_i,
	now_ms_i,
	tmr_arm_valid_o,
	tmr_arm_cancel_o,
	tmr_arm_slot_o,
	tmr_arm_owner_o,
	tmr_arm_deadline_ms_o,
	tmr_exp_valid_i,
	tmr_exp_slot_i,
	tmr_exp_owner_i,
	txs_alloc_req_o,
	txs_oversize_o,
	txs_alloc_gnt_i,
	txs_alloc_slot_i,
	txs_wr_slot_o,
	txs_wr_addr_o,
	txs_wr_valid_o,
	txs_wr_data_o,
	txs_wr_commit_o,
	txs_wr_len_o,
	txreq_valid_o,
	txreq_slot_o,
	txreq_if_o,
	bound_i,
	bound_talker_eid_i,
	evt_valid_o,
	evt_departed_o,
	evt_sink_o,
	gm_changed_tick_o,
	dbg_adv_state_o,
	dbg_avail_index_o,
	dbg_tk_discovered_o
);
	reg _sv2v_0;
	parameter [31:0] N_IF_P = 1;
	parameter [31:0] N_SINK_P = 8;
	parameter [31:0] TMR_SLOT_ADV_BASE_P = 0;
	parameter [31:0] TMR_SLOT_NOADP_BASE_P = TMR_SLOT_ADV_BASE_P + N_IF_P;
	parameter [31:0] RX_SLOTS_P = 4;
	parameter [31:0] RX_BYTES_P = 576;
	parameter [31:0] TX_STD_SLOTS_P = 4;
	parameter [31:0] TX_OVERSIZE_BYTES_P = 1600;
	localparam [31:0] pp_pkg_PP_CA_POOL_C = 4;
	localparam [31:0] pp_pkg_PP_N_CTRL_C = 16;
	localparam [31:0] pp_pkg_PP_N_IF_C = 1;
	localparam [31:0] pp_pkg_PP_N_STREAM_IN_C = 8;
	localparam [31:0] pp_pkg_PP_N_STREAM_OUT_C = 8;
	localparam [31:0] pp_pkg_PP_MAAP_SLOTS_C = 2;
	localparam [31:0] pp_pkg_PP_SINGLETON_SLOTS_C = 5;
	localparam [31:0] pp_pkg_PP_SRP_CAD_SLOTS_C = 7;
	function automatic [415:0] pp_pkg_pp_timer_map;
		input reg [31:0] n_if;
		input reg [31:0] si;
		input reg [31:0] so;
		input reg [31:0] n_ctrl;
		input reg [31:0] ca_pool;
		reg [415:0] m;
		begin
			m[415-:32] = 32'd0;
			m[383-:32] = m[415-:32] + n_if;
			m[351-:32] = m[383-:32] + si;
			m[319-:32] = m[351-:32] + si;
			m[287-:32] = m[319-:32] + so;
			m[255-:32] = m[287-:32] + ((32'd2 * n_ctrl) * n_if);
			m[223-:32] = m[255-:32] + ca_pool;
			m[191-:32] = m[223-:32] + pp_pkg_PP_SINGLETON_SLOTS_C;
			m[159-:32] = m[191-:32] + pp_pkg_PP_MAAP_SLOTS_C;
			m[127-:32] = m[159-:32];
			m[95-:32] = m[127-:32] + pp_pkg_PP_SRP_CAD_SLOTS_C;
			m[63-:32] = m[95-:32] + so;
			m[31-:32] = m[127-:32] + (((pp_pkg_PP_SRP_CAD_SLOTS_C + si) + so) * n_if);
			pp_pkg_pp_timer_map = m;
		end
	endfunction
	function automatic [31:0] pp_pkg_pp_timer_slots;
		input reg [31:0] n_if;
		input reg [31:0] si;
		input reg [31:0] so;
		input reg [31:0] n_ctrl;
		input reg [31:0] ca_pool;
		input reg en_srp;
		reg [415:0] m;
		begin
			m = pp_pkg_pp_timer_map(n_if, si, so, n_ctrl, ca_pool);
			pp_pkg_pp_timer_slots = (en_srp ? m[31-:32] : m[159-:32]);
		end
	endfunction
	localparam [31:0] pp_pkg_PP_TIMER_SLOTS_C = pp_pkg_pp_timer_slots(pp_pkg_PP_N_IF_C, pp_pkg_PP_N_STREAM_IN_C, pp_pkg_PP_N_STREAM_OUT_C, pp_pkg_PP_N_CTRL_C, pp_pkg_PP_CA_POOL_C, 1'b1);
	parameter [31:0] TMR_SLOTS_P = pp_pkg_PP_TIMER_SLOTS_C;
	localparam [31:0] IF_W_C = (N_IF_P > 1 ? $clog2(N_IF_P) : 1);
	localparam [31:0] SNK_W_C = (N_SINK_P > 1 ? $clog2(N_SINK_P) : 1);
	localparam [31:0] TMR_AW_C = (TMR_SLOTS_P > 32'd1 ? $clog2(TMR_SLOTS_P) : 32'd1);
	localparam [31:0] RXS_SLOT_W_C = (RX_SLOTS_P > 1 ? $clog2(RX_SLOTS_P) : 1);
	localparam [31:0] RXS_ADDR_W_C = $clog2(RX_BYTES_P);
	localparam [31:0] TXS_SLOT_W_C = $clog2(TX_STD_SLOTS_P + 1);
	localparam [31:0] TXS_LEN_W_C = $clog2(TX_OVERSIZE_BYTES_P + 1);
	input wire clk_i;
	input wire rst_n;
	input wire entity_enable_i;
	input wire [N_IF_P - 1:0] link_up_i;
	input wire [N_IF_P - 1:0] gm_change_i;
	input wire [(N_IF_P * 64) - 1:0] gm_id_i;
	input wire [(N_IF_P * 8) - 1:0] gptp_domain_i;
	input wire [63:0] entity_id_i;
	input wire [63:0] entity_model_id_i;
	input wire [47:0] own_mac_i;
	input wire [15:0] talker_sources_i;
	input wire [15:0] talker_caps_i;
	input wire [15:0] listener_sinks_i;
	input wire [15:0] listener_caps_i;
	input wire [15:0] current_cfg_i;
	input wire [15:0] identify_index_i;
	input wire txn_valid_i;
	localparam [31:0] pp_pkg_PP_TXN_W_C = 393;
	input wire [392:0] txn_i;
	output wire txn_ready_o;
	output wire [RXS_SLOT_W_C - 1:0] rxs_rd_slot_o;
	output wire [RXS_ADDR_W_C - 1:0] rxs_rd_addr_o;
	output wire rxs_rd_en_o;
	input wire [7:0] rxs_rd_data_i;
	output wire rxs_free_o;
	output wire [RXS_SLOT_W_C - 1:0] rxs_free_slot_o;
	output wire prng_draw_req_o;
	output wire [2:0] prng_draw_kind_o;
	input wire prng_draw_busy_i;
	input wire prng_draw_valid_i;
	input wire [15:0] prng_draw_ms_i;
	input wire [31:0] now_ms_i;
	output reg tmr_arm_valid_o;
	output reg tmr_arm_cancel_o;
	output reg [TMR_AW_C - 1:0] tmr_arm_slot_o;
	localparam [31:0] pp_pkg_PP_TIMER_OWNER_W_C = 8;
	output wire [7:0] tmr_arm_owner_o;
	output reg [31:0] tmr_arm_deadline_ms_o;
	input wire tmr_exp_valid_i;
	input wire [TMR_AW_C - 1:0] tmr_exp_slot_i;
	input wire [7:0] tmr_exp_owner_i;
	output wire txs_alloc_req_o;
	output wire txs_oversize_o;
	input wire txs_alloc_gnt_i;
	input wire [TXS_SLOT_W_C - 1:0] txs_alloc_slot_i;
	output wire [TXS_SLOT_W_C - 1:0] txs_wr_slot_o;
	output wire [TXS_LEN_W_C - 1:0] txs_wr_addr_o;
	output wire txs_wr_valid_o;
	output wire [7:0] txs_wr_data_o;
	output wire txs_wr_commit_o;
	output wire [TXS_LEN_W_C - 1:0] txs_wr_len_o;
	output wire txreq_valid_o;
	output wire [TXS_SLOT_W_C - 1:0] txreq_slot_o;
	output wire [IF_W_C - 1:0] txreq_if_o;
	input wire [N_SINK_P - 1:0] bound_i;
	input wire [(N_SINK_P * 64) - 1:0] bound_talker_eid_i;
	output reg evt_valid_o;
	output reg evt_departed_o;
	output reg [SNK_W_C - 1:0] evt_sink_o;
	output wire [N_IF_P - 1:0] gm_changed_tick_o;
	output reg [(N_IF_P * 2) - 1:0] dbg_adv_state_o;
	output reg [(N_IF_P * 32) - 1:0] dbg_avail_index_o;
	output wire [N_SINK_P - 1:0] dbg_tk_discovered_o;
	wire [392:0] txn_in_w;
	function automatic [392:0] sv2v_cast_393;
		input reg [392:0] inp;
		sv2v_cast_393 = inp;
	endfunction
	assign txn_in_w = sv2v_cast_393(txn_i);
	function automatic [7:0] byte64_f;
		input reg [63:0] v;
		input reg [31:0] n;
		reg [63:0] sh;
		begin
			sh = v >> (8 * (7 - n));
			byte64_f = sh[7:0];
		end
	endfunction
	function automatic [7:0] byte48_f;
		input reg [47:0] v;
		input reg [31:0] n;
		reg [47:0] sh;
		begin
			sh = v >> (8 * (5 - n));
			byte48_f = sh[7:0];
		end
	endfunction
	function automatic [7:0] byte32_f;
		input reg [31:0] v;
		input reg [31:0] n;
		reg [31:0] sh;
		begin
			sh = v >> (8 * (3 - n));
			byte32_f = sh[7:0];
		end
	endfunction
	function automatic [7:0] byte16_f;
		input reg [15:0] v;
		input reg [31:0] n;
		reg [15:0] sh;
		begin
			sh = v >> (8 * (1 - n));
			byte16_f = sh[7:0];
		end
	endfunction
	function automatic [31:0] sv2v_cast_32;
		input reg [31:0] inp;
		sv2v_cast_32 = inp;
	endfunction
	function automatic [63:0] gm_slice_f;
		input reg [IF_W_C - 1:0] ifx;
		reg [31:0] i;
		begin
			i = (sv2v_cast_32(ifx) < N_IF_P ? sv2v_cast_32(ifx) : 32'd0);
			gm_slice_f = gm_id_i[64 * i+:64];
		end
	endfunction
	function automatic [7:0] dom_slice_f;
		input reg [IF_W_C - 1:0] ifx;
		reg [31:0] i;
		begin
			i = (sv2v_cast_32(ifx) < N_IF_P ? sv2v_cast_32(ifx) : 32'd0);
			dom_slice_f = gptp_domain_i[8 * i+:8];
		end
	endfunction
	reg [N_IF_P - 1:0] link_q_r;
	reg enable_q_r;
	reg [N_SINK_P - 1:0] bound_q_r;
	reg [N_IF_P - 1:0] gm_tick_r;
	wire [N_IF_P - 1:0] link_fall_w;
	wire [N_IF_P - 1:0] link_rise_w;
	wire enable_rise_w;
	wire enable_fall_w;
	wire [N_SINK_P - 1:0] bound_fall_w;
	assign link_fall_w = link_q_r & ~link_up_i;
	assign link_rise_w = ~link_q_r & link_up_i;
	assign enable_rise_w = entity_enable_i && !enable_q_r;
	assign enable_fall_w = !entity_enable_i && enable_q_r;
	assign bound_fall_w = bound_q_r & ~bound_i;
	always @(posedge clk_i) begin : edge_sync
		if (!rst_n) begin
			link_q_r <= 1'sb0;
			enable_q_r <= 1'b0;
			bound_q_r <= 1'sb0;
			gm_tick_r <= 1'sb0;
		end
		else begin
			link_q_r <= link_up_i;
			enable_q_r <= entity_enable_i;
			bound_q_r <= bound_i;
			gm_tick_r <= gm_change_i;
		end
	end
	assign gm_changed_tick_o = gm_tick_r;
	localparam [31:0] PDU_FLD_FIRST_C = 36;
	localparam [31:0] PDU_FLD_LAST_C = 55;
	reg [3:0] rx_st_r;
	reg [3:0] rxq_msg_r;
	reg [63:0] rxq_eid_r;
	reg [4:0] rxq_vt_r;
	reg [IF_W_C - 1:0] rxq_if_r;
	reg [2:0] rxq_slot_r;
	reg [5:0] rd_ptr_r;
	reg cap_vld_r;
	reg [5:0] cap_idx_r;
	reg [31:0] rx_aidx_r;
	reg [63:0] rx_gm_r;
	reg [7:0] rx_dom_r;
	reg [15:0] rx_ifx_r;
	reg [SNK_W_C - 1:0] sink_r;
	wire rx_have_slot_w;
	localparam [2:0] pp_pkg_PP_SLOT_NULL_C = 3'd7;
	assign rx_have_slot_w = (rxq_slot_r != pp_pkg_PP_SLOT_NULL_C) && (sv2v_cast_32(rxq_slot_r) < RX_SLOTS_P);
	reg [N_SINK_P - 1:0] match_w;
	always @(*) begin : sink_match
		if (_sv2v_0)
			;
		begin : sv2v_autoblock_1
			reg [31:0] s;
			for (s = 0; s < N_SINK_P; s = s + 1)
				match_w[s] = bound_i[s] && (bound_talker_eid_i[64 * s+:64] == rxq_eid_r);
		end
	end
	reg [47:0] disc_rec_r [0:N_SINK_P - 1];
	reg [47:0] disc_rec_q_r;
	wire rec_rd_en_w;
	reg rec_wr_en_w;
	reg [47:0] rec_wr_data_w;
	reg [N_SINK_P - 1:0] disc_st_r;
	wire [15:0] rec_ifx_w;
	wire [31:0] rec_aidx_w;
	assign {rec_ifx_w, rec_aidx_w} = disc_rec_q_r;
	wire gm_dom_ok_w;
	assign gm_dom_ok_w = (rx_gm_r == gm_slice_f(rxq_if_r)) && (rx_dom_r == dom_slice_f(rxq_if_r));
	reg ev_dep_w;
	reg ev_disc_w;
	reg st_set_w;
	reg st_clr_w;
	reg iter_arm_w;
	reg iter_cancel_w;
	localparam [3:0] pp_adp_pkg_ADP_MSG_AVAILABLE_C = 4'd0;
	localparam [3:0] pp_adp_pkg_ADP_MSG_DEPARTING_C = 4'd1;
	always @(*) begin : disc_eval
		if (_sv2v_0)
			;
		ev_dep_w = 1'b0;
		ev_disc_w = 1'b0;
		st_set_w = 1'b0;
		st_clr_w = 1'b0;
		iter_arm_w = 1'b0;
		iter_cancel_w = 1'b0;
		rec_wr_en_w = 1'b0;
		rec_wr_data_w = {rx_ifx_r, rx_aidx_r};
		if (rx_st_r == 4'd4) begin
			if (rxq_msg_r == pp_adp_pkg_ADP_MSG_AVAILABLE_C) begin
				if (!disc_st_r[sink_r]) begin
					if (gm_dom_ok_w) begin
						ev_disc_w = 1'b1;
						st_set_w = 1'b1;
						rec_wr_en_w = 1'b1;
						iter_arm_w = 1'b1;
					end
				end
				else if (rx_ifx_r == rec_ifx_w) begin
					if (rx_aidx_r > rec_aidx_w) begin
						rec_wr_en_w = 1'b1;
						iter_arm_w = 1'b1;
					end
					else if (gm_dom_ok_w) begin
						ev_dep_w = 1'b1;
						ev_disc_w = 1'b1;
						rec_wr_en_w = 1'b1;
						iter_arm_w = 1'b1;
					end
					else begin
						ev_dep_w = 1'b1;
						st_clr_w = 1'b1;
						iter_cancel_w = 1'b1;
					end
				end
			end
			else if (rxq_msg_r == pp_adp_pkg_ADP_MSG_DEPARTING_C) begin
				if (disc_st_r[sink_r] && (rx_ifx_r == rec_ifx_w)) begin
					ev_dep_w = 1'b1;
					st_clr_w = 1'b1;
					iter_cancel_w = 1'b1;
				end
			end
		end
	end
	assign rec_rd_en_w = rx_st_r == 4'd3;
	always @(posedge clk_i) begin : disc_rec_ram
		if (rec_rd_en_w)
			disc_rec_q_r <= disc_rec_r[sink_r];
		if (rec_wr_en_w)
			disc_rec_r[sink_r] <= rec_wr_data_w;
	end
	wire noadp_exp_w;
	wire [31:0] exp_slot_ext_w;
	wire [31:0] noadp_rel_w;
	wire [SNK_W_C - 1:0] noadp_exp_sink_w;
	assign exp_slot_ext_w = {{32 - TMR_AW_C {1'b0}}, tmr_exp_slot_i};
	assign noadp_rel_w = exp_slot_ext_w - TMR_SLOT_NOADP_BASE_P;
	assign noadp_exp_w = tmr_exp_valid_i && (noadp_rel_w < N_SINK_P);
	function automatic [SNK_W_C - 1:0] sv2v_cast_B2660;
		input reg [SNK_W_C - 1:0] inp;
		sv2v_cast_B2660 = inp;
	endfunction
	assign noadp_exp_sink_w = sv2v_cast_B2660(noadp_rel_w);
	always @(posedge clk_i) begin : disc_state
		if (!rst_n)
			disc_st_r <= 1'sb0;
		else begin
			if (noadp_exp_w)
				disc_st_r[noadp_exp_sink_w] <= 1'b0;
			begin : sv2v_autoblock_2
				reg [31:0] s;
				for (s = 0; s < N_SINK_P; s = s + 1)
					if (bound_fall_w[s])
						disc_st_r[s] <= 1'b0;
			end
			if (st_set_w)
				disc_st_r[sink_r] <= 1'b1;
			if (st_clr_w)
				disc_st_r[sink_r] <= 1'b0;
		end
	end
	assign dbg_tk_discovered_o = disc_st_r;
	reg txn_in_valid_q_r;
	wire disc_hit_w;
	wire [IF_W_C - 1:0] disc_hit_if_w;
	localparam [3:0] pp_adp_pkg_ADP_MSG_DISCOVER_C = 4'd2;
	assign disc_hit_w = (((rx_st_r == 4'd1) && txn_in_valid_q_r) && (rxq_msg_r == pp_adp_pkg_ADP_MSG_DISCOVER_C)) && ((rxq_eid_r == 64'd0) || (rxq_eid_r == entity_id_i));
	assign disc_hit_if_w = rxq_if_r;
	function automatic [IF_W_C - 1:0] sv2v_cast_6AF68;
		input reg [IF_W_C - 1:0] inp;
		sv2v_cast_6AF68 = inp;
	endfunction
	function automatic [5:0] sv2v_cast_6;
		input reg [5:0] inp;
		sv2v_cast_6 = inp;
	endfunction
	function automatic signed [SNK_W_C - 1:0] sv2v_cast_B2660_signed;
		input reg signed [SNK_W_C - 1:0] inp;
		sv2v_cast_B2660_signed = inp;
	endfunction
	always @(posedge clk_i) begin : rx_pipe
		if (!rst_n) begin
			rx_st_r <= 4'd0;
			rxq_msg_r <= 4'd0;
			rxq_eid_r <= 64'd0;
			rxq_vt_r <= 5'd0;
			rxq_if_r <= 1'sb0;
			rxq_slot_r <= pp_pkg_PP_SLOT_NULL_C;
			rd_ptr_r <= 6'd0;
			cap_vld_r <= 1'b0;
			cap_idx_r <= 6'd0;
			rx_aidx_r <= 32'd0;
			rx_gm_r <= 64'd0;
			rx_dom_r <= 8'd0;
			rx_ifx_r <= 16'd0;
			sink_r <= 1'sb0;
			txn_in_valid_q_r <= 1'b0;
		end
		else begin
			cap_vld_r <= 1'b0;
			(* full_case, parallel_case *)
			case (rx_st_r)
				4'd0:
					if (txn_valid_i) begin
						rxq_msg_r <= txn_in_w[353-:4];
						rxq_eid_r <= txn_in_w[221-:64];
						rxq_vt_r <= txn_in_w[349-:5];
						rxq_if_r <= sv2v_cast_6AF68(txn_in_w[390-:2]);
						rxq_slot_r <= txn_in_w[59-:3];
						txn_in_valid_q_r <= txn_in_w[356-:3] == 3'd0;
						rx_st_r <= 4'd1;
					end
				4'd1:
					if ((txn_in_valid_q_r && ((rxq_msg_r == pp_adp_pkg_ADP_MSG_AVAILABLE_C) || (rxq_msg_r == pp_adp_pkg_ADP_MSG_DEPARTING_C))) && rx_have_slot_w) begin
						rd_ptr_r <= sv2v_cast_6(PDU_FLD_FIRST_C);
						rx_st_r <= 4'd2;
					end
					else
						rx_st_r <= 4'd7;
				4'd2: begin
					cap_vld_r <= 1'b1;
					cap_idx_r <= rd_ptr_r;
					if (rd_ptr_r != sv2v_cast_6(PDU_FLD_LAST_C))
						rd_ptr_r <= rd_ptr_r + 6'd1;
					if (cap_vld_r) begin
						if (cap_idx_r <= 6'd39)
							rx_aidx_r <= {rx_aidx_r[23:0], rxs_rd_data_i};
						else if (cap_idx_r <= 6'd47)
							rx_gm_r <= {rx_gm_r[55:0], rxs_rd_data_i};
						else if (cap_idx_r == 6'd48)
							rx_dom_r <= rxs_rd_data_i;
						else if (cap_idx_r >= 6'd54)
							rx_ifx_r <= {rx_ifx_r[7:0], rxs_rd_data_i};
						if (cap_idx_r == sv2v_cast_6(PDU_FLD_LAST_C)) begin
							sink_r <= 1'sb0;
							rx_st_r <= 4'd3;
						end
					end
				end
				4'd3:
					if (match_w[sink_r])
						rx_st_r <= 4'd4;
					else
						rx_st_r <= 4'd6;
				4'd4:
					if (ev_dep_w && ev_disc_w)
						rx_st_r <= 4'd5;
					else
						rx_st_r <= 4'd6;
				4'd5: rx_st_r <= 4'd6;
				4'd6:
					if (sv2v_cast_32(sink_r) == (N_SINK_P - 1))
						rx_st_r <= 4'd7;
					else begin
						sink_r <= sink_r + sv2v_cast_B2660_signed(1);
						rx_st_r <= 4'd3;
					end
				4'd7: rx_st_r <= 4'd0;
				default: rx_st_r <= 4'd0;
			endcase
		end
	end
	assign txn_ready_o = rx_st_r == 4'd0;
	assign rxs_rd_slot_o = rxq_slot_r[RXS_SLOT_W_C - 1:0];
	function automatic [RXS_ADDR_W_C - 1:0] sv2v_cast_E1968;
		input reg [RXS_ADDR_W_C - 1:0] inp;
		sv2v_cast_E1968 = inp;
	endfunction
	assign rxs_rd_addr_o = sv2v_cast_E1968(rd_ptr_r);
	assign rxs_rd_en_o = rx_st_r == 4'd2;
	assign rxs_free_o = (rx_st_r == 4'd7) && rx_have_slot_w;
	assign rxs_free_slot_o = rxq_slot_r[RXS_SLOT_W_C - 1:0];
	reg [1:0] adv_st_r [0:N_IF_P - 1];
	reg [N_IF_P - 1:0] adv_startup_r;
	reg [1:0] tpend_r [0:N_IF_P - 1];
	reg [31:0] tpend_deadline_r [0:N_IF_P - 1];
	reg [N_IF_P - 1:0] pend_avail_r;
	reg [N_IF_P - 1:0] pend_dep_r;
	wire adv_exp_w;
	wire [31:0] adv_rel_w;
	wire [IF_W_C - 1:0] adv_exp_if_w;
	assign adv_rel_w = exp_slot_ext_w - TMR_SLOT_ADV_BASE_P;
	assign adv_exp_w = tmr_exp_valid_i && (adv_rel_w < N_IF_P);
	assign adv_exp_if_w = sv2v_cast_6AF68(adv_rel_w);
	wire draw_del_w;
	wire [IF_W_C - 1:0] draw_del_if_w;
	wire [15:0] draw_del_ms_w;
	wire bld_done_avail_w;
	wire bld_done_dep_w;
	wire [IF_W_C - 1:0] bld_done_if_w;
	wire tpend_issue_w;
	wire [IF_W_C - 1:0] tpend_issue_if_w;
	localparam [31:0] pp_adp_pkg_ADP_T_ADV_MS_C = 32'd5000;
	always @(posedge clk_i) begin : adv_sm
		if (!rst_n) begin
			begin : sv2v_autoblock_3
				reg [31:0] i;
				for (i = 0; i < N_IF_P; i = i + 1)
					begin
						adv_st_r[i] <= 2'd0;
						tpend_r[i] <= 2'd0;
						tpend_deadline_r[i] <= 32'd0;
					end
			end
			adv_startup_r <= 1'sb0;
		end
		else begin
			if (tpend_issue_w)
				tpend_r[tpend_issue_if_w] <= 2'd0;
			begin : sv2v_autoblock_4
				reg [31:0] i;
				for (i = 0; i < N_IF_P; i = i + 1)
					begin
						if (adv_exp_w && (sv2v_cast_32(adv_exp_if_w) == i)) begin
							if (adv_st_r[i] == 2'd2)
								adv_st_r[i] <= 2'd3;
							else if (adv_st_r[i] == 2'd3) begin
								adv_st_r[i] <= 2'd1;
								adv_startup_r[i] <= 1'b0;
							end
						end
						if ((disc_hit_w && (sv2v_cast_32(disc_hit_if_w) == i)) && (adv_st_r[i] == 2'd3)) begin
							adv_st_r[i] <= 2'd1;
							adv_startup_r[i] <= 1'b0;
							tpend_r[i] <= 2'd2;
						end
						if (gm_change_i[i] && (adv_st_r[i] == 2'd3)) begin
							adv_st_r[i] <= 2'd1;
							adv_startup_r[i] <= 1'b0;
							tpend_r[i] <= 2'd2;
						end
						if ((draw_del_w && (sv2v_cast_32(draw_del_if_w) == i)) && (adv_st_r[i] == 2'd1)) begin
							adv_st_r[i] <= 2'd2;
							tpend_r[i] <= 2'd1;
							tpend_deadline_r[i] <= now_ms_i + {16'd0, draw_del_ms_w};
						end
						if ((bld_done_avail_w && (sv2v_cast_32(bld_done_if_w) == i)) && (adv_st_r[i] == 2'd3)) begin
							tpend_r[i] <= 2'd1;
							tpend_deadline_r[i] <= now_ms_i + pp_adp_pkg_ADP_T_ADV_MS_C;
						end
						if (link_fall_w[i] && (adv_st_r[i] != 2'd0)) begin
							adv_st_r[i] <= 2'd0;
							tpend_r[i] <= 2'd2;
						end
						if (enable_fall_w && (adv_st_r[i] != 2'd0)) begin
							adv_st_r[i] <= 2'd0;
							tpend_r[i] <= 2'd2;
						end
						if ((entity_enable_i && !enable_fall_w) && (adv_st_r[i] == 2'd0)) begin
							if (enable_rise_w && link_up_i[i]) begin
								adv_st_r[i] <= 2'd1;
								adv_startup_r[i] <= 1'b1;
							end
							else if (link_rise_w[i] && !enable_rise_w) begin
								adv_st_r[i] <= 2'd1;
								adv_startup_r[i] <= 1'b0;
							end
						end
					end
			end
		end
	end
	wire bld_take_w;
	wire bld_take_dep_w;
	wire [IF_W_C - 1:0] bld_take_if_w;
	always @(posedge clk_i) begin : send_queue
		if (!rst_n) begin
			pend_avail_r <= 1'sb0;
			pend_dep_r <= 1'sb0;
		end
		else begin : sv2v_autoblock_5
			reg [31:0] i;
			for (i = 0; i < N_IF_P; i = i + 1)
				begin
					if ((adv_exp_w && (sv2v_cast_32(adv_exp_if_w) == i)) && (adv_st_r[i] == 2'd2))
						pend_avail_r[i] <= 1'b1;
					if (enable_fall_w && (adv_st_r[i] != 2'd0)) begin
						pend_dep_r[i] <= 1'b1;
						pend_avail_r[i] <= 1'b0;
					end
					if (link_fall_w[i])
						pend_avail_r[i] <= 1'b0;
					if (bld_take_w && (sv2v_cast_32(bld_take_if_w) == i)) begin
						if (bld_take_dep_w)
							pend_dep_r[i] <= 1'b0;
						else
							pend_avail_r[i] <= 1'b0;
					end
				end
		end
	end
	reg [31:0] aidx_r [0:N_IF_P - 1];
	always @(posedge clk_i) begin : avail_index_mgr
		if (!rst_n) begin : sv2v_autoblock_6
			reg [31:0] i;
			for (i = 0; i < N_IF_P; i = i + 1)
				aidx_r[i] <= 32'd0;
		end
		else begin
			if (bld_done_avail_w)
				aidx_r[bld_done_if_w] <= aidx_r[bld_done_if_w] + 32'd1;
			if (bld_done_dep_w)
				aidx_r[bld_done_if_w] <= 32'd0;
		end
	end
	reg draw_act_r;
	reg [IF_W_C - 1:0] draw_if_r;
	reg [2:0] draw_kind_r;
	reg draw_req_r;
	reg [2:0] draw_req_kind_r;
	reg draw_need_w;
	reg [IF_W_C - 1:0] draw_need_if_w;
	reg [2:0] draw_need_kind_w;
	localparam [2:0] pp_adp_pkg_ADP_DRAW_KIND_DELAY_C = 3'd2;
	localparam [2:0] pp_adp_pkg_ADP_DRAW_KIND_START_C = 3'd1;
	always @(*) begin : draw_pick
		if (_sv2v_0)
			;
		draw_need_w = 1'b0;
		draw_need_if_w = 1'sb0;
		draw_need_kind_w = pp_adp_pkg_ADP_DRAW_KIND_DELAY_C;
		begin : sv2v_autoblock_7
			reg [31:0] i;
			for (i = 0; i < N_IF_P; i = i + 1)
				if (!draw_need_w && (adv_st_r[i] == 2'd1)) begin
					draw_need_w = 1'b1;
					draw_need_if_w = sv2v_cast_6AF68(i);
					draw_need_kind_w = (adv_startup_r[i] ? pp_adp_pkg_ADP_DRAW_KIND_START_C : pp_adp_pkg_ADP_DRAW_KIND_DELAY_C);
				end
		end
	end
	wire [2:0] draw_want_now_w;
	assign draw_want_now_w = (adv_startup_r[draw_if_r] ? pp_adp_pkg_ADP_DRAW_KIND_START_C : pp_adp_pkg_ADP_DRAW_KIND_DELAY_C);
	assign draw_del_w = ((prng_draw_valid_i && draw_act_r) && (adv_st_r[draw_if_r] == 2'd1)) && (draw_want_now_w == draw_kind_r);
	assign draw_del_if_w = draw_if_r;
	assign draw_del_ms_w = prng_draw_ms_i;
	always @(posedge clk_i) begin : prng_serializer
		if (!rst_n) begin
			draw_act_r <= 1'b0;
			draw_if_r <= 1'sb0;
			draw_kind_r <= 3'd0;
			draw_req_r <= 1'b0;
			draw_req_kind_r <= 3'd0;
		end
		else begin
			draw_req_r <= 1'b0;
			if (draw_act_r) begin
				if (prng_draw_valid_i)
					draw_act_r <= 1'b0;
			end
			else if ((draw_need_w && !prng_draw_busy_i) && !draw_req_r) begin
				draw_req_r <= 1'b1;
				draw_req_kind_r <= draw_need_kind_w;
				draw_if_r <= draw_need_if_w;
				draw_kind_r <= draw_need_kind_w;
				draw_act_r <= 1'b1;
			end
		end
	end
	assign prng_draw_req_o = draw_req_r;
	assign prng_draw_kind_o = draw_req_kind_r;
	reg [2:0] bld_st_r;
	reg bld_dep_r;
	reg [IF_W_C - 1:0] bld_if_r;
	reg [TXS_SLOT_W_C - 1:0] bld_slot_r;
	reg [6:0] bld_idx_r;
	reg [63:0] bld_gm_r;
	reg [7:0] bld_dom_r;
	reg [31:0] bld_aidx_r;
	reg pick_vld_w;
	reg pick_dep_w;
	reg [IF_W_C - 1:0] pick_if_w;
	always @(*) begin : bld_pick
		if (_sv2v_0)
			;
		pick_vld_w = 1'b0;
		pick_dep_w = 1'b0;
		pick_if_w = 1'sb0;
		begin : sv2v_autoblock_8
			reg [31:0] i;
			for (i = 0; i < N_IF_P; i = i + 1)
				if (!pick_vld_w && pend_dep_r[i]) begin
					pick_vld_w = 1'b1;
					pick_dep_w = 1'b1;
					pick_if_w = sv2v_cast_6AF68(i);
				end
		end
		begin : sv2v_autoblock_9
			reg [31:0] i;
			for (i = 0; i < N_IF_P; i = i + 1)
				if (!pick_vld_w && pend_avail_r[i]) begin
					pick_vld_w = 1'b1;
					pick_dep_w = 1'b0;
					pick_if_w = sv2v_cast_6AF68(i);
				end
		end
	end
	assign bld_take_w = (bld_st_r == 3'd0) && pick_vld_w;
	assign bld_take_dep_w = pick_dep_w;
	assign bld_take_if_w = pick_if_w;
	localparam [10:0] pp_adp_pkg_ADP_CDL_C = 11'd56;
	localparam [31:0] pp_adp_pkg_ADP_ENTITY_CAPS_C = 32'h0000c588;
	localparam [15:0] pp_adp_pkg_ADP_ETHERTYPE_C = 16'h22f0;
	localparam [47:0] pp_adp_pkg_ADP_MCAST_DA_C = 48'h91e0f0010000;
	localparam [7:0] pp_adp_pkg_ADP_SUBTYPE_C = 8'hfa;
	localparam [4:0] pp_adp_pkg_ADP_VALID_TIME_C = 5'd10;
	function automatic [7:0] frame_byte_f;
		input reg [6:0] idx;
		input reg dep;
		input reg [IF_W_C - 1:0] ifx;
		input reg [63:0] gm;
		input reg [7:0] dom;
		input reg [31:0] aidx;
		reg [31:0] i;
		reg [7:0] b;
		begin
			i = sv2v_cast_32(idx);
			b = 8'h00;
			if (i < 6)
				b = byte48_f(pp_adp_pkg_ADP_MCAST_DA_C, i);
			else if (i < 12)
				b = byte48_f(own_mac_i, i - 6);
			else if (i < 14)
				b = byte16_f(pp_adp_pkg_ADP_ETHERTYPE_C, i - 12);
			else if (i == 14)
				b = pp_adp_pkg_ADP_SUBTYPE_C;
			else if (i == 15)
				b = {4'b0000, (dep ? pp_adp_pkg_ADP_MSG_DEPARTING_C : pp_adp_pkg_ADP_MSG_AVAILABLE_C)};
			else if (i == 16)
				b = {(dep ? 5'd0 : pp_adp_pkg_ADP_VALID_TIME_C), pp_adp_pkg_ADP_CDL_C[10:8]};
			else if (i == 17)
				b = pp_adp_pkg_ADP_CDL_C[7:0];
			else if (i < 26)
				b = byte64_f(entity_id_i, i - 18);
			else if (i < 34)
				b = byte64_f(entity_model_id_i, i - 26);
			else if (i < 38)
				b = byte32_f(pp_adp_pkg_ADP_ENTITY_CAPS_C, i - 34);
			else if (i < 40)
				b = byte16_f(talker_sources_i, i - 38);
			else if (i < 42)
				b = byte16_f(talker_caps_i, i - 40);
			else if (i < 44)
				b = byte16_f(listener_sinks_i, i - 42);
			else if (i < 46)
				b = byte16_f(listener_caps_i, i - 44);
			else if (i < 50)
				b = 8'h00;
			else if (i < 54)
				b = byte32_f(aidx, i - 50);
			else if (i < 62)
				b = byte64_f(gm, i - 54);
			else if (i == 62)
				b = dom;
			else if (i == 63)
				b = 8'h00;
			else if (i < 66)
				b = byte16_f(current_cfg_i, i - 64);
			else if (i < 68)
				b = byte16_f(identify_index_i, i - 66);
			else if (i < 70)
				b = byte16_f({{16 - IF_W_C {1'b0}}, ifx}, i - 68);
			else
				b = 8'h00;
			frame_byte_f = b;
		end
	endfunction
	localparam [31:0] pp_adp_pkg_ADP_FRAME_BYTES_C = 82;
	always @(posedge clk_i) begin : builder
		if (!rst_n) begin
			bld_st_r <= 3'd0;
			bld_dep_r <= 1'b0;
			bld_if_r <= 1'sb0;
			bld_slot_r <= 1'sb0;
			bld_idx_r <= 7'd0;
			bld_gm_r <= 64'd0;
			bld_dom_r <= 8'd0;
			bld_aidx_r <= 32'd0;
		end
		else
			(* full_case, parallel_case *)
			case (bld_st_r)
				3'd0:
					if (pick_vld_w) begin
						bld_dep_r <= pick_dep_w;
						bld_if_r <= pick_if_w;
						bld_st_r <= 3'd1;
					end
				3'd1: begin
					bld_gm_r <= gm_slice_f(bld_if_r);
					bld_dom_r <= dom_slice_f(bld_if_r);
					bld_aidx_r <= aidx_r[bld_if_r];
					bld_st_r <= 3'd2;
				end
				3'd2: bld_st_r <= 3'd3;
				3'd3:
					if (txs_alloc_gnt_i) begin
						bld_slot_r <= txs_alloc_slot_i;
						bld_idx_r <= 7'd0;
						bld_st_r <= 3'd4;
					end
					else
						bld_st_r <= 3'd2;
				3'd4:
					if (sv2v_cast_32(bld_idx_r) == 81)
						bld_st_r <= 3'd5;
					else
						bld_idx_r <= bld_idx_r + 7'd1;
				3'd5: bld_st_r <= 3'd6;
				3'd6: bld_st_r <= 3'd0;
				default: bld_st_r <= 3'd0;
			endcase
	end
	assign txs_alloc_req_o = bld_st_r == 3'd2;
	assign txs_oversize_o = 1'b0;
	assign txs_wr_slot_o = bld_slot_r;
	function automatic [TXS_LEN_W_C - 1:0] sv2v_cast_EFC2D;
		input reg [TXS_LEN_W_C - 1:0] inp;
		sv2v_cast_EFC2D = inp;
	endfunction
	assign txs_wr_addr_o = sv2v_cast_EFC2D(bld_idx_r);
	assign txs_wr_valid_o = bld_st_r == 3'd4;
	assign txs_wr_data_o = frame_byte_f(bld_idx_r, bld_dep_r, bld_if_r, bld_gm_r, bld_dom_r, bld_aidx_r);
	assign txs_wr_commit_o = bld_st_r == 3'd5;
	assign txs_wr_len_o = sv2v_cast_EFC2D(pp_adp_pkg_ADP_FRAME_BYTES_C);
	assign txreq_valid_o = bld_st_r == 3'd6;
	assign txreq_slot_o = bld_slot_r;
	assign txreq_if_o = bld_if_r;
	assign bld_done_avail_w = (bld_st_r == 3'd6) && !bld_dep_r;
	assign bld_done_dep_w = (bld_st_r == 3'd6) && bld_dep_r;
	assign bld_done_if_w = bld_if_r;
	reg [N_SINK_P - 1:0] ucancel_pend_r;
	reg ucancel_issue_w;
	reg [SNK_W_C - 1:0] ucancel_sink_w;
	always @(*) begin : ucancel_pick
		if (_sv2v_0)
			;
		ucancel_issue_w = 1'b0;
		ucancel_sink_w = 1'sb0;
		begin : sv2v_autoblock_10
			reg [31:0] s;
			for (s = 0; s < N_SINK_P; s = s + 1)
				if (!ucancel_issue_w && ucancel_pend_r[s]) begin
					ucancel_issue_w = 1'b1;
					ucancel_sink_w = sv2v_cast_B2660(s);
				end
		end
	end
	reg tpend_any_w;
	reg [IF_W_C - 1:0] tpend_if_w;
	always @(*) begin : tpend_pick
		if (_sv2v_0)
			;
		tpend_any_w = 1'b0;
		tpend_if_w = 1'sb0;
		begin : sv2v_autoblock_11
			reg [31:0] i;
			for (i = 0; i < N_IF_P; i = i + 1)
				if (!tpend_any_w && (tpend_r[i] != 2'd0)) begin
					tpend_any_w = 1'b1;
					tpend_if_w = sv2v_cast_6AF68(i);
				end
		end
	end
	wire iter_port_w;
	assign iter_port_w = iter_arm_w || iter_cancel_w;
	assign tpend_issue_w = (tpend_any_w && !iter_port_w) && !ucancel_issue_w;
	assign tpend_issue_if_w = tpend_if_w;
	wire ucancel_grant_w;
	assign ucancel_grant_w = ucancel_issue_w && !iter_port_w;
	always @(posedge clk_i) begin : ucancel_pend
		if (!rst_n)
			ucancel_pend_r <= 1'sb0;
		else begin
			begin : sv2v_autoblock_12
				reg [31:0] s;
				for (s = 0; s < N_SINK_P; s = s + 1)
					if (bound_fall_w[s] && disc_st_r[s])
						ucancel_pend_r[s] <= 1'b1;
			end
			if (ucancel_grant_w)
				ucancel_pend_r[ucancel_sink_w] <= 1'b0;
		end
	end
	function automatic [31:0] pp_adp_pkg_adp_vt_to_ms_f;
		input reg [4:0] vt;
		pp_adp_pkg_adp_vt_to_ms_f = sv2v_cast_32(vt) * 32'd2000;
	endfunction
	function automatic [TMR_AW_C - 1:0] sv2v_cast_5A563;
		input reg [TMR_AW_C - 1:0] inp;
		sv2v_cast_5A563 = inp;
	endfunction
	always @(*) begin : tmr_port_mux
		if (_sv2v_0)
			;
		tmr_arm_valid_o = 1'b0;
		tmr_arm_cancel_o = 1'b0;
		tmr_arm_slot_o = 1'sb0;
		tmr_arm_deadline_ms_o = 32'd0;
		if (iter_port_w) begin
			tmr_arm_valid_o = 1'b1;
			tmr_arm_cancel_o = iter_cancel_w;
			tmr_arm_slot_o = sv2v_cast_5A563(TMR_SLOT_NOADP_BASE_P + sv2v_cast_32(sink_r));
			tmr_arm_deadline_ms_o = now_ms_i + pp_adp_pkg_adp_vt_to_ms_f(rxq_vt_r);
		end
		else if (ucancel_issue_w) begin
			tmr_arm_valid_o = 1'b1;
			tmr_arm_cancel_o = 1'b1;
			tmr_arm_slot_o = sv2v_cast_5A563(TMR_SLOT_NOADP_BASE_P + sv2v_cast_32(ucancel_sink_w));
		end
		else if (tpend_any_w) begin
			tmr_arm_valid_o = 1'b1;
			tmr_arm_cancel_o = tpend_r[tpend_if_w] == 2'd2;
			tmr_arm_slot_o = sv2v_cast_5A563(TMR_SLOT_ADV_BASE_P + sv2v_cast_32(tpend_if_w));
			tmr_arm_deadline_ms_o = tpend_deadline_r[tpend_if_w];
		end
	end
	assign tmr_arm_owner_o = {{pp_pkg_PP_TIMER_OWNER_W_C - TMR_AW_C {1'b0}}, tmr_arm_slot_o};
	reg [N_SINK_P - 1:0] pend_dep_evt_r;
	reg drain_any_w;
	reg [SNK_W_C - 1:0] drain_sink_w;
	always @(*) begin : drain_pick
		if (_sv2v_0)
			;
		drain_any_w = 1'b0;
		drain_sink_w = 1'sb0;
		begin : sv2v_autoblock_13
			reg [31:0] s;
			for (s = 0; s < N_SINK_P; s = s + 1)
				if (!drain_any_w && pend_dep_evt_r[s]) begin
					drain_any_w = 1'b1;
					drain_sink_w = sv2v_cast_B2660(s);
				end
		end
	end
	wire iter_evt_w;
	assign iter_evt_w = (rx_st_r == 4'd4) && (ev_dep_w || ev_disc_w);
	always @(posedge clk_i) begin : event_emitter
		if (!rst_n) begin
			evt_valid_o <= 1'b0;
			evt_departed_o <= 1'b0;
			evt_sink_o <= 1'sb0;
			pend_dep_evt_r <= 1'sb0;
		end
		else begin
			evt_valid_o <= 1'b0;
			if (noadp_exp_w && disc_st_r[noadp_exp_sink_w])
				pend_dep_evt_r[noadp_exp_sink_w] <= 1'b1;
			if (iter_evt_w) begin
				evt_valid_o <= 1'b1;
				evt_departed_o <= ev_dep_w;
				evt_sink_o <= sink_r;
			end
			else if (rx_st_r == 4'd5) begin
				evt_valid_o <= 1'b1;
				evt_departed_o <= 1'b0;
				evt_sink_o <= sink_r;
			end
			else if (drain_any_w) begin
				evt_valid_o <= 1'b1;
				evt_departed_o <= 1'b1;
				evt_sink_o <= drain_sink_w;
				pend_dep_evt_r[drain_sink_w] <= 1'b0;
			end
		end
	end
	always @(*) begin : dbg_flatten
		if (_sv2v_0)
			;
		begin : sv2v_autoblock_14
			reg [31:0] i;
			for (i = 0; i < N_IF_P; i = i + 1)
				begin
					dbg_adv_state_o[2 * i+:2] = adv_st_r[i];
					dbg_avail_index_o[32 * i+:32] = aidx_r[i];
				end
		end
	end
	initial _sv2v_0 = 0;
endmodule
`default_nettype wire
`default_nettype none
module KL_aecp_ca_originator (
	clk_i,
	rst_n,
	entity_id_i,
	own_mac_i,
	req_valid_i,
	req_owner_i,
	req_ctlr_eid_i,
	req_mac_i,
	req_ready_o,
	cancel_valid_i,
	cancel_owner_i,
	cancel_release_valid_o,
	cancel_release_slot_o,
	issued_valid_o,
	issued_owner_o,
	txs_alloc_req_o,
	txs_alloc_gnt_i,
	txs_alloc_slot_i,
	txs_wr_slot_o,
	txs_wr_addr_o,
	txs_wr_valid_o,
	txs_wr_data_o,
	txs_wr_commit_o,
	txs_wr_len_o,
	txs_abort_o,
	iss_valid_o,
	iss_owner_o,
	iss_tx_slot_o,
	iss_key_o,
	iss_tmr_slot_o,
	iss_timeout_ms_o,
	iss_ready_i,
	iss_gnt_i,
	iss_seq_i,
	iss_id_i
);
	reg _sv2v_0;
	localparam [31:0] pp_pkg_PP_CA_POOL_C = 4;
	localparam [31:0] pp_pkg_PP_N_CTRL_C = 16;
	localparam [31:0] pp_pkg_PP_N_IF_C = 1;
	localparam [31:0] pp_pkg_PP_N_STREAM_IN_C = 8;
	localparam [31:0] pp_pkg_PP_N_STREAM_OUT_C = 8;
	localparam [31:0] pp_pkg_PP_MAAP_SLOTS_C = 2;
	localparam [31:0] pp_pkg_PP_SINGLETON_SLOTS_C = 5;
	localparam [31:0] pp_pkg_PP_SRP_CAD_SLOTS_C = 7;
	function automatic [415:0] pp_pkg_pp_timer_map;
		input reg [31:0] n_if;
		input reg [31:0] si;
		input reg [31:0] so;
		input reg [31:0] n_ctrl;
		input reg [31:0] ca_pool;
		reg [415:0] m;
		begin
			m[415-:32] = 32'd0;
			m[383-:32] = m[415-:32] + n_if;
			m[351-:32] = m[383-:32] + si;
			m[319-:32] = m[351-:32] + si;
			m[287-:32] = m[319-:32] + so;
			m[255-:32] = m[287-:32] + ((32'd2 * n_ctrl) * n_if);
			m[223-:32] = m[255-:32] + ca_pool;
			m[191-:32] = m[223-:32] + pp_pkg_PP_SINGLETON_SLOTS_C;
			m[159-:32] = m[191-:32] + pp_pkg_PP_MAAP_SLOTS_C;
			m[127-:32] = m[159-:32];
			m[95-:32] = m[127-:32] + pp_pkg_PP_SRP_CAD_SLOTS_C;
			m[63-:32] = m[95-:32] + so;
			m[31-:32] = m[127-:32] + (((pp_pkg_PP_SRP_CAD_SLOTS_C + si) + so) * n_if);
			pp_pkg_pp_timer_map = m;
		end
	endfunction
	function automatic [31:0] pp_pkg_pp_timer_slots;
		input reg [31:0] n_if;
		input reg [31:0] si;
		input reg [31:0] so;
		input reg [31:0] n_ctrl;
		input reg [31:0] ca_pool;
		input reg en_srp;
		reg [415:0] m;
		begin
			m = pp_pkg_pp_timer_map(n_if, si, so, n_ctrl, ca_pool);
			pp_pkg_pp_timer_slots = (en_srp ? m[31-:32] : m[159-:32]);
		end
	endfunction
	localparam [31:0] pp_pkg_PP_TIMER_SLOTS_C = pp_pkg_pp_timer_slots(pp_pkg_PP_N_IF_C, pp_pkg_PP_N_STREAM_IN_C, pp_pkg_PP_N_STREAM_OUT_C, pp_pkg_PP_N_CTRL_C, pp_pkg_PP_CA_POOL_C, 1'b1);
	parameter [31:0] TMR_SLOTS_P = pp_pkg_PP_TIMER_SLOTS_C;
	parameter [31:0] TMR_CA_BASE_P = 57;
	parameter [31:0] TX_STD_SLOTS_P = 4;
	parameter [31:0] TX_OVERSIZE_BYTES_P = 1600;
	localparam [31:0] TMR_AW_C = (TMR_SLOTS_P > 1 ? $clog2(TMR_SLOTS_P) : 1);
	localparam [31:0] TXS_W_C = $clog2(TX_STD_SLOTS_P + 1);
	localparam [31:0] TXA_W_C = $clog2(TX_OVERSIZE_BYTES_P + 1);
	input wire clk_i;
	input wire rst_n;
	input wire [63:0] entity_id_i;
	input wire [47:0] own_mac_i;
	input wire req_valid_i;
	input wire [3:0] req_owner_i;
	input wire [63:0] req_ctlr_eid_i;
	input wire [47:0] req_mac_i;
	output wire req_ready_o;
	input wire cancel_valid_i;
	input wire [3:0] cancel_owner_i;
	output reg cancel_release_valid_o;
	output reg [TXS_W_C - 1:0] cancel_release_slot_o;
	output reg issued_valid_o;
	output reg [3:0] issued_owner_o;
	output wire txs_alloc_req_o;
	input wire txs_alloc_gnt_i;
	input wire [TXS_W_C - 1:0] txs_alloc_slot_i;
	output wire [TXS_W_C - 1:0] txs_wr_slot_o;
	output wire [TXA_W_C - 1:0] txs_wr_addr_o;
	output wire txs_wr_valid_o;
	output reg [7:0] txs_wr_data_o;
	output wire txs_wr_commit_o;
	output wire [TXA_W_C - 1:0] txs_wr_len_o;
	output reg txs_abort_o;
	output wire iss_valid_o;
	output wire [3:0] iss_owner_o;
	output wire [2:0] iss_tx_slot_o;
	output wire [111:0] iss_key_o;
	output wire [TMR_AW_C - 1:0] iss_tmr_slot_o;
	output wire [15:0] iss_timeout_ms_o;
	input wire iss_ready_i;
	input wire iss_gnt_i;
	input wire [15:0] iss_seq_i;
	input wire [3:0] iss_id_i;
	reg [2:0] c_st_r;
	reg [3:0] owner_r;
	reg [63:0] ctlr_eid_r;
	reg [47:0] ctlr_mac_r;
	reg [15:0] seq_r;
	reg [TXS_W_C - 1:0] slot_r;
	reg [5:0] byte_r;
	reg alloc_wait_r;
	wire cancel_hit_w;
	always @(*) begin : frame_byte
		if (_sv2v_0)
			;
		txs_wr_data_o = 8'd0;
		if (byte_r < 6)
			txs_wr_data_o = ctlr_mac_r[47 - (8 * byte_r)-:8];
		else if (byte_r < 12)
			txs_wr_data_o = own_mac_i[47 - (8 * (byte_r - 6))-:8];
		else if (byte_r == 12)
			txs_wr_data_o = 8'h22;
		else if (byte_r == 13)
			txs_wr_data_o = 8'hf0;
		else if (byte_r == 14)
			txs_wr_data_o = 8'hfb;
		else if (byte_r == 15)
			txs_wr_data_o = 8'h00;
		else if (byte_r == 16)
			txs_wr_data_o = 8'h00;
		else if (byte_r == 17)
			txs_wr_data_o = 8'h0c;
		else if (byte_r < 26)
			txs_wr_data_o = ctlr_eid_r[63 - (8 * (byte_r - 18))-:8];
		else if (byte_r < 34)
			txs_wr_data_o = entity_id_i[63 - (8 * (byte_r - 26))-:8];
		else if (byte_r == 34)
			txs_wr_data_o = seq_r[15:8];
		else if (byte_r == 35)
			txs_wr_data_o = seq_r[7:0];
		else if (byte_r == 36)
			txs_wr_data_o = 8'h00;
		else if (byte_r == 37)
			txs_wr_data_o = 8'h03;
	end
	assign cancel_hit_w = (cancel_valid_i && (cancel_owner_i == owner_r)) && (c_st_r != 3'd0);
	assign req_ready_o = c_st_r == 3'd0;
	assign txs_alloc_req_o = ((c_st_r == 3'd1) && !cancel_hit_w) && !alloc_wait_r;
	assign txs_wr_slot_o = slot_r;
	function automatic [TXA_W_C - 1:0] sv2v_cast_FE6CB;
		input reg [TXA_W_C - 1:0] inp;
		sv2v_cast_FE6CB = inp;
	endfunction
	assign txs_wr_addr_o = sv2v_cast_FE6CB(byte_r);
	assign txs_wr_valid_o = (c_st_r == 3'd2) && !cancel_hit_w;
	assign txs_wr_commit_o = (c_st_r == 3'd3) && !cancel_hit_w;
	function automatic signed [TXA_W_C - 1:0] sv2v_cast_FE6CB_signed;
		input reg signed [TXA_W_C - 1:0] inp;
		sv2v_cast_FE6CB_signed = inp;
	endfunction
	assign txs_wr_len_o = sv2v_cast_FE6CB_signed(60);
	assign iss_valid_o = (c_st_r == 3'd4) && !cancel_hit_w;
	assign iss_owner_o = owner_r;
	function automatic [2:0] sv2v_cast_3;
		input reg [2:0] inp;
		sv2v_cast_3 = inp;
	endfunction
	assign iss_tx_slot_o = sv2v_cast_3(slot_r);
	assign iss_key_o = {ctlr_eid_r, ctlr_mac_r};
	function automatic [31:0] sv2v_cast_32;
		input reg [31:0] inp;
		sv2v_cast_32 = inp;
	endfunction
	function automatic [TMR_AW_C - 1:0] sv2v_cast_5A563;
		input reg [TMR_AW_C - 1:0] inp;
		sv2v_cast_5A563 = inp;
	endfunction
	assign iss_tmr_slot_o = sv2v_cast_5A563(TMR_CA_BASE_P + sv2v_cast_32(iss_id_i));
	assign iss_timeout_ms_o = 16'd250;
	always @(posedge clk_i) begin : builder
		if (!rst_n) begin
			c_st_r <= 3'd0;
			owner_r <= 4'd0;
			ctlr_eid_r <= 64'd0;
			ctlr_mac_r <= 48'd0;
			seq_r <= 16'd0;
			slot_r <= 1'sb0;
			byte_r <= 6'd0;
			alloc_wait_r <= 1'b0;
			issued_valid_o <= 1'b0;
			issued_owner_o <= 4'd0;
			txs_abort_o <= 1'b0;
			cancel_release_valid_o <= 1'b0;
			cancel_release_slot_o <= 1'sb0;
		end
		else begin
			issued_valid_o <= 1'b0;
			txs_abort_o <= 1'b0;
			cancel_release_valid_o <= 1'b0;
			cancel_release_slot_o <= 1'sb0;
			(* full_case, parallel_case *)
			case (c_st_r)
				3'd0:
					if (req_valid_i) begin
						owner_r <= req_owner_i;
						ctlr_eid_r <= req_ctlr_eid_i;
						ctlr_mac_r <= req_mac_i;
						alloc_wait_r <= 1'b0;
						c_st_r <= 3'd1;
					end
				3'd1:
					if (cancel_hit_w) begin
						txs_abort_o <= 1'b1;
						if (txs_alloc_gnt_i) begin
							cancel_release_valid_o <= 1'b1;
							cancel_release_slot_o <= txs_alloc_slot_i;
						end
						alloc_wait_r <= 1'b0;
						c_st_r <= 3'd0;
					end
					else if (txs_alloc_gnt_i) begin
						slot_r <= txs_alloc_slot_i;
						seq_r <= iss_seq_i;
						byte_r <= 6'd0;
						alloc_wait_r <= 1'b0;
						c_st_r <= 3'd2;
					end
					else
						alloc_wait_r <= !alloc_wait_r;
				3'd2:
					if (cancel_hit_w) begin
						txs_abort_o <= 1'b1;
						cancel_release_valid_o <= 1'b1;
						cancel_release_slot_o <= slot_r;
						c_st_r <= 3'd0;
					end
					else if (byte_r == 6'd59)
						c_st_r <= 3'd3;
					else
						byte_r <= byte_r + 6'd1;
				3'd3:
					if (cancel_hit_w) begin
						txs_abort_o <= 1'b1;
						cancel_release_valid_o <= 1'b1;
						cancel_release_slot_o <= slot_r;
						c_st_r <= 3'd0;
					end
					else
						c_st_r <= 3'd4;
				3'd4:
					if (cancel_hit_w) begin
						txs_abort_o <= 1'b1;
						cancel_release_valid_o <= 1'b1;
						cancel_release_slot_o <= slot_r;
						c_st_r <= 3'd0;
					end
					else if (iss_gnt_i) begin
						issued_valid_o <= 1'b1;
						issued_owner_o <= owner_r;
						c_st_r <= 3'd0;
					end
				default: c_st_r <= 3'd0;
			endcase
		end
	end
	wire unused_ready_w;
	assign unused_ready_w = iss_ready_i;
	initial _sv2v_0 = 0;
endmodule
`default_nettype wire
`default_nettype none
module KL_aecp_desc_store (
	clk_i,
	rst_n,
	st_req_i,
	st_we_i,
	st_name_i,
	st_addr_i,
	st_wdata_i,
	st_wstrb_i,
	st_ready_o,
	st_rvalid_o,
	st_rdata_o,
	st_err_o,
	mem_req_valid_o,
	mem_req_ready_i,
	mem_req_addr_o,
	mem_req_beats_o,
	mem_rsp_valid_i,
	mem_rsp_ready_o,
	mem_rsp_data_i,
	mem_rsp_last_i,
	mem_rsp_err_i,
	dbg_img_valid_o,
	dbg_fault_o,
	dbg_locate_miss_o,
	dbg_fetch_cnt_o,
	dbg_ro_write_o,
	dbg_desc_len_o
);
	reg _sv2v_0;
	parameter [31:0] DESC_BASE_P = 32'h20000000;
	parameter [31:0] LINE_BYTES_P = 576;
	parameter [31:0] IDX_ENTRIES_P = 32;
	parameter [31:0] NAME_ENTRIES_P = 32;
	parameter [31:0] MEM_TIMEOUT_CYC_P = 4096;
	localparam [31:0] LINE_LANES_C = LINE_BYTES_P / 8;
	localparam [31:0] LINE_AW_C = $clog2(LINE_LANES_C);
	localparam [31:0] NAME_LANES_C = NAME_ENTRIES_P * 8;
	localparam [31:0] NAME_AW_C = $clog2(NAME_LANES_C);
	localparam [31:0] IDX_AW_C = $clog2(IDX_ENTRIES_P);
	localparam [31:0] TMO_W_C = $clog2(MEM_TIMEOUT_CYC_P + 1);
	input wire clk_i;
	input wire rst_n;
	input wire st_req_i;
	input wire st_we_i;
	input wire st_name_i;
	input wire [19:0] st_addr_i;
	input wire [63:0] st_wdata_i;
	input wire [7:0] st_wstrb_i;
	output wire st_ready_o;
	output wire st_rvalid_o;
	output wire [63:0] st_rdata_o;
	output wire st_err_o;
	output wire mem_req_valid_o;
	input wire mem_req_ready_i;
	output wire [31:0] mem_req_addr_o;
	output wire [8:0] mem_req_beats_o;
	input wire mem_rsp_valid_i;
	output wire mem_rsp_ready_o;
	input wire [63:0] mem_rsp_data_i;
	input wire mem_rsp_last_i;
	input wire mem_rsp_err_i;
	output wire dbg_img_valid_o;
	output wire [3:0] dbg_fault_o;
	output wire [15:0] dbg_locate_miss_o;
	output wire [15:0] dbg_fetch_cnt_o;
	output wire [15:0] dbg_ro_write_o;
	output wire [15:0] dbg_desc_len_o;
	localparam [31:0] IMG_MAGIC_C = 32'h41454d49;
	localparam [15:0] IMG_VERSION_C = 16'd1;
	localparam [15:0] NAME_NONE_C = 16'hffff;
	localparam [31:0] HDR_BEATS_C = 4;
	localparam [31:0] NAME_BURST_BEATS_C = 504;
	localparam [3:0] FAULT_NONE_C = 4'd0;
	localparam [3:0] FAULT_MAGIC_C = 4'd1;
	localparam [3:0] FAULT_VERSION_C = 4'd2;
	localparam [3:0] FAULT_CKSUM_C = 4'd3;
	localparam [3:0] FAULT_NIDX_C = 4'd4;
	localparam [3:0] FAULT_NNAME_C = 4'd5;
	localparam [3:0] FAULT_DESCLEN_C = 4'd6;
	localparam [3:0] FAULT_MEMERR_C = 4'd7;
	localparam [3:0] FAULT_TIMEOUT_C = 4'd8;
	localparam [3:0] RGN_DATA_C = 4'h0;
	localparam [3:0] RGN_NADDR_C = 4'hb;
	localparam [3:0] RGN_NBASE_C = 4'hc;
	localparam [3:0] RGN_NCFG_C = 4'hd;
	localparam [3:0] RGN_LEN_C = 4'he;
	localparam [3:0] RGN_LOCATE_C = 4'hf;
	generate
		if ((LINE_BYTES_P % 8) != 0) begin : gen_g_line_align
			initial $display("Error [elaboration] $VALIDATION_STORAGE/reviews/r247-520-r1/protocol-processor/hdl/aecp/KL_aecp_desc_store.sv:238:5 - KL_aecp_desc_store.gen_g_line_align\n msg: ", "LINE_BYTES_P=%0d must be a multiple of 8 (64-bit lanes)", LINE_BYTES_P);
		end
		if ((LINE_LANES_C > 511) || ((IDX_ENTRIES_P * 2) > 511)) begin : gen_g_beats
			initial $display("Error [elaboration] $VALIDATION_STORAGE/reviews/r247-520-r1/protocol-processor/hdl/aecp/KL_aecp_desc_store.sv:242:5 - KL_aecp_desc_store.gen_g_beats\n msg: ", "a burst exceeds the 9-bit mem_req_beats_o field");
		end
		if ((NAME_ENTRIES_P == 0) || (NAME_ENTRIES_P > 1024)) begin : gen_g_names
			initial $display("Error [elaboration] $VALIDATION_STORAGE/reviews/r247-520-r1/protocol-processor/hdl/aecp/KL_aecp_desc_store.sv:245:5 - KL_aecp_desc_store.gen_g_names\n msg: ", "NAME_ENTRIES_P=%0d must be in 1..1024", NAME_ENTRIES_P);
		end
		if (DESC_BASE_P[2:0] != 3'd0) begin : gen_g_base_align
			initial $display("Error [elaboration] $VALIDATION_STORAGE/reviews/r247-520-r1/protocol-processor/hdl/aecp/KL_aecp_desc_store.sv:248:5 - KL_aecp_desc_store.gen_g_base_align\n msg: ", "DESC_BASE_P=%08h must be 8-byte aligned", DESC_BASE_P);
		end
	endgenerate
	localparam [31:0] IDX_W_C = 128;
	reg [127:0] idx_r [0:IDX_ENTRIES_P - 1];
	reg [127:0] idx_q_r;
	reg [IDX_AW_C - 1:0] idx_waddr_w;
	reg [IDX_AW_C - 1:0] idx_raddr_w;
	reg idx_we_w;
	reg [127:0] idx_wdata_w;
	always @(posedge clk_i) begin : idx_ram
		if (idx_we_w)
			idx_r[idx_waddr_w] <= idx_wdata_w;
		idx_q_r <= idx_r[idx_raddr_w];
	end
	reg [63:0] line_r [0:LINE_LANES_C - 1];
	reg [63:0] line_q_r;
	reg [LINE_AW_C - 1:0] line_waddr_w;
	reg [LINE_AW_C - 1:0] line_raddr_w;
	reg line_we_w;
	reg [63:0] line_wdata_w;
	always @(posedge clk_i) begin : line_ram
		if (line_we_w)
			line_r[line_waddr_w] <= line_wdata_w;
		line_q_r <= line_r[line_raddr_w];
	end
	reg [63:0] name_r [0:NAME_LANES_C - 1];
	reg [63:0] name_q_r;
	reg [NAME_AW_C - 1:0] name_waddr_w;
	reg [NAME_AW_C - 1:0] name_raddr_w;
	reg name_we_w;
	reg [63:0] name_wdata_w;
	reg [7:0] name_wstrb_w;
	always @(posedge clk_i) begin : name_ram
		if (name_we_w) begin : sv2v_autoblock_1
			reg [31:0] b;
			for (b = 0; b < 8; b = b + 1)
				if (name_wstrb_w[b])
					name_r[name_waddr_w][8 * b+:8] <= name_wdata_w[8 * b+:8];
		end
		name_q_r <= name_r[name_raddr_w];
	end
	reg [15:0] hdr_n_config_r;
	reg [15:0] hdr_n_entries_r;
	reg [15:0] hdr_n_names_r;
	reg [15:0] hdr_desc_max_r;
	reg [31:0] hdr_index_off_r;
	reg [31:0] hdr_names_off_r;
	reg [31:0] cksum_r;
	reg [63:0] hdr_b0_r;
	reg [63:0] idx_b0_r;
	reg [3:0] st_r;
	reg img_valid_r;
	reg [3:0] fault_r;
	reg [15:0] miss_cnt_r;
	reg [15:0] fetch_cnt_r;
	reg [15:0] rowr_cnt_r;
	reg [31:0] mreq_addr_r;
	reg [8:0] mreq_beats_r;
	reg mreq_valid_r;
	reg [8:0] beat_ix_r;
	reg [19:0] name_load_lane_r;
	reg [TMO_W_C - 1:0] tmo_r;
	reg mem_busy_r;
	wire [19:0] name_total_lanes_w;
	wire [19:0] name_lanes_left_w;
	assign name_total_lanes_w = {4'd0, hdr_n_names_r} << 3;
	assign name_lanes_left_w = name_total_lanes_w - name_load_lane_r;
	wire beat_w;
	wire accept_w;
	wire tmo_hit_w;
	assign beat_w = mem_rsp_valid_i && mem_busy_r;
	assign accept_w = mreq_valid_r && mem_req_ready_i;
	function automatic [TMO_W_C - 1:0] sv2v_cast_BA630;
		input reg [TMO_W_C - 1:0] inp;
		sv2v_cast_BA630 = inp;
	endfunction
	assign tmo_hit_w = tmo_r == sv2v_cast_BA630(MEM_TIMEOUT_CYC_P);
	assign mem_req_valid_o = mreq_valid_r;
	assign mem_req_addr_o = mreq_addr_r;
	assign mem_req_beats_o = mreq_beats_r;
	assign mem_rsp_ready_o = 1'b1;
	reg [15:0] key_cfg_r;
	reg [15:0] key_type_r;
	reg [15:0] key_index_r;
	reg [15:0] desc_len_r;
	reg [15:0] desc_nbase_r;
	reg [31:0] desc_off_r;
	reg ans_err_r;
	reg [63:0] ans_data_r;
	reg [63:0] rd_reg_r;
	reg ans_pend_r;
	reg rd_pipe_r;
	reg req_seen_r;
	reg [1:0] rd_kind_r;
	reg [IDX_AW_C - 1:0] scan_rd_r;
	reg [15:0] scan_cmp_r;
	reg scan_rdy_r;
	reg [15:0] scan_base_r;
	reg heal_pend_r;
	reg heal_kind_r;
	reg patch_answer_r;
	reg patch_name_r;
	reg [5:0] patch_byte_r;
	wire [15:0] e_cfg_w;
	wire [15:0] e_type_w;
	wire [15:0] e_cnt_w;
	wire [15:0] e_len_w;
	wire [15:0] e_nbase_w;
	wire [15:0] e_strd_w;
	wire [31:0] e_off_w;
	assign e_cfg_w = idx_q_r[127:112];
	assign e_type_w = idx_q_r[111:96];
	assign e_cnt_w = idx_q_r[95:80];
	assign e_len_w = idx_q_r[79:64];
	assign e_off_w = idx_q_r[63:32];
	assign e_nbase_w = idx_q_r[31:16];
	assign e_strd_w = idx_q_r[15:0];
	wire e_usable_w;
	reg e_name_ok_w;
	function automatic [31:0] sv2v_cast_32;
		input reg [31:0] inp;
		sv2v_cast_32 = inp;
	endfunction
	always @(*) begin : entry_name_shape
		if (_sv2v_0)
			;
		e_name_ok_w = 1'b1;
		if (e_nbase_w != NAME_NONE_C) begin
			if (e_type_w == 16'h0000)
				e_name_ok_w = ((e_cnt_w == 16'd1) && (e_len_w >= 16'd244)) && ((sv2v_cast_32(e_nbase_w) + 32'd2) <= sv2v_cast_32(hdr_n_names_r));
			else
				e_name_ok_w = (e_len_w >= 16'd68) && ((sv2v_cast_32(e_nbase_w) + sv2v_cast_32(e_cnt_w)) <= sv2v_cast_32(hdr_n_names_r));
		end
	end
	assign e_usable_w = ((((e_len_w != 16'd0) && (sv2v_cast_32(e_len_w) <= LINE_BYTES_P)) && (e_strd_w >= e_len_w)) && (e_strd_w[2:0] == 3'd0)) && e_name_ok_w;
	wire type_hit_w;
	wire last_w;
	wire [15:0] rel_w;
	assign type_hit_w = (e_cfg_w == key_cfg_r) && (e_type_w == key_type_r);
	assign rel_w = key_index_r - scan_base_r;
	assign last_w = (scan_cmp_r + 16'd1) >= hdr_n_entries_r;
	wire [3:0] region_w;
	assign region_w = st_addr_i[19:16];
	assign st_ready_o = (st_r == 4'd6) || (st_r == 4'd7);
	wire take_rd_w;
	wire take_wr_w;
	assign take_rd_w = ((st_req_i && !st_we_i) && !req_seen_r) && st_ready_o;
	assign take_wr_w = (st_req_i && st_we_i) && st_ready_o;
	assign st_rvalid_o = (ans_pend_r && !rd_pipe_r) && (st_r == 4'd13);
	assign st_rdata_o = ans_data_r;
	assign st_err_o = ans_err_r;
	assign dbg_img_valid_o = img_valid_r;
	assign dbg_fault_o = fault_r;
	assign dbg_locate_miss_o = miss_cnt_r;
	assign dbg_fetch_cnt_o = fetch_cnt_r;
	assign dbg_ro_write_o = rowr_cnt_r;
	assign dbg_desc_len_o = desc_len_r;
	wire [15:0] len_lanes_w;
	assign len_lanes_w = (desc_len_r + 16'd7) >> 3;
	wire [15:0] patch_field_off_w;
	wire [15:0] patch_abs_byte_w;
	wire [15:0] patch_name_lane_w;
	wire [2:0] patch_line_byte_w;
	wire [2:0] patch_name_byte_w;
	reg [7:0] patch_data_w;
	wire [15:0] write_name_entry_w;
	wire write_hits_current_w;
	wire [16:0] name_lookup_entry_w;
	wire name_lookup_valid_w;
	assign patch_field_off_w = (key_type_r == 16'h0000 ? (patch_name_r ? 16'd180 : 16'd48) : 16'd4);
	assign patch_abs_byte_w = patch_field_off_w + {10'd0, patch_byte_r};
	assign patch_name_lane_w = ((desc_nbase_r + {15'd0, patch_name_r}) << 3) + {13'd0, patch_byte_r[5:3]};
	assign patch_line_byte_w = patch_abs_byte_w[2:0];
	assign patch_name_byte_w = patch_byte_r[2:0];
	assign write_name_entry_w = {6'd0, st_addr_i[15:6]};
	assign write_hits_current_w = (img_valid_r && (desc_nbase_r != NAME_NONE_C)) && ((write_name_entry_w == desc_nbase_r) || ((key_type_r == 16'h0000) && (write_name_entry_w == (desc_nbase_r + 16'd1))));
	assign name_lookup_entry_w = {1'b0, desc_nbase_r} + {1'b0, st_wdata_i[15:0]};
	assign name_lookup_valid_w = ((img_valid_r && (desc_nbase_r != NAME_NONE_C)) && ((st_wdata_i[15:0] == 16'd0) || ((key_type_r == 16'h0000) && (st_wdata_i[15:0] == 16'd1)))) && (name_lookup_entry_w < {1'b0, hdr_n_names_r});
	function automatic [2:0] sv2v_cast_3;
		input reg [2:0] inp;
		sv2v_cast_3 = inp;
	endfunction
	always @(*) begin : patch_byte_select
		if (_sv2v_0)
			;
		patch_data_w = 8'd0;
		begin : sv2v_autoblock_2
			reg [31:0] b;
			for (b = 0; b < 8; b = b + 1)
				if (patch_name_byte_w == sv2v_cast_3(b))
					patch_data_w = name_q_r[63 - (8 * b)-:8];
		end
	end
	function automatic [IDX_AW_C - 1:0] sv2v_cast_1746D;
		input reg [IDX_AW_C - 1:0] inp;
		sv2v_cast_1746D = inp;
	endfunction
	function automatic [LINE_AW_C - 1:0] sv2v_cast_A5527;
		input reg [LINE_AW_C - 1:0] inp;
		sv2v_cast_A5527 = inp;
	endfunction
	function automatic [NAME_AW_C - 1:0] sv2v_cast_786DE;
		input reg [NAME_AW_C - 1:0] inp;
		sv2v_cast_786DE = inp;
	endfunction
	always @(*) begin : ram_ports
		if (_sv2v_0)
			;
		idx_we_w = ((st_r == 4'd3) && beat_w) && beat_ix_r[0];
		idx_waddr_w = sv2v_cast_1746D(beat_ix_r >> 1);
		idx_wdata_w = {idx_b0_r, mem_rsp_data_i};
		idx_raddr_w = scan_rd_r;
		line_we_w = ((st_r == 4'd10) && beat_w) || (st_r == 4'd12);
		line_waddr_w = (st_r == 4'd12 ? sv2v_cast_A5527(patch_abs_byte_w >> 3) : sv2v_cast_A5527(beat_ix_r));
		line_raddr_w = (|{st_r == 4'd11, st_r == 4'd12} ? sv2v_cast_A5527(patch_abs_byte_w >> 3) : sv2v_cast_A5527(st_addr_i[15:3]));
		line_wdata_w = mem_rsp_data_i;
		if (st_r == 4'd12) begin
			line_wdata_w = line_q_r;
			begin : sv2v_autoblock_3
				reg [31:0] b;
				for (b = 0; b < 8; b = b + 1)
					if (patch_line_byte_w == sv2v_cast_3(b))
						line_wdata_w[63 - (8 * b)-:8] = patch_data_w;
			end
		end
		name_raddr_w = (|{st_r == 4'd11, st_r == 4'd12} ? sv2v_cast_786DE(patch_name_lane_w) : sv2v_cast_786DE(st_addr_i[15:3]));
		if ((st_r == 4'd5) && beat_w) begin
			name_we_w = 1'b1;
			name_waddr_w = sv2v_cast_786DE(name_load_lane_r + {11'd0, beat_ix_r});
			name_wdata_w = mem_rsp_data_i;
			name_wstrb_w = 8'hff;
		end
		else begin
			name_we_w = take_wr_w && st_name_i;
			name_waddr_w = sv2v_cast_786DE(st_addr_i[15:3]);
			name_wdata_w = st_wdata_i;
			name_wstrb_w = st_wstrb_i;
		end
	end
	reg hdr_ok_w;
	reg [3:0] hdr_fault_w;
	always @(*) begin : header_check
		if (_sv2v_0)
			;
		hdr_ok_w = 1'b0;
		hdr_fault_w = FAULT_NONE_C;
		if (hdr_b0_r[63:32] != IMG_MAGIC_C)
			hdr_fault_w = FAULT_MAGIC_C;
		else if (hdr_b0_r[31:16] != IMG_VERSION_C)
			hdr_fault_w = FAULT_VERSION_C;
		else if (cksum_r != 32'hffffffff)
			hdr_fault_w = FAULT_CKSUM_C;
		else if (((hdr_n_entries_r == 16'd0) || (hdr_n_config_r == 16'd0)) || (sv2v_cast_32(hdr_n_entries_r) > IDX_ENTRIES_P))
			hdr_fault_w = FAULT_NIDX_C;
		else if (sv2v_cast_32(hdr_n_names_r) > NAME_ENTRIES_P)
			hdr_fault_w = FAULT_NNAME_C;
		else if ((hdr_desc_max_r == 16'd0) || (sv2v_cast_32(hdr_desc_max_r) > LINE_BYTES_P))
			hdr_fault_w = FAULT_DESCLEN_C;
		else
			hdr_ok_w = 1'b1;
	end
	function automatic signed [TMO_W_C - 1:0] sv2v_cast_BA630_signed;
		input reg signed [TMO_W_C - 1:0] inp;
		sv2v_cast_BA630_signed = inp;
	endfunction
	function automatic [8:0] sv2v_cast_9;
		input reg [8:0] inp;
		sv2v_cast_9 = inp;
	endfunction
	function automatic [19:0] sv2v_cast_20;
		input reg [19:0] inp;
		sv2v_cast_20 = inp;
	endfunction
	function automatic signed [IDX_AW_C - 1:0] sv2v_cast_1746D_signed;
		input reg signed [IDX_AW_C - 1:0] inp;
		sv2v_cast_1746D_signed = inp;
	endfunction
	always @(posedge clk_i) begin : core
		if (!rst_n) begin
			st_r <= 4'd0;
			img_valid_r <= 1'b0;
			fault_r <= FAULT_NONE_C;
			miss_cnt_r <= 16'd0;
			fetch_cnt_r <= 16'd0;
			rowr_cnt_r <= 16'd0;
			mreq_valid_r <= 1'b0;
			mreq_addr_r <= 32'd0;
			mreq_beats_r <= 9'd0;
			mem_busy_r <= 1'b0;
			beat_ix_r <= 9'd0;
			tmo_r <= 1'sb0;
			hdr_b0_r <= 64'd0;
			idx_b0_r <= 64'd0;
			hdr_n_config_r <= 16'd0;
			hdr_n_entries_r <= 16'd0;
			hdr_n_names_r <= 16'd0;
			hdr_desc_max_r <= 16'd0;
			hdr_index_off_r <= 32'd0;
			hdr_names_off_r <= 32'd0;
			cksum_r <= 32'd0;
			key_cfg_r <= 16'd0;
			key_type_r <= 16'd0;
			key_index_r <= 16'd0;
			desc_len_r <= 16'd0;
			desc_nbase_r <= NAME_NONE_C;
			desc_off_r <= 32'd0;
			ans_err_r <= 1'b0;
			ans_data_r <= 64'd0;
			rd_reg_r <= 64'd0;
			ans_pend_r <= 1'b0;
			rd_pipe_r <= 1'b0;
			req_seen_r <= 1'b0;
			rd_kind_r <= 2'd0;
			scan_rd_r <= 1'sb0;
			scan_cmp_r <= 16'd0;
			scan_rdy_r <= 1'b0;
			scan_base_r <= 16'd0;
			heal_pend_r <= 1'b0;
			heal_kind_r <= 1'b0;
			patch_answer_r <= 1'b0;
			patch_name_r <= 1'b0;
			patch_byte_r <= 6'd0;
			name_load_lane_r <= 20'd0;
		end
		else begin
			if (take_rd_w)
				req_seen_r <= 1'b1;
			if (st_rvalid_o)
				req_seen_r <= 1'b0;
			if (accept_w) begin
				mreq_valid_r <= 1'b0;
				mem_busy_r <= 1'b1;
				beat_ix_r <= 9'd0;
				tmo_r <= 1'sb0;
			end
			if (beat_w) begin
				beat_ix_r <= beat_ix_r + 9'd1;
				tmo_r <= 1'sb0;
				if (mem_rsp_last_i || mem_rsp_err_i)
					mem_busy_r <= 1'b0;
			end
			if (((mreq_valid_r || mem_busy_r) && !beat_w) && !tmo_hit_w)
				tmo_r <= tmo_r + sv2v_cast_BA630_signed(1);
			(* full_case, parallel_case *)
			case (st_r)
				4'd0: begin
					if (!mreq_valid_r && !mem_busy_r) begin
						mreq_valid_r <= 1'b1;
						mreq_addr_r <= DESC_BASE_P;
						mreq_beats_r <= sv2v_cast_9(HDR_BEATS_C);
						cksum_r <= 32'd0;
					end
					if (accept_w)
						st_r <= 4'd1;
					else if (tmo_hit_w) begin
						fault_r <= FAULT_TIMEOUT_C;
						mreq_valid_r <= 1'b0;
						tmo_r <= 1'sb0;
						st_r <= 4'd7;
					end
				end
				4'd1: begin
					if (beat_w) begin
						cksum_r <= (cksum_r + mem_rsp_data_i[63:32]) + mem_rsp_data_i[31:0];
						(* full_case, parallel_case *)
						case (beat_ix_r[1:0])
							2'd0: begin
								hdr_b0_r <= mem_rsp_data_i;
								hdr_n_config_r <= mem_rsp_data_i[15:0];
							end
							2'd1: begin
								hdr_n_entries_r <= mem_rsp_data_i[63:48];
								hdr_n_names_r <= mem_rsp_data_i[47:32];
								hdr_index_off_r <= mem_rsp_data_i[31:0];
							end
							2'd2: hdr_names_off_r <= mem_rsp_data_i[63:32];
							default: hdr_desc_max_r <= mem_rsp_data_i[63:48];
						endcase
					end
					if (beat_w && mem_rsp_err_i) begin
						fault_r <= FAULT_MEMERR_C;
						st_r <= 4'd7;
					end
					else if (beat_w && mem_rsp_last_i)
						st_r <= 4'd2;
					else if (tmo_hit_w) begin
						fault_r <= FAULT_TIMEOUT_C;
						mem_busy_r <= 1'b0;
						tmo_r <= 1'sb0;
						st_r <= 4'd7;
					end
				end
				4'd2:
					if (!hdr_ok_w) begin
						fault_r <= hdr_fault_w;
						st_r <= 4'd7;
					end
					else begin
						if (!mreq_valid_r && !mem_busy_r) begin
							mreq_valid_r <= 1'b1;
							mreq_addr_r <= DESC_BASE_P + hdr_index_off_r;
							mreq_beats_r <= sv2v_cast_9(hdr_n_entries_r << 1);
						end
						if (accept_w)
							st_r <= 4'd3;
						else if (tmo_hit_w) begin
							fault_r <= FAULT_TIMEOUT_C;
							mreq_valid_r <= 1'b0;
							tmo_r <= 1'sb0;
							st_r <= 4'd7;
						end
					end
				4'd3: begin
					if (beat_w && !beat_ix_r[0])
						idx_b0_r <= mem_rsp_data_i;
					if (beat_w && mem_rsp_err_i) begin
						fault_r <= FAULT_MEMERR_C;
						st_r <= 4'd7;
					end
					else if (beat_w && mem_rsp_last_i) begin
						name_load_lane_r <= 20'd0;
						st_r <= 4'd4;
					end
					else if (tmo_hit_w) begin
						fault_r <= FAULT_TIMEOUT_C;
						mem_busy_r <= 1'b0;
						tmo_r <= 1'sb0;
						st_r <= 4'd7;
					end
				end
				4'd4:
					if (hdr_n_names_r == 16'd0) begin
						img_valid_r <= 1'b1;
						fault_r <= FAULT_NONE_C;
						if (heal_pend_r && !heal_kind_r) begin
							heal_pend_r <= 1'b0;
							scan_rd_r <= 1'sb0;
							scan_cmp_r <= 16'd0;
							scan_rdy_r <= 1'b0;
							scan_base_r <= 16'd0;
							st_r <= 4'd8;
						end
						else if (heal_pend_r) begin
							heal_pend_r <= 1'b0;
							ans_err_r <= 1'b0;
							ans_data_r <= {48'd0, hdr_n_config_r};
							rd_pipe_r <= 1'b0;
							st_r <= 4'd13;
						end
						else
							st_r <= 4'd6;
					end
					else begin
						if (!mreq_valid_r && !mem_busy_r) begin
							mreq_valid_r <= 1'b1;
							mreq_addr_r <= (DESC_BASE_P + hdr_names_off_r) + sv2v_cast_32(name_load_lane_r << 3);
							mreq_beats_r <= (name_lanes_left_w > sv2v_cast_20(NAME_BURST_BEATS_C) ? sv2v_cast_9(NAME_BURST_BEATS_C) : sv2v_cast_9(name_lanes_left_w));
						end
						if (accept_w)
							st_r <= 4'd5;
						else if (tmo_hit_w) begin
							fault_r <= FAULT_TIMEOUT_C;
							mreq_valid_r <= 1'b0;
							tmo_r <= 1'sb0;
							st_r <= 4'd7;
						end
					end
				4'd5:
					if (beat_w && mem_rsp_err_i) begin
						fault_r <= FAULT_MEMERR_C;
						st_r <= 4'd7;
					end
					else if (beat_w && mem_rsp_last_i) begin
						if ((name_load_lane_r + {11'd0, mreq_beats_r}) < name_total_lanes_w) begin
							name_load_lane_r <= name_load_lane_r + {11'd0, mreq_beats_r};
							st_r <= 4'd4;
						end
						else begin
							img_valid_r <= 1'b1;
							fault_r <= FAULT_NONE_C;
							if (heal_pend_r && !heal_kind_r) begin
								heal_pend_r <= 1'b0;
								scan_rd_r <= 1'sb0;
								scan_cmp_r <= 16'd0;
								scan_rdy_r <= 1'b0;
								scan_base_r <= 16'd0;
								st_r <= 4'd8;
							end
							else if (heal_pend_r) begin
								heal_pend_r <= 1'b0;
								ans_err_r <= 1'b0;
								ans_data_r <= {48'd0, hdr_n_config_r};
								rd_pipe_r <= 1'b0;
								st_r <= 4'd13;
							end
							else
								st_r <= 4'd6;
						end
					end
					else if (tmo_hit_w) begin
						fault_r <= FAULT_TIMEOUT_C;
						mem_busy_r <= 1'b0;
						tmo_r <= 1'sb0;
						st_r <= 4'd7;
					end
				4'd6, 4'd7: begin
					if (heal_pend_r) begin
						heal_pend_r <= 1'b0;
						ans_pend_r <= 1'b1;
						ans_err_r <= !heal_kind_r;
						ans_data_r <= 64'd0;
						rd_pipe_r <= 1'b0;
						if (!heal_kind_r) begin
							desc_len_r <= 16'd0;
							desc_nbase_r <= NAME_NONE_C;
							if (miss_cnt_r != 16'hffff)
								miss_cnt_r <= miss_cnt_r + 16'd1;
						end
						st_r <= 4'd13;
					end
					if ((take_wr_w && !st_name_i) && (rowr_cnt_r != 16'hffff))
						rowr_cnt_r <= rowr_cnt_r + 16'd1;
					if ((((st_r == 4'd6) && take_wr_w) && st_name_i) && write_hits_current_w) begin
						patch_answer_r <= 1'b0;
						patch_name_r <= 1'b0;
						patch_byte_r <= 6'd0;
						st_r <= 4'd11;
					end
					if (take_rd_w) begin
						ans_pend_r <= 1'b1;
						ans_err_r <= 1'b0;
						if (st_name_i) begin
							rd_pipe_r <= 1'b1;
							rd_kind_r <= 2'd1;
							st_r <= 4'd13;
						end
						else if (region_w == RGN_LOCATE_C) begin
							key_cfg_r <= st_wdata_i[15:0];
							key_type_r <= st_wdata_i[31:16];
							key_index_r <= st_wdata_i[47:32];
							if (img_valid_r) begin
								scan_rd_r <= 1'sb0;
								scan_cmp_r <= 16'd0;
								scan_rdy_r <= 1'b0;
								scan_base_r <= 16'd0;
								st_r <= 4'd8;
							end
							else begin
								heal_pend_r <= 1'b1;
								heal_kind_r <= 1'b0;
								st_r <= 4'd0;
							end
						end
						else if ((region_w == RGN_NCFG_C) && !img_valid_r) begin
							heal_pend_r <= 1'b1;
							heal_kind_r <= 1'b1;
							st_r <= 4'd0;
						end
						else begin
							rd_pipe_r <= 1'b1;
							(* full_case, parallel_case *)
							case (region_w)
								RGN_NADDR_C: begin
									rd_kind_r <= 2'd2;
									if (name_lookup_valid_w)
										rd_reg_r <= {41'd0, name_lookup_entry_w, 6'd0};
									else begin
										rd_reg_r <= 64'd0;
										ans_err_r <= 1'b1;
									end
								end
								RGN_NBASE_C: begin
									rd_kind_r <= 2'd2;
									rd_reg_r <= (img_valid_r ? {48'd0, desc_nbase_r} : 64'd0);
								end
								RGN_NCFG_C: begin
									rd_kind_r <= 2'd2;
									rd_reg_r <= {48'd0, hdr_n_config_r};
								end
								RGN_LEN_C: begin
									rd_kind_r <= 2'd2;
									rd_reg_r <= (img_valid_r ? {48'd0, desc_len_r} : 64'd0);
								end
								default: rd_kind_r <= 2'd0;
							endcase
							st_r <= 4'd13;
						end
					end
				end
				4'd8: begin
					scan_rd_r <= scan_rd_r + sv2v_cast_1746D_signed(1);
					scan_rdy_r <= 1'b1;
					if (scan_rdy_r) begin
						scan_cmp_r <= scan_cmp_r + 16'd1;
						if (((type_hit_w && e_usable_w) && (key_index_r >= scan_base_r)) && (rel_w < e_cnt_w)) begin
							desc_len_r <= e_len_w;
							desc_nbase_r <= (e_nbase_w == NAME_NONE_C ? NAME_NONE_C : e_nbase_w + rel_w);
							desc_off_r <= e_off_w + (sv2v_cast_32(e_strd_w) * sv2v_cast_32(rel_w));
							st_r <= 4'd9;
						end
						else if ((type_hit_w && e_usable_w) && !last_w)
							scan_base_r <= scan_base_r + e_cnt_w;
						else if (last_w || (type_hit_w && !e_usable_w)) begin
							ans_err_r <= 1'b1;
							ans_data_r <= 64'd0;
							rd_pipe_r <= 1'b0;
							desc_len_r <= 16'd0;
							desc_nbase_r <= NAME_NONE_C;
							if (miss_cnt_r != 16'hffff)
								miss_cnt_r <= miss_cnt_r + 16'd1;
							st_r <= 4'd13;
						end
					end
				end
				4'd9: begin
					if (!mreq_valid_r && !mem_busy_r) begin
						mreq_valid_r <= 1'b1;
						mreq_addr_r <= DESC_BASE_P + {desc_off_r[31:3], 3'd0};
						mreq_beats_r <= sv2v_cast_9(len_lanes_w);
					end
					if (accept_w) begin
						if (fetch_cnt_r != 16'hffff)
							fetch_cnt_r <= fetch_cnt_r + 16'd1;
						st_r <= 4'd10;
					end
					else if (tmo_hit_w) begin
						mreq_valid_r <= 1'b0;
						tmo_r <= 1'sb0;
						ans_err_r <= 1'b1;
						ans_data_r <= 64'd0;
						rd_pipe_r <= 1'b0;
						desc_len_r <= 16'd0;
						desc_nbase_r <= NAME_NONE_C;
						if (miss_cnt_r != 16'hffff)
							miss_cnt_r <= miss_cnt_r + 16'd1;
						st_r <= 4'd13;
					end
				end
				4'd10:
					if (beat_w && mem_rsp_err_i) begin
						ans_err_r <= 1'b1;
						ans_data_r <= 64'd0;
						rd_pipe_r <= 1'b0;
						desc_len_r <= 16'd0;
						desc_nbase_r <= NAME_NONE_C;
						if (miss_cnt_r != 16'hffff)
							miss_cnt_r <= miss_cnt_r + 16'd1;
						st_r <= 4'd13;
					end
					else if (beat_w && mem_rsp_last_i) begin
						if (desc_nbase_r != NAME_NONE_C) begin
							patch_answer_r <= 1'b1;
							patch_name_r <= 1'b0;
							patch_byte_r <= 6'd0;
							st_r <= 4'd11;
						end
						else begin
							ans_err_r <= 1'b0;
							ans_data_r <= 64'd0;
							rd_pipe_r <= 1'b0;
							st_r <= 4'd13;
						end
					end
					else if (tmo_hit_w) begin
						ans_err_r <= 1'b1;
						ans_data_r <= 64'd0;
						rd_pipe_r <= 1'b0;
						mem_busy_r <= 1'b0;
						desc_len_r <= 16'd0;
						desc_nbase_r <= NAME_NONE_C;
						if (miss_cnt_r != 16'hffff)
							miss_cnt_r <= miss_cnt_r + 16'd1;
						st_r <= 4'd13;
					end
				4'd11: st_r <= 4'd12;
				4'd12:
					if (patch_byte_r != 6'd63) begin
						patch_byte_r <= patch_byte_r + 6'd1;
						st_r <= 4'd11;
					end
					else if ((key_type_r == 16'h0000) && !patch_name_r) begin
						patch_name_r <= 1'b1;
						patch_byte_r <= 6'd0;
						st_r <= 4'd11;
					end
					else if (patch_answer_r) begin
						ans_err_r <= 1'b0;
						ans_data_r <= 64'd0;
						rd_pipe_r <= 1'b0;
						st_r <= 4'd13;
					end
					else
						st_r <= 4'd6;
				4'd13:
					if (rd_pipe_r) begin
						rd_pipe_r <= 1'b0;
						(* full_case, parallel_case *)
						case (rd_kind_r)
							2'd1: ans_data_r <= name_q_r;
							2'd2: ans_data_r <= rd_reg_r;
							default: ans_data_r <= (sv2v_cast_32(st_addr_i[15:3]) < sv2v_cast_32(len_lanes_w) ? line_q_r : 64'd0);
						endcase
					end
					else begin
						ans_pend_r <= 1'b0;
						st_r <= (img_valid_r ? 4'd6 : 4'd0);
					end
				default: st_r <= 4'd7;
			endcase
		end
	end
	initial _sv2v_0 = 0;
endmodule
`default_nettype wire
`default_nettype none
module KL_aecp_dyn_state (
	clk_i,
	rst_n,
	st_req_i,
	st_we_i,
	st_addr_i,
	st_wdata_i,
	st_ready_o,
	st_rvalid_o,
	st_rdata_o,
	desc_index_i,
	cur_config_o,
	identify_o,
	clk_src_index_o,
	pt_offset_o,
	pt_offset_v_o,
	fmt_in_o,
	fmt_in_v_o,
	fmt_out_o,
	fmt_out_v_o,
	dirty_o,
	dbg_writes_o,
	dbg_oob_o
);
	reg _sv2v_0;
	parameter [31:0] N_STREAM_IN_P = 8;
	parameter [31:0] N_STREAM_OUT_P = 8;
	parameter [31:0] N_AUDIO_UNIT_P = 1;
	parameter [31:0] N_CLK_DOMAIN_P = 1;
	parameter [31:0] N_CONTROL_P = 1;
	input wire clk_i;
	input wire rst_n;
	input wire st_req_i;
	input wire st_we_i;
	input wire [19:0] st_addr_i;
	input wire [63:0] st_wdata_i;
	output wire st_ready_o;
	output wire st_rvalid_o;
	output wire [63:0] st_rdata_o;
	input wire [15:0] desc_index_i;
	output wire [15:0] cur_config_o;
	output wire [7:0] identify_o;
	output wire [15:0] clk_src_index_o;
	output reg [(N_STREAM_OUT_P * 32) - 1:0] pt_offset_o;
	output wire [N_STREAM_OUT_P - 1:0] pt_offset_v_o;
	output reg [(N_STREAM_IN_P * 64) - 1:0] fmt_in_o;
	output wire [N_STREAM_IN_P - 1:0] fmt_in_v_o;
	output reg [(N_STREAM_OUT_P * 64) - 1:0] fmt_out_o;
	output wire [N_STREAM_OUT_P - 1:0] fmt_out_v_o;
	output reg dirty_o;
	output wire [15:0] dbg_writes_o;
	output wire [15:0] dbg_oob_o;
	localparam [31:0] SEL_CFG_C = 0;
	localparam [31:0] SEL_RATE_C = 1;
	localparam [31:0] SEL_CLKSRC_C = 2;
	localparam [31:0] SEL_FMTIN_C = 3;
	localparam [31:0] SEL_FMTOUT_C = 4;
	localparam [31:0] SEL_PTOFF_C = 5;
	localparam [31:0] SEL_IDENT_C = 7;
	localparam [3:0] RGN_DYN_C = 4'h1;
	localparam [3:0] RGN_DYNV_C = 4'h2;
	localparam [31:0] AUW_C = (N_AUDIO_UNIT_P > 1 ? $clog2(N_AUDIO_UNIT_P) : 1);
	localparam [31:0] CDW_C = (N_CLK_DOMAIN_P > 1 ? $clog2(N_CLK_DOMAIN_P) : 1);
	localparam [31:0] SIW_C = (N_STREAM_IN_P > 1 ? $clog2(N_STREAM_IN_P) : 1);
	localparam [31:0] SOW_C = (N_STREAM_OUT_P > 1 ? $clog2(N_STREAM_OUT_P) : 1);
	localparam [31:0] CTW_C = (N_CONTROL_P > 1 ? $clog2(N_CONTROL_P) : 1);
	reg [15:0] cfg_r;
	reg cfg_v_r;
	reg [31:0] rate_r [0:N_AUDIO_UNIT_P - 1];
	reg [N_AUDIO_UNIT_P - 1:0] rate_v_r;
	reg [15:0] clksrc_r [0:N_CLK_DOMAIN_P - 1];
	reg [N_CLK_DOMAIN_P - 1:0] clksrc_v_r;
	reg [63:0] fmtin_r [0:N_STREAM_IN_P - 1];
	reg [N_STREAM_IN_P - 1:0] fmtin_v_r;
	reg [63:0] fmtout_r [0:N_STREAM_OUT_P - 1];
	reg [N_STREAM_OUT_P - 1:0] fmtout_v_r;
	reg [31:0] ptoff_r [0:N_STREAM_OUT_P - 1];
	reg [N_STREAM_OUT_P - 1:0] ptoff_v_r;
	reg [7:0] ident_r [0:N_CONTROL_P - 1];
	reg [N_CONTROL_P - 1:0] ident_v_r;
	reg [15:0] wr_cnt_r;
	reg [15:0] oob_cnt_r;
	wire [3:0] region_w;
	wire [12:0] sel_w;
	assign region_w = st_addr_i[19:16];
	assign sel_w = st_addr_i[15:3];
	reg [15:0] count_w;
	function automatic [12:0] sv2v_cast_13;
		input reg [12:0] inp;
		sv2v_cast_13 = inp;
	endfunction
	function automatic [15:0] sv2v_cast_16;
		input reg [15:0] inp;
		sv2v_cast_16 = inp;
	endfunction
	always @(*) begin : sel_count
		if (_sv2v_0)
			;
		(* full_case, parallel_case *)
		case (sel_w)
			sv2v_cast_13(SEL_CFG_C): count_w = 16'd1;
			sv2v_cast_13(SEL_RATE_C): count_w = sv2v_cast_16(N_AUDIO_UNIT_P);
			sv2v_cast_13(SEL_CLKSRC_C): count_w = sv2v_cast_16(N_CLK_DOMAIN_P);
			sv2v_cast_13(SEL_FMTIN_C): count_w = sv2v_cast_16(N_STREAM_IN_P);
			sv2v_cast_13(SEL_FMTOUT_C): count_w = sv2v_cast_16(N_STREAM_OUT_P);
			sv2v_cast_13(SEL_PTOFF_C): count_w = sv2v_cast_16(N_STREAM_OUT_P);
			sv2v_cast_13(SEL_IDENT_C): count_w = sv2v_cast_16(N_CONTROL_P);
			default: count_w = 16'd0;
		endcase
	end
	wire in_range_w;
	assign in_range_w = desc_index_i < count_w;
	wire [AUW_C - 1:0] au_ix_w;
	function automatic [AUW_C - 1:0] sv2v_cast_62E8F;
		input reg [AUW_C - 1:0] inp;
		sv2v_cast_62E8F = inp;
	endfunction
	assign au_ix_w = sv2v_cast_62E8F(desc_index_i);
	wire [CDW_C - 1:0] cd_ix_w;
	function automatic [CDW_C - 1:0] sv2v_cast_0711C;
		input reg [CDW_C - 1:0] inp;
		sv2v_cast_0711C = inp;
	endfunction
	assign cd_ix_w = sv2v_cast_0711C(desc_index_i);
	wire [SIW_C - 1:0] si_ix_w;
	function automatic [SIW_C - 1:0] sv2v_cast_997A1;
		input reg [SIW_C - 1:0] inp;
		sv2v_cast_997A1 = inp;
	endfunction
	assign si_ix_w = sv2v_cast_997A1(desc_index_i);
	wire [SOW_C - 1:0] so_ix_w;
	function automatic [SOW_C - 1:0] sv2v_cast_A8627;
		input reg [SOW_C - 1:0] inp;
		sv2v_cast_A8627 = inp;
	endfunction
	assign so_ix_w = sv2v_cast_A8627(desc_index_i);
	wire [CTW_C - 1:0] ct_ix_w;
	function automatic [CTW_C - 1:0] sv2v_cast_457CC;
		input reg [CTW_C - 1:0] inp;
		sv2v_cast_457CC = inp;
	endfunction
	assign ct_ix_w = sv2v_cast_457CC(desc_index_i);
	reg [63:0] val_w;
	reg [63:0] vld_w;
	always @(*) begin : read_mux
		if (_sv2v_0)
			;
		val_w = 64'd0;
		vld_w = 64'd0;
		if (in_range_w)
			(* full_case, parallel_case *)
			case (sel_w)
				sv2v_cast_13(SEL_CFG_C): begin
					val_w = {48'd0, cfg_r};
					vld_w = {63'd0, cfg_v_r};
				end
				sv2v_cast_13(SEL_RATE_C): begin
					val_w = {32'd0, rate_r[au_ix_w]};
					vld_w = {63'd0, rate_v_r[au_ix_w]};
				end
				sv2v_cast_13(SEL_CLKSRC_C): begin
					val_w = {48'd0, clksrc_r[cd_ix_w]};
					vld_w = {63'd0, clksrc_v_r[cd_ix_w]};
				end
				sv2v_cast_13(SEL_FMTIN_C): begin
					val_w = fmtin_r[si_ix_w];
					vld_w = {63'd0, fmtin_v_r[si_ix_w]};
				end
				sv2v_cast_13(SEL_FMTOUT_C): begin
					val_w = fmtout_r[so_ix_w];
					vld_w = {63'd0, fmtout_v_r[so_ix_w]};
				end
				sv2v_cast_13(SEL_PTOFF_C): begin
					val_w = {32'd0, ptoff_r[so_ix_w]};
					vld_w = {63'd0, ptoff_v_r[so_ix_w]};
				end
				sv2v_cast_13(SEL_IDENT_C): begin
					val_w = {56'd0, ident_r[ct_ix_w]};
					vld_w = {63'd0, ident_v_r[ct_ix_w]};
				end
				default:
					;
			endcase
	end
	reg rd_pend_r;
	reg [63:0] rd_data_r;
	assign st_rvalid_o = rd_pend_r;
	assign st_rdata_o = rd_data_r;
	assign st_ready_o = st_req_i && st_we_i;
	wire take_wr_w;
	wire oob_wr_w;
	assign take_wr_w = ((st_req_i && st_we_i) && (region_w == RGN_DYN_C)) && in_range_w;
	assign oob_wr_w = ((st_req_i && st_we_i) && (region_w == RGN_DYN_C)) && !in_range_w;
	always @(posedge clk_i) begin : dyn_core
		if (!rst_n) begin
			cfg_r <= 16'd0;
			cfg_v_r <= 1'b0;
			rate_v_r <= 1'sb0;
			clksrc_v_r <= 1'sb0;
			fmtin_v_r <= 1'sb0;
			fmtout_v_r <= 1'sb0;
			ptoff_v_r <= 1'sb0;
			ident_v_r <= 1'sb0;
			rd_pend_r <= 1'b0;
			rd_data_r <= 64'd0;
			dirty_o <= 1'b0;
			wr_cnt_r <= 16'd0;
			oob_cnt_r <= 16'd0;
			begin : sv2v_autoblock_1
				reg [31:0] i;
				for (i = 0; i < N_AUDIO_UNIT_P; i = i + 1)
					rate_r[i] <= 32'd0;
			end
			begin : sv2v_autoblock_2
				reg [31:0] i;
				for (i = 0; i < N_CLK_DOMAIN_P; i = i + 1)
					clksrc_r[i] <= 16'd0;
			end
			begin : sv2v_autoblock_3
				reg [31:0] i;
				for (i = 0; i < N_STREAM_IN_P; i = i + 1)
					fmtin_r[i] <= 64'd0;
			end
			begin : sv2v_autoblock_4
				reg [31:0] i;
				for (i = 0; i < N_STREAM_OUT_P; i = i + 1)
					fmtout_r[i] <= 64'd0;
			end
			begin : sv2v_autoblock_5
				reg [31:0] i;
				for (i = 0; i < N_STREAM_OUT_P; i = i + 1)
					ptoff_r[i] <= 32'd0;
			end
			begin : sv2v_autoblock_6
				reg [31:0] i;
				for (i = 0; i < N_CONTROL_P; i = i + 1)
					ident_r[i] <= 8'd0;
			end
		end
		else begin
			rd_pend_r <= st_req_i && !st_we_i;
			rd_data_r <= (region_w == RGN_DYNV_C ? vld_w : val_w);
			if (oob_wr_w && (oob_cnt_r != 16'hffff))
				oob_cnt_r <= oob_cnt_r + 16'd1;
			if (take_wr_w) begin
				if (wr_cnt_r != 16'hffff)
					wr_cnt_r <= wr_cnt_r + 16'd1;
				if (sel_w != sv2v_cast_13(SEL_IDENT_C))
					dirty_o <= 1'b1;
				(* full_case, parallel_case *)
				case (sel_w)
					sv2v_cast_13(SEL_CFG_C): begin
						cfg_r <= st_wdata_i[15:0];
						cfg_v_r <= 1'b1;
					end
					sv2v_cast_13(SEL_RATE_C): begin
						rate_r[au_ix_w] <= st_wdata_i[31:0];
						rate_v_r[au_ix_w] <= 1'b1;
					end
					sv2v_cast_13(SEL_CLKSRC_C): begin
						clksrc_r[cd_ix_w] <= st_wdata_i[15:0];
						clksrc_v_r[cd_ix_w] <= 1'b1;
					end
					sv2v_cast_13(SEL_FMTIN_C): begin
						fmtin_r[si_ix_w] <= st_wdata_i;
						fmtin_v_r[si_ix_w] <= 1'b1;
					end
					sv2v_cast_13(SEL_FMTOUT_C): begin
						fmtout_r[so_ix_w] <= st_wdata_i;
						fmtout_v_r[so_ix_w] <= 1'b1;
					end
					sv2v_cast_13(SEL_PTOFF_C): begin
						ptoff_r[so_ix_w] <= st_wdata_i[31:0];
						ptoff_v_r[so_ix_w] <= 1'b1;
					end
					sv2v_cast_13(SEL_IDENT_C): begin
						ident_r[ct_ix_w] <= st_wdata_i[7:0];
						ident_v_r[ct_ix_w] <= 1'b1;
					end
					default:
						;
				endcase
			end
		end
	end
	assign cur_config_o = cfg_r;
	assign identify_o = ident_r[0];
	assign clk_src_index_o = clksrc_r[0];
	always @(*) begin : live_rows
		if (_sv2v_0)
			;
		begin : sv2v_autoblock_7
			reg [31:0] i;
			for (i = 0; i < N_STREAM_OUT_P; i = i + 1)
				begin
					pt_offset_o[32 * i+:32] = ptoff_r[i];
					fmt_out_o[64 * i+:64] = fmtout_r[i];
				end
		end
		begin : sv2v_autoblock_8
			reg [31:0] i;
			for (i = 0; i < N_STREAM_IN_P; i = i + 1)
				fmt_in_o[64 * i+:64] = fmtin_r[i];
		end
	end
	assign pt_offset_v_o = ptoff_v_r;
	assign fmt_in_v_o = fmtin_v_r;
	assign fmt_out_v_o = fmtout_v_r;
	assign dbg_writes_o = wr_cnt_r;
	assign dbg_oob_o = oob_cnt_r;
	initial _sv2v_0 = 0;
endmodule
`default_nettype wire
`default_nettype none
module KL_aecp_engine (
	clk_i,
	rst_n,
	entity_id_i,
	own_mac_i,
	txn_valid_i,
	txn_i,
	txn_ready_o,
	rxs_rd_slot_o,
	rxs_rd_addr_o,
	rxs_rd_en_o,
	rxs_rd_data_i,
	rxs_slot_len_i,
	rxs_free_o,
	rxs_free_slot_o,
	txs_alloc_req_o,
	txs_oversize_o,
	txs_alloc_gnt_i,
	txs_alloc_slot_i,
	txs_wr_slot_o,
	txs_wr_addr_o,
	txs_wr_valid_o,
	txs_wr_data_o,
	txs_wr_commit_o,
	txs_wr_len_o,
	txreq_valid_o,
	txreq_slot_o,
	txreq_ready_i,
	mem_req_valid_o,
	mem_req_ready_i,
	mem_req_addr_o,
	mem_req_beats_o,
	mem_rsp_valid_i,
	mem_rsp_ready_o,
	mem_rsp_data_i,
	mem_rsp_last_i,
	mem_rsp_err_i,
	rmem_req_valid_o,
	rmem_req_ready_i,
	rmem_req_addr_o,
	rmem_req_beats_o,
	rmem_rsp_valid_i,
	rmem_rsp_ready_o,
	rmem_rsp_data_i,
	rmem_rsp_last_i,
	rmem_rsp_err_i,
	rmem_wr_valid_o,
	rmem_wr_ready_i,
	rmem_wr_addr_o,
	rmem_wr_data_o,
	rmem_wr_strb_o,
	rmem_wr_done_i,
	rmem_wr_err_i,
	ctr_req_o,
	ctr_desc_type_o,
	ctr_desc_index_o,
	ctr_word_o,
	ctr_data_i,
	ctr_wait_i,
	amap_req_o,
	amap_desc_type_o,
	amap_desc_index_o,
	amap_map_index_o,
	amap_sel_o,
	amap_rec_o,
	amap_data_i,
	amap_wait_i,
	amap_edit_req_o,
	amap_edit_phase_o,
	amap_edit_remove_o,
	amap_edit_desc_type_o,
	amap_edit_desc_index_o,
	amap_edit_count_o,
	amap_edit_rec_o,
	amap_edit_record_o,
	amap_edit_value_o,
	amap_edit_data_i,
	amap_edit_wait_i,
	gsi_req_o,
	gsi_kind_o,
	gsi_desc_type_o,
	gsi_desc_index_o,
	gsi_sel_o,
	gsi_ord_o,
	gsi_prop_fmt_o,
	gsi_data_i,
	gsi_wait_i,
	rgy_req_o,
	rgy_state_o,
	rgy_op_o,
	rgy_eid_o,
	rgy_mac_o,
	rgy_tl_o,
	rgy_data_i,
	rgy_wait_i,
	uns_valid_i,
	uns_kind_i,
	uns_desc_type_i,
	uns_desc_index_i,
	uns_ctlr_eid_i,
	uns_mac_i,
	uns_seq_i,
	uns_amap_remove_i,
	uns_amap_count_i,
	uns_arg0_i,
	uns_arg1_i,
	amap_notify_busy_i,
	uns_done_o,
	txreq_uns_valid_o,
	txreq_uns_ready_i,
	strm_bound_i,
	strm_started_i,
	strm_set_valid_o,
	strm_set_index_o,
	strm_set_val_o,
	strm_set_ready_i,
	strm_set_error_i,
	strm_streaming_i,
	lock_held_i,
	lock_ctlr_i,
	eff_commit_o,
	eff_nvm_mark_o,
	eff_nvm_stb_o,
	eff_notify_class_o,
	eff_notify_stb_o,
	eff_notify_type_o,
	eff_notify_index_o,
	eff_notify_arg0_o,
	eff_notify_arg1_o,
	eff_notify_excl_eid_o,
	dbg_busy_o,
	dbg_cmd_cnt_o,
	dbg_resp_cnt_o,
	dbg_drop_cnt_o,
	dbg_status_o,
	dbg_len_o,
	dbg_img_valid_o,
	dbg_img_fault_o,
	dbg_locate_miss_o,
	dbg_resp_fault_o,
	dbg_resp_err_o,
	dbg_resp_lane_o,
	dyn_cur_config_o,
	dyn_identify_o,
	dyn_clk_src_index_o,
	dyn_pt_offset_o,
	dyn_pt_offset_v_o,
	dyn_fmt_in_o,
	dyn_fmt_in_v_o,
	dyn_fmt_out_o,
	dyn_fmt_out_v_o,
	dyn_dirty_o
);
	reg _sv2v_0;
	parameter UCODE_HEX_P = "ucode.hex";
	parameter [31:0] DESC_BASE_P = 32'h20000000;
	parameter [31:0] RESP_BASE_P = 32'h20100000;
	parameter [31:0] LINE_BYTES_P = 576;
	parameter [31:0] IDX_ENTRIES_P = 32;
	parameter [31:0] NAME_ENTRIES_P = 32;
	parameter [31:0] MEM_TIMEOUT_CYC_P = 4096;
	parameter [31:0] N_STREAM_IN_P = 8;
	parameter [31:0] N_STREAM_OUT_P = 8;
	parameter [31:0] N_AUDIO_UNIT_P = 1;
	parameter [31:0] N_CLK_DOMAIN_P = 1;
	parameter [31:0] N_CONTROL_P = 1;
	parameter [31:0] RX_SLOTS_P = 4;
	parameter [31:0] RX_SLOT_BYTES_P = 576;
	parameter [31:0] TX_STD_SLOTS_P = 4;
	parameter [31:0] TX_STD_BYTES_P = 576;
	parameter [31:0] TX_OVERSIZE_BYTES_P = 1600;
	localparam [31:0] RXS_W_C = (RX_SLOTS_P > 1 ? $clog2(RX_SLOTS_P) : 1);
	localparam [31:0] RXA_W_C = $clog2(RX_SLOT_BYTES_P);
	localparam [31:0] RXL_W_C = $clog2(RX_SLOT_BYTES_P + 1);
	localparam [31:0] TXS_W_C = $clog2(TX_STD_SLOTS_P + 1);
	localparam [31:0] TXA_W_C = $clog2(TX_OVERSIZE_BYTES_P + 1);
	input wire clk_i;
	input wire rst_n;
	input wire [63:0] entity_id_i;
	input wire [47:0] own_mac_i;
	input wire txn_valid_i;
	localparam [31:0] pp_pkg_PP_TXN_W_C = 393;
	input wire [392:0] txn_i;
	output wire txn_ready_o;
	output wire [RXS_W_C - 1:0] rxs_rd_slot_o;
	output wire [RXA_W_C - 1:0] rxs_rd_addr_o;
	output wire rxs_rd_en_o;
	input wire [7:0] rxs_rd_data_i;
	input wire [RXL_W_C - 1:0] rxs_slot_len_i;
	output wire rxs_free_o;
	output wire [RXS_W_C - 1:0] rxs_free_slot_o;
	output wire txs_alloc_req_o;
	output wire txs_oversize_o;
	input wire txs_alloc_gnt_i;
	input wire [TXS_W_C - 1:0] txs_alloc_slot_i;
	output wire [TXS_W_C - 1:0] txs_wr_slot_o;
	output wire [TXA_W_C - 1:0] txs_wr_addr_o;
	output wire txs_wr_valid_o;
	output wire [7:0] txs_wr_data_o;
	output wire txs_wr_commit_o;
	output wire [TXA_W_C - 1:0] txs_wr_len_o;
	output wire txreq_valid_o;
	output wire [TXS_W_C - 1:0] txreq_slot_o;
	input wire txreq_ready_i;
	output wire mem_req_valid_o;
	input wire mem_req_ready_i;
	output wire [31:0] mem_req_addr_o;
	output wire [8:0] mem_req_beats_o;
	input wire mem_rsp_valid_i;
	output wire mem_rsp_ready_o;
	input wire [63:0] mem_rsp_data_i;
	input wire mem_rsp_last_i;
	input wire mem_rsp_err_i;
	output wire rmem_req_valid_o;
	input wire rmem_req_ready_i;
	output wire [31:0] rmem_req_addr_o;
	output wire [8:0] rmem_req_beats_o;
	input wire rmem_rsp_valid_i;
	output wire rmem_rsp_ready_o;
	input wire [63:0] rmem_rsp_data_i;
	input wire rmem_rsp_last_i;
	input wire rmem_rsp_err_i;
	output wire rmem_wr_valid_o;
	input wire rmem_wr_ready_i;
	output wire [31:0] rmem_wr_addr_o;
	output wire [63:0] rmem_wr_data_o;
	output wire [7:0] rmem_wr_strb_o;
	input wire rmem_wr_done_i;
	input wire rmem_wr_err_i;
	output wire ctr_req_o;
	output wire [15:0] ctr_desc_type_o;
	output wire [15:0] ctr_desc_index_o;
	output wire [5:0] ctr_word_o;
	input wire [31:0] ctr_data_i;
	input wire ctr_wait_i;
	output wire amap_req_o;
	output wire [15:0] amap_desc_type_o;
	output wire [15:0] amap_desc_index_o;
	output wire [15:0] amap_map_index_o;
	output wire [1:0] amap_sel_o;
	output wire [7:0] amap_rec_o;
	input wire [63:0] amap_data_i;
	input wire amap_wait_i;
	output wire amap_edit_req_o;
	output reg [2:0] amap_edit_phase_o;
	output wire amap_edit_remove_o;
	output wire [15:0] amap_edit_desc_type_o;
	output wire [15:0] amap_edit_desc_index_o;
	output wire [15:0] amap_edit_count_o;
	output wire [7:0] amap_edit_rec_o;
	output wire [63:0] amap_edit_record_o;
	output wire [63:0] amap_edit_value_o;
	input wire [63:0] amap_edit_data_i;
	input wire amap_edit_wait_i;
	output wire gsi_req_o;
	output wire [1:0] gsi_kind_o;
	output wire [15:0] gsi_desc_type_o;
	output wire [15:0] gsi_desc_index_o;
	output wire [3:0] gsi_sel_o;
	output wire [7:0] gsi_ord_o;
	output wire [63:0] gsi_prop_fmt_o;
	input wire [63:0] gsi_data_i;
	input wire gsi_wait_i;
	output wire rgy_req_o;
	output wire rgy_state_o;
	output wire [1:0] rgy_op_o;
	output wire [63:0] rgy_eid_o;
	output wire [47:0] rgy_mac_o;
	output wire rgy_tl_o;
	input wire [63:0] rgy_data_i;
	input wire rgy_wait_i;
	input wire uns_valid_i;
	input wire [3:0] uns_kind_i;
	input wire [15:0] uns_desc_type_i;
	input wire [15:0] uns_desc_index_i;
	input wire [63:0] uns_ctlr_eid_i;
	input wire [47:0] uns_mac_i;
	input wire [15:0] uns_seq_i;
	input wire uns_amap_remove_i;
	input wire [15:0] uns_amap_count_i;
	input wire [15:0] uns_arg0_i;
	input wire [15:0] uns_arg1_i;
	input wire amap_notify_busy_i;
	output wire uns_done_o;
	output wire txreq_uns_valid_o;
	input wire txreq_uns_ready_i;
	input wire [N_STREAM_IN_P - 1:0] strm_bound_i;
	input wire [N_STREAM_IN_P - 1:0] strm_started_i;
	output wire strm_set_valid_o;
	output wire [15:0] strm_set_index_o;
	output wire strm_set_val_o;
	input wire strm_set_ready_i;
	input wire strm_set_error_i;
	input wire [N_STREAM_OUT_P - 1:0] strm_streaming_i;
	input wire lock_held_i;
	input wire [63:0] lock_ctlr_i;
	output wire eff_commit_o;
	output wire [7:0] eff_nvm_mark_o;
	output wire eff_nvm_stb_o;
	output wire [3:0] eff_notify_class_o;
	output wire eff_notify_stb_o;
	output reg [15:0] eff_notify_type_o;
	output reg [15:0] eff_notify_index_o;
	output reg [15:0] eff_notify_arg0_o;
	output reg [15:0] eff_notify_arg1_o;
	output reg [63:0] eff_notify_excl_eid_o;
	output wire dbg_busy_o;
	output wire [15:0] dbg_cmd_cnt_o;
	output wire [15:0] dbg_resp_cnt_o;
	output wire [15:0] dbg_drop_cnt_o;
	output wire [4:0] dbg_status_o;
	output wire [10:0] dbg_len_o;
	output wire dbg_img_valid_o;
	output wire [3:0] dbg_img_fault_o;
	output wire [15:0] dbg_locate_miss_o;
	output wire [2:0] dbg_resp_fault_o;
	output wire [15:0] dbg_resp_err_o;
	output wire [15:0] dbg_resp_lane_o;
	output wire [15:0] dyn_cur_config_o;
	output wire [7:0] dyn_identify_o;
	output wire [15:0] dyn_clk_src_index_o;
	output wire [(N_STREAM_OUT_P * 32) - 1:0] dyn_pt_offset_o;
	output wire [N_STREAM_OUT_P - 1:0] dyn_pt_offset_v_o;
	output wire [(N_STREAM_IN_P * 64) - 1:0] dyn_fmt_in_o;
	output wire [N_STREAM_IN_P - 1:0] dyn_fmt_in_v_o;
	output wire [(N_STREAM_OUT_P * 64) - 1:0] dyn_fmt_out_o;
	output wire [N_STREAM_OUT_P - 1:0] dyn_fmt_out_v_o;
	output wire dyn_dirty_o;
	localparam [15:0] OP_READ_DESCRIPTOR_C = 16'h0004;
	localparam [15:0] OP_IDENTIFY_NOTIF_C = 16'h0026;
	localparam [15:0] OP_GET_COUNTERS_C = 16'h0029;
	localparam [15:0] OP_GET_AUDIO_MAP_C = 16'h002b;
	localparam [15:0] OP_GET_DYNAMIC_INFO_C = 16'h004b;
	localparam [15:0] OP_SET_NAME_C = 16'h0010;
	localparam [15:0] OP_GET_NAME_C = 16'h0011;
	localparam [15:0] GDI_GET_VIDEO_FMT_C = 16'h000b;
	localparam [15:0] GDI_GET_SENSOR_FMT_C = 16'h000d;
	localparam [15:0] GDI_GET_ASSOC_ID_C = 16'h0013;
	localparam [15:0] GDI_GET_SIGNAL_SEL_C = 16'h001d;
	localparam [15:0] GDI_GET_MEM_LEN_C = 16'h0048;
	localparam [15:0] GDI_GET_STREAM_BKUP_C = 16'h004a;
	localparam [15:0] OP_ADD_AUDIO_MAP_C = 16'h002c;
	localparam [15:0] OP_REMOVE_AUDIO_MAP_C = 16'h002d;
	localparam [15:0] OP_REG_UNSOL_C = 16'h0024;
	localparam [15:0] OP_DEREG_UNSOL_C = 16'h0025;
	localparam [15:0] OP_ACQUIRE_C = 16'h0000;
	localparam [15:0] OP_LOCK_C = 16'h0001;
	localparam [15:0] OP_GET_STREAM_INFO_C = 16'h000f;
	localparam [15:0] DT_STREAM_INPUT_C = 16'h0005;
	localparam [15:0] DT_STREAM_OUTPUT_C = 16'h0006;
	localparam [15:0] OP_GET_AVB_INFO_C = 16'h0027;
	localparam [15:0] OP_GET_AS_PATH_C = 16'h0028;
	localparam [15:0] DT_AVB_INTERFACE_C = 16'h0009;
	localparam [15:0] DT_CLOCK_DOMAIN_C = 16'h0024;
	localparam [15:0] OP_ENTITY_AVAIL_C = 16'h0002;
	localparam [15:0] OP_GET_CONFIG_C = 16'h0007;
	localparam [15:0] OP_GET_STREAM_FMT_C = 16'h0009;
	localparam [15:0] OP_GET_SAMP_RATE_C = 16'h0015;
	localparam [15:0] OP_GET_CLOCK_SRC_C = 16'h0017;
	localparam [15:0] DT_ENTITY_C = 16'h0000;
	localparam [15:0] DT_AUDIO_UNIT_C = 16'h0002;
	localparam [15:0] OP_SET_SAMP_RATE_C = 16'h0014;
	localparam [15:0] OP_SET_CLOCK_SRC_C = 16'h0016;
	localparam [15:0] OP_SET_CONTROL_C = 16'h0018;
	localparam [15:0] OP_GET_CONTROL_C = 16'h0019;
	localparam [15:0] DT_CONTROL_C = 16'h001a;
	localparam [15:0] OP_SET_CONFIG_C = 16'h0006;
	localparam [15:0] OP_SET_STREAM_FMT_C = 16'h0008;
	localparam [15:0] OP_SET_STREAM_INFO_C = 16'h000e;
	localparam [31:0] SIF_ACC_LAT_C = 32'h20000000;
	localparam [15:0] OP_START_STRM_C = 16'h0022;
	localparam [15:0] OP_STOP_STRM_C = 16'h0023;
	localparam [15:0] DT_STREAM_PORT_IN_C = 16'h000e;
	localparam [15:0] DT_STREAM_PORT_OUT_C = 16'h000f;
	localparam [15:0] MVU_PID_HI_C = 16'h001b;
	localparam [15:0] MVU_PID_MD_C = 16'hc50a;
	localparam [7:0] MVU_PID_L1_C = 8'hc1;
	localparam [7:0] MVU_PID_L0_C = 8'h00;
	localparam [15:0] MVU_GET_MILAN_INFO_C = 16'h0000;
	localparam [10:0] MVU_CMD_PLD_C = 11'd8;
	localparam [10:0] UPC_NOTIMPL_C = 11'd560;
	localparam [10:0] UPC_RDESC_C = 11'd640;
	localparam [10:0] UPC_BADARG_C = 11'd704;
	localparam [10:0] UPC_MVUINFO_C = 11'd736;
	localparam [10:0] UPC_GCTRS_C = 11'd768;
	localparam [10:0] UPC_GAMAP_C = 11'd800;
	localparam [10:0] UPC_REGUN_C = 11'd832;
	localparam [10:0] UPC_DEREG_C = 11'd844;
	localparam [10:0] UPC_UNSOK_C = 11'd852;
	localparam [10:0] UPC_NOSEND_C = 11'd858;
	localparam [10:0] UPC_NSUPPE_C = 11'd864;
	localparam [10:0] UPC_LOCKEN_C = 11'd872;
	localparam [10:0] UPC_LOCKUNS_C = 11'd896;
	localparam [10:0] UPC_GSTRI_C = 11'd912;
	localparam [10:0] UPC_GAVB_C = 11'd944;
	localparam [10:0] UPC_GASP_C = 11'd976;
	localparam [10:0] UPC_GAMAPO_C = 11'd996;
	localparam [10:0] UPC_GCTRSNS_C = 11'd796;
	localparam [10:0] UPC_EAVL_C = 11'd1008;
	localparam [10:0] UPC_GCFG_C = 11'd1024;
	localparam [10:0] UPC_GSFMT_C = 11'd1056;
	localparam [10:0] UPC_GSRATE_C = 11'd1088;
	localparam [10:0] UPC_GCLKS_C = 11'd1120;
	localparam [10:0] UPC_SSRATE_C = 11'd1152;
	localparam [10:0] UPC_SCLKS_C = 11'd1184;
	localparam [10:0] UPC_TIZ8NS_C = 11'd1216;
	localparam [10:0] UPC_TIZ4NS_C = 11'd1224;
	localparam [10:0] UPC_LOCKED4_C = 11'd1232;
	localparam [10:0] UPC_BADARG4_C = 11'd1240;
	localparam [10:0] UPC_GCTRL_C = 11'd1248;
	localparam [10:0] UPC_SCTRL_C = 11'd1280;
	localparam [10:0] UPC_LOCKED1_C = 11'd1312;
	localparam [10:0] UPC_BADARG1_C = 11'd1320;
	localparam [10:0] UPC_NSUPP1_C = 11'd1328;
	localparam [10:0] UPC_SCFG_C = 11'd1456;
	localparam [10:0] UPC_SCFGRUN_C = 11'd1488;
	localparam [10:0] UPC_SCFGBAD_C = 11'd1513;
	localparam [10:0] UPC_RDESCENT_C = 11'd1568;
	localparam [10:0] UPC_STRT_C = 11'd1600;
	localparam [10:0] UPC_STOP_C = 11'd1632;
	localparam [10:0] UPC_STRMNS_C = 11'd1664;
	localparam [10:0] UPC_STRMUNS_C = 11'd1672;
	localparam [10:0] UPC_STRMBAD_C = 11'd1696;
	localparam [10:0] UPC_AMADD_C = 11'd1712;
	localparam [10:0] UPC_AMREMOVE_C = 11'd1760;
	localparam [10:0] UPC_GNAME_C = 11'd1344;
	localparam [10:0] UPC_SNAME_C = 11'd1392;
	localparam [10:0] UPC_NAMEERR_C = 11'd1352;
	localparam [10:0] UPC_NAMEBAD_C = 11'd1384;
	localparam [10:0] UPC_SFMTI_C = 11'd1792;
	localparam [10:0] UPC_SFMTO_C = 11'd1824;
	localparam [10:0] UPC_SINFO_C = 11'd1856;
	localparam [10:0] UPC_SFRUN_C = 11'd1888;
	localparam [10:0] UPC_SFBAD_C = 11'd1912;
	localparam [10:0] UPC_SIBAD_C = 11'd1920;
	localparam [10:0] UPC_SIRUN_C = 11'd1936;
	localparam [31:0] ETH_HDR_C = 14;
	localparam [31:0] AECP_HDR_C = 24;
	localparam [31:0] FRAME_HDR_C = ETH_HDR_C + AECP_HDR_C;
	localparam [31:0] ETH_MIN_C = 60;
	localparam [31:0] RESP_BUF_C = ((16 + LINE_BYTES_P) + 15) & ~32'd15;
	localparam [31:0] PLD_MAX_C = RESP_BUF_C - 12;
	localparam [31:0] FRAME_MAX_C = FRAME_HDR_C + PLD_MAX_C;
	generate
		if (FRAME_MAX_C > TX_OVERSIZE_BYTES_P) begin : gen_g_frame_fit
			initial $display("Error [elaboration] $VALIDATION_STORAGE/reviews/r247-520-r1/protocol-processor/hdl/aecp/KL_aecp_engine.sv:809:5 - KL_aecp_engine.gen_g_frame_fit\n msg: ", "a maximum AECP response (%0d B) exceeds the oversize slot (%0d B)", FRAME_MAX_C, TX_OVERSIZE_BYTES_P);
		end
	endgenerate
	localparam [31:0] ucpu_pkg_RESP_CAP_C = 524;
	generate
		if (RESP_BUF_C < ucpu_pkg_RESP_CAP_C) begin : gen_g_resp_cap_fit
			initial $display("Error [elaboration] $VALIDATION_STORAGE/reviews/r247-520-r1/protocol-processor/hdl/aecp/KL_aecp_engine.sv:814:5 - KL_aecp_engine.gen_g_resp_cap_fit\n msg: ", "response buffer (%0d B) is smaller than GET_DYNAMIC_INFO limit (%0d B)", RESP_BUF_C, ucpu_pkg_RESP_CAP_C);
		end
	endgenerate
	wire [392:0] txn_w;
	function automatic [392:0] sv2v_cast_393;
		input reg [392:0] inp;
		sv2v_cast_393 = inp;
	endfunction
	assign txn_w = sv2v_cast_393(txn_i);
	wire rb_we_w;
	wire [9:0] rb_addr_w;
	wire [31:0] rb_wdata_w;
	wire [3:0] rb_wstrb_w;
	wire rb_ready_w;
	wire urb_we_w;
	reg g_rb_we_w;
	wire [9:0] urb_addr_w;
	reg [9:0] g_rb_addr_w;
	wire [31:0] urb_wdata_w;
	reg [31:0] g_rb_wdata_w;
	wire [3:0] urb_wstrb_w;
	reg [3:0] g_rb_wstrb_w;
	wire rsp_open_w;
	wire rsp_seal_w;
	wire [10:0] rsp_seal_len_w;
	wire rsp_rd_valid_w;
	wire rsp_rd_take_w;
	wire [7:0] rsp_rd_data_w;
	wire rsp_err_w;
	wire rsp_busy_w;
	reg [3:0] a_st_r;
	reg [392:0] cmd_r;
	reg [15:0] raw_ct_r;
	reg [15:0] cfg_ix_r;
	reg [15:0] desc_ty_r;
	reg [15:0] desc_ix_r;
	reg [15:0] name_ix_r;
	reg [15:0] name_cfg_r;
	reg [10:0] pld_cmd_r;
	reg [10:0] pld_r;
	reg [10:0] walk_r;
	reg [1:0] pid_lo_r;
	reg echo_r;
	reg sent_r;
	reg ctrs_r;
	reg amap_r;
	reg amap_edit_r;
	reg amap_remove_r;
	reg amap_uns_r;
	reg regun_r;
	reg acq_r;
	reg lockc_r;
	reg gstri_r;
	reg gavb_r;
	reg gasp_r;
	reg eavl_r;
	reg gcfg_r;
	reg gsfmt_r;
	reg gsrate_r;
	reg gclks_r;
	reg ssrate_r;
	reg sclks_r;
	reg ssfmt_r;
	reg ssinfo_r;
	reg gctrl_r;
	reg sctrl_r;
	reg gname_r;
	reg sname_r;
	reg scfg_r;
	reg strt_r;
	reg stop_r;
	reg strm_r;
	reg setc_r;
	reg gdi_r;
	reg [63:0] setval_r;
	reg [31:0] silat_r;
	reg lock_ent_ok_r;
	reg uns_r;
	reg [7:0] amap_rec_r;
	reg [10:0] upc_r;
	reg [4:0] status_r;
	reg [10:0] bidx_r;
	reg [10:0] frame_len_r;
	reg err_mode_r;
	reg [TXS_W_C - 1:0] tx_slot_r;
	reg [15:0] cmd_cnt_r;
	reg [15:0] resp_cnt_r;
	reg [15:0] drop_cnt_r;
	reg [15:0] rerr_cnt_r;
	reg g_scan_started_r;
	reg g_rd_pending_r;
	reg g_load_data_r;
	reg [2:0] g_hdr_ix_r;
	reg [1:0] g_wr_phase_r;
	reg [10:0] g_total_r;
	reg [10:0] g_rd_pos_r;
	reg [10:0] g_data_ix_r;
	reg [10:0] g_data_start_r;
	reg [10:0] g_next_pos_r;
	reg [10:0] g_out_r;
	reg [10:0] g_rec_rlen_r;
	reg [10:0] g_sub_end_r;
	reg [15:0] g_scan_len_r;
	reg [7:0] g_scan_cmd_hi_r;
	reg [15:0] g_rec_len_r;
	reg [15:0] g_rec_cmd_r;
	reg [7:0] g_rec_cmd_status_r;
	reg [63:0] g_data_head_r;
	reg g_rec_exec_r;
	reg [4:0] g_rec_status_r;
	reg g_shape_fault_r;
	function automatic gdi_allowed;
		input reg [15:0] command_type;
		(* full_case, parallel_case *)
		case (command_type)
			OP_GET_CONFIG_C, OP_GET_STREAM_FMT_C, GDI_GET_VIDEO_FMT_C, GDI_GET_SENSOR_FMT_C, OP_GET_STREAM_INFO_C, OP_GET_NAME_C, GDI_GET_ASSOC_ID_C, OP_GET_SAMP_RATE_C, OP_GET_CLOCK_SRC_C, GDI_GET_SIGNAL_SEL_C, OP_GET_COUNTERS_C, GDI_GET_MEM_LEN_C, GDI_GET_STREAM_BKUP_C: gdi_allowed = 1'b1;
			default: gdi_allowed = 1'b0;
		endcase
	endfunction
	reg g_sub_exec_w;
	reg [10:0] g_sub_rlen_w;
	reg [10:0] g_sub_upc_w;
	reg [4:0] g_sub_status_w;
	wire [15:0] g_sub_type_w;
	assign g_sub_type_w = g_data_head_r[63:48];
	localparam [4:0] ucpu_pkg_ST_BAD_ARGUMENTS_C = 5'd7;
	localparam [4:0] ucpu_pkg_ST_NOT_SUPPORTED_C = 5'd11;
	function automatic [10:0] sv2v_cast_11;
		input reg [10:0] inp;
		sv2v_cast_11 = inp;
	endfunction
	always @(*) begin : gdi_subcommand_decode
		if (_sv2v_0)
			;
		g_sub_exec_w = 1'b0;
		g_sub_rlen_w = sv2v_cast_11(g_rec_len_r);
		g_sub_upc_w = UPC_NOTIMPL_C;
		g_sub_status_w = ucpu_pkg_ST_NOT_SUPPORTED_C;
		(* full_case, parallel_case *)
		case (g_rec_cmd_r)
			OP_GET_CONFIG_C: begin
				g_sub_exec_w = 1'b1;
				g_sub_rlen_w = 11'd4;
				g_sub_upc_w = UPC_GCFG_C;
			end
			OP_GET_STREAM_FMT_C:
				if (g_rec_len_r < 16'd4)
					g_sub_status_w = ucpu_pkg_ST_BAD_ARGUMENTS_C;
				else begin
					g_sub_exec_w = 1'b1;
					g_sub_rlen_w = 11'd12;
					g_sub_upc_w = ((g_sub_type_w == DT_STREAM_INPUT_C) || (g_sub_type_w == DT_STREAM_OUTPUT_C) ? UPC_GSFMT_C : UPC_TIZ8NS_C);
				end
			OP_GET_STREAM_INFO_C:
				if (g_rec_len_r < 16'd4)
					g_sub_status_w = ucpu_pkg_ST_BAD_ARGUMENTS_C;
				else if ((g_sub_type_w != DT_STREAM_INPUT_C) && (g_sub_type_w != DT_STREAM_OUTPUT_C))
					g_sub_status_w = ucpu_pkg_ST_NOT_SUPPORTED_C;
				else begin
					g_sub_exec_w = 1'b1;
					g_sub_rlen_w = 11'd56;
					g_sub_upc_w = UPC_GSTRI_C;
				end
			OP_GET_SAMP_RATE_C:
				if (g_rec_len_r < 16'd4)
					g_sub_status_w = ucpu_pkg_ST_BAD_ARGUMENTS_C;
				else begin
					g_sub_exec_w = 1'b1;
					g_sub_rlen_w = 11'd8;
					g_sub_upc_w = (g_sub_type_w == DT_AUDIO_UNIT_C ? UPC_GSRATE_C : UPC_TIZ4NS_C);
				end
			OP_GET_CLOCK_SRC_C:
				if (g_rec_len_r < 16'd4)
					g_sub_status_w = ucpu_pkg_ST_BAD_ARGUMENTS_C;
				else begin
					g_sub_exec_w = 1'b1;
					g_sub_rlen_w = 11'd8;
					g_sub_upc_w = (g_sub_type_w == DT_CLOCK_DOMAIN_C ? UPC_GCLKS_C : UPC_TIZ4NS_C);
				end
			OP_GET_NAME_C:
				if (g_rec_len_r < 16'd8)
					g_sub_status_w = ucpu_pkg_ST_BAD_ARGUMENTS_C;
				else begin
					g_sub_exec_w = 1'b1;
					g_sub_rlen_w = 11'd72;
					g_sub_upc_w = UPC_GNAME_C;
				end
			OP_GET_COUNTERS_C:
				if (g_rec_len_r < 16'd4)
					g_sub_status_w = ucpu_pkg_ST_BAD_ARGUMENTS_C;
				else begin
					g_sub_exec_w = 1'b1;
					g_sub_rlen_w = 11'd136;
					g_sub_upc_w = ((((g_sub_type_w == DT_STREAM_INPUT_C) || (g_sub_type_w == DT_STREAM_OUTPUT_C)) || (g_sub_type_w == DT_AVB_INTERFACE_C)) || (g_sub_type_w == DT_CLOCK_DOMAIN_C) ? UPC_GCTRS_C : UPC_GCTRSNS_C);
				end
			default:
				;
		endcase
		if (g_rec_cmd_status_r != 8'd0) begin
			g_sub_exec_w = 1'b0;
			g_sub_rlen_w = sv2v_cast_11(g_rec_len_r);
			g_sub_upc_w = UPC_NOTIMPL_C;
			g_sub_status_w = ucpu_pkg_ST_BAD_ARGUMENTS_C;
		end
	end
	(* ram_style = "block" *) reg [63:0] amap_stage_r [0:255];
	reg [63:0] amap_stage_q_r;
	reg [63:0] amap_stage_assem_r;
	reg amap_stage_ready_r;
	reg [7:0] amap_rsp_count_r;
	wire [7:0] amap_rx_count_w;
	wire [10:0] amap_edit_pld_w;
	wire amap_stage_ser_w;
	wire amap_stage_ser_load_w;
	wire amap_stage_edit_load_w;
	wire amap_stage_name_load_w;
	wire amap_stage_rd_en_w;
	wire [7:0] amap_stage_raddr_w;
	function automatic [7:0] sv2v_cast_8;
		input reg [7:0] inp;
		sv2v_cast_8 = inp;
	endfunction
	assign amap_rx_count_w = (pld_cmd_r >= 11'd8 ? sv2v_cast_8((pld_cmd_r - 11'd8) >> 3) : 8'd0);
	assign amap_edit_pld_w = 11'd8 + ({3'd0, amap_rsp_count_r} << 3);
	reg [10:0] upc_w;
	reg echo_w;
	wire short_w;
	wire short_ct_w;
	wire short_am_w;
	wire ctrs_w;
	wire amap_w;
	wire aem_w;
	wire gdi_w;
	wire amap_edit_w;
	wire amap_remove_w;
	assign short_w = txn_w[344-:11] < 11'd20;
	assign short_ct_w = txn_w[344-:11] < 11'd16;
	assign short_am_w = txn_w[344-:11] < 11'd20;
	assign ctrs_w = (aem_w && (txn_w[139-:16] == OP_GET_COUNTERS_C)) && !short_ct_w;
	assign amap_w = (aem_w && (txn_w[139-:16] == OP_GET_AUDIO_MAP_C)) && !short_am_w;
	assign gdi_w = aem_w && (txn_w[139-:16] == OP_GET_DYNAMIC_INFO_C);
	assign amap_edit_w = aem_w && ((txn_w[139-:16] == OP_ADD_AUDIO_MAP_C) || (txn_w[139-:16] == OP_REMOVE_AUDIO_MAP_C));
	assign aem_w = (txn_w[356-:3] == 3'd2) && (txn_w[353-:4] == 4'd0);
	assign amap_remove_w = aem_w && (txn_w[139-:16] == OP_REMOVE_AUDIO_MAP_C);
	always @(*) begin : dispatch_decode
		if (_sv2v_0)
			;
		if ((aem_w && (txn_w[139-:16] == OP_READ_DESCRIPTOR_C)) && !short_w) begin
			upc_w = UPC_RDESC_C;
			echo_w = 1'b0;
		end
		else if (ctrs_w) begin
			upc_w = UPC_GCTRS_C;
			echo_w = 1'b0;
		end
		else if (amap_w) begin
			upc_w = UPC_GAMAP_C;
			echo_w = 1'b0;
		end
		else if (aem_w && ((((txn_w[139-:16] == OP_IDENTIFY_NOTIF_C) || ((txn_w[139-:16] == OP_READ_DESCRIPTOR_C) && short_w)) || ((txn_w[139-:16] == OP_GET_COUNTERS_C) && short_ct_w)) || ((txn_w[139-:16] == OP_GET_AUDIO_MAP_C) && short_am_w))) begin
			upc_w = UPC_BADARG_C;
			echo_w = 1'b1;
		end
		else begin
			upc_w = UPC_NOTIMPL_C;
			echo_w = 1'b1;
		end
	end
	wire drop_w;
	assign drop_w = txn_w[350] || (txn_w[221-:64] != entity_id_i);
	wire regun_w;
	wire acq_w;
	wire lockc_w;
	assign regun_w = aem_w && ((txn_w[139-:16] == OP_REG_UNSOL_C) || (txn_w[139-:16] == OP_DEREG_UNSOL_C));
	assign acq_w = aem_w && (txn_w[139-:16] == OP_ACQUIRE_C);
	assign lockc_w = aem_w && (txn_w[139-:16] == OP_LOCK_C);
	wire gstri_w;
	wire gavb_w;
	wire gasp_w;
	assign gstri_w = aem_w && (txn_w[139-:16] == OP_GET_STREAM_INFO_C);
	assign gavb_w = aem_w && (txn_w[139-:16] == OP_GET_AVB_INFO_C);
	assign gasp_w = aem_w && (txn_w[139-:16] == OP_GET_AS_PATH_C);
	wire eavl_w;
	wire gcfg_w;
	wire gsfmt_w;
	wire gsrate_w;
	wire gclks_w;
	assign eavl_w = aem_w && (txn_w[139-:16] == OP_ENTITY_AVAIL_C);
	assign gcfg_w = aem_w && (txn_w[139-:16] == OP_GET_CONFIG_C);
	assign gsfmt_w = aem_w && (txn_w[139-:16] == OP_GET_STREAM_FMT_C);
	assign gsrate_w = aem_w && (txn_w[139-:16] == OP_GET_SAMP_RATE_C);
	assign gclks_w = aem_w && (txn_w[139-:16] == OP_GET_CLOCK_SRC_C);
	wire ssrate_w;
	wire sclks_w;
	wire setc_w;
	assign ssrate_w = aem_w && (txn_w[139-:16] == OP_SET_SAMP_RATE_C);
	assign sclks_w = aem_w && (txn_w[139-:16] == OP_SET_CLOCK_SRC_C);
	wire gctrl_w;
	wire sctrl_w;
	assign gctrl_w = aem_w && (txn_w[139-:16] == OP_GET_CONTROL_C);
	assign sctrl_w = aem_w && (txn_w[139-:16] == OP_SET_CONTROL_C);
	wire gname_w;
	wire sname_w;
	assign gname_w = aem_w && (txn_w[139-:16] == OP_GET_NAME_C);
	assign sname_w = aem_w && (txn_w[139-:16] == OP_SET_NAME_C);
	wire ssfmt_w;
	wire ssinfo_w;
	assign ssfmt_w = aem_w && (txn_w[139-:16] == OP_SET_STREAM_FMT_C);
	assign ssinfo_w = aem_w && (txn_w[139-:16] == OP_SET_STREAM_INFO_C);
	assign setc_w = (((ssrate_w | sclks_w) | sctrl_w) | ssfmt_w) | ssinfo_w;
	wire scfg_w;
	assign scfg_w = aem_w && (txn_w[139-:16] == OP_SET_CONFIG_C);
	wire strt_w;
	wire stop_w;
	wire strm_w;
	assign strt_w = aem_w && (txn_w[139-:16] == OP_START_STRM_C);
	assign stop_w = aem_w && (txn_w[139-:16] == OP_STOP_STRM_C);
	assign strm_w = strt_w | stop_w;
	reg [15:0] uns_ct_w;
	reg [10:0] uns_upc_w;
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
	always @(*) begin : uns_kind_map
		if (_sv2v_0)
			;
		(* full_case, parallel_case *)
		case (uns_kind_i)
			pp_pkg_PP_UNS_DEREG_C: begin
				uns_ct_w = OP_DEREG_UNSOL_C;
				uns_upc_w = UPC_UNSOK_C;
			end
			pp_pkg_PP_UNS_LOCK_C: begin
				uns_ct_w = OP_LOCK_C;
				uns_upc_w = UPC_LOCKUNS_C;
			end
			pp_pkg_PP_UNS_STRI_C: begin
				uns_ct_w = OP_GET_STREAM_INFO_C;
				uns_upc_w = UPC_GSTRI_C;
			end
			pp_pkg_PP_UNS_AVB_C: begin
				uns_ct_w = OP_GET_AVB_INFO_C;
				uns_upc_w = UPC_GAVB_C;
			end
			pp_pkg_PP_UNS_ASP_C: begin
				uns_ct_w = OP_GET_AS_PATH_C;
				uns_upc_w = UPC_GASP_C;
			end
			pp_pkg_PP_UNS_AMAP_C: begin
				uns_ct_w = (uns_amap_remove_i ? OP_REMOVE_AUDIO_MAP_C : OP_ADD_AUDIO_MAP_C);
				uns_upc_w = UPC_UNSOK_C;
			end
			pp_pkg_PP_UNS_CTRS_C: begin
				uns_ct_w = OP_GET_COUNTERS_C;
				uns_upc_w = UPC_GCTRS_C;
			end
			pp_pkg_PP_UNS_SRATE_C: begin
				uns_ct_w = OP_SET_SAMP_RATE_C;
				uns_upc_w = UPC_GSRATE_C;
			end
			pp_pkg_PP_UNS_NAME_C: begin
				uns_ct_w = OP_SET_NAME_C;
				uns_upc_w = UPC_GNAME_C;
			end
			pp_pkg_PP_UNS_CFG_C: begin
				uns_ct_w = OP_SET_CONFIG_C;
				uns_upc_w = UPC_GCFG_C;
			end
			pp_pkg_PP_UNS_SFMT_C: begin
				uns_ct_w = OP_SET_STREAM_FMT_C;
				uns_upc_w = UPC_GSFMT_C;
			end
			pp_pkg_PP_UNS_SINFO_C: begin
				uns_ct_w = OP_SET_STREAM_INFO_C;
				uns_upc_w = UPC_GSTRI_C;
			end
			pp_pkg_PP_UNS_CTRL_C: begin
				uns_ct_w = OP_SET_CONTROL_C;
				uns_upc_w = UPC_GCTRL_C;
			end
			pp_pkg_PP_UNS_CLKS_C: begin
				uns_ct_w = OP_SET_CLOCK_SRC_C;
				uns_upc_w = UPC_GCLKS_C;
			end
			pp_pkg_PP_UNS_STRM_C: begin
				uns_ct_w = (uns_arg0_i[0] ? OP_STOP_STRM_C : OP_START_STRM_C);
				uns_upc_w = UPC_STRMUNS_C;
			end
			default: begin
				uns_ct_w = 16'd0;
				uns_upc_w = UPC_NOSEND_C;
			end
		endcase
	end
	wire mvu_get_milan_info_w;
	assign mvu_get_milan_info_w = (((((cmd_r[356-:3] == 3'd3) && (pld_cmd_r >= MVU_CMD_PLD_C)) && (raw_ct_r == MVU_PID_HI_C)) && (cfg_ix_r == MVU_PID_MD_C)) && (pid_lo_r == 2'b11)) && (desc_ty_r == MVU_GET_MILAN_INFO_C);
	wire [10:0] cdl_pld_w;
	wire [10:0] slot_pld_w;
	wire [10:0] pld_cap_w;
	wire [10:0] pld_trim_w;
	assign cdl_pld_w = (txn_w[344-:11] > 11'd12 ? txn_w[344-:11] - 11'd12 : 11'd0);
	assign pld_cap_w = (cdl_pld_w > sv2v_cast_11(PLD_MAX_C) ? sv2v_cast_11(PLD_MAX_C) : cdl_pld_w);
	function automatic [31:0] sv2v_cast_32;
		input reg [31:0] inp;
		sv2v_cast_32 = inp;
	endfunction
	assign slot_pld_w = (sv2v_cast_32(rxs_slot_len_i) > AECP_HDR_C ? sv2v_cast_11(sv2v_cast_32(rxs_slot_len_i) - AECP_HDR_C) : 11'd0);
	assign pld_trim_w = (pld_r > slot_pld_w ? slot_pld_w : pld_r);
	reg disp_valid_r;
	wire disp_ready_w;
	wire ucpu_busy_w;
	wire ucpu_done_w;
	wire resp_send_w;
	wire [10:0] resp_len_w;
	wire [4:0] resp_status_w;
	wire [63:0] opd0_w;
	wire [63:0] opd1_w;
	wire [63:0] opd2_w;
	wire any_running_w;
	assign any_running_w = |strm_bound_i || |strm_streaming_i;
	wire run_this_w;
	function automatic [0:0] sv2v_cast_1;
		input reg [0:0] inp;
		sv2v_cast_1 = inp;
	endfunction
	assign run_this_w = (cfg_ix_r == DT_STREAM_INPUT_C ? (sv2v_cast_32(desc_ix_r) < N_STREAM_IN_P) && sv2v_cast_1(strm_bound_i >> desc_ix_r) : (sv2v_cast_32(desc_ix_r) < N_STREAM_OUT_P) && sv2v_cast_1(strm_streaming_i >> desc_ix_r));
	wire ix26_w;
	wire tix_w;
	assign tix_w = (((((((((((((ctrs_r | amap_r) | amap_edit_r) | gstri_r) | gavb_r) | gsfmt_r) | gsrate_r) | gclks_r) | setc_r) | gctrl_r) | strm_r) | ssfmt_r) | ssinfo_r) | gname_r) | sname_r;
	assign ix26_w = ((tix_w | regun_r) | lockc_r) | scfg_r;
	assign opd0_w = (gname_r || sname_r ? {16'd0, desc_ix_r, cfg_ix_r, name_cfg_r} : (tix_w ? {16'd0, desc_ix_r, cfg_ix_r, 16'd0} : (gasp_r ? {16'd0, cfg_ix_r, DT_AVB_INTERFACE_C, 16'd0} : (lockc_r ? {32'd0, cfg_ix_r, desc_ix_r} : {16'd0, desc_ix_r, desc_ty_r, cfg_ix_r}))));
	assign opd1_w = (gname_r || sname_r ? {cfg_ix_r, desc_ix_r, name_ix_r, name_cfg_r} : (amap_r ? {32'd0, desc_ix_r, desc_ty_r} : (tix_w ? {32'd0, cfg_ix_r, desc_ix_r} : (gasp_r ? {48'd0, cfg_ix_r} : (scfg_r ? {48'd0, desc_ix_r} : {32'd0, desc_ty_r, desc_ix_r})))));
	assign opd2_w = (gname_r || sname_r ? {48'd0, name_ix_r} : (amap_edit_r ? {48'd0, desc_ty_r} : (ssrate_r ? {32'd0, setval_r[63:32]} : (sclks_r ? {48'd0, setval_r[63:48]} : (sctrl_r ? {56'd0, setval_r[63:56]} : (scfg_r ? {48'd0, desc_ix_r} : (ssinfo_r ? {32'd0, silat_r} : setval_r)))))));
	reg [63:0] opd0_r;
	reg [63:0] opd1_r;
	reg [63:0] opd2_r;
	wire st_req_w;
	wire st_we_w;
	wire st_name_w;
	wire [19:0] st_addr_w;
	wire [63:0] st_wdata_w;
	wire [63:0] st_rdata_w;
	wire [7:0] st_wstrb_w;
	wire st_ready_w;
	wire st_rvalid_w;
	wire st_err_w;
	localparam [3:0] RGN_DYN_C = 4'h1;
	localparam [3:0] RGN_DYNV_C = 4'h2;
	localparam [3:0] RGN_STRQ_C = 4'h3;
	wire dyn_sel_w;
	wire strq_sel_w;
	wire dyn_ready_w;
	wire dyn_rvalid_w;
	wire [63:0] dyn_rdata_w;
	wire store_ready_w;
	wire store_rvalid_w;
	wire store_err_w;
	wire [63:0] store_rdata_w;
	assign dyn_sel_w = !st_name_w && ((st_addr_w[19:16] == RGN_DYN_C) || (st_addr_w[19:16] == RGN_DYNV_C));
	assign strq_sel_w = (!st_name_w && st_we_w) && (st_addr_w[19:16] == RGN_STRQ_C);
	assign st_ready_w = (strq_sel_w ? strm_set_ready_i : (dyn_sel_w ? dyn_ready_w : store_ready_w));
	assign st_rvalid_w = (strq_sel_w ? 1'b0 : (dyn_sel_w ? dyn_rvalid_w : store_rvalid_w));
	assign st_rdata_w = (dyn_sel_w ? dyn_rdata_w : store_rdata_w);
	assign strm_set_valid_o = strq_sel_w && st_req_w;
	assign strm_set_index_o = desc_ix_r;
	assign strm_set_val_o = st_wdata_w[0];
	assign st_err_w = (strq_sel_w ? strm_set_error_i : (dyn_sel_w ? 1'b0 : store_err_w));
	wire gx_req_w;
	wire gx_valid_w;
	wire [7:0] gx_sel_w;
	wire [63:0] gx_data_w;
	wire ucpu_ovf_nc_w;
	wire [10:0] ucpu_upc_nc_w;
	wire [4:0] ucpu_st_nc_w;
	function automatic [9:0] sv2v_cast_10;
		input reg [9:0] inp;
		sv2v_cast_10 = inp;
	endfunction
	KL_aecp_ucpu #(.UCODE_HEX_P(UCODE_HEX_P)) u_ucpu(
		.clk_i(clk_i),
		.rst_n(rst_n),
		.disp_valid_i(disp_valid_r),
		.disp_ready_o(disp_ready_w),
		.disp_upc_i(upc_r),
		.disp_ctlr_eid_i(cmd_r[285-:64]),
		.disp_opd0_i(opd0_r),
		.disp_opd1_i(opd1_r),
		.disp_opd2_i(opd2_r),
		.disp_batch_i(gdi_r),
		.disp_resp_base_i(sv2v_cast_10(g_out_r + 11'd8)),
		.st_req_o(st_req_w),
		.st_we_o(st_we_w),
		.st_name_o(st_name_w),
		.st_addr_o(st_addr_w),
		.st_wdata_o(st_wdata_w),
		.st_wstrb_o(st_wstrb_w),
		.st_ready_i(st_ready_w),
		.st_rvalid_i(st_rvalid_w),
		.st_rdata_i(st_rdata_w),
		.st_err_i(st_err_w),
		.gx_req_o(gx_req_w),
		.gx_sel_o(gx_sel_w),
		.gx_valid_i(gx_valid_w),
		.gx_data_i(gx_data_w),
		.lock_held_i(lock_held_i),
		.lock_ctlr_i(lock_ctlr_i),
		.rb_we_o(urb_we_w),
		.rb_addr_o(urb_addr_w),
		.rb_wdata_o(urb_wdata_w),
		.rb_wstrb_o(urb_wstrb_w),
		.rb_ready_i(rb_ready_w),
		.resp_send_o(resp_send_w),
		.resp_len_o(resp_len_w),
		.resp_status_o(resp_status_w),
		.tx_ready_i(1'b1),
		.eff_commit_o(eff_commit_o),
		.eff_nvm_mark_o(eff_nvm_mark_o),
		.eff_nvm_stb_o(eff_nvm_stb_o),
		.eff_notify_class_o(eff_notify_class_o),
		.eff_notify_stb_o(eff_notify_stb_o),
		.busy_o(ucpu_busy_w),
		.done_o(ucpu_done_w),
		.dbg_upc_o(ucpu_upc_nc_w),
		.dbg_status_o(ucpu_st_nc_w),
		.dbg_ovf_o(ucpu_ovf_nc_w)
	);
	always @(*) begin : notify_effect_context
		if (_sv2v_0)
			;
		eff_notify_type_o = cfg_ix_r;
		eff_notify_index_o = desc_ix_r;
		eff_notify_arg0_o = 16'd0;
		eff_notify_arg1_o = 16'd0;
		eff_notify_excl_eid_o = cmd_r[285-:64];
		if (eff_notify_class_o == 4'd1) begin
			eff_notify_type_o = DT_ENTITY_C;
			eff_notify_index_o = 16'd0;
			eff_notify_arg0_o = desc_ix_r;
		end
		else if (eff_notify_class_o == 4'd7) begin
			eff_notify_arg0_o = name_ix_r;
			eff_notify_arg1_o = name_cfg_r;
		end
		else if (eff_notify_class_o == 4'd9)
			eff_notify_arg0_o = cmd_r[139-:16];
	end
	wire [15:0] store_fetch_nc_w;
	wire [15:0] store_rowr_nc_w;
	wire [15:0] store_dlen_nc_w;
	KL_aecp_desc_store #(
		.DESC_BASE_P(DESC_BASE_P),
		.LINE_BYTES_P(LINE_BYTES_P),
		.IDX_ENTRIES_P(IDX_ENTRIES_P),
		.NAME_ENTRIES_P(NAME_ENTRIES_P),
		.MEM_TIMEOUT_CYC_P(MEM_TIMEOUT_CYC_P)
	) u_store(
		.clk_i(clk_i),
		.rst_n(rst_n),
		.st_req_i((st_req_w && !dyn_sel_w) && !strq_sel_w),
		.st_we_i(st_we_w),
		.st_name_i(st_name_w),
		.st_addr_i(st_addr_w),
		.st_wdata_i(st_wdata_w),
		.st_wstrb_i(st_wstrb_w),
		.st_ready_o(store_ready_w),
		.st_rvalid_o(store_rvalid_w),
		.st_rdata_o(store_rdata_w),
		.st_err_o(store_err_w),
		.mem_req_valid_o(mem_req_valid_o),
		.mem_req_ready_i(mem_req_ready_i),
		.mem_req_addr_o(mem_req_addr_o),
		.mem_req_beats_o(mem_req_beats_o),
		.mem_rsp_valid_i(mem_rsp_valid_i),
		.mem_rsp_ready_o(mem_rsp_ready_o),
		.mem_rsp_data_i(mem_rsp_data_i),
		.mem_rsp_last_i(mem_rsp_last_i),
		.mem_rsp_err_i(mem_rsp_err_i),
		.dbg_img_valid_o(dbg_img_valid_o),
		.dbg_fault_o(dbg_img_fault_o),
		.dbg_locate_miss_o(dbg_locate_miss_o),
		.dbg_fetch_cnt_o(store_fetch_nc_w),
		.dbg_ro_write_o(store_rowr_nc_w),
		.dbg_desc_len_o(store_dlen_nc_w)
	);
	wire [15:0] dyn_writes_nc_w;
	wire [15:0] dyn_oob_nc_w;
	KL_aecp_dyn_state #(
		.N_STREAM_IN_P(N_STREAM_IN_P),
		.N_STREAM_OUT_P(N_STREAM_OUT_P),
		.N_AUDIO_UNIT_P(N_AUDIO_UNIT_P),
		.N_CLK_DOMAIN_P(N_CLK_DOMAIN_P),
		.N_CONTROL_P(N_CONTROL_P)
	) u_dyn(
		.clk_i(clk_i),
		.rst_n(rst_n),
		.st_req_i(st_req_w && dyn_sel_w),
		.st_we_i(st_we_w),
		.st_addr_i(st_addr_w),
		.st_wdata_i(st_wdata_w),
		.st_ready_o(dyn_ready_w),
		.st_rvalid_o(dyn_rvalid_w),
		.st_rdata_o(dyn_rdata_w),
		.desc_index_i((scfg_r ? 16'd0 : desc_ix_r)),
		.cur_config_o(dyn_cur_config_o),
		.identify_o(dyn_identify_o),
		.clk_src_index_o(dyn_clk_src_index_o),
		.pt_offset_o(dyn_pt_offset_o),
		.pt_offset_v_o(dyn_pt_offset_v_o),
		.fmt_in_o(dyn_fmt_in_o),
		.fmt_in_v_o(dyn_fmt_in_v_o),
		.fmt_out_o(dyn_fmt_out_o),
		.fmt_out_v_o(dyn_fmt_out_v_o),
		.dirty_o(dyn_dirty_o),
		.dbg_writes_o(dyn_writes_nc_w),
		.dbg_oob_o(dyn_oob_nc_w)
	);
	wire [15:0] resp_burst_nc_w;
	wire [15:0] resp_drop_nc_w;
	always @(*) begin : gdi_response_write
		if (_sv2v_0)
			;
		g_rb_we_w = 1'b0;
		g_rb_addr_w = sv2v_cast_10(g_out_r);
		g_rb_wdata_w = 32'd0;
		g_rb_wstrb_w = 4'hf;
		if (a_st_r == 4'd12) begin
			g_rb_we_w = 1'b1;
			if (g_wr_phase_r == 2'd0)
				g_rb_wdata_w = {5'd0, g_rec_rlen_r, 16'd0};
			else begin
				g_rb_addr_w = sv2v_cast_10(g_out_r + 11'd4);
				g_rb_wdata_w = {3'd0, (g_rec_exec_r ? 5'd0 : g_rec_status_r), 8'd0, g_rec_cmd_r};
			end
		end
		else if ((a_st_r == 4'd13) && g_rd_pending_r) begin
			g_rb_we_w = 1'b1;
			g_rb_addr_w = sv2v_cast_10((g_out_r + 11'd8) + g_data_ix_r);
			g_rb_wdata_w = {24'd0, rxs_rd_data_i};
			g_rb_wstrb_w = 4'h1;
		end
		else if (a_st_r == 4'd14) begin
			g_rb_we_w = 1'b1;
			g_rb_addr_w = sv2v_cast_10(g_out_r + 11'd4);
			g_rb_wdata_w = {27'h0000000, g_rec_status_r};
			g_rb_wstrb_w = 4'h1;
		end
	end
	assign rb_we_w = (g_rb_we_w ? 1'b1 : urb_we_w);
	assign rb_addr_w = (g_rb_we_w ? g_rb_addr_w : urb_addr_w);
	assign rb_wdata_w = (g_rb_we_w ? g_rb_wdata_w : urb_wdata_w);
	assign rb_wstrb_w = (g_rb_we_w ? g_rb_wstrb_w : urb_wstrb_w);
	KL_aecp_resp_buf #(
		.RESP_BASE_P(RESP_BASE_P),
		.RESP_BYTES_P(RESP_BUF_C),
		.MEM_TIMEOUT_CYC_P(MEM_TIMEOUT_CYC_P)
	) u_resp(
		.clk_i(clk_i),
		.rst_n(rst_n),
		.open_i(rsp_open_w),
		.seal_i(rsp_seal_w),
		.seal_len_i(rsp_seal_len_w),
		.wr_we_i(rb_we_w),
		.wr_addr_i(rb_addr_w),
		.wr_wdata_i(rb_wdata_w),
		.wr_wstrb_i(rb_wstrb_w),
		.wr_ready_o(rb_ready_w),
		.rd_valid_o(rsp_rd_valid_w),
		.rd_data_o(rsp_rd_data_w),
		.rd_take_i(rsp_rd_take_w),
		.mem_req_valid_o(rmem_req_valid_o),
		.mem_req_ready_i(rmem_req_ready_i),
		.mem_req_addr_o(rmem_req_addr_o),
		.mem_req_beats_o(rmem_req_beats_o),
		.mem_rsp_valid_i(rmem_rsp_valid_i),
		.mem_rsp_ready_o(rmem_rsp_ready_o),
		.mem_rsp_data_i(rmem_rsp_data_i),
		.mem_rsp_last_i(rmem_rsp_last_i),
		.mem_rsp_err_i(rmem_rsp_err_i),
		.mem_wr_valid_o(rmem_wr_valid_o),
		.mem_wr_ready_i(rmem_wr_ready_i),
		.mem_wr_addr_o(rmem_wr_addr_o),
		.mem_wr_data_o(rmem_wr_data_o),
		.mem_wr_strb_o(rmem_wr_strb_o),
		.mem_wr_done_i(rmem_wr_done_i),
		.mem_wr_err_i(rmem_wr_err_i),
		.busy_o(rsp_busy_w),
		.err_o(rsp_err_w),
		.dbg_fault_o(dbg_resp_fault_o),
		.dbg_lane_wr_o(dbg_resp_lane_o),
		.dbg_burst_o(resp_burst_nc_w),
		.dbg_drop_o(resp_drop_nc_w)
	);
	wire gx_alt_w;
	wire gsi_any_w;
	wire rgy_any_w;
	wire strm_state_w;
	assign gsi_any_w = ((((gstri_r | gavb_r) | gasp_r) | gsfmt_r) | ssfmt_r) | ssinfo_r;
	assign rgy_any_w = (regun_r | lockc_r) | eavl_r;
	assign strm_state_w = (strt_r || stop_r) && (gx_sel_w[7:4] == 4'hd);
	assign gx_alt_w = ((((amap_r | amap_edit_r) | sname_r) | rgy_any_w) | gsi_any_w) | strm_state_w;
	assign ctr_req_o = gx_req_w && !gx_alt_w;
	assign ctr_desc_type_o = cfg_ix_r;
	assign ctr_desc_index_o = desc_ix_r;
	assign ctr_word_o = (gx_sel_w[7] ? 6'd32 : {1'b0, gx_sel_w[6:4], gx_sel_w[1:0]});
	assign gsi_req_o = gx_req_w && gsi_any_w;
	assign gsi_kind_o = (((gstri_r || gsfmt_r) || ssfmt_r) || ssinfo_r ? 2'd0 : (gavb_r ? 2'd1 : 2'd2));
	assign gsi_desc_type_o = cfg_ix_r;
	assign gsi_desc_index_o = desc_ix_r;
	assign gsi_sel_o = gx_sel_w[3:0];
	assign gsi_ord_o = amap_rec_r;
	assign gsi_prop_fmt_o = setval_r;
	assign rgy_req_o = gx_req_w && rgy_any_w;
	assign rgy_state_o = gx_sel_w[0];
	assign rgy_op_o = (lockc_r ? {1'b1, desc_ix_r[0]} : {1'b0, cmd_r[124]});
	assign rgy_eid_o = cmd_r[285-:64];
	assign rgy_mac_o = cmd_r[333-:48];
	assign rgy_tl_o = (cmd_r[344-:11] >= 11'd16) && desc_ix_r[0];
	assign amap_req_o = gx_req_w && amap_r;
	assign amap_desc_type_o = cfg_ix_r;
	assign amap_desc_index_o = desc_ix_r;
	assign amap_map_index_o = desc_ty_r;
	assign amap_sel_o = (gx_sel_w[4] ? 2'd2 : {1'b0, gx_sel_w[0]});
	assign amap_rec_o = amap_rec_r;
	always @(*) begin : amap_edit_phase_decode
		if (_sv2v_0)
			;
		(* full_case, parallel_case *)
		case (gx_sel_w)
			8'h20: amap_edit_phase_o = 3'd0;
			8'h30: amap_edit_phase_o = 3'd1;
			8'h22: amap_edit_phase_o = 3'd2;
			8'h23: amap_edit_phase_o = 3'd3;
			8'h40: amap_edit_phase_o = 3'd4;
			8'h50: amap_edit_phase_o = 3'd5;
			default: amap_edit_phase_o = 3'd3;
		endcase
	end
	assign amap_edit_req_o = (gx_req_w && amap_edit_r) && ((amap_edit_phase_o < 3'd4) || amap_stage_ready_r);
	assign amap_edit_remove_o = amap_remove_r;
	assign amap_edit_desc_type_o = cfg_ix_r;
	assign amap_edit_desc_index_o = desc_ix_r;
	assign amap_edit_count_o = desc_ty_r;
	assign amap_edit_rec_o = amap_rec_r;
	assign amap_edit_record_o = amap_stage_q_r;
	assign amap_edit_value_o = setval_r;
	assign amap_stage_ser_w = (amap_uns_r || amap_edit_r) && (a_st_r == 4'd5);
	assign amap_stage_ser_load_w = ((amap_stage_ser_w && (bidx_r >= sv2v_cast_11(FRAME_HDR_C + 7))) && (bidx_r < (sv2v_cast_11(FRAME_HDR_C) + pld_r))) && (((bidx_r - sv2v_cast_11(FRAME_HDR_C + 7)) & 11'd7) == 0);
	assign amap_stage_edit_load_w = (((!amap_stage_ser_w && gx_req_w) && amap_edit_r) && (amap_edit_phase_o >= 3'd4)) && !amap_stage_ready_r;
	assign amap_stage_name_load_w = (((!amap_stage_ser_w && gx_req_w) && sname_r) && (gx_sel_w[7:3] == 5'b01100)) && !amap_stage_ready_r;
	assign amap_stage_rd_en_w = (amap_stage_ser_load_w || amap_stage_edit_load_w) || amap_stage_name_load_w;
	assign amap_stage_raddr_w = (amap_stage_ser_w ? sv2v_cast_8((bidx_r - sv2v_cast_11(FRAME_HDR_C + 7)) >> 3) : (sname_r ? {5'd0, gx_sel_w[2:0]} : amap_rec_r));
	always @(posedge clk_i) begin : amap_stage_read
		if (!rst_n) begin
			amap_stage_q_r <= 64'd0;
			amap_stage_ready_r <= 1'b0;
		end
		else begin
			if (amap_stage_ser_w)
				amap_stage_ready_r <= 1'b0;
			else if (!gx_req_w || (!(amap_edit_r && (amap_edit_phase_o >= 3'd4)) && !sname_r))
				amap_stage_ready_r <= 1'b0;
			else if (!amap_stage_ready_r)
				amap_stage_ready_r <= 1'b1;
			if (amap_stage_rd_en_w)
				amap_stage_q_r <= amap_stage_r[amap_stage_raddr_w];
		end
	end
	always @(posedge clk_i) begin : amap_stage_write
		if (!rst_n)
			amap_stage_assem_r <= 64'd0;
		else if (a_st_r == 4'd0)
			amap_stage_assem_r <= 64'd0;
		else if (((a_st_r == 4'd1) && (amap_edit_r || sname_r)) && (walk_r >= 11'd11)) begin
			amap_stage_assem_r <= {amap_stage_assem_r[55:0], rxs_rd_data_i};
			if (((walk_r - 11'd11) & 11'd7) == 11'd7)
				amap_stage_r[sv2v_cast_8((walk_r - 11'd11) >> 3)] <= {amap_stage_assem_r[55:0], rxs_rd_data_i};
		end
	end
	localparam [31:0] CTO_W_C = $clog2(MEM_TIMEOUT_CYC_P + 1);
	reg [CTO_W_C - 1:0] gxf_tmo_r;
	reg gxf_fail_r;
	wire ctr_hold_w;
	wire amap_hold_w;
	wire amap_edit_hold_w;
	wire name_hold_w;
	wire rgy_hold_w;
	wire gsi_hold_w;
	assign ctr_hold_w = ((gx_req_w && !gx_alt_w) && ctr_wait_i) && !gxf_fail_r;
	assign amap_hold_w = ((gx_req_w && amap_r) && amap_wait_i) && !gxf_fail_r;
	assign amap_edit_hold_w = ((gx_req_w && amap_edit_r) && !gxf_fail_r) && (((amap_edit_phase_o >= 3'd4) && !amap_stage_ready_r) || (((amap_edit_req_o && amap_edit_wait_i) && (amap_edit_phase_o != 3'd2)) && (amap_edit_phase_o != 3'd5)));
	assign name_hold_w = ((gx_req_w && sname_r) && !amap_stage_ready_r) && !gxf_fail_r;
	assign rgy_hold_w = ((gx_req_w && (regun_r || lockc_r)) && rgy_wait_i) && !gxf_fail_r;
	assign gsi_hold_w = ((gx_req_w && gsi_any_w) && gsi_wait_i) && !gxf_fail_r;
	reg gxr_valid_r;
	reg [63:0] gxr_data_r;
	always @(posedge clk_i) begin : gather_answer
		if (!rst_n) begin
			gxr_valid_r <= 1'b0;
			gxr_data_r <= 64'd0;
		end
		else begin
			gxr_valid_r <= (gx_req_w && !gxr_valid_r) && !(((((ctr_hold_w || amap_hold_w) || amap_edit_hold_w) || name_hold_w) || rgy_hold_w) || gsi_hold_w);
			gxr_data_r <= (gxf_fail_r ? 64'd0 : (amap_r ? amap_data_i : (amap_edit_r ? amap_edit_data_i : (sname_r ? amap_stage_q_r : (rgy_any_w ? rgy_data_i : (strm_state_w ? (sv2v_cast_32(desc_ix_r) < N_STREAM_IN_P ? {63'd0, sv2v_cast_1(strm_bound_i >> desc_ix_r) && sv2v_cast_1(strm_started_i >> desc_ix_r)} : 64'd0) : (gsi_any_w ? gsi_data_i : {32'd0, ctr_data_i})))))));
		end
	end
	assign gx_valid_w = gxr_valid_r;
	assign gx_data_w = gxr_data_r;
	function automatic [CTO_W_C - 1:0] sv2v_cast_0112E;
		input reg [CTO_W_C - 1:0] inp;
		sv2v_cast_0112E = inp;
	endfunction
	function automatic signed [CTO_W_C - 1:0] sv2v_cast_0112E_signed;
		input reg signed [CTO_W_C - 1:0] inp;
		sv2v_cast_0112E_signed = inp;
	endfunction
	always @(posedge clk_i) begin : gather_watchdog
		if (!rst_n) begin
			gxf_tmo_r <= 1'sb0;
			gxf_fail_r <= 1'b0;
		end
		else if (a_st_r == 4'd0) begin
			gxf_tmo_r <= 1'sb0;
			gxf_fail_r <= 1'b0;
		end
		else if (((((ctr_hold_w || amap_hold_w) || amap_edit_hold_w) || name_hold_w) || rgy_hold_w) || gsi_hold_w) begin
			if (gxf_tmo_r == sv2v_cast_0112E(MEM_TIMEOUT_CYC_P))
				gxf_fail_r <= 1'b1;
			else
				gxf_tmo_r <= gxf_tmo_r + sv2v_cast_0112E_signed(1);
		end
		else
			gxf_tmo_r <= 1'sb0;
	end
	always @(posedge clk_i) begin : amap_record_ordinal
		if (!rst_n)
			amap_rec_r <= 8'd0;
		else if (a_st_r == 4'd0)
			amap_rec_r <= 8'd0;
		else if ((amap_edit_req_o && gx_valid_w) && (amap_edit_phase_o <= 3'd1))
			amap_rec_r <= 8'd0;
		else if (((((amap_req_o && gx_sel_w[4]) || (amap_edit_req_o && (amap_edit_phase_o >= 3'd4))) || (gsi_req_o && gx_sel_w[3])) && gx_valid_w) && (amap_rec_r != 8'hff))
			amap_rec_r <= amap_rec_r + 8'd1;
	end
	wire [15:0] cdl_w;
	assign cdl_w = 16'd12 + {5'd0, pld_r};
	wire [3:0] resp_mt_w;
	assign resp_mt_w = cmd_r[353-:4] | 4'd1;
	reg [7:0] hdr_byte_w;
	always @(*) begin : frame_header_byte
		if (_sv2v_0)
			;
		(* full_case, parallel_case *)
		case (bidx_r[5:0])
			6'd0: hdr_byte_w = cmd_r[333:326];
			6'd1: hdr_byte_w = cmd_r[325:318];
			6'd2: hdr_byte_w = cmd_r[317:310];
			6'd3: hdr_byte_w = cmd_r[309:302];
			6'd4: hdr_byte_w = cmd_r[301:294];
			6'd5: hdr_byte_w = cmd_r[293:286];
			6'd6: hdr_byte_w = own_mac_i[47:40];
			6'd7: hdr_byte_w = own_mac_i[39:32];
			6'd8: hdr_byte_w = own_mac_i[31:24];
			6'd9: hdr_byte_w = own_mac_i[23:16];
			6'd10: hdr_byte_w = own_mac_i[15:8];
			6'd11: hdr_byte_w = own_mac_i[7:0];
			6'd12: hdr_byte_w = 8'h22;
			6'd13: hdr_byte_w = 8'hf0;
			6'd14: hdr_byte_w = 8'hfb;
			6'd15: hdr_byte_w = {4'b0000, resp_mt_w};
			6'd16: hdr_byte_w = {status_r, cdl_w[10:8]};
			6'd17: hdr_byte_w = cdl_w[7:0];
			6'd18: hdr_byte_w = entity_id_i[63:56];
			6'd19: hdr_byte_w = entity_id_i[55:48];
			6'd20: hdr_byte_w = entity_id_i[47:40];
			6'd21: hdr_byte_w = entity_id_i[39:32];
			6'd22: hdr_byte_w = entity_id_i[31:24];
			6'd23: hdr_byte_w = entity_id_i[23:16];
			6'd24: hdr_byte_w = entity_id_i[15:8];
			6'd25: hdr_byte_w = entity_id_i[7:0];
			6'd26: hdr_byte_w = cmd_r[285:278];
			6'd27: hdr_byte_w = cmd_r[277:270];
			6'd28: hdr_byte_w = cmd_r[269:262];
			6'd29: hdr_byte_w = cmd_r[261:254];
			6'd30: hdr_byte_w = cmd_r[253:246];
			6'd31: hdr_byte_w = cmd_r[245:238];
			6'd32: hdr_byte_w = cmd_r[237:230];
			6'd33: hdr_byte_w = cmd_r[229:222];
			6'd34: hdr_byte_w = cmd_r[157:150];
			6'd35: hdr_byte_w = cmd_r[149:142];
			6'd36: hdr_byte_w = ((cmd_r[356-:3] == 3'd2) && (cmd_r[353-:4] == 4'd0) ? {uns_r, raw_ct_r[14:8]} : raw_ct_r[15:8]);
			6'd37: hdr_byte_w = raw_ct_r[7:0];
			default: hdr_byte_w = 8'd0;
		endcase
	end
	wire pay_w;
	assign pay_w = (bidx_r >= sv2v_cast_11(FRAME_HDR_C)) && (bidx_r < (sv2v_cast_11(FRAME_HDR_C) + pld_r));
	reg [7:0] frame_byte_w;
	reg [10:0] amap_uns_pidx_w;
	reg [7:0] amap_uns_byte_w;
	wire [15:0] amap_emit_count_w;
	assign amap_emit_count_w = (amap_uns_r ? desc_ty_r : {8'd0, amap_rsp_count_r});
	always @(*) begin : amap_uns_payload
		if (_sv2v_0)
			;
		amap_uns_pidx_w = bidx_r - sv2v_cast_11(FRAME_HDR_C);
		(* full_case, parallel_case *)
		case (amap_uns_pidx_w)
			11'd0: amap_uns_byte_w = cfg_ix_r[15:8];
			11'd1: amap_uns_byte_w = cfg_ix_r[7:0];
			11'd2: amap_uns_byte_w = desc_ix_r[15:8];
			11'd3: amap_uns_byte_w = desc_ix_r[7:0];
			11'd4: amap_uns_byte_w = amap_emit_count_w[15:8];
			11'd5: amap_uns_byte_w = amap_emit_count_w[7:0];
			11'd6, 11'd7: amap_uns_byte_w = 8'd0;
			default: amap_uns_byte_w = amap_stage_q_r[63 - (8 * ((amap_uns_pidx_w - 11'd8) & 11'd7))-:8];
		endcase
	end
	always @(*) begin : frame_byte
		if (_sv2v_0)
			;
		if (bidx_r < sv2v_cast_11(FRAME_HDR_C))
			frame_byte_w = hdr_byte_w;
		else if (pay_w)
			frame_byte_w = (amap_uns_r || amap_edit_r ? amap_uns_byte_w : (echo_r ? rxs_rd_data_i : rsp_rd_data_w));
		else
			frame_byte_w = 8'd0;
	end
	wire byte_ok_w;
	assign byte_ok_w = (((!pay_w || amap_uns_r) || amap_edit_r) || echo_r) || rsp_rd_valid_w;
	assign rsp_rd_take_w = ((((a_st_r == 4'd5) && pay_w) && !echo_r) && !amap_edit_r) && rsp_rd_valid_w;
	wire [10:0] pref_ix_w;
	wire pref_en_w;
	assign pref_ix_w = (bidx_r + 11'd1) - sv2v_cast_11(FRAME_HDR_C);
	assign pref_en_w = (((((a_st_r == 4'd5) && echo_r) && !amap_uns_r) && !amap_edit_r) && ((bidx_r + 11'd1) >= sv2v_cast_11(FRAME_HDR_C))) && ((bidx_r + 11'd1) < (sv2v_cast_11(FRAME_HDR_C) + pld_r));
	assign rxs_rd_slot_o = cmd_r[56 + RXS_W_C:57];
	function automatic [RXA_W_C - 1:0] sv2v_cast_3BB6D;
		input reg [RXA_W_C - 1:0] inp;
		sv2v_cast_3BB6D = inp;
	endfunction
	assign rxs_rd_addr_o = (|{a_st_r == 4'd9, a_st_r == 4'd10, a_st_r == 4'd13} ? sv2v_cast_3BB6D(32'd24 + sv2v_cast_32(g_rd_pos_r)) : (a_st_r == 4'd5 ? sv2v_cast_3BB6D(32'd24 + sv2v_cast_32(pref_ix_w)) : sv2v_cast_3BB6D(32'd22 + sv2v_cast_32(walk_r))));
	assign rxs_rd_en_o = (((((a_st_r == 4'd1) && (walk_r < (pld_r + 11'd2))) || pref_en_w) || ((((a_st_r == 4'd9) && g_scan_started_r) && !g_rd_pending_r) && (g_rd_pos_r < g_total_r))) || (((a_st_r == 4'd10) && !g_rd_pending_r) && (g_rd_pos_r < g_total_r))) || (((a_st_r == 4'd13) && !g_rd_pending_r) && (g_data_ix_r < sv2v_cast_11(g_rec_len_r)));
	assign txn_ready_o = ((a_st_r == 4'd0) && !rsp_busy_w) && !amap_notify_busy_i;
	assign txs_alloc_req_o = a_st_r == 4'd4;
	assign txs_oversize_o = frame_len_r > sv2v_cast_11(TX_STD_BYTES_P);
	assign txs_wr_slot_o = tx_slot_r;
	function automatic [TXA_W_C - 1:0] sv2v_cast_FE6CB;
		input reg [TXA_W_C - 1:0] inp;
		sv2v_cast_FE6CB = inp;
	endfunction
	assign txs_wr_addr_o = sv2v_cast_FE6CB(bidx_r);
	assign txs_wr_valid_o = (a_st_r == 4'd5) && byte_ok_w;
	assign txs_wr_data_o = frame_byte_w;
	assign txs_wr_commit_o = a_st_r == 4'd6;
	assign txs_wr_len_o = sv2v_cast_FE6CB(frame_len_r);
	assign txreq_valid_o = (a_st_r == 4'd7) && !uns_r;
	assign txreq_uns_valid_o = (a_st_r == 4'd7) && uns_r;
	assign txreq_slot_o = tx_slot_r;
	localparam [2:0] pp_pkg_PP_SLOT_NULL_C = 3'd7;
	assign rxs_free_o = (a_st_r == 4'd8) && (cmd_r[59-:3] != pp_pkg_PP_SLOT_NULL_C);
	assign rxs_free_slot_o = cmd_r[56 + RXS_W_C:57];
	assign uns_done_o = (a_st_r == 4'd8) && uns_r;
	assign dbg_busy_o = (a_st_r != 4'd0) || ucpu_busy_w;
	assign dbg_cmd_cnt_o = cmd_cnt_r;
	assign dbg_resp_cnt_o = resp_cnt_r;
	assign dbg_drop_cnt_o = drop_cnt_r;
	assign dbg_status_o = status_r;
	assign dbg_len_o = frame_len_r;
	assign dbg_resp_err_o = rerr_cnt_r;
	wire [10:0] pad_len_w;
	assign pad_len_w = ((sv2v_cast_11(FRAME_HDR_C) + pld_r) < sv2v_cast_11(ETH_MIN_C) ? sv2v_cast_11(ETH_MIN_C) : sv2v_cast_11(FRAME_HDR_C) + pld_r);
	assign rsp_open_w = ((a_st_r == 4'd0) && !rsp_busy_w) && (((txn_valid_i && !drop_w) && !amap_notify_busy_i) || (uns_valid_i && (!txn_valid_i || amap_notify_busy_i)));
	assign rsp_seal_w = ((((a_st_r == 4'd3) && !gdi_r) && ucpu_done_w) && (sent_r || resp_send_w)) || (a_st_r == 4'd15);
	assign rsp_seal_len_w = ((echo_r || amap_edit_r) || gxf_fail_r ? 11'd0 : pld_r);
	wire rsp_fail_w;
	assign rsp_fail_w = ((rsp_err_w || gxf_fail_r) && !err_mode_r) && (!echo_r || amap_edit_r);
	localparam [4:0] ucpu_pkg_ST_ENTITY_MISBEHAVING_C = 5'd10;
	localparam [4:0] ucpu_pkg_ST_SUCCESS_C = 5'd0;
	function automatic [16:0] sv2v_cast_17;
		input reg [16:0] inp;
		sv2v_cast_17 = inp;
	endfunction
	always @(posedge clk_i) begin : command_machine
		if (!rst_n) begin
			a_st_r <= 4'd0;
			cmd_r <= 1'sb0;
			raw_ct_r <= 16'd0;
			cfg_ix_r <= 16'd0;
			desc_ty_r <= 16'd0;
			desc_ix_r <= 16'd0;
			name_ix_r <= 16'd0;
			name_cfg_r <= 16'd0;
			pld_cmd_r <= 11'd0;
			pld_r <= 11'd0;
			amap_rsp_count_r <= 8'd0;
			walk_r <= 11'd0;
			pid_lo_r <= 2'b00;
			echo_r <= 1'b0;
			ctrs_r <= 1'b0;
			amap_r <= 1'b0;
			amap_edit_r <= 1'b0;
			amap_remove_r <= 1'b0;
			amap_uns_r <= 1'b0;
			regun_r <= 1'b0;
			acq_r <= 1'b0;
			lockc_r <= 1'b0;
			gstri_r <= 1'b0;
			gavb_r <= 1'b0;
			gasp_r <= 1'b0;
			eavl_r <= 1'b0;
			gcfg_r <= 1'b0;
			gsfmt_r <= 1'b0;
			gsrate_r <= 1'b0;
			gclks_r <= 1'b0;
			ssrate_r <= 1'b0;
			sclks_r <= 1'b0;
			ssfmt_r <= 1'b0;
			ssinfo_r <= 1'b0;
			gctrl_r <= 1'b0;
			sctrl_r <= 1'b0;
			gname_r <= 1'b0;
			sname_r <= 1'b0;
			scfg_r <= 1'b0;
			strt_r <= 1'b0;
			stop_r <= 1'b0;
			strm_r <= 1'b0;
			setc_r <= 1'b0;
			gdi_r <= 1'b0;
			setval_r <= 64'd0;
			silat_r <= 32'd0;
			opd2_r <= 64'd0;
			lock_ent_ok_r <= 1'b0;
			uns_r <= 1'b0;
			upc_r <= 11'd0;
			status_r <= 5'd0;
			bidx_r <= 11'd0;
			frame_len_r <= 11'd0;
			err_mode_r <= 1'b0;
			tx_slot_r <= 1'sb0;
			disp_valid_r <= 1'b0;
			opd0_r <= 64'd0;
			opd1_r <= 64'd0;
			sent_r <= 1'b0;
			cmd_cnt_r <= 16'd0;
			resp_cnt_r <= 16'd0;
			drop_cnt_r <= 16'd0;
			rerr_cnt_r <= 16'd0;
			g_scan_started_r <= 1'b0;
			g_rd_pending_r <= 1'b0;
			g_load_data_r <= 1'b0;
			g_hdr_ix_r <= 3'd0;
			g_wr_phase_r <= 2'd0;
			g_total_r <= 11'd0;
			g_rd_pos_r <= 11'd0;
			g_data_ix_r <= 11'd0;
			g_data_start_r <= 11'd0;
			g_next_pos_r <= 11'd0;
			g_out_r <= 11'd12;
			g_rec_rlen_r <= 11'd0;
			g_sub_end_r <= 11'd0;
			g_scan_len_r <= 16'd0;
			g_scan_cmd_hi_r <= 8'd0;
			g_rec_len_r <= 16'd0;
			g_rec_cmd_r <= 16'd0;
			g_rec_cmd_status_r <= 8'd0;
			g_data_head_r <= 64'd0;
			g_rec_exec_r <= 1'b0;
			g_rec_status_r <= ucpu_pkg_ST_SUCCESS_C;
			g_shape_fault_r <= 1'b0;
		end
		else
			(* full_case, parallel_case *)
			case (a_st_r)
				4'd0:
					if ((txn_valid_i && !rsp_busy_w) && !amap_notify_busy_i) begin
						cmd_r <= txn_w;
						if (drop_w) begin
							if (drop_cnt_r != 16'hffff)
								drop_cnt_r <= drop_cnt_r + 16'd1;
							a_st_r <= 4'd8;
						end
						else begin
							if (cmd_cnt_r != 16'hffff)
								cmd_cnt_r <= cmd_cnt_r + 16'd1;
							upc_r <= upc_w;
							echo_r <= echo_w;
							ctrs_r <= ctrs_w;
							amap_r <= amap_w;
							amap_edit_r <= amap_edit_w;
							amap_remove_r <= amap_remove_w;
							amap_uns_r <= 1'b0;
							regun_r <= regun_w;
							acq_r <= acq_w;
							lockc_r <= lockc_w;
							gstri_r <= gstri_w;
							gavb_r <= gavb_w;
							gasp_r <= gasp_w;
							eavl_r <= eavl_w;
							gcfg_r <= gcfg_w;
							gsfmt_r <= gsfmt_w;
							gsrate_r <= gsrate_w;
							gclks_r <= gclks_w;
							ssrate_r <= ssrate_w;
							sclks_r <= sclks_w;
							ssfmt_r <= ssfmt_w;
							ssinfo_r <= ssinfo_w;
							gctrl_r <= gctrl_w;
							sctrl_r <= sctrl_w;
							gname_r <= gname_w;
							sname_r <= sname_w;
							scfg_r <= scfg_w;
							strt_r <= strt_w;
							stop_r <= stop_w;
							strm_r <= strm_w;
							setc_r <= setc_w;
							gdi_r <= gdi_w;
							setval_r <= 64'd0;
							silat_r <= 32'd0;
							lock_ent_ok_r <= 1'b1;
							uns_r <= 1'b0;
							err_mode_r <= 1'b0;
							pld_cmd_r <= (txn_w[59-:3] == pp_pkg_PP_SLOT_NULL_C ? 11'd0 : pld_cap_w);
							pld_r <= (txn_w[59-:3] == pp_pkg_PP_SLOT_NULL_C ? 11'd0 : pld_cap_w);
							amap_rsp_count_r <= 8'd0;
							cfg_ix_r <= 16'd0;
							desc_ty_r <= 16'd0;
							desc_ix_r <= 16'd0;
							name_ix_r <= 16'd0;
							name_cfg_r <= 16'd0;
							raw_ct_r <= (gdi_w ? txn_w[139-:16] : 16'd0);
							walk_r <= 11'd0;
							pid_lo_r <= 2'b00;
							sent_r <= 1'b0;
							g_scan_started_r <= 1'b0;
							g_rd_pending_r <= 1'b0;
							g_load_data_r <= 1'b0;
							g_hdr_ix_r <= 3'd0;
							g_wr_phase_r <= 2'd0;
							g_total_r <= 11'd0;
							g_rd_pos_r <= 11'd0;
							g_data_ix_r <= 11'd0;
							g_out_r <= 11'd12;
							g_rec_rlen_r <= 11'd0;
							g_sub_end_r <= 11'd0;
							g_rec_cmd_status_r <= 8'd0;
							g_shape_fault_r <= 1'b0;
							g_data_head_r <= 64'd0;
							a_st_r <= (gdi_w ? 4'd9 : (txn_w[59-:3] == pp_pkg_PP_SLOT_NULL_C ? 4'd2 : 4'd1));
						end
					end
					else if (uns_valid_i && !rsp_busy_w) begin
						cmd_r[392-:2] <= 2'd2;
						cmd_r[356-:3] <= 3'd2;
						cmd_r[353-:4] <= 4'd0;
						cmd_r[344-:11] <= 11'd12;
						cmd_r[333-:48] <= uns_mac_i;
						cmd_r[285-:64] <= uns_ctlr_eid_i;
						cmd_r[221-:64] <= entity_id_i;
						cmd_r[157-:16] <= uns_seq_i;
						cmd_r[139-:16] <= uns_ct_w;
						cmd_r[59-:3] <= pp_pkg_PP_SLOT_NULL_C;
						upc_r <= uns_upc_w;
						echo_r <= uns_kind_i == pp_pkg_PP_UNS_AMAP_C;
						ctrs_r <= uns_kind_i == pp_pkg_PP_UNS_CTRS_C;
						amap_r <= 1'b0;
						amap_edit_r <= 1'b0;
						amap_remove_r <= uns_amap_remove_i;
						amap_uns_r <= uns_kind_i == pp_pkg_PP_UNS_AMAP_C;
						regun_r <= uns_kind_i == pp_pkg_PP_UNS_LOCK_C;
						acq_r <= 1'b0;
						lockc_r <= 1'b0;
						gstri_r <= (uns_kind_i == pp_pkg_PP_UNS_STRI_C) || (uns_kind_i == pp_pkg_PP_UNS_SINFO_C);
						gavb_r <= uns_kind_i == pp_pkg_PP_UNS_AVB_C;
						gasp_r <= uns_kind_i == pp_pkg_PP_UNS_ASP_C;
						eavl_r <= 1'b0;
						gcfg_r <= 1'b0;
						gsfmt_r <= uns_kind_i == pp_pkg_PP_UNS_SFMT_C;
						gsrate_r <= uns_kind_i == pp_pkg_PP_UNS_SRATE_C;
						gclks_r <= uns_kind_i == pp_pkg_PP_UNS_CLKS_C;
						ssrate_r <= 1'b0;
						sclks_r <= 1'b0;
						ssfmt_r <= 1'b0;
						ssinfo_r <= 1'b0;
						gctrl_r <= uns_kind_i == pp_pkg_PP_UNS_CTRL_C;
						sctrl_r <= 1'b0;
						gname_r <= uns_kind_i == pp_pkg_PP_UNS_NAME_C;
						sname_r <= 1'b0;
						scfg_r <= uns_kind_i == pp_pkg_PP_UNS_CFG_C;
						strt_r <= (uns_kind_i == pp_pkg_PP_UNS_STRM_C) && !uns_arg0_i[0];
						stop_r <= (uns_kind_i == pp_pkg_PP_UNS_STRM_C) && uns_arg0_i[0];
						strm_r <= uns_kind_i == pp_pkg_PP_UNS_STRM_C;
						setc_r <= 1'b0;
						gdi_r <= 1'b0;
						g_shape_fault_r <= 1'b0;
						lock_ent_ok_r <= 1'b1;
						uns_r <= 1'b1;
						err_mode_r <= 1'b0;
						pld_cmd_r <= (uns_kind_i == pp_pkg_PP_UNS_AMAP_C ? 11'd8 + (sv2v_cast_11(uns_amap_count_i) << 3) : 11'd0);
						pld_r <= (uns_kind_i == pp_pkg_PP_UNS_AMAP_C ? 11'd8 + (sv2v_cast_11(uns_amap_count_i) << 3) : 11'd0);
						amap_rsp_count_r <= 8'd0;
						cfg_ix_r <= (uns_kind_i == pp_pkg_PP_UNS_ASP_C ? uns_desc_index_i : uns_desc_type_i);
						desc_ix_r <= (uns_kind_i == pp_pkg_PP_UNS_CFG_C ? uns_arg0_i : uns_desc_index_i);
						name_ix_r <= uns_arg0_i;
						name_cfg_r <= uns_arg1_i;
						desc_ty_r <= (uns_kind_i == pp_pkg_PP_UNS_AMAP_C ? uns_amap_count_i : 16'd0);
						raw_ct_r <= uns_ct_w;
						walk_r <= 11'd0;
						pid_lo_r <= 2'b00;
						sent_r <= 1'b0;
						a_st_r <= 4'd2;
					end
				4'd9:
					if (!g_scan_started_r) begin
						if (cmd_r[344-:11] > sv2v_cast_11(ucpu_pkg_RESP_CAP_C)) begin
							upc_r <= UPC_BADARG_C;
							echo_r <= 1'b1;
							gdi_r <= 1'b0;
							a_st_r <= 4'd2;
						end
						else begin
							g_scan_started_r <= 1'b1;
							g_total_r <= pld_trim_w;
							pld_r <= pld_trim_w;
							pld_cmd_r <= pld_trim_w;
							g_rd_pos_r <= 11'd0;
							g_hdr_ix_r <= 3'd0;
							g_rd_pending_r <= 1'b0;
						end
					end
					else if (!g_rd_pending_r) begin
						if (g_rd_pos_r >= g_total_r) begin
							if (g_hdr_ix_r != 3'd0) begin
								upc_r <= UPC_BADARG_C;
								echo_r <= 1'b1;
								gdi_r <= 1'b0;
								a_st_r <= 4'd2;
							end
							else if (g_total_r == 11'd0) begin
								pld_r <= 11'd0;
								status_r <= ucpu_pkg_ST_SUCCESS_C;
								a_st_r <= 4'd15;
							end
							else begin
								pld_r <= 11'd0;
								g_rd_pos_r <= 11'd0;
								g_hdr_ix_r <= 3'd0;
								g_load_data_r <= 1'b0;
								g_data_head_r <= 64'd0;
								a_st_r <= 4'd10;
							end
						end
						else if ((g_hdr_ix_r == 3'd0) && ((g_total_r - g_rd_pos_r) < 11'd8)) begin
							upc_r <= UPC_BADARG_C;
							echo_r <= 1'b1;
							gdi_r <= 1'b0;
							a_st_r <= 4'd2;
						end
						else
							g_rd_pending_r <= 1'b1;
					end
					else begin
						g_rd_pending_r <= 1'b0;
						(* full_case, parallel_case *)
						case (g_hdr_ix_r)
							3'd0: begin
								g_scan_len_r[15:8] <= rxs_rd_data_i;
								g_hdr_ix_r <= 3'd1;
								g_rd_pos_r <= g_rd_pos_r + 11'd1;
							end
							3'd1: begin
								g_scan_len_r[7:0] <= rxs_rd_data_i;
								g_hdr_ix_r <= 3'd2;
								g_rd_pos_r <= g_rd_pos_r + 11'd1;
							end
							3'd2, 3'd3, 3'd5: begin
								g_hdr_ix_r <= g_hdr_ix_r + 3'd1;
								g_rd_pos_r <= g_rd_pos_r + 11'd1;
							end
							3'd4: begin
								g_hdr_ix_r <= 3'd5;
								g_rd_pos_r <= g_rd_pos_r + 11'd1;
							end
							3'd6: begin
								g_scan_cmd_hi_r <= rxs_rd_data_i;
								g_hdr_ix_r <= 3'd7;
								g_rd_pos_r <= g_rd_pos_r + 11'd1;
							end
							default:
								if (!gdi_allowed({g_scan_cmd_hi_r, rxs_rd_data_i}) || (((sv2v_cast_17(g_rd_pos_r) + 17'd1) + sv2v_cast_17(g_scan_len_r)) > sv2v_cast_17(g_total_r))) begin
									upc_r <= UPC_BADARG_C;
									echo_r <= 1'b1;
									gdi_r <= 1'b0;
									a_st_r <= 4'd2;
								end
								else begin
									g_rd_pos_r <= (g_rd_pos_r + 11'd1) + sv2v_cast_11(g_scan_len_r);
									g_hdr_ix_r <= 3'd0;
								end
						endcase
					end
				4'd10:
					if (!g_rd_pending_r)
						g_rd_pending_r <= 1'b1;
					else begin
						g_rd_pending_r <= 1'b0;
						if (!g_load_data_r) begin
							(* full_case, parallel_case *)
							case (g_hdr_ix_r)
								3'd0: g_rec_len_r[15:8] <= rxs_rd_data_i;
								3'd1: g_rec_len_r[7:0] <= rxs_rd_data_i;
								3'd4: g_rec_cmd_status_r <= rxs_rd_data_i;
								3'd6: g_rec_cmd_r[15:8] <= rxs_rd_data_i;
								3'd7: begin
									g_rec_cmd_r[7:0] <= rxs_rd_data_i;
									g_data_start_r <= g_rd_pos_r + 11'd1;
									g_next_pos_r <= (g_rd_pos_r + 11'd1) + sv2v_cast_11(g_rec_len_r);
									g_data_ix_r <= 11'd0;
									g_data_head_r <= 64'd0;
									g_load_data_r <= g_rec_len_r != 16'd0;
									if (g_rec_len_r == 16'd0)
										a_st_r <= 4'd11;
								end
								default:
									;
							endcase
							g_rd_pos_r <= g_rd_pos_r + 11'd1;
							if (g_hdr_ix_r != 3'd7)
								g_hdr_ix_r <= g_hdr_ix_r + 3'd1;
						end
						else begin
							(* full_case, parallel_case *)
							case (g_data_ix_r[2:0])
								3'd0:
									if (g_data_ix_r < 11'd8)
										g_data_head_r[63:56] <= rxs_rd_data_i;
								3'd1:
									if (g_data_ix_r < 11'd8)
										g_data_head_r[55:48] <= rxs_rd_data_i;
								3'd2:
									if (g_data_ix_r < 11'd8)
										g_data_head_r[47:40] <= rxs_rd_data_i;
								3'd3:
									if (g_data_ix_r < 11'd8)
										g_data_head_r[39:32] <= rxs_rd_data_i;
								3'd4:
									if (g_data_ix_r < 11'd8)
										g_data_head_r[31:24] <= rxs_rd_data_i;
								3'd5:
									if (g_data_ix_r < 11'd8)
										g_data_head_r[23:16] <= rxs_rd_data_i;
								3'd6:
									if (g_data_ix_r < 11'd8)
										g_data_head_r[15:8] <= rxs_rd_data_i;
								default:
									if (g_data_ix_r < 11'd8)
										g_data_head_r[7:0] <= rxs_rd_data_i;
							endcase
							g_rd_pos_r <= g_rd_pos_r + 11'd1;
							g_data_ix_r <= g_data_ix_r + 11'd1;
							if ((g_data_ix_r + 11'd1) >= sv2v_cast_11(g_rec_len_r)) begin
								g_load_data_r <= 1'b0;
								a_st_r <= 4'd11;
							end
						end
					end
				4'd11:
					if (((g_out_r + 11'd8) + g_sub_rlen_w) > sv2v_cast_11(ucpu_pkg_RESP_CAP_C)) begin
						g_rd_pos_r <= g_next_pos_r;
						g_hdr_ix_r <= 3'd0;
						g_load_data_r <= 1'b0;
						g_data_head_r <= 64'd0;
						g_rd_pending_r <= 1'b0;
						a_st_r <= (g_next_pos_r >= g_total_r ? 4'd15 : 4'd10);
					end
					else begin
						g_rec_exec_r <= g_sub_exec_w;
						g_rec_rlen_r <= g_sub_rlen_w;
						g_rec_status_r <= g_sub_status_w;
						g_wr_phase_r <= 2'd0;
						upc_r <= g_sub_upc_w;
						cfg_ix_r <= g_data_head_r[63:48];
						desc_ix_r <= g_data_head_r[47:32];
						desc_ty_r <= 16'd0;
						name_ix_r <= g_data_head_r[31:16];
						name_cfg_r <= g_data_head_r[15:0];
						ctrs_r <= g_sub_exec_w && (g_rec_cmd_r == OP_GET_COUNTERS_C);
						amap_r <= 1'b0;
						regun_r <= 1'b0;
						acq_r <= 1'b0;
						lockc_r <= 1'b0;
						gstri_r <= g_sub_exec_w && (g_rec_cmd_r == OP_GET_STREAM_INFO_C);
						gavb_r <= 1'b0;
						gasp_r <= 1'b0;
						eavl_r <= 1'b0;
						gcfg_r <= g_sub_exec_w && (g_rec_cmd_r == OP_GET_CONFIG_C);
						gsfmt_r <= g_sub_exec_w && (g_rec_cmd_r == OP_GET_STREAM_FMT_C);
						gsrate_r <= g_sub_exec_w && (g_rec_cmd_r == OP_GET_SAMP_RATE_C);
						gclks_r <= g_sub_exec_w && (g_rec_cmd_r == OP_GET_CLOCK_SRC_C);
						ssrate_r <= 1'b0;
						sclks_r <= 1'b0;
						ssfmt_r <= 1'b0;
						ssinfo_r <= 1'b0;
						gctrl_r <= 1'b0;
						sctrl_r <= 1'b0;
						gname_r <= g_sub_exec_w && (g_rec_cmd_r == OP_GET_NAME_C);
						sname_r <= 1'b0;
						scfg_r <= 1'b0;
						setc_r <= 1'b0;
						echo_r <= 1'b0;
						a_st_r <= 4'd12;
					end
				4'd12:
					if (rb_ready_w) begin
						if (g_wr_phase_r == 2'd0)
							g_wr_phase_r <= 2'd1;
						else begin
							g_wr_phase_r <= 2'd0;
							if (g_rec_exec_r)
								a_st_r <= 4'd2;
							else if (g_rec_len_r != 16'd0) begin
								g_rd_pos_r <= g_data_start_r;
								g_data_ix_r <= 11'd0;
								g_rd_pending_r <= 1'b0;
								a_st_r <= 4'd13;
							end
							else begin
								g_out_r <= (g_out_r + 11'd8) + g_rec_rlen_r;
								pld_r <= (g_out_r + g_rec_rlen_r) - 11'd4;
								g_rd_pos_r <= g_next_pos_r;
								g_hdr_ix_r <= 3'd0;
								g_data_head_r <= 64'd0;
								a_st_r <= (g_next_pos_r >= g_total_r ? 4'd15 : 4'd10);
							end
						end
					end
				4'd13:
					if (!g_rd_pending_r)
						g_rd_pending_r <= 1'b1;
					else if (rb_ready_w) begin
						g_rd_pending_r <= 1'b0;
						g_rd_pos_r <= g_rd_pos_r + 11'd1;
						g_data_ix_r <= g_data_ix_r + 11'd1;
						if ((g_data_ix_r + 11'd1) >= sv2v_cast_11(g_rec_len_r)) begin
							g_out_r <= (g_out_r + 11'd8) + g_rec_rlen_r;
							pld_r <= (g_out_r + g_rec_rlen_r) - 11'd4;
							g_rd_pos_r <= g_next_pos_r;
							g_hdr_ix_r <= 3'd0;
							g_data_head_r <= 64'd0;
							a_st_r <= (g_next_pos_r >= g_total_r ? 4'd15 : 4'd10);
						end
					end
				4'd14:
					if (rb_ready_w) begin
						g_out_r <= g_sub_end_r;
						pld_r <= g_sub_end_r - 11'd12;
						g_rd_pos_r <= g_next_pos_r;
						g_hdr_ix_r <= 3'd0;
						g_data_head_r <= 64'd0;
						g_rd_pending_r <= 1'b0;
						a_st_r <= (g_next_pos_r >= g_total_r ? 4'd15 : 4'd10);
					end
				4'd15: begin
					status_r <= (g_shape_fault_r ? ucpu_pkg_ST_ENTITY_MISBEHAVING_C : ucpu_pkg_ST_SUCCESS_C);
					echo_r <= 1'b0;
					sent_r <= 1'b1;
					bidx_r <= 11'd0;
					frame_len_r <= pad_len_w;
					a_st_r <= 4'd4;
				end
				4'd1: begin
					if (walk_r == 11'd0) begin
						pld_r <= pld_trim_w;
						pld_cmd_r <= pld_trim_w;
					end
					if (walk_r < (pld_r + 11'd2))
						walk_r <= walk_r + 11'd1;
					else begin
						if (mvu_get_milan_info_w) begin
							upc_r <= UPC_MVUINFO_C;
							echo_r <= 1'b0;
						end
						if (((((cmd_r[356-:3] == 3'd2) && (cmd_r[353-:4] == 4'd0)) && (cmd_r[139-:16] == OP_READ_DESCRIPTOR_C)) && (cmd_r[344-:11] >= 11'd20)) && (desc_ty_r == DT_ENTITY_C)) begin
							upc_r <= UPC_RDESCENT_C;
							echo_r <= 1'b0;
						end
						if (amap_r && (cfg_ix_r == DT_STREAM_PORT_OUT_C))
							upc_r <= UPC_GAMAPO_C;
						else if (amap_r && (cfg_ix_r != DT_STREAM_PORT_IN_C)) begin
							upc_r <= UPC_NOTIMPL_C;
							echo_r <= 1'b1;
						end
						if (amap_edit_r) begin
							amap_rsp_count_r <= amap_rx_count_w;
							if (((({8'd0, cmd_r[344-:11]} != (19'd20 + ({3'd0, desc_ty_r} << 3))) || (cmd_r[344-:11] < 11'd20)) || (cmd_r[344-:11] > 11'd524)) || (pld_cmd_r != (cmd_r[344-:11] - 11'd12))) begin
								upc_r <= UPC_BADARG_C;
								echo_r <= 1'b1;
							end
							else if ((cfg_ix_r != DT_STREAM_PORT_IN_C) && (cfg_ix_r != DT_STREAM_PORT_OUT_C)) begin
								upc_r <= UPC_NSUPPE_C;
								echo_r <= 1'b1;
							end
							else begin
								upc_r <= (amap_remove_r ? UPC_AMREMOVE_C : UPC_AMADD_C);
								echo_r <= 1'b1;
							end
						end
						if (regun_r)
							upc_r <= (cmd_r[124] ? UPC_DEREG_C : UPC_REGUN_C);
						if (acq_r)
							upc_r <= UPC_NSUPPE_C;
						if (lockc_r) begin
							if (cmd_r[344-:11] < 11'd28)
								upc_r <= UPC_BADARG_C;
							else if (!lock_ent_ok_r)
								upc_r <= UPC_NSUPPE_C;
							else begin
								upc_r <= UPC_LOCKEN_C;
								echo_r <= 1'b0;
							end
						end
						if ((((ctrs_r && (cfg_ix_r != DT_STREAM_INPUT_C)) && (cfg_ix_r != DT_STREAM_OUTPUT_C)) && (cfg_ix_r != DT_AVB_INTERFACE_C)) && (cfg_ix_r != DT_CLOCK_DOMAIN_C)) begin
							upc_r <= UPC_GCTRSNS_C;
							echo_r <= 1'b0;
						end
						if (gstri_r) begin
							if (cmd_r[344-:11] < 11'd16)
								upc_r <= UPC_BADARG_C;
							else if ((cfg_ix_r != DT_STREAM_INPUT_C) && (cfg_ix_r != DT_STREAM_OUTPUT_C))
								upc_r <= UPC_NSUPPE_C;
							else begin
								upc_r <= UPC_GSTRI_C;
								echo_r <= 1'b0;
							end
						end
						if (gavb_r) begin
							if (cmd_r[344-:11] < 11'd16)
								upc_r <= UPC_BADARG_C;
							else if (cfg_ix_r != DT_AVB_INTERFACE_C)
								upc_r <= UPC_NSUPPE_C;
							else begin
								upc_r <= UPC_GAVB_C;
								echo_r <= 1'b0;
							end
						end
						if (gasp_r) begin
							if (cmd_r[344-:11] < 11'd16)
								upc_r <= UPC_BADARG_C;
							else begin
								upc_r <= UPC_GASP_C;
								echo_r <= 1'b0;
							end
						end
						if (eavl_r) begin
							upc_r <= UPC_EAVL_C;
							echo_r <= 1'b0;
						end
						if (gcfg_r) begin
							upc_r <= UPC_GCFG_C;
							echo_r <= 1'b0;
						end
						if (gsfmt_r) begin
							if (cmd_r[344-:11] < 11'd16)
								upc_r <= UPC_BADARG_C;
							else if ((cfg_ix_r != DT_STREAM_INPUT_C) && (cfg_ix_r != DT_STREAM_OUTPUT_C)) begin
								upc_r <= UPC_TIZ8NS_C;
								echo_r <= 1'b0;
							end
							else begin
								upc_r <= UPC_GSFMT_C;
								echo_r <= 1'b0;
							end
						end
						if (gsrate_r) begin
							if (cmd_r[344-:11] < 11'd16)
								upc_r <= UPC_BADARG_C;
							else if (cfg_ix_r != DT_AUDIO_UNIT_C) begin
								upc_r <= UPC_TIZ4NS_C;
								echo_r <= 1'b0;
							end
							else begin
								upc_r <= UPC_GSRATE_C;
								echo_r <= 1'b0;
							end
						end
						if (gclks_r) begin
							if (cmd_r[344-:11] < 11'd16)
								upc_r <= UPC_BADARG_C;
							else if (cfg_ix_r != DT_CLOCK_DOMAIN_C) begin
								upc_r <= UPC_TIZ4NS_C;
								echo_r <= 1'b0;
							end
							else begin
								upc_r <= UPC_GCLKS_C;
								echo_r <= 1'b0;
							end
						end
						if (gname_r) begin
							upc_r <= ((cmd_r[344-:11] < 11'd20) || (pld_cmd_r < 11'd8) ? UPC_NAMEBAD_C : UPC_GNAME_C);
							echo_r <= 1'b0;
						end
						if (sname_r) begin
							upc_r <= ((cmd_r[344-:11] != 11'd84) || (pld_cmd_r != 11'd72) ? UPC_NAMEBAD_C : UPC_SNAME_C);
							echo_r <= 1'b0;
						end
						if (ssrate_r) begin
							if (cmd_r[344-:11] < 11'd20)
								upc_r <= UPC_BADARG4_C;
							else if (cfg_ix_r != DT_AUDIO_UNIT_C)
								upc_r <= UPC_TIZ4NS_C;
							else
								upc_r <= UPC_SSRATE_C;
							echo_r <= 1'b0;
						end
						if (sclks_r) begin
							if (cmd_r[344-:11] < 11'd20)
								upc_r <= UPC_BADARG4_C;
							else if (cfg_ix_r != DT_CLOCK_DOMAIN_C)
								upc_r <= UPC_TIZ4NS_C;
							else
								upc_r <= UPC_SCLKS_C;
							echo_r <= 1'b0;
						end
						if (gctrl_r) begin
							if (cmd_r[344-:11] < 11'd16)
								upc_r <= UPC_BADARG1_C;
							else if (cfg_ix_r != DT_CONTROL_C)
								upc_r <= UPC_NSUPP1_C;
							else
								upc_r <= UPC_GCTRL_C;
							echo_r <= 1'b0;
						end
						if (sctrl_r) begin
							if (cmd_r[344-:11] < 11'd17)
								upc_r <= UPC_BADARG1_C;
							else if (cfg_ix_r != DT_CONTROL_C)
								upc_r <= UPC_NSUPP1_C;
							else
								upc_r <= UPC_SCTRL_C;
							echo_r <= 1'b0;
						end
						if (scfg_r) begin
							if (cmd_r[344-:11] < 11'd16)
								upc_r <= UPC_SCFGBAD_C;
							else if (any_running_w)
								upc_r <= UPC_SCFGRUN_C;
							else
								upc_r <= UPC_SCFG_C;
							echo_r <= 1'b0;
						end
						if (strm_r) begin
							if (cmd_r[344-:11] < 11'd16)
								upc_r <= UPC_STRMBAD_C;
							else if (cfg_ix_r != DT_STREAM_INPUT_C)
								upc_r <= UPC_STRMNS_C;
							else if (strt_r)
								upc_r <= UPC_STRT_C;
							else
								upc_r <= UPC_STOP_C;
							echo_r <= 1'b0;
						end
						if (ssfmt_r) begin
							if ((cmd_r[344-:11] < 11'd24) || (pld_cmd_r < 11'd12))
								upc_r <= UPC_SFBAD_C;
							else if ((cfg_ix_r != DT_STREAM_INPUT_C) && (cfg_ix_r != DT_STREAM_OUTPUT_C))
								upc_r <= UPC_TIZ8NS_C;
							else if (run_this_w)
								upc_r <= UPC_SFRUN_C;
							else if (cfg_ix_r == DT_STREAM_INPUT_C)
								upc_r <= UPC_SFMTI_C;
							else
								upc_r <= UPC_SFMTO_C;
							echo_r <= 1'b0;
						end
						if (ssinfo_r) begin
							if ((cmd_r[344-:11] < 11'd96) || (pld_cmd_r < 11'd84)) begin
								upc_r <= UPC_SIBAD_C;
								echo_r <= 1'b0;
							end
							else if (cfg_ix_r != DT_STREAM_OUTPUT_C)
								upc_r <= UPC_NSUPPE_C;
							else if (run_this_w)
								upc_r <= UPC_SIRUN_C;
							else if (setval_r[63:32] != SIF_ACC_LAT_C)
								upc_r <= UPC_NSUPPE_C;
							else if (silat_r[31])
								upc_r <= UPC_BADARG_C;
							else
								upc_r <= UPC_SINFO_C;
						end
						a_st_r <= 4'd2;
					end
					if (walk_r != 11'd0)
						(* full_case, parallel_case *)
						case (walk_r - 11'd1)
							11'd0: raw_ct_r[15:8] <= rxs_rd_data_i;
							11'd1: raw_ct_r[7:0] <= rxs_rd_data_i;
							11'd2: cfg_ix_r[15:8] <= rxs_rd_data_i;
							11'd3: cfg_ix_r[7:0] <= rxs_rd_data_i;
							11'd4: begin
								pid_lo_r[1] <= rxs_rd_data_i == MVU_PID_L1_C;
								if (ix26_w)
									desc_ix_r[15:8] <= rxs_rd_data_i;
							end
							11'd5: begin
								pid_lo_r[0] <= rxs_rd_data_i == MVU_PID_L0_C;
								if (ix26_w)
									desc_ix_r[7:0] <= rxs_rd_data_i;
							end
							11'd6: begin
								if (!ctrs_r)
									desc_ty_r[15:8] <= rxs_rd_data_i;
								if (gname_r || sname_r)
									name_ix_r[15:8] <= rxs_rd_data_i;
								if (setc_r)
									setval_r[63:56] <= rxs_rd_data_i;
							end
							11'd7: begin
								if (!ctrs_r)
									desc_ty_r[7:0] <= rxs_rd_data_i;
								if (gname_r || sname_r)
									name_ix_r[7:0] <= rxs_rd_data_i;
								if (setc_r)
									setval_r[55:48] <= rxs_rd_data_i;
							end
							11'd8: begin
								if (!ix26_w && !gasp_r)
									desc_ix_r[15:8] <= rxs_rd_data_i;
								if (gname_r || sname_r)
									name_cfg_r[15:8] <= rxs_rd_data_i;
								if (setc_r)
									setval_r[47:40] <= rxs_rd_data_i;
							end
							11'd9: begin
								if (!ix26_w && !gasp_r)
									desc_ix_r[7:0] <= rxs_rd_data_i;
								if (gname_r || sname_r)
									name_cfg_r[7:0] <= rxs_rd_data_i;
								if (setc_r)
									setval_r[39:32] <= rxs_rd_data_i;
							end
							11'd10:
								if (setc_r)
									setval_r[31:24] <= rxs_rd_data_i;
							11'd11:
								if (setc_r)
									setval_r[23:16] <= rxs_rd_data_i;
							11'd12:
								if (setc_r)
									setval_r[15:8] <= rxs_rd_data_i;
							11'd13:
								if (setc_r)
									setval_r[7:0] <= rxs_rd_data_i;
							11'd14, 11'd15, 11'd16, 11'd17:
								if (lockc_r && (rxs_rd_data_i != 8'd0))
									lock_ent_ok_r <= 1'b0;
							11'd26:
								if (ssinfo_r)
									silat_r[31:24] <= rxs_rd_data_i;
							11'd27:
								if (ssinfo_r)
									silat_r[23:16] <= rxs_rd_data_i;
							11'd28:
								if (ssinfo_r)
									silat_r[15:8] <= rxs_rd_data_i;
							11'd29:
								if (ssinfo_r)
									silat_r[7:0] <= rxs_rd_data_i;
							default:
								;
						endcase
				end
				4'd2: begin
					if (!disp_valid_r) begin
						opd0_r <= opd0_w;
						opd1_r <= opd1_w;
						opd2_r <= opd2_w;
					end
					disp_valid_r <= 1'b1;
					if (disp_valid_r && disp_ready_w) begin
						disp_valid_r <= 1'b0;
						a_st_r <= 4'd3;
					end
				end
				4'd3: begin
					if (resp_send_w) begin
						if (gdi_r) begin
							g_rec_status_r <= resp_status_w;
							g_sub_end_r <= resp_len_w;
						end
						else begin
							sent_r <= 1'b1;
							status_r <= resp_status_w;
							if (amap_edit_r)
								pld_r <= amap_edit_pld_w;
							else if (!echo_r)
								pld_r <= (resp_len_w > 11'd12 ? ((resp_len_w - 11'd12) > sv2v_cast_11(PLD_MAX_C) ? sv2v_cast_11(PLD_MAX_C) : resp_len_w - 11'd12) : 11'd0);
							else
								pld_r <= pld_cmd_r;
						end
					end
					if (ucpu_done_w) begin
						if (gdi_r) begin
							if ((resp_send_w ? resp_len_w : g_sub_end_r) != ((g_out_r + 11'd8) + g_rec_rlen_r)) begin
								g_shape_fault_r <= 1'b1;
								pld_r <= 11'd0;
								echo_r <= 1'b0;
								a_st_r <= 4'd15;
							end
							else
								a_st_r <= 4'd14;
						end
						else begin
							bidx_r <= 11'd0;
							frame_len_r <= pad_len_w;
							a_st_r <= (sent_r || resp_send_w ? 4'd4 : 4'd8);
							if (!(sent_r || resp_send_w) && (drop_cnt_r != 16'hffff))
								drop_cnt_r <= drop_cnt_r + 16'd1;
						end
					end
				end
				4'd4:
					if (rsp_fail_w) begin
						err_mode_r <= 1'b1;
						status_r <= ucpu_pkg_ST_ENTITY_MISBEHAVING_C;
						pld_r <= (amap_edit_r ? amap_edit_pld_w : 11'd0);
						frame_len_r <= (amap_edit_r ? ((sv2v_cast_11(FRAME_HDR_C) + amap_edit_pld_w) < sv2v_cast_11(ETH_MIN_C) ? sv2v_cast_11(ETH_MIN_C) : sv2v_cast_11(FRAME_HDR_C) + amap_edit_pld_w) : sv2v_cast_11(ETH_MIN_C));
						bidx_r <= 11'd0;
						if (rerr_cnt_r != 16'hffff)
							rerr_cnt_r <= rerr_cnt_r + 16'd1;
					end
					else if (txs_alloc_gnt_i) begin
						tx_slot_r <= txs_alloc_slot_i;
						a_st_r <= 4'd5;
					end
				4'd5:
					if (rsp_fail_w) begin
						err_mode_r <= 1'b1;
						status_r <= ucpu_pkg_ST_ENTITY_MISBEHAVING_C;
						pld_r <= (amap_edit_r ? amap_edit_pld_w : 11'd0);
						frame_len_r <= (amap_edit_r ? ((sv2v_cast_11(FRAME_HDR_C) + amap_edit_pld_w) < sv2v_cast_11(ETH_MIN_C) ? sv2v_cast_11(ETH_MIN_C) : sv2v_cast_11(FRAME_HDR_C) + amap_edit_pld_w) : sv2v_cast_11(ETH_MIN_C));
						bidx_r <= 11'd0;
						if (rerr_cnt_r != 16'hffff)
							rerr_cnt_r <= rerr_cnt_r + 16'd1;
					end
					else if (byte_ok_w) begin
						if ((bidx_r + 11'd1) >= frame_len_r)
							a_st_r <= 4'd6;
						bidx_r <= bidx_r + 11'd1;
					end
				4'd6: begin
					if (resp_cnt_r != 16'hffff)
						resp_cnt_r <= resp_cnt_r + 16'd1;
					a_st_r <= 4'd7;
				end
				4'd7:
					if ((uns_r ? txreq_uns_ready_i : txreq_ready_i))
						a_st_r <= 4'd8;
				4'd8: a_st_r <= 4'd0;
				default: a_st_r <= 4'd0;
			endcase
	end
	initial _sv2v_0 = 0;
endmodule
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
	always @(*) begin : command_registry_hit
		if (_sv2v_0)
			;
		rx_cmd_hit_w = 1'sb0;
		begin : sv2v_autoblock_2
			reg [31:0] i;
			for (i = 0; i < N_CTRL_P; i = i + 1)
				rx_cmd_hit_w[i] = ((rx_cmd_valid_i && valid_r[i]) && (rows_r[i][127:64] == rx_cmd_eid_i)) && (rows_r[i][63:16] == rx_cmd_mac_i);
		end
	end
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
			begin : sv2v_autoblock_3
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
			begin : sv2v_autoblock_4
				reg [31:0] s;
				for (s = 0; s < N_STREAM_IN_P; s = s + 1)
					if (!pick_any_w && pe_sin_r[s]) begin
						pick_any_w = 1'b1;
						pick_kind_w = pp_pkg_PP_UNS_STRI_C;
						pick_dt_w = 16'h0005;
						pick_di_w = sv2v_cast_16(s);
					end
			end
			begin : sv2v_autoblock_5
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
	reg pd_any_w;
	always @(*) begin : pend_pick
		if (_sv2v_0)
			;
		pd_any_w = 1'b0;
		pd_ix_w = 1'sb0;
		begin : sv2v_autoblock_6
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
	assign uns_valid_o = n_st_r == 4'd6;
	assign uns_kind_o = em_kind_r;
	assign uns_desc_type_o = em_dt_r;
	assign uns_desc_index_o = em_di_r;
	assign uns_ctlr_eid_o = hold_eid_r;
	assign uns_mac_o = hold_mac_r;
	assign uns_seq_o = hold_seq_r;
	assign uns_amap_remove_o = em_amap_remove_r;
	assign uns_amap_count_o = em_amap_count_r;
	assign uns_arg0_o = em_arg0_r;
	assign uns_arg1_o = em_arg1_r;
	assign amap_busy_o = ((((((((dh_v_r || em_active_r) || pe_lock_r) || pe_amap_r) || pe_avb_r) || pe_asp_r) || |pe_sin_r) || |pe_sout_r) || (cmdq_count_r != 5'd0)) || |ctr_pend_r;
	assign prng_draw_kind_o = 3'd4;
	assign dbg_uns_cnt_o = uns_cnt_r;
	assign dbg_coalesce_o = coalesce_r;
	always @(*) begin : reg_count
		if (_sv2v_0)
			;
		dbg_reg_cnt_o = 8'd0;
		begin : sv2v_autoblock_7
			reg [31:0] i;
			for (i = 0; i < N_CTRL_P; i = i + 1)
				dbg_reg_cnt_o = dbg_reg_cnt_o + {7'd0, valid_r[i]};
		end
	end
	function automatic [CIX_W_C - 1:0] sv2v_cast_17814;
		input reg [CIX_W_C - 1:0] inp;
		sv2v_cast_17814 = inp;
	endfunction
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
			begin : sv2v_autoblock_8
				reg [31:0] c;
				for (c = 0; c < N_CTR_DESC_C; c = c + 1)
					ctr_last_r[c] <= 32'd0;
			end
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
			uns_cnt_r <= 16'd0;
			coalesce_r <= 8'd0;
			wr_en_r <= 1'b0;
			wr_ix_r <= 1'sb0;
			wr_row_r <= 1'sb0;
			tmr_arm_valid_o <= 1'b0;
			tmr_arm_cancel_o <= 1'b0;
			tmr_arm_slot_o <= 1'sb0;
			tmr_arm_owner_o <= 1'sb0;
			tmr_arm_deadline_ms_o <= 32'd0;
		end
		else begin
			wr_en_r <= 1'b0;
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
						if (dh_v_r) begin
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
				4'd6:
					if (uns_done_i)
						n_st_r <= 4'd7;
					else if (rgy_new_w)
						n_st_r <= 4'd0;
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
`default_nettype none
module KL_aecp_resp_buf (
	clk_i,
	rst_n,
	open_i,
	seal_i,
	seal_len_i,
	wr_we_i,
	wr_addr_i,
	wr_wdata_i,
	wr_wstrb_i,
	wr_ready_o,
	rd_valid_o,
	rd_data_o,
	rd_take_i,
	mem_req_valid_o,
	mem_req_ready_i,
	mem_req_addr_o,
	mem_req_beats_o,
	mem_rsp_valid_i,
	mem_rsp_ready_o,
	mem_rsp_data_i,
	mem_rsp_last_i,
	mem_rsp_err_i,
	mem_wr_valid_o,
	mem_wr_ready_i,
	mem_wr_addr_o,
	mem_wr_data_o,
	mem_wr_strb_o,
	mem_wr_done_i,
	mem_wr_err_i,
	busy_o,
	err_o,
	dbg_fault_o,
	dbg_lane_wr_o,
	dbg_burst_o,
	dbg_drop_o
);
	reg _sv2v_0;
	parameter [31:0] RESP_BASE_P = 32'h20100000;
	parameter [31:0] RESP_BYTES_P = 592;
	parameter [31:0] MEM_TIMEOUT_CYC_P = 4096;
	localparam [31:0] LANES_C = (RESP_BYTES_P + 7) / 8;
	localparam [31:0] LANE_W_C = $clog2(LANES_C);
	localparam [31:0] TMO_W_C = $clog2(MEM_TIMEOUT_CYC_P + 1);
	input wire clk_i;
	input wire rst_n;
	input wire open_i;
	input wire seal_i;
	input wire [10:0] seal_len_i;
	input wire wr_we_i;
	input wire [9:0] wr_addr_i;
	input wire [31:0] wr_wdata_i;
	input wire [3:0] wr_wstrb_i;
	output wire wr_ready_o;
	output wire rd_valid_o;
	output reg [7:0] rd_data_o;
	input wire rd_take_i;
	output wire mem_req_valid_o;
	input wire mem_req_ready_i;
	output wire [31:0] mem_req_addr_o;
	output wire [8:0] mem_req_beats_o;
	input wire mem_rsp_valid_i;
	output wire mem_rsp_ready_o;
	input wire [63:0] mem_rsp_data_i;
	input wire mem_rsp_last_i;
	input wire mem_rsp_err_i;
	output wire mem_wr_valid_o;
	input wire mem_wr_ready_i;
	output wire [31:0] mem_wr_addr_o;
	output wire [63:0] mem_wr_data_o;
	output wire [7:0] mem_wr_strb_o;
	input wire mem_wr_done_i;
	input wire mem_wr_err_i;
	output wire busy_o;
	output wire err_o;
	output wire [2:0] dbg_fault_o;
	output wire [15:0] dbg_lane_wr_o;
	output wire [15:0] dbg_burst_o;
	output wire [15:0] dbg_drop_o;
	localparam [2:0] FAULT_NONE_C = 3'd0;
	localparam [2:0] FAULT_WTMO_C = 3'd1;
	localparam [2:0] FAULT_WERR_C = 3'd2;
	localparam [2:0] FAULT_RTMO_C = 3'd3;
	localparam [2:0] FAULT_RERR_C = 3'd4;
	localparam [9:0] HDR_BYTES_C = 10'd12;
	localparam [2:0] FIRST_OFF_C = 3'd4;
	generate
		if (RESP_BASE_P[2:0] != 3'd0) begin : gen_g_base_align
			initial $display("Error [elaboration] $VALIDATION_STORAGE/reviews/r247-520-r1/protocol-processor/hdl/aecp/KL_aecp_resp_buf.sv:194:5 - KL_aecp_resp_buf.gen_g_base_align\n msg: ", "RESP_BASE_P=%08h must be 8-byte aligned", RESP_BASE_P);
		end
		if (RESP_BYTES_P <= 16) begin : gen_g_size
			initial $display("Error [elaboration] $VALIDATION_STORAGE/reviews/r247-520-r1/protocol-processor/hdl/aecp/KL_aecp_resp_buf.sv:197:5 - KL_aecp_resp_buf.gen_g_size\n msg: ", "RESP_BYTES_P=%0d leaves no payload above the header record", RESP_BYTES_P);
		end
		if (LANES_C > 511) begin : gen_g_beats
			initial $display("Error [elaboration] $VALIDATION_STORAGE/reviews/r247-520-r1/protocol-processor/hdl/aecp/KL_aecp_resp_buf.sv:201:5 - KL_aecp_resp_buf.gen_g_beats\n msg: ", "a read burst of %0d beats exceeds the 9-bit mem_req_beats_o field", LANES_C);
		end
	endgenerate
	reg [63:0] lane_d_r;
	reg [7:0] lane_s_r;
	reg [LANE_W_C - 1:0] lane_ix_r;
	reg lane_open_r;
	reg [2:0] st_r;
	reg seal_pend_r;
	reg [10:0] len_r;
	reg [10:0] served_r;
	reg [63:0] rlane_r;
	reg rvalid_r;
	reg [2:0] roff_r;
	reg fault_r;
	reg [2:0] fcode_r;
	reg [15:0] lanewr_r;
	reg [15:0] burst_r;
	reg [15:0] drop_r;
	reg sk_valid_r;
	reg [9:0] sk_addr_r;
	reg [31:0] sk_data_r;
	reg [3:0] sk_strb_r;
	reg [1:0] bix_r;
	reg wr_ready_r;
	reg wreq_r;
	reg wbusy_r;
	reg rreq_r;
	reg rbusy_r;
	reg [TMO_W_C - 1:0] tmo_r;
	wire beat_w;
	wire tmo_hit_w;
	wire wait_w;
	assign beat_w = (mem_rsp_valid_i && mem_rsp_ready_o) && rbusy_r;
	function automatic [TMO_W_C - 1:0] sv2v_cast_BA630;
		input reg [TMO_W_C - 1:0] inp;
		sv2v_cast_BA630 = inp;
	endfunction
	assign tmo_hit_w = tmo_r == sv2v_cast_BA630(MEM_TIMEOUT_CYC_P);
	assign wait_w = (((wreq_r && !mem_wr_ready_i) || (wbusy_r && !mem_wr_done_i)) || (rreq_r && !mem_req_ready_i)) || ((rbusy_r && mem_rsp_ready_o) && !mem_rsp_valid_i);
	assign wr_ready_o = wr_ready_r;
	wire accept_w;
	assign accept_w = wr_we_i && wr_ready_r;
	reg [2:0] m_w;
	always @(*) begin : strobe_width
		if (_sv2v_0)
			;
		if (sk_strb_r[3])
			m_w = 3'd4;
		else if (sk_strb_r[1])
			m_w = 3'd2;
		else if (sk_strb_r[0])
			m_w = 3'd1;
		else
			m_w = 3'd0;
	end
	wire [10:0] babs_w;
	assign babs_w = {1'b0, sk_addr_r} + {9'd0, bix_r};
	reg [7:0] bval_w;
	always @(*) begin : byte_value
		if (_sv2v_0)
			;
		(* full_case, parallel_case *)
		case (m_w)
			3'd1: bval_w = sk_data_r[7:0];
			3'd2: bval_w = (bix_r == 2'd0 ? sk_data_r[15:8] : sk_data_r[7:0]);
			default:
				(* full_case, parallel_case *)
				case (bix_r)
					2'd0: bval_w = sk_data_r[31:24];
					2'd1: bval_w = sk_data_r[23:16];
					2'd2: bval_w = sk_data_r[15:8];
					default: bval_w = sk_data_r[7:0];
				endcase
		endcase
	end
	wire keep_w;
	function automatic [10:0] sv2v_cast_11;
		input reg [10:0] inp;
		sv2v_cast_11 = inp;
	endfunction
	assign keep_w = (babs_w >= {1'b0, HDR_BYTES_C}) && (babs_w < sv2v_cast_11(RESP_BYTES_P));
	wire [LANE_W_C - 1:0] tgt_lane_w;
	wire [2:0] tgt_off_w;
	function automatic [LANE_W_C - 1:0] sv2v_cast_BE6CF;
		input reg [LANE_W_C - 1:0] inp;
		sv2v_cast_BE6CF = inp;
	endfunction
	assign tgt_lane_w = sv2v_cast_BE6CF(babs_w >> 3);
	assign tgt_off_w = babs_w[2:0];
	wire need_flush_w;
	assign need_flush_w = ((((sk_valid_r && (st_r == 3'd0)) && (m_w != 3'd0)) && keep_w) && lane_open_r) && (tgt_lane_w != lane_ix_r);
	wire take_byte_w;
	wire last_byte_w;
	assign last_byte_w = ({1'b0, bix_r} + 3'd1) >= m_w;
	assign take_byte_w = (sk_valid_r && (st_r == 3'd0)) && !need_flush_w;
	assign rd_valid_o = rvalid_r && (st_r == 3'd3);
	function automatic [2:0] sv2v_cast_3;
		input reg [2:0] inp;
		sv2v_cast_3 = inp;
	endfunction
	always @(*) begin : read_byte
		if (_sv2v_0)
			;
		rd_data_o = 8'd0;
		begin : sv2v_autoblock_1
			reg [31:0] k;
			for (k = 0; k < 8; k = k + 1)
				if (roff_r == sv2v_cast_3(k))
					rd_data_o = rlane_r[63 - (8 * k)-:8];
		end
	end
	assign mem_rsp_ready_o = (st_r == 3'd4) || ((st_r == 3'd3) && !rvalid_r);
	wire [10:0] last_byte_ix_w;
	wire [8:0] rbeats_w;
	assign last_byte_ix_w = ({1'b0, HDR_BYTES_C} + len_r) - 11'd1;
	function automatic [8:0] sv2v_cast_9;
		input reg [8:0] inp;
		sv2v_cast_9 = inp;
	endfunction
	assign rbeats_w = sv2v_cast_9(last_byte_ix_w >> 3);
	assign mem_req_valid_o = rreq_r;
	assign mem_req_addr_o = RESP_BASE_P + 32'd8;
	assign mem_req_beats_o = rbeats_w;
	assign mem_wr_valid_o = wreq_r;
	function automatic [31:0] sv2v_cast_32;
		input reg [31:0] inp;
		sv2v_cast_32 = inp;
	endfunction
	assign mem_wr_addr_o = RESP_BASE_P + (sv2v_cast_32(lane_ix_r) << 3);
	assign mem_wr_data_o = lane_d_r;
	assign mem_wr_strb_o = lane_s_r;
	assign busy_o = ((wreq_r || wbusy_r) || rreq_r) || rbusy_r;
	assign err_o = fault_r;
	assign dbg_fault_o = fcode_r;
	assign dbg_lane_wr_o = lanewr_r;
	assign dbg_burst_o = burst_r;
	assign dbg_drop_o = drop_r;
	function automatic signed [TMO_W_C - 1:0] sv2v_cast_BA630_signed;
		input reg signed [TMO_W_C - 1:0] inp;
		sv2v_cast_BA630_signed = inp;
	endfunction
	always @(posedge clk_i) begin : core
		if (!rst_n) begin
			st_r <= 3'd0;
			lane_d_r <= 64'd0;
			lane_s_r <= 8'd0;
			lane_ix_r <= 1'sb0;
			lane_open_r <= 1'b0;
			seal_pend_r <= 1'b0;
			len_r <= 11'd0;
			served_r <= 11'd0;
			rlane_r <= 64'd0;
			rvalid_r <= 1'b0;
			roff_r <= FIRST_OFF_C;
			fault_r <= 1'b0;
			fcode_r <= FAULT_NONE_C;
			lanewr_r <= 16'd0;
			burst_r <= 16'd0;
			drop_r <= 16'd0;
			sk_valid_r <= 1'b0;
			sk_addr_r <= 10'd0;
			sk_data_r <= 32'd0;
			sk_strb_r <= 4'd0;
			bix_r <= 2'd0;
			wr_ready_r <= 1'b1;
			wreq_r <= 1'b0;
			wbusy_r <= 1'b0;
			rreq_r <= 1'b0;
			rbusy_r <= 1'b0;
			tmo_r <= 1'sb0;
		end
		else begin
			if (!wait_w)
				tmo_r <= 1'sb0;
			else if (!tmo_hit_w)
				tmo_r <= tmo_r + sv2v_cast_BA630_signed(1);
			if (open_i) begin
				st_r <= 3'd0;
				lane_open_r <= 1'b0;
				lane_s_r <= 8'd0;
				seal_pend_r <= 1'b0;
				served_r <= 11'd0;
				rvalid_r <= 1'b0;
				roff_r <= FIRST_OFF_C;
				fault_r <= 1'b0;
				fcode_r <= FAULT_NONE_C;
				len_r <= 11'd0;
				sk_valid_r <= 1'b0;
				bix_r <= 2'd0;
				wr_ready_r <= 1'b1;
				tmo_r <= 1'sb0;
			end
			else begin
				if (accept_w) begin
					sk_valid_r <= 1'b1;
					sk_addr_r <= wr_addr_i;
					sk_data_r <= wr_wdata_i;
					sk_strb_r <= wr_wstrb_i;
					bix_r <= 2'd0;
					wr_ready_r <= 1'b0;
				end
				else if (!sk_valid_r)
					wr_ready_r <= (st_r == 3'd0) || (st_r == 3'd6);
				(* full_case, parallel_case *)
				case (st_r)
					3'd0: begin
						if (take_byte_w) begin
							if (keep_w && (m_w != 3'd0)) begin
								if (!lane_open_r) begin
									lane_open_r <= 1'b1;
									lane_ix_r <= tgt_lane_w;
									lane_d_r <= 64'd0;
									lane_s_r <= 8'd0;
								end
								begin : sv2v_autoblock_2
									reg [31:0] k;
									for (k = 0; k < 8; k = k + 1)
										if (tgt_off_w == sv2v_cast_3(k)) begin
											lane_d_r[63 - (8 * k)-:8] <= bval_w;
											lane_s_r[k] <= 1'b1;
										end
								end
							end
							else if ((m_w != 3'd0) && (drop_r != 16'hffff))
								drop_r <= drop_r + 16'd1;
							if (last_byte_w) begin
								sk_valid_r <= 1'b0;
								bix_r <= 2'd0;
								wr_ready_r <= 1'b1;
							end
							else
								bix_r <= bix_r + 2'd1;
						end
						if (seal_i) begin
							len_r <= seal_len_i;
							seal_pend_r <= 1'b1;
						end
						if (need_flush_w) begin
							wreq_r <= 1'b1;
							st_r <= 3'd1;
						end
						else if ((seal_pend_r || seal_i) && !sk_valid_r) begin
							if (lane_open_r) begin
								wreq_r <= 1'b1;
								st_r <= 3'd1;
							end
							else
								st_r <= 3'd2;
						end
					end
					3'd1: begin
						if (seal_i) begin
							len_r <= seal_len_i;
							seal_pend_r <= 1'b1;
						end
						if (wreq_r && mem_wr_ready_i) begin
							wreq_r <= 1'b0;
							wbusy_r <= 1'b1;
						end
						if (wbusy_r && mem_wr_done_i) begin
							wbusy_r <= 1'b0;
							lane_open_r <= 1'b0;
							lane_s_r <= 8'd0;
							if (lanewr_r != 16'hffff)
								lanewr_r <= lanewr_r + 16'd1;
							if (mem_wr_err_i) begin
								fault_r <= 1'b1;
								fcode_r <= FAULT_WERR_C;
								st_r <= 3'd6;
							end
							else
								st_r <= (seal_pend_r && !sk_valid_r ? 3'd2 : 3'd0);
						end
						else if (tmo_hit_w) begin
							wreq_r <= 1'b0;
							wbusy_r <= 1'b0;
							fault_r <= 1'b1;
							fcode_r <= FAULT_WTMO_C;
							st_r <= 3'd6;
						end
					end
					3'd2: begin
						seal_pend_r <= 1'b0;
						if (len_r == 11'd0)
							st_r <= 3'd5;
						else begin
							rreq_r <= 1'b1;
							if (rreq_r && mem_req_ready_i) begin
								rreq_r <= 1'b0;
								rbusy_r <= 1'b1;
								roff_r <= FIRST_OFF_C;
								if (burst_r != 16'hffff)
									burst_r <= burst_r + 16'd1;
								st_r <= 3'd3;
							end
							else if (tmo_hit_w) begin
								rreq_r <= 1'b0;
								fault_r <= 1'b1;
								fcode_r <= FAULT_RTMO_C;
								st_r <= 3'd6;
							end
						end
					end
					3'd3: begin
						if (beat_w) begin
							rlane_r <= mem_rsp_data_i;
							rvalid_r <= 1'b1;
							if (mem_rsp_last_i)
								rbusy_r <= 1'b0;
							if (mem_rsp_err_i) begin
								rvalid_r <= 1'b0;
								rbusy_r <= 1'b0;
								fault_r <= 1'b1;
								fcode_r <= FAULT_RERR_C;
								st_r <= 3'd6;
							end
						end
						if (rd_take_i && rvalid_r) begin
							served_r <= served_r + 11'd1;
							roff_r <= roff_r + 3'd1;
							if (roff_r == 3'd7)
								rvalid_r <= 1'b0;
							if ((served_r + 11'd1) >= len_r) begin
								rvalid_r <= 1'b0;
								st_r <= (rbusy_r ? 3'd4 : 3'd5);
							end
						end
						if (tmo_hit_w) begin
							rbusy_r <= 1'b0;
							rvalid_r <= 1'b0;
							fault_r <= 1'b1;
							fcode_r <= FAULT_RTMO_C;
							st_r <= 3'd6;
						end
					end
					3'd4:
						if (beat_w) begin
							if (mem_rsp_last_i || mem_rsp_err_i) begin
								rbusy_r <= 1'b0;
								st_r <= 3'd5;
							end
						end
						else if (tmo_hit_w) begin
							rbusy_r <= 1'b0;
							st_r <= 3'd5;
						end
					3'd5:
						;
					default: begin
						rvalid_r <= 1'b0;
						sk_valid_r <= 1'b0;
						wr_ready_r <= 1'b1;
					end
				endcase
			end
		end
	end
	initial _sv2v_0 = 0;
endmodule
`default_nettype wire
`default_nettype none
module KL_aecp_ucpu (
	clk_i,
	rst_n,
	disp_valid_i,
	disp_ready_o,
	disp_upc_i,
	disp_ctlr_eid_i,
	disp_opd0_i,
	disp_opd1_i,
	disp_opd2_i,
	disp_batch_i,
	disp_resp_base_i,
	st_req_o,
	st_we_o,
	st_name_o,
	st_addr_o,
	st_wdata_o,
	st_wstrb_o,
	st_ready_i,
	st_rvalid_i,
	st_rdata_i,
	st_err_i,
	gx_req_o,
	gx_sel_o,
	gx_valid_i,
	gx_data_i,
	lock_held_i,
	lock_ctlr_i,
	rb_we_o,
	rb_addr_o,
	rb_wdata_o,
	rb_wstrb_o,
	rb_ready_i,
	resp_send_o,
	resp_len_o,
	resp_status_o,
	tx_ready_i,
	eff_commit_o,
	eff_nvm_mark_o,
	eff_nvm_stb_o,
	eff_notify_class_o,
	eff_notify_stb_o,
	busy_o,
	done_o,
	dbg_upc_o,
	dbg_status_o,
	dbg_ovf_o
);
	reg _sv2v_0;
	parameter UCODE_HEX_P = "ucode.hex";
	input wire clk_i;
	input wire rst_n;
	input wire disp_valid_i;
	output wire disp_ready_o;
	input wire [10:0] disp_upc_i;
	input wire [63:0] disp_ctlr_eid_i;
	input wire [63:0] disp_opd0_i;
	input wire [63:0] disp_opd1_i;
	input wire [63:0] disp_opd2_i;
	input wire disp_batch_i;
	input wire [9:0] disp_resp_base_i;
	output reg st_req_o;
	output reg st_we_o;
	output reg st_name_o;
	output reg [19:0] st_addr_o;
	output reg [63:0] st_wdata_o;
	output reg [7:0] st_wstrb_o;
	input wire st_ready_i;
	input wire st_rvalid_i;
	input wire [63:0] st_rdata_i;
	input wire st_err_i;
	output reg gx_req_o;
	output reg [7:0] gx_sel_o;
	input wire gx_valid_i;
	input wire [63:0] gx_data_i;
	input wire lock_held_i;
	input wire [63:0] lock_ctlr_i;
	output reg rb_we_o;
	output reg [9:0] rb_addr_o;
	output reg [31:0] rb_wdata_o;
	output reg [3:0] rb_wstrb_o;
	input wire rb_ready_i;
	output reg resp_send_o;
	output reg [10:0] resp_len_o;
	output reg [4:0] resp_status_o;
	input wire tx_ready_i;
	output reg eff_commit_o;
	output reg [7:0] eff_nvm_mark_o;
	output reg eff_nvm_stb_o;
	output reg [3:0] eff_notify_class_o;
	output reg eff_notify_stb_o;
	output wire busy_o;
	output reg done_o;
	output wire [10:0] dbg_upc_o;
	output wire [4:0] dbg_status_o;
	output wire dbg_ovf_o;
	localparam [31:0] ucpu_pkg_UCODE_W_C = 48;
	localparam [31:0] ucpu_pkg_UPC_W_C = 11;
	reg [47:0] rom_r [0:2047];
	initial $readmemh(UCODE_HEX_P, rom_r);
	reg [47:0] rom_q_r;
	reg [10:0] upc_r;
	(* ram_style = "distributed" *) reg [63:0] rf_r [0:15];
	reg [3:0] rf_waddr_w;
	reg [63:0] rf_wdata_w;
	reg rf_we_w;
	always @(posedge clk_i) begin : rf_write
		if (rf_we_w)
			rf_r[rf_waddr_w] <= rf_wdata_w;
	end
	reg [2:0] ms_r;
	reg vld_d_r;
	reg [47:0] uop_e_r;
	reg vld_e_r;
	reg [63:0] opa_e_r;
	reg [63:0] opb_e_r;
	reg [63:0] opd_e_r;
	reg [3:0] wb_rd_r;
	reg [63:0] wb_data_r;
	reg wb_we_r;
	reg [4:0] status_r;
	reg z_r;
	reg lt_r;
	reg ovf_r;
	reg [19:0] desc_base_r;
	reg [7:0] iter_cnt_r;
	reg [7:0] iter_idx_r;
	reg [9:0] cursor_r;
	reg [10:0] resp_len_r;
	reg batch_r;
	reg [3:0] eseq_r;
	reg copy_go_r;
	reg [15:0] copy_left_r;
	reg [12:0] copy_idx_r;
	reg [63:0] copy_lane_r;
	wire [47:0] uop_d_w;
	function automatic [47:0] sv2v_cast_48;
		input reg [47:0] inp;
		sv2v_cast_48 = inp;
	endfunction
	assign uop_d_w = sv2v_cast_48(rom_q_r);
	reg raw_d_w;
	reg e_writes_w;
	always @(*) begin : raw_detect
		if (_sv2v_0)
			;
		e_writes_w = vld_e_r && |{uop_e_r[47-:5] == 5'd4, uop_e_r[47-:5] == 5'd6, uop_e_r[47-:5] == 5'd29, uop_e_r[47-:5] == 5'd8, uop_e_r[47-:5] == 5'd10, uop_e_r[47-:5] == 5'd16};
		raw_d_w = vld_d_r && ((e_writes_w && (((uop_d_w[38-:4] == uop_e_r[42-:4]) || (uop_d_w[34-:4] == uop_e_r[42-:4])) || (uop_d_w[42-:4] == uop_e_r[42-:4]))) || (wb_we_r && (((uop_d_w[38-:4] == wb_rd_r) || (uop_d_w[34-:4] == wb_rd_r)) || (uop_d_w[42-:4] == wb_rd_r))));
	end
	reg [63:0] a_fmt_w;
	reg [63:0] b_or_imm_w;
	localparam [2:0] ucpu_pkg_FMT_B_C = 3'd0;
	localparam [2:0] ucpu_pkg_FMT_D_C = 3'd2;
	localparam [2:0] ucpu_pkg_FMT_W_C = 3'd1;
	always @(*) begin : operand_shape
		if (_sv2v_0)
			;
		(* full_case, parallel_case *)
		case (uop_e_r[30-:3])
			ucpu_pkg_FMT_B_C: a_fmt_w = {56'd0, opa_e_r[7:0]};
			ucpu_pkg_FMT_W_C: a_fmt_w = {48'd0, opa_e_r[15:0]};
			ucpu_pkg_FMT_D_C: a_fmt_w = {32'd0, opa_e_r[31:0]};
			default: a_fmt_w = opa_e_r;
		endcase
		b_or_imm_w = (uop_e_r[34-:4] != 4'd0 ? opb_e_r : {40'd0, uop_e_r[23-:24]});
	end
	reg [32:0] sub_w;
	reg cmp_z_w;
	reg cmp_lt_w;
	reg [63:0] merged_w;
	localparam [2:0] ucpu_pkg_FMT_Q_C = 3'd3;
	always @(*) begin : alu
		if (_sv2v_0)
			;
		sub_w = {1'b0, a_fmt_w[31:0]} - {1'b0, b_or_imm_w[31:0]};
		cmp_z_w = (uop_e_r[30-:3] == ucpu_pkg_FMT_Q_C ? opa_e_r == b_or_imm_w : sub_w[31:0] == 32'd0);
		cmp_lt_w = sub_w[32];
		merged_w = (opd_e_r & ~opb_e_r) | (opa_e_r & opb_e_r);
	end
	reg rel_pass_w;
	always @(*) begin : relation
		if (_sv2v_0)
			;
		(* full_case, parallel_case *)
		case (uop_e_r[26:24])
			3'd0: rel_pass_w = cmp_z_w;
			3'd1: rel_pass_w = !cmp_z_w;
			3'd2: rel_pass_w = cmp_lt_w;
			3'd3: rel_pass_w = !cmp_lt_w;
			default: rel_pass_w = cmp_z_w;
		endcase
	end
	reg brflag_w;
	localparam [4:0] ucpu_pkg_ST_SUCCESS_C = 5'd0;
	always @(*) begin : branch_flag
		if (_sv2v_0)
			;
		(* full_case, parallel_case *)
		case (uop_e_r[27-:4])
			4'd0: brflag_w = status_r != ucpu_pkg_ST_SUCCESS_C;
			4'd1: brflag_w = iter_idx_r == iter_cnt_r;
			4'd2: brflag_w = z_r;
			4'd3: brflag_w = lt_r;
			4'd4: brflag_w = ovf_r;
			default: brflag_w = 1'b0;
		endcase
	end
	reg [3:0] fld_len_w;
	always @(*) begin : field_len
		if (_sv2v_0)
			;
		(* full_case, parallel_case *)
		case (uop_e_r[30-:3])
			ucpu_pkg_FMT_B_C: fld_len_w = 4'd1;
			ucpu_pkg_FMT_W_C: fld_len_w = 4'd2;
			ucpu_pkg_FMT_D_C: fld_len_w = 4'd4;
			default: fld_len_w = 4'd8;
		endcase
	end
	reg [3:0] copy_adv1_w;
	reg [3:0] copy_adv2_w;
	function automatic [3:0] sv2v_cast_4;
		input reg [3:0] inp;
		sv2v_cast_4 = inp;
	endfunction
	always @(*) begin : copy_residual
		if (_sv2v_0)
			;
		copy_adv1_w = (copy_left_r > 16'd4 ? 4'd4 : copy_left_r[3:0]);
		if (copy_left_r <= 16'd4)
			copy_adv2_w = 4'd0;
		else if (copy_left_r > 16'd8)
			copy_adv2_w = 4'd4;
		else
			copy_adv2_w = sv2v_cast_4(copy_left_r[3:0] - 4'd4);
	end
	wire append_skip_w;
	localparam [31:0] ucpu_pkg_RESP_CAP_C = 524;
	function automatic [10:0] sv2v_cast_11;
		input reg [10:0] inp;
		sv2v_cast_11 = inp;
	endfunction
	assign append_skip_w = (uop_e_r[47-:5] == 5'd20) && (({1'b0, cursor_r} + {7'd0, fld_len_w}) > sv2v_cast_11(ucpu_pkg_RESP_CAP_C));
	wire is_q_field_w;
	assign is_q_field_w = (|{uop_e_r[47-:5] == 5'd27, uop_e_r[47-:5] == 5'd20} && (uop_e_r[30-:3] == ucpu_pkg_FMT_Q_C)) && !append_skip_w;
	wire rb_hold_w;
	assign rb_hold_w = rb_we_o && !rb_ready_i;
	reg stall_e_w;
	reg br_taken_w;
	reg [10:0] br_tgt_w;
	reg end_op_w;
	always @(*) begin : e_control
		if (_sv2v_0)
			;
		stall_e_w = 1'b0;
		br_taken_w = 1'b0;
		br_tgt_w = uop_e_r[10:0];
		end_op_w = 1'b0;
		if (vld_e_r) begin
			(* full_case, parallel_case *)
			case (uop_e_r[47-:5])
				5'd1: br_taken_w = 1'b1;
				5'd2: br_taken_w = brflag_w;
				5'd3: end_op_w = 1'b1;
				5'd7, 5'd8, 5'd10: stall_e_w = !st_rvalid_i;
				5'd9, 5'd11: stall_e_w = !st_ready_i;
				5'd16, 5'd15: stall_e_w = !gx_valid_i;
				5'd17: stall_e_w = eseq_r != 4'd4;
				5'd12: stall_e_w = (!copy_go_r || (copy_left_r != 16'd0)) || (eseq_r != 4'd0);
				5'd26: stall_e_w = eseq_r != 4'd2;
				5'd27, 5'd20: stall_e_w = is_q_field_w && (eseq_r == 4'd0);
				5'd28: stall_e_w = !tx_ready_i;
				5'd13: br_taken_w = lock_held_i && (lock_ctlr_i != opa_e_r);
				5'd14: br_taken_w = !rel_pass_w;
				default:
					;
			endcase
			if (((uop_e_r[47-:5] == 5'd15) && gx_valid_i) && !gx_data_i[0])
				br_taken_w = 1'b1;
			if (rb_hold_w)
				stall_e_w = 1'b1;
		end
	end
	always @(*) begin : state_port
		if (_sv2v_0)
			;
		st_req_o = 1'b0;
		st_we_o = 1'b0;
		st_name_o = 1'b0;
		st_wdata_o = opa_e_r;
		st_addr_o = desc_base_r + uop_e_r[19:0];
		(* full_case, parallel_case *)
		case (uop_e_r[30-:3])
			ucpu_pkg_FMT_B_C: st_wstrb_o = 8'h01;
			ucpu_pkg_FMT_W_C: st_wstrb_o = 8'h03;
			ucpu_pkg_FMT_D_C: st_wstrb_o = 8'h0f;
			default: st_wstrb_o = 8'hff;
		endcase
		if (vld_e_r)
			(* full_case, parallel_case *)
			case (uop_e_r[47-:5])
				5'd7: begin
					st_req_o = 1'b1;
					st_addr_o = uop_e_r[19:0] ^ {4'd0, opa_e_r[15:0]};
				end
				5'd8: st_req_o = 1'b1;
				5'd10: begin
					st_req_o = 1'b1;
					st_name_o = 1'b1;
					st_addr_o = opa_e_r[19:0] + uop_e_r[19:0];
				end
				5'd9: begin
					st_req_o = 1'b1;
					st_we_o = 1'b1;
				end
				5'd11: begin
					st_req_o = 1'b1;
					st_we_o = 1'b1;
					st_name_o = 1'b1;
					st_addr_o = opb_e_r[19:0] + uop_e_r[19:0];
				end
				5'd12: begin
					st_req_o = (copy_go_r && (copy_left_r != 16'd0)) && (eseq_r == 4'd0);
					st_addr_o = (desc_base_r + uop_e_r[19:0]) + {4'd0, copy_idx_r, 3'd0};
				end
				default:
					;
			endcase
	end
	always @(*) begin : gather_port
		if (_sv2v_0)
			;
		gx_req_o = 1'b0;
		gx_sel_o = {uop_e_r[27-:4], uop_e_r[3:0]};
		if (vld_e_r)
			(* full_case, parallel_case *)
			case (uop_e_r[47-:5])
				5'd16: gx_req_o = 1'b1;
				5'd15: begin
					gx_req_o = 1'b1;
					gx_sel_o = {uop_e_r[27-:4], 4'd0};
				end
				5'd17: begin
					gx_req_o = eseq_r < 4'd4;
					gx_sel_o = {uop_e_r[27-:4], eseq_r};
				end
				default:
					;
			endcase
	end
	reg [31:0] hdr_word_w;
	always @(*) begin : header_word
		if (_sv2v_0)
			;
		(* full_case, parallel_case *)
		case (eseq_r)
			4'd0: hdr_word_w = opa_e_r[63:32];
			4'd1: hdr_word_w = opa_e_r[31:0];
			default: hdr_word_w = {opb_e_r[15:0], 3'd0, status_r, 8'd0};
		endcase
	end
	always @(*) begin : resp_buffer
		if (_sv2v_0)
			;
		rb_we_o = 1'b0;
		rb_addr_o = cursor_r;
		rb_wdata_o = a_fmt_w[31:0];
		rb_wstrb_o = 4'hf;
		if (vld_e_r)
			(* full_case, parallel_case *)
			case (uop_e_r[47-:5])
				5'd26: begin
					rb_we_o = !batch_r;
					rb_addr_o = {4'd0, eseq_r[1:0], 4'd0} >> 2;
					rb_wdata_o = hdr_word_w;
				end
				5'd27, 5'd20: begin
					rb_we_o = !append_skip_w;
					if (is_q_field_w) begin
						rb_addr_o = cursor_r + (eseq_r == 4'd1 ? 10'd4 : 10'd0);
						rb_wdata_o = (eseq_r == 4'd0 ? opa_e_r[63:32] : opa_e_r[31:0]);
					end
					else
						(* full_case, parallel_case *)
						case (uop_e_r[30-:3])
							ucpu_pkg_FMT_B_C: rb_wstrb_o = 4'h1;
							ucpu_pkg_FMT_W_C: rb_wstrb_o = 4'h3;
							default: rb_wstrb_o = 4'hf;
						endcase
				end
				5'd17: begin
					rb_we_o = gx_valid_i && (eseq_r < 4'd4);
					rb_wdata_o = gx_data_i[31:0];
				end
				5'd12: begin
					rb_we_o = ((eseq_r == 4'd1) && (copy_adv1_w != 4'd0)) || ((eseq_r == 4'd2) && (copy_adv2_w != 4'd0));
					rb_wdata_o = (eseq_r == 4'd1 ? copy_lane_r[63:32] : copy_lane_r[31:0]);
				end
				default:
					;
			endcase
	end
	wire advance_e_w;
	assign advance_e_w = vld_e_r && !stall_e_w;
	always @(*) begin : effects
		if (_sv2v_0)
			;
		eff_commit_o = advance_e_w && (uop_e_r[47-:5] == 5'd21);
		eff_nvm_stb_o = advance_e_w && (uop_e_r[47-:5] == 5'd22);
		eff_nvm_mark_o = uop_e_r[7:0];
		eff_notify_stb_o = advance_e_w && (uop_e_r[47-:5] == 5'd23);
		eff_notify_class_o = uop_e_r[3:0];
		resp_send_o = advance_e_w && (uop_e_r[47-:5] == 5'd28);
		resp_len_o = resp_len_r;
		resp_status_o = status_r;
	end
	always @(*) begin : writeback_mux
		if (_sv2v_0)
			;
		rf_we_w = wb_we_r;
		rf_waddr_w = wb_rd_r;
		rf_wdata_w = wb_data_r;
		(* full_case, parallel_case *)
		case (ms_r)
			3'd1: begin
				rf_we_w = 1'b1;
				rf_waddr_w = 4'd12;
				rf_wdata_w = disp_opd2_i;
			end
			3'd2: begin
				rf_we_w = 1'b1;
				rf_waddr_w = 4'd15;
				rf_wdata_w = disp_ctlr_eid_i;
			end
			3'd3: begin
				rf_we_w = 1'b1;
				rf_waddr_w = 4'd14;
				rf_wdata_w = disp_opd0_i;
			end
			3'd4: begin
				rf_we_w = 1'b1;
				rf_waddr_w = 4'd13;
				rf_wdata_w = disp_opd1_i;
			end
			default:
				;
		endcase
	end
	localparam [4:0] ucpu_pkg_ST_BAD_ARGUMENTS_C = 5'd7;
	localparam [4:0] ucpu_pkg_ST_ENTITY_MISBEHAVING_C = 5'd10;
	localparam [4:0] ucpu_pkg_ST_LOCKED_C = 5'd3;
	localparam [4:0] ucpu_pkg_ST_NOT_SUPPORTED_C = 5'd11;
	localparam [4:0] ucpu_pkg_ST_NO_SUCH_DESC_C = 5'd2;
	function automatic signed [10:0] sv2v_cast_8D9A8_signed;
		input reg signed [10:0] inp;
		sv2v_cast_8D9A8_signed = inp;
	endfunction
	always @(posedge clk_i) begin : core
		if (!rst_n) begin
			ms_r <= 3'd0;
			upc_r <= 1'sb0;
			vld_d_r <= 1'b0;
			vld_e_r <= 1'b0;
			wb_we_r <= 1'b0;
			wb_rd_r <= 1'sb0;
			wb_data_r <= 1'sb0;
			status_r <= ucpu_pkg_ST_SUCCESS_C;
			z_r <= 1'b0;
			lt_r <= 1'b0;
			ovf_r <= 1'b0;
			desc_base_r <= 1'sb0;
			iter_cnt_r <= 1'sb0;
			iter_idx_r <= 1'sb0;
			cursor_r <= 1'sb0;
			resp_len_r <= 1'sb0;
			batch_r <= 1'b0;
			eseq_r <= 1'sb0;
			copy_go_r <= 1'b0;
			copy_left_r <= 1'sb0;
			copy_idx_r <= 1'sb0;
			copy_lane_r <= 1'sb0;
			rom_q_r <= 1'sb0;
			uop_e_r <= 1'sb0;
			opa_e_r <= 1'sb0;
			opb_e_r <= 1'sb0;
			opd_e_r <= 1'sb0;
			done_o <= 1'b0;
		end
		else begin
			done_o <= 1'b0;
			wb_we_r <= 1'b0;
			(* full_case, parallel_case *)
			case (ms_r)
				3'd0: begin
					vld_d_r <= 1'b0;
					vld_e_r <= 1'b0;
					if (disp_valid_i) begin
						ms_r <= 3'd1;
						upc_r <= disp_upc_i;
						status_r <= ucpu_pkg_ST_SUCCESS_C;
						z_r <= 1'b0;
						lt_r <= 1'b0;
						ovf_r <= 1'b0;
						batch_r <= disp_batch_i;
						cursor_r <= (disp_batch_i ? disp_resp_base_i : 10'd12);
						resp_len_r <= (disp_batch_i ? {1'b0, disp_resp_base_i} : 11'd12);
						iter_cnt_r <= 1'sb0;
						iter_idx_r <= 1'sb0;
						eseq_r <= 1'sb0;
						copy_go_r <= 1'b0;
						copy_left_r <= 1'sb0;
					end
				end
				3'd1: ms_r <= 3'd2;
				3'd2: ms_r <= 3'd3;
				3'd3: ms_r <= 3'd4;
				3'd4: ms_r <= 3'd5;
				3'd5: begin
					if (!stall_e_w && !raw_d_w) begin
						rom_q_r <= rom_r[upc_r];
						vld_d_r <= 1'b1;
						upc_r <= upc_r + sv2v_cast_8D9A8_signed(1);
					end
					if (!stall_e_w) begin
						if (raw_d_w)
							vld_e_r <= 1'b0;
						else begin
							vld_e_r <= vld_d_r;
							uop_e_r <= uop_d_w;
							opa_e_r <= rf_r[uop_d_w[38-:4]];
							opb_e_r <= rf_r[uop_d_w[34-:4]];
							opd_e_r <= rf_r[uop_d_w[42-:4]];
						end
					end
					if (vld_e_r && !rb_hold_w) begin
						(* full_case, parallel_case *)
						case (uop_e_r[47-:5])
							5'd26: eseq_r <= (eseq_r == 4'd2 ? 4'd0 : eseq_r + 4'd1);
							5'd27, 5'd20:
								if (is_q_field_w)
									eseq_r <= (eseq_r == 4'd1 ? 4'd0 : 4'd1);
							5'd17:
								if (gx_valid_i && (eseq_r < 4'd4)) begin
									eseq_r <= eseq_r + 4'd1;
									cursor_r <= cursor_r + 10'd4;
									resp_len_r <= resp_len_r + 11'd4;
								end
								else if (eseq_r == 4'd4)
									eseq_r <= 4'd0;
							5'd12:
								if (!copy_go_r) begin
									copy_go_r <= 1'b1;
									copy_left_r <= opa_e_r[15:0];
									copy_idx_r <= 1'sb0;
								end
								else if (((eseq_r == 4'd0) && st_rvalid_i) && (copy_left_r != 16'd0)) begin
									copy_lane_r <= st_rdata_i;
									eseq_r <= 4'd1;
								end
								else if (eseq_r == 4'd1) begin
									eseq_r <= 4'd2;
									cursor_r <= cursor_r + {6'd0, copy_adv1_w};
									resp_len_r <= resp_len_r + {7'd0, copy_adv1_w};
								end
								else if (eseq_r == 4'd2) begin
									eseq_r <= 4'd0;
									cursor_r <= cursor_r + {6'd0, copy_adv2_w};
									resp_len_r <= resp_len_r + {7'd0, copy_adv2_w};
									copy_left_r <= (copy_left_r > 16'd8 ? copy_left_r - 16'd8 : 16'd0);
									copy_idx_r <= copy_idx_r + 13'd1;
								end
							default: eseq_r <= 4'd0;
						endcase
						if (advance_e_w) begin
							copy_go_r <= 1'b0;
							(* full_case, parallel_case *)
							case (uop_e_r[47-:5])
								5'd4: begin
									wb_we_r <= 1'b1;
									wb_rd_r <= uop_e_r[42-:4];
									wb_data_r <= (uop_e_r[38-:4] == 4'd0 ? {40'd0, uop_e_r[23-:24]} : a_fmt_w);
								end
								5'd6: begin
									wb_we_r <= 1'b1;
									wb_rd_r <= uop_e_r[42-:4];
									wb_data_r <= merged_w;
								end
								5'd29: begin
									wb_we_r <= 1'b1;
									wb_rd_r <= uop_e_r[42-:4];
									wb_data_r <= opa_e_r >> uop_e_r[5:0];
								end
								5'd8, 5'd10: begin
									wb_we_r <= 1'b1;
									wb_rd_r <= uop_e_r[42-:4];
									wb_data_r <= st_rdata_i;
								end
								5'd16: begin
									wb_we_r <= 1'b1;
									wb_rd_r <= uop_e_r[42-:4];
									wb_data_r <= gx_data_i;
								end
								default:
									;
							endcase
							(* full_case, parallel_case *)
							case (uop_e_r[47-:5])
								5'd5: begin
									z_r <= cmp_z_w;
									lt_r <= cmp_lt_w;
								end
								5'd7:
									if (st_err_i)
										status_r <= ucpu_pkg_ST_NO_SUCH_DESC_C;
									else
										desc_base_r <= st_rdata_i[19:0];
								5'd8:
									if (st_err_i)
										status_r <= ucpu_pkg_ST_BAD_ARGUMENTS_C;
								5'd9:
									if (st_err_i)
										status_r <= ucpu_pkg_ST_ENTITY_MISBEHAVING_C;
								5'd13:
									if (br_taken_w)
										status_r <= ucpu_pkg_ST_LOCKED_C;
								5'd14:
									if (br_taken_w)
										status_r <= (uop_e_r[27] ? ucpu_pkg_ST_NOT_SUPPORTED_C : ucpu_pkg_ST_BAD_ARGUMENTS_C);
								5'd15:
									if (br_taken_w)
										status_r <= ucpu_pkg_ST_BAD_ARGUMENTS_C;
								5'd18: begin
									iter_cnt_r <= opa_e_r[7:0];
									iter_idx_r <= 1'sb0;
								end
								5'd19: iter_idx_r <= iter_idx_r + 8'd1;
								5'd24: status_r <= uop_e_r[4:0];
								5'd25: resp_len_r <= uop_e_r[10:0];
								5'd27, 5'd20:
									if (append_skip_w)
										ovf_r <= 1'b1;
									else begin
										cursor_r <= cursor_r + {6'd0, fld_len_w};
										resp_len_r <= resp_len_r + {7'd0, fld_len_w};
									end
								default:
									;
							endcase
							if (end_op_w) begin
								ms_r <= 3'd0;
								vld_d_r <= 1'b0;
								vld_e_r <= 1'b0;
								done_o <= 1'b1;
							end
							else if (br_taken_w) begin
								upc_r <= br_tgt_w;
								vld_d_r <= 1'b0;
								vld_e_r <= 1'b0;
							end
						end
					end
				end
				default: ms_r <= 3'd0;
			endcase
		end
	end
	assign disp_ready_o = ms_r == 3'd0;
	assign busy_o = ms_r != 3'd0;
	assign dbg_upc_o = upc_r;
	assign dbg_status_o = status_r;
	assign dbg_ovf_o = ovf_r;
	initial _sv2v_0 = 0;
endmodule
`default_nettype wire
`default_nettype none
module KL_pp_prng (
	clk_i,
	rst_n,
	entity_id_i,
	link_up_i,
	draw_req_i,
	draw_kind_i,
	draw_busy_o,
	draw_valid_o,
	draw_ms_o,
	dbg_lfsr_o,
	dbg_seeded_o
);
	reg _sv2v_0;
	input wire clk_i;
	input wire rst_n;
	input wire [63:0] entity_id_i;
	input wire link_up_i;
	input wire draw_req_i;
	input wire [2:0] draw_kind_i;
	output wire draw_busy_o;
	output reg draw_valid_o;
	output reg [15:0] draw_ms_o;
	output wire [63:0] dbg_lfsr_o;
	output wire dbg_seeded_o;
	localparam [63:0] POLY_C = 64'hd800000000000000;
	localparam [63:0] NONZERO_C = 64'h0000000000000001;
	reg [63:0] lfsr_r;
	reg [63:0] ctr_r;
	reg seeded_r;
	reg link_up_q_r;
	reg [63:0] lfsr_next_w;
	wire [63:0] seed_w;
	wire link_rise_w;
	function automatic [63:0] lfsr_step_f;
		input reg [63:0] s;
		lfsr_step_f = (s >> 1) ^ (s[0] ? POLY_C : 64'h0000000000000000);
	endfunction
	localparam [31:0] STEPS_C = 16;
	always @(*) begin : advance_16
		reg [63:0] s;
		if (_sv2v_0)
			;
		s = lfsr_r;
		begin : sv2v_autoblock_1
			reg [31:0] i;
			for (i = 0; i < STEPS_C; i = i + 1)
				s = lfsr_step_f(s);
		end
		lfsr_next_w = s;
	end
	assign link_rise_w = link_up_i && !link_up_q_r;
	assign seed_w = entity_id_i ^ ctr_r;
	always @(posedge clk_i) begin : seed_and_advance
		if (!rst_n) begin
			lfsr_r <= NONZERO_C;
			ctr_r <= 64'd0;
			seeded_r <= 1'b0;
			link_up_q_r <= 1'b0;
		end
		else begin
			ctr_r <= ctr_r + 64'd1;
			link_up_q_r <= link_up_i;
			if (link_rise_w && !seeded_r) begin
				lfsr_r <= (seed_w == 64'd0 ? NONZERO_C : seed_w);
				seeded_r <= 1'b1;
			end
			else
				lfsr_r <= lfsr_next_w;
		end
	end
	reg [2:0] kind_r;
	reg busy_r;
	reg [15:0] mask_w;
	reg [15:0] limit_w;
	reg [15:0] base_w;
	wire [15:0] span_w;
	wire accept_w;
	always @(*) begin : kind_decode
		if (_sv2v_0)
			;
		(* full_case, parallel_case *)
		case (kind_r)
			3'd0: begin
				mask_w = 16'h03ff;
				limit_w = 16'd1000;
				base_w = 16'd0;
			end
			3'd1: begin
				mask_w = 16'h07ff;
				limit_w = 16'd2000;
				base_w = 16'd0;
			end
			3'd2: begin
				mask_w = 16'h0fff;
				limit_w = 16'd4000;
				base_w = 16'd0;
			end
			3'd3: begin
				mask_w = 16'h1fff;
				limit_w = 16'd5000;
				base_w = 16'd10000;
			end
			3'd4: begin
				mask_w = 16'h7fff;
				limit_w = 16'd30000;
				base_w = 16'd30000;
			end
			3'd5: begin
				mask_w = 16'h007f;
				limit_w = 16'd98;
				base_w = 16'd501;
			end
			3'd6: begin
				mask_w = 16'h07ff;
				limit_w = 16'd1998;
				base_w = 16'd30001;
			end
			default: begin
				mask_w = 16'hffff;
				limit_w = 16'hfdff;
				base_w = 16'd0;
			end
		endcase
	end
	assign span_w = lfsr_r[15:0] & mask_w;
	assign accept_w = span_w <= limit_w;
	always @(posedge clk_i) begin : draw_sm
		if (!rst_n) begin
			busy_r <= 1'b0;
			kind_r <= 3'd0;
			draw_valid_o <= 1'b0;
			draw_ms_o <= 16'd0;
		end
		else begin
			draw_valid_o <= 1'b0;
			if (!busy_r) begin
				if (draw_req_i) begin
					kind_r <= draw_kind_i;
					busy_r <= 1'b1;
				end
			end
			else if (accept_w) begin
				draw_ms_o <= span_w + base_w;
				draw_valid_o <= 1'b1;
				busy_r <= 1'b0;
			end
		end
	end
	assign draw_busy_o = busy_r;
	assign dbg_lfsr_o = lfsr_r;
	assign dbg_seeded_o = seeded_r;
	initial _sv2v_0 = 0;
endmodule
`default_nettype wire
`default_nettype none
module KL_pp_timer_service (
	clk_i,
	rst_n,
	tick_ms_o,
	now_ms_o,
	arm_valid_i,
	arm_cancel_i,
	arm_slot_i,
	arm_owner_i,
	arm_deadline_ms_i,
	exp_valid_o,
	exp_slot_o,
	exp_owner_o
);
	parameter [31:0] CLK_HZ_P = 100000000;
	localparam [31:0] pp_pkg_PP_CA_POOL_C = 4;
	localparam [31:0] pp_pkg_PP_N_CTRL_C = 16;
	localparam [31:0] pp_pkg_PP_N_IF_C = 1;
	localparam [31:0] pp_pkg_PP_N_STREAM_IN_C = 8;
	localparam [31:0] pp_pkg_PP_N_STREAM_OUT_C = 8;
	localparam [31:0] pp_pkg_PP_MAAP_SLOTS_C = 2;
	localparam [31:0] pp_pkg_PP_SINGLETON_SLOTS_C = 5;
	localparam [31:0] pp_pkg_PP_SRP_CAD_SLOTS_C = 7;
	function automatic [415:0] pp_pkg_pp_timer_map;
		input reg [31:0] n_if;
		input reg [31:0] si;
		input reg [31:0] so;
		input reg [31:0] n_ctrl;
		input reg [31:0] ca_pool;
		reg [415:0] m;
		begin
			m[415-:32] = 32'd0;
			m[383-:32] = m[415-:32] + n_if;
			m[351-:32] = m[383-:32] + si;
			m[319-:32] = m[351-:32] + si;
			m[287-:32] = m[319-:32] + so;
			m[255-:32] = m[287-:32] + ((32'd2 * n_ctrl) * n_if);
			m[223-:32] = m[255-:32] + ca_pool;
			m[191-:32] = m[223-:32] + pp_pkg_PP_SINGLETON_SLOTS_C;
			m[159-:32] = m[191-:32] + pp_pkg_PP_MAAP_SLOTS_C;
			m[127-:32] = m[159-:32];
			m[95-:32] = m[127-:32] + pp_pkg_PP_SRP_CAD_SLOTS_C;
			m[63-:32] = m[95-:32] + so;
			m[31-:32] = m[127-:32] + (((pp_pkg_PP_SRP_CAD_SLOTS_C + si) + so) * n_if);
			pp_pkg_pp_timer_map = m;
		end
	endfunction
	function automatic [31:0] pp_pkg_pp_timer_slots;
		input reg [31:0] n_if;
		input reg [31:0] si;
		input reg [31:0] so;
		input reg [31:0] n_ctrl;
		input reg [31:0] ca_pool;
		input reg en_srp;
		reg [415:0] m;
		begin
			m = pp_pkg_pp_timer_map(n_if, si, so, n_ctrl, ca_pool);
			pp_pkg_pp_timer_slots = (en_srp ? m[31-:32] : m[159-:32]);
		end
	endfunction
	localparam [31:0] pp_pkg_PP_TIMER_SLOTS_C = pp_pkg_pp_timer_slots(pp_pkg_PP_N_IF_C, pp_pkg_PP_N_STREAM_IN_C, pp_pkg_PP_N_STREAM_OUT_C, pp_pkg_PP_N_CTRL_C, pp_pkg_PP_CA_POOL_C, 1'b1);
	parameter [31:0] SLOTS_P = pp_pkg_PP_TIMER_SLOTS_C;
	parameter [31:0] DIV_US_P = CLK_HZ_P / 32'd1000000;
	parameter [31:0] DIV_MS_P = 1000;
	localparam [31:0] SLOT_AW_C = (SLOTS_P > 32'd1 ? $clog2(SLOTS_P) : 32'd1);
	input wire clk_i;
	input wire rst_n;
	output wire tick_ms_o;
	output wire [31:0] now_ms_o;
	input wire arm_valid_i;
	input wire arm_cancel_i;
	input wire [SLOT_AW_C - 1:0] arm_slot_i;
	localparam [31:0] pp_pkg_PP_TIMER_OWNER_W_C = 8;
	input wire [7:0] arm_owner_i;
	input wire [31:0] arm_deadline_ms_i;
	output wire exp_valid_o;
	output wire [SLOT_AW_C - 1:0] exp_slot_o;
	output wire [7:0] exp_owner_o;
	localparam [31:0] pp_pkg_PP_TIMER_SLOT_DW_C = 40;
	localparam [31:0] SLOT_DW_C = pp_pkg_PP_TIMER_SLOT_DW_C;
	reg [31:0] us_cnt_r;
	reg [31:0] ms_cnt_r;
	reg [31:0] now_ms_r;
	wire tick_us_w;
	wire tick_ms_w;
	assign tick_us_w = us_cnt_r == (DIV_US_P - 32'd1);
	assign tick_ms_w = tick_us_w && (ms_cnt_r == (DIV_MS_P - 32'd1));
	always @(posedge clk_i) begin : prescaler
		if (!rst_n) begin
			us_cnt_r <= 32'd0;
			ms_cnt_r <= 32'd0;
			now_ms_r <= 32'd0;
		end
		else begin
			us_cnt_r <= (tick_us_w ? 32'd0 : us_cnt_r + 32'd1);
			if (tick_us_w)
				ms_cnt_r <= (tick_ms_w ? 32'd0 : ms_cnt_r + 32'd1);
			if (tick_ms_w)
				now_ms_r <= now_ms_r + 32'd1;
		end
	end
	assign tick_ms_o = tick_ms_w;
	assign now_ms_o = now_ms_r;
	reg [39:0] slot_ram_r [0:SLOTS_P - 1];
	reg [39:0] sweep_rdata_r;
	reg [SLOT_AW_C - 1:0] sweep_addr_r;
	always @(posedge clk_i) begin : slot_ram_write
		if (arm_valid_i && !arm_cancel_i)
			slot_ram_r[arm_slot_i] <= {arm_owner_i, arm_deadline_ms_i};
	end
	always @(posedge clk_i) begin : slot_ram_read
		sweep_rdata_r <= slot_ram_r[sweep_addr_r];
	end
	reg sweep_act_r;
	reg sweep_pend_r;
	reg chk_valid_r;
	reg [SLOT_AW_C - 1:0] chk_slot_r;
	function automatic [SLOT_AW_C - 1:0] sv2v_cast_72D6D;
		input reg [SLOT_AW_C - 1:0] inp;
		sv2v_cast_72D6D = inp;
	endfunction
	function automatic signed [SLOT_AW_C - 1:0] sv2v_cast_72D6D_signed;
		input reg signed [SLOT_AW_C - 1:0] inp;
		sv2v_cast_72D6D_signed = inp;
	endfunction
	always @(posedge clk_i) begin : sweep_ctrl
		if (!rst_n) begin
			sweep_act_r <= 1'b0;
			sweep_pend_r <= 1'b0;
			sweep_addr_r <= 1'sb0;
			chk_valid_r <= 1'b0;
			chk_slot_r <= 1'sb0;
		end
		else begin
			chk_valid_r <= sweep_act_r;
			chk_slot_r <= sweep_addr_r;
			if (sweep_act_r) begin
				if (sweep_addr_r == sv2v_cast_72D6D(SLOTS_P - 32'd1)) begin
					sweep_act_r <= 1'b0;
					sweep_addr_r <= 1'sb0;
				end
				else
					sweep_addr_r <= sweep_addr_r + sv2v_cast_72D6D_signed(1);
				if (tick_ms_w)
					sweep_pend_r <= 1'b1;
			end
			else if (tick_ms_w || sweep_pend_r) begin
				sweep_act_r <= 1'b1;
				sweep_pend_r <= 1'b0;
			end
		end
	end
	wire [7:0] chk_owner_w;
	wire [31:0] chk_deadline_w;
	wire [31:0] age_w;
	wire exp_fire_w;
	reg [SLOTS_P - 1:0] armed_r;
	reg arm_q_valid_r;
	reg [SLOT_AW_C - 1:0] arm_q_slot_r;
	wire arm_shadow_w;
	always @(posedge clk_i) begin : arm_shadow
		if (!rst_n) begin
			arm_q_valid_r <= 1'b0;
			arm_q_slot_r <= 1'sb0;
		end
		else begin
			arm_q_valid_r <= arm_valid_i;
			arm_q_slot_r <= arm_slot_i;
		end
	end
	assign arm_shadow_w = (arm_valid_i && (arm_slot_i == chk_slot_r)) || (arm_q_valid_r && (arm_q_slot_r == chk_slot_r));
	assign {chk_owner_w, chk_deadline_w} = sweep_rdata_r;
	assign age_w = now_ms_r - chk_deadline_w;
	assign exp_fire_w = ((chk_valid_r && armed_r[chk_slot_r]) && !age_w[31]) && !arm_shadow_w;
	always @(posedge clk_i) begin : armed_flags
		if (!rst_n)
			armed_r <= 1'sb0;
		else begin
			if (exp_fire_w)
				armed_r[chk_slot_r] <= 1'b0;
			if (arm_valid_i)
				armed_r[arm_slot_i] <= !arm_cancel_i;
		end
	end
	assign exp_valid_o = exp_fire_w;
	assign exp_slot_o = chk_slot_r;
	assign exp_owner_o = chk_owner_w;
endmodule
`default_nettype wire
`default_nettype none
module KL_pp_maap (
	clk_i,
	rst_n,
	cfg_en_i,
	cfg_count_i,
	cfg_seed_offset_i,
	cfg_seed_valid_i,
	own_mac_i,
	link_up_i,
	txn_valid_i,
	txn_i,
	txn_ready_o,
	rxs_free_o,
	rxs_free_slot_o,
	prng_draw_req_o,
	prng_draw_kind_o,
	prng_draw_busy_i,
	prng_draw_valid_i,
	prng_draw_ms_i,
	now_ms_i,
	tmr_arm_valid_o,
	tmr_arm_cancel_o,
	tmr_arm_slot_o,
	tmr_arm_owner_o,
	tmr_arm_deadline_ms_o,
	tmr_exp_valid_i,
	tmr_exp_slot_i,
	tmr_exp_owner_i,
	txs_alloc_req_o,
	txs_oversize_o,
	txs_alloc_gnt_i,
	txs_alloc_slot_i,
	txs_wr_slot_o,
	txs_wr_addr_o,
	txs_wr_valid_o,
	txs_wr_data_o,
	txs_wr_commit_o,
	txs_wr_len_o,
	txreq_valid_o,
	txreq_slot_o,
	txreq_ready_i,
	alloc_req_valid_i,
	alloc_req_ready_o,
	alloc_req_release_i,
	alloc_req_src_i,
	alloc_rsp_valid_o,
	alloc_rsp_ok_o,
	alloc_rsp_da_o,
	conflict_valid_o,
	conflict_src_o,
	conflict_ack_i,
	addr_o,
	addr_valid_o,
	state_o,
	conflicts_o,
	defends_o
);
	reg _sv2v_0;
	parameter [31:0] N_SRC_P = 8;
	parameter [31:0] RX_SLOTS_P = 4;
	localparam [31:0] pp_pkg_PP_CA_POOL_C = 4;
	localparam [31:0] pp_pkg_PP_N_CTRL_C = 16;
	localparam [31:0] pp_pkg_PP_N_IF_C = 1;
	localparam [31:0] pp_pkg_PP_N_STREAM_IN_C = 8;
	localparam [31:0] pp_pkg_PP_N_STREAM_OUT_C = 8;
	localparam [31:0] pp_pkg_PP_MAAP_SLOTS_C = 2;
	localparam [31:0] pp_pkg_PP_SINGLETON_SLOTS_C = 5;
	localparam [31:0] pp_pkg_PP_SRP_CAD_SLOTS_C = 7;
	function automatic [415:0] pp_pkg_pp_timer_map;
		input reg [31:0] n_if;
		input reg [31:0] si;
		input reg [31:0] so;
		input reg [31:0] n_ctrl;
		input reg [31:0] ca_pool;
		reg [415:0] m;
		begin
			m[415-:32] = 32'd0;
			m[383-:32] = m[415-:32] + n_if;
			m[351-:32] = m[383-:32] + si;
			m[319-:32] = m[351-:32] + si;
			m[287-:32] = m[319-:32] + so;
			m[255-:32] = m[287-:32] + ((32'd2 * n_ctrl) * n_if);
			m[223-:32] = m[255-:32] + ca_pool;
			m[191-:32] = m[223-:32] + pp_pkg_PP_SINGLETON_SLOTS_C;
			m[159-:32] = m[191-:32] + pp_pkg_PP_MAAP_SLOTS_C;
			m[127-:32] = m[159-:32];
			m[95-:32] = m[127-:32] + pp_pkg_PP_SRP_CAD_SLOTS_C;
			m[63-:32] = m[95-:32] + so;
			m[31-:32] = m[127-:32] + (((pp_pkg_PP_SRP_CAD_SLOTS_C + si) + so) * n_if);
			pp_pkg_pp_timer_map = m;
		end
	endfunction
	function automatic [31:0] pp_pkg_pp_timer_slots;
		input reg [31:0] n_if;
		input reg [31:0] si;
		input reg [31:0] so;
		input reg [31:0] n_ctrl;
		input reg [31:0] ca_pool;
		input reg en_srp;
		reg [415:0] m;
		begin
			m = pp_pkg_pp_timer_map(n_if, si, so, n_ctrl, ca_pool);
			pp_pkg_pp_timer_slots = (en_srp ? m[31-:32] : m[159-:32]);
		end
	endfunction
	localparam [31:0] pp_pkg_PP_TIMER_SLOTS_C = pp_pkg_pp_timer_slots(pp_pkg_PP_N_IF_C, pp_pkg_PP_N_STREAM_IN_C, pp_pkg_PP_N_STREAM_OUT_C, pp_pkg_PP_N_CTRL_C, pp_pkg_PP_CA_POOL_C, 1'b1);
	parameter [31:0] TMR_SLOTS_P = pp_pkg_PP_TIMER_SLOTS_C;
	parameter [31:0] TMR_SLOT_BASE_P = 61;
	parameter [7:0] TMR_OWNER_BASE_P = 8'h90;
	parameter [31:0] TX_STD_SLOTS_P = 4;
	parameter [31:0] TX_OVERSIZE_BYTES_P = 1600;
	localparam [31:0] SRC_W_C = (N_SRC_P > 32'd1 ? $clog2(N_SRC_P) : 32'd1);
	localparam [31:0] TMR_AW_C = (TMR_SLOTS_P > 32'd1 ? $clog2(TMR_SLOTS_P) : 32'd1);
	localparam [31:0] TXS_SLOT_W_C = $clog2(TX_STD_SLOTS_P + 1);
	localparam [31:0] TXS_LEN_W_C = $clog2(TX_OVERSIZE_BYTES_P + 1);
	input wire clk_i;
	input wire rst_n;
	input wire cfg_en_i;
	input wire [7:0] cfg_count_i;
	input wire [15:0] cfg_seed_offset_i;
	input wire cfg_seed_valid_i;
	input wire [47:0] own_mac_i;
	input wire link_up_i;
	input wire txn_valid_i;
	localparam [31:0] pp_pkg_PP_TXN_W_C = 393;
	input wire [392:0] txn_i;
	output wire txn_ready_o;
	output wire rxs_free_o;
	output wire [2:0] rxs_free_slot_o;
	output wire prng_draw_req_o;
	output wire [2:0] prng_draw_kind_o;
	input wire prng_draw_busy_i;
	input wire prng_draw_valid_i;
	input wire [15:0] prng_draw_ms_i;
	input wire [31:0] now_ms_i;
	output wire tmr_arm_valid_o;
	output wire tmr_arm_cancel_o;
	output wire [TMR_AW_C - 1:0] tmr_arm_slot_o;
	localparam [31:0] pp_pkg_PP_TIMER_OWNER_W_C = 8;
	output wire [7:0] tmr_arm_owner_o;
	output wire [31:0] tmr_arm_deadline_ms_o;
	input wire tmr_exp_valid_i;
	input wire [TMR_AW_C - 1:0] tmr_exp_slot_i;
	input wire [7:0] tmr_exp_owner_i;
	output wire txs_alloc_req_o;
	output wire txs_oversize_o;
	input wire txs_alloc_gnt_i;
	input wire [TXS_SLOT_W_C - 1:0] txs_alloc_slot_i;
	output wire [TXS_SLOT_W_C - 1:0] txs_wr_slot_o;
	output wire [TXS_LEN_W_C - 1:0] txs_wr_addr_o;
	output wire txs_wr_valid_o;
	output wire [7:0] txs_wr_data_o;
	output wire txs_wr_commit_o;
	output wire [TXS_LEN_W_C - 1:0] txs_wr_len_o;
	output wire txreq_valid_o;
	output wire [TXS_SLOT_W_C - 1:0] txreq_slot_o;
	input wire txreq_ready_i;
	input wire alloc_req_valid_i;
	output wire alloc_req_ready_o;
	input wire alloc_req_release_i;
	input wire [SRC_W_C - 1:0] alloc_req_src_i;
	output wire alloc_rsp_valid_o;
	output wire alloc_rsp_ok_o;
	output wire [47:0] alloc_rsp_da_o;
	output wire conflict_valid_o;
	output reg [SRC_W_C - 1:0] conflict_src_o;
	input wire conflict_ack_i;
	output wire [47:0] addr_o;
	output wire addr_valid_o;
	output wire [1:0] state_o;
	output wire [7:0] conflicts_o;
	output wire [7:0] defends_o;
	localparam [31:0] POOL_HI_C = 32'h91e0f000;
	localparam [15:0] POOL_SIZE_C = 16'hfe00;
	localparam [47:0] MAAP_DST_C = 48'h91e0f000ff00;
	localparam [15:0] ETHERTYPE_C = 16'h22f0;
	localparam [7:0] SUBTYPE_C = 8'hfe;
	localparam [3:0] MSG_PROBE_C = 4'd1;
	localparam [3:0] MSG_DEFEND_C = 4'd2;
	localparam [3:0] MSG_ANNOUNCE_C = 4'd3;
	localparam [4:0] MAAP_VER_C = 5'd1;
	localparam [10:0] MAAP_CDL_C = 11'd16;
	localparam [1:0] PROBE_RETX_C = 2'd3;
	localparam [31:0] FRAME_BYTES_C = 60;
	localparam [2:0] KIND_PROBE_C = 3'd5;
	localparam [2:0] KIND_ANNOUNCE_C = 3'd6;
	localparam [2:0] KIND_ADDR_C = 3'd7;
	wire [392:0] txn_in_w;
	function automatic [392:0] sv2v_cast_393;
		input reg [392:0] inp;
		sv2v_cast_393 = inp;
	endfunction
	assign txn_in_w = sv2v_cast_393(txn_i);
	function automatic [7:0] byte48_f;
		input reg [47:0] v;
		input reg [31:0] n;
		reg [47:0] sh;
		begin
			sh = v >> (8 * (5 - n));
			byte48_f = sh[7:0];
		end
	endfunction
	function automatic [7:0] byte16_f;
		input reg [15:0] v;
		input reg [31:0] n;
		reg [15:0] sh;
		begin
			sh = v >> (8 * (1 - n));
			byte16_f = sh[7:0];
		end
	endfunction
	function automatic [47:0] rev48_f;
		input reg [47:0] m;
		rev48_f = {m[7:0], m[15:8], m[23:16], m[31:24], m[39:32], m[47:40]};
	endfunction
	reg [1:0] pstate_r;
	reg [15:0] offset_r;
	reg [1:0] probe_left_r;
	reg seed_used_r;
	reg [7:0] conflicts_r;
	reg [7:0] defends_r;
	assign state_o = pstate_r;
	assign addr_o = {POOL_HI_C, offset_r};
	assign addr_valid_o = pstate_r == 2'd2;
	assign conflicts_o = conflicts_r;
	assign defends_o = defends_r;
	wire eng_w;
	reg eng_q_r;
	assign eng_w = (cfg_en_i && link_up_i) && (cfg_count_i != 8'd0);
	wire [48:0] our_lo_w;
	wire [48:0] our_hi_w;
	assign our_lo_w = {1'b0, POOL_HI_C, offset_r};
	assign our_hi_w = (our_lo_w + {41'd0, cfg_count_i}) - 49'd1;
	wire exp_probe_w;
	wire exp_ann_w;
	function automatic [31:0] sv2v_cast_32;
		input reg [31:0] inp;
		sv2v_cast_32 = inp;
	endfunction
	assign exp_probe_w = tmr_exp_valid_i && (sv2v_cast_32(tmr_exp_slot_i) == TMR_SLOT_BASE_P);
	assign exp_ann_w = tmr_exp_valid_i && (sv2v_cast_32(tmr_exp_slot_i) == (TMR_SLOT_BASE_P + 32'd1));
	reg pend_probe_exp_r;
	reg pend_ann_exp_r;
	reg [3:0] w_st_r;
	reg ival_ann_r;
	reg [3:0] send_msg_r;
	reg chain_ann_r;
	reg teardown_ph_r;
	reg draw_act_r;
	reg draw_req_r;
	reg [2:0] draw_kind_r;
	reg [TXS_SLOT_W_C - 1:0] bld_slot_r;
	reg [5:0] bld_idx_r;
	reg [3:0] rxm_msg_r;
	reg [47:0] rxm_sa_r;
	reg [47:0] rxm_req_start_r;
	reg [15:0] rxm_req_cnt_r;
	reg [47:0] rxm_conf_start_r;
	reg [15:0] rxm_conf_cnt_r;
	reg [47:0] def_da_r;
	reg [47:0] def_req_start_r;
	reg [15:0] def_req_cnt_r;
	reg [47:0] def_conf_start_r;
	reg [15:0] def_conf_cnt_r;
	wire [48:0] req_lo_w;
	wire [48:0] req_hi_w;
	wire [48:0] conf_lo_w;
	wire [48:0] conf_hi_w;
	wire ovl_req_w;
	wire ovl_conf_w;
	assign req_lo_w = {1'b0, rxm_req_start_r};
	assign req_hi_w = (req_lo_w + {33'd0, rxm_req_cnt_r}) - 49'd1;
	assign conf_lo_w = {1'b0, rxm_conf_start_r};
	assign conf_hi_w = (conf_lo_w + {33'd0, rxm_conf_cnt_r}) - 49'd1;
	assign ovl_req_w = ((rxm_req_cnt_r != 16'd0) && (req_lo_w <= our_hi_w)) && (our_lo_w <= req_hi_w);
	assign ovl_conf_w = ((rxm_conf_cnt_r != 16'd0) && (conf_lo_w <= our_hi_w)) && (our_lo_w <= conf_hi_w);
	wire cmp_mac_true_w;
	assign cmp_mac_true_w = rev48_f(own_mac_i) < rev48_f(rxm_sa_r);
	wire [48:0] isect_lo_w;
	wire [48:0] isect_hi_w;
	assign isect_lo_w = (req_lo_w > our_lo_w ? req_lo_w : our_lo_w);
	assign isect_hi_w = (req_hi_w < our_hi_w ? req_hi_w : our_hi_w);
	reg ev_hit_w;
	reg act_defend_w;
	reg act_yield_w;
	always @(*) begin : row_decode
		if (_sv2v_0)
			;
		ev_hit_w = 1'b0;
		act_defend_w = 1'b0;
		act_yield_w = 1'b0;
		if (rxm_msg_r == MSG_PROBE_C) begin
			ev_hit_w = ovl_req_w;
			if (ev_hit_w && (pstate_r == 2'd1))
				act_yield_w = !cmp_mac_true_w;
			else if (ev_hit_w && (pstate_r == 2'd2))
				act_defend_w = 1'b1;
		end
		else if ((rxm_msg_r == MSG_DEFEND_C) || (rxm_msg_r == MSG_ANNOUNCE_C)) begin
			ev_hit_w = ovl_req_w || ovl_conf_w;
			if (ev_hit_w && (pstate_r == 2'd1))
				act_yield_w = 1'b1;
			else if (ev_hit_w && (pstate_r == 2'd2))
				act_yield_w = !cmp_mac_true_w;
		end
	end
	function automatic [7:0] frame_byte_f;
		input reg [5:0] idx;
		input reg [3:0] msg;
		input reg [15:0] off;
		input reg [7:0] cnt;
		input reg [47:0] dda;
		input reg [47:0] ereq_s;
		input reg [15:0] ereq_c;
		input reg [47:0] econ_s;
		input reg [15:0] econ_c;
		reg [31:0] i;
		reg [7:0] b;
		reg dfd;
		reg [47:0] req_s;
		reg [15:0] req_c;
		begin
			i = sv2v_cast_32(idx);
			dfd = msg == MSG_DEFEND_C;
			req_s = (dfd ? ereq_s : {POOL_HI_C, off});
			req_c = (dfd ? ereq_c : {8'd0, cnt});
			b = 8'h00;
			if (i < 6)
				b = byte48_f((dfd ? dda : MAAP_DST_C), i);
			else if (i < 12)
				b = byte48_f(own_mac_i, i - 6);
			else if (i < 14)
				b = byte16_f(ETHERTYPE_C, i - 12);
			else if (i == 14)
				b = SUBTYPE_C;
			else if (i == 15)
				b = {4'b0000, msg};
			else if (i == 16)
				b = {MAAP_VER_C, MAAP_CDL_C[10:8]};
			else if (i == 17)
				b = MAAP_CDL_C[7:0];
			else if ((i >= 26) && (i < 32))
				b = byte48_f(req_s, i - 26);
			else if ((i >= 32) && (i < 34))
				b = byte16_f(req_c, i - 32);
			else if ((dfd && (i >= 34)) && (i < 40))
				b = byte48_f(econ_s, i - 34);
			else if ((dfd && (i >= 40)) && (i < 42))
				b = byte16_f(econ_c, i - 40);
			frame_byte_f = b;
		end
	endfunction
	assign txs_wr_slot_o = bld_slot_r;
	function automatic [TXS_LEN_W_C - 1:0] sv2v_cast_EFC2D;
		input reg [TXS_LEN_W_C - 1:0] inp;
		sv2v_cast_EFC2D = inp;
	endfunction
	assign txs_wr_addr_o = sv2v_cast_EFC2D(bld_idx_r);
	assign txs_wr_valid_o = w_st_r == 4'd6;
	assign txs_wr_data_o = frame_byte_f(bld_idx_r, send_msg_r, offset_r, cfg_count_i, def_da_r, def_req_start_r, def_req_cnt_r, def_conf_start_r, def_conf_cnt_r);
	assign txs_wr_commit_o = w_st_r == 4'd7;
	assign txs_wr_len_o = sv2v_cast_EFC2D(FRAME_BYTES_C);
	assign txs_alloc_req_o = w_st_r == 4'd4;
	assign txs_oversize_o = 1'b0;
	assign txreq_valid_o = w_st_r == 4'd8;
	assign txreq_slot_o = bld_slot_r;
	reg arm_v_r;
	reg arm_c_r;
	reg arm_ann_r;
	reg [31:0] arm_dl_r;
	assign tmr_arm_valid_o = arm_v_r;
	assign tmr_arm_cancel_o = arm_c_r;
	function automatic [TMR_AW_C - 1:0] sv2v_cast_5A563;
		input reg [TMR_AW_C - 1:0] inp;
		sv2v_cast_5A563 = inp;
	endfunction
	assign tmr_arm_slot_o = sv2v_cast_5A563(TMR_SLOT_BASE_P + (arm_ann_r ? 32'd1 : 32'd0));
	assign tmr_arm_owner_o = TMR_OWNER_BASE_P + {7'd0, arm_ann_r};
	assign tmr_arm_deadline_ms_o = arm_dl_r;
	assign prng_draw_req_o = draw_req_r;
	assign prng_draw_kind_o = draw_kind_r;
	assign txn_ready_o = ((w_st_r == 4'd1) || (w_st_r == 4'd0)) && txn_valid_i;
	localparam [2:0] pp_pkg_PP_SLOT_NULL_C = 3'd7;
	assign rxs_free_o = (txn_ready_o && (txn_in_w[59-:3] != pp_pkg_PP_SLOT_NULL_C)) && (sv2v_cast_32(txn_in_w[59-:3]) < RX_SLOTS_P);
	assign rxs_free_slot_o = txn_in_w[59-:3];
	function automatic [15:0] sv2v_cast_16;
		input reg [15:0] inp;
		sv2v_cast_16 = inp;
	endfunction
	always @(posedge clk_i) begin : walker
		if (!rst_n) begin
			pstate_r <= 2'd0;
			offset_r <= 16'd0;
			probe_left_r <= 2'd0;
			seed_used_r <= 1'b0;
			conflicts_r <= 8'd0;
			defends_r <= 8'd0;
			eng_q_r <= 1'b0;
			pend_probe_exp_r <= 1'b0;
			pend_ann_exp_r <= 1'b0;
			w_st_r <= 4'd0;
			ival_ann_r <= 1'b0;
			send_msg_r <= 4'd0;
			chain_ann_r <= 1'b0;
			teardown_ph_r <= 1'b0;
			draw_act_r <= 1'b0;
			draw_req_r <= 1'b0;
			draw_kind_r <= 3'd0;
			bld_slot_r <= 1'sb0;
			bld_idx_r <= 6'd0;
			rxm_msg_r <= 4'd0;
			rxm_sa_r <= 48'd0;
			rxm_req_start_r <= 48'd0;
			rxm_req_cnt_r <= 16'd0;
			rxm_conf_start_r <= 48'd0;
			rxm_conf_cnt_r <= 16'd0;
			def_da_r <= 48'd0;
			def_req_start_r <= 48'd0;
			def_req_cnt_r <= 16'd0;
			def_conf_start_r <= 48'd0;
			def_conf_cnt_r <= 16'd0;
			arm_v_r <= 1'b0;
			arm_c_r <= 1'b0;
			arm_ann_r <= 1'b0;
			arm_dl_r <= 32'd0;
		end
		else begin
			arm_v_r <= 1'b0;
			draw_req_r <= 1'b0;
			eng_q_r <= eng_w;
			if (exp_probe_w)
				pend_probe_exp_r <= 1'b1;
			if (exp_ann_w)
				pend_ann_exp_r <= 1'b1;
			(* full_case, parallel_case *)
			case (w_st_r)
				4'd0: begin
					pstate_r <= 2'd0;
					if (eng_w && !eng_q_r)
						w_st_r <= 4'd2;
				end
				4'd2:
					if (!eng_w)
						w_st_r <= 4'd0;
					else if (cfg_seed_valid_i && !seed_used_r) begin
						offset_r <= (cfg_seed_offset_i > (POOL_SIZE_C - {8'd0, cfg_count_i}) ? POOL_SIZE_C - {8'd0, cfg_count_i} : cfg_seed_offset_i);
						seed_used_r <= 1'b1;
						probe_left_r <= PROBE_RETX_C;
						ival_ann_r <= 1'b0;
						w_st_r <= 4'd3;
					end
					else if (draw_act_r) begin
						if (prng_draw_valid_i) begin
							draw_act_r <= 1'b0;
							if (prng_draw_ms_i <= (POOL_SIZE_C - {8'd0, cfg_count_i})) begin
								offset_r <= prng_draw_ms_i;
								probe_left_r <= PROBE_RETX_C;
								ival_ann_r <= 1'b0;
								w_st_r <= 4'd3;
							end
						end
					end
					else if (!prng_draw_busy_i && !draw_req_r) begin
						draw_req_r <= 1'b1;
						draw_kind_r <= KIND_ADDR_C;
						draw_act_r <= 1'b1;
					end
				4'd3:
					if (draw_act_r) begin
						if (prng_draw_valid_i) begin
							draw_act_r <= 1'b0;
							arm_v_r <= 1'b1;
							arm_c_r <= 1'b0;
							arm_ann_r <= ival_ann_r;
							arm_dl_r <= now_ms_i + {16'd0, prng_draw_ms_i};
							if (ival_ann_r) begin
								pend_ann_exp_r <= 1'b0;
								send_msg_r <= MSG_ANNOUNCE_C;
							end
							else begin
								pend_probe_exp_r <= 1'b0;
								send_msg_r <= MSG_PROBE_C;
							end
							w_st_r <= 4'd4;
						end
					end
					else if (!prng_draw_busy_i && !draw_req_r) begin
						draw_req_r <= 1'b1;
						draw_kind_r <= (ival_ann_r ? KIND_ANNOUNCE_C : KIND_PROBE_C);
						draw_act_r <= 1'b1;
					end
				4'd4: w_st_r <= 4'd5;
				4'd5:
					if (txs_alloc_gnt_i) begin
						bld_slot_r <= txs_alloc_slot_i;
						bld_idx_r <= 6'd0;
						w_st_r <= 4'd6;
					end
					else
						w_st_r <= 4'd4;
				4'd6:
					if (sv2v_cast_32(bld_idx_r) == 59)
						w_st_r <= 4'd7;
					else
						bld_idx_r <= bld_idx_r + 6'd1;
				4'd7: w_st_r <= 4'd8;
				4'd8:
					if (txreq_ready_i)
						w_st_r <= 4'd9;
				4'd9: begin
					w_st_r <= 4'd1;
					if (send_msg_r == MSG_PROBE_C) begin
						if (pstate_r != 2'd1)
							pstate_r <= 2'd1;
						if (chain_ann_r) begin
							chain_ann_r <= 1'b0;
							ival_ann_r <= 1'b1;
							w_st_r <= 4'd3;
						end
					end
					else if (send_msg_r == MSG_ANNOUNCE_C)
						pstate_r <= 2'd2;
				end
				4'd1:
					if (!eng_w) begin
						pstate_r <= 2'd0;
						seed_used_r <= 1'b0;
						teardown_ph_r <= 1'b0;
						w_st_r <= 4'd11;
					end
					else if (txn_valid_i) begin
						rxm_msg_r <= txn_in_w[353-:4];
						rxm_sa_r <= txn_in_w[333-:48];
						rxm_req_start_r <= txn_in_w[285:238];
						rxm_req_cnt_r <= txn_in_w[237:222];
						rxm_conf_start_r <= {txn_in_w[123-:16], txn_in_w[107-:16], txn_in_w[91-:16]};
						rxm_conf_cnt_r <= txn_in_w[75-:16];
						w_st_r <= 4'd10;
					end
					else if (pend_probe_exp_r) begin
						pend_probe_exp_r <= 1'b0;
						if (pstate_r == 2'd1) begin
							if (probe_left_r == 2'd1)
								chain_ann_r <= 1'b1;
							probe_left_r <= probe_left_r - 2'd1;
							if (probe_left_r == 2'd1) begin
								send_msg_r <= MSG_PROBE_C;
								w_st_r <= 4'd4;
							end
							else begin
								ival_ann_r <= 1'b0;
								w_st_r <= 4'd3;
							end
						end
					end
					else if (pend_ann_exp_r) begin
						pend_ann_exp_r <= 1'b0;
						if (pstate_r == 2'd2) begin
							ival_ann_r <= 1'b1;
							w_st_r <= 4'd3;
						end
					end
					else if (pstate_r == 2'd0)
						w_st_r <= 4'd2;
				4'd10: begin
					w_st_r <= 4'd1;
					if ((pstate_r != 2'd0) && eng_w) begin
						if (act_defend_w) begin
							def_da_r <= rxm_sa_r;
							def_req_start_r <= rxm_req_start_r;
							def_req_cnt_r <= rxm_req_cnt_r;
							def_conf_start_r <= isect_lo_w[47:0];
							def_conf_cnt_r <= sv2v_cast_16(isect_hi_w - isect_lo_w) + 16'd1;
							defends_r <= (&defends_r ? defends_r : defends_r + 8'd1);
							send_msg_r <= MSG_DEFEND_C;
							w_st_r <= 4'd4;
						end
						else if (act_yield_w) begin
							arm_v_r <= 1'b1;
							arm_c_r <= 1'b1;
							arm_ann_r <= pstate_r == 2'd2;
							if (pstate_r == 2'd2)
								pend_ann_exp_r <= 1'b0;
							else
								pend_probe_exp_r <= 1'b0;
							pstate_r <= 2'd0;
							conflicts_r <= (&conflicts_r ? conflicts_r : conflicts_r + 8'd1);
							w_st_r <= 4'd2;
						end
					end
				end
				4'd11: begin
					arm_v_r <= 1'b1;
					arm_c_r <= 1'b1;
					arm_ann_r <= teardown_ph_r;
					teardown_ph_r <= 1'b1;
					if (!teardown_ph_r)
						pend_probe_exp_r <= 1'b0;
					else begin
						pend_ann_exp_r <= 1'b0;
						w_st_r <= 4'd0;
					end
				end
				default: w_st_r <= 4'd0;
			endcase
		end
	end
	wire [7:0] src8_w;
	function automatic [7:0] sv2v_cast_8;
		input reg [7:0] inp;
		sv2v_cast_8 = inp;
	endfunction
	assign src8_w = sv2v_cast_8(alloc_req_src_i);
	wire in_block_w;
	assign in_block_w = addr_valid_o && (src8_w < cfg_count_i);
	wire [15:0] grant_off_w;
	wire [47:0] grant_da_w;
	assign grant_off_w = offset_r + {{16 - SRC_W_C {1'b0}}, alloc_req_src_i};
	assign grant_da_w = {POOL_HI_C, grant_off_w};
	assign alloc_req_ready_o = ~alloc_rsp_valid_o;
	reg rsp_valid_r;
	reg rsp_ok_r;
	reg [47:0] rsp_da_r;
	assign alloc_rsp_valid_o = rsp_valid_r;
	assign alloc_rsp_ok_o = rsp_ok_r;
	assign alloc_rsp_da_o = rsp_da_r;
	wire grant_w;
	assign grant_w = ~alloc_req_release_i & in_block_w;
	always @(posedge clk_i) begin : rsp_path
		if (!rst_n) begin
			rsp_valid_r <= 1'b0;
			rsp_ok_r <= 1'b0;
			rsp_da_r <= 48'd0;
		end
		else begin
			rsp_valid_r <= 1'b0;
			if (alloc_req_valid_i & alloc_req_ready_o) begin
				rsp_valid_r <= 1'b1;
				rsp_ok_r <= grant_w;
				rsp_da_r <= (grant_w ? grant_da_w : 48'd0);
			end
		end
	end
	reg blk_valid_q_r;
	reg [15:0] blk_off_q_r;
	reg [7:0] blk_cnt_q_r;
	wire moved_w;
	assign moved_w = blk_valid_q_r && ((!addr_valid_o || (offset_r != blk_off_q_r)) || (cfg_count_i != blk_cnt_q_r));
	reg [N_SRC_P - 1:0] confl_pend_r;
	assign conflict_valid_o = |confl_pend_r;
	function automatic [SRC_W_C - 1:0] sv2v_cast_14954;
		input reg [SRC_W_C - 1:0] inp;
		sv2v_cast_14954 = inp;
	endfunction
	always @(*) begin : confl_pick
		if (_sv2v_0)
			;
		conflict_src_o = 1'sb0;
		begin : sv2v_autoblock_1
			reg [31:0] i;
			for (i = N_SRC_P; i > 0; i = i - 1)
				if (confl_pend_r[i - 1])
					conflict_src_o = sv2v_cast_14954(i - 1);
		end
	end
	always @(posedge clk_i) begin : confl_path
		if (!rst_n) begin
			blk_valid_q_r <= 1'b0;
			blk_off_q_r <= 16'd0;
			blk_cnt_q_r <= 8'd0;
			confl_pend_r <= 1'sb0;
		end
		else begin
			blk_valid_q_r <= addr_valid_o;
			blk_off_q_r <= offset_r;
			blk_cnt_q_r <= cfg_count_i;
			if (moved_w)
				confl_pend_r <= 1'sb1;
			else if (conflict_valid_o & conflict_ack_i)
				confl_pend_r[conflict_src_o] <= 1'b0;
		end
	end
	wire unused_owner_w;
	assign unused_owner_w = ^tmr_exp_owner_i;
	initial _sv2v_0 = 0;
endmodule
`default_nettype wire
`default_nettype none
module KL_pp_dispatch (
	clk_i,
	rst_n,
	enq_valid_i,
	enq_txn_i,
	enq_ready_o,
	adp_txn_valid_o,
	adp_txn_o,
	adp_txn_ready_i,
	acmp_txn_valid_o,
	acmp_txn_o,
	acmp_txn_ready_i,
	aecp_txn_valid_o,
	aecp_txn_o,
	aecp_txn_ready_i,
	maap_txn_valid_o,
	maap_txn_o,
	maap_txn_ready_i,
	adp_level_o,
	acmp_level_o,
	aecp_level_o,
	maap_level_o,
	adp_stall_count_o,
	acmp_stall_count_o,
	aecp_stall_count_o,
	maap_stall_count_o
);
	parameter [31:0] ADP_DEPTH_P = 4;
	parameter [31:0] ACMP_DEPTH_P = 4;
	parameter [31:0] AECP_DEPTH_P = 4;
	parameter [31:0] MAAP_DEPTH_P = 2;
	input wire clk_i;
	input wire rst_n;
	input wire enq_valid_i;
	localparam [31:0] pp_pkg_PP_TXN_W_C = 393;
	input wire [392:0] enq_txn_i;
	output wire enq_ready_o;
	output wire adp_txn_valid_o;
	output wire [392:0] adp_txn_o;
	input wire adp_txn_ready_i;
	output wire acmp_txn_valid_o;
	output wire [392:0] acmp_txn_o;
	input wire acmp_txn_ready_i;
	output wire aecp_txn_valid_o;
	output wire [392:0] aecp_txn_o;
	input wire aecp_txn_ready_i;
	output wire maap_txn_valid_o;
	output wire [392:0] maap_txn_o;
	input wire maap_txn_ready_i;
	output wire [7:0] adp_level_o;
	output wire [7:0] acmp_level_o;
	output wire [7:0] aecp_level_o;
	output wire [7:0] maap_level_o;
	output wire [15:0] adp_stall_count_o;
	output wire [15:0] acmp_stall_count_o;
	output wire [15:0] aecp_stall_count_o;
	output wire [15:0] maap_stall_count_o;
	localparam [15:0] STALL_MAX_C = 16'hffff;
	wire [392:0] enq_txn_w;
	wire sel_adp_w;
	wire sel_acmp_w;
	wire sel_maap_w;
	wire sel_aecp_w;
	function automatic [392:0] sv2v_cast_393;
		input reg [392:0] inp;
		sv2v_cast_393 = inp;
	endfunction
	assign enq_txn_w = sv2v_cast_393(enq_txn_i);
	assign sel_adp_w = enq_txn_w[356-:3] == 3'd0;
	assign sel_acmp_w = enq_txn_w[356-:3] == 3'd1;
	assign sel_maap_w = enq_txn_w[356-:3] == 3'd5;
	assign sel_aecp_w = (!sel_adp_w && !sel_acmp_w) && !sel_maap_w;
	wire adp_full_w;
	wire acmp_full_w;
	wire aecp_full_w;
	wire maap_full_w;
	assign enq_ready_o = (((sel_adp_w && !adp_full_w) || (sel_acmp_w && !acmp_full_w)) || (sel_maap_w && !maap_full_w)) || (sel_aecp_w && !aecp_full_w);
	KL_pp_dispatch_fifo #(.DEPTH_P(ADP_DEPTH_P)) u_adp_q(
		.clk_i(clk_i),
		.rst_n(rst_n),
		.push_i(enq_valid_i && sel_adp_w),
		.wdata_i(enq_txn_i),
		.full_o(adp_full_w),
		.pop_valid_o(adp_txn_valid_o),
		.pop_data_o(adp_txn_o),
		.pop_ready_i(adp_txn_ready_i),
		.level_o(adp_level_o)
	);
	KL_pp_dispatch_fifo #(.DEPTH_P(ACMP_DEPTH_P)) u_acmp_q(
		.clk_i(clk_i),
		.rst_n(rst_n),
		.push_i(enq_valid_i && sel_acmp_w),
		.wdata_i(enq_txn_i),
		.full_o(acmp_full_w),
		.pop_valid_o(acmp_txn_valid_o),
		.pop_data_o(acmp_txn_o),
		.pop_ready_i(acmp_txn_ready_i),
		.level_o(acmp_level_o)
	);
	KL_pp_dispatch_fifo #(.DEPTH_P(AECP_DEPTH_P)) u_aecp_q(
		.clk_i(clk_i),
		.rst_n(rst_n),
		.push_i(enq_valid_i && sel_aecp_w),
		.wdata_i(enq_txn_i),
		.full_o(aecp_full_w),
		.pop_valid_o(aecp_txn_valid_o),
		.pop_data_o(aecp_txn_o),
		.pop_ready_i(aecp_txn_ready_i),
		.level_o(aecp_level_o)
	);
	KL_pp_dispatch_fifo #(.DEPTH_P(MAAP_DEPTH_P)) u_maap_q(
		.clk_i(clk_i),
		.rst_n(rst_n),
		.push_i(enq_valid_i && sel_maap_w),
		.wdata_i(enq_txn_i),
		.full_o(maap_full_w),
		.pop_valid_o(maap_txn_valid_o),
		.pop_data_o(maap_txn_o),
		.pop_ready_i(maap_txn_ready_i),
		.level_o(maap_level_o)
	);
	reg [15:0] adp_stall_r;
	reg [15:0] acmp_stall_r;
	reg [15:0] aecp_stall_r;
	reg [15:0] maap_stall_r;
	always @(posedge clk_i) begin : stall_counters
		if (!rst_n) begin
			adp_stall_r <= 1'sb0;
			acmp_stall_r <= 1'sb0;
			aecp_stall_r <= 1'sb0;
			maap_stall_r <= 1'sb0;
		end
		else begin
			if (((enq_valid_i && sel_adp_w) && adp_full_w) && (adp_stall_r != STALL_MAX_C))
				adp_stall_r <= adp_stall_r + 16'd1;
			if (((enq_valid_i && sel_acmp_w) && acmp_full_w) && (acmp_stall_r != STALL_MAX_C))
				acmp_stall_r <= acmp_stall_r + 16'd1;
			if (((enq_valid_i && sel_aecp_w) && aecp_full_w) && (aecp_stall_r != STALL_MAX_C))
				aecp_stall_r <= aecp_stall_r + 16'd1;
			if (((enq_valid_i && sel_maap_w) && maap_full_w) && (maap_stall_r != STALL_MAX_C))
				maap_stall_r <= maap_stall_r + 16'd1;
		end
	end
	assign adp_stall_count_o = adp_stall_r;
	assign acmp_stall_count_o = acmp_stall_r;
	assign aecp_stall_count_o = aecp_stall_r;
	assign maap_stall_count_o = maap_stall_r;
endmodule
module KL_pp_dispatch_fifo (
	clk_i,
	rst_n,
	push_i,
	wdata_i,
	full_o,
	pop_valid_o,
	pop_data_o,
	pop_ready_i,
	level_o
);
	parameter [31:0] DEPTH_P = 4;
	localparam [31:0] PTR_W_C = (DEPTH_P > 1 ? $clog2(DEPTH_P) : 1);
	localparam [31:0] CNT_W_C = $clog2(DEPTH_P + 1);
	input wire clk_i;
	input wire rst_n;
	input wire push_i;
	localparam [31:0] pp_pkg_PP_TXN_W_C = 393;
	input wire [392:0] wdata_i;
	output wire full_o;
	output wire pop_valid_o;
	output wire [392:0] pop_data_o;
	input wire pop_ready_i;
	output wire [7:0] level_o;
	reg [PTR_W_C - 1:0] wr_ptr_r;
	reg [PTR_W_C - 1:0] rd_ptr_r;
	reg [CNT_W_C - 1:0] cnt_r;
	reg out_valid_r;
	wire push_w;
	wire rd_en_w;
	function automatic [CNT_W_C - 1:0] sv2v_cast_7417F;
		input reg [CNT_W_C - 1:0] inp;
		sv2v_cast_7417F = inp;
	endfunction
	assign full_o = cnt_r == sv2v_cast_7417F(DEPTH_P);
	assign push_w = push_i && !full_o;
	assign rd_en_w = (cnt_r != {CNT_W_C {1'sb0}}) && (!out_valid_r || pop_ready_i);
	function automatic [PTR_W_C - 1:0] sv2v_cast_2FDC0;
		input reg [PTR_W_C - 1:0] inp;
		sv2v_cast_2FDC0 = inp;
	endfunction
	function automatic signed [PTR_W_C - 1:0] sv2v_cast_2FDC0_signed;
		input reg signed [PTR_W_C - 1:0] inp;
		sv2v_cast_2FDC0_signed = inp;
	endfunction
	function automatic signed [CNT_W_C - 1:0] sv2v_cast_7417F_signed;
		input reg signed [CNT_W_C - 1:0] inp;
		sv2v_cast_7417F_signed = inp;
	endfunction
	always @(posedge clk_i) begin : fifo_ctrl
		if (!rst_n) begin
			wr_ptr_r <= 1'sb0;
			rd_ptr_r <= 1'sb0;
			cnt_r <= 1'sb0;
			out_valid_r <= 1'b0;
		end
		else begin
			if (push_w)
				wr_ptr_r <= (wr_ptr_r == sv2v_cast_2FDC0(DEPTH_P - 1) ? {PTR_W_C {1'sb0}} : wr_ptr_r + sv2v_cast_2FDC0_signed(1));
			if (rd_en_w) begin
				rd_ptr_r <= (rd_ptr_r == sv2v_cast_2FDC0(DEPTH_P - 1) ? {PTR_W_C {1'sb0}} : rd_ptr_r + sv2v_cast_2FDC0_signed(1));
				out_valid_r <= 1'b1;
			end
			else if (out_valid_r && pop_ready_i)
				out_valid_r <= 1'b0;
			case ({push_w, rd_en_w})
				2'b10: cnt_r <= cnt_r + sv2v_cast_7417F_signed(1);
				2'b01: cnt_r <= cnt_r - sv2v_cast_7417F_signed(1);
				default:
					;
			endcase
		end
	end
	(* ram_style = "distributed" *) reg [392:0] mem_r [0:DEPTH_P - 1];
	reg [392:0] out_data_r;
	always @(posedge clk_i) begin : fifo_mem_wr
		if (push_w)
			mem_r[wr_ptr_r] <= wdata_i;
	end
	always @(posedge clk_i) begin : fifo_mem_rd
		if (rd_en_w)
			out_data_r <= mem_r[rd_ptr_r];
	end
	assign pop_valid_o = out_valid_r;
	assign pop_data_o = out_data_r;
	function automatic [7:0] sv2v_cast_8;
		input reg [7:0] inp;
		sv2v_cast_8 = inp;
	endfunction
	assign level_o = sv2v_cast_8(cnt_r) + {7'h00, out_valid_r};
endmodule
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
`default_nettype none
module KL_pp_normalizer (
	clk_i,
	rst_n,
	now_ms_i,
	budget_adp_ms_i,
	budget_acmp_ms_i,
	budget_aecp_ms_i,
	rx_valid_i,
	rx_ready_o,
	rx_if_index_i,
	rx_protocol_i,
	rx_msg_type_i,
	rx_status_i,
	rx_cdl_i,
	rx_src_mac_i,
	rx_controller_eid_i,
	rx_target_eid_i,
	rx_sequence_id_i,
	rx_u_i,
	rx_cr_i,
	rx_opcode_i,
	rx_operands_i,
	rx_slot_i,
	hz_valid_o,
	hz_protocol_o,
	hz_opcode_o,
	hz_class_i,
	hz_key_i,
	tmr_valid_i,
	tmr_txn_i,
	tmr_ready_o,
	self_valid_i,
	self_txn_i,
	self_ready_o,
	mgmt_valid_i,
	mgmt_txn_i,
	mgmt_ready_o,
	txn_valid_o,
	txn_o,
	txn_ready_i
);
	reg _sv2v_0;
	input wire clk_i;
	input wire rst_n;
	input wire [31:0] now_ms_i;
	input wire [15:0] budget_adp_ms_i;
	input wire [15:0] budget_acmp_ms_i;
	input wire [15:0] budget_aecp_ms_i;
	input wire rx_valid_i;
	output wire rx_ready_o;
	input wire [1:0] rx_if_index_i;
	input wire [2:0] rx_protocol_i;
	input wire [3:0] rx_msg_type_i;
	input wire [4:0] rx_status_i;
	input wire [10:0] rx_cdl_i;
	input wire [47:0] rx_src_mac_i;
	input wire [63:0] rx_controller_eid_i;
	input wire [63:0] rx_target_eid_i;
	input wire [15:0] rx_sequence_id_i;
	input wire rx_u_i;
	input wire rx_cr_i;
	input wire [15:0] rx_opcode_i;
	input wire [63:0] rx_operands_i;
	input wire [2:0] rx_slot_i;
	output wire hz_valid_o;
	output wire [2:0] hz_protocol_o;
	output wire [15:0] hz_opcode_o;
	input wire [3:0] hz_class_i;
	input wire [15:0] hz_key_i;
	input wire tmr_valid_i;
	localparam [31:0] pp_pkg_PP_TXN_W_C = 393;
	input wire [392:0] tmr_txn_i;
	output wire tmr_ready_o;
	input wire self_valid_i;
	input wire [392:0] self_txn_i;
	output wire self_ready_o;
	input wire mgmt_valid_i;
	input wire [392:0] mgmt_txn_i;
	output wire mgmt_ready_o;
	output wire txn_valid_o;
	output wire [392:0] txn_o;
	input wire txn_ready_i;
	wire [2:0] proto_w;
	reg [15:0] budget_sel_w;
	reg [392:0] rx_txn_w;
	assign proto_w = rx_protocol_i;
	always @(*) begin : budget_sel
		if (_sv2v_0)
			;
		case (proto_w)
			3'd0: budget_sel_w = budget_adp_ms_i;
			3'd1: budget_sel_w = budget_acmp_ms_i;
			default: budget_sel_w = budget_aecp_ms_i;
		endcase
	end
	localparam [2:0] pp_pkg_PP_SLOT_NULL_C = 3'd7;
	always @(*) begin : rx_assemble
		if (_sv2v_0)
			;
		rx_txn_w[392-:2] = 2'd0;
		rx_txn_w[390-:2] = rx_if_index_i;
		rx_txn_w[388-:32] = now_ms_i;
		rx_txn_w[356-:3] = proto_w;
		rx_txn_w[353-:4] = rx_msg_type_i;
		rx_txn_w[349-:5] = rx_status_i;
		rx_txn_w[344-:11] = rx_cdl_i;
		rx_txn_w[333-:48] = rx_src_mac_i;
		rx_txn_w[285-:64] = rx_controller_eid_i;
		rx_txn_w[221-:64] = rx_target_eid_i;
		rx_txn_w[157-:16] = rx_sequence_id_i;
		rx_txn_w[141] = rx_u_i;
		rx_txn_w[140] = rx_cr_i;
		rx_txn_w[139-:16] = rx_opcode_i;
		rx_txn_w[123-:64] = rx_operands_i;
		rx_txn_w[59-:3] = rx_slot_i;
		rx_txn_w[56-:4] = hz_class_i;
		rx_txn_w[52-:16] = hz_key_i;
		rx_txn_w[36-:3] = pp_pkg_PP_SLOT_NULL_C;
		rx_txn_w[33-:32] = now_ms_i + {16'h0000, budget_sel_w};
		rx_txn_w[1-:2] = ((proto_w == 3'd0) || (proto_w == 3'd1) ? 2'd1 : 2'd0);
	end
	assign hz_valid_o = rx_valid_i;
	assign hz_protocol_o = rx_protocol_i;
	assign hz_opcode_o = rx_opcode_i;
	reg sel_valid_w;
	reg [392:0] sel_txn_w;
	function automatic [392:0] sv2v_cast_393;
		input reg [392:0] inp;
		sv2v_cast_393 = inp;
	endfunction
	always @(*) begin : producer_pick
		if (_sv2v_0)
			;
		sel_valid_w = 1'b1;
		if (rx_valid_i)
			sel_txn_w = rx_txn_w;
		else if (tmr_valid_i)
			sel_txn_w = sv2v_cast_393(tmr_txn_i);
		else if (self_valid_i)
			sel_txn_w = sv2v_cast_393(self_txn_i);
		else if (mgmt_valid_i)
			sel_txn_w = sv2v_cast_393(mgmt_txn_i);
		else begin
			sel_valid_w = 1'b0;
			sel_txn_w = sv2v_cast_393({pp_pkg_PP_TXN_W_C {1'b0}});
		end
	end
	reg [392:0] txn_r;
	reg txn_valid_r;
	wire can_load_w;
	wire accept_w;
	assign can_load_w = !txn_valid_r || txn_ready_i;
	assign accept_w = sel_valid_w && can_load_w;
	assign rx_ready_o = can_load_w && rx_valid_i;
	assign tmr_ready_o = (can_load_w && !rx_valid_i) && tmr_valid_i;
	assign self_ready_o = ((can_load_w && !rx_valid_i) && !tmr_valid_i) && self_valid_i;
	assign mgmt_ready_o = (((can_load_w && !rx_valid_i) && !tmr_valid_i) && !self_valid_i) && mgmt_valid_i;
	always @(posedge clk_i) begin : out_stage
		if (!rst_n) begin
			txn_valid_r <= 1'b0;
			txn_r <= sv2v_cast_393({pp_pkg_PP_TXN_W_C {1'b0}});
		end
		else if (accept_w) begin
			txn_r <= sel_txn_w;
			txn_valid_r <= 1'b1;
		end
		else if (txn_valid_r && txn_ready_i)
			txn_valid_r <= 1'b0;
	end
	assign txn_valid_o = txn_valid_r;
	assign txn_o = txn_r;
	initial _sv2v_0 = 0;
endmodule
`default_nettype wire
`default_nettype none
module KL_pp_nvm_port (
	clk_i,
	rst_n,
	nvm_req_i,
	nvm_we_i,
	nvm_record_id_i,
	nvm_wvalid_i,
	nvm_wready_o,
	nvm_wdata_i,
	nvm_rvalid_o,
	nvm_rready_i,
	nvm_rdata_o,
	nvm_busy_o,
	nvm_done_o,
	nvm_err_o,
	dev_req_o,
	dev_gnt_i,
	dev_op_o,
	dev_region_o,
	dev_offset_o,
	dev_len_o,
	dev_wvalid_o,
	dev_wready_i,
	dev_wdata_o,
	dev_rvalid_i,
	dev_rdata_i,
	dev_rready_o,
	dev_busy_i,
	dev_done_i,
	dev_err_i
);
	reg _sv2v_0;
	parameter [31:0] MAX_PAYLOAD_P = 1024;
	input wire clk_i;
	input wire rst_n;
	input wire nvm_req_i;
	input wire nvm_we_i;
	input wire [7:0] nvm_record_id_i;
	input wire nvm_wvalid_i;
	output wire nvm_wready_o;
	input wire [7:0] nvm_wdata_i;
	output wire nvm_rvalid_o;
	input wire nvm_rready_i;
	output wire [7:0] nvm_rdata_o;
	output wire nvm_busy_o;
	output wire nvm_done_o;
	output wire nvm_err_o;
	output wire dev_req_o;
	input wire dev_gnt_i;
	output reg [1:0] dev_op_o;
	output wire [7:0] dev_region_o;
	output reg [15:0] dev_offset_o;
	output reg [15:0] dev_len_o;
	output wire dev_wvalid_o;
	input wire dev_wready_i;
	output wire [7:0] dev_wdata_o;
	input wire dev_rvalid_i;
	input wire [7:0] dev_rdata_i;
	output wire dev_rready_o;
	input wire dev_busy_i;
	input wire dev_done_i;
	input wire dev_err_i;
	localparam [1:0] NVMP_OP_READ_C = 2'd0;
	localparam [1:0] NVMP_OP_WRITE_C = 2'd1;
	localparam [1:0] NVMP_OP_ERASE_C = 2'd2;
	localparam [7:0] MAGIC_HI_C = 8'h17;
	localparam [7:0] MAGIC_LO_C = 8'h22;
	localparam [15:0] HDR_LEN_C = 16'd8;
	function automatic [15:0] sv2v_cast_16;
		input reg [15:0] inp;
		sv2v_cast_16 = inp;
	endfunction
	localparam [15:0] MAXP_C = sv2v_cast_16(MAX_PAYLOAD_P);
	reg [3:0] state_r;
	reg err_r;
	reg [7:0] hdr_r [0:7];
	reg [2:0] hidx_r;
	reg [15:0] bcnt_r;
	reg [15:0] plen_r;
	reg [7:0] rec_r;
	reg done_seen_r;
	wire [15:0] hdr_plen_w;
	wire hdr_ok_w;
	assign hdr_plen_w = {hdr_r[4], hdr_r[5]};
	assign hdr_ok_w = ((hdr_r[0] == MAGIC_HI_C) && (hdr_r[1] == MAGIC_LO_C)) && (hdr_plen_w <= MAXP_C);
	wire dev_cmd_owned_w;
	assign dev_cmd_owned_w = ((((((((dev_req_o && dev_gnt_i) || (state_r == 4'd3)) || (state_r == 4'd5)) || (state_r == 4'd6)) || (state_r == 4'd7)) || (state_r == 4'd9)) || (state_r == 4'd10)) || (state_r == 4'd13)) || (state_r == 4'd14);
	always @(posedge clk_i) begin : nvm_port_fsm
		if (!rst_n) begin
			state_r <= 4'd0;
			err_r <= 1'b0;
			hidx_r <= 1'sb0;
			bcnt_r <= 1'sb0;
			plen_r <= 1'sb0;
			rec_r <= 1'sb0;
			done_seen_r <= 1'b0;
			begin : sv2v_autoblock_1
				reg [31:0] i;
				for (i = 0; i < 8; i = i + 1)
					hdr_r[i] <= 1'sb0;
			end
		end
		else begin
			if (dev_done_i && dev_cmd_owned_w)
				done_seen_r <= 1'b1;
			case (state_r)
				4'd0: begin
					err_r <= 1'b0;
					if (nvm_req_i) begin
						rec_r <= nvm_record_id_i;
						hidx_r <= 1'sb0;
						bcnt_r <= 1'sb0;
						done_seen_r <= 1'b0;
						state_r <= (nvm_we_i ? 4'd1 : 4'd8);
					end
				end
				4'd1:
					if (nvm_wvalid_i) begin
						hdr_r[hidx_r] <= nvm_wdata_i;
						hidx_r <= hidx_r + 3'd1;
						if (hidx_r == 3'd7) begin
							plen_r <= hdr_plen_w;
							if (hdr_ok_w)
								state_r <= 4'd2;
							else begin
								err_r <= 1'b1;
								state_r <= 4'd15;
							end
						end
					end
				4'd2:
					if (dev_err_i) begin
						err_r <= 1'b1;
						state_r <= 4'd15;
					end
					else if (dev_gnt_i)
						state_r <= 4'd3;
				4'd3:
					if (dev_err_i) begin
						err_r <= 1'b1;
						state_r <= 4'd15;
					end
					else if (dev_done_i || done_seen_r) begin
						done_seen_r <= 1'b0;
						state_r <= 4'd4;
					end
				4'd4:
					if (dev_err_i) begin
						err_r <= 1'b1;
						state_r <= 4'd15;
					end
					else if (dev_gnt_i) begin
						hidx_r <= 1'sb0;
						state_r <= 4'd5;
					end
				4'd5:
					if (dev_err_i) begin
						err_r <= 1'b1;
						state_r <= 4'd15;
					end
					else if (dev_wready_i) begin
						hidx_r <= hidx_r + 3'd1;
						if (hidx_r == 3'd7) begin
							bcnt_r <= 1'sb0;
							state_r <= (plen_r == 16'd0 ? 4'd7 : 4'd6);
						end
					end
				4'd6:
					if (dev_err_i) begin
						err_r <= 1'b1;
						state_r <= 4'd15;
					end
					else if (nvm_wvalid_i && dev_wready_i) begin
						bcnt_r <= bcnt_r + 16'd1;
						if (bcnt_r == (plen_r - 16'd1))
							state_r <= 4'd7;
					end
				4'd7:
					if (dev_err_i) begin
						err_r <= 1'b1;
						state_r <= 4'd15;
					end
					else if (dev_done_i || done_seen_r) begin
						done_seen_r <= 1'b0;
						state_r <= 4'd15;
					end
				4'd8:
					if (dev_err_i) begin
						err_r <= 1'b1;
						state_r <= 4'd15;
					end
					else if (dev_gnt_i) begin
						hidx_r <= 1'sb0;
						state_r <= 4'd9;
					end
				4'd9:
					if (dev_err_i) begin
						err_r <= 1'b1;
						state_r <= 4'd15;
					end
					else begin
						if (dev_rvalid_i) begin
							hdr_r[hidx_r] <= dev_rdata_i;
							hidx_r <= hidx_r + 3'd1;
							if (hidx_r == 3'd7)
								state_r <= 4'd10;
						end
						if (dev_done_i && !(dev_rvalid_i && (hidx_r == 3'd7))) begin
							err_r <= 1'b1;
							state_r <= 4'd15;
						end
					end
				4'd10:
					if (dev_err_i) begin
						err_r <= 1'b1;
						state_r <= 4'd15;
					end
					else if (dev_done_i || done_seen_r) begin
						done_seen_r <= 1'b0;
						plen_r <= hdr_plen_w;
						if (hdr_ok_w) begin
							hidx_r <= 1'sb0;
							state_r <= 4'd11;
						end
						else begin
							err_r <= 1'b1;
							state_r <= 4'd15;
						end
					end
				4'd11:
					if (nvm_rready_i) begin
						hidx_r <= hidx_r + 3'd1;
						if (hidx_r == 3'd7) begin
							bcnt_r <= 1'sb0;
							state_r <= (plen_r == 16'd0 ? 4'd15 : 4'd12);
						end
					end
				4'd12:
					if (dev_err_i) begin
						err_r <= 1'b1;
						state_r <= 4'd15;
					end
					else if (dev_gnt_i) begin
						bcnt_r <= 1'sb0;
						state_r <= 4'd13;
					end
				4'd13:
					if (dev_err_i) begin
						err_r <= 1'b1;
						state_r <= 4'd15;
					end
					else if (dev_rvalid_i && nvm_rready_i) begin
						bcnt_r <= bcnt_r + 16'd1;
						if (bcnt_r == (plen_r - 16'd1))
							state_r <= 4'd14;
					end
				4'd14:
					if (dev_err_i) begin
						err_r <= 1'b1;
						state_r <= 4'd15;
					end
					else if (dev_done_i || done_seen_r) begin
						done_seen_r <= 1'b0;
						state_r <= 4'd15;
					end
				4'd15: begin
					done_seen_r <= 1'b0;
					state_r <= 4'd0;
				end
				default: state_r <= 4'd0;
			endcase
		end
	end
	assign nvm_busy_o = (state_r != 4'd0) && (state_r != 4'd15);
	assign nvm_done_o = (state_r == 4'd15) && !err_r;
	assign nvm_err_o = (state_r == 4'd15) && err_r;
	assign nvm_wready_o = (state_r == 4'd1) || ((state_r == 4'd6) && dev_wready_i);
	assign nvm_rvalid_o = (state_r == 4'd11) || ((state_r == 4'd13) && dev_rvalid_i);
	assign nvm_rdata_o = (state_r == 4'd11 ? hdr_r[hidx_r] : dev_rdata_i);
	assign dev_req_o = (((state_r == 4'd2) || (state_r == 4'd4)) || (state_r == 4'd8)) || (state_r == 4'd12);
	assign dev_region_o = rec_r;
	assign dev_wvalid_o = (state_r == 4'd5) || ((state_r == 4'd6) && nvm_wvalid_i);
	assign dev_wdata_o = (state_r == 4'd5 ? hdr_r[hidx_r] : nvm_wdata_i);
	assign dev_rready_o = (state_r == 4'd9) || ((state_r == 4'd13) && nvm_rready_i);
	always @(*) begin : dev_cmd
		if (_sv2v_0)
			;
		dev_op_o = NVMP_OP_READ_C;
		dev_offset_o = 16'd0;
		dev_len_o = 16'd0;
		case (state_r)
			4'd2: dev_op_o = NVMP_OP_ERASE_C;
			4'd4: begin
				dev_op_o = NVMP_OP_WRITE_C;
				dev_len_o = HDR_LEN_C + plen_r;
			end
			4'd8: dev_len_o = HDR_LEN_C;
			4'd12: begin
				dev_offset_o = HDR_LEN_C;
				dev_len_o = plen_r;
			end
			default:
				;
		endcase
	end
	initial _sv2v_0 = 0;
endmodule
`default_nettype wire
`default_nettype none
module KL_pp_originator (
	clk_i,
	rst_n,
	iss_valid_i,
	iss_owner_i,
	iss_tx_slot_i,
	iss_key_i,
	iss_tmr_slot_i,
	iss_timeout_ms_i,
	iss_ready_o,
	iss_gnt_o,
	iss_seq_o,
	iss_id_o,
	cancel_valid_i,
	cancel_owner_i,
	rsp_valid_i,
	rsp_seq_i,
	rsp_key_i,
	rt_valid_o,
	rt_owner_o,
	rt_id_o,
	fail_valid_o,
	fail_owner_o,
	fail_id_o,
	send_valid_o,
	send_slot_o,
	resend_valid_o,
	resend_slot_o,
	send_accept_valid_i,
	send_accept_slot_i,
	hold_valid_o,
	hold_slot_o,
	release_valid_o,
	release_slot_o,
	withdraw_slot_mask_o,
	tmr_arm_valid_o,
	tmr_arm_cancel_o,
	tmr_arm_slot_o,
	tmr_arm_owner_o,
	tmr_arm_deadline_ms_o,
	now_ms_i,
	exp_valid_i,
	exp_slot_i,
	exp_owner_i,
	rsp_ign_cnt_o,
	inflight_busy_o
);
	reg _sv2v_0;
	parameter [31:0] CA_POOL_P = 4;
	parameter [31:0] PROBE_SLOTS_P = 8;
	parameter [31:0] INFLIGHT_P = CA_POOL_P + PROBE_SLOTS_P;
	parameter [31:0] KEY_W_P = 16;
	localparam [31:0] pp_pkg_PP_CA_POOL_C = 4;
	localparam [31:0] pp_pkg_PP_N_CTRL_C = 16;
	localparam [31:0] pp_pkg_PP_N_IF_C = 1;
	localparam [31:0] pp_pkg_PP_N_STREAM_IN_C = 8;
	localparam [31:0] pp_pkg_PP_N_STREAM_OUT_C = 8;
	localparam [31:0] pp_pkg_PP_MAAP_SLOTS_C = 2;
	localparam [31:0] pp_pkg_PP_SINGLETON_SLOTS_C = 5;
	localparam [31:0] pp_pkg_PP_SRP_CAD_SLOTS_C = 7;
	function automatic [415:0] pp_pkg_pp_timer_map;
		input reg [31:0] n_if;
		input reg [31:0] si;
		input reg [31:0] so;
		input reg [31:0] n_ctrl;
		input reg [31:0] ca_pool;
		reg [415:0] m;
		begin
			m[415-:32] = 32'd0;
			m[383-:32] = m[415-:32] + n_if;
			m[351-:32] = m[383-:32] + si;
			m[319-:32] = m[351-:32] + si;
			m[287-:32] = m[319-:32] + so;
			m[255-:32] = m[287-:32] + ((32'd2 * n_ctrl) * n_if);
			m[223-:32] = m[255-:32] + ca_pool;
			m[191-:32] = m[223-:32] + pp_pkg_PP_SINGLETON_SLOTS_C;
			m[159-:32] = m[191-:32] + pp_pkg_PP_MAAP_SLOTS_C;
			m[127-:32] = m[159-:32];
			m[95-:32] = m[127-:32] + pp_pkg_PP_SRP_CAD_SLOTS_C;
			m[63-:32] = m[95-:32] + so;
			m[31-:32] = m[127-:32] + (((pp_pkg_PP_SRP_CAD_SLOTS_C + si) + so) * n_if);
			pp_pkg_pp_timer_map = m;
		end
	endfunction
	function automatic [31:0] pp_pkg_pp_timer_slots;
		input reg [31:0] n_if;
		input reg [31:0] si;
		input reg [31:0] so;
		input reg [31:0] n_ctrl;
		input reg [31:0] ca_pool;
		input reg en_srp;
		reg [415:0] m;
		begin
			m = pp_pkg_pp_timer_map(n_if, si, so, n_ctrl, ca_pool);
			pp_pkg_pp_timer_slots = (en_srp ? m[31-:32] : m[159-:32]);
		end
	endfunction
	localparam [31:0] pp_pkg_PP_TIMER_SLOTS_C = pp_pkg_pp_timer_slots(pp_pkg_PP_N_IF_C, pp_pkg_PP_N_STREAM_IN_C, pp_pkg_PP_N_STREAM_OUT_C, pp_pkg_PP_N_CTRL_C, pp_pkg_PP_CA_POOL_C, 1'b1);
	parameter [31:0] TMR_SLOTS_P = pp_pkg_PP_TIMER_SLOTS_C;
	localparam [31:0] IFL_AW_C = 4;
	localparam [31:0] pp_pkg_PP_TIMER_OWNER_W_C = 8;
	localparam [31:0] TAG_W_C = pp_pkg_PP_TIMER_OWNER_W_C - IFL_AW_C;
	parameter [TAG_W_C - 1:0] TMR_TAG_P = 4'hc;
	localparam [31:0] TMR_AW_C = (TMR_SLOTS_P > 32'd1 ? $clog2(TMR_SLOTS_P) : 32'd1);
	input wire clk_i;
	input wire rst_n;
	input wire iss_valid_i;
	input wire [3:0] iss_owner_i;
	input wire [2:0] iss_tx_slot_i;
	input wire [KEY_W_P - 1:0] iss_key_i;
	input wire [TMR_AW_C - 1:0] iss_tmr_slot_i;
	input wire [15:0] iss_timeout_ms_i;
	output wire iss_ready_o;
	output wire iss_gnt_o;
	output wire [15:0] iss_seq_o;
	output wire [3:0] iss_id_o;
	input wire cancel_valid_i;
	input wire [3:0] cancel_owner_i;
	input wire rsp_valid_i;
	input wire [15:0] rsp_seq_i;
	input wire [KEY_W_P - 1:0] rsp_key_i;
	output reg rt_valid_o;
	output reg [3:0] rt_owner_o;
	output reg [3:0] rt_id_o;
	output reg fail_valid_o;
	output reg [3:0] fail_owner_o;
	output reg [3:0] fail_id_o;
	output reg send_valid_o;
	output reg [2:0] send_slot_o;
	output reg resend_valid_o;
	output reg [2:0] resend_slot_o;
	input wire send_accept_valid_i;
	input wire [2:0] send_accept_slot_i;
	output reg hold_valid_o;
	output reg [2:0] hold_slot_o;
	output reg release_valid_o;
	output reg [2:0] release_slot_o;
	output reg [7:0] withdraw_slot_mask_o;
	output reg tmr_arm_valid_o;
	output reg tmr_arm_cancel_o;
	output reg [TMR_AW_C - 1:0] tmr_arm_slot_o;
	output reg [7:0] tmr_arm_owner_o;
	output reg [31:0] tmr_arm_deadline_ms_o;
	input wire [31:0] now_ms_i;
	input wire exp_valid_i;
	input wire [TMR_AW_C - 1:0] exp_slot_i;
	input wire [7:0] exp_owner_i;
	output reg [7:0] rsp_ign_cnt_o;
	output wire [INFLIGHT_P - 1:0] inflight_busy_o;
	localparam [31:0] IFL_N_C = 32'd1 << IFL_AW_C;
	generate
		if ((INFLIGHT_P < 32'd1) || (INFLIGHT_P > IFL_N_C)) begin : g_inflight_check
			initial $display("Error [elaboration] $VALIDATION_STORAGE/reviews/r247-520-r1/protocol-processor/hdl/packet_engine/KL_pp_originator.sv:149:5 - KL_pp_originator.g_inflight_check\n msg: ", "KL_pp_originator: INFLIGHT_P must be 1..16 (owner-tag nibble)");
		end
	endgenerate
	reg [IFL_N_C - 1:0] valid_r;
	reg [IFL_N_C - 1:0] retried_r;
	reg [IFL_N_C - 1:0] exp_pend_r;
	reg [IFL_N_C - 1:0] await_tx_r;
	reg [IFL_N_C - 1:0] accept_pend_r;
	reg [IFL_N_C - 1:0] cancel_pend_r;
	reg [3:0] owner_r [0:IFL_N_C - 1];
	reg [KEY_W_P - 1:0] key_r [0:IFL_N_C - 1];
	reg [15:0] seq_r [0:IFL_N_C - 1];
	reg [TMR_AW_C - 1:0] tslot_r [0:IFL_N_C - 1];
	reg [15:0] tout_r [0:IFL_N_C - 1];
	reg [2:0] txs_r [0:IFL_N_C - 1];
	reg [15:0] seq_ctr_r [0:IFL_N_C - 1];
	reg free_ok_w;
	reg [3:0] free_ix_w;
	function automatic signed [3:0] sv2v_cast_3838D_signed;
		input reg signed [3:0] inp;
		sv2v_cast_3838D_signed = inp;
	endfunction
	function automatic signed [31:0] sv2v_cast_32_signed;
		input reg signed [31:0] inp;
		sv2v_cast_32_signed = inp;
	endfunction
	always @(*) begin : alloc_pick
		if (_sv2v_0)
			;
		free_ok_w = 1'b0;
		free_ix_w = 1'sb0;
		begin : sv2v_autoblock_1
			reg signed [31:0] i;
			for (i = sv2v_cast_32_signed(INFLIGHT_P) - 1; i >= 0; i = i - 1)
				if (!valid_r[i]) begin
					free_ok_w = 1'b1;
					free_ix_w = sv2v_cast_3838D_signed(i);
				end
		end
	end
	reg [IFL_N_C - 1:0] cancel_work_w;
	reg cancel_pend_ok_w;
	reg [3:0] cancel_pend_ix_w;
	reg cancel_hit_w;
	reg [3:0] cancel_ix_w;
	always @(*) begin : cancel_pending_pick
		if (_sv2v_0)
			;
		cancel_work_w = cancel_pend_r;
		if (cancel_valid_i && cancel_hit_w)
			cancel_work_w[cancel_ix_w] = 1'b1;
		cancel_pend_ok_w = 1'b0;
		cancel_pend_ix_w = 1'sb0;
		begin : sv2v_autoblock_2
			reg signed [31:0] i;
			for (i = sv2v_cast_32_signed(INFLIGHT_P) - 1; i >= 0; i = i - 1)
				if (cancel_work_w[i]) begin
					cancel_pend_ok_w = 1'b1;
					cancel_pend_ix_w = sv2v_cast_3838D_signed(i);
				end
		end
	end
	reg accept_ok_w;
	reg [3:0] accept_pend_ix_w;
	always @(*) begin : accept_pending_pick
		if (_sv2v_0)
			;
		accept_ok_w = 1'b0;
		accept_pend_ix_w = 1'sb0;
		begin : sv2v_autoblock_3
			reg signed [31:0] i;
			for (i = sv2v_cast_32_signed(INFLIGHT_P) - 1; i >= 0; i = i - 1)
				if (accept_pend_r[i]) begin
					accept_ok_w = 1'b1;
					accept_pend_ix_w = sv2v_cast_3838D_signed(i);
				end
		end
	end
	reg hit_ok_w;
	reg [3:0] hit_ix_w;
	always @(*) begin : cam_pick
		if (_sv2v_0)
			;
		hit_ok_w = 1'b0;
		hit_ix_w = 1'sb0;
		begin : sv2v_autoblock_4
			reg signed [31:0] i;
			for (i = sv2v_cast_32_signed(INFLIGHT_P) - 1; i >= 0; i = i - 1)
				if ((valid_r[i] && (key_r[i] == rsp_key_i)) && (seq_r[i] == rsp_seq_i)) begin
					hit_ok_w = 1'b1;
					hit_ix_w = sv2v_cast_3838D_signed(i);
				end
		end
	end
	always @(*) begin : cancel_pick
		if (_sv2v_0)
			;
		cancel_hit_w = 1'b0;
		cancel_ix_w = 1'sb0;
		begin : sv2v_autoblock_5
			reg signed [31:0] i;
			for (i = sv2v_cast_32_signed(INFLIGHT_P) - 1; i >= 0; i = i - 1)
				if (valid_r[i] && (owner_r[i] == cancel_owner_i)) begin
					cancel_hit_w = 1'b1;
					cancel_ix_w = sv2v_cast_3838D_signed(i);
				end
		end
	end
	reg accept_hit_w;
	reg [3:0] accept_ix_w;
	always @(*) begin : accept_pick
		if (_sv2v_0)
			;
		accept_hit_w = 1'b0;
		accept_ix_w = 1'sb0;
		begin : sv2v_autoblock_6
			reg signed [31:0] i;
			for (i = sv2v_cast_32_signed(INFLIGHT_P) - 1; i >= 0; i = i - 1)
				if ((valid_r[i] && await_tx_r[i]) && (txs_r[i] == send_accept_slot_i)) begin
					accept_hit_w = 1'b1;
					accept_ix_w = sv2v_cast_3838D_signed(i);
				end
		end
	end
	wire exp_ours_w;
	wire [3:0] exp_ix_w;
	wire exp_genuine_w;
	assign exp_ours_w = exp_valid_i && (exp_owner_i[7:IFL_AW_C] == TMR_TAG_P);
	assign exp_ix_w = exp_owner_i[3:0];
	function automatic [31:0] sv2v_cast_32;
		input reg [31:0] inp;
		sv2v_cast_32 = inp;
	endfunction
	assign exp_genuine_w = ((exp_ours_w && (sv2v_cast_32(exp_ix_w) < INFLIGHT_P)) && valid_r[exp_ix_w]) && (tslot_r[exp_ix_w] == exp_slot_i);
	reg pend_ok_w;
	reg [3:0] pend_ix_w;
	always @(*) begin : pend_pick
		if (_sv2v_0)
			;
		pend_ok_w = 1'b0;
		pend_ix_w = 1'sb0;
		begin : sv2v_autoblock_7
			reg signed [31:0] i;
			for (i = sv2v_cast_32_signed(INFLIGHT_P) - 1; i >= 0; i = i - 1)
				if (exp_pend_r[i]) begin
					pend_ok_w = 1'b1;
					pend_ix_w = sv2v_cast_3838D_signed(i);
				end
		end
	end
	wire ev_rsp_w;
	wire ev_cancel_w;
	wire ev_accept_w;
	wire ev_exp_w;
	wire ev_iss_w;
	assign ev_rsp_w = rsp_valid_i && hit_ok_w;
	assign ev_cancel_w = !ev_rsp_w && cancel_pend_ok_w;
	assign ev_accept_w = (!ev_rsp_w && !ev_cancel_w) && accept_ok_w;
	assign ev_exp_w = ((!ev_rsp_w && !ev_cancel_w) && !ev_accept_w) && pend_ok_w;
	assign iss_ready_o = (((free_ok_w && !ev_rsp_w) && !ev_cancel_w) && !ev_accept_w) && !pend_ok_w;
	assign ev_iss_w = iss_valid_i && iss_ready_o;
	always @(*) begin : withdraw_mask
		if (_sv2v_0)
			;
		withdraw_slot_mask_o = 1'sb0;
		begin : sv2v_autoblock_8
			reg signed [31:0] i;
			for (i = 0; i < sv2v_cast_32_signed(INFLIGHT_P); i = i + 1)
				if (cancel_work_w[i] && valid_r[i])
					withdraw_slot_mask_o[txs_r[i]] = 1'b1;
		end
		if (ev_rsp_w)
			withdraw_slot_mask_o[txs_r[hit_ix_w]] = 1'b1;
		if ((ev_exp_w && valid_r[pend_ix_w]) && retried_r[pend_ix_w])
			withdraw_slot_mask_o[txs_r[pend_ix_w]] = 1'b1;
	end
	assign iss_gnt_o = ev_iss_w;
	assign iss_id_o = free_ix_w;
	assign iss_seq_o = seq_ctr_r[iss_owner_i];
	always @(posedge clk_i) begin : inflight_state
		if (!rst_n) begin
			valid_r <= 1'sb0;
			retried_r <= 1'sb0;
			exp_pend_r <= 1'sb0;
			await_tx_r <= 1'sb0;
			accept_pend_r <= 1'sb0;
			cancel_pend_r <= 1'sb0;
			begin : sv2v_autoblock_9
				reg signed [31:0] i;
				for (i = 0; i < sv2v_cast_32_signed(IFL_N_C); i = i + 1)
					seq_ctr_r[i] <= 16'd0;
			end
		end
		else begin
			if (exp_genuine_w)
				exp_pend_r[exp_ix_w] <= 1'b1;
			if (send_accept_valid_i && accept_hit_w)
				accept_pend_r[accept_ix_w] <= 1'b1;
			if (cancel_valid_i && cancel_hit_w)
				cancel_pend_r[cancel_ix_w] <= 1'b1;
			if (ev_rsp_w) begin
				valid_r[hit_ix_w] <= 1'b0;
				exp_pend_r[hit_ix_w] <= 1'b0;
				await_tx_r[hit_ix_w] <= 1'b0;
				accept_pend_r[hit_ix_w] <= 1'b0;
				cancel_pend_r[hit_ix_w] <= 1'b0;
			end
			else if (ev_cancel_w) begin
				valid_r[cancel_pend_ix_w] <= 1'b0;
				exp_pend_r[cancel_pend_ix_w] <= 1'b0;
				await_tx_r[cancel_pend_ix_w] <= 1'b0;
				accept_pend_r[cancel_pend_ix_w] <= 1'b0;
				cancel_pend_r[cancel_pend_ix_w] <= 1'b0;
			end
			else if (ev_accept_w) begin
				await_tx_r[accept_pend_ix_w] <= 1'b0;
				accept_pend_r[accept_pend_ix_w] <= 1'b0;
			end
			else if (ev_exp_w) begin
				exp_pend_r[pend_ix_w] <= 1'b0;
				if (valid_r[pend_ix_w]) begin
					if (!retried_r[pend_ix_w]) begin
						retried_r[pend_ix_w] <= 1'b1;
						await_tx_r[pend_ix_w] <= 1'b1;
					end
					else begin
						valid_r[pend_ix_w] <= 1'b0;
						await_tx_r[pend_ix_w] <= 1'b0;
						accept_pend_r[pend_ix_w] <= 1'b0;
					end
				end
			end
			else if (ev_iss_w) begin
				valid_r[free_ix_w] <= 1'b1;
				retried_r[free_ix_w] <= 1'b0;
				exp_pend_r[free_ix_w] <= 1'b0;
				await_tx_r[free_ix_w] <= 1'b1;
				accept_pend_r[free_ix_w] <= 1'b0;
				owner_r[free_ix_w] <= iss_owner_i;
				key_r[free_ix_w] <= iss_key_i;
				seq_r[free_ix_w] <= seq_ctr_r[iss_owner_i];
				tslot_r[free_ix_w] <= iss_tmr_slot_i;
				tout_r[free_ix_w] <= iss_timeout_ms_i;
				txs_r[free_ix_w] <= iss_tx_slot_i;
				seq_ctr_r[iss_owner_i] <= seq_ctr_r[iss_owner_i] + 16'd1;
			end
		end
	end
	always @(posedge clk_i) begin : action_regs
		if (!rst_n) begin
			rt_valid_o <= 1'b0;
			rt_owner_o <= 1'sb0;
			rt_id_o <= 1'sb0;
			fail_valid_o <= 1'b0;
			fail_owner_o <= 1'sb0;
			fail_id_o <= 1'sb0;
			send_valid_o <= 1'b0;
			send_slot_o <= 1'sb0;
			resend_valid_o <= 1'b0;
			resend_slot_o <= 1'sb0;
			hold_valid_o <= 1'b0;
			hold_slot_o <= 1'sb0;
			release_valid_o <= 1'b0;
			release_slot_o <= 1'sb0;
			tmr_arm_valid_o <= 1'b0;
			tmr_arm_cancel_o <= 1'b0;
			tmr_arm_slot_o <= 1'sb0;
			tmr_arm_owner_o <= 1'sb0;
			tmr_arm_deadline_ms_o <= 32'd0;
		end
		else begin
			rt_valid_o <= 1'b0;
			fail_valid_o <= 1'b0;
			send_valid_o <= 1'b0;
			resend_valid_o <= 1'b0;
			hold_valid_o <= 1'b0;
			release_valid_o <= 1'b0;
			tmr_arm_valid_o <= 1'b0;
			if (ev_rsp_w) begin
				rt_valid_o <= 1'b1;
				rt_owner_o <= owner_r[hit_ix_w];
				rt_id_o <= hit_ix_w;
				release_valid_o <= 1'b1;
				release_slot_o <= txs_r[hit_ix_w];
				tmr_arm_valid_o <= 1'b1;
				tmr_arm_cancel_o <= 1'b1;
				tmr_arm_slot_o <= tslot_r[hit_ix_w];
				tmr_arm_owner_o <= {TMR_TAG_P, hit_ix_w};
				tmr_arm_deadline_ms_o <= 32'd0;
			end
			else if (ev_cancel_w) begin
				release_valid_o <= 1'b1;
				release_slot_o <= txs_r[cancel_pend_ix_w];
				tmr_arm_valid_o <= 1'b1;
				tmr_arm_cancel_o <= 1'b1;
				tmr_arm_slot_o <= tslot_r[cancel_pend_ix_w];
				tmr_arm_owner_o <= {TMR_TAG_P, cancel_pend_ix_w};
				tmr_arm_deadline_ms_o <= 32'd0;
			end
			else if (ev_accept_w) begin
				tmr_arm_valid_o <= 1'b1;
				tmr_arm_cancel_o <= 1'b0;
				tmr_arm_slot_o <= tslot_r[accept_pend_ix_w];
				tmr_arm_owner_o <= {TMR_TAG_P, accept_pend_ix_w};
				tmr_arm_deadline_ms_o <= now_ms_i + sv2v_cast_32(tout_r[accept_pend_ix_w]);
			end
			else if (ev_exp_w) begin
				if (valid_r[pend_ix_w]) begin
					if (!retried_r[pend_ix_w]) begin
						resend_valid_o <= 1'b1;
						resend_slot_o <= txs_r[pend_ix_w];
					end
					else begin
						fail_valid_o <= 1'b1;
						fail_owner_o <= owner_r[pend_ix_w];
						fail_id_o <= pend_ix_w;
						release_valid_o <= 1'b1;
						release_slot_o <= txs_r[pend_ix_w];
					end
				end
			end
			else if (ev_iss_w) begin
				send_valid_o <= 1'b1;
				send_slot_o <= iss_tx_slot_i;
				hold_valid_o <= 1'b1;
				hold_slot_o <= iss_tx_slot_i;
			end
		end
	end
	always @(posedge clk_i) begin : ign_count
		if (!rst_n)
			rsp_ign_cnt_o <= 8'd0;
		else if (rsp_valid_i && !hit_ok_w)
			rsp_ign_cnt_o <= rsp_ign_cnt_o + 8'd1;
	end
	assign inflight_busy_o = valid_r[INFLIGHT_P - 1:0];
	initial _sv2v_0 = 0;
endmodule
`default_nettype wire
`default_nettype none
module KL_pp_release_merge (
	clk_i,
	rst_n,
	a_valid_i,
	a_slot_i,
	b_valid_i,
	b_slot_i,
	release_valid_o,
	release_slot_o
);
	reg _sv2v_0;
	parameter [31:0] N_SLOTS_P = 5;
	localparam [31:0] SLOT_W_C = (N_SLOTS_P > 1 ? $clog2(N_SLOTS_P) : 1);
	input wire clk_i;
	input wire rst_n;
	input wire a_valid_i;
	input wire [SLOT_W_C - 1:0] a_slot_i;
	input wire b_valid_i;
	input wire [SLOT_W_C - 1:0] b_slot_i;
	output reg release_valid_o;
	output reg [SLOT_W_C - 1:0] release_slot_o;
	generate
		if (N_SLOTS_P < 1) begin : g_slot_count_check
			initial $display("Error [elaboration] $VALIDATION_STORAGE/reviews/r247-520-r1/protocol-processor/hdl/packet_engine/KL_pp_release_merge.sv:38:5 - KL_pp_release_merge.g_slot_count_check\n msg: ", "KL_pp_release_merge: N_SLOTS_P must be positive");
		end
	endgenerate
	reg [N_SLOTS_P - 1:0] pending_r;
	reg [N_SLOTS_P - 1:0] request_w;
	wire [N_SLOTS_P - 1:0] available_w;
	function automatic [31:0] sv2v_cast_32;
		input reg [31:0] inp;
		sv2v_cast_32 = inp;
	endfunction
	always @(*) begin : collect_requests
		if (_sv2v_0)
			;
		request_w = 1'sb0;
		if (a_valid_i && (sv2v_cast_32(a_slot_i) < N_SLOTS_P))
			request_w[a_slot_i] = 1'b1;
		if (b_valid_i && (sv2v_cast_32(b_slot_i) < N_SLOTS_P))
			request_w[b_slot_i] = 1'b1;
	end
	assign available_w = pending_r | request_w;
	function automatic signed [SLOT_W_C - 1:0] sv2v_cast_63BED_signed;
		input reg signed [SLOT_W_C - 1:0] inp;
		sv2v_cast_63BED_signed = inp;
	endfunction
	function automatic signed [31:0] sv2v_cast_32_signed;
		input reg signed [31:0] inp;
		sv2v_cast_32_signed = inp;
	endfunction
	always @(*) begin : release_pick
		if (_sv2v_0)
			;
		release_valid_o = 1'b0;
		release_slot_o = 1'sb0;
		begin : sv2v_autoblock_1
			reg signed [31:0] i;
			for (i = sv2v_cast_32_signed(N_SLOTS_P) - 1; i >= 0; i = i - 1)
				if (available_w[i]) begin
					release_valid_o = 1'b1;
					release_slot_o = sv2v_cast_63BED_signed(i);
				end
		end
	end
	always @(posedge clk_i) begin : pending_state
		if (!rst_n)
			pending_r <= 1'sb0;
		else begin
			pending_r <= available_w;
			if (release_valid_o)
				pending_r[release_slot_o] <= 1'b0;
		end
	end
	initial _sv2v_0 = 0;
endmodule
`default_nettype wire
`default_nettype none
module KL_pp_rx_slots (
	clk_i,
	rst_n,
	alloc_req_i,
	alloc_gnt_o,
	alloc_slot_o,
	wr_valid_i,
	wr_data_i,
	wr_last_i,
	wr_abort_i,
	wr_commit_i,
	rd_slot_i,
	rd_addr_i,
	rd_en_i,
	rd_data_o,
	slot_len_o,
	free_i,
	free_slot_i,
	slots_free_o,
	rx_overrun_count_o
);
	reg _sv2v_0;
	parameter [31:0] SLOTS_P = 4;
	parameter [31:0] BYTES_P = 576;
	localparam [31:0] SLOT_W_C = (SLOTS_P > 1 ? $clog2(SLOTS_P) : 1);
	localparam [31:0] ADDR_W_C = $clog2(BYTES_P);
	localparam [31:0] LEN_W_C = $clog2(BYTES_P + 1);
	localparam [31:0] FREE_W_C = $clog2(SLOTS_P + 1);
	input wire clk_i;
	input wire rst_n;
	input wire alloc_req_i;
	output wire alloc_gnt_o;
	output wire [SLOT_W_C - 1:0] alloc_slot_o;
	input wire wr_valid_i;
	input wire [7:0] wr_data_i;
	input wire wr_last_i;
	input wire wr_abort_i;
	input wire wr_commit_i;
	input wire [SLOT_W_C - 1:0] rd_slot_i;
	input wire [ADDR_W_C - 1:0] rd_addr_i;
	input wire rd_en_i;
	output reg [7:0] rd_data_o;
	output wire [LEN_W_C - 1:0] slot_len_o;
	input wire free_i;
	input wire [SLOT_W_C - 1:0] free_slot_i;
	output reg [FREE_W_C - 1:0] slots_free_o;
	output wire [15:0] rx_overrun_count_o;
	localparam [31:0] MADDR_W_C = $clog2(SLOTS_P * BYTES_P);
	localparam [15:0] OVR_MAX_C = 16'hffff;
	reg [SLOTS_P - 1:0] writing_r;
	reg [SLOTS_P - 1:0] occupied_r;
	wire [SLOTS_P - 1:0] free_mask_w;
	reg [SLOT_W_C - 1:0] cur_slot_r;
	reg wr_active_r;
	reg wr_closed_r;
	reg [LEN_W_C - 1:0] wr_ptr_r;
	reg [LEN_W_C - 1:0] len_r [0:SLOTS_P - 1];
	reg [15:0] ovr_cnt_r;
	assign free_mask_w = ~(writing_r | occupied_r);
	assign rx_overrun_count_o = ovr_cnt_r;
	reg ff_valid_w;
	reg [SLOT_W_C - 1:0] ff_slot_w;
	function automatic [SLOT_W_C - 1:0] sv2v_cast_63BED;
		input reg [SLOT_W_C - 1:0] inp;
		sv2v_cast_63BED = inp;
	endfunction
	always @(*) begin : first_free_enc
		if (_sv2v_0)
			;
		ff_valid_w = 1'b0;
		ff_slot_w = 1'sb0;
		begin : sv2v_autoblock_1
			reg [31:0] i;
			for (i = 0; i < SLOTS_P; i = i + 1)
				if (!ff_valid_w && free_mask_w[i]) begin
					ff_valid_w = 1'b1;
					ff_slot_w = sv2v_cast_63BED(i);
				end
		end
	end
	assign alloc_gnt_o = (alloc_req_i && ff_valid_w) && !wr_active_r;
	assign alloc_slot_o = ff_slot_w;
	function automatic signed [FREE_W_C - 1:0] sv2v_cast_5E54D_signed;
		input reg signed [FREE_W_C - 1:0] inp;
		sv2v_cast_5E54D_signed = inp;
	endfunction
	always @(*) begin : free_count
		if (_sv2v_0)
			;
		slots_free_o = 1'sb0;
		begin : sv2v_autoblock_2
			reg [31:0] i;
			for (i = 0; i < SLOTS_P; i = i + 1)
				if (free_mask_w[i])
					slots_free_o = slots_free_o + sv2v_cast_5E54D_signed(1);
		end
	end
	wire byte_acc_w;
	wire [LEN_W_C - 1:0] wr_len_now_w;
	function automatic [LEN_W_C - 1:0] sv2v_cast_E8FD1;
		input reg [LEN_W_C - 1:0] inp;
		sv2v_cast_E8FD1 = inp;
	endfunction
	assign byte_acc_w = ((wr_active_r && wr_valid_i) && !wr_closed_r) && (wr_ptr_r < sv2v_cast_E8FD1(BYTES_P));
	function automatic signed [LEN_W_C - 1:0] sv2v_cast_E8FD1_signed;
		input reg signed [LEN_W_C - 1:0] inp;
		sv2v_cast_E8FD1_signed = inp;
	endfunction
	assign wr_len_now_w = (byte_acc_w ? wr_ptr_r + sv2v_cast_E8FD1_signed(1) : wr_ptr_r);
	always @(posedge clk_i) begin : slot_ctrl
		if (!rst_n) begin
			writing_r <= 1'sb0;
			occupied_r <= 1'sb0;
			cur_slot_r <= 1'sb0;
			wr_active_r <= 1'b0;
			wr_closed_r <= 1'b0;
			wr_ptr_r <= 1'sb0;
			ovr_cnt_r <= 1'sb0;
			begin : sv2v_autoblock_3
				reg [31:0] i;
				for (i = 0; i < SLOTS_P; i = i + 1)
					len_r[i] <= 1'sb0;
			end
		end
		else begin
			if (alloc_gnt_o) begin
				cur_slot_r <= ff_slot_w;
				writing_r[ff_slot_w] <= 1'b1;
				wr_active_r <= 1'b1;
				wr_closed_r <= 1'b0;
				wr_ptr_r <= 1'sb0;
			end
			if ((alloc_req_i && !ff_valid_w) && (ovr_cnt_r != OVR_MAX_C))
				ovr_cnt_r <= ovr_cnt_r + 16'd1;
			if (byte_acc_w) begin
				wr_ptr_r <= wr_ptr_r + sv2v_cast_E8FD1_signed(1);
				if (wr_last_i)
					wr_closed_r <= 1'b1;
			end
			if (wr_active_r && wr_abort_i) begin
				writing_r[cur_slot_r] <= 1'b0;
				wr_active_r <= 1'b0;
			end
			else if (wr_active_r && wr_commit_i) begin
				writing_r[cur_slot_r] <= 1'b0;
				occupied_r[cur_slot_r] <= 1'b1;
				len_r[cur_slot_r] <= wr_len_now_w;
				wr_active_r <= 1'b0;
			end
			if (free_i && occupied_r[free_slot_i])
				occupied_r[free_slot_i] <= 1'b0;
		end
	end
	reg [7:0] mem_r [0:(SLOTS_P * BYTES_P) - 1];
	wire [MADDR_W_C - 1:0] wr_maddr_w;
	wire [MADDR_W_C - 1:0] rd_maddr_w;
	function automatic [MADDR_W_C - 1:0] sv2v_cast_50D76;
		input reg [MADDR_W_C - 1:0] inp;
		sv2v_cast_50D76 = inp;
	endfunction
	assign wr_maddr_w = (sv2v_cast_50D76(cur_slot_r) * sv2v_cast_50D76(BYTES_P)) + sv2v_cast_50D76(wr_ptr_r);
	assign rd_maddr_w = (sv2v_cast_50D76(rd_slot_i) * sv2v_cast_50D76(BYTES_P)) + sv2v_cast_50D76(rd_addr_i);
	always @(posedge clk_i) begin : slot_mem_wr
		if (byte_acc_w)
			mem_r[wr_maddr_w] <= wr_data_i;
	end
	always @(posedge clk_i) begin : slot_mem_rd
		if (rd_en_i)
			rd_data_o <= mem_r[rd_maddr_w];
	end
	assign slot_len_o = len_r[rd_slot_i];
	initial _sv2v_0 = 0;
endmodule
`default_nettype wire
`default_nettype none
module KL_pp_rx_validator (
	clk_i,
	rst_n,
	rx_valid_i,
	rx_data_i,
	rx_last_i,
	own_mac_i,
	mrp_valid_o,
	mrp_data_o,
	mrp_last_o,
	alloc_req_o,
	alloc_gnt_i,
	alloc_slot_i,
	wr_valid_o,
	wr_data_o,
	wr_last_o,
	wr_abort_o,
	wr_commit_o,
	hdr_valid_o,
	hdr_protocol_o,
	hdr_msg_type_o,
	hdr_status_o,
	hdr_cdl_o,
	hdr_src_mac_o,
	hdr_controller_eid_o,
	hdr_target_eid_o,
	hdr_sequence_id_o,
	hdr_u_o,
	hdr_cr_o,
	hdr_opcode_o,
	hdr_operands_o,
	hdr_rx_slot_o,
	rx_da_count_o,
	rx_ethertype_count_o,
	rx_subtype_count_o,
	rx_version_count_o,
	rx_length_count_o
);
	reg _sv2v_0;
	parameter [31:0] SLOTS_P = 4;
	parameter [31:0] BYTES_P = 576;
	localparam [31:0] SLOT_W_C = (SLOTS_P > 1 ? $clog2(SLOTS_P) : 1);
	input wire clk_i;
	input wire rst_n;
	input wire rx_valid_i;
	input wire [7:0] rx_data_i;
	input wire rx_last_i;
	input wire [47:0] own_mac_i;
	output wire mrp_valid_o;
	output wire [7:0] mrp_data_o;
	output wire mrp_last_o;
	output wire alloc_req_o;
	input wire alloc_gnt_i;
	input wire [SLOT_W_C - 1:0] alloc_slot_i;
	output wire wr_valid_o;
	output wire [7:0] wr_data_o;
	output wire wr_last_o;
	output wire wr_abort_o;
	output wire wr_commit_o;
	output wire hdr_valid_o;
	output wire [2:0] hdr_protocol_o;
	output wire [3:0] hdr_msg_type_o;
	output wire [4:0] hdr_status_o;
	output wire [10:0] hdr_cdl_o;
	output wire [47:0] hdr_src_mac_o;
	output wire [63:0] hdr_controller_eid_o;
	output wire [63:0] hdr_target_eid_o;
	output wire [15:0] hdr_sequence_id_o;
	output wire hdr_u_o;
	output wire hdr_cr_o;
	output wire [15:0] hdr_opcode_o;
	output wire [63:0] hdr_operands_o;
	output wire [2:0] hdr_rx_slot_o;
	output wire [15:0] rx_da_count_o;
	output wire [15:0] rx_ethertype_count_o;
	output wire [15:0] rx_subtype_count_o;
	output wire [15:0] rx_version_count_o;
	output wire [15:0] rx_length_count_o;
	localparam [47:0] DA_AVDECC_C = 48'h91e0f0010000;
	localparam [47:0] DA_MAAP_C = 48'h91e0f000ff00;
	localparam [47:0] DA_MSRP_C = 48'h0180c200000e;
	localparam [47:0] DA_MVRP_C = 48'h0180c2000021;
	localparam [15:0] ET_1722_C = 16'h22f0;
	localparam [15:0] ET_MSRP_C = 16'h22ea;
	localparam [15:0] ET_MVRP_C = 16'h88f5;
	localparam [7:0] SUB_ADP_C = 8'hfa;
	localparam [7:0] SUB_AECP_C = 8'hfb;
	localparam [7:0] SUB_ACMP_C = 8'hfc;
	localparam [7:0] SUB_MAAP_C = 8'hfe;
	localparam [15:0] CNT_MAX_C = 16'hffff;
	function automatic [31:0] sv2v_cast_32;
		input reg [31:0] inp;
		sv2v_cast_32 = inp;
	endfunction
	function automatic [7:0] mac_byte_f;
		input reg [47:0] m;
		input reg [10:0] i;
		reg [31:0] k;
		begin
			k = (i > 11'd5 ? 32'd0 : 32'd5 - sv2v_cast_32(i));
			mac_byte_f = m[k * 8+:8];
		end
	endfunction
	reg [1:0] fr_st_r;
	reg [10:0] idx_r;
	reg da_own_r;
	reg da_mcast_r;
	reg da_maap_r;
	reg da_msrp_r;
	reg da_mvrp_r;
	reg [7:0] et_hi_r;
	reg vpushed_r;
	reg alloc_req_r;
	reg slot_held_r;
	reg [SLOT_W_C - 1:0] slot_r;
	reg cdl_known_r;
	reg [7:0] subtype_r;
	reg [3:0] msg_type_r;
	reg [4:0] status_r;
	reg [10:0] cdl_r;
	reg [47:0] src_mac_r;
	reg [63:0] target_eid_r;
	reg [63:0] ctlr_eid_r;
	reg [15:0] seq_r;
	reg [15:0] opcode_r;
	reg [15:0] desc_type_r;
	reg [15:0] desc_index_r;
	reg [15:0] tuid_r;
	reg [15:0] luid_r;
	reg u_r;
	reg cr_r;
	reg end_pend_r;
	reg end_pass_r;
	reg abort_pend_r;
	reg [1:0] cp_r;
	reg p1_en_r;
	reg p2_en_r;
	reg [7:0] p1_d_r;
	reg [7:0] p2_d_r;
	reg p1_l_r;
	reg p2_l_r;
	reg [2:0] hdr_protocol_r;
	reg [3:0] hdr_msg_type_r;
	reg [4:0] hdr_status_r;
	reg [10:0] hdr_cdl_r;
	reg [47:0] hdr_src_mac_r;
	reg [63:0] hdr_ctlr_eid_r;
	reg [63:0] hdr_target_eid_r;
	reg [15:0] hdr_seq_r;
	reg [15:0] hdr_opcode_r;
	reg hdr_u_r;
	reg hdr_cr_r;
	reg [63:0] hdr_operands_r;
	reg [2:0] hdr_rx_slot_r;
	reg [15:0] cnt_da_r;
	reg [15:0] cnt_et_r;
	reg [15:0] cnt_sub_r;
	reg [15:0] cnt_ver_r;
	reg [15:0] cnt_len_r;
	wire acc_w;
	wire end_w;
	wire [10:0] pidx_w;
	reg da_own_a_w;
	reg da_mcast_a_w;
	reg da_maap_a_w;
	reg da_msrp_a_w;
	reg da_mvrp_a_w;
	wire da_1722_a_w;
	wire da_mrp_a_w;
	wire [15:0] et_w;
	wire et_1722_ok_w;
	wire et_mrp_ok_w;
	wire slot_now_w;
	wire [11:0] lim_w;
	wire in_budget_w;
	wire pdu_byte_w;
	wire sub_fail_w;
	wire ver_fail_w;
	wire fail_now_w;
	wire wr_en_w;
	wire wlast_w;
	wire [11:0] pcnt_end_w;
	wire v1_pass_w;
	wire ev_da_w;
	wire ev_et_w;
	wire ev_len_w;
	assign acc_w = rx_valid_i;
	assign end_w = rx_valid_i && rx_last_i;
	assign pidx_w = idx_r - 11'd14;
	always @(*) begin : da_fold
		if (_sv2v_0)
			;
		da_own_a_w = da_own_r;
		da_mcast_a_w = da_mcast_r;
		da_maap_a_w = da_maap_r;
		da_msrp_a_w = da_msrp_r;
		da_mvrp_a_w = da_mvrp_r;
		if ((acc_w && (fr_st_r == 2'd0)) && (idx_r <= 11'd5)) begin
			if (rx_data_i != mac_byte_f(own_mac_i, idx_r))
				da_own_a_w = 1'b0;
			if (rx_data_i != mac_byte_f(DA_AVDECC_C, idx_r))
				da_mcast_a_w = 1'b0;
			if (rx_data_i != mac_byte_f(DA_MAAP_C, idx_r))
				da_maap_a_w = 1'b0;
			if (rx_data_i != mac_byte_f(DA_MSRP_C, idx_r))
				da_msrp_a_w = 1'b0;
			if (rx_data_i != mac_byte_f(DA_MVRP_C, idx_r))
				da_mvrp_a_w = 1'b0;
		end
	end
	assign da_1722_a_w = (da_own_a_w | da_mcast_a_w) | da_maap_a_w;
	assign da_mrp_a_w = da_msrp_a_w | da_mvrp_a_w;
	assign et_w = {et_hi_r, rx_data_i};
	assign et_1722_ok_w = et_w == ET_1722_C;
	assign et_mrp_ok_w = (da_msrp_r && (et_w == ET_MSRP_C)) | (da_mvrp_r && (et_w == ET_MVRP_C));
	assign slot_now_w = slot_held_r | (alloc_req_r & alloc_gnt_i);
	assign lim_w = {1'b0, cdl_r} + 12'd12;
	assign in_budget_w = (cdl_known_r ? {1'b0, pidx_w} < lim_w : 1'b1);
	assign pdu_byte_w = ((acc_w && (fr_st_r == 2'd1)) && (idx_r >= 11'd14)) && slot_now_w;
	assign sub_fail_w = ((pdu_byte_w && (pidx_w == 11'd0)) && !((((rx_data_i == SUB_ADP_C) || (rx_data_i == SUB_AECP_C)) || (rx_data_i == SUB_ACMP_C)) && (da_own_r | da_mcast_r))) && !((rx_data_i == SUB_MAAP_C) && (da_own_r | da_maap_r));
	assign ver_fail_w = (pdu_byte_w && (pidx_w == 11'd1)) && (rx_data_i[7:4] != 4'h0);
	assign fail_now_w = sub_fail_w | ver_fail_w;
	assign wr_en_w = (pdu_byte_w && in_budget_w) && !fail_now_w;
	assign wlast_w = (wr_en_w && cdl_known_r) && ({1'b0, pidx_w} == (lim_w - 12'd1));
	assign pcnt_end_w = {1'b0, pidx_w} + 12'd1;
	function automatic [11:0] sv2v_cast_12;
		input reg [11:0] inp;
		sv2v_cast_12 = inp;
	endfunction
	assign v1_pass_w = (((((fr_st_r == 2'd1) && slot_now_w) && !fail_now_w) && cdl_known_r) && (pcnt_end_w >= lim_w)) && (lim_w <= sv2v_cast_12(BYTES_P));
	assign ev_da_w = (((acc_w && (fr_st_r == 2'd0)) && (idx_r == 11'd5)) && !(da_1722_a_w | da_mrp_a_w)) | ((end_w && (fr_st_r == 2'd0)) && (idx_r < 11'd5));
	assign ev_et_w = ((fr_st_r == 2'd0) && da_1722_a_w) && (((acc_w && (idx_r == 11'd13)) && !et_1722_ok_w) || ((end_w && (idx_r >= 11'd5)) && (idx_r < 11'd13)));
	assign ev_len_w = (((((acc_w && (fr_st_r == 2'd0)) && da_1722_a_w) && (idx_r == 11'd13)) && et_1722_ok_w) && rx_last_i) | ((((end_w && (fr_st_r == 2'd1)) && slot_now_w) && !fail_now_w) && !v1_pass_w);
	reg vd_push_w;
	wire vq_full_w;
	localparam [2:0] pp_pkg_PP_SLOT_NULL_C = 3'd7;
	function automatic [2:0] sv2v_cast_3;
		input reg [2:0] inp;
		sv2v_cast_3 = inp;
	endfunction
	always @(posedge clk_i) begin : validator_seq
		if (!rst_n) begin
			fr_st_r <= 2'd0;
			idx_r <= 1'sb0;
			da_own_r <= 1'b1;
			da_mcast_r <= 1'b1;
			da_maap_r <= 1'b1;
			da_msrp_r <= 1'b1;
			da_mvrp_r <= 1'b1;
			et_hi_r <= 1'sb0;
			vpushed_r <= 1'b0;
			alloc_req_r <= 1'b0;
			slot_held_r <= 1'b0;
			slot_r <= 1'sb0;
			cdl_known_r <= 1'b0;
			subtype_r <= 1'sb0;
			msg_type_r <= 1'sb0;
			status_r <= 1'sb0;
			cdl_r <= 1'sb0;
			src_mac_r <= 1'sb0;
			target_eid_r <= 1'sb0;
			ctlr_eid_r <= 1'sb0;
			seq_r <= 1'sb0;
			opcode_r <= 1'sb0;
			desc_type_r <= 1'sb0;
			desc_index_r <= 1'sb0;
			tuid_r <= 1'sb0;
			luid_r <= 1'sb0;
			u_r <= 1'b0;
			cr_r <= 1'b0;
			end_pend_r <= 1'b0;
			end_pass_r <= 1'b0;
			abort_pend_r <= 1'b0;
			cp_r <= 1'sb0;
			p1_en_r <= 1'b0;
			p2_en_r <= 1'b0;
			p1_d_r <= 1'sb0;
			p2_d_r <= 1'sb0;
			p1_l_r <= 1'b0;
			p2_l_r <= 1'b0;
			hdr_protocol_r <= 1'sb0;
			hdr_msg_type_r <= 1'sb0;
			hdr_status_r <= 1'sb0;
			hdr_cdl_r <= 1'sb0;
			hdr_src_mac_r <= 1'sb0;
			hdr_ctlr_eid_r <= 1'sb0;
			hdr_target_eid_r <= 1'sb0;
			hdr_seq_r <= 1'sb0;
			hdr_opcode_r <= 1'sb0;
			hdr_u_r <= 1'b0;
			hdr_cr_r <= 1'b0;
			hdr_operands_r <= 1'sb0;
			hdr_rx_slot_r <= pp_pkg_PP_SLOT_NULL_C;
			cnt_da_r <= 1'sb0;
			cnt_et_r <= 1'sb0;
			cnt_sub_r <= 1'sb0;
			cnt_ver_r <= 1'sb0;
			cnt_len_r <= 1'sb0;
		end
		else begin
			alloc_req_r <= 1'b0;
			abort_pend_r <= 1'b0;
			end_pend_r <= 1'b0;
			p1_en_r <= wr_en_w;
			p1_d_r <= rx_data_i;
			p1_l_r <= wlast_w;
			p2_en_r <= p1_en_r;
			p2_d_r <= p1_d_r;
			p2_l_r <= p1_l_r;
			if (vd_push_w && !vq_full_w)
				vpushed_r <= 1'b1;
			if (alloc_req_r) begin
				if (alloc_gnt_i) begin
					slot_held_r <= 1'b1;
					slot_r <= alloc_slot_i;
				end
				else
					fr_st_r <= 2'd2;
			end
			if (acc_w) begin
				idx_r <= (end_w ? 11'd0 : (idx_r == 11'h7ff ? idx_r : idx_r + 11'd1));
				if (fr_st_r == 2'd0) begin
					if (idx_r <= 11'd5) begin
						da_own_r <= da_own_a_w;
						da_mcast_r <= da_mcast_a_w;
						da_maap_r <= da_maap_a_w;
						da_msrp_r <= da_msrp_a_w;
						da_mvrp_r <= da_mvrp_a_w;
						if ((idx_r == 11'd5) && !(da_1722_a_w | da_mrp_a_w))
							fr_st_r <= 2'd2;
					end
					if ((idx_r >= 11'd6) && (idx_r <= 11'd11))
						src_mac_r[(32'd11 - sv2v_cast_32(idx_r)) * 8+:8] <= rx_data_i;
					if (idx_r == 11'd12)
						et_hi_r <= rx_data_i;
					if (idx_r == 11'd13) begin
						if (da_1722_a_w) begin
							if (et_1722_ok_w && !rx_last_i) begin
								fr_st_r <= 2'd1;
								alloc_req_r <= 1'b1;
							end
							else
								fr_st_r <= 2'd2;
						end
						else
							fr_st_r <= 2'd2;
					end
				end
				else if (fr_st_r == 2'd1) begin
					if (pdu_byte_w && in_budget_w) begin : field_cap
						if (pidx_w == 11'd0)
							subtype_r <= rx_data_i;
						if (pidx_w == 11'd1)
							msg_type_r <= rx_data_i[3:0];
						if (pidx_w == 11'd2) begin
							status_r <= rx_data_i[7:3];
							cdl_r[10:8] <= rx_data_i[2:0];
						end
						if (pidx_w == 11'd3) begin
							cdl_r[7:0] <= rx_data_i;
							cdl_known_r <= 1'b1;
						end
						if ((pidx_w >= 11'd4) && (pidx_w <= 11'd11))
							target_eid_r[(32'd11 - sv2v_cast_32(pidx_w)) * 8+:8] <= rx_data_i;
						if (((subtype_r != SUB_ADP_C) && (pidx_w >= 11'd12)) && (pidx_w <= 11'd19))
							ctlr_eid_r[(32'd19 - sv2v_cast_32(pidx_w)) * 8+:8] <= rx_data_i;
						if (subtype_r == SUB_AECP_C) begin
							if (pidx_w == 11'd20)
								seq_r[15:8] <= rx_data_i;
							if (pidx_w == 11'd21)
								seq_r[7:0] <= rx_data_i;
							if (pidx_w == 11'd22) begin
								u_r <= rx_data_i[7];
								cr_r <= rx_data_i[6];
								opcode_r[15:8] <= {2'b00, rx_data_i[5:0]};
							end
							if (pidx_w == 11'd23)
								opcode_r[7:0] <= rx_data_i;
							if (pidx_w == 11'd24)
								desc_type_r[15:8] <= rx_data_i;
							if (pidx_w == 11'd25)
								desc_type_r[7:0] <= rx_data_i;
							if (pidx_w == 11'd26)
								desc_index_r[15:8] <= rx_data_i;
							if (pidx_w == 11'd27)
								desc_index_r[7:0] <= rx_data_i;
						end
						if (subtype_r == SUB_ACMP_C) begin
							if (pidx_w == 11'd36)
								tuid_r[15:8] <= rx_data_i;
							if (pidx_w == 11'd37)
								tuid_r[7:0] <= rx_data_i;
							if (pidx_w == 11'd38)
								luid_r[15:8] <= rx_data_i;
							if (pidx_w == 11'd39)
								luid_r[7:0] <= rx_data_i;
							if (pidx_w == 11'd48)
								seq_r[15:8] <= rx_data_i;
							if (pidx_w == 11'd49)
								seq_r[7:0] <= rx_data_i;
						end
						if (subtype_r == SUB_MAAP_C) begin
							if (pidx_w == 11'd20)
								desc_type_r[15:8] <= rx_data_i;
							if (pidx_w == 11'd21)
								desc_type_r[7:0] <= rx_data_i;
							if (pidx_w == 11'd22)
								desc_index_r[15:8] <= rx_data_i;
							if (pidx_w == 11'd23)
								desc_index_r[7:0] <= rx_data_i;
							if (pidx_w == 11'd24)
								tuid_r[15:8] <= rx_data_i;
							if (pidx_w == 11'd25)
								tuid_r[7:0] <= rx_data_i;
							if (pidx_w == 11'd26)
								luid_r[15:8] <= rx_data_i;
							if (pidx_w == 11'd27)
								luid_r[7:0] <= rx_data_i;
						end
					end
					if (fail_now_w)
						fr_st_r <= 2'd2;
				end
				if (end_w) begin
					end_pend_r <= 1'b1;
					end_pass_r <= v1_pass_w;
					fr_st_r <= 2'd0;
					da_own_r <= 1'b1;
					da_mcast_r <= 1'b1;
					da_maap_r <= 1'b1;
					da_msrp_r <= 1'b1;
					da_mvrp_r <= 1'b1;
					vpushed_r <= 1'b0;
				end
			end
			if ((fail_now_w && slot_now_w) || ((((end_w && (fr_st_r == 2'd1)) && slot_now_w) && !fail_now_w) && !v1_pass_w))
				abort_pend_r <= 1'b1;
			if (abort_pend_r)
				slot_held_r <= 1'b0;
			cp_r <= {cp_r[0], end_pend_r & end_pass_r};
			if (end_pend_r) begin
				if (end_pass_r) begin : hdr_latch
					hdr_msg_type_r <= msg_type_r;
					hdr_status_r <= status_r;
					hdr_cdl_r <= cdl_r;
					hdr_src_mac_r <= src_mac_r;
					hdr_target_eid_r <= target_eid_r;
					hdr_ctlr_eid_r <= (subtype_r == SUB_ADP_C ? 64'd0 : ctlr_eid_r);
					hdr_seq_r <= seq_r;
					hdr_u_r <= u_r;
					hdr_cr_r <= cr_r;
					hdr_rx_slot_r <= sv2v_cast_3(slot_r);
					if (subtype_r == SUB_ADP_C) begin
						hdr_protocol_r <= 3'd0;
						hdr_opcode_r <= {12'd0, msg_type_r};
						hdr_operands_r <= 1'sb0;
					end
					else if (subtype_r == SUB_MAAP_C) begin
						hdr_protocol_r <= 3'd5;
						hdr_opcode_r <= {12'd0, msg_type_r};
						hdr_operands_r <= {desc_type_r, desc_index_r, tuid_r, luid_r};
					end
					else if (subtype_r == SUB_ACMP_C) begin
						hdr_protocol_r <= 3'd1;
						hdr_opcode_r <= {12'd0, msg_type_r};
						hdr_operands_r <= {48'h000000000000, ((((msg_type_r == 4'd0) || (msg_type_r == 4'd2)) || (msg_type_r == 4'd4)) || (msg_type_r == 4'd12) ? tuid_r : luid_r)};
					end
					else begin
						hdr_protocol_r <= ((msg_type_r == 4'd6) || (msg_type_r == 4'd7) ? 3'd3 : ((msg_type_r == 4'd2) || (msg_type_r == 4'd3) ? 3'd4 : 3'd2));
						hdr_opcode_r <= opcode_r;
						hdr_operands_r <= {desc_type_r, desc_index_r, 32'h00000000};
					end
				end
				cdl_known_r <= 1'b0;
				subtype_r <= 1'sb0;
				msg_type_r <= 1'sb0;
				status_r <= 1'sb0;
				cdl_r <= 1'sb0;
				src_mac_r <= 1'sb0;
				target_eid_r <= 1'sb0;
				ctlr_eid_r <= 1'sb0;
				seq_r <= 1'sb0;
				opcode_r <= 1'sb0;
				desc_type_r <= 1'sb0;
				desc_index_r <= 1'sb0;
				tuid_r <= 1'sb0;
				luid_r <= 1'sb0;
				u_r <= 1'b0;
				cr_r <= 1'b0;
			end
			if (cp_r[1])
				slot_held_r <= 1'b0;
			if (ev_da_w && (cnt_da_r != CNT_MAX_C))
				cnt_da_r <= cnt_da_r + 16'd1;
			if (ev_et_w && (cnt_et_r != CNT_MAX_C))
				cnt_et_r <= cnt_et_r + 16'd1;
			if (sub_fail_w && (cnt_sub_r != CNT_MAX_C))
				cnt_sub_r <= cnt_sub_r + 16'd1;
			if (ver_fail_w && (cnt_ver_r != CNT_MAX_C))
				cnt_ver_r <= cnt_ver_r + 16'd1;
			if (ev_len_w && (cnt_len_r != CNT_MAX_C))
				cnt_len_r <= cnt_len_r + 16'd1;
		end
	end
	reg [8:0] mrp_mem_r [0:63];
	reg [6:0] wptr_r;
	reg [6:0] rptr_r;
	reg vq_r [0:15];
	reg [4:0] vwptr_r;
	reg [4:0] vrptr_r;
	reg od_last_r;
	reg [7:0] od_data_r;
	reg out_valid_r;
	reg out_emit_r;
	wire fifo_ne_w;
	wire fifo_full_w;
	wire vq_ne_w;
	wire vq_head_w;
	wire push_w;
	reg vd_val_w;
	wire rd_fire_w;
	wire retire_w;
	assign fifo_ne_w = wptr_r != rptr_r;
	assign fifo_full_w = wptr_r == (rptr_r ^ 7'h40);
	assign vq_ne_w = vwptr_r != vrptr_r;
	assign vq_full_w = vwptr_r == (vrptr_r ^ 5'h10);
	assign vq_head_w = vq_r[vrptr_r[3:0]];
	assign push_w = acc_w && !fifo_full_w;
	always @(*) begin : verdict_point
		if (_sv2v_0)
			;
		vd_push_w = 1'b0;
		vd_val_w = 1'b0;
		if ((acc_w && (fr_st_r == 2'd0)) && !vpushed_r) begin
			if ((idx_r == 11'd5) && !da_mrp_a_w)
				vd_push_w = 1'b1;
			else if ((idx_r == 11'd13) && da_mrp_a_w) begin
				vd_push_w = 1'b1;
				vd_val_w = et_mrp_ok_w;
			end
		end
		if ((end_w && !vpushed_r) && !vd_push_w)
			vd_push_w = 1'b1;
	end
	assign retire_w = out_valid_r && od_last_r;
	assign rd_fire_w = (fifo_ne_w && vq_ne_w) && !retire_w;
	always @(posedge clk_i) begin : mrp_ctrl
		if (!rst_n) begin
			wptr_r <= 1'sb0;
			rptr_r <= 1'sb0;
			vwptr_r <= 1'sb0;
			vrptr_r <= 1'sb0;
			out_valid_r <= 1'b0;
			out_emit_r <= 1'b0;
			begin : sv2v_autoblock_1
				reg [31:0] i;
				for (i = 0; i < 16; i = i + 1)
					vq_r[i] <= 1'b0;
			end
		end
		else begin
			if (push_w)
				wptr_r <= wptr_r + 7'd1;
			if (vd_push_w && !vq_full_w) begin
				vq_r[vwptr_r[3:0]] <= vd_val_w;
				vwptr_r <= vwptr_r + 5'd1;
			end
			if (rd_fire_w) begin
				rptr_r <= rptr_r + 7'd1;
				out_valid_r <= 1'b1;
				out_emit_r <= vq_head_w;
			end
			else
				out_valid_r <= 1'b0;
			if (retire_w)
				vrptr_r <= vrptr_r + 5'd1;
		end
	end
	always @(posedge clk_i) begin : mrp_mem_wr
		if (push_w)
			mrp_mem_r[wptr_r[5:0]] <= {rx_last_i, rx_data_i};
	end
	always @(posedge clk_i) begin : mrp_mem_rd
		if (rd_fire_w)
			{od_last_r, od_data_r} <= mrp_mem_r[rptr_r[5:0]];
	end
	assign mrp_valid_o = out_valid_r && out_emit_r;
	assign mrp_data_o = od_data_r;
	assign mrp_last_o = (out_valid_r && out_emit_r) && od_last_r;
	assign alloc_req_o = alloc_req_r;
	assign wr_valid_o = p2_en_r;
	assign wr_data_o = p2_d_r;
	assign wr_last_o = p2_l_r;
	assign wr_abort_o = abort_pend_r;
	assign wr_commit_o = cp_r[1];
	assign hdr_valid_o = cp_r[1];
	assign hdr_protocol_o = hdr_protocol_r;
	assign hdr_msg_type_o = hdr_msg_type_r;
	assign hdr_status_o = hdr_status_r;
	assign hdr_cdl_o = hdr_cdl_r;
	assign hdr_src_mac_o = hdr_src_mac_r;
	assign hdr_controller_eid_o = hdr_ctlr_eid_r;
	assign hdr_target_eid_o = hdr_target_eid_r;
	assign hdr_sequence_id_o = hdr_seq_r;
	assign hdr_u_o = hdr_u_r;
	assign hdr_cr_o = hdr_cr_r;
	assign hdr_opcode_o = hdr_opcode_r;
	assign hdr_operands_o = hdr_operands_r;
	assign hdr_rx_slot_o = hdr_rx_slot_r;
	assign rx_da_count_o = cnt_da_r;
	assign rx_ethertype_count_o = cnt_et_r;
	assign rx_subtype_count_o = cnt_sub_r;
	assign rx_version_count_o = cnt_ver_r;
	assign rx_length_count_o = cnt_len_r;
	initial _sv2v_0 = 0;
endmodule
`default_nettype wire
`default_nettype none
module KL_pp_scoreboard (
	clk_i,
	rst_n,
	adm_req_i,
	adm_class_i,
	adm_key_i,
	adm_gnt_o,
	adm_id_o,
	rel_valid_i,
	rel_id_i,
	kill_valid_i,
	kill_id_i,
	kill_resp_queued_i,
	kill_ack_o,
	holds_o,
	full_o,
	barrier_pend_o
);
	reg _sv2v_0;
	parameter [31:0] MAX_HOLDS_P = 8;
	localparam [31:0] ID_W_C = (MAX_HOLDS_P > 32'd1 ? $clog2(MAX_HOLDS_P) : 32'd1);
	input wire clk_i;
	input wire rst_n;
	input wire adm_req_i;
	input wire [3:0] adm_class_i;
	input wire [15:0] adm_key_i;
	output wire adm_gnt_o;
	output wire [ID_W_C - 1:0] adm_id_o;
	input wire rel_valid_i;
	input wire [ID_W_C - 1:0] rel_id_i;
	input wire kill_valid_i;
	input wire [ID_W_C - 1:0] kill_id_i;
	input wire kill_resp_queued_i;
	output wire kill_ack_o;
	output wire [MAX_HOLDS_P - 1:0] holds_o;
	output wire full_o;
	output wire barrier_pend_o;
	localparam [3:0] HZ_RO_SNAPSHOT_C = 4'd0;
	localparam [3:0] HZ_CFG_BARRIER_C = 4'd1;
	localparam [3:0] HZ_STREAM_CFG_C = 4'd2;
	localparam [3:0] HZ_MAP_CFG_C = 4'd3;
	localparam [3:0] HZ_CLOCK_CFG_C = 4'd4;
	localparam [3:0] HZ_NAME_WR_C = 4'd5;
	localparam [3:0] HZ_LOCK_OP_C = 4'd6;
	localparam [3:0] HZ_REGISTRY_OP_C = 4'd7;
	localparam [3:0] HZ_IDENTIFY_C = 4'd8;
	function automatic hz_is_lockprot;
		input reg [3:0] c;
		hz_is_lockprot = (((((c == HZ_CFG_BARRIER_C) || (c == HZ_STREAM_CFG_C)) || (c == HZ_MAP_CFG_C)) || (c == HZ_CLOCK_CFG_C)) || (c == HZ_NAME_WR_C)) || (c == HZ_IDENTIFY_C);
	endfunction
	function automatic hz_conflict;
		input reg [3:0] a_cls;
		input reg [15:0] a_key;
		input reg [3:0] b_cls;
		input reg [15:0] b_key;
		reg same_key_v;
		reg [3:0] other_v;
		reg [0:1] _sv2v_jump;
		begin
			_sv2v_jump = 2'b00;
			same_key_v = a_key == b_key;
			other_v = (a_cls == HZ_LOCK_OP_C ? b_cls : a_cls);
			if ((a_cls == HZ_CFG_BARRIER_C) || (b_cls == HZ_CFG_BARRIER_C)) begin
				hz_conflict = 1'b1;
				_sv2v_jump = 2'b11;
			end
			if (_sv2v_jump == 2'b00) begin
				if ((a_cls == HZ_RO_SNAPSHOT_C) && (b_cls == HZ_RO_SNAPSHOT_C)) begin
					hz_conflict = 1'b0;
					_sv2v_jump = 2'b11;
				end
				if (_sv2v_jump == 2'b00) begin
					if ((a_cls == HZ_RO_SNAPSHOT_C) || (b_cls == HZ_RO_SNAPSHOT_C)) begin
						hz_conflict = same_key_v;
						_sv2v_jump = 2'b11;
					end
					if (_sv2v_jump == 2'b00) begin
						if ((a_cls == HZ_LOCK_OP_C) || (b_cls == HZ_LOCK_OP_C)) begin
							hz_conflict = (other_v == HZ_LOCK_OP_C) || hz_is_lockprot(other_v);
							_sv2v_jump = 2'b11;
						end
						if (_sv2v_jump == 2'b00) begin
							if (a_cls == b_cls) begin
								if ((a_cls == HZ_REGISTRY_OP_C) || (a_cls == HZ_IDENTIFY_C)) begin
									hz_conflict = 1'b1;
									_sv2v_jump = 2'b11;
								end
								if (_sv2v_jump == 2'b00) begin
									hz_conflict = same_key_v;
									_sv2v_jump = 2'b11;
								end
							end
							if (_sv2v_jump == 2'b00) begin
								if (((a_cls == HZ_STREAM_CFG_C) && (b_cls == HZ_MAP_CFG_C)) || ((a_cls == HZ_MAP_CFG_C) && (b_cls == HZ_STREAM_CFG_C))) begin
									hz_conflict = 1'b1;
									_sv2v_jump = 2'b11;
								end
								if (_sv2v_jump == 2'b00) begin
									hz_conflict = 1'b0;
									_sv2v_jump = 2'b11;
								end
							end
						end
					end
				end
			end
		end
	endfunction
	reg [MAX_HOLDS_P - 1:0] valid_r;
	reg [3:0] cls_r [0:MAX_HOLDS_P - 1];
	reg [15:0] key_r [0:MAX_HOLDS_P - 1];
	reg barrier_pend_r;
	reg conflict_any_w;
	always @(*) begin : conflict_scan
		if (_sv2v_0)
			;
		conflict_any_w = 1'b0;
		begin : sv2v_autoblock_1
			reg [31:0] i;
			for (i = 0; i < MAX_HOLDS_P; i = i + 1)
				if (valid_r[i] && hz_conflict(adm_class_i, adm_key_i, cls_r[i], key_r[i]))
					conflict_any_w = 1'b1;
		end
	end
	reg ff_valid_w;
	reg [ID_W_C - 1:0] ff_id_w;
	function automatic [ID_W_C - 1:0] sv2v_cast_592CA;
		input reg [ID_W_C - 1:0] inp;
		sv2v_cast_592CA = inp;
	endfunction
	always @(*) begin : first_free
		if (_sv2v_0)
			;
		ff_valid_w = 1'b0;
		ff_id_w = 1'sb0;
		begin : sv2v_autoblock_2
			reg [31:0] i;
			for (i = 0; i < MAX_HOLDS_P; i = i + 1)
				if (!ff_valid_w && !valid_r[i]) begin
					ff_valid_w = 1'b1;
					ff_id_w = sv2v_cast_592CA(i);
				end
		end
	end
	wire adm_is_barrier_w;
	assign adm_is_barrier_w = adm_class_i == HZ_CFG_BARRIER_C;
	assign adm_gnt_o = ((adm_req_i && ff_valid_w) && !conflict_any_w) && (adm_is_barrier_w || !barrier_pend_r);
	assign adm_id_o = ff_id_w;
	assign kill_ack_o = (kill_valid_i && kill_resp_queued_i) && valid_r[kill_id_i];
	assign holds_o = valid_r;
	assign full_o = !ff_valid_w;
	assign barrier_pend_o = barrier_pend_r;
	always @(posedge clk_i) begin : holds_table
		if (!rst_n) begin
			valid_r <= 1'sb0;
			barrier_pend_r <= 1'b0;
			begin : sv2v_autoblock_3
				reg [31:0] i;
				for (i = 0; i < MAX_HOLDS_P; i = i + 1)
					begin
						cls_r[i] <= 4'd0;
						key_r[i] <= 16'd0;
					end
			end
		end
		else begin
			if (rel_valid_i && valid_r[rel_id_i])
				valid_r[rel_id_i] <= 1'b0;
			if (kill_ack_o)
				valid_r[kill_id_i] <= 1'b0;
			if (adm_gnt_o) begin
				valid_r[ff_id_w] <= 1'b1;
				cls_r[ff_id_w] <= adm_class_i;
				key_r[ff_id_w] <= adm_key_i;
			end
			if (adm_req_i && adm_is_barrier_w)
				barrier_pend_r <= !adm_gnt_o;
		end
	end
	initial _sv2v_0 = 0;
endmodule
`default_nettype wire
`default_nettype none
module KL_pp_side_port (
	clk_i,
	rst_n,
	entity_enable_i,
	req_valid_i,
	we_i,
	addr_i,
	wdata_i,
	rdata_o,
	rvalid_o,
	err_o,
	img_req_o,
	img_we_o,
	img_addr_o,
	img_wdata_o,
	img_rdata_i,
	img_rvalid_i,
	dbg_req_o,
	dbg_addr_o,
	dbg_rdata_i,
	dbg_rvalid_i,
	snap_req_o,
	snap_addr_o,
	snap_rdata_i,
	snap_rvalid_i,
	ctrl_req_o,
	ctrl_we_o,
	ctrl_addr_o,
	ctrl_wdata_o,
	ctrl_rdata_i,
	ctrl_rvalid_i,
	trace_req_o,
	trace_addr_o,
	trace_rdata_i,
	trace_rvalid_i,
	fw_req_o,
	fw_we_o,
	fw_addr_o,
	fw_wdata_o,
	fw_rdata_i,
	fw_rvalid_i
);
	reg _sv2v_0;
	parameter [0:0] EN_FW_ASSIST_P = 1'b0;
	input wire clk_i;
	input wire rst_n;
	input wire entity_enable_i;
	input wire req_valid_i;
	input wire we_i;
	input wire [19:0] addr_i;
	input wire [31:0] wdata_i;
	output reg [31:0] rdata_o;
	output reg rvalid_o;
	output reg err_o;
	output wire img_req_o;
	output wire img_we_o;
	output wire [15:0] img_addr_o;
	output wire [31:0] img_wdata_o;
	input wire [31:0] img_rdata_i;
	input wire img_rvalid_i;
	output wire dbg_req_o;
	output wire [15:0] dbg_addr_o;
	input wire [31:0] dbg_rdata_i;
	input wire dbg_rvalid_i;
	output wire snap_req_o;
	output wire [15:0] snap_addr_o;
	input wire [31:0] snap_rdata_i;
	input wire snap_rvalid_i;
	output wire ctrl_req_o;
	output wire ctrl_we_o;
	output wire [7:0] ctrl_addr_o;
	output wire [31:0] ctrl_wdata_o;
	input wire [31:0] ctrl_rdata_i;
	input wire ctrl_rvalid_i;
	output wire trace_req_o;
	output wire [15:0] trace_addr_o;
	input wire [31:0] trace_rdata_i;
	input wire trace_rvalid_i;
	output wire fw_req_o;
	output wire fw_we_o;
	output wire [15:0] fw_addr_o;
	output wire [31:0] fw_wdata_o;
	input wire [31:0] fw_rdata_i;
	input wire fw_rvalid_i;
	localparam [3:0] WIN_IMG_C = 4'h0;
	localparam [3:0] WIN_DBG_C = 4'h1;
	localparam [3:0] WIN_SNAP_C = 4'h2;
	localparam [3:0] WIN_CTRL_C = 4'h3;
	localparam [3:0] WIN_TRACE_C = 4'h4;
	localparam [3:0] WIN_FW_C = 4'h5;
	reg [1:0] state_r;
	reg [2:0] sel_r;
	wire [3:0] win_w;
	reg fwd_ok_w;
	wire accept_w;
	reg sel_rvalid_w;
	reg [31:0] sel_rdata_w;
	assign win_w = addr_i[19:16];
	assign accept_w = req_valid_i && (state_r == 2'd0);
	always @(*) begin : win_decode
		if (_sv2v_0)
			;
		case (win_w)
			WIN_IMG_C: fwd_ok_w = (we_i ? !entity_enable_i : 1'b1);
			WIN_DBG_C: fwd_ok_w = !we_i;
			WIN_SNAP_C: fwd_ok_w = !we_i;
			WIN_CTRL_C: fwd_ok_w = addr_i[15:8] == 8'h00;
			WIN_TRACE_C: fwd_ok_w = !we_i;
			WIN_FW_C: fwd_ok_w = EN_FW_ASSIST_P != 1'b0;
			default: fwd_ok_w = 1'b0;
		endcase
	end
	assign img_req_o = (accept_w && fwd_ok_w) && (win_w == WIN_IMG_C);
	assign img_we_o = img_req_o && we_i;
	assign img_addr_o = addr_i[15:0];
	assign img_wdata_o = wdata_i;
	assign dbg_req_o = (accept_w && fwd_ok_w) && (win_w == WIN_DBG_C);
	assign dbg_addr_o = addr_i[15:0];
	assign snap_req_o = (accept_w && fwd_ok_w) && (win_w == WIN_SNAP_C);
	assign snap_addr_o = addr_i[15:0];
	assign ctrl_req_o = (accept_w && fwd_ok_w) && (win_w == WIN_CTRL_C);
	assign ctrl_we_o = ctrl_req_o && we_i;
	assign ctrl_addr_o = addr_i[7:0];
	assign ctrl_wdata_o = wdata_i;
	assign trace_req_o = (accept_w && fwd_ok_w) && (win_w == WIN_TRACE_C);
	assign trace_addr_o = addr_i[15:0];
	assign fw_req_o = (accept_w && fwd_ok_w) && (win_w == WIN_FW_C);
	assign fw_we_o = fw_req_o && we_i;
	assign fw_addr_o = addr_i[15:0];
	assign fw_wdata_o = wdata_i;
	always @(*) begin : rsp_mux
		if (_sv2v_0)
			;
		case (sel_r)
			3'd0: begin
				sel_rvalid_w = img_rvalid_i;
				sel_rdata_w = img_rdata_i;
			end
			3'd1: begin
				sel_rvalid_w = dbg_rvalid_i;
				sel_rdata_w = dbg_rdata_i;
			end
			3'd2: begin
				sel_rvalid_w = snap_rvalid_i;
				sel_rdata_w = snap_rdata_i;
			end
			3'd3: begin
				sel_rvalid_w = ctrl_rvalid_i;
				sel_rdata_w = ctrl_rdata_i;
			end
			3'd4: begin
				sel_rvalid_w = trace_rvalid_i;
				sel_rdata_w = trace_rdata_i;
			end
			3'd5: begin
				sel_rvalid_w = fw_rvalid_i;
				sel_rdata_w = fw_rdata_i;
			end
			default: begin
				sel_rvalid_w = 1'b0;
				sel_rdata_w = 32'h00000000;
			end
		endcase
	end
	always @(*) begin : rsp_drive
		if (_sv2v_0)
			;
		rvalid_o = 1'b0;
		err_o = 1'b0;
		rdata_o = 32'h00000000;
		case (state_r)
			2'd1: begin
				rvalid_o = sel_rvalid_w;
				rdata_o = (sel_rvalid_w ? sel_rdata_w : 32'h00000000);
			end
			2'd2: begin
				rvalid_o = 1'b1;
				err_o = 1'b1;
			end
			default:
				;
		endcase
	end
	always @(posedge clk_i) begin : sp_fsm
		if (!rst_n) begin
			state_r <= 2'd0;
			sel_r <= 3'd0;
		end
		else
			case (state_r)
				2'd0:
					if (accept_w) begin
						state_r <= (fwd_ok_w ? 2'd1 : 2'd2);
						sel_r <= win_w[2:0];
					end
				2'd1:
					if (sel_rvalid_w)
						state_r <= 2'd0;
				default: state_r <= 2'd0;
			endcase
	end
	initial _sv2v_0 = 0;
endmodule
`default_nettype wire
`default_nettype none
module KL_pp_trace_ring (
	clk_i,
	rst_n,
	wr_valid_i,
	wr_data_i,
	wr_count_o,
	rd_en_i,
	rd_addr_i,
	rd_lane_i,
	rd_data_o
);
	reg _sv2v_0;
	parameter [31:0] RECORDS_P = 256;
	parameter [31:0] RECORD_W_P = 128;
	localparam [31:0] ADDR_W_C = $clog2(RECORDS_P);
	localparam [31:0] LANES_C = RECORD_W_P / 32;
	localparam [31:0] LANE_W_C = $clog2(LANES_C);
	input wire clk_i;
	input wire rst_n;
	input wire wr_valid_i;
	input wire [RECORD_W_P - 1:0] wr_data_i;
	output wire [15:0] wr_count_o;
	input wire rd_en_i;
	input wire [ADDR_W_C - 1:0] rd_addr_i;
	input wire [LANE_W_C - 1:0] rd_lane_i;
	output reg [31:0] rd_data_o;
	reg [15:0] wr_count_r;
	wire [ADDR_W_C - 1:0] wr_ptr_w;
	assign wr_ptr_w = wr_count_r[ADDR_W_C - 1:0];
	assign wr_count_o = wr_count_r;
	always @(posedge clk_i) begin : count_ff
		if (!rst_n)
			wr_count_r <= 16'h0000;
		else if (wr_valid_i)
			wr_count_r <= wr_count_r + 16'd1;
	end
	reg [RECORD_W_P - 1:0] mem_r [0:RECORDS_P - 1];
	reg [RECORD_W_P - 1:0] rd_word_r;
	reg [LANE_W_C - 1:0] rd_lane_r;
	always @(posedge clk_i) begin : ring_wr
		if (wr_valid_i)
			mem_r[wr_ptr_w] <= wr_data_i;
	end
	always @(posedge clk_i) begin : ring_rd
		if (rd_en_i) begin
			rd_word_r <= mem_r[rd_addr_i];
			rd_lane_r <= rd_lane_i;
		end
	end
	function automatic [LANE_W_C - 1:0] sv2v_cast_BE6CF;
		input reg [LANE_W_C - 1:0] inp;
		sv2v_cast_BE6CF = inp;
	endfunction
	always @(*) begin : lane_mux
		if (_sv2v_0)
			;
		rd_data_o = 32'h00000000;
		begin : sv2v_autoblock_1
			reg [31:0] l;
			for (l = 0; l < LANES_C; l = l + 1)
				if (rd_lane_r == sv2v_cast_BE6CF(l))
					rd_data_o = rd_word_r[((LANES_C - 1) - l) * 32+:32];
		end
	end
	initial _sv2v_0 = 0;
endmodule
`default_nettype wire
`default_nettype none
module KL_pp_tx_arbiter (
	clk_i,
	rst_n,
	tick_ms_i,
	req_valid_i,
	tx_slot_i,
	start_abort_i,
	gnt_o,
	gnt_count_o,
	ser_req_o,
	ser_slot_o,
	ser_valid_i,
	ser_data_i,
	ser_last_i,
	ser_ready_o,
	tx_valid_o,
	tx_sof_o,
	tx_data_o,
	tx_eof_o,
	tx_ready_i
);
	reg _sv2v_0;
	parameter [31:0] N_REQ_P = 6;
	parameter [(2 * N_REQ_P) - 1:0] PRIO_MAP_P = 12'h6c9;
	parameter [N_REQ_P - 1:0] SOLICITED_MASK_P = 6'b100101;
	parameter [31:0] AGING_MS_P = 10;
	parameter [31:0] TX_STD_SLOTS_P = 4;
	parameter [31:0] CNT_W_P = 16;
	localparam [31:0] SLOT_W_C = $clog2(TX_STD_SLOTS_P + 1);
	input wire clk_i;
	input wire rst_n;
	input wire tick_ms_i;
	input wire [N_REQ_P - 1:0] req_valid_i;
	input wire [(N_REQ_P * SLOT_W_C) - 1:0] tx_slot_i;
	input wire start_abort_i;
	output wire [N_REQ_P - 1:0] gnt_o;
	output reg [(N_REQ_P * CNT_W_P) - 1:0] gnt_count_o;
	output wire ser_req_o;
	output wire [SLOT_W_C - 1:0] ser_slot_o;
	input wire ser_valid_i;
	input wire [7:0] ser_data_i;
	input wire ser_last_i;
	output wire ser_ready_o;
	output wire tx_valid_o;
	output wire tx_sof_o;
	output wire [7:0] tx_data_o;
	output wire tx_eof_o;
	input wire tx_ready_i;
	localparam [31:0] REQ_IX_W_C = (N_REQ_P <= 1 ? 1 : $clog2(N_REQ_P));
	localparam [31:0] AGE_W_C = (AGING_MS_P == 0 ? 1 : $clog2(AGING_MS_P + 1));
	function automatic [AGE_W_C - 1:0] sv2v_cast_E8235;
		input reg [AGE_W_C - 1:0] inp;
		sv2v_cast_E8235 = inp;
	endfunction
	localparam [AGE_W_C - 1:0] AGE_SAT_C = sv2v_cast_E8235(AGING_MS_P);
	reg [1:0] arb_st_r;
	reg [SLOT_W_C - 1:0] slot_r;
	reg [REQ_IX_W_C - 1:0] owner_r;
	reg start_sent_r;
	reg sof_pend_r;
	reg pace_nonsol_r;
	reg [N_REQ_P - 1:0] gnt_r;
	reg [AGE_W_C - 1:0] age_r [0:N_REQ_P - 1];
	reg [CNT_W_P - 1:0] cnt_r [0:N_REQ_P - 1];
	reg [N_REQ_P - 1:0] aged_w;
	function automatic signed [31:0] sv2v_cast_32_signed;
		input reg signed [31:0] inp;
		sv2v_cast_32_signed = inp;
	endfunction
	always @(*) begin : aged_flags
		if (_sv2v_0)
			;
		begin : sv2v_autoblock_1
			reg signed [31:0] i;
			for (i = 0; i < sv2v_cast_32_signed(N_REQ_P); i = i + 1)
				aged_w[i] = age_r[i] == AGE_SAT_C;
		end
	end
	reg [N_REQ_P - 1:0] pend_r;
	reg [N_REQ_P - 1:0] pend_w;
	reg sol_pend_w;
	reg [N_REQ_P - 1:0] elig_w;
	reg pick_ok_w;
	reg [REQ_IX_W_C - 1:0] pick_w;
	localparam [2:0] pp_pkg_PP_SLOT_NULL_C = 3'd7;
	function automatic [SLOT_W_C - 1:0] sv2v_cast_63BED;
		input reg [SLOT_W_C - 1:0] inp;
		sv2v_cast_63BED = inp;
	endfunction
	always @(posedge clk_i) begin : slot_qualify
		if (!rst_n)
			pend_r <= 1'sb0;
		else begin : sv2v_autoblock_2
			reg signed [31:0] i;
			for (i = 0; i < sv2v_cast_32_signed(N_REQ_P); i = i + 1)
				pend_r[i] <= req_valid_i[i] && (tx_slot_i[i * SLOT_W_C+:SLOT_W_C] != sv2v_cast_63BED(pp_pkg_PP_SLOT_NULL_C));
		end
	end
	function automatic signed [REQ_IX_W_C - 1:0] sv2v_cast_46903_signed;
		input reg signed [REQ_IX_W_C - 1:0] inp;
		sv2v_cast_46903_signed = inp;
	endfunction
	always @(*) begin : selection
		reg [2:0] key_w;
		reg [2:0] best_w;
		if (_sv2v_0)
			;
		pend_w = pend_r & req_valid_i;
		sol_pend_w = |(pend_w & SOLICITED_MASK_P);
		elig_w = (pace_nonsol_r && sol_pend_w ? pend_w & SOLICITED_MASK_P : pend_w);
		pick_ok_w = 1'b0;
		pick_w = 1'sb0;
		best_w = 3'b111;
		begin : sv2v_autoblock_3
			reg signed [31:0] i;
			for (i = 0; i < sv2v_cast_32_signed(N_REQ_P); i = i + 1)
				begin
					key_w = {~aged_w[i], PRIO_MAP_P[2 * i+:2]};
					if (elig_w[i] && (!pick_ok_w || (key_w < best_w))) begin
						pick_ok_w = 1'b1;
						pick_w = sv2v_cast_46903_signed(i);
						best_w = key_w;
					end
				end
		end
	end
	wire select_w;
	wire accept_w;
	wire abort_w;
	wire consume_w;
	wire eof_w;
	assign select_w = (arb_st_r == 2'd0) && pick_ok_w;
	assign accept_w = ((arb_st_r == 2'd1) && !start_sent_r) && !start_abort_i;
	assign abort_w = ((arb_st_r == 2'd1) && !start_sent_r) && start_abort_i;
	assign consume_w = ser_valid_i && tx_ready_i;
	assign eof_w = consume_w && ser_last_i;
	always @(posedge clk_i) begin : arbiter_fsm
		if (!rst_n) begin
			arb_st_r <= 2'd0;
			slot_r <= 1'sb0;
			owner_r <= 1'sb0;
			start_sent_r <= 1'b0;
			sof_pend_r <= 1'b0;
			pace_nonsol_r <= 1'b0;
			gnt_r <= 1'sb0;
		end
		else begin
			gnt_r <= 1'sb0;
			case (arb_st_r)
				2'd0:
					if (select_w) begin
						arb_st_r <= 2'd1;
						slot_r <= tx_slot_i[pick_w * SLOT_W_C+:SLOT_W_C];
						owner_r <= pick_w;
						start_sent_r <= 1'b0;
						sof_pend_r <= 1'b1;
					end
				2'd1:
					if (abort_w) begin
						arb_st_r <= 2'd0;
						start_sent_r <= 1'b0;
						sof_pend_r <= 1'b0;
					end
					else begin
						if (accept_w) begin
							start_sent_r <= 1'b1;
							gnt_r[owner_r] <= 1'b1;
							pace_nonsol_r <= !SOLICITED_MASK_P[owner_r];
						end
						if (sof_pend_r && consume_w)
							sof_pend_r <= 1'b0;
						if (eof_w)
							arb_st_r <= 2'd0;
						else if (ser_valid_i)
							arb_st_r <= 2'd2;
					end
				2'd2: begin
					if (sof_pend_r && consume_w)
						sof_pend_r <= 1'b0;
					if (eof_w)
						arb_st_r <= 2'd0;
				end
				default: arb_st_r <= 2'd0;
			endcase
		end
	end
	function automatic signed [AGE_W_C - 1:0] sv2v_cast_E8235_signed;
		input reg signed [AGE_W_C - 1:0] inp;
		sv2v_cast_E8235_signed = inp;
	endfunction
	always @(posedge clk_i) begin : aging
		if (!rst_n) begin : sv2v_autoblock_4
			reg signed [31:0] i;
			for (i = 0; i < sv2v_cast_32_signed(N_REQ_P); i = i + 1)
				age_r[i] <= 1'sb0;
		end
		else begin : sv2v_autoblock_5
			reg signed [31:0] i;
			for (i = 0; i < sv2v_cast_32_signed(N_REQ_P); i = i + 1)
				if (accept_w && (owner_r == sv2v_cast_46903_signed(i)))
					age_r[i] <= 1'sb0;
				else if (!pend_w[i])
					age_r[i] <= 1'sb0;
				else if (tick_ms_i && (age_r[i] != AGE_SAT_C))
					age_r[i] <= age_r[i] + sv2v_cast_E8235_signed(1);
		end
	end
	function automatic signed [CNT_W_P - 1:0] sv2v_cast_CAE1C_signed;
		input reg signed [CNT_W_P - 1:0] inp;
		sv2v_cast_CAE1C_signed = inp;
	endfunction
	always @(posedge clk_i) begin : grant_counters
		if (!rst_n) begin : sv2v_autoblock_6
			reg signed [31:0] i;
			for (i = 0; i < sv2v_cast_32_signed(N_REQ_P); i = i + 1)
				cnt_r[i] <= 1'sb0;
		end
		else if (accept_w)
			cnt_r[owner_r] <= cnt_r[owner_r] + sv2v_cast_CAE1C_signed(1);
	end
	assign ser_req_o = (arb_st_r == 2'd1) && (start_sent_r || !start_abort_i);
	assign ser_slot_o = slot_r;
	assign ser_ready_o = tx_ready_i;
	assign tx_valid_o = ser_valid_i;
	assign tx_data_o = ser_data_i;
	assign tx_sof_o = ser_valid_i && sof_pend_r;
	assign tx_eof_o = ser_valid_i && ser_last_i;
	assign gnt_o = gnt_r;
	always @(*) begin : count_out
		if (_sv2v_0)
			;
		begin : sv2v_autoblock_7
			reg signed [31:0] i;
			for (i = 0; i < sv2v_cast_32_signed(N_REQ_P); i = i + 1)
				gnt_count_o[i * CNT_W_P+:CNT_W_P] = cnt_r[i];
		end
	end
	initial _sv2v_0 = 0;
endmodule
`default_nettype wire
`default_nettype none
module KL_pp_tx_slots (
	clk_i,
	rst_n,
	alloc_req_i,
	oversize_i,
	alloc_gnt_o,
	alloc_slot_o,
	wr_slot_i,
	wr_addr_i,
	wr_valid_i,
	wr_data_i,
	wr_commit_i,
	wr_len_i,
	hold_valid_i,
	hold_slot_i,
	release_valid_i,
	release_slot_i,
	ser_req_i,
	ser_slot_i,
	ser_valid_o,
	ser_data_o,
	ser_last_o,
	ser_ready_i,
	slots_ready_o,
	slots_free_o
);
	reg _sv2v_0;
	parameter [31:0] TX_STD_SLOTS_P = 4;
	parameter [31:0] TX_STD_BYTES_P = 576;
	parameter [31:0] TX_OVERSIZE_BYTES_P = 1600;
	input wire clk_i;
	input wire rst_n;
	input wire alloc_req_i;
	input wire oversize_i;
	output wire alloc_gnt_o;
	output wire [$clog2(TX_STD_SLOTS_P + 1) - 1:0] alloc_slot_o;
	input wire [$clog2(TX_STD_SLOTS_P + 1) - 1:0] wr_slot_i;
	input wire [$clog2(TX_OVERSIZE_BYTES_P + 1) - 1:0] wr_addr_i;
	input wire wr_valid_i;
	input wire [7:0] wr_data_i;
	input wire wr_commit_i;
	input wire [$clog2(TX_OVERSIZE_BYTES_P + 1) - 1:0] wr_len_i;
	input wire hold_valid_i;
	input wire [$clog2(TX_STD_SLOTS_P + 1) - 1:0] hold_slot_i;
	input wire release_valid_i;
	input wire [$clog2(TX_STD_SLOTS_P + 1) - 1:0] release_slot_i;
	input wire ser_req_i;
	input wire [$clog2(TX_STD_SLOTS_P + 1) - 1:0] ser_slot_i;
	output wire ser_valid_o;
	output wire [7:0] ser_data_o;
	output wire ser_last_o;
	input wire ser_ready_i;
	output reg [TX_STD_SLOTS_P:0] slots_ready_o;
	output reg [$clog2(TX_STD_SLOTS_P + 2) - 1:0] slots_free_o;
	localparam [31:0] N_SLOTS_C = TX_STD_SLOTS_P + 1;
	localparam [31:0] OVERSIZE_IX_C = TX_STD_SLOTS_P;
	localparam [31:0] MEM_BYTES_C = (TX_STD_SLOTS_P * TX_STD_BYTES_P) + TX_OVERSIZE_BYTES_P;
	localparam [31:0] SLOT_W_C = $clog2(N_SLOTS_C);
	localparam [31:0] LEN_W_C = $clog2(TX_OVERSIZE_BYTES_P + 1);
	localparam [31:0] ADDR_W_C = $clog2(MEM_BYTES_C);
	localparam [31:0] FREE_W_C = $clog2(N_SLOTS_C + 1);
	function automatic [31:0] sv2v_cast_32;
		input reg [31:0] inp;
		sv2v_cast_32 = inp;
	endfunction
	function automatic [ADDR_W_C - 1:0] sv2v_cast_81A7A;
		input reg [ADDR_W_C - 1:0] inp;
		sv2v_cast_81A7A = inp;
	endfunction
	function automatic [ADDR_W_C - 1:0] slot_base_f;
		input reg [SLOT_W_C - 1:0] s;
		slot_base_f = sv2v_cast_81A7A(sv2v_cast_32(s) * TX_STD_BYTES_P);
	endfunction
	function automatic [LEN_W_C - 1:0] sv2v_cast_E8FD1;
		input reg [LEN_W_C - 1:0] inp;
		sv2v_cast_E8FD1 = inp;
	endfunction
	function automatic [LEN_W_C - 1:0] slot_cap_f;
		input reg [SLOT_W_C - 1:0] s;
		slot_cap_f = (sv2v_cast_32(s) == OVERSIZE_IX_C ? sv2v_cast_E8FD1(TX_OVERSIZE_BYTES_P) : sv2v_cast_E8FD1(TX_STD_BYTES_P));
	endfunction
	reg [1:0] st_r [0:(1 << SLOT_W_C) - 1];
	reg [LEN_W_C - 1:0] len_r [0:(1 << SLOT_W_C) - 1];
	reg [(1 << SLOT_W_C) - 1:0] held_r;
	reg [(1 << SLOT_W_C) - 1:0] release_pend_r;
	reg alloc_gnt_r;
	reg [SLOT_W_C - 1:0] alloc_slot_r;
	reg run_r;
	reg out_valid_r;
	reg out_last_r;
	reg [SLOT_W_C - 1:0] cur_slot_r;
	reg [LEN_W_C - 1:0] fetch_idx_r;
	reg pick_ok_w;
	reg [SLOT_W_C - 1:0] pick_w;
	function automatic [SLOT_W_C - 1:0] sv2v_cast_63BED;
		input reg [SLOT_W_C - 1:0] inp;
		sv2v_cast_63BED = inp;
	endfunction
	function automatic signed [SLOT_W_C - 1:0] sv2v_cast_63BED_signed;
		input reg signed [SLOT_W_C - 1:0] inp;
		sv2v_cast_63BED_signed = inp;
	endfunction
	function automatic signed [31:0] sv2v_cast_32_signed;
		input reg signed [31:0] inp;
		sv2v_cast_32_signed = inp;
	endfunction
	always @(*) begin : alloc_pick
		if (_sv2v_0)
			;
		pick_ok_w = 1'b0;
		pick_w = 1'sb0;
		if (oversize_i) begin
			pick_ok_w = st_r[OVERSIZE_IX_C] == 2'd0;
			pick_w = sv2v_cast_63BED(OVERSIZE_IX_C);
		end
		else begin : sv2v_autoblock_1
			reg signed [31:0] i;
			for (i = sv2v_cast_32_signed(TX_STD_SLOTS_P) - 1; i >= 0; i = i - 1)
				if (st_r[i] == 2'd0) begin
					pick_ok_w = 1'b1;
					pick_w = sv2v_cast_63BED_signed(i);
				end
		end
	end
	wire grant_w;
	wire commit_w;
	wire ser_start_w;
	wire ser_zero_w;
	wire consume_w;
	wire done_w;
	wire rd_en_w;
	wire [LEN_W_C - 1:0] cur_len_w;
	assign grant_w = alloc_req_i && pick_ok_w;
	assign commit_w = wr_commit_i && (st_r[wr_slot_i] == 2'd1);
	assign cur_len_w = len_r[cur_slot_r];
	assign consume_w = out_valid_r && ser_ready_i;
	assign done_w = consume_w && out_last_r;
	assign ser_start_w = (((!run_r && ser_req_i) && (st_r[ser_slot_i] == 2'd2)) && (len_r[ser_slot_i] != {LEN_W_C {1'sb0}})) && !(release_valid_i && (release_slot_i == ser_slot_i));
	assign ser_zero_w = (((!run_r && ser_req_i) && (st_r[ser_slot_i] == 2'd2)) && (len_r[ser_slot_i] == {LEN_W_C {1'sb0}})) && !(release_valid_i && (release_slot_i == ser_slot_i));
	assign rd_en_w = (run_r && (fetch_idx_r < cur_len_w)) && (!out_valid_r || ser_ready_i);
	always @(posedge clk_i) begin : slot_state
		if (!rst_n) begin
			begin : sv2v_autoblock_2
				reg signed [31:0] i;
				for (i = 0; i < (1 << SLOT_W_C); i = i + 1)
					begin
						st_r[i] <= 2'd0;
						len_r[i] <= 1'sb0;
					end
			end
			alloc_gnt_r <= 1'b0;
			alloc_slot_r <= 1'sb0;
			held_r <= 1'sb0;
			release_pend_r <= 1'sb0;
		end
		else begin
			alloc_gnt_r <= grant_w;
			if (grant_w) begin
				alloc_slot_r <= pick_w;
				st_r[pick_w] <= 2'd1;
			end
			if (commit_w) begin
				st_r[wr_slot_i] <= 2'd2;
				len_r[wr_slot_i] <= (wr_len_i > slot_cap_f(wr_slot_i) ? slot_cap_f(wr_slot_i) : wr_len_i);
			end
			if (hold_valid_i && (sv2v_cast_32(hold_slot_i) < N_SLOTS_C))
				held_r[hold_slot_i] <= 1'b1;
			if (release_valid_i && (sv2v_cast_32(release_slot_i) < N_SLOTS_C)) begin
				held_r[release_slot_i] <= 1'b0;
				if (st_r[release_slot_i] == 2'd3)
					release_pend_r[release_slot_i] <= 1'b1;
				else if ((st_r[release_slot_i] == 2'd2) || (st_r[release_slot_i] == 2'd1)) begin
					st_r[release_slot_i] <= 2'd0;
					release_pend_r[release_slot_i] <= 1'b0;
				end
			end
			if (ser_start_w)
				st_r[ser_slot_i] <= 2'd3;
			if (ser_zero_w)
				st_r[ser_slot_i] <= 2'd0;
			if (done_w) begin
				if ((held_r[cur_slot_r] && !release_pend_r[cur_slot_r]) && !(release_valid_i && (release_slot_i == cur_slot_r)))
					st_r[cur_slot_r] <= 2'd2;
				else begin
					st_r[cur_slot_r] <= 2'd0;
					held_r[cur_slot_r] <= 1'b0;
					release_pend_r[cur_slot_r] <= 1'b0;
				end
			end
		end
	end
	function automatic signed [LEN_W_C - 1:0] sv2v_cast_E8FD1_signed;
		input reg signed [LEN_W_C - 1:0] inp;
		sv2v_cast_E8FD1_signed = inp;
	endfunction
	always @(posedge clk_i) begin : serializer
		if (!rst_n) begin
			run_r <= 1'b0;
			out_valid_r <= 1'b0;
			out_last_r <= 1'b0;
			cur_slot_r <= 1'sb0;
			fetch_idx_r <= 1'sb0;
		end
		else if (ser_start_w) begin
			run_r <= 1'b1;
			cur_slot_r <= ser_slot_i;
			fetch_idx_r <= 1'sb0;
		end
		else if (run_r) begin
			if (rd_en_w) begin
				fetch_idx_r <= fetch_idx_r + sv2v_cast_E8FD1_signed(1);
				out_valid_r <= 1'b1;
				out_last_r <= fetch_idx_r == (cur_len_w - sv2v_cast_E8FD1_signed(1));
			end
			else if (consume_w) begin
				out_valid_r <= 1'b0;
				if (out_last_r) begin
					out_last_r <= 1'b0;
					run_r <= 1'b0;
				end
			end
		end
	end
	reg [7:0] mem_r [0:MEM_BYTES_C - 1];
	reg [7:0] rd_q_r;
	wire wr_en_w;
	wire [ADDR_W_C - 1:0] wr_madr_w;
	wire [ADDR_W_C - 1:0] rd_madr_w;
	assign wr_en_w = (wr_valid_i && (st_r[wr_slot_i] == 2'd1)) && (wr_addr_i < slot_cap_f(wr_slot_i));
	assign wr_madr_w = slot_base_f(wr_slot_i) + sv2v_cast_81A7A(wr_addr_i);
	assign rd_madr_w = slot_base_f(cur_slot_r) + sv2v_cast_81A7A(fetch_idx_r);
	always @(posedge clk_i) begin : mem_write
		if (wr_en_w)
			mem_r[wr_madr_w] <= wr_data_i;
	end
	always @(posedge clk_i) begin : mem_read
		if (rd_en_w)
			rd_q_r <= mem_r[rd_madr_w];
	end
	assign alloc_gnt_o = alloc_gnt_r;
	assign alloc_slot_o = alloc_slot_r;
	assign ser_valid_o = out_valid_r;
	assign ser_data_o = rd_q_r;
	assign ser_last_o = out_last_r;
	function automatic signed [FREE_W_C - 1:0] sv2v_cast_5E54D_signed;
		input reg signed [FREE_W_C - 1:0] inp;
		sv2v_cast_5E54D_signed = inp;
	endfunction
	always @(*) begin : status
		if (_sv2v_0)
			;
		slots_free_o = 1'sb0;
		begin : sv2v_autoblock_3
			reg signed [31:0] i;
			for (i = 0; i < sv2v_cast_32_signed(N_SLOTS_C); i = i + 1)
				begin
					slots_ready_o[i] = st_r[i] == 2'd2;
					if (st_r[i] == 2'd0)
						slots_free_o = slots_free_o + sv2v_cast_5E54D_signed(1);
				end
		end
	end
	initial _sv2v_0 = 0;
endmodule
`default_nettype wire
`default_nettype none
module KL_srp_admission (
	clk_i,
	rst_n,
	req_i,
	max_frame_i,
	interval_frames_i,
	port_rate_bps_i,
	sr_admitted_o,
	granted_slope_bps_o,
	sum_slope_bps_o,
	over_limit_o,
	round_done_o
);
	reg _sv2v_0;
	parameter [31:0] N_SOURCES_P = 8;
	localparam [31:0] SRC_W_C = (N_SOURCES_P > 1 ? $clog2(N_SOURCES_P) : 1);
	input wire clk_i;
	input wire rst_n;
	input wire [N_SOURCES_P - 1:0] req_i;
	input wire [(N_SOURCES_P * 16) - 1:0] max_frame_i;
	input wire [(N_SOURCES_P * 16) - 1:0] interval_frames_i;
	input wire [31:0] port_rate_bps_i;
	output reg [N_SOURCES_P - 1:0] sr_admitted_o;
	output reg [(N_SOURCES_P * 32) - 1:0] granted_slope_bps_o;
	output wire [31:0] sum_slope_bps_o;
	output wire over_limit_o;
	output reg round_done_o;
	localparam [16:0] L2_OVERHEAD_C = 17'd22;
	localparam [16:0] MIN_L2_BYTES_C = 17'd68;
	localparam [16:0] WIRE_OVERHEAD_C = 17'd20;
	localparam [32:0] BPS_PER_IVB_C = 33'd64000;
	localparam [32:0] IV_MAX_C = 33'd67108;
	localparam [31:0] SLOPE_SAT_C = 32'hffffffff;
	wire [31:0] limit_w;
	assign limit_w = (port_rate_bps_i >> 1) + (port_rate_bps_i >> 2);
	reg [SRC_W_C - 1:0] cidx_r;
	reg [SRC_W_C - 1:0] cidx_q1_r;
	reg [SRC_W_C - 1:0] cidx_q2_r;
	reg [16:0] frame_bytes_r;
	reg [32:0] iv_bytes_r;
	reg [(N_SOURCES_P * 32) - 1:0] slope_q_r;
	wire [16:0] f_raw_w;
	wire [32:0] slope_prod_w;
	assign f_raw_w = {1'b0, max_frame_i[cidx_r * 16+:16]} + L2_OVERHEAD_C;
	assign slope_prod_w = {16'd0, iv_bytes_r[16:0]} * BPS_PER_IVB_C;
	function automatic [31:0] sv2v_cast_32;
		input reg [31:0] inp;
		sv2v_cast_32 = inp;
	endfunction
	function automatic signed [SRC_W_C - 1:0] sv2v_cast_14954_signed;
		input reg signed [SRC_W_C - 1:0] inp;
		sv2v_cast_14954_signed = inp;
	endfunction
	always @(posedge clk_i) begin : slope_walk
		if (!rst_n) begin
			cidx_r <= 1'sb0;
			cidx_q1_r <= 1'sb0;
			cidx_q2_r <= 1'sb0;
			frame_bytes_r <= 1'sb0;
			iv_bytes_r <= 1'sb0;
			slope_q_r <= 1'sb0;
		end
		else begin
			cidx_r <= (sv2v_cast_32(cidx_r) == (N_SOURCES_P - 1) ? {SRC_W_C {1'sb0}} : cidx_r + sv2v_cast_14954_signed(1));
			cidx_q1_r <= cidx_r;
			cidx_q2_r <= cidx_q1_r;
			frame_bytes_r <= (f_raw_w < MIN_L2_BYTES_C ? MIN_L2_BYTES_C : f_raw_w) + WIRE_OVERHEAD_C;
			iv_bytes_r <= {16'd0, interval_frames_i[cidx_q1_r * 16+:16]} * {16'd0, frame_bytes_r};
			slope_q_r[cidx_q2_r * 32+:32] <= (iv_bytes_r > IV_MAX_C ? SLOPE_SAT_C : slope_prod_w[31:0]);
		end
	end
	reg [SRC_W_C - 1:0] aidx_r;
	reg [31:0] acc_r;
	reg over_acc_r;
	reg [N_SOURCES_P - 1:0] wgrant_r;
	reg [(N_SOURCES_P * 32) - 1:0] wgslope_r;
	reg [N_SOURCES_P - 1:0] grant_r;
	reg [(N_SOURCES_P * 32) - 1:0] gslope_r;
	reg [31:0] sum_r;
	reg over_r;
	wire [32:0] cand_w;
	wire fit_w;
	wire refuse_w;
	wire round_w;
	assign cand_w = {1'b0, acc_r} + {1'b0, slope_q_r[aidx_r * 32+:32]};
	assign fit_w = req_i[aidx_r] && (cand_w <= {1'b0, limit_w});
	assign refuse_w = req_i[aidx_r] && !fit_w;
	assign round_w = sv2v_cast_32(aidx_r) == (N_SOURCES_P - 1);
	reg [N_SOURCES_P - 1:0] wgrant_now_w;
	reg [(N_SOURCES_P * 32) - 1:0] wgslope_now_w;
	always @(*) begin : grant_merge
		if (_sv2v_0)
			;
		wgrant_now_w = wgrant_r;
		wgslope_now_w = wgslope_r;
		wgrant_now_w[aidx_r] = fit_w;
		wgslope_now_w[aidx_r * 32+:32] = (fit_w ? slope_q_r[aidx_r * 32+:32] : 32'd0);
	end
	always @(posedge clk_i) begin : admission_walk
		if (!rst_n) begin
			aidx_r <= 1'sb0;
			acc_r <= 32'd0;
			over_acc_r <= 1'b0;
			wgrant_r <= 1'sb0;
			wgslope_r <= 1'sb0;
			grant_r <= 1'sb0;
			gslope_r <= 1'sb0;
			sum_r <= 32'd0;
			over_r <= 1'b0;
			round_done_o <= 1'b0;
		end
		else begin
			round_done_o <= 1'b0;
			if (round_w) begin
				grant_r <= wgrant_now_w;
				gslope_r <= wgslope_now_w;
				sum_r <= (fit_w ? cand_w[31:0] : acc_r);
				over_r <= over_acc_r | refuse_w;
				round_done_o <= 1'b1;
				aidx_r <= 1'sb0;
				acc_r <= 32'd0;
				over_acc_r <= 1'b0;
				wgrant_r <= 1'sb0;
				wgslope_r <= 1'sb0;
			end
			else begin
				wgrant_r <= wgrant_now_w;
				wgslope_r <= wgslope_now_w;
				acc_r <= (fit_w ? cand_w[31:0] : acc_r);
				over_acc_r <= over_acc_r | refuse_w;
				aidx_r <= aidx_r + sv2v_cast_14954_signed(1);
			end
		end
	end
	always @(*) begin : publish
		if (_sv2v_0)
			;
		begin : sv2v_autoblock_1
			reg [31:0] s;
			for (s = 0; s < N_SOURCES_P; s = s + 1)
				begin
					sr_admitted_o[s] = grant_r[s] && req_i[s];
					granted_slope_bps_o[s * 32+:32] = (grant_r[s] && req_i[s] ? gslope_r[s * 32+:32] : 32'd0);
				end
		end
	end
	assign sum_slope_bps_o = sum_r;
	assign over_limit_o = over_r;
	initial _sv2v_0 = 0;
endmodule
`default_nettype wire
`default_nettype none
module KL_srp_decoder (
	clk_i,
	rst_n,
	mrp_valid_i,
	mrp_data_i,
	mrp_last_i,
	mrp_msrp_i,
	mrp_ready_o,
	evt_valid_o,
	evt_msrp_o,
	evt_attr_type_o,
	evt_stream_id_o,
	evt_da_o,
	evt_vid_o,
	evt_mrp_event_o,
	evt_fourpacked_o,
	evt_max_frame_size_o,
	evt_max_interval_frames_o,
	evt_priority_o,
	evt_rank_o,
	evt_acc_latency_o,
	evt_failure_system_id_o,
	evt_failure_code_o,
	evt_class_id_o,
	evt_class_a_o,
	la_msrp_o,
	la_mvrp_o,
	pdu_done_o,
	pdu_ok_o,
	pdu_malformed_o,
	listlen_bad_o,
	dbg_listlen_cnt_o
);
	reg _sv2v_0;
	parameter [31:0] TP_DEPTH_P = 1024;
	input wire clk_i;
	input wire rst_n;
	input wire mrp_valid_i;
	input wire [7:0] mrp_data_i;
	input wire mrp_last_i;
	input wire mrp_msrp_i;
	output reg mrp_ready_o;
	output reg evt_valid_o;
	output reg evt_msrp_o;
	output reg [7:0] evt_attr_type_o;
	output reg [63:0] evt_stream_id_o;
	output reg [47:0] evt_da_o;
	output reg [15:0] evt_vid_o;
	output reg [2:0] evt_mrp_event_o;
	output reg [1:0] evt_fourpacked_o;
	output reg [15:0] evt_max_frame_size_o;
	output reg [15:0] evt_max_interval_frames_o;
	output reg [7:0] evt_priority_o;
	output reg evt_rank_o;
	output reg [31:0] evt_acc_latency_o;
	output reg [63:0] evt_failure_system_id_o;
	output reg [7:0] evt_failure_code_o;
	output reg [7:0] evt_class_id_o;
	output reg evt_class_a_o;
	output reg la_msrp_o;
	output reg la_mvrp_o;
	output reg pdu_done_o;
	output reg pdu_ok_o;
	output reg pdu_malformed_o;
	output reg listlen_bad_o;
	output reg [15:0] dbg_listlen_cnt_o;
	localparam [31:0] PTR_W_C = $clog2(TP_DEPTH_P);
	reg [3:0] state_r;
	reg app_msrp_r;
	reg [7:0] attr_type_r;
	reg [7:0] attr_len_r;
	reg [15:0] listlen_decl_r;
	reg [15:0] listlen_cnt_r;
	reg [7:0] vhdr1_r;
	reg [12:0] values_left_r;
	reg [5:0] fv_idx_r;
	reg last_seen_r;
	reg [63:0] sid_r;
	reg [47:0] da_r;
	reg [15:0] vid_r;
	reg [15:0] mfs_r;
	reg [15:0] mif_r;
	reg [7:0] pr_r;
	reg [31:0] lat_r;
	reg [63:0] sysid_r;
	reg [7:0] fcode_r;
	reg [7:0] dcid_r;
	reg [7:0] dprio_r;
	reg [7:0] pend_byte_r;
	reg [7:0] fp_byte_r;
	reg [1:0] idx_r;
	reg [2:0] slot_left_r;
	reg [12:0] store_left_r;
	reg [7:0] tp_ram [0:TP_DEPTH_P - 1];
	reg [PTR_W_C:0] tp_wptr_r;
	reg [PTR_W_C - 1:0] tp_rd_byte_r;
	reg [1:0] tp_rd_dig_r;
	reg [7:0] tp_rdata_r;
	wire [PTR_W_C - 1:0] tp_raddr_w;
	wire tp_we_w;
	wire accept_w;
	assign accept_w = mrp_valid_i && mrp_ready_o;
	always @(*) begin : ready_map
		if (_sv2v_0)
			;
		mrp_ready_o = !((state_r == 4'd10) || (state_r == 4'd13));
	end
	reg len_ok_w;
	localparam [7:0] srp_pkg_SRP_FV_LEN_DOMAIN_C = 8'd4;
	localparam [7:0] srp_pkg_SRP_FV_LEN_LISTENER_C = 8'd8;
	localparam [7:0] srp_pkg_SRP_FV_LEN_TALKER_ADV_C = 8'd25;
	localparam [7:0] srp_pkg_SRP_FV_LEN_TALKER_FAILED_C = 8'd34;
	localparam [7:0] srp_pkg_SRP_FV_LEN_VID_C = 8'd2;
	localparam [7:0] srp_pkg_SRP_MSRP_ATTR_DOMAIN_C = 8'd4;
	localparam [7:0] srp_pkg_SRP_MSRP_ATTR_LISTENER_C = 8'd3;
	localparam [7:0] srp_pkg_SRP_MSRP_ATTR_TALKER_ADV_C = 8'd1;
	localparam [7:0] srp_pkg_SRP_MSRP_ATTR_TALKER_FAILED_C = 8'd2;
	localparam [7:0] srp_pkg_SRP_MVRP_ATTR_VID_C = 8'd1;
	always @(*) begin : alen_check
		if (_sv2v_0)
			;
		if (app_msrp_r)
			(* full_case, parallel_case *)
			case (attr_type_r)
				srp_pkg_SRP_MSRP_ATTR_TALKER_ADV_C: len_ok_w = mrp_data_i == srp_pkg_SRP_FV_LEN_TALKER_ADV_C;
				srp_pkg_SRP_MSRP_ATTR_TALKER_FAILED_C: len_ok_w = mrp_data_i == srp_pkg_SRP_FV_LEN_TALKER_FAILED_C;
				srp_pkg_SRP_MSRP_ATTR_LISTENER_C: len_ok_w = mrp_data_i == srp_pkg_SRP_FV_LEN_LISTENER_C;
				srp_pkg_SRP_MSRP_ATTR_DOMAIN_C: len_ok_w = mrp_data_i == srp_pkg_SRP_FV_LEN_DOMAIN_C;
				default: len_ok_w = 1'b0;
			endcase
		else
			len_ok_w = (attr_type_r == srp_pkg_SRP_MVRP_ATTR_VID_C) && (mrp_data_i == srp_pkg_SRP_FV_LEN_VID_C);
	end
	wire is_listener_w;
	wire is_domain_w;
	assign is_listener_w = app_msrp_r && (attr_type_r == srp_pkg_SRP_MSRP_ATTR_LISTENER_C);
	assign is_domain_w = app_msrp_r && (attr_type_r == srp_pkg_SRP_MSRP_ATTR_DOMAIN_C);
	wire in_list_w;
	assign in_list_w = (((((state_r == 4'd6) || (state_r == 4'd7)) || (state_r == 4'd8)) || (state_r == 4'd9)) || (state_r == 4'd11)) || (state_r == 4'd12);
	wire [2:0] tpd_digit_w;
	wire [2:0] fpd_digit_w;
	wire [2:0] cur_digit_w;
	reg [1:0] fp_code_w;
	function automatic [2:0] srp_pkg_srp_tp_digit;
		input reg [7:0] b;
		input reg [1:0] idx;
		reg [7:0] q;
		begin
			(* full_case, parallel_case *)
			case (idx)
				2'd0: q = b / 8'd36;
				2'd1: q = (b / 8'd6) % 8'd6;
				default: q = b % 8'd6;
			endcase
			srp_pkg_srp_tp_digit = q[2:0];
		end
	endfunction
	assign tpd_digit_w = srp_pkg_srp_tp_digit(pend_byte_r, idx_r);
	assign fpd_digit_w = srp_pkg_srp_tp_digit(tp_rdata_r, tp_rd_dig_r);
	assign cur_digit_w = (state_r == 4'd13 ? fpd_digit_w : tpd_digit_w);
	always @(*) begin : fp_code_sel
		if (_sv2v_0)
			;
		(* full_case, parallel_case *)
		case (idx_r)
			2'd0: fp_code_w = fp_byte_r[7:6];
			2'd1: fp_code_w = fp_byte_r[5:4];
			2'd2: fp_code_w = fp_byte_r[3:2];
			default: fp_code_w = fp_byte_r[1:0];
		endcase
	end
	function automatic [((PTR_W_C + 0) >= 0 ? PTR_W_C + 1 : 1 - (PTR_W_C + 0)) - 1:0] sv2v_cast_7F4A0;
		input reg [((PTR_W_C + 0) >= 0 ? PTR_W_C + 1 : 1 - (PTR_W_C + 0)) - 1:0] inp;
		sv2v_cast_7F4A0 = inp;
	endfunction
	assign tp_we_w = (accept_w && (state_r == 4'd11)) && (tp_wptr_r < sv2v_cast_7F4A0(TP_DEPTH_P));
	function automatic signed [PTR_W_C - 1:0] sv2v_cast_2FDC0_signed;
		input reg signed [PTR_W_C - 1:0] inp;
		sv2v_cast_2FDC0_signed = inp;
	endfunction
	assign tp_raddr_w = ((state_r == 4'd13) && (tp_rd_dig_r == 2'd2) ? tp_rd_byte_r + sv2v_cast_2FDC0_signed(1) : tp_rd_byte_r);
	always @(posedge clk_i) begin : tp_buffer
		if (tp_we_w)
			tp_ram[tp_wptr_r[PTR_W_C - 1:0]] <= mrp_data_i;
		tp_rdata_r <= tp_ram[tp_raddr_w];
	end
	task pdu_fail_t;
		begin
			pdu_done_o <= 1'b1;
			pdu_ok_o <= 1'b0;
			pdu_malformed_o <= 1'b1;
			last_seen_r <= 1'b0;
			state_r <= 4'd0;
		end
	endtask
	localparam [7:0] srp_pkg_SRP_CLASS_A_ID_C = 8'd6;
	localparam [2:0] srp_pkg_SRP_LEAVEALL_EV_C = 3'd1;
	function automatic signed [((PTR_W_C + 0) >= 0 ? PTR_W_C + 1 : 1 - (PTR_W_C + 0)) - 1:0] sv2v_cast_7F4A0_signed;
		input reg signed [((PTR_W_C + 0) >= 0 ? PTR_W_C + 1 : 1 - (PTR_W_C + 0)) - 1:0] inp;
		sv2v_cast_7F4A0_signed = inp;
	endfunction
	always @(posedge clk_i) begin : decode_walk
		if (!rst_n) begin
			state_r <= 4'd0;
			app_msrp_r <= 1'b0;
			attr_type_r <= 8'd0;
			attr_len_r <= 8'd0;
			listlen_decl_r <= 16'd0;
			listlen_cnt_r <= 16'd0;
			vhdr1_r <= 8'd0;
			values_left_r <= 13'd0;
			fv_idx_r <= 6'd0;
			last_seen_r <= 1'b0;
			sid_r <= 64'd0;
			da_r <= 48'd0;
			vid_r <= 16'd0;
			mfs_r <= 16'd0;
			mif_r <= 16'd0;
			pr_r <= 8'd0;
			lat_r <= 32'd0;
			sysid_r <= 64'd0;
			fcode_r <= 8'd0;
			dcid_r <= 8'd0;
			dprio_r <= 8'd0;
			pend_byte_r <= 8'd0;
			fp_byte_r <= 8'd0;
			idx_r <= 2'd0;
			slot_left_r <= 3'd0;
			store_left_r <= 13'd0;
			tp_wptr_r <= 1'sb0;
			tp_rd_byte_r <= 1'sb0;
			tp_rd_dig_r <= 2'd0;
			evt_valid_o <= 1'b0;
			evt_msrp_o <= 1'b0;
			evt_attr_type_o <= 8'd0;
			evt_stream_id_o <= 64'd0;
			evt_da_o <= 48'd0;
			evt_vid_o <= 16'd0;
			evt_mrp_event_o <= 3'd0;
			evt_fourpacked_o <= 2'd0;
			evt_max_frame_size_o <= 16'd0;
			evt_max_interval_frames_o <= 16'd0;
			evt_priority_o <= 8'd0;
			evt_rank_o <= 1'b0;
			evt_acc_latency_o <= 32'd0;
			evt_failure_system_id_o <= 64'd0;
			evt_failure_code_o <= 8'd0;
			evt_class_id_o <= 8'd0;
			evt_class_a_o <= 1'b0;
			la_msrp_o <= 1'b0;
			la_mvrp_o <= 1'b0;
			pdu_done_o <= 1'b0;
			pdu_ok_o <= 1'b0;
			pdu_malformed_o <= 1'b0;
			listlen_bad_o <= 1'b0;
			dbg_listlen_cnt_o <= 16'd0;
		end
		else begin
			evt_valid_o <= 1'b0;
			la_msrp_o <= 1'b0;
			la_mvrp_o <= 1'b0;
			pdu_done_o <= 1'b0;
			listlen_bad_o <= 1'b0;
			if (accept_w) begin
				if (in_list_w)
					listlen_cnt_r <= listlen_cnt_r + 16'd1;
				(* full_case, parallel_case *)
				case (state_r)
					4'd0: begin
						app_msrp_r <= mrp_msrp_i;
						if (mrp_last_i)
							pdu_fail_t;
						else
							state_r <= 4'd1;
					end
					4'd1:
						if (mrp_data_i == 8'h00) begin
							if (mrp_last_i)
								pdu_fail_t;
							else
								state_r <= 4'd2;
						end
						else begin
							attr_type_r <= mrp_data_i;
							if (mrp_last_i)
								pdu_fail_t;
							else
								state_r <= 4'd3;
						end
					4'd2:
						if (mrp_data_i == 8'h00) begin
							pdu_done_o <= 1'b1;
							pdu_ok_o <= 1'b1;
							pdu_malformed_o <= 1'b0;
							state_r <= (mrp_last_i ? 4'd0 : 4'd14);
						end
						else if (mrp_last_i)
							pdu_fail_t;
						else
							state_r <= 4'd15;
					4'd3: begin
						attr_len_r <= mrp_data_i;
						if (!len_ok_w) begin
							if (mrp_last_i)
								pdu_fail_t;
							else
								state_r <= 4'd15;
						end
						else if (mrp_last_i)
							pdu_fail_t;
						else
							state_r <= (app_msrp_r ? 4'd4 : 4'd6);
					end
					4'd4: begin
						listlen_decl_r[15:8] <= mrp_data_i;
						if (mrp_last_i)
							pdu_fail_t;
						else
							state_r <= 4'd5;
					end
					4'd5: begin
						listlen_decl_r[7:0] <= mrp_data_i;
						listlen_cnt_r <= 16'd0;
						if (mrp_last_i)
							pdu_fail_t;
						else
							state_r <= 4'd6;
					end
					4'd6: begin
						vhdr1_r <= mrp_data_i;
						if (mrp_last_i)
							pdu_fail_t;
						else
							state_r <= 4'd7;
					end
					4'd7:
						if ((vhdr1_r == 8'h00) && (mrp_data_i == 8'h00)) begin
							dbg_listlen_cnt_o <= listlen_cnt_r + 16'd1;
							if (app_msrp_r && ((listlen_cnt_r + 16'd1) != listlen_decl_r))
								listlen_bad_o <= 1'b1;
							if (mrp_last_i)
								pdu_fail_t;
							else
								state_r <= 4'd1;
						end
						else begin
							if (vhdr1_r[7:5] == srp_pkg_SRP_LEAVEALL_EV_C) begin
								la_msrp_o <= app_msrp_r;
								la_mvrp_o <= ~app_msrp_r;
							end
							values_left_r <= {vhdr1_r[4:0], mrp_data_i};
							fv_idx_r <= 6'd0;
							sid_r <= 64'd0;
							da_r <= 48'd0;
							vid_r <= 16'd0;
							mfs_r <= 16'd0;
							mif_r <= 16'd0;
							pr_r <= 8'd0;
							lat_r <= 32'd0;
							sysid_r <= 64'd0;
							fcode_r <= 8'd0;
							dcid_r <= 8'd0;
							dprio_r <= 8'd0;
							if (mrp_last_i)
								pdu_fail_t;
							else
								state_r <= 4'd8;
						end
					4'd8: begin
						if (app_msrp_r)
							(* full_case, parallel_case *)
							case (attr_type_r)
								srp_pkg_SRP_MSRP_ATTR_TALKER_ADV_C, srp_pkg_SRP_MSRP_ATTR_TALKER_FAILED_C:
									if (fv_idx_r < 6'd8)
										sid_r <= {sid_r[55:0], mrp_data_i};
									else if (fv_idx_r < 6'd14)
										da_r <= {da_r[39:0], mrp_data_i};
									else if (fv_idx_r < 6'd16)
										vid_r <= {vid_r[7:0], mrp_data_i};
									else if (fv_idx_r < 6'd18)
										mfs_r <= {mfs_r[7:0], mrp_data_i};
									else if (fv_idx_r < 6'd20)
										mif_r <= {mif_r[7:0], mrp_data_i};
									else if (fv_idx_r == 6'd20)
										pr_r <= mrp_data_i;
									else if (fv_idx_r < 6'd25)
										lat_r <= {lat_r[23:0], mrp_data_i};
									else if (fv_idx_r < 6'd33)
										sysid_r <= {sysid_r[55:0], mrp_data_i};
									else
										fcode_r <= mrp_data_i;
								srp_pkg_SRP_MSRP_ATTR_LISTENER_C: sid_r <= {sid_r[55:0], mrp_data_i};
								default:
									if (fv_idx_r == 6'd0)
										dcid_r <= mrp_data_i;
									else if (fv_idx_r == 6'd1)
										dprio_r <= mrp_data_i;
									else
										vid_r <= {vid_r[7:0], mrp_data_i};
							endcase
						else
							vid_r <= {vid_r[7:0], mrp_data_i};
						fv_idx_r <= fv_idx_r + 6'd1;
						if (fv_idx_r == (attr_len_r[5:0] - 6'd1)) begin
							if (mrp_last_i)
								pdu_fail_t;
							else if (values_left_r == 13'd0)
								state_r <= 4'd6;
							else if (is_listener_w) begin
								store_left_r <= values_left_r;
								tp_wptr_r <= 1'sb0;
								tp_rd_byte_r <= 1'sb0;
								tp_rd_dig_r <= 2'd0;
								state_r <= 4'd11;
							end
							else
								state_r <= 4'd9;
						end
						else if (mrp_last_i)
							pdu_fail_t;
					end
					4'd9: begin
						pend_byte_r <= mrp_data_i;
						idx_r <= 2'd0;
						slot_left_r <= (values_left_r > 13'd3 ? 3'd3 : values_left_r[2:0]);
						last_seen_r <= mrp_last_i;
						state_r <= 4'd10;
					end
					4'd11:
						if (tp_wptr_r >= sv2v_cast_7F4A0(TP_DEPTH_P)) begin
							if (mrp_last_i)
								pdu_fail_t;
							else
								state_r <= 4'd15;
						end
						else begin
							tp_wptr_r <= tp_wptr_r + sv2v_cast_7F4A0_signed(1);
							if (store_left_r <= 13'd3) begin
								if (mrp_last_i)
									pdu_fail_t;
								else
									state_r <= 4'd12;
							end
							else begin
								store_left_r <= store_left_r - 13'd3;
								if (mrp_last_i)
									pdu_fail_t;
							end
						end
					4'd12: begin
						fp_byte_r <= mrp_data_i;
						idx_r <= 2'd0;
						slot_left_r <= (values_left_r > 13'd4 ? 3'd4 : values_left_r[2:0]);
						last_seen_r <= mrp_last_i;
						state_r <= 4'd13;
					end
					4'd14:
						if (mrp_last_i)
							state_r <= 4'd0;
					4'd15:
						if (mrp_last_i)
							pdu_fail_t;
					default: state_r <= 4'd0;
				endcase
			end
			if ((state_r == 4'd10) || (state_r == 4'd13)) begin
				if (cur_digit_w > 3'd5) begin
					if (last_seen_r)
						pdu_fail_t;
					else
						state_r <= 4'd15;
				end
				else begin
					evt_valid_o <= 1'b1;
					evt_msrp_o <= app_msrp_r;
					evt_attr_type_o <= attr_type_r;
					evt_stream_id_o <= sid_r;
					evt_da_o <= da_r;
					evt_vid_o <= vid_r;
					evt_mrp_event_o <= cur_digit_w;
					evt_fourpacked_o <= (state_r == 4'd13 ? fp_code_w : 2'd0);
					evt_max_frame_size_o <= mfs_r;
					evt_max_interval_frames_o <= mif_r;
					evt_priority_o <= (is_domain_w ? dprio_r : {5'd0, pr_r[7:5]});
					evt_rank_o <= pr_r[4];
					evt_acc_latency_o <= lat_r;
					evt_failure_system_id_o <= sysid_r;
					evt_failure_code_o <= fcode_r;
					evt_class_id_o <= dcid_r;
					evt_class_a_o <= is_domain_w && (dcid_r == srp_pkg_SRP_CLASS_A_ID_C);
					if (is_domain_w) begin
						dcid_r <= dcid_r + 8'd1;
						dprio_r <= dprio_r + 8'd1;
					end
					else if (app_msrp_r) begin
						sid_r[15:0] <= sid_r[15:0] + 16'd1;
						da_r <= da_r + 48'd1;
					end
					else
						vid_r <= vid_r + 16'd1;
					values_left_r <= values_left_r - 13'd1;
					idx_r <= idx_r + 2'd1;
					slot_left_r <= slot_left_r - 3'd1;
					if (state_r == 4'd13) begin
						if (tp_rd_dig_r == 2'd2) begin
							tp_rd_dig_r <= 2'd0;
							tp_rd_byte_r <= tp_rd_byte_r + sv2v_cast_2FDC0_signed(1);
						end
						else
							tp_rd_dig_r <= tp_rd_dig_r + 2'd1;
					end
					if (slot_left_r == 3'd1) begin
						if (values_left_r == 13'd1) begin
							if (last_seen_r)
								pdu_fail_t;
							else
								state_r <= 4'd6;
							last_seen_r <= 1'b0;
						end
						else if (last_seen_r)
							pdu_fail_t;
						else
							state_r <= (state_r == 4'd10 ? 4'd9 : 4'd12);
					end
				end
			end
		end
	end
	initial _sv2v_0 = 0;
endmodule
`default_nettype wire
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
	periodic_tick_i,
	leaveall_tick_i,
	dom_ev_valid_o,
	dom_ev_event_o,
	dom_ev_value_o,
	dom_ev_ready_i,
	evt_domain_change_o,
	class_a_prio_o,
	class_a_vid_o,
	adopted_o
);
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
	input wire periodic_tick_i;
	input wire leaveall_tick_i;
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
	wire covers6_w;
	wire [7:0] surf_prio_w;
	wire link_rise_w;
	wire link_fall_w;
	wire q_empty_w;
	assign covers6_w = (rxdom_class_id_i <= CLASS_A_ID_C) && (({6'd0, rxdom_class_id_i} + {1'b0, rxdom_nov_i}) > 14'd6);
	assign surf_prio_w = rxdom_prio_i + (CLASS_A_ID_C - rxdom_class_id_i);
	assign link_rise_w = link_up_i && !link_q_r;
	assign link_fall_w = !link_up_i && link_q_r;
	assign q_empty_w = !q0_valid_r && !q1_valid_r;
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
			evt_domain_change_o <= 1'b0;
		end
		else begin
			evt_domain_change_o <= 1'b0;
			link_q_r <= link_up_i;
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
			end
			if ((periodic_tick_i || leaveall_tick_i) && declared_r)
				rejoin_pend_r <= 1'b1;
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
			end
			else if (link_rise_w) begin
				q0_valid_r <= 1'b1;
				q0_ev_r <= EV_NEW_C;
				q0_val_r <= {CLASS_A_ID_C, DEF_PRIO_P, DEF_VID_P};
				declared_r <= 1'b1;
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
				adopted_r <= 1'b1;
				rx_pend_v_r <= 1'b0;
				evt_domain_change_o <= 1'b1;
			end
			else if ((rejoin_pend_r && declared_r) && q_empty_w) begin
				q0_valid_r <= 1'b1;
				q0_ev_r <= EV_JOININ_C;
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
endmodule
`default_nettype wire
`default_nettype none
module KL_srp_encoder (
	clk_i,
	rst_n,
	ev_valid_i,
	ev_ready_o,
	ev_app_i,
	ev_attr_type_i,
	ev_event_i,
	ev_fourpack_i,
	ev_value_i,
	ev_drop_o,
	join_tick_i,
	leaveall_i,
	own_mac_i,
	alloc_req_o,
	oversize_o,
	alloc_slot_i,
	alloc_gnt_i,
	wr_slot_o,
	wr_addr_o,
	wr_valid_o,
	wr_data_o,
	wr_commit_o,
	wr_len_o,
	txreq_valid_o,
	txreq_slot_o,
	txreq_ready_i,
	dbg_cnt_msrp_o,
	dbg_cnt_mvrp_o
);
	reg _sv2v_0;
	parameter [31:0] DEPTH_P = 12;
	parameter [31:0] TX_STD_BYTES_P = 576;
	parameter [31:0] TX_OVERSIZE_BYTES_P = 1600;
	input wire clk_i;
	input wire rst_n;
	input wire ev_valid_i;
	output wire ev_ready_o;
	input wire ev_app_i;
	input wire [7:0] ev_attr_type_i;
	input wire [2:0] ev_event_i;
	input wire [1:0] ev_fourpack_i;
	input wire [271:0] ev_value_i;
	output wire ev_drop_o;
	input wire [1:0] join_tick_i;
	input wire [1:0] leaveall_i;
	input wire [47:0] own_mac_i;
	output wire alloc_req_o;
	output wire oversize_o;
	localparam [2:0] pp_pkg_PP_SLOT_NULL_C = 3'd7;
	input wire [2:0] alloc_slot_i;
	input wire alloc_gnt_i;
	output wire [2:0] wr_slot_o;
	output wire [$clog2(TX_OVERSIZE_BYTES_P + 1) - 1:0] wr_addr_o;
	output wire wr_valid_o;
	output wire [7:0] wr_data_o;
	output wire wr_commit_o;
	output wire [$clog2(TX_OVERSIZE_BYTES_P + 1) - 1:0] wr_len_o;
	output wire txreq_valid_o;
	output wire [2:0] txreq_slot_o;
	input wire txreq_ready_i;
	output wire [$clog2(DEPTH_P + 1) - 1:0] dbg_cnt_msrp_o;
	output wire [$clog2(DEPTH_P + 1) - 1:0] dbg_cnt_mvrp_o;
	localparam [31:0] SLOT_W_C = 3;
	localparam [31:0] ADDR_W_C = $clog2(TX_OVERSIZE_BYTES_P + 1);
	localparam [31:0] CNT_W_C = $clog2(DEPTH_P + 1);
	localparam [31:0] IDX_W_C = (DEPTH_P > 1 ? $clog2(DEPTH_P) : 1);
	localparam [31:0] WORST_BYTES_C = (39 + (DEPTH_P * 37)) + 2;
	generate
		if (WORST_BYTES_C > TX_STD_BYTES_P) begin : g_depth_check
			initial $display("Error [elaboration] $VALIDATION_STORAGE/reviews/r247-520-r1/protocol-processor/hdl/srp/KL_srp_encoder.sv:119:5 - KL_srp_encoder.g_depth_check\n msg: ", "DEPTH_P drain cannot fit a standard TX slot");
		end
	endgenerate
	localparam [0:0] APP_MSRP_C = 1'b0;
	localparam [0:0] APP_MVRP_C = 1'b1;
	localparam [47:0] MSRP_DA_C = 48'h0180c200000e;
	localparam [47:0] MVRP_DA_C = 48'h0180c2000021;
	localparam [15:0] MSRP_ETYPE_C = 16'h22ea;
	localparam [15:0] MVRP_ETYPE_C = 16'h88f5;
	localparam [7:0] ATTR_TALKER_ADV_C = 8'd1;
	localparam [7:0] ATTR_TALKER_FAIL_C = 8'd2;
	localparam [7:0] ATTR_LISTENER_C = 8'd3;
	localparam [7:0] ATTR_DOMAIN_C = 8'd4;
	localparam [7:0] ATTR_MVRP_VID_C = 8'd1;
	function automatic [5:0] attr_len_f;
		input reg app;
		input reg [7:0] t;
		reg [0:1] _sv2v_jump;
		begin
			_sv2v_jump = 2'b00;
			if (app == APP_MVRP_C) begin
				attr_len_f = 6'd2;
				_sv2v_jump = 2'b11;
			end
			if (_sv2v_jump == 2'b00)
				case (t)
					ATTR_TALKER_ADV_C: begin
						attr_len_f = 6'd25;
						_sv2v_jump = 2'b11;
					end
					ATTR_TALKER_FAIL_C: begin
						attr_len_f = 6'd34;
						_sv2v_jump = 2'b11;
					end
					ATTR_LISTENER_C: begin
						attr_len_f = 6'd8;
						_sv2v_jump = 2'b11;
					end
					ATTR_DOMAIN_C: begin
						attr_len_f = 6'd4;
						_sv2v_jump = 2'b11;
					end
					default: begin
						attr_len_f = 6'd0;
						_sv2v_jump = 2'b11;
					end
				endcase
		end
	endfunction
	function automatic succ_f;
		input reg app;
		input reg [7:0] t;
		input reg [271:0] prev;
		input reg [271:0] nxt;
		reg [63:0] sid_w;
		reg [47:0] da_w;
		reg [7:0] cid_w;
		reg [7:0] pri_w;
		reg [15:0] vid_w;
		reg [0:1] _sv2v_jump;
		begin
			_sv2v_jump = 2'b00;
			sid_w = prev[271:208] + 64'd1;
			da_w = prev[207:160] + 48'd1;
			cid_w = prev[271:264] + 8'd1;
			pri_w = prev[263:256] + 8'd1;
			vid_w = prev[271:256] + 16'd1;
			if (app == APP_MVRP_C) begin
				succ_f = (nxt[271:256] == vid_w) && (nxt[255:0] == prev[255:0]);
				_sv2v_jump = 2'b11;
			end
			if (_sv2v_jump == 2'b00)
				case (t)
					ATTR_TALKER_ADV_C, ATTR_TALKER_FAIL_C: begin
						succ_f = ((nxt[271:208] == sid_w) && (nxt[207:160] == da_w)) && (nxt[159:0] == prev[159:0]);
						_sv2v_jump = 2'b11;
					end
					ATTR_LISTENER_C: begin
						succ_f = (nxt[271:208] == sid_w) && (nxt[207:0] == prev[207:0]);
						_sv2v_jump = 2'b11;
					end
					ATTR_DOMAIN_C: begin
						succ_f = ((nxt[271:264] == cid_w) && (nxt[263:256] == pri_w)) && (nxt[255:0] == prev[255:0]);
						_sv2v_jump = 2'b11;
					end
					default: begin
						succ_f = 1'b0;
						_sv2v_jump = 2'b11;
					end
				endcase
		end
	endfunction
	function automatic signed [31:0] sv2v_cast_32_signed;
		input reg signed [31:0] inp;
		sv2v_cast_32_signed = inp;
	endfunction
	function automatic [7:0] fv_byte_f;
		input reg [271:0] v;
		input reg [5:0] i;
		fv_byte_f = v[271 - (8 * sv2v_cast_32_signed(i))-:8];
	endfunction
	function automatic [7:0] mac_byte_f;
		input reg [47:0] v;
		input reg [5:0] i;
		mac_byte_f = v[47 - (8 * sv2v_cast_32_signed(i))-:8];
	endfunction
	function automatic [7:0] sv2v_cast_8;
		input reg [7:0] inp;
		sv2v_cast_8 = inp;
	endfunction
	function automatic [7:0] pack3_f;
		input reg [2:0] a;
		input reg [2:0] b;
		input reg [2:0] c;
		pack3_f = ((sv2v_cast_8(a) * 8'd36) + (sv2v_cast_8(b) * 8'd6)) + sv2v_cast_8(c);
	endfunction
	function automatic [7:0] pack4_f;
		input reg [1:0] a;
		input reg [1:0] b;
		input reg [1:0] c;
		input reg [1:0] d;
		pack4_f = (((sv2v_cast_8(a) * 8'd64) + (sv2v_cast_8(b) * 8'd16)) + (sv2v_cast_8(c) * 8'd4)) + sv2v_cast_8(d);
	endfunction
	localparam [31:0] MSRP_EW_C = 285;
	localparam [31:0] MVRP_EW_C = 19;
	(* ram_style = "distributed" *) reg [284:0] msrp_ram_r [0:DEPTH_P - 1];
	reg [18:0] mvrp_ram_r [0:DEPTH_P - 1];
	reg [284:0] msrp_q_r;
	reg [18:0] mvrp_q_r;
	reg [CNT_W_C - 1:0] cnt_msrp_r;
	reg [CNT_W_C - 1:0] cnt_mvrp_r;
	reg [CNT_W_C - 1:0] rd_idx_r;
	reg [3:0] st_r;
	reg cur_app_r;
	reg [CNT_W_C - 1:0] drain_n_r;
	reg [2:0] slot_r;
	reg [ADDR_W_C - 1:0] waddr_r;
	reg [5:0] bidx_r;
	reg [ADDR_W_C - 1:0] ll_addr_r;
	reg msg_open_r;
	reg [7:0] msg_type_r;
	reg first_vec_r;
	reg close_for_pdu_r;
	reg run_open_r;
	reg [7:0] run_type_r;
	reg [271:0] run_first_r;
	reg [271:0] run_last_r;
	reg [CNT_W_C - 1:0] run_len_r;
	reg [(DEPTH_P * 3) - 1:0] run_ev_r;
	reg [(DEPTH_P * 2) - 1:0] run_fp_r;
	reg hold_valid_r;
	reg [7:0] hold_type_r;
	reg [2:0] hold_ev_r;
	reg [1:0] hold_fp_r;
	reg [271:0] hold_val_r;
	reg [1:0] join_pend_r;
	reg [1:0] la_pend_r;
	wire valid_type_w;
	wire ev_accept_w;
	wire push_msrp_w;
	wire push_mvrp_w;
	wire go0_w;
	wire go1_w;
	wire start0_w;
	wire start1_w;
	wire busy_app_w;
	wire tgt_full_w;
	wire start_tgt_w;
	assign valid_type_w = (ev_app_i == APP_MVRP_C ? ev_attr_type_i == ATTR_MVRP_VID_C : (ev_attr_type_i >= ATTR_TALKER_ADV_C) && (ev_attr_type_i <= ATTR_DOMAIN_C));
	assign ev_accept_w = ev_valid_i && ev_ready_o;
	assign push_msrp_w = (ev_accept_w && valid_type_w) && (ev_app_i == APP_MSRP_C);
	assign push_mvrp_w = (ev_accept_w && valid_type_w) && (ev_app_i == APP_MVRP_C);
	assign ev_drop_o = ev_accept_w && !valid_type_w;
	assign go0_w = join_tick_i[0] || join_pend_r[0];
	assign go1_w = join_tick_i[1] || join_pend_r[1];
	assign start0_w = ((st_r == 4'd0) && go0_w) && (cnt_msrp_r != {CNT_W_C {1'sb0}});
	assign start1_w = (((st_r == 4'd0) && !start0_w) && go1_w) && (cnt_mvrp_r != {CNT_W_C {1'sb0}});
	assign busy_app_w = (st_r != 4'd0) && (cur_app_r == ev_app_i);
	function automatic [CNT_W_C - 1:0] sv2v_cast_7417F;
		input reg [CNT_W_C - 1:0] inp;
		sv2v_cast_7417F = inp;
	endfunction
	assign tgt_full_w = (ev_app_i == APP_MSRP_C ? cnt_msrp_r == sv2v_cast_7417F(DEPTH_P) : cnt_mvrp_r == sv2v_cast_7417F(DEPTH_P));
	assign start_tgt_w = (ev_app_i == APP_MSRP_C ? start0_w : start1_w);
	assign ev_ready_o = (!tgt_full_w && !busy_app_w) && !start_tgt_w;
	always @(posedge clk_i) begin : pend_write
		if (push_msrp_w)
			msrp_ram_r[cnt_msrp_r[IDX_W_C - 1:0]] <= {ev_attr_type_i, ev_event_i, ev_fourpack_i, ev_value_i};
		if (push_mvrp_w)
			mvrp_ram_r[cnt_mvrp_r[IDX_W_C - 1:0]] <= {ev_event_i, ev_value_i[271:256]};
	end
	always @(posedge clk_i) begin : pend_read
		msrp_q_r <= msrp_ram_r[rd_idx_r[IDX_W_C - 1:0]];
		mvrp_q_r <= mvrp_ram_r[rd_idx_r[IDX_W_C - 1:0]];
	end
	reg [7:0] cap_type_w;
	reg [2:0] cap_ev_w;
	reg [1:0] cap_fp_w;
	reg [271:0] cap_val_w;
	wire open_w;
	wire ext_w;
	wire more_w;
	always @(*) begin : cap_unpack
		if (_sv2v_0)
			;
		if (cur_app_r == APP_MSRP_C) begin
			cap_type_w = msrp_q_r[284:277];
			cap_ev_w = msrp_q_r[276:274];
			cap_fp_w = msrp_q_r[273:272];
			cap_val_w = msrp_q_r[271:0];
		end
		else begin
			cap_type_w = ATTR_MVRP_VID_C;
			cap_ev_w = mvrp_q_r[18:16];
			cap_fp_w = 2'd0;
			cap_val_w = {mvrp_q_r[15:0], 256'd0};
		end
	end
	assign open_w = !run_open_r;
	assign ext_w = ((run_open_r && (cap_type_w == run_type_r)) && succ_f(cur_app_r, run_type_r, run_last_r, cap_val_w)) && (run_len_r < sv2v_cast_7417F(DEPTH_P));
	function automatic signed [CNT_W_C - 1:0] sv2v_cast_7417F_signed;
		input reg signed [CNT_W_C - 1:0] inp;
		sv2v_cast_7417F_signed = inp;
	endfunction
	assign more_w = (rd_idx_r + sv2v_cast_7417F_signed(1)) < drain_n_r;
	function automatic [31:0] sv2v_cast_32;
		input reg [31:0] inp;
		sv2v_cast_32 = inp;
	endfunction
	function automatic [2:0] run_ev_at_f;
		input reg [5:0] j;
		reg [0:1] _sv2v_jump;
		begin
			_sv2v_jump = 2'b00;
			if (sv2v_cast_32(j) >= sv2v_cast_32(run_len_r)) begin
				run_ev_at_f = 3'd0;
				_sv2v_jump = 2'b11;
			end
			if (_sv2v_jump == 2'b00) begin
				run_ev_at_f = run_ev_r[j[IDX_W_C - 1:0] * 3+:3];
				_sv2v_jump = 2'b11;
			end
		end
	endfunction
	function automatic [1:0] run_fp_at_f;
		input reg [5:0] j;
		reg [0:1] _sv2v_jump;
		begin
			_sv2v_jump = 2'b00;
			if (sv2v_cast_32(j) >= sv2v_cast_32(run_len_r)) begin
				run_fp_at_f = 2'd0;
				_sv2v_jump = 2'b11;
			end
			if (_sv2v_jump == 2'b00) begin
				run_fp_at_f = run_fp_r[j[IDX_W_C - 1:0] * 2+:2];
				_sv2v_jump = 2'b11;
			end
		end
	endfunction
	reg wr_valid_w;
	reg [7:0] wr_data_w;
	reg [5:0] nbytes_w;
	wire last_byte_w;
	wire [47:0] da_sel_w;
	wire [15:0] et_sel_w;
	wire [5:0] alen_w;
	wire [2:0] la3_w;
	wire [12:0] nov_w;
	wire [ADDR_W_C - 1:0] ll_val_w;
	wire [5:0] j3_w;
	wire [5:0] j4_w;
	assign da_sel_w = (cur_app_r == APP_MVRP_C ? MVRP_DA_C : MSRP_DA_C);
	assign et_sel_w = (cur_app_r == APP_MVRP_C ? MVRP_ETYPE_C : MSRP_ETYPE_C);
	assign alen_w = attr_len_f(cur_app_r, run_type_r);
	assign la3_w = (first_vec_r && la_pend_r[cur_app_r] ? 3'd1 : 3'd0);
	function automatic [12:0] sv2v_cast_13;
		input reg [12:0] inp;
		sv2v_cast_13 = inp;
	endfunction
	assign nov_w = sv2v_cast_13(run_len_r);
	function automatic signed [ADDR_W_C - 1:0] sv2v_cast_81A7A_signed;
		input reg signed [ADDR_W_C - 1:0] inp;
		sv2v_cast_81A7A_signed = inp;
	endfunction
	assign ll_val_w = (waddr_r - ll_addr_r) - sv2v_cast_81A7A_signed(2);
	assign j3_w = 6'd3 * bidx_r;
	assign j4_w = 6'd4 * bidx_r;
	function automatic [5:0] sv2v_cast_6;
		input reg [5:0] inp;
		sv2v_cast_6 = inp;
	endfunction
	always @(ll_val_w[7:0] or ll_val_w[10:8] or bidx_r or j4_w or run_fp_r or run_len_r or j4_w or run_fp_r or run_len_r or j4_w or run_fp_r or run_len_r or j4_w or run_fp_r or run_len_r or run_len_r or j3_w or run_ev_r or run_len_r or j3_w or run_ev_r or run_len_r or j3_w or run_ev_r or run_len_r or run_len_r or bidx_r or run_first_r or alen_w or nov_w[7:0] or nov_w[12:8] or la3_w or bidx_r or alen_w or bidx_r or run_type_r or bidx_r or cur_app_r or et_sel_w[7:0] or bidx_r or et_sel_w[15:8] or bidx_r or bidx_r or own_mac_i or bidx_r or bidx_r or da_sel_w or bidx_r or st_r or _sv2v_0) begin : emit_byte
		if (_sv2v_0)
			;
		wr_valid_w = 1'b0;
		wr_data_w = 8'h00;
		nbytes_w = 6'd1;
		(* full_case, parallel_case *)
		case (st_r)
			4'd2: begin
				wr_valid_w = 1'b1;
				nbytes_w = 6'd15;
				if (bidx_r < 6'd6)
					wr_data_w = mac_byte_f(da_sel_w, bidx_r);
				else if (bidx_r < 6'd12)
					wr_data_w = mac_byte_f(own_mac_i, bidx_r - 6'd6);
				else if (bidx_r == 6'd12)
					wr_data_w = et_sel_w[15:8];
				else if (bidx_r == 6'd13)
					wr_data_w = et_sel_w[7:0];
				else
					wr_data_w = 8'h00;
			end
			4'd6: begin
				wr_valid_w = 1'b1;
				nbytes_w = (cur_app_r == APP_MSRP_C ? 6'd4 : 6'd2);
				if (bidx_r == 6'd0)
					wr_data_w = run_type_r;
				else if (bidx_r == 6'd1)
					wr_data_w = {2'd0, alen_w};
				else
					wr_data_w = 8'h00;
			end
			4'd7: begin
				wr_valid_w = 1'b1;
				nbytes_w = 6'd2;
				wr_data_w = (bidx_r == 6'd0 ? {la3_w, nov_w[12:8]} : nov_w[7:0]);
			end
			4'd8: begin
				wr_valid_w = 1'b1;
				nbytes_w = alen_w;
				wr_data_w = fv_byte_f(run_first_r, bidx_r);
			end
			4'd9: begin
				wr_valid_w = 1'b1;
				nbytes_w = (sv2v_cast_6(run_len_r) + 6'd2) / 6'd3;
				wr_data_w = pack3_f(run_ev_at_f(j3_w), run_ev_at_f(j3_w + 6'd1), run_ev_at_f(j3_w + 6'd2));
			end
			4'd10: begin
				wr_valid_w = 1'b1;
				nbytes_w = (sv2v_cast_6(run_len_r) + 6'd3) / 6'd4;
				wr_data_w = pack4_f(run_fp_at_f(j4_w), run_fp_at_f(j4_w + 6'd1), run_fp_at_f(j4_w + 6'd2), run_fp_at_f(j4_w + 6'd3));
			end
			4'd11, 4'd13: begin
				wr_valid_w = 1'b1;
				nbytes_w = 6'd2;
				wr_data_w = 8'h00;
			end
			4'd12: begin
				wr_valid_w = 1'b1;
				nbytes_w = 6'd2;
				wr_data_w = (bidx_r == 6'd0 ? {5'd0, ll_val_w[10:8]} : ll_val_w[7:0]);
			end
			default: wr_valid_w = 1'b0;
		endcase
	end
	assign last_byte_w = wr_valid_w && (bidx_r == (nbytes_w - 6'd1));
	always @(posedge clk_i) begin : enc_fsm
		if (!rst_n) begin
			st_r <= 4'd0;
			cur_app_r <= APP_MSRP_C;
			drain_n_r <= 1'sb0;
			slot_r <= 1'sb0;
			waddr_r <= 1'sb0;
			bidx_r <= 1'sb0;
			ll_addr_r <= 1'sb0;
			msg_open_r <= 1'b0;
			msg_type_r <= 8'd0;
			first_vec_r <= 1'b0;
			close_for_pdu_r <= 1'b0;
			run_open_r <= 1'b0;
			run_type_r <= 8'd0;
			run_first_r <= 1'sb0;
			run_last_r <= 1'sb0;
			run_len_r <= 1'sb0;
			hold_valid_r <= 1'b0;
			hold_type_r <= 8'd0;
			hold_ev_r <= 3'd0;
			hold_fp_r <= 2'd0;
			hold_val_r <= 1'sb0;
			cnt_msrp_r <= 1'sb0;
			cnt_mvrp_r <= 1'sb0;
			rd_idx_r <= 1'sb0;
			join_pend_r <= 2'b00;
			la_pend_r <= 2'b00;
		end
		else begin
			if (push_msrp_w)
				cnt_msrp_r <= cnt_msrp_r + sv2v_cast_7417F_signed(1);
			if (push_mvrp_w)
				cnt_mvrp_r <= cnt_mvrp_r + sv2v_cast_7417F_signed(1);
			if (wr_valid_w) begin
				if (st_r != 4'd12)
					waddr_r <= waddr_r + sv2v_cast_81A7A_signed(1);
				bidx_r <= (last_byte_w ? 6'd0 : bidx_r + 6'd1);
			end
			(* full_case, parallel_case *)
			case (st_r)
				4'd0:
					if (start0_w || start1_w) begin
						cur_app_r <= (start0_w ? APP_MSRP_C : APP_MVRP_C);
						drain_n_r <= (start0_w ? cnt_msrp_r : cnt_mvrp_r);
						if (start0_w)
							join_pend_r[0] <= 1'b0;
						else
							join_pend_r[1] <= 1'b0;
						rd_idx_r <= 1'sb0;
						waddr_r <= 1'sb0;
						bidx_r <= 1'sb0;
						msg_open_r <= 1'b0;
						first_vec_r <= 1'b1;
						run_open_r <= 1'b0;
						hold_valid_r <= 1'b0;
						st_r <= 4'd1;
					end
					else begin
						if (join_pend_r[0] && (cnt_msrp_r == {CNT_W_C {1'sb0}}))
							join_pend_r[0] <= 1'b0;
						if (join_pend_r[1] && (cnt_mvrp_r == {CNT_W_C {1'sb0}}))
							join_pend_r[1] <= 1'b0;
					end
				4'd1:
					if (alloc_gnt_i) begin
						slot_r <= alloc_slot_i;
						bidx_r <= 1'sb0;
						st_r <= 4'd2;
					end
				4'd2:
					if (last_byte_w)
						st_r <= 4'd3;
				4'd3: st_r <= 4'd4;
				4'd4: begin
					rd_idx_r <= rd_idx_r + sv2v_cast_7417F_signed(1);
					if (open_w || ext_w) begin
						if (open_w) begin
							run_open_r <= 1'b1;
							run_type_r <= cap_type_w;
							run_first_r <= cap_val_w;
							run_last_r <= cap_val_w;
							run_ev_r[0+:3] <= cap_ev_w;
							run_fp_r[0+:2] <= cap_fp_w;
							run_len_r <= sv2v_cast_7417F_signed(1);
						end
						else begin
							run_last_r <= cap_val_w;
							run_ev_r[run_len_r[IDX_W_C - 1:0] * 3+:3] <= cap_ev_w;
							run_fp_r[run_len_r[IDX_W_C - 1:0] * 2+:2] <= cap_fp_w;
							run_len_r <= run_len_r + sv2v_cast_7417F_signed(1);
						end
						st_r <= (more_w ? 4'd3 : 4'd5);
					end
					else begin
						hold_type_r <= cap_type_w;
						hold_ev_r <= cap_ev_w;
						hold_fp_r <= cap_fp_w;
						hold_val_r <= cap_val_w;
						hold_valid_r <= 1'b1;
						st_r <= 4'd5;
					end
				end
				4'd5:
					if (!msg_open_r)
						st_r <= 4'd6;
					else if (msg_type_r != run_type_r) begin
						close_for_pdu_r <= 1'b0;
						st_r <= 4'd11;
					end
					else
						st_r <= 4'd7;
				4'd6: begin
					if (bidx_r == 6'd2)
						ll_addr_r <= waddr_r;
					if (last_byte_w) begin
						msg_open_r <= 1'b1;
						msg_type_r <= run_type_r;
						st_r <= 4'd7;
					end
				end
				4'd7:
					if (last_byte_w) begin
						first_vec_r <= 1'b0;
						st_r <= 4'd8;
					end
				4'd8:
					if (last_byte_w)
						st_r <= 4'd9;
				4'd9:
					if (last_byte_w) begin
						if ((cur_app_r == APP_MSRP_C) && (run_type_r == ATTR_LISTENER_C))
							st_r <= 4'd10;
						else if (hold_valid_r) begin
							hold_valid_r <= 1'b0;
							run_type_r <= hold_type_r;
							run_first_r <= hold_val_r;
							run_last_r <= hold_val_r;
							run_ev_r[0+:3] <= hold_ev_r;
							run_fp_r[0+:2] <= hold_fp_r;
							run_len_r <= sv2v_cast_7417F_signed(1);
							st_r <= (rd_idx_r < drain_n_r ? 4'd3 : 4'd5);
						end
						else begin
							run_open_r <= 1'b0;
							close_for_pdu_r <= 1'b1;
							st_r <= 4'd11;
						end
					end
				4'd10:
					if (last_byte_w) begin
						if (hold_valid_r) begin
							hold_valid_r <= 1'b0;
							run_type_r <= hold_type_r;
							run_first_r <= hold_val_r;
							run_last_r <= hold_val_r;
							run_ev_r[0+:3] <= hold_ev_r;
							run_fp_r[0+:2] <= hold_fp_r;
							run_len_r <= sv2v_cast_7417F_signed(1);
							st_r <= (rd_idx_r < drain_n_r ? 4'd3 : 4'd5);
						end
						else begin
							run_open_r <= 1'b0;
							close_for_pdu_r <= 1'b1;
							st_r <= 4'd11;
						end
					end
				4'd11:
					if (last_byte_w) begin
						msg_open_r <= 1'b0;
						if (cur_app_r == APP_MSRP_C)
							st_r <= 4'd12;
						else if (close_for_pdu_r)
							st_r <= 4'd13;
						else
							st_r <= 4'd6;
					end
				4'd12:
					if (last_byte_w)
						st_r <= (close_for_pdu_r ? 4'd13 : 4'd6);
				4'd13:
					if (last_byte_w)
						st_r <= 4'd14;
				4'd14: begin
					if (cur_app_r == APP_MSRP_C)
						cnt_msrp_r <= 1'sb0;
					else
						cnt_mvrp_r <= 1'sb0;
					la_pend_r[cur_app_r] <= 1'b0;
					st_r <= 4'd15;
				end
				4'd15:
					if (txreq_ready_i)
						st_r <= 4'd0;
				default: st_r <= 4'd0;
			endcase
			if (join_tick_i[0] && !start0_w)
				join_pend_r[0] <= 1'b1;
			if (join_tick_i[1] && !start1_w)
				join_pend_r[1] <= 1'b1;
			if (leaveall_i[0])
				la_pend_r[0] <= 1'b1;
			if (leaveall_i[1])
				la_pend_r[1] <= 1'b1;
		end
	end
	assign alloc_req_o = (st_r == 4'd1) && !alloc_gnt_i;
	assign oversize_o = 1'b0;
	assign wr_slot_o = slot_r;
	function automatic [ADDR_W_C - 1:0] sv2v_cast_81A7A;
		input reg [ADDR_W_C - 1:0] inp;
		sv2v_cast_81A7A = inp;
	endfunction
	assign wr_addr_o = (st_r == 4'd12 ? ll_addr_r + sv2v_cast_81A7A(bidx_r) : waddr_r);
	assign wr_valid_o = wr_valid_w;
	assign wr_data_o = wr_data_w;
	assign wr_commit_o = st_r == 4'd14;
	assign wr_len_o = waddr_r;
	assign txreq_valid_o = st_r == 4'd15;
	assign txreq_slot_o = slot_r;
	assign dbg_cnt_msrp_o = cnt_msrp_r;
	assign dbg_cnt_mvrp_o = cnt_mvrp_r;
	initial _sv2v_0 = 0;
endmodule
`default_nettype wire
`default_nettype none
module KL_srp_listener_fsm (
	clk_i,
	rst_n,
	p2p_i,
	ctl_valid_i,
	ctl_ready_o,
	ctl_settle_i,
	ctl_sink_i,
	ctl_stream_id_i,
	ctl_da_i,
	ctl_vid_i,
	evt_valid_i,
	evt_msrp_i,
	evt_attr_type_i,
	evt_stream_id_i,
	evt_da_i,
	evt_vid_i,
	evt_mrp_event_i,
	evt_acc_latency_i,
	evt_failure_system_id_i,
	evt_failure_code_i,
	join_tick_i,
	periodic_tick_i,
	leaveall_rx_i,
	leaveall_own_i,
	txop_done_o,
	ev_valid_o,
	ev_ready_i,
	ev_app_o,
	ev_attr_type_o,
	ev_event_o,
	ev_fourpack_o,
	ev_value_o,
	user_valid_o,
	user_join_o,
	user_vid_o,
	user_ready_i,
	now_ms_i,
	arm_valid_o,
	arm_cancel_o,
	arm_slot_o,
	arm_owner_o,
	arm_deadline_ms_o,
	exp_valid_i,
	exp_slot_i,
	evt_tk_registered_o,
	evt_tk_unregistered_o,
	tk_reg_state_o,
	lstn_decl_state_o,
	acc_latency_o,
	msrp_fail_code_o,
	msrp_fail_bridge_o,
	dbg_app_state_o,
	dbg_reg_state_o
);
	reg _sv2v_0;
	parameter [31:0] N_SINKS_P = 8;
	parameter [31:0] LEAVE_MS_P = 5000;
	parameter [31:0] SLOT_BASE_P = 0;
	parameter [31:0] SLOT_AW_P = 7;
	parameter [7:0] OWNER_BASE_P = 8'h60;
	localparam [31:0] SNK_W_C = (N_SINKS_P > 1 ? $clog2(N_SINKS_P) : 1);
	input wire clk_i;
	input wire rst_n;
	input wire p2p_i;
	input wire ctl_valid_i;
	output wire ctl_ready_o;
	input wire ctl_settle_i;
	input wire [SNK_W_C - 1:0] ctl_sink_i;
	input wire [63:0] ctl_stream_id_i;
	input wire [47:0] ctl_da_i;
	input wire [11:0] ctl_vid_i;
	input wire evt_valid_i;
	input wire evt_msrp_i;
	input wire [7:0] evt_attr_type_i;
	input wire [63:0] evt_stream_id_i;
	input wire [47:0] evt_da_i;
	input wire [15:0] evt_vid_i;
	input wire [2:0] evt_mrp_event_i;
	input wire [31:0] evt_acc_latency_i;
	input wire [63:0] evt_failure_system_id_i;
	input wire [7:0] evt_failure_code_i;
	input wire join_tick_i;
	input wire periodic_tick_i;
	input wire leaveall_rx_i;
	input wire leaveall_own_i;
	output reg txop_done_o;
	output wire ev_valid_o;
	input wire ev_ready_i;
	output wire ev_app_o;
	output wire [7:0] ev_attr_type_o;
	output wire [2:0] ev_event_o;
	output wire [1:0] ev_fourpack_o;
	output wire [271:0] ev_value_o;
	output wire user_valid_o;
	output wire user_join_o;
	output reg [11:0] user_vid_o;
	input wire user_ready_i;
	input wire [31:0] now_ms_i;
	output reg arm_valid_o;
	output reg arm_cancel_o;
	output reg [SLOT_AW_P - 1:0] arm_slot_o;
	output reg [7:0] arm_owner_o;
	output reg [31:0] arm_deadline_ms_o;
	input wire exp_valid_i;
	input wire [SLOT_AW_P - 1:0] exp_slot_i;
	output reg [N_SINKS_P - 1:0] evt_tk_registered_o;
	output reg [N_SINKS_P - 1:0] evt_tk_unregistered_o;
	output reg [(N_SINKS_P * 2) - 1:0] tk_reg_state_o;
	output reg [(N_SINKS_P * 2) - 1:0] lstn_decl_state_o;
	output reg [(N_SINKS_P * 32) - 1:0] acc_latency_o;
	output reg [(N_SINKS_P * 8) - 1:0] msrp_fail_code_o;
	output reg [(N_SINKS_P * 64) - 1:0] msrp_fail_bridge_o;
	output reg [(N_SINKS_P * 4) - 1:0] dbg_app_state_o;
	output reg [(N_SINKS_P * 2) - 1:0] dbg_reg_state_o;
	localparam [3:0] A_VO_C = 4'd0;
	localparam [3:0] A_VP_C = 4'd1;
	localparam [3:0] A_VN_C = 4'd2;
	localparam [3:0] A_AN_C = 4'd3;
	localparam [3:0] A_AA_C = 4'd4;
	localparam [3:0] A_QA_C = 4'd5;
	localparam [3:0] A_LA_C = 4'd6;
	localparam [3:0] A_AO_C = 4'd7;
	localparam [3:0] A_QO_C = 4'd8;
	localparam [3:0] A_AP_C = 4'd9;
	localparam [3:0] A_QP_C = 4'd10;
	localparam [3:0] A_LO_C = 4'd11;
	localparam [3:0] AE_NEW_C = 4'd0;
	localparam [3:0] AE_JOIN_C = 4'd1;
	localparam [3:0] AE_LV_C = 4'd2;
	localparam [3:0] AE_RNEW_C = 4'd3;
	localparam [3:0] AE_RJOININ_C = 4'd4;
	localparam [3:0] AE_RIN_C = 4'd5;
	localparam [3:0] AE_RJOINMT_C = 4'd6;
	localparam [3:0] AE_RMT_C = 4'd7;
	localparam [3:0] AE_RLV_C = 4'd8;
	localparam [3:0] AE_RLA_C = 4'd9;
	localparam [3:0] AE_PER_C = 4'd10;
	localparam [3:0] AE_TX_C = 4'd11;
	localparam [3:0] AE_TXLA_C = 4'd12;
	localparam [1:0] R_MT_C = 2'd0;
	localparam [1:0] R_IN_C = 2'd1;
	localparam [1:0] R_LV_C = 2'd2;
	localparam [1:0] T_NOP_C = 2'd0;
	localparam [1:0] T_ARM_C = 2'd1;
	localparam [1:0] T_CANCEL_C = 2'd2;
	localparam [1:0] D_NOP_C = 2'd0;
	localparam [1:0] D_DECLARE_C = 2'd1;
	localparam [1:0] D_WITHDRAW_C = 2'd2;
	function automatic [3:0] app_next_f;
		input reg [3:0] st;
		input reg [3:0] ev;
		input reg reg_in_i;
		input reg p2p;
		reg [3:0] nx;
		begin
			nx = st;
			case (ev)
				AE_NEW_C:
					if (!(|{st == A_VN_C, st == A_AN_C}))
						nx = A_VN_C;
				AE_JOIN_C:
					case (st)
						A_VO_C: nx = A_VP_C;
						A_LA_C: nx = A_AA_C;
						A_AO_C: nx = A_AP_C;
						A_QO_C: nx = A_QP_C;
						A_LO_C: nx = A_VP_C;
						default: nx = st;
					endcase
				AE_LV_C:
					case (st)
						A_VP_C: nx = A_VO_C;
						A_VN_C, A_AN_C, A_AA_C, A_QA_C: nx = A_LA_C;
						A_AP_C: nx = A_AO_C;
						A_QP_C: nx = A_QO_C;
						default: nx = st;
					endcase
				AE_RNEW_C: nx = st;
				AE_RJOININ_C:
					case (st)
						A_VO_C: nx = (p2p ? st : A_AO_C);
						A_VP_C: nx = (p2p ? st : A_AP_C);
						A_AA_C: nx = A_QA_C;
						A_AO_C: nx = A_QO_C;
						A_AP_C: nx = A_QP_C;
						default: nx = st;
					endcase
				AE_RIN_C:
					if (p2p && (st == A_AA_C))
						nx = A_QA_C;
				AE_RJOINMT_C, AE_RMT_C:
					case (st)
						A_QA_C: nx = A_AA_C;
						A_QO_C: nx = A_AO_C;
						A_QP_C: nx = A_AP_C;
						A_LO_C: nx = A_VO_C;
						default: nx = st;
					endcase
				AE_RLV_C, AE_RLA_C:
					case (st)
						A_VO_C, A_AO_C, A_QO_C: nx = A_LO_C;
						A_AN_C: nx = A_VN_C;
						A_AA_C, A_QA_C, A_AP_C, A_QP_C: nx = A_VP_C;
						default: nx = st;
					endcase
				AE_PER_C:
					case (st)
						A_QA_C: nx = A_AA_C;
						A_QP_C: nx = A_AP_C;
						default: nx = st;
					endcase
				AE_TX_C:
					case (st)
						A_VP_C: nx = A_AA_C;
						A_VN_C: nx = A_AN_C;
						A_AN_C: nx = (reg_in_i ? A_QA_C : A_AA_C);
						A_AA_C: nx = A_QA_C;
						A_LA_C: nx = A_VO_C;
						A_AP_C: nx = A_QA_C;
						A_LO_C: nx = A_VO_C;
						default: nx = st;
					endcase
				AE_TXLA_C:
					case (st)
						A_VO_C, A_LA_C, A_AO_C, A_QO_C: nx = A_LO_C;
						A_VP_C: nx = A_AA_C;
						A_VN_C: nx = A_AN_C;
						A_AN_C, A_AA_C, A_AP_C, A_QP_C: nx = A_QA_C;
						default: nx = st;
					endcase
				default: nx = st;
			endcase
			app_next_f = nx;
		end
	endfunction
	function automatic [3:0] app_msg_f;
		input reg [3:0] st;
		input reg txla;
		input reg reg_in_i;
		reg [2:0] sj_w;
		reg [2:0] s_w;
		reg [3:0] m;
		begin
			sj_w = (reg_in_i ? 3'd1 : 3'd3);
			s_w = (reg_in_i ? 3'd2 : 3'd4);
			if (!txla)
				case (st)
					A_VP_C, A_AA_C, A_AP_C: m = {1'b1, sj_w};
					A_VN_C, A_AN_C: m = 4'h8;
					A_LA_C: m = 4'hd;
					A_LO_C: m = {1'b1, s_w};
					default: m = 4'h0;
				endcase
			else
				case (st)
					A_VP_C: m = {1'b1, s_w};
					A_VN_C, A_AN_C: m = 4'h8;
					A_AA_C, A_QA_C, A_AP_C, A_QP_C: m = {1'b1, sj_w};
					default: m = 4'h0;
				endcase
			app_msg_f = m;
		end
	endfunction
	function automatic app_declaring_f;
		input reg [3:0] st;
		app_declaring_f = |{st == A_VP_C, st == A_VN_C, st == A_AN_C, st == A_AA_C, st == A_QA_C, st == A_AP_C, st == A_QP_C};
	endfunction
	reg [N_SINKS_P - 1:0] rec_valid_r;
	reg [N_SINKS_P - 1:0] armed_r;
	reg [(N_SINKS_P * 64) - 1:0] sid_r;
	reg [(N_SINKS_P * 48) - 1:0] da_r;
	reg [(N_SINKS_P * 12) - 1:0] vid_r;
	reg [(N_SINKS_P * 4) - 1:0] app_r;
	reg [(N_SINKS_P * 2) - 1:0] fourpack_r;
	reg [(N_SINKS_P * 2) - 1:0] decl_pend_r;
	reg [(N_SINKS_P * 2) - 1:0] decl_fp_r;
	reg [N_SINKS_P - 1:0] rla_pend_r;
	reg [N_SINKS_P - 1:0] per_pend_r;
	reg [1:0] walk_r;
	reg [SNK_W_C - 1:0] wsrc_r;
	reg wtxla_r;
	reg tick_pend_r;
	reg laown_pend_r;
	reg [2:0] push_code_r;
	reg [1:0] push_fp_r;
	reg [271:0] push_val_r;
	reg [(N_SINKS_P * 2) - 1:0] reg_r;
	reg [N_SINKS_P - 1:0] rtype_r;
	reg [(N_SINKS_P * 32) - 1:0] lat_r;
	reg [(N_SINKS_P * 8) - 1:0] fcode_r;
	reg [(N_SINKS_P * 64) - 1:0] fsysid_r;
	reg [(N_SINKS_P * 2) - 1:0] tpend_r;
	reg [N_SINKS_P - 1:0] vj_pend_r;
	reg [N_SINKS_P - 1:0] vl_pend_r;
	reg [(N_SINKS_P * 12) - 1:0] vj_vid_r;
	reg [(N_SINKS_P * 12) - 1:0] vl_vid_r;
	reg [N_SINKS_P - 1:0] app_rx_hit_w;
	reg [N_SINKS_P - 1:0] reg_rx_hit_w;
	reg [3:0] rx_app_ev_w;
	reg rx_is_failed_w;
	reg rx_registering_w;
	localparam [7:0] srp_pkg_SRP_MSRP_ATTR_LISTENER_C = 8'd3;
	localparam [7:0] srp_pkg_SRP_MSRP_ATTR_TALKER_ADV_C = 8'd1;
	localparam [7:0] srp_pkg_SRP_MSRP_ATTR_TALKER_FAILED_C = 8'd2;
	always @(*) begin : hit_map
		if (_sv2v_0)
			;
		rx_app_ev_w = {1'b0, evt_mrp_event_i} + AE_RNEW_C;
		rx_is_failed_w = evt_attr_type_i == srp_pkg_SRP_MSRP_ATTR_TALKER_FAILED_C;
		rx_registering_w = ((evt_mrp_event_i == 3'd0) || (evt_mrp_event_i == 3'd1)) || (evt_mrp_event_i == 3'd3);
		begin : sv2v_autoblock_1
			reg [31:0] s;
			for (s = 0; s < N_SINKS_P; s = s + 1)
				begin
					app_rx_hit_w[s] = ((((evt_valid_i && evt_msrp_i) && rec_valid_r[s]) && (evt_attr_type_i == srp_pkg_SRP_MSRP_ATTR_LISTENER_C)) && (evt_mrp_event_i <= 3'd5)) && (evt_stream_id_i == sid_r[s * 64+:64]);
					reg_rx_hit_w[s] = (((((evt_valid_i && evt_msrp_i) && armed_r[s]) && ((evt_attr_type_i == srp_pkg_SRP_MSRP_ATTR_TALKER_ADV_C) || (evt_attr_type_i == srp_pkg_SRP_MSRP_ATTR_TALKER_FAILED_C))) && (evt_stream_id_i == sid_r[s * 64+:64])) && (evt_da_i == da_r[s * 48+:48])) && (evt_vid_i == {4'd0, vid_r[s * 12+:12]});
				end
		end
	end
	wire leaveall_any_w;
	wire exp_hit_w;
	wire [31:0] exp_idx_w;
	reg [N_SINKS_P - 1:0] ind_reg_w;
	reg [N_SINKS_P - 1:0] ind_unreg_w;
	assign leaveall_any_w = leaveall_rx_i || leaveall_own_i;
	function automatic [31:0] sv2v_cast_32;
		input reg [31:0] inp;
		sv2v_cast_32 = inp;
	endfunction
	assign exp_idx_w = sv2v_cast_32(exp_slot_i) - SLOT_BASE_P;
	assign exp_hit_w = exp_valid_i && (exp_idx_w < N_SINKS_P);
	always @(*) begin : reg_ind
		if (_sv2v_0)
			;
		begin : sv2v_autoblock_2
			reg [31:0] s;
			for (s = 0; s < N_SINKS_P; s = s + 1)
				begin
					ind_reg_w[s] = (reg_rx_hit_w[s] && rx_registering_w) && ((reg_r[s * 2+:2] == R_MT_C) || (rtype_r[s] != rx_is_failed_w));
					ind_unreg_w[s] = ((reg_rx_hit_w[s] && (evt_mrp_event_i == 3'd5)) && (reg_r[s * 2+:2] == R_IN_C)) || ((((exp_hit_w && (exp_idx_w == s)) && (reg_r[s * 2+:2] == R_LV_C)) && (tpend_r[s * 2+:2] != T_ARM_C)) && !(reg_rx_hit_w[s] && rx_registering_w));
				end
		end
	end
	wire ctl_acc_w;
	reg [N_SINKS_P - 1:0] app_ev_v_w;
	reg [(N_SINKS_P * 4) - 1:0] app_ev_w;
	reg [N_SINKS_P - 1:0] decl_grant_w;
	reg [N_SINKS_P - 1:0] rla_grant_w;
	reg [N_SINKS_P - 1:0] per_grant_w;
	reg walk_grant_w;
	assign ctl_ready_o = !evt_valid_i;
	assign ctl_acc_w = ctl_valid_i && ctl_ready_o;
	function automatic [SNK_W_C - 1:0] sv2v_cast_B2660;
		input reg [SNK_W_C - 1:0] inp;
		sv2v_cast_B2660 = inp;
	endfunction
	always @(*) begin : app_arb
		if (_sv2v_0)
			;
		walk_grant_w = 1'b0;
		begin : sv2v_autoblock_3
			reg [31:0] s;
			for (s = 0; s < N_SINKS_P; s = s + 1)
				begin
					app_ev_v_w[s] = 1'b0;
					app_ev_w[s * 4+:4] = AE_RNEW_C;
					decl_grant_w[s] = 1'b0;
					rla_grant_w[s] = 1'b0;
					per_grant_w[s] = 1'b0;
					if (app_rx_hit_w[s]) begin
						app_ev_v_w[s] = 1'b1;
						app_ev_w[s * 4+:4] = rx_app_ev_w;
					end
					else if (ctl_acc_w && (ctl_sink_i == sv2v_cast_B2660(s))) begin
						app_ev_v_w[s] = !ctl_settle_i;
						app_ev_w[s * 4+:4] = AE_LV_C;
					end
					else if (decl_pend_r[s * 2+:2] != D_NOP_C) begin
						app_ev_v_w[s] = 1'b1;
						app_ev_w[s * 4+:4] = (decl_pend_r[s * 2+:2] == D_DECLARE_C ? AE_NEW_C : AE_LV_C);
						decl_grant_w[s] = 1'b1;
					end
					else if (rla_pend_r[s] || leaveall_rx_i) begin
						app_ev_v_w[s] = 1'b1;
						app_ev_w[s * 4+:4] = AE_RLA_C;
						rla_grant_w[s] = 1'b1;
					end
					else if (per_pend_r[s] || periodic_tick_i) begin
						app_ev_v_w[s] = 1'b1;
						app_ev_w[s * 4+:4] = AE_PER_C;
						per_grant_w[s] = 1'b1;
					end
					else if ((walk_r == 2'd1) && (wsrc_r == sv2v_cast_B2660(s))) begin
						app_ev_v_w[s] = 1'b1;
						app_ev_w[s * 4+:4] = (wtxla_r ? AE_TXLA_C : AE_TX_C);
						walk_grant_w = 1'b1;
					end
				end
		end
	end
	reg [271:0] wval_w;
	reg [3:0] wmsg_w;
	always @(*) begin : walk_msg
		if (_sv2v_0)
			;
		wval_w = 272'd0;
		wval_w[271:208] = sid_r[wsrc_r * 64+:64];
		wmsg_w = app_msg_f(app_r[wsrc_r * 4+:4], wtxla_r, 1'b0);
	end
	function automatic signed [SNK_W_C - 1:0] sv2v_cast_B2660_signed;
		input reg signed [SNK_W_C - 1:0] inp;
		sv2v_cast_B2660_signed = inp;
	endfunction
	always @(posedge clk_i) begin : app_plane
		if (!rst_n) begin
			rec_valid_r <= 1'sb0;
			armed_r <= 1'sb0;
			sid_r <= 1'sb0;
			da_r <= 1'sb0;
			vid_r <= 1'sb0;
			app_r <= 1'sb0;
			fourpack_r <= 1'sb0;
			decl_pend_r <= 1'sb0;
			decl_fp_r <= 1'sb0;
			rla_pend_r <= 1'sb0;
			per_pend_r <= 1'sb0;
			walk_r <= 2'd0;
			wsrc_r <= 1'sb0;
			wtxla_r <= 1'b0;
			tick_pend_r <= 1'b0;
			laown_pend_r <= 1'b0;
			push_code_r <= 3'd0;
			push_fp_r <= 2'd0;
			push_val_r <= 1'sb0;
			txop_done_o <= 1'b0;
		end
		else begin
			txop_done_o <= 1'b0;
			begin : sv2v_autoblock_4
				reg [31:0] s;
				for (s = 0; s < N_SINKS_P; s = s + 1)
					begin
						if (app_ev_v_w[s])
							app_r[s * 4+:4] <= app_next_f(app_r[s * 4+:4], app_ev_w[s * 4+:4], 1'b0, p2p_i);
						if (ind_reg_w[s]) begin
							decl_pend_r[s * 2+:2] <= D_DECLARE_C;
							decl_fp_r[s * 2+:2] <= (rx_is_failed_w ? 2'd1 : 2'd2);
						end
						else if (ind_unreg_w[s])
							decl_pend_r[s * 2+:2] <= D_WITHDRAW_C;
						else if (decl_grant_w[s])
							decl_pend_r[s * 2+:2] <= D_NOP_C;
						if (decl_grant_w[s] && (decl_pend_r[s * 2+:2] == D_DECLARE_C))
							fourpack_r[s * 2+:2] <= decl_fp_r[s * 2+:2];
						if ((leaveall_rx_i && !rla_grant_w[s]) && (!app_ev_v_w[s] || (app_ev_w[s * 4+:4] != AE_RLA_C)))
							rla_pend_r[s] <= 1'b1;
						else if (rla_grant_w[s])
							rla_pend_r[s] <= 1'b0;
						if ((periodic_tick_i && !per_grant_w[s]) && (!app_ev_v_w[s] || (app_ev_w[s * 4+:4] != AE_PER_C)))
							per_pend_r[s] <= 1'b1;
						else if (per_grant_w[s])
							per_pend_r[s] <= 1'b0;
					end
			end
			if (ctl_acc_w) begin
				if (ctl_settle_i) begin
					rec_valid_r[ctl_sink_i] <= 1'b1;
					armed_r[ctl_sink_i] <= 1'b1;
					sid_r[ctl_sink_i * 64+:64] <= ctl_stream_id_i;
					da_r[ctl_sink_i * 48+:48] <= ctl_da_i;
					vid_r[ctl_sink_i * 12+:12] <= ctl_vid_i;
					app_r[ctl_sink_i * 4+:4] <= A_VO_C;
					decl_pend_r[ctl_sink_i * 2+:2] <= D_NOP_C;
					fourpack_r[ctl_sink_i * 2+:2] <= 2'd0;
				end
				else begin
					armed_r[ctl_sink_i] <= 1'b0;
					decl_pend_r[ctl_sink_i * 2+:2] <= D_NOP_C;
				end
			end
			if (leaveall_own_i)
				laown_pend_r <= 1'b1;
			case (walk_r)
				2'd0:
					if (join_tick_i || tick_pend_r) begin
						tick_pend_r <= 1'b0;
						wtxla_r <= laown_pend_r;
						laown_pend_r <= 1'b0;
						wsrc_r <= 1'sb0;
						walk_r <= 2'd1;
					end
				2'd1: begin
					if (join_tick_i)
						tick_pend_r <= 1'b1;
					if (walk_grant_w) begin
						if (wmsg_w[3] && rec_valid_r[wsrc_r]) begin
							push_code_r <= wmsg_w[2:0];
							push_fp_r <= fourpack_r[wsrc_r * 2+:2];
							push_val_r <= wval_w;
							walk_r <= 2'd2;
						end
						else if (wsrc_r == sv2v_cast_B2660(N_SINKS_P - 1))
							walk_r <= 2'd3;
						else
							wsrc_r <= wsrc_r + sv2v_cast_B2660_signed(1);
					end
				end
				2'd2: begin
					if (join_tick_i)
						tick_pend_r <= 1'b1;
					if (ev_ready_i) begin
						if (wsrc_r == sv2v_cast_B2660(N_SINKS_P - 1))
							walk_r <= 2'd3;
						else begin
							wsrc_r <= wsrc_r + sv2v_cast_B2660_signed(1);
							walk_r <= 2'd1;
						end
					end
				end
				default: begin
					if (join_tick_i)
						tick_pend_r <= 1'b1;
					txop_done_o <= 1'b1;
					walk_r <= 2'd0;
				end
			endcase
		end
	end
	assign ev_valid_o = walk_r == 2'd2;
	assign ev_app_o = 1'b0;
	assign ev_attr_type_o = srp_pkg_SRP_MSRP_ATTR_LISTENER_C;
	assign ev_event_o = push_code_r;
	assign ev_fourpack_o = push_fp_r;
	assign ev_value_o = push_val_r;
	reg tsel_v_w;
	reg [SNK_W_C - 1:0] tsel_ix_w;
	always @(*) begin : tissue_sel
		if (_sv2v_0)
			;
		tsel_v_w = 1'b0;
		tsel_ix_w = 1'sb0;
		begin : sv2v_autoblock_5
			reg [31:0] s;
			for (s = 0; s < N_SINKS_P; s = s + 1)
				if (!tsel_v_w && (tpend_r[s * 2+:2] != T_NOP_C)) begin
					tsel_v_w = 1'b1;
					tsel_ix_w = sv2v_cast_B2660(s);
				end
		end
	end
	function automatic [SLOT_AW_P - 1:0] sv2v_cast_42C2E;
		input reg [SLOT_AW_P - 1:0] inp;
		sv2v_cast_42C2E = inp;
	endfunction
	always @(posedge clk_i) begin : reg_plane
		if (!rst_n) begin
			reg_r <= 1'sb0;
			rtype_r <= 1'sb0;
			lat_r <= 1'sb0;
			fcode_r <= 1'sb0;
			fsysid_r <= 1'sb0;
			tpend_r <= 1'sb0;
			evt_tk_registered_o <= 1'sb0;
			evt_tk_unregistered_o <= 1'sb0;
			arm_valid_o <= 1'b0;
			arm_cancel_o <= 1'b0;
			arm_slot_o <= 1'sb0;
			arm_owner_o <= 8'd0;
			arm_deadline_ms_o <= 32'd0;
		end
		else begin
			evt_tk_registered_o <= 1'sb0;
			evt_tk_unregistered_o <= 1'sb0;
			arm_valid_o <= 1'b0;
			if (tsel_v_w) begin
				arm_valid_o <= 1'b1;
				arm_cancel_o <= tpend_r[tsel_ix_w * 2+:2] == T_CANCEL_C;
				arm_slot_o <= sv2v_cast_42C2E(SLOT_BASE_P + sv2v_cast_32(tsel_ix_w));
				arm_owner_o <= OWNER_BASE_P + {{8 - SNK_W_C {1'b0}}, tsel_ix_w};
				arm_deadline_ms_o <= now_ms_i + LEAVE_MS_P;
				tpend_r[tsel_ix_w * 2+:2] <= T_NOP_C;
			end
			begin : sv2v_autoblock_6
				reg [31:0] s;
				for (s = 0; s < N_SINKS_P; s = s + 1)
					begin
						if (reg_rx_hit_w[s] && rx_registering_w) begin
							if (reg_r[s * 2+:2] == R_LV_C)
								tpend_r[s * 2+:2] <= T_CANCEL_C;
							reg_r[s * 2+:2] <= R_IN_C;
							rtype_r[s] <= rx_is_failed_w;
							lat_r[s * 32+:32] <= evt_acc_latency_i;
							if (rx_is_failed_w) begin
								fcode_r[s * 8+:8] <= evt_failure_code_i;
								fsysid_r[s * 64+:64] <= evt_failure_system_id_i;
							end
							if (ind_reg_w[s])
								evt_tk_registered_o[s] <= 1'b1;
						end
						else if (reg_rx_hit_w[s] && (evt_mrp_event_i == 3'd5)) begin
							if (reg_r[s * 2+:2] == R_IN_C) begin
								reg_r[s * 2+:2] <= R_MT_C;
								evt_tk_unregistered_o[s] <= 1'b1;
							end
						end
						else if (leaveall_any_w && (reg_r[s * 2+:2] == R_IN_C)) begin
							reg_r[s * 2+:2] <= R_LV_C;
							tpend_r[s * 2+:2] <= T_ARM_C;
						end
						else if (((exp_hit_w && (exp_idx_w == s)) && (reg_r[s * 2+:2] == R_LV_C)) && (tpend_r[s * 2+:2] != T_ARM_C)) begin
							reg_r[s * 2+:2] <= R_MT_C;
							evt_tk_unregistered_o[s] <= 1'b1;
						end
						if (ctl_acc_w && (ctl_sink_i == sv2v_cast_B2660(s))) begin
							if (reg_r[s * 2+:2] == R_LV_C)
								tpend_r[s * 2+:2] <= T_CANCEL_C;
							reg_r[s * 2+:2] <= R_MT_C;
							rtype_r[s] <= 1'b0;
							lat_r[s * 32+:32] <= 32'd0;
							fcode_r[s * 8+:8] <= 8'd0;
							fsysid_r[s * 64+:64] <= 64'd0;
						end
					end
			end
		end
	end
	reg vsel_v_w;
	reg vsel_join_w;
	reg [SNK_W_C - 1:0] vsel_ix_w;
	always @(*) begin : vlan_sel
		if (_sv2v_0)
			;
		vsel_v_w = 1'b0;
		vsel_join_w = 1'b0;
		vsel_ix_w = 1'sb0;
		user_vid_o = 12'd0;
		begin : sv2v_autoblock_7
			reg [31:0] s;
			for (s = 0; s < N_SINKS_P; s = s + 1)
				if (!vsel_v_w) begin
					if (vl_pend_r[s]) begin
						vsel_v_w = 1'b1;
						vsel_join_w = 1'b0;
						vsel_ix_w = sv2v_cast_B2660(s);
						user_vid_o = vl_vid_r[s * 12+:12];
					end
					else if (vj_pend_r[s]) begin
						vsel_v_w = 1'b1;
						vsel_join_w = 1'b1;
						vsel_ix_w = sv2v_cast_B2660(s);
						user_vid_o = vj_vid_r[s * 12+:12];
					end
				end
		end
	end
	assign user_valid_o = vsel_v_w;
	assign user_join_o = vsel_join_w;
	always @(posedge clk_i) begin : vlan_plane
		if (!rst_n) begin
			vj_pend_r <= 1'sb0;
			vl_pend_r <= 1'sb0;
			vj_vid_r <= 1'sb0;
			vl_vid_r <= 1'sb0;
		end
		else begin
			if (vsel_v_w && user_ready_i) begin
				if (vsel_join_w)
					vj_pend_r[vsel_ix_w] <= 1'b0;
				else
					vl_pend_r[vsel_ix_w] <= 1'b0;
			end
			if (ctl_acc_w) begin
				if (ctl_settle_i) begin
					if ((vl_pend_r[ctl_sink_i] && (vl_vid_r[ctl_sink_i * 12+:12] == ctl_vid_i)) && !(((vsel_v_w && user_ready_i) && !vsel_join_w) && (vsel_ix_w == ctl_sink_i)))
						vl_pend_r[ctl_sink_i] <= 1'b0;
					else begin
						vj_pend_r[ctl_sink_i] <= 1'b1;
						vj_vid_r[ctl_sink_i * 12+:12] <= ctl_vid_i;
					end
				end
				else if (vj_pend_r[ctl_sink_i] && !(((vsel_v_w && user_ready_i) && vsel_join_w) && (vsel_ix_w == ctl_sink_i)))
					vj_pend_r[ctl_sink_i] <= 1'b0;
				else begin
					vl_pend_r[ctl_sink_i] <= 1'b1;
					vl_vid_r[ctl_sink_i * 12+:12] <= vid_r[ctl_sink_i * 12+:12];
				end
			end
		end
	end
	always @(*) begin : status_map
		if (_sv2v_0)
			;
		begin : sv2v_autoblock_8
			reg [31:0] s;
			for (s = 0; s < N_SINKS_P; s = s + 1)
				begin
					tk_reg_state_o[s * 2+:2] = (armed_r[s] && (reg_r[s * 2+:2] != R_MT_C) ? (rtype_r[s] ? 2'd2 : 2'd1) : 2'd0);
					lstn_decl_state_o[s * 2+:2] = (rec_valid_r[s] && app_declaring_f(app_r[s * 4+:4]) ? fourpack_r[s * 2+:2] : 2'd0);
					acc_latency_o[s * 32+:32] = lat_r[s * 32+:32];
					msrp_fail_code_o[s * 8+:8] = (tk_reg_state_o[s * 2+:2] == 2'd2 ? fcode_r[s * 8+:8] : 8'd0);
					msrp_fail_bridge_o[s * 64+:64] = (tk_reg_state_o[s * 2+:2] == 2'd2 ? fsysid_r[s * 64+:64] : 64'd0);
					dbg_app_state_o[s * 4+:4] = app_r[s * 4+:4];
					dbg_reg_state_o[s * 2+:2] = reg_r[s * 2+:2];
				end
		end
	end
	initial _sv2v_0 = 0;
endmodule
`default_nettype wire
`default_nettype none
module KL_srp_talker_fsm (
	clk_i,
	rst_n,
	own_mac_i,
	p2p_i,
	gate_valid_i,
	gate_ready_o,
	gate_open_i,
	gate_src_i,
	gate_stream_id_i,
	gate_da_i,
	gate_vid_i,
	gate_max_frame_i,
	gate_max_interval_i,
	gate_prio_i,
	gate_rank_i,
	gate_acc_lat_i,
	sr_admitted_i,
	evt_valid_i,
	evt_msrp_i,
	evt_attr_type_i,
	evt_stream_id_i,
	evt_da_i,
	evt_vid_i,
	evt_mrp_event_i,
	evt_fourpacked_i,
	join_tick_i,
	periodic_tick_i,
	leaveall_rx_i,
	leaveall_own_i,
	txop_done_o,
	ev_valid_o,
	ev_ready_i,
	ev_app_o,
	ev_attr_type_o,
	ev_event_o,
	ev_fourpack_o,
	ev_value_o,
	user_valid_o,
	user_join_o,
	user_vid_o,
	user_ready_i,
	now_ms_i,
	arm_valid_o,
	arm_cancel_o,
	arm_slot_o,
	arm_owner_o,
	arm_deadline_ms_o,
	exp_valid_i,
	exp_slot_i,
	lstn_reg_change_o,
	tk_decl_state_o,
	lstn_reg_state_o,
	active_o,
	msrp_fail_code_o,
	msrp_fail_bridge_o,
	dbg_app_state_o,
	dbg_reg_state_o
);
	reg _sv2v_0;
	parameter [31:0] N_SOURCES_P = 8;
	parameter [31:0] LEAVE_MS_P = 5000;
	parameter [31:0] SLOT_BASE_P = 0;
	parameter [31:0] SLOT_AW_P = 7;
	parameter [7:0] OWNER_BASE_P = 8'h40;
	localparam [31:0] SRC_W_C = (N_SOURCES_P > 1 ? $clog2(N_SOURCES_P) : 1);
	input wire clk_i;
	input wire rst_n;
	input wire [47:0] own_mac_i;
	input wire p2p_i;
	input wire gate_valid_i;
	output wire gate_ready_o;
	input wire gate_open_i;
	input wire [SRC_W_C - 1:0] gate_src_i;
	input wire [63:0] gate_stream_id_i;
	input wire [47:0] gate_da_i;
	input wire [11:0] gate_vid_i;
	input wire [15:0] gate_max_frame_i;
	input wire [15:0] gate_max_interval_i;
	input wire [2:0] gate_prio_i;
	input wire gate_rank_i;
	input wire [31:0] gate_acc_lat_i;
	input wire [N_SOURCES_P - 1:0] sr_admitted_i;
	input wire evt_valid_i;
	input wire evt_msrp_i;
	input wire [7:0] evt_attr_type_i;
	input wire [63:0] evt_stream_id_i;
	input wire [47:0] evt_da_i;
	input wire [15:0] evt_vid_i;
	input wire [2:0] evt_mrp_event_i;
	input wire [1:0] evt_fourpacked_i;
	input wire join_tick_i;
	input wire periodic_tick_i;
	input wire leaveall_rx_i;
	input wire leaveall_own_i;
	output reg txop_done_o;
	output wire ev_valid_o;
	input wire ev_ready_i;
	output wire ev_app_o;
	output wire [7:0] ev_attr_type_o;
	output wire [2:0] ev_event_o;
	output wire [1:0] ev_fourpack_o;
	output wire [271:0] ev_value_o;
	output wire user_valid_o;
	output wire user_join_o;
	output reg [11:0] user_vid_o;
	input wire user_ready_i;
	input wire [31:0] now_ms_i;
	output reg arm_valid_o;
	output reg arm_cancel_o;
	output reg [SLOT_AW_P - 1:0] arm_slot_o;
	output reg [7:0] arm_owner_o;
	output reg [31:0] arm_deadline_ms_o;
	input wire exp_valid_i;
	input wire [SLOT_AW_P - 1:0] exp_slot_i;
	output reg [N_SOURCES_P - 1:0] lstn_reg_change_o;
	output reg [(N_SOURCES_P * 2) - 1:0] tk_decl_state_o;
	output reg [(N_SOURCES_P * 2) - 1:0] lstn_reg_state_o;
	output reg [N_SOURCES_P - 1:0] active_o;
	output reg [(N_SOURCES_P * 8) - 1:0] msrp_fail_code_o;
	output reg [(N_SOURCES_P * 64) - 1:0] msrp_fail_bridge_o;
	output reg [(N_SOURCES_P * 4) - 1:0] dbg_app_state_o;
	output reg [(N_SOURCES_P * 2) - 1:0] dbg_reg_state_o;
	localparam [3:0] A_VO_C = 4'd0;
	localparam [3:0] A_VP_C = 4'd1;
	localparam [3:0] A_VN_C = 4'd2;
	localparam [3:0] A_AN_C = 4'd3;
	localparam [3:0] A_AA_C = 4'd4;
	localparam [3:0] A_QA_C = 4'd5;
	localparam [3:0] A_LA_C = 4'd6;
	localparam [3:0] A_AO_C = 4'd7;
	localparam [3:0] A_QO_C = 4'd8;
	localparam [3:0] A_AP_C = 4'd9;
	localparam [3:0] A_QP_C = 4'd10;
	localparam [3:0] A_LO_C = 4'd11;
	localparam [3:0] AE_NEW_C = 4'd0;
	localparam [3:0] AE_JOIN_C = 4'd1;
	localparam [3:0] AE_LV_C = 4'd2;
	localparam [3:0] AE_RNEW_C = 4'd3;
	localparam [3:0] AE_RJOININ_C = 4'd4;
	localparam [3:0] AE_RIN_C = 4'd5;
	localparam [3:0] AE_RJOINMT_C = 4'd6;
	localparam [3:0] AE_RMT_C = 4'd7;
	localparam [3:0] AE_RLV_C = 4'd8;
	localparam [3:0] AE_RLA_C = 4'd9;
	localparam [3:0] AE_PER_C = 4'd10;
	localparam [3:0] AE_TX_C = 4'd11;
	localparam [3:0] AE_TXLA_C = 4'd12;
	localparam [1:0] R_MT_C = 2'd0;
	localparam [1:0] R_IN_C = 2'd1;
	localparam [1:0] R_LV_C = 2'd2;
	localparam [1:0] T_NOP_C = 2'd0;
	localparam [1:0] T_ARM_C = 2'd1;
	localparam [1:0] T_CANCEL_C = 2'd2;
	function automatic [3:0] app_next_f;
		input reg [3:0] st;
		input reg [3:0] ev;
		input reg reg_in_i;
		input reg p2p;
		reg [3:0] nx;
		begin
			nx = st;
			case (ev)
				AE_NEW_C:
					if (!(|{st == A_VN_C, st == A_AN_C}))
						nx = A_VN_C;
				AE_JOIN_C:
					case (st)
						A_VO_C: nx = A_VP_C;
						A_LA_C: nx = A_AA_C;
						A_AO_C: nx = A_AP_C;
						A_QO_C: nx = A_QP_C;
						A_LO_C: nx = A_VP_C;
						default: nx = st;
					endcase
				AE_LV_C:
					case (st)
						A_VP_C: nx = A_VO_C;
						A_VN_C, A_AN_C, A_AA_C, A_QA_C: nx = A_LA_C;
						A_AP_C: nx = A_AO_C;
						A_QP_C: nx = A_QO_C;
						default: nx = st;
					endcase
				AE_RNEW_C: nx = st;
				AE_RJOININ_C:
					case (st)
						A_VO_C: nx = (p2p ? st : A_AO_C);
						A_VP_C: nx = (p2p ? st : A_AP_C);
						A_AA_C: nx = A_QA_C;
						A_AO_C: nx = A_QO_C;
						A_AP_C: nx = A_QP_C;
						default: nx = st;
					endcase
				AE_RIN_C:
					if (p2p && (st == A_AA_C))
						nx = A_QA_C;
				AE_RJOINMT_C, AE_RMT_C:
					case (st)
						A_QA_C: nx = A_AA_C;
						A_QO_C: nx = A_AO_C;
						A_QP_C: nx = A_AP_C;
						A_LO_C: nx = A_VO_C;
						default: nx = st;
					endcase
				AE_RLV_C, AE_RLA_C:
					case (st)
						A_VO_C, A_AO_C, A_QO_C: nx = A_LO_C;
						A_AN_C: nx = A_VN_C;
						A_AA_C, A_QA_C, A_AP_C, A_QP_C: nx = A_VP_C;
						default: nx = st;
					endcase
				AE_PER_C:
					case (st)
						A_QA_C: nx = A_AA_C;
						A_QP_C: nx = A_AP_C;
						default: nx = st;
					endcase
				AE_TX_C:
					case (st)
						A_VP_C: nx = A_AA_C;
						A_VN_C: nx = A_AN_C;
						A_AN_C: nx = (reg_in_i ? A_QA_C : A_AA_C);
						A_AA_C: nx = A_QA_C;
						A_LA_C: nx = A_VO_C;
						A_AP_C: nx = A_QA_C;
						A_LO_C: nx = A_VO_C;
						default: nx = st;
					endcase
				AE_TXLA_C:
					case (st)
						A_VO_C, A_LA_C, A_AO_C, A_QO_C: nx = A_LO_C;
						A_VP_C: nx = A_AA_C;
						A_VN_C: nx = A_AN_C;
						A_AN_C, A_AA_C, A_AP_C, A_QP_C: nx = A_QA_C;
						default: nx = st;
					endcase
				default: nx = st;
			endcase
			app_next_f = nx;
		end
	endfunction
	function automatic [3:0] app_msg_f;
		input reg [3:0] st;
		input reg txla;
		input reg reg_in_i;
		reg [2:0] sj_w;
		reg [2:0] s_w;
		reg [3:0] m;
		begin
			sj_w = (reg_in_i ? 3'd1 : 3'd3);
			s_w = (reg_in_i ? 3'd2 : 3'd4);
			m = 4'h0;
			if (!txla)
				case (st)
					A_VP_C, A_AA_C, A_AP_C: m = {1'b1, sj_w};
					A_VN_C, A_AN_C: m = 4'h8;
					A_LA_C: m = 4'hd;
					A_LO_C: m = {1'b1, s_w};
					default: m = 4'h0;
				endcase
			else
				case (st)
					A_VP_C: m = {1'b1, s_w};
					A_VN_C, A_AN_C: m = 4'h8;
					A_AA_C, A_QA_C, A_AP_C, A_QP_C: m = {1'b1, sj_w};
					default: m = 4'h0;
				endcase
			app_msg_f = m;
		end
	endfunction
	function automatic app_declaring_f;
		input reg [3:0] st;
		app_declaring_f = |{st == A_VP_C, st == A_VN_C, st == A_AN_C, st == A_AA_C, st == A_QA_C, st == A_AP_C, st == A_QP_C};
	endfunction
	reg [N_SOURCES_P - 1:0] rec_valid_r;
	reg [(N_SOURCES_P * 64) - 1:0] sid_r;
	reg [(N_SOURCES_P * 48) - 1:0] da_r;
	reg [(N_SOURCES_P * 12) - 1:0] vid_r;
	reg [(N_SOURCES_P * 16) - 1:0] mfs_r;
	reg [(N_SOURCES_P * 16) - 1:0] mif_r;
	reg [(N_SOURCES_P * 3) - 1:0] prio_r;
	reg [N_SOURCES_P - 1:0] rank_r;
	reg [(N_SOURCES_P * 32) - 1:0] lat_r;
	reg [(N_SOURCES_P * 4) - 1:0] app_r;
	reg [N_SOURCES_P - 1:0] fail_r;
	reg [N_SOURCES_P - 1:0] rla_pend_r;
	reg [N_SOURCES_P - 1:0] per_pend_r;
	reg [1:0] walk_r;
	reg [SRC_W_C - 1:0] wsrc_r;
	reg wtxla_r;
	reg tick_pend_r;
	reg laown_pend_r;
	reg [2:0] push_code_r;
	reg [7:0] push_type_r;
	reg [271:0] push_val_r;
	reg [(N_SOURCES_P * 2) - 1:0] reg_r;
	reg [(N_SOURCES_P * 2) - 1:0] lstn_val_r;
	reg [(N_SOURCES_P * 2) - 1:0] lstn_prev_r;
	reg [(N_SOURCES_P * 2) - 1:0] tpend_r;
	reg [N_SOURCES_P - 1:0] vj_pend_r;
	reg [N_SOURCES_P - 1:0] vl_pend_r;
	reg [(N_SOURCES_P * 12) - 1:0] vj_vid_r;
	reg [(N_SOURCES_P * 12) - 1:0] vl_vid_r;
	reg [N_SOURCES_P - 1:0] app_rx_hit_w;
	reg [N_SOURCES_P - 1:0] reg_rx_hit_w;
	reg [3:0] rx_app_ev_w;
	localparam [7:0] srp_pkg_SRP_MSRP_ATTR_LISTENER_C = 8'd3;
	localparam [7:0] srp_pkg_SRP_MSRP_ATTR_TALKER_ADV_C = 8'd1;
	localparam [7:0] srp_pkg_SRP_MSRP_ATTR_TALKER_FAILED_C = 8'd2;
	always @(*) begin : hit_map
		if (_sv2v_0)
			;
		rx_app_ev_w = {1'b0, evt_mrp_event_i} + AE_RNEW_C;
		begin : sv2v_autoblock_1
			reg [31:0] s;
			for (s = 0; s < N_SOURCES_P; s = s + 1)
				begin
					app_rx_hit_w[s] = ((((((evt_valid_i && evt_msrp_i) && rec_valid_r[s]) && ((evt_attr_type_i == srp_pkg_SRP_MSRP_ATTR_TALKER_ADV_C) || (evt_attr_type_i == srp_pkg_SRP_MSRP_ATTR_TALKER_FAILED_C))) && (evt_mrp_event_i <= 3'd5)) && (evt_stream_id_i == sid_r[s * 64+:64])) && (evt_da_i == da_r[s * 48+:48])) && (evt_vid_i == {4'd0, vid_r[s * 12+:12]});
					reg_rx_hit_w[s] = (((evt_valid_i && evt_msrp_i) && rec_valid_r[s]) && (evt_attr_type_i == srp_pkg_SRP_MSRP_ATTR_LISTENER_C)) && (evt_stream_id_i == sid_r[s * 64+:64]);
				end
		end
	end
	wire gate_acc_w;
	reg [N_SOURCES_P - 1:0] app_ev_v_w;
	reg [(N_SOURCES_P * 4) - 1:0] app_ev_w;
	reg [N_SOURCES_P - 1:0] adm_grant_w;
	reg [N_SOURCES_P - 1:0] rla_grant_w;
	reg [N_SOURCES_P - 1:0] per_grant_w;
	reg walk_grant_w;
	reg [N_SOURCES_P - 1:0] adm_fix_w;
	assign gate_ready_o = !evt_valid_i;
	assign gate_acc_w = gate_valid_i && gate_ready_o;
	function automatic [SRC_W_C - 1:0] sv2v_cast_14954;
		input reg [SRC_W_C - 1:0] inp;
		sv2v_cast_14954 = inp;
	endfunction
	always @(*) begin : app_arb
		if (_sv2v_0)
			;
		walk_grant_w = 1'b0;
		begin : sv2v_autoblock_2
			reg [31:0] s;
			for (s = 0; s < N_SOURCES_P; s = s + 1)
				begin
					adm_fix_w[s] = (rec_valid_r[s] && app_declaring_f(app_r[s * 4+:4])) && (fail_r[s] != !sr_admitted_i[s]);
					app_ev_v_w[s] = 1'b0;
					app_ev_w[s * 4+:4] = AE_RNEW_C;
					adm_grant_w[s] = 1'b0;
					rla_grant_w[s] = 1'b0;
					per_grant_w[s] = 1'b0;
					if (app_rx_hit_w[s]) begin
						app_ev_v_w[s] = 1'b1;
						app_ev_w[s * 4+:4] = rx_app_ev_w;
					end
					else if (gate_acc_w && (gate_src_i == sv2v_cast_14954(s))) begin
						app_ev_v_w[s] = 1'b1;
						app_ev_w[s * 4+:4] = (gate_open_i ? (rec_valid_r[s] ? AE_JOIN_C : AE_NEW_C) : AE_LV_C);
					end
					else if (rla_pend_r[s] || leaveall_rx_i) begin
						app_ev_v_w[s] = 1'b1;
						app_ev_w[s * 4+:4] = AE_RLA_C;
						rla_grant_w[s] = 1'b1;
					end
					else if (adm_fix_w[s]) begin
						app_ev_v_w[s] = 1'b1;
						app_ev_w[s * 4+:4] = AE_NEW_C;
						adm_grant_w[s] = 1'b1;
					end
					else if (per_pend_r[s] || periodic_tick_i) begin
						app_ev_v_w[s] = 1'b1;
						app_ev_w[s * 4+:4] = AE_PER_C;
						per_grant_w[s] = 1'b1;
					end
					else if ((walk_r == 2'd1) && (wsrc_r == sv2v_cast_14954(s))) begin
						app_ev_v_w[s] = 1'b1;
						app_ev_w[s * 4+:4] = (wtxla_r ? AE_TXLA_C : AE_TX_C);
						walk_grant_w = 1'b1;
					end
				end
		end
	end
	reg [271:0] wval_w;
	reg [3:0] wmsg_w;
	always @(*) begin : walk_msg
		if (_sv2v_0)
			;
		wval_w = 272'd0;
		wval_w[271:208] = sid_r[wsrc_r * 64+:64];
		wval_w[207:160] = da_r[wsrc_r * 48+:48];
		wval_w[159:144] = {4'd0, vid_r[wsrc_r * 12+:12]};
		wval_w[143:128] = mfs_r[wsrc_r * 16+:16];
		wval_w[127:112] = mif_r[wsrc_r * 16+:16];
		wval_w[111:104] = {prio_r[wsrc_r * 3+:3], rank_r[wsrc_r], 4'd0};
		wval_w[103:72] = lat_r[wsrc_r * 32+:32];
		if (fail_r[wsrc_r]) begin
			wval_w[71:8] = {16'd0, own_mac_i};
			wval_w[7:0] = 8'd1;
		end
		wmsg_w = app_msg_f(app_r[wsrc_r * 4+:4], wtxla_r, 1'b0);
	end
	function automatic signed [SRC_W_C - 1:0] sv2v_cast_14954_signed;
		input reg signed [SRC_W_C - 1:0] inp;
		sv2v_cast_14954_signed = inp;
	endfunction
	always @(posedge clk_i) begin : app_plane
		if (!rst_n) begin
			rec_valid_r <= 1'sb0;
			sid_r <= 1'sb0;
			da_r <= 1'sb0;
			vid_r <= 1'sb0;
			mfs_r <= 1'sb0;
			mif_r <= 1'sb0;
			prio_r <= 1'sb0;
			rank_r <= 1'sb0;
			lat_r <= 1'sb0;
			app_r <= 1'sb0;
			fail_r <= 1'sb0;
			rla_pend_r <= 1'sb0;
			per_pend_r <= 1'sb0;
			walk_r <= 2'd0;
			wsrc_r <= 1'sb0;
			wtxla_r <= 1'b0;
			tick_pend_r <= 1'b0;
			laown_pend_r <= 1'b0;
			push_code_r <= 3'd0;
			push_type_r <= 8'd0;
			push_val_r <= 1'sb0;
			txop_done_o <= 1'b0;
		end
		else begin
			txop_done_o <= 1'b0;
			begin : sv2v_autoblock_3
				reg [31:0] s;
				for (s = 0; s < N_SOURCES_P; s = s + 1)
					begin
						if (app_ev_v_w[s])
							app_r[s * 4+:4] <= app_next_f(app_r[s * 4+:4], app_ev_w[s * 4+:4], 1'b0, p2p_i);
						if ((leaveall_rx_i && !rla_grant_w[s]) && (!app_ev_v_w[s] || (app_ev_w[s * 4+:4] != AE_RLA_C)))
							rla_pend_r[s] <= 1'b1;
						else if (rla_grant_w[s])
							rla_pend_r[s] <= 1'b0;
						if ((periodic_tick_i && !per_grant_w[s]) && (!app_ev_v_w[s] || (app_ev_w[s * 4+:4] != AE_PER_C)))
							per_pend_r[s] <= 1'b1;
						else if (per_grant_w[s])
							per_pend_r[s] <= 1'b0;
						if (adm_grant_w[s])
							fail_r[s] <= !sr_admitted_i[s];
					end
			end
			if (gate_acc_w) begin
				if (gate_open_i) begin
					rec_valid_r[gate_src_i] <= 1'b1;
					sid_r[gate_src_i * 64+:64] <= gate_stream_id_i;
					da_r[gate_src_i * 48+:48] <= gate_da_i;
					vid_r[gate_src_i * 12+:12] <= gate_vid_i;
					mfs_r[gate_src_i * 16+:16] <= gate_max_frame_i;
					mif_r[gate_src_i * 16+:16] <= gate_max_interval_i;
					prio_r[gate_src_i * 3+:3] <= gate_prio_i;
					rank_r[gate_src_i] <= gate_rank_i;
					lat_r[gate_src_i * 32+:32] <= gate_acc_lat_i;
				end
				else
					fail_r[gate_src_i] <= 1'b0;
			end
			if (leaveall_own_i)
				laown_pend_r <= 1'b1;
			case (walk_r)
				2'd0:
					if (join_tick_i || tick_pend_r) begin
						tick_pend_r <= 1'b0;
						wtxla_r <= laown_pend_r;
						laown_pend_r <= 1'b0;
						wsrc_r <= 1'sb0;
						walk_r <= 2'd1;
					end
				2'd1: begin
					if (join_tick_i)
						tick_pend_r <= 1'b1;
					if (walk_grant_w) begin
						if (wmsg_w[3] && rec_valid_r[wsrc_r]) begin
							push_code_r <= wmsg_w[2:0];
							push_type_r <= (fail_r[wsrc_r] ? srp_pkg_SRP_MSRP_ATTR_TALKER_FAILED_C : srp_pkg_SRP_MSRP_ATTR_TALKER_ADV_C);
							push_val_r <= wval_w;
							walk_r <= 2'd2;
						end
						else if (wsrc_r == sv2v_cast_14954(N_SOURCES_P - 1))
							walk_r <= 2'd3;
						else
							wsrc_r <= wsrc_r + sv2v_cast_14954_signed(1);
					end
				end
				2'd2: begin
					if (join_tick_i)
						tick_pend_r <= 1'b1;
					if (ev_ready_i) begin
						if (wsrc_r == sv2v_cast_14954(N_SOURCES_P - 1))
							walk_r <= 2'd3;
						else begin
							wsrc_r <= wsrc_r + sv2v_cast_14954_signed(1);
							walk_r <= 2'd1;
						end
					end
				end
				default: begin
					if (join_tick_i)
						tick_pend_r <= 1'b1;
					txop_done_o <= 1'b1;
					walk_r <= 2'd0;
				end
			endcase
		end
	end
	assign ev_valid_o = walk_r == 2'd2;
	assign ev_app_o = 1'b0;
	assign ev_attr_type_o = push_type_r;
	assign ev_event_o = push_code_r;
	assign ev_fourpack_o = 2'd0;
	assign ev_value_o = push_val_r;
	wire leaveall_any_w;
	wire exp_hit_w;
	wire [31:0] exp_idx_w;
	assign leaveall_any_w = leaveall_rx_i || leaveall_own_i;
	function automatic [31:0] sv2v_cast_32;
		input reg [31:0] inp;
		sv2v_cast_32 = inp;
	endfunction
	assign exp_idx_w = sv2v_cast_32(exp_slot_i) - SLOT_BASE_P;
	assign exp_hit_w = exp_valid_i && (exp_idx_w < N_SOURCES_P);
	reg [(N_SOURCES_P * 2) - 1:0] lstn_out_w;
	always @(*) begin : lstn_out_map
		if (_sv2v_0)
			;
		begin : sv2v_autoblock_4
			reg [31:0] s;
			for (s = 0; s < N_SOURCES_P; s = s + 1)
				lstn_out_w[s * 2+:2] = (reg_r[s * 2+:2] != R_MT_C ? lstn_val_r[s * 2+:2] : 2'd0);
		end
	end
	reg tsel_v_w;
	reg [SRC_W_C - 1:0] tsel_ix_w;
	always @(*) begin : tissue_sel
		if (_sv2v_0)
			;
		tsel_v_w = 1'b0;
		tsel_ix_w = 1'sb0;
		begin : sv2v_autoblock_5
			reg [31:0] s;
			for (s = 0; s < N_SOURCES_P; s = s + 1)
				if (!tsel_v_w && (tpend_r[s * 2+:2] != T_NOP_C)) begin
					tsel_v_w = 1'b1;
					tsel_ix_w = sv2v_cast_14954(s);
				end
		end
	end
	function automatic [SLOT_AW_P - 1:0] sv2v_cast_42C2E;
		input reg [SLOT_AW_P - 1:0] inp;
		sv2v_cast_42C2E = inp;
	endfunction
	always @(posedge clk_i) begin : reg_plane
		if (!rst_n) begin
			reg_r <= 1'sb0;
			lstn_val_r <= 1'sb0;
			lstn_prev_r <= 1'sb0;
			tpend_r <= 1'sb0;
			lstn_reg_change_o <= 1'sb0;
			arm_valid_o <= 1'b0;
			arm_cancel_o <= 1'b0;
			arm_slot_o <= 1'sb0;
			arm_owner_o <= 8'd0;
			arm_deadline_ms_o <= 32'd0;
		end
		else begin
			lstn_reg_change_o <= 1'sb0;
			arm_valid_o <= 1'b0;
			if (tsel_v_w) begin
				arm_valid_o <= 1'b1;
				arm_cancel_o <= tpend_r[tsel_ix_w * 2+:2] == T_CANCEL_C;
				arm_slot_o <= sv2v_cast_42C2E(SLOT_BASE_P + sv2v_cast_32(tsel_ix_w));
				arm_owner_o <= OWNER_BASE_P + {{8 - SRC_W_C {1'b0}}, tsel_ix_w};
				arm_deadline_ms_o <= now_ms_i + LEAVE_MS_P;
				tpend_r[tsel_ix_w * 2+:2] <= T_NOP_C;
			end
			begin : sv2v_autoblock_6
				reg [31:0] s;
				for (s = 0; s < N_SOURCES_P; s = s + 1)
					begin
						if (reg_rx_hit_w[s] && (((evt_mrp_event_i == 3'd0) || (evt_mrp_event_i == 3'd1)) || (evt_mrp_event_i == 3'd3))) begin
							if (reg_r[s * 2+:2] == R_LV_C)
								tpend_r[s * 2+:2] <= T_CANCEL_C;
							reg_r[s * 2+:2] <= R_IN_C;
							lstn_val_r[s * 2+:2] <= evt_fourpacked_i;
						end
						else if (reg_rx_hit_w[s] && (evt_mrp_event_i == 3'd5)) begin
							if (reg_r[s * 2+:2] == R_IN_C)
								reg_r[s * 2+:2] <= R_MT_C;
						end
						else if (leaveall_any_w && (reg_r[s * 2+:2] == R_IN_C)) begin
							reg_r[s * 2+:2] <= R_LV_C;
							tpend_r[s * 2+:2] <= T_ARM_C;
						end
						else if (((exp_hit_w && (exp_idx_w == s)) && (reg_r[s * 2+:2] == R_LV_C)) && (tpend_r[s * 2+:2] != T_ARM_C))
							reg_r[s * 2+:2] <= R_MT_C;
						if ((gate_acc_w && gate_open_i) && (gate_src_i == sv2v_cast_14954(s))) begin
							if (reg_r[s * 2+:2] == R_LV_C)
								tpend_r[s * 2+:2] <= T_CANCEL_C;
							reg_r[s * 2+:2] <= R_MT_C;
							lstn_val_r[s * 2+:2] <= 2'd0;
						end
					end
			end
			begin : sv2v_autoblock_7
				reg [31:0] s;
				for (s = 0; s < N_SOURCES_P; s = s + 1)
					if (lstn_out_w[s * 2+:2] != lstn_prev_r[s * 2+:2]) begin
						lstn_prev_r[s * 2+:2] <= lstn_out_w[s * 2+:2];
						lstn_reg_change_o[s] <= 1'b1;
					end
			end
		end
	end
	reg vsel_v_w;
	reg vsel_join_w;
	reg [SRC_W_C - 1:0] vsel_ix_w;
	always @(*) begin : vlan_sel
		if (_sv2v_0)
			;
		vsel_v_w = 1'b0;
		vsel_join_w = 1'b0;
		vsel_ix_w = 1'sb0;
		user_vid_o = 12'd0;
		begin : sv2v_autoblock_8
			reg [31:0] s;
			for (s = 0; s < N_SOURCES_P; s = s + 1)
				if (!vsel_v_w) begin
					if (vl_pend_r[s]) begin
						vsel_v_w = 1'b1;
						vsel_join_w = 1'b0;
						vsel_ix_w = sv2v_cast_14954(s);
						user_vid_o = vl_vid_r[s * 12+:12];
					end
					else if (vj_pend_r[s]) begin
						vsel_v_w = 1'b1;
						vsel_join_w = 1'b1;
						vsel_ix_w = sv2v_cast_14954(s);
						user_vid_o = vj_vid_r[s * 12+:12];
					end
				end
		end
	end
	assign user_valid_o = vsel_v_w;
	assign user_join_o = vsel_join_w;
	always @(posedge clk_i) begin : vlan_plane
		if (!rst_n) begin
			vj_pend_r <= 1'sb0;
			vl_pend_r <= 1'sb0;
			vj_vid_r <= 1'sb0;
			vl_vid_r <= 1'sb0;
		end
		else begin
			if (vsel_v_w && user_ready_i) begin
				if (vsel_join_w)
					vj_pend_r[vsel_ix_w] <= 1'b0;
				else
					vl_pend_r[vsel_ix_w] <= 1'b0;
			end
			if (gate_acc_w) begin
				if (gate_open_i) begin
					if ((vl_pend_r[gate_src_i] && (vl_vid_r[gate_src_i * 12+:12] == gate_vid_i)) && !(((vsel_v_w && user_ready_i) && !vsel_join_w) && (vsel_ix_w == gate_src_i)))
						vl_pend_r[gate_src_i] <= 1'b0;
					else begin
						vj_pend_r[gate_src_i] <= 1'b1;
						vj_vid_r[gate_src_i * 12+:12] <= gate_vid_i;
					end
				end
				else if (vj_pend_r[gate_src_i] && !(((vsel_v_w && user_ready_i) && vsel_join_w) && (vsel_ix_w == gate_src_i)))
					vj_pend_r[gate_src_i] <= 1'b0;
				else begin
					vl_pend_r[gate_src_i] <= 1'b1;
					vl_vid_r[gate_src_i * 12+:12] <= vid_r[gate_src_i * 12+:12];
				end
			end
		end
	end
	always @(*) begin : status_map
		if (_sv2v_0)
			;
		begin : sv2v_autoblock_9
			reg [31:0] s;
			for (s = 0; s < N_SOURCES_P; s = s + 1)
				begin
					tk_decl_state_o[s * 2+:2] = (rec_valid_r[s] && app_declaring_f(app_r[s * 4+:4]) ? (fail_r[s] ? 2'd2 : 2'd1) : 2'd0);
					lstn_reg_state_o[s * 2+:2] = lstn_out_w[s * 2+:2];
					active_o[s] = (((rec_valid_r[s] && app_declaring_f(app_r[s * 4+:4])) && !fail_r[s]) && ((lstn_out_w[s * 2+:2] == 2'd2) || (lstn_out_w[s * 2+:2] == 2'd3))) && sr_admitted_i[s];
					msrp_fail_code_o[s * 8+:8] = (tk_decl_state_o[s * 2+:2] == 2'd2 ? 8'd1 : 8'd0);
					msrp_fail_bridge_o[s * 64+:64] = (tk_decl_state_o[s * 2+:2] == 2'd2 ? {16'd0, own_mac_i} : 64'd0);
					dbg_app_state_o[s * 4+:4] = app_r[s * 4+:4];
					dbg_reg_state_o[s * 2+:2] = reg_r[s * 2+:2];
				end
		end
	end
	initial _sv2v_0 = 0;
endmodule
`default_nettype wire
`default_nettype none
module KL_srp_top (
	clk_i,
	rst_n,
	own_mac_i,
	link_up_i,
	p2p_i,
	cfg_rank_i,
	cfg_acc_lat_ns_i,
	port_rate_bps_i,
	mrp_valid_i,
	mrp_data_i,
	mrp_last_i,
	mrp_msrp_i,
	mrp_ready_o,
	req_valid_i,
	req_ready_o,
	req_op_i,
	req_index_i,
	req_stream_id_i,
	req_da_i,
	req_vid_i,
	req_max_frame_i,
	req_max_interval_i,
	req_lstn_state_i,
	rsp_valid_o,
	rsp_status_o,
	rsp_data_o,
	alloc_req_o,
	oversize_o,
	alloc_slot_i,
	alloc_gnt_i,
	wr_slot_o,
	wr_addr_o,
	wr_valid_o,
	wr_data_o,
	wr_commit_o,
	wr_len_o,
	txreq_valid_o,
	txreq_slot_o,
	txreq_ready_i,
	now_ms_i,
	arm_valid_o,
	arm_cancel_o,
	arm_slot_o,
	arm_owner_o,
	arm_deadline_ms_o,
	exp_valid_i,
	exp_slot_i,
	draw_req_o,
	draw_kind_o,
	draw_busy_i,
	draw_valid_i,
	draw_ms_i,
	evt_tk_registered_o,
	evt_tk_unregistered_o,
	lstn_reg_change_o,
	evt_domain_change_o,
	class_a_prio_o,
	class_a_vid_o,
	domain_adopted_o,
	tk_decl_state_o,
	lstn_reg_state_o,
	active_o,
	src_fail_code_o,
	src_fail_bridge_o,
	tk_reg_state_o,
	lstn_decl_state_o,
	acc_latency_o,
	snk_fail_code_o,
	snk_fail_bridge_o,
	granted_slope_bps_o,
	sr_admitted_o,
	sum_slope_bps_o,
	over_limit_o,
	dbg_vid_active_o,
	dbg_vlan_err_o,
	dbg_adm_round_o,
	dbg_pdu_done_o,
	dbg_pdu_ok_o,
	dbg_pdu_malformed_o
);
	reg _sv2v_0;
	parameter [31:0] N_SOURCES_P = 8;
	parameter [31:0] N_SINKS_P = 8;
	parameter [31:0] JOIN_MS_P = 200;
	parameter [31:0] PERIODIC_MS_P = 1000;
	parameter [31:0] LEAVE_MS_P = 5000;
	parameter [7:0] DOM_DEF_PRIO_P = 8'd3;
	parameter [15:0] DOM_DEF_VID_P = 16'd2;
	parameter [31:0] N_VIDS_P = 4;
	parameter [31:0] REFCNT_W_P = 5;
	parameter [31:0] ENC_DEPTH_P = 12;
	parameter [31:0] TP_DEPTH_P = 1024;
	parameter [31:0] TX_STD_BYTES_P = 576;
	parameter [31:0] TX_OVERSIZE_BYTES_P = 1600;
	parameter [31:0] SLOT_AW_P = 7;
	parameter [31:0] CAD_SLOT_BASE_P = 0;
	parameter [7:0] CAD_OWNER_BASE_P = 8'h20;
	parameter [31:0] TK_SLOT_BASE_P = 16;
	parameter [7:0] TK_OWNER_BASE_P = 8'h40;
	parameter [31:0] LS_SLOT_BASE_P = 24;
	parameter [7:0] LS_OWNER_BASE_P = 8'h60;
	localparam [31:0] SRC_W_C = (N_SOURCES_P > 1 ? $clog2(N_SOURCES_P) : 1);
	localparam [31:0] SNK_W_C = (N_SINKS_P > 1 ? $clog2(N_SINKS_P) : 1);
	localparam [2:0] pp_pkg_PP_SLOT_NULL_C = 3'd7;
	localparam [31:0] SLOT_W_C = 3;
	localparam [31:0] TXA_W_C = $clog2(TX_OVERSIZE_BYTES_P + 1);
	input wire clk_i;
	input wire rst_n;
	input wire [47:0] own_mac_i;
	input wire link_up_i;
	input wire p2p_i;
	input wire cfg_rank_i;
	input wire [31:0] cfg_acc_lat_ns_i;
	input wire [31:0] port_rate_bps_i;
	input wire mrp_valid_i;
	input wire [7:0] mrp_data_i;
	input wire mrp_last_i;
	input wire mrp_msrp_i;
	output wire mrp_ready_o;
	input wire req_valid_i;
	output wire req_ready_o;
	input wire [2:0] req_op_i;
	input wire [7:0] req_index_i;
	input wire [63:0] req_stream_id_i;
	input wire [47:0] req_da_i;
	input wire [11:0] req_vid_i;
	input wire [15:0] req_max_frame_i;
	input wire [15:0] req_max_interval_i;
	input wire [1:0] req_lstn_state_i;
	output reg rsp_valid_o;
	output wire [1:0] rsp_status_o;
	output wire [31:0] rsp_data_o;
	output wire alloc_req_o;
	output wire oversize_o;
	input wire [2:0] alloc_slot_i;
	input wire alloc_gnt_i;
	output wire [2:0] wr_slot_o;
	output wire [TXA_W_C - 1:0] wr_addr_o;
	output wire wr_valid_o;
	output wire [7:0] wr_data_o;
	output wire wr_commit_o;
	output wire [TXA_W_C - 1:0] wr_len_o;
	output wire txreq_valid_o;
	output wire [2:0] txreq_slot_o;
	input wire txreq_ready_i;
	input wire [31:0] now_ms_i;
	output reg arm_valid_o;
	output reg arm_cancel_o;
	output reg [SLOT_AW_P - 1:0] arm_slot_o;
	output reg [7:0] arm_owner_o;
	output reg [31:0] arm_deadline_ms_o;
	input wire exp_valid_i;
	input wire [SLOT_AW_P - 1:0] exp_slot_i;
	output reg draw_req_o;
	output wire [2:0] draw_kind_o;
	input wire draw_busy_i;
	input wire draw_valid_i;
	input wire [15:0] draw_ms_i;
	output wire [N_SINKS_P - 1:0] evt_tk_registered_o;
	output wire [N_SINKS_P - 1:0] evt_tk_unregistered_o;
	output wire [N_SOURCES_P - 1:0] lstn_reg_change_o;
	output wire evt_domain_change_o;
	output wire [2:0] class_a_prio_o;
	output wire [11:0] class_a_vid_o;
	output wire domain_adopted_o;
	output wire [(N_SOURCES_P * 2) - 1:0] tk_decl_state_o;
	output wire [(N_SOURCES_P * 2) - 1:0] lstn_reg_state_o;
	output wire [N_SOURCES_P - 1:0] active_o;
	output wire [(N_SOURCES_P * 8) - 1:0] src_fail_code_o;
	output wire [(N_SOURCES_P * 64) - 1:0] src_fail_bridge_o;
	output wire [(N_SINKS_P * 2) - 1:0] tk_reg_state_o;
	output wire [(N_SINKS_P * 2) - 1:0] lstn_decl_state_o;
	output wire [(N_SINKS_P * 32) - 1:0] acc_latency_o;
	output wire [(N_SINKS_P * 8) - 1:0] snk_fail_code_o;
	output wire [(N_SINKS_P * 64) - 1:0] snk_fail_bridge_o;
	output wire [(N_SOURCES_P * 32) - 1:0] granted_slope_bps_o;
	output wire [N_SOURCES_P - 1:0] sr_admitted_o;
	output wire [31:0] sum_slope_bps_o;
	output wire over_limit_o;
	output wire [N_VIDS_P - 1:0] dbg_vid_active_o;
	output wire dbg_vlan_err_o;
	output wire dbg_adm_round_o;
	output wire dbg_pdu_done_o;
	output wire dbg_pdu_ok_o;
	output wire dbg_pdu_malformed_o;
	localparam [2:0] OP_DECLARE_TALKER_C = 3'd0;
	localparam [2:0] OP_WITHDRAW_TALKER_C = 3'd1;
	localparam [2:0] OP_DECLARE_LISTENER_C = 3'd2;
	localparam [2:0] OP_WITHDRAW_LISTENER_C = 3'd3;
	localparam [2:0] OP_GET_DOMAIN_C = 3'd4;
	localparam [1:0] RSP_OK_C = 2'd0;
	localparam [1:0] RSP_FAIL_C = 2'd1;
	localparam [1:0] RSP_UNSUPPORTED_C = 2'd2;
	localparam [31:0] CAD_JOIN_MSRP_C = 0;
	localparam [31:0] CAD_JOIN_MVRP_C = 1;
	localparam [31:0] CAD_PERIODIC_C = 2;
	localparam [31:0] CAD_LA_MSRP_C = 3;
	localparam [31:0] CAD_LA_MVRP_C = 4;
	localparam [31:0] N_CAD_C = 5;
	wire dec_evt_valid_w;
	wire dec_evt_msrp_w;
	wire [7:0] dec_evt_attr_type_w;
	wire [63:0] dec_evt_stream_id_w;
	wire [47:0] dec_evt_da_w;
	wire [15:0] dec_evt_vid_w;
	wire [2:0] dec_evt_mrp_event_w;
	wire [1:0] dec_evt_fourpacked_w;
	wire [15:0] dec_evt_max_frame_w;
	wire [15:0] dec_evt_max_interval_w;
	wire [7:0] dec_evt_priority_w;
	wire dec_evt_rank_w;
	wire [31:0] dec_evt_acc_latency_w;
	wire [63:0] dec_evt_fail_sysid_w;
	wire [7:0] dec_evt_fail_code_w;
	wire [7:0] dec_evt_class_id_w;
	wire dec_evt_class_a_w;
	wire dec_la_msrp_w;
	wire dec_la_mvrp_w;
	wire [15:0] dec_dbg_listlen_w;
	wire dec_listlen_bad_w;
	KL_srp_decoder #(.TP_DEPTH_P(TP_DEPTH_P)) u_decoder(
		.clk_i(clk_i),
		.rst_n(rst_n),
		.mrp_valid_i(mrp_valid_i),
		.mrp_data_i(mrp_data_i),
		.mrp_last_i(mrp_last_i),
		.mrp_msrp_i(mrp_msrp_i),
		.mrp_ready_o(mrp_ready_o),
		.evt_valid_o(dec_evt_valid_w),
		.evt_msrp_o(dec_evt_msrp_w),
		.evt_attr_type_o(dec_evt_attr_type_w),
		.evt_stream_id_o(dec_evt_stream_id_w),
		.evt_da_o(dec_evt_da_w),
		.evt_vid_o(dec_evt_vid_w),
		.evt_mrp_event_o(dec_evt_mrp_event_w),
		.evt_fourpacked_o(dec_evt_fourpacked_w),
		.evt_max_frame_size_o(dec_evt_max_frame_w),
		.evt_max_interval_frames_o(dec_evt_max_interval_w),
		.evt_priority_o(dec_evt_priority_w),
		.evt_rank_o(dec_evt_rank_w),
		.evt_acc_latency_o(dec_evt_acc_latency_w),
		.evt_failure_system_id_o(dec_evt_fail_sysid_w),
		.evt_failure_code_o(dec_evt_fail_code_w),
		.evt_class_id_o(dec_evt_class_id_w),
		.evt_class_a_o(dec_evt_class_a_w),
		.la_msrp_o(dec_la_msrp_w),
		.la_mvrp_o(dec_la_mvrp_w),
		.pdu_done_o(dbg_pdu_done_o),
		.pdu_ok_o(dbg_pdu_ok_o),
		.pdu_malformed_o(dbg_pdu_malformed_o),
		.listlen_bad_o(dec_listlen_bad_w),
		.dbg_listlen_cnt_o(dec_dbg_listlen_w)
	);
	reg p_join_fsm_r;
	reg p_periodic_r;
	reg p_la_msrp_r;
	reg p_la_mvrp_r;
	reg [1:0] enc_join_r;
	reg [1:0] enc_la_r;
	wire dom_rx_valid_w;
	wire dom_rx_reg_w;
	wire dom_ev_valid_w;
	wire [2:0] dom_ev_event_w;
	wire [31:0] dom_ev_value_w;
	wire dom_ev_ready_w;
	wire [2:0] dom_prio_w;
	wire [11:0] dom_vid_w;
	assign dom_rx_reg_w = ((dec_evt_mrp_event_w == 3'd0) || (dec_evt_mrp_event_w == 3'd1)) || (dec_evt_mrp_event_w == 3'd3);
	localparam [7:0] srp_pkg_SRP_MSRP_ATTR_DOMAIN_C = 8'd4;
	assign dom_rx_valid_w = (((dec_evt_valid_w && dec_evt_msrp_w) && (dec_evt_attr_type_w == srp_pkg_SRP_MSRP_ATTR_DOMAIN_C)) && dec_evt_class_a_w) && dom_rx_reg_w;
	KL_srp_domain #(
		.DEF_PRIO_P(DOM_DEF_PRIO_P),
		.DEF_VID_P(DOM_DEF_VID_P)
	) u_domain(
		.clk_i(clk_i),
		.rst_n(rst_n),
		.link_up_i(link_up_i),
		.rxdom_valid_i(dom_rx_valid_w),
		.rxdom_class_id_i(dec_evt_class_id_w),
		.rxdom_prio_i(dec_evt_priority_w),
		.rxdom_vid_i(dec_evt_vid_w),
		.rxdom_nov_i(13'd1),
		.periodic_tick_i(p_periodic_r),
		.leaveall_tick_i(dec_la_msrp_w || p_la_msrp_r),
		.dom_ev_valid_o(dom_ev_valid_w),
		.dom_ev_event_o(dom_ev_event_w),
		.dom_ev_value_o(dom_ev_value_w),
		.dom_ev_ready_i(dom_ev_ready_w),
		.evt_domain_change_o(evt_domain_change_o),
		.class_a_prio_o(dom_prio_w),
		.class_a_vid_o(dom_vid_w),
		.adopted_o(domain_adopted_o)
	);
	assign class_a_prio_o = dom_prio_w;
	assign class_a_vid_o = dom_vid_w;
	wire vlan_user_valid_w;
	wire vlan_user_join_w;
	wire [11:0] vlan_user_vid_w;
	wire vlan_user_ready_w;
	wire vlan_ev_valid_w;
	wire [2:0] vlan_ev_event_w;
	wire [15:0] vlan_ev_vid_w;
	wire vlan_ev_ready_w;
	wire tk_user_valid_w;
	wire tk_user_join_w;
	wire [11:0] tk_user_vid_w;
	wire ls_user_valid_w;
	wire ls_user_join_w;
	wire [11:0] ls_user_vid_w;
	wire vu_sel_ls_w;
	reg vrr_r;
	assign vu_sel_ls_w = ls_user_valid_w && (!tk_user_valid_w || vrr_r);
	assign vlan_user_valid_w = tk_user_valid_w || ls_user_valid_w;
	assign vlan_user_join_w = (vu_sel_ls_w ? ls_user_join_w : tk_user_join_w);
	assign vlan_user_vid_w = (vu_sel_ls_w ? ls_user_vid_w : tk_user_vid_w);
	always @(posedge clk_i) begin : vlan_user_rr
		if (!rst_n)
			vrr_r <= 1'b0;
		else if (vlan_user_valid_w && vlan_user_ready_w)
			vrr_r <= ~vrr_r;
	end
	KL_srp_vlan #(
		.N_VIDS_P(N_VIDS_P),
		.REFCNT_W_P(REFCNT_W_P)
	) u_vlan(
		.clk_i(clk_i),
		.rst_n(rst_n),
		.user_valid_i(vlan_user_valid_w),
		.user_join_i(vlan_user_join_w),
		.user_vid_i(vlan_user_vid_w),
		.user_ready_o(vlan_user_ready_w),
		.user_err_o(dbg_vlan_err_o),
		.periodic_tick_i(p_periodic_r),
		.leaveall_tick_i(dec_la_mvrp_w || p_la_mvrp_r),
		.vlan_ev_valid_o(vlan_ev_valid_w),
		.vlan_ev_event_o(vlan_ev_event_w),
		.vlan_ev_vid_o(vlan_ev_vid_w),
		.vlan_ev_ready_i(vlan_ev_ready_w),
		.vid_active_o(dbg_vid_active_o)
	);
	reg [N_SOURCES_P - 1:0] adm_req_r;
	reg [(N_SOURCES_P * 16) - 1:0] adm_mfs_r;
	reg [(N_SOURCES_P * 16) - 1:0] adm_mif_r;
	wire [N_SOURCES_P - 1:0] adm_admitted_w;
	wire adm_round_w;
	reg [N_SOURCES_P - 1:0] opt_r;
	reg [(N_SOURCES_P * 2) - 1:0] opt_cnt_r;
	wire [N_SOURCES_P - 1:0] sr_adm_fsm_w;
	KL_srp_admission #(.N_SOURCES_P(N_SOURCES_P)) u_admission(
		.clk_i(clk_i),
		.rst_n(rst_n),
		.req_i(adm_req_r),
		.max_frame_i(adm_mfs_r),
		.interval_frames_i(adm_mif_r),
		.port_rate_bps_i(port_rate_bps_i),
		.sr_admitted_o(adm_admitted_w),
		.granted_slope_bps_o(granted_slope_bps_o),
		.sum_slope_bps_o(sum_slope_bps_o),
		.over_limit_o(over_limit_o),
		.round_done_o(adm_round_w)
	);
	assign sr_admitted_o = adm_admitted_w;
	assign dbg_adm_round_o = adm_round_w;
	assign sr_adm_fsm_w = opt_r | adm_admitted_w;
	wire gate_valid_w;
	wire gate_ready_w;
	wire tk_txop_done_w;
	wire tk_ev_valid_w;
	wire tk_ev_ready_w;
	wire tk_ev_app_w;
	wire [7:0] tk_ev_type_w;
	wire [2:0] tk_ev_event_w;
	wire [1:0] tk_ev_fp_w;
	wire [271:0] tk_ev_value_w;
	wire tk_user_ready_w;
	wire tk_arm_v_w;
	wire tk_arm_cancel_w;
	wire [SLOT_AW_P - 1:0] tk_arm_slot_w;
	wire [7:0] tk_arm_owner_w;
	wire [31:0] tk_arm_dl_w;
	wire [(N_SOURCES_P * 4) - 1:0] tk_dbg_app_w;
	wire [(N_SOURCES_P * 2) - 1:0] tk_dbg_reg_w;
	reg [7:0] a_idx_r;
	reg [63:0] a_sid_r;
	reg [47:0] a_da_r;
	reg [11:0] a_vid_r;
	reg [15:0] a_mfs_r;
	reg [15:0] a_mif_r;
	reg a_open_r;
	KL_srp_talker_fsm #(
		.N_SOURCES_P(N_SOURCES_P),
		.LEAVE_MS_P(LEAVE_MS_P),
		.SLOT_BASE_P(TK_SLOT_BASE_P),
		.SLOT_AW_P(SLOT_AW_P),
		.OWNER_BASE_P(TK_OWNER_BASE_P)
	) u_talker(
		.clk_i(clk_i),
		.rst_n(rst_n),
		.own_mac_i(own_mac_i),
		.p2p_i(p2p_i),
		.gate_valid_i(gate_valid_w),
		.gate_ready_o(gate_ready_w),
		.gate_open_i(a_open_r),
		.gate_src_i(a_idx_r[SRC_W_C - 1:0]),
		.gate_stream_id_i(a_sid_r),
		.gate_da_i(a_da_r),
		.gate_vid_i(a_vid_r),
		.gate_max_frame_i(a_mfs_r),
		.gate_max_interval_i(a_mif_r),
		.gate_prio_i(dom_prio_w),
		.gate_rank_i(cfg_rank_i),
		.gate_acc_lat_i(cfg_acc_lat_ns_i),
		.sr_admitted_i(sr_adm_fsm_w),
		.evt_valid_i(dec_evt_valid_w),
		.evt_msrp_i(dec_evt_msrp_w),
		.evt_attr_type_i(dec_evt_attr_type_w),
		.evt_stream_id_i(dec_evt_stream_id_w),
		.evt_da_i(dec_evt_da_w),
		.evt_vid_i(dec_evt_vid_w),
		.evt_mrp_event_i(dec_evt_mrp_event_w),
		.evt_fourpacked_i(dec_evt_fourpacked_w),
		.join_tick_i(p_join_fsm_r),
		.periodic_tick_i(p_periodic_r),
		.leaveall_rx_i(dec_la_msrp_w),
		.leaveall_own_i(p_la_msrp_r),
		.txop_done_o(tk_txop_done_w),
		.ev_valid_o(tk_ev_valid_w),
		.ev_ready_i(tk_ev_ready_w),
		.ev_app_o(tk_ev_app_w),
		.ev_attr_type_o(tk_ev_type_w),
		.ev_event_o(tk_ev_event_w),
		.ev_fourpack_o(tk_ev_fp_w),
		.ev_value_o(tk_ev_value_w),
		.user_valid_o(tk_user_valid_w),
		.user_join_o(tk_user_join_w),
		.user_vid_o(tk_user_vid_w),
		.user_ready_i(tk_user_ready_w),
		.now_ms_i(now_ms_i),
		.arm_valid_o(tk_arm_v_w),
		.arm_cancel_o(tk_arm_cancel_w),
		.arm_slot_o(tk_arm_slot_w),
		.arm_owner_o(tk_arm_owner_w),
		.arm_deadline_ms_o(tk_arm_dl_w),
		.exp_valid_i(exp_valid_i),
		.exp_slot_i(exp_slot_i),
		.lstn_reg_change_o(lstn_reg_change_o),
		.tk_decl_state_o(tk_decl_state_o),
		.lstn_reg_state_o(lstn_reg_state_o),
		.active_o(active_o),
		.msrp_fail_code_o(src_fail_code_o),
		.msrp_fail_bridge_o(src_fail_bridge_o),
		.dbg_app_state_o(tk_dbg_app_w),
		.dbg_reg_state_o(tk_dbg_reg_w)
	);
	wire ctl_valid_w;
	wire ctl_ready_w;
	wire ls_txop_done_w;
	wire ls_ev_valid_w;
	wire ls_ev_ready_w;
	wire ls_ev_app_w;
	wire [7:0] ls_ev_type_w;
	wire [2:0] ls_ev_event_w;
	wire [1:0] ls_ev_fp_w;
	wire [271:0] ls_ev_value_w;
	wire ls_user_ready_w;
	wire ls_arm_v_w;
	wire ls_arm_cancel_w;
	wire [SLOT_AW_P - 1:0] ls_arm_slot_w;
	wire [7:0] ls_arm_owner_w;
	wire [31:0] ls_arm_dl_w;
	wire [(N_SINKS_P * 4) - 1:0] ls_dbg_app_w;
	wire [(N_SINKS_P * 2) - 1:0] ls_dbg_reg_w;
	KL_srp_listener_fsm #(
		.N_SINKS_P(N_SINKS_P),
		.LEAVE_MS_P(LEAVE_MS_P),
		.SLOT_BASE_P(LS_SLOT_BASE_P),
		.SLOT_AW_P(SLOT_AW_P),
		.OWNER_BASE_P(LS_OWNER_BASE_P)
	) u_listener(
		.clk_i(clk_i),
		.rst_n(rst_n),
		.p2p_i(p2p_i),
		.ctl_valid_i(ctl_valid_w),
		.ctl_ready_o(ctl_ready_w),
		.ctl_settle_i(a_open_r),
		.ctl_sink_i(a_idx_r[SNK_W_C - 1:0]),
		.ctl_stream_id_i(a_sid_r),
		.ctl_da_i(a_da_r),
		.ctl_vid_i(a_vid_r),
		.evt_valid_i(dec_evt_valid_w),
		.evt_msrp_i(dec_evt_msrp_w),
		.evt_attr_type_i(dec_evt_attr_type_w),
		.evt_stream_id_i(dec_evt_stream_id_w),
		.evt_da_i(dec_evt_da_w),
		.evt_vid_i(dec_evt_vid_w),
		.evt_mrp_event_i(dec_evt_mrp_event_w),
		.evt_acc_latency_i(dec_evt_acc_latency_w),
		.evt_failure_system_id_i(dec_evt_fail_sysid_w),
		.evt_failure_code_i(dec_evt_fail_code_w),
		.join_tick_i(p_join_fsm_r),
		.periodic_tick_i(p_periodic_r),
		.leaveall_rx_i(dec_la_msrp_w),
		.leaveall_own_i(p_la_msrp_r),
		.txop_done_o(ls_txop_done_w),
		.ev_valid_o(ls_ev_valid_w),
		.ev_ready_i(ls_ev_ready_w),
		.ev_app_o(ls_ev_app_w),
		.ev_attr_type_o(ls_ev_type_w),
		.ev_event_o(ls_ev_event_w),
		.ev_fourpack_o(ls_ev_fp_w),
		.ev_value_o(ls_ev_value_w),
		.user_valid_o(ls_user_valid_w),
		.user_join_o(ls_user_join_w),
		.user_vid_o(ls_user_vid_w),
		.user_ready_i(ls_user_ready_w),
		.now_ms_i(now_ms_i),
		.arm_valid_o(ls_arm_v_w),
		.arm_cancel_o(ls_arm_cancel_w),
		.arm_slot_o(ls_arm_slot_w),
		.arm_owner_o(ls_arm_owner_w),
		.arm_deadline_ms_o(ls_arm_dl_w),
		.exp_valid_i(exp_valid_i),
		.exp_slot_i(exp_slot_i),
		.evt_tk_registered_o(evt_tk_registered_o),
		.evt_tk_unregistered_o(evt_tk_unregistered_o),
		.tk_reg_state_o(tk_reg_state_o),
		.lstn_decl_state_o(lstn_decl_state_o),
		.acc_latency_o(acc_latency_o),
		.msrp_fail_code_o(snk_fail_code_o),
		.msrp_fail_bridge_o(snk_fail_bridge_o),
		.dbg_app_state_o(ls_dbg_app_w),
		.dbg_reg_state_o(ls_dbg_reg_w)
	);
	assign tk_user_ready_w = (vlan_user_ready_w && tk_user_valid_w) && !vu_sel_ls_w;
	assign ls_user_ready_w = vlan_user_ready_w && vu_sel_ls_w;
	reg enc_ev_valid_w;
	wire enc_ev_ready_w;
	reg enc_ev_app_w;
	reg [7:0] enc_ev_type_w;
	reg [2:0] enc_ev_event_w;
	reg [1:0] enc_ev_fp_w;
	reg [271:0] enc_ev_value_w;
	wire enc_ev_drop_w;
	wire [$clog2(ENC_DEPTH_P + 1) - 1:0] enc_cnt_msrp_w;
	wire [$clog2(ENC_DEPTH_P + 1) - 1:0] enc_cnt_mvrp_w;
	localparam [7:0] srp_pkg_SRP_MVRP_ATTR_VID_C = 8'd1;
	always @(*) begin : enc_intake_mux
		if (_sv2v_0)
			;
		enc_ev_valid_w = 1'b1;
		if (dom_ev_valid_w) begin
			enc_ev_app_w = 1'b0;
			enc_ev_type_w = srp_pkg_SRP_MSRP_ATTR_DOMAIN_C;
			enc_ev_event_w = dom_ev_event_w;
			enc_ev_fp_w = 2'd0;
			enc_ev_value_w = {dom_ev_value_w, 240'd0};
		end
		else if (vlan_ev_valid_w) begin
			enc_ev_app_w = 1'b1;
			enc_ev_type_w = srp_pkg_SRP_MVRP_ATTR_VID_C;
			enc_ev_event_w = vlan_ev_event_w;
			enc_ev_fp_w = 2'd0;
			enc_ev_value_w = {vlan_ev_vid_w, 256'd0};
		end
		else if (tk_ev_valid_w) begin
			enc_ev_app_w = tk_ev_app_w;
			enc_ev_type_w = tk_ev_type_w;
			enc_ev_event_w = tk_ev_event_w;
			enc_ev_fp_w = tk_ev_fp_w;
			enc_ev_value_w = tk_ev_value_w;
		end
		else if (ls_ev_valid_w) begin
			enc_ev_app_w = ls_ev_app_w;
			enc_ev_type_w = ls_ev_type_w;
			enc_ev_event_w = ls_ev_event_w;
			enc_ev_fp_w = ls_ev_fp_w;
			enc_ev_value_w = ls_ev_value_w;
		end
		else begin
			enc_ev_valid_w = 1'b0;
			enc_ev_app_w = 1'b0;
			enc_ev_type_w = 8'd0;
			enc_ev_event_w = 3'd0;
			enc_ev_fp_w = 2'd0;
			enc_ev_value_w = 272'd0;
		end
	end
	assign dom_ev_ready_w = enc_ev_ready_w && dom_ev_valid_w;
	assign vlan_ev_ready_w = (enc_ev_ready_w && !dom_ev_valid_w) && vlan_ev_valid_w;
	assign tk_ev_ready_w = ((enc_ev_ready_w && !dom_ev_valid_w) && !vlan_ev_valid_w) && tk_ev_valid_w;
	assign ls_ev_ready_w = (((enc_ev_ready_w && !dom_ev_valid_w) && !vlan_ev_valid_w) && !tk_ev_valid_w) && ls_ev_valid_w;
	KL_srp_encoder #(
		.DEPTH_P(ENC_DEPTH_P),
		.TX_STD_BYTES_P(TX_STD_BYTES_P),
		.TX_OVERSIZE_BYTES_P(TX_OVERSIZE_BYTES_P)
	) u_encoder(
		.clk_i(clk_i),
		.rst_n(rst_n),
		.ev_valid_i(enc_ev_valid_w),
		.ev_ready_o(enc_ev_ready_w),
		.ev_app_i(enc_ev_app_w),
		.ev_attr_type_i(enc_ev_type_w),
		.ev_event_i(enc_ev_event_w),
		.ev_fourpack_i(enc_ev_fp_w),
		.ev_value_i(enc_ev_value_w),
		.ev_drop_o(enc_ev_drop_w),
		.join_tick_i(enc_join_r),
		.leaveall_i(enc_la_r),
		.own_mac_i(own_mac_i),
		.alloc_req_o(alloc_req_o),
		.oversize_o(oversize_o),
		.alloc_slot_i(alloc_slot_i),
		.alloc_gnt_i(alloc_gnt_i),
		.wr_slot_o(wr_slot_o),
		.wr_addr_o(wr_addr_o),
		.wr_valid_o(wr_valid_o),
		.wr_data_o(wr_data_o),
		.wr_commit_o(wr_commit_o),
		.wr_len_o(wr_len_o),
		.txreq_valid_o(txreq_valid_o),
		.txreq_slot_o(txreq_slot_o),
		.txreq_ready_i(txreq_ready_i),
		.dbg_cnt_msrp_o(enc_cnt_msrp_w),
		.dbg_cnt_mvrp_o(enc_cnt_mvrp_w)
	);
	reg [1:0] svc_st_r;
	reg [1:0] rsp_status_r;
	reg [31:0] rsp_data_r;
	wire svc_acc_w;
	wire gate_acc_w;
	wire ctl_acc_w;
	assign req_ready_o = svc_st_r == 2'd0;
	assign svc_acc_w = req_valid_i && req_ready_o;
	assign gate_valid_w = svc_st_r == 2'd1;
	assign ctl_valid_w = svc_st_r == 2'd2;
	assign gate_acc_w = gate_valid_w && gate_ready_w;
	assign ctl_acc_w = ctl_valid_w && ctl_ready_w;
	localparam [7:0] srp_pkg_SRP_CLASS_A_ID_C = 8'd6;
	function automatic [31:0] sv2v_cast_32;
		input reg [31:0] inp;
		sv2v_cast_32 = inp;
	endfunction
	always @(posedge clk_i) begin : service_plane
		if (!rst_n) begin
			svc_st_r <= 2'd0;
			a_idx_r <= 8'd0;
			a_sid_r <= 64'd0;
			a_da_r <= 48'd0;
			a_vid_r <= 12'd0;
			a_mfs_r <= 16'd0;
			a_mif_r <= 16'd0;
			a_open_r <= 1'b0;
			rsp_status_r <= RSP_OK_C;
			rsp_data_r <= 32'd0;
			rsp_valid_o <= 1'b0;
			adm_req_r <= 1'sb0;
			adm_mfs_r <= 1'sb0;
			adm_mif_r <= 1'sb0;
			opt_r <= 1'sb0;
			opt_cnt_r <= 1'sb0;
		end
		else begin
			rsp_valid_o <= 1'b0;
			if (adm_round_w) begin : sv2v_autoblock_1
				reg [31:0] s;
				for (s = 0; s < N_SOURCES_P; s = s + 1)
					if (opt_r[s]) begin
						if (opt_cnt_r[s * 2+:2] != 2'd0)
							opt_cnt_r[s * 2+:2] <= opt_cnt_r[s * 2+:2] - 2'd1;
						else
							opt_r[s] <= 1'b0;
					end
			end
			(* full_case, parallel_case *)
			case (svc_st_r)
				2'd0:
					if (svc_acc_w) begin
						a_idx_r <= req_index_i;
						a_sid_r <= req_stream_id_i;
						a_da_r <= req_da_i;
						a_vid_r <= req_vid_i;
						a_mfs_r <= req_max_frame_i;
						a_mif_r <= req_max_interval_i;
						(* full_case, parallel_case *)
						case (req_op_i)
							OP_DECLARE_TALKER_C:
								if (sv2v_cast_32(req_index_i) < N_SOURCES_P) begin
									a_open_r <= 1'b1;
									svc_st_r <= 2'd1;
								end
								else begin
									rsp_status_r <= RSP_FAIL_C;
									svc_st_r <= 2'd3;
								end
							OP_WITHDRAW_TALKER_C:
								if (sv2v_cast_32(req_index_i) < N_SOURCES_P) begin
									a_open_r <= 1'b0;
									svc_st_r <= 2'd1;
								end
								else begin
									rsp_status_r <= RSP_FAIL_C;
									svc_st_r <= 2'd3;
								end
							OP_DECLARE_LISTENER_C:
								if (sv2v_cast_32(req_index_i) < N_SINKS_P) begin
									a_open_r <= req_lstn_state_i != 2'd0;
									svc_st_r <= 2'd2;
								end
								else begin
									rsp_status_r <= RSP_FAIL_C;
									svc_st_r <= 2'd3;
								end
							OP_WITHDRAW_LISTENER_C:
								if (sv2v_cast_32(req_index_i) < N_SINKS_P) begin
									a_open_r <= 1'b0;
									svc_st_r <= 2'd2;
								end
								else begin
									rsp_status_r <= RSP_FAIL_C;
									svc_st_r <= 2'd3;
								end
							OP_GET_DOMAIN_C: begin
								if (req_index_i == srp_pkg_SRP_CLASS_A_ID_C) begin
									rsp_status_r <= RSP_OK_C;
									rsp_data_r <= {13'd0, dom_prio_w, 4'd0, dom_vid_w};
								end
								else begin
									rsp_status_r <= RSP_FAIL_C;
									rsp_data_r <= 32'd0;
								end
								svc_st_r <= 2'd3;
							end
							default: begin
								rsp_status_r <= RSP_UNSUPPORTED_C;
								svc_st_r <= 2'd3;
							end
						endcase
					end
				2'd1:
					if (gate_acc_w) begin
						if (a_open_r) begin
							adm_req_r[a_idx_r[SRC_W_C - 1:0]] <= 1'b1;
							adm_mfs_r[a_idx_r[SRC_W_C - 1:0] * 16+:16] <= a_mfs_r;
							adm_mif_r[a_idx_r[SRC_W_C - 1:0] * 16+:16] <= a_mif_r;
							opt_r[a_idx_r[SRC_W_C - 1:0]] <= 1'b1;
							opt_cnt_r[a_idx_r[SRC_W_C - 1:0] * 2+:2] <= 2'd2;
						end
						else begin
							adm_req_r[a_idx_r[SRC_W_C - 1:0]] <= 1'b0;
							opt_r[a_idx_r[SRC_W_C - 1:0]] <= 1'b0;
						end
						rsp_status_r <= RSP_OK_C;
						svc_st_r <= 2'd3;
					end
				2'd2:
					if (ctl_acc_w) begin
						rsp_status_r <= RSP_OK_C;
						svc_st_r <= 2'd3;
					end
				default: begin
					rsp_valid_o <= 1'b1;
					svc_st_r <= 2'd0;
				end
			endcase
		end
	end
	assign rsp_status_o = rsp_status_r;
	assign rsp_data_o = rsp_data_r;
	localparam [31:0] TFW_C = (1 + SLOT_AW_P) + 40;
	localparam [31:0] TFD_C = 32;
	reg [TFW_C - 1:0] tf_ram_r [0:1][0:31];
	reg [TFW_C - 1:0] tf_q_r [0:1];
	reg [4:0] tf_wptr_r [0:1];
	reg [4:0] tf_rptr_r [0:1];
	reg [5:0] tf_cnt_r [0:1];
	wire [1:0] tf_push_w;
	wire [1:0] tf_pop_w;
	function automatic [5:0] sv2v_cast_6;
		input reg [5:0] inp;
		sv2v_cast_6 = inp;
	endfunction
	assign tf_push_w[0] = tk_arm_v_w && (tf_cnt_r[0] != sv2v_cast_6(TFD_C));
	assign tf_push_w[1] = ls_arm_v_w && (tf_cnt_r[1] != sv2v_cast_6(TFD_C));
	always @(posedge clk_i) begin : tf_write
		if (tf_push_w[0])
			tf_ram_r[0][tf_wptr_r[0]] <= {tk_arm_cancel_w, tk_arm_slot_w, tk_arm_owner_w, tk_arm_dl_w};
		if (tf_push_w[1])
			tf_ram_r[1][tf_wptr_r[1]] <= {ls_arm_cancel_w, ls_arm_slot_w, ls_arm_owner_w, ls_arm_dl_w};
	end
	always @(posedge clk_i) begin : tf_read
		tf_q_r[0] <= tf_ram_r[0][tf_rptr_r[0]];
		tf_q_r[1] <= tf_ram_r[1][tf_rptr_r[1]];
	end
	reg tm_st_r;
	reg tm_sel_r;
	reg tm_rr_r;
	reg init_done_r;
	reg [4:0] cad_pend_r;
	reg [159:0] cad_dl_r;
	reg [2:0] cad_ix_w;
	reg [1:0] need_draw_r;
	reg dr_inflight_r;
	reg dr_app_r;
	reg rnd_act_r;
	reg td_tk_r;
	reg td_ls_r;
	reg hw_full_q_r;
	wire enc_msrp_full_w;
	wire cad_hit_w;
	wire [31:0] cad_exp_ix_w;
	function automatic signed [2:0] sv2v_cast_3_signed;
		input reg signed [2:0] inp;
		sv2v_cast_3_signed = inp;
	endfunction
	function automatic signed [31:0] sv2v_cast_32_signed;
		input reg signed [31:0] inp;
		sv2v_cast_32_signed = inp;
	endfunction
	always @(*) begin : cad_pick
		if (_sv2v_0)
			;
		cad_ix_w = 3'd0;
		begin : sv2v_autoblock_2
			reg signed [31:0] i;
			for (i = sv2v_cast_32_signed(N_CAD_C) - 1; i >= 0; i = i - 1)
				if (cad_pend_r[i])
					cad_ix_w = sv2v_cast_3_signed(i);
		end
	end
	assign cad_exp_ix_w = sv2v_cast_32(exp_slot_i) - CAD_SLOT_BASE_P;
	assign cad_hit_w = exp_valid_i && (cad_exp_ix_w < N_CAD_C);
	assign enc_msrp_full_w = sv2v_cast_32(enc_cnt_msrp_w) == ENC_DEPTH_P;
	assign draw_kind_o = 3'd3;
	function automatic [SLOT_AW_P - 1:0] sv2v_cast_42C2E;
		input reg [SLOT_AW_P - 1:0] inp;
		sv2v_cast_42C2E = inp;
	endfunction
	function automatic [2:0] sv2v_cast_3;
		input reg [2:0] inp;
		sv2v_cast_3 = inp;
	endfunction
	always @(posedge clk_i) begin : timer_cadence_plane
		if (!rst_n) begin
			arm_valid_o <= 1'b0;
			arm_cancel_o <= 1'b0;
			arm_slot_o <= 1'sb0;
			arm_owner_o <= 8'd0;
			arm_deadline_ms_o <= 32'd0;
			tf_wptr_r[0] <= 1'sb0;
			tf_wptr_r[1] <= 1'sb0;
			tf_rptr_r[0] <= 1'sb0;
			tf_rptr_r[1] <= 1'sb0;
			tf_cnt_r[0] <= 1'sb0;
			tf_cnt_r[1] <= 1'sb0;
			tm_st_r <= 1'b0;
			tm_sel_r <= 1'b0;
			tm_rr_r <= 1'b0;
			init_done_r <= 1'b0;
			cad_pend_r <= 1'sb0;
			cad_dl_r <= 1'sb0;
			need_draw_r <= 2'b00;
			dr_inflight_r <= 1'b0;
			dr_app_r <= 1'b0;
			draw_req_o <= 1'b0;
			rnd_act_r <= 1'b0;
			td_tk_r <= 1'b0;
			td_ls_r <= 1'b0;
			hw_full_q_r <= 1'b0;
			p_join_fsm_r <= 1'b0;
			p_periodic_r <= 1'b0;
			p_la_msrp_r <= 1'b0;
			p_la_mvrp_r <= 1'b0;
			enc_join_r <= 2'b00;
			enc_la_r <= 2'b00;
		end
		else begin
			arm_valid_o <= 1'b0;
			draw_req_o <= 1'b0;
			p_join_fsm_r <= 1'b0;
			p_periodic_r <= 1'b0;
			p_la_msrp_r <= 1'b0;
			p_la_mvrp_r <= 1'b0;
			enc_join_r <= 2'b00;
			enc_la_r <= 2'b00;
			begin : sv2v_autoblock_3
				reg [31:0] u;
				for (u = 0; u < 2; u = u + 1)
					begin
						if (tf_push_w[u])
							tf_wptr_r[u] <= tf_wptr_r[u] + 5'd1;
						tf_cnt_r[u] <= (tf_cnt_r[u] + {5'd0, tf_push_w[u]}) - {5'd0, tf_pop_w[u]};
					end
			end
			(* full_case, parallel_case *)
			case (tm_st_r)
				1'b0:
					if ((tf_cnt_r[0] != 6'd0) && (!tm_rr_r || (tf_cnt_r[1] == 6'd0))) begin
						tm_sel_r <= 1'b0;
						tm_st_r <= 1'b1;
					end
					else if (tf_cnt_r[1] != 6'd0) begin
						tm_sel_r <= 1'b1;
						tm_st_r <= 1'b1;
					end
					else if (cad_pend_r != {5 {1'sb0}}) begin
						arm_valid_o <= 1'b1;
						arm_cancel_o <= 1'b0;
						arm_slot_o <= sv2v_cast_42C2E(CAD_SLOT_BASE_P + sv2v_cast_32(cad_ix_w));
						arm_owner_o <= CAD_OWNER_BASE_P + {5'd0, cad_ix_w};
						arm_deadline_ms_o <= cad_dl_r[cad_ix_w * 32+:32];
						cad_pend_r[cad_ix_w] <= 1'b0;
					end
				default: begin
					arm_valid_o <= 1'b1;
					{arm_cancel_o, arm_slot_o, arm_owner_o, arm_deadline_ms_o} <= tf_q_r[tm_sel_r];
					tf_rptr_r[tm_sel_r] <= tf_rptr_r[tm_sel_r] + 5'd1;
					tm_rr_r <= ~tm_rr_r;
					tm_st_r <= 1'b0;
				end
			endcase
			if (rnd_act_r && tk_txop_done_w)
				td_tk_r <= 1'b1;
			if (rnd_act_r && ls_txop_done_w)
				td_ls_r <= 1'b1;
			if ((rnd_act_r && (td_tk_r || tk_txop_done_w)) && (td_ls_r || ls_txop_done_w)) begin
				enc_join_r[0] <= 1'b1;
				rnd_act_r <= 1'b0;
			end
			hw_full_q_r <= enc_msrp_full_w;
			if ((rnd_act_r && enc_msrp_full_w) && !hw_full_q_r)
				enc_join_r[0] <= 1'b1;
			if (dr_inflight_r) begin
				if (draw_valid_i) begin
					dr_inflight_r <= 1'b0;
					if (dr_app_r) begin
						cad_pend_r[CAD_LA_MVRP_C] <= 1'b1;
						cad_dl_r[128+:32] <= now_ms_i + {16'd0, draw_ms_i};
					end
					else begin
						cad_pend_r[CAD_LA_MSRP_C] <= 1'b1;
						cad_dl_r[96+:32] <= now_ms_i + {16'd0, draw_ms_i};
					end
				end
			end
			else if (!draw_busy_i && (need_draw_r != 2'b00)) begin
				draw_req_o <= 1'b1;
				dr_inflight_r <= 1'b1;
				dr_app_r <= !need_draw_r[0];
				if (need_draw_r[0])
					need_draw_r[0] <= 1'b0;
				else
					need_draw_r[1] <= 1'b0;
			end
			if (!init_done_r) begin
				init_done_r <= 1'b1;
				cad_pend_r[CAD_JOIN_MSRP_C] <= 1'b1;
				cad_dl_r[0+:32] <= now_ms_i + JOIN_MS_P;
				cad_pend_r[CAD_JOIN_MVRP_C] <= 1'b1;
				cad_dl_r[32+:32] <= now_ms_i + JOIN_MS_P;
				cad_pend_r[CAD_PERIODIC_C] <= 1'b1;
				cad_dl_r[64+:32] <= now_ms_i + PERIODIC_MS_P;
				need_draw_r <= 2'b11;
			end
			if (cad_hit_w)
				(* full_case, parallel_case *)
				case (cad_exp_ix_w[2:0])
					sv2v_cast_3(CAD_JOIN_MSRP_C): begin
						p_join_fsm_r <= 1'b1;
						rnd_act_r <= 1'b1;
						td_tk_r <= 1'b0;
						td_ls_r <= 1'b0;
						cad_pend_r[CAD_JOIN_MSRP_C] <= 1'b1;
						cad_dl_r[0+:32] <= now_ms_i + JOIN_MS_P;
					end
					sv2v_cast_3(CAD_JOIN_MVRP_C): begin
						enc_join_r[1] <= 1'b1;
						cad_pend_r[CAD_JOIN_MVRP_C] <= 1'b1;
						cad_dl_r[32+:32] <= now_ms_i + JOIN_MS_P;
					end
					sv2v_cast_3(CAD_PERIODIC_C): begin
						p_periodic_r <= 1'b1;
						cad_pend_r[CAD_PERIODIC_C] <= 1'b1;
						cad_dl_r[64+:32] <= now_ms_i + PERIODIC_MS_P;
					end
					sv2v_cast_3(CAD_LA_MSRP_C): begin
						p_la_msrp_r <= 1'b1;
						enc_la_r[0] <= 1'b1;
						need_draw_r[0] <= 1'b1;
					end
					default: begin
						p_la_mvrp_r <= 1'b1;
						enc_la_r[1] <= 1'b1;
						need_draw_r[1] <= 1'b1;
					end
				endcase
		end
	end
	assign tf_pop_w[0] = (tm_st_r == 1'b1) && !tm_sel_r;
	assign tf_pop_w[1] = (tm_st_r == 1'b1) && tm_sel_r;
	initial _sv2v_0 = 0;
endmodule
`default_nettype wire
`default_nettype none
module KL_srp_vlan (
	clk_i,
	rst_n,
	user_valid_i,
	user_join_i,
	user_vid_i,
	user_ready_o,
	user_err_o,
	periodic_tick_i,
	leaveall_tick_i,
	vlan_ev_valid_o,
	vlan_ev_event_o,
	vlan_ev_vid_o,
	vlan_ev_ready_i,
	vid_active_o
);
	reg _sv2v_0;
	parameter [31:0] N_VIDS_P = 4;
	parameter [31:0] REFCNT_W_P = 5;
	input wire clk_i;
	input wire rst_n;
	input wire user_valid_i;
	input wire user_join_i;
	input wire [11:0] user_vid_i;
	output wire user_ready_o;
	output reg user_err_o;
	input wire periodic_tick_i;
	input wire leaveall_tick_i;
	output wire vlan_ev_valid_o;
	output wire [2:0] vlan_ev_event_o;
	output wire [15:0] vlan_ev_vid_o;
	input wire vlan_ev_ready_i;
	output wire [N_VIDS_P - 1:0] vid_active_o;
	localparam [31:0] IDX_W_C = (N_VIDS_P > 1 ? $clog2(N_VIDS_P) : 1);
	localparam [31:0] ENT_W_C = 12 + REFCNT_W_P;
	function automatic signed [REFCNT_W_P - 1:0] sv2v_cast_27020_signed;
		input reg signed [REFCNT_W_P - 1:0] inp;
		sv2v_cast_27020_signed = inp;
	endfunction
	localparam [REFCNT_W_P - 1:0] CNT_ONE_C = sv2v_cast_27020_signed(1);
	localparam [REFCNT_W_P - 1:0] CNT_MAX_C = 1'sb1;
	localparam [2:0] EV_NEW_C = 3'd0;
	localparam [2:0] EV_JOININ_C = 3'd1;
	localparam [2:0] EV_LV_C = 3'd5;
	reg [ENT_W_C - 1:0] tbl_r [0:N_VIDS_P - 1];
	reg [ENT_W_C - 1:0] tbl_q_r;
	reg [N_VIDS_P - 1:0] active_r;
	wire [IDX_W_C - 1:0] rd_addr_w;
	reg tbl_we_w;
	reg [IDX_W_C - 1:0] tbl_wix_w;
	reg [ENT_W_C - 1:0] tbl_wdat_w;
	always @(posedge clk_i) begin : tbl_write
		if (tbl_we_w)
			tbl_r[tbl_wix_w] <= tbl_wdat_w;
	end
	always @(posedge clk_i) begin : tbl_read
		tbl_q_r <= tbl_r[rd_addr_w];
	end
	reg [3:0] st_r;
	reg op_join_r;
	reg [11:0] op_vid_r;
	reg [IDX_W_C - 1:0] scan_ix_r;
	reg [IDX_W_C - 1:0] chk_ix_r;
	reg chk_v_r;
	reg found_v_r;
	reg [IDX_W_C - 1:0] found_ix_r;
	reg [REFCNT_W_P - 1:0] found_cnt_r;
	reg free_v_r;
	reg [IDX_W_C - 1:0] free_ix_r;
	reg [IDX_W_C - 1:0] ridx_r;
	reg rejoin_pend_r;
	reg [2:0] ev_code_r;
	reg [15:0] ev_vid_r;
	wire [11:0] q_vid_w;
	wire [REFCNT_W_P - 1:0] q_cnt_w;
	wire scan_done_w;
	assign {q_vid_w, q_cnt_w} = tbl_q_r;
	function automatic [IDX_W_C - 1:0] sv2v_cast_FC713;
		input reg [IDX_W_C - 1:0] inp;
		sv2v_cast_FC713 = inp;
	endfunction
	assign scan_done_w = chk_v_r && (chk_ix_r == sv2v_cast_FC713(N_VIDS_P - 1));
	assign rd_addr_w = (st_r == 4'd1 ? scan_ix_r : ridx_r);
	always @(*) begin : tbl_wmux
		if (_sv2v_0)
			;
		tbl_we_w = 1'b0;
		tbl_wix_w = 1'sb0;
		tbl_wdat_w = 1'sb0;
		if (st_r == 4'd2) begin
			if (op_join_r && found_v_r) begin
				tbl_we_w = 1'b1;
				tbl_wix_w = found_ix_r;
				tbl_wdat_w = {op_vid_r, (found_cnt_r == CNT_MAX_C ? CNT_MAX_C : found_cnt_r + CNT_ONE_C)};
			end
			else if (op_join_r && free_v_r) begin
				tbl_we_w = 1'b1;
				tbl_wix_w = free_ix_r;
				tbl_wdat_w = {op_vid_r, CNT_ONE_C};
			end
			else if ((!op_join_r && found_v_r) && (found_cnt_r != CNT_ONE_C)) begin
				tbl_we_w = 1'b1;
				tbl_wix_w = found_ix_r;
				tbl_wdat_w = {op_vid_r, found_cnt_r - CNT_ONE_C};
			end
		end
	end
	function automatic signed [IDX_W_C - 1:0] sv2v_cast_FC713_signed;
		input reg signed [IDX_W_C - 1:0] inp;
		sv2v_cast_FC713_signed = inp;
	endfunction
	always @(posedge clk_i) begin : vlan_sm
		if (!rst_n) begin
			st_r <= 4'd0;
			active_r <= 1'sb0;
			op_join_r <= 1'b0;
			op_vid_r <= 12'd0;
			scan_ix_r <= 1'sb0;
			chk_ix_r <= 1'sb0;
			chk_v_r <= 1'b0;
			found_v_r <= 1'b0;
			found_ix_r <= 1'sb0;
			found_cnt_r <= 1'sb0;
			free_v_r <= 1'b0;
			free_ix_r <= 1'sb0;
			ridx_r <= 1'sb0;
			rejoin_pend_r <= 1'b0;
			ev_code_r <= 3'd0;
			ev_vid_r <= 16'd0;
			user_err_o <= 1'b0;
		end
		else begin
			user_err_o <= 1'b0;
			if (periodic_tick_i || leaveall_tick_i)
				rejoin_pend_r <= 1'b1;
			(* full_case, parallel_case *)
			case (st_r)
				4'd0: begin
					chk_v_r <= 1'b0;
					if (user_valid_i) begin
						op_join_r <= user_join_i;
						op_vid_r <= user_vid_i;
						scan_ix_r <= 1'sb0;
						found_v_r <= 1'b0;
						free_v_r <= 1'b0;
						st_r <= 4'd1;
					end
					else if (rejoin_pend_r) begin
						rejoin_pend_r <= 1'b0;
						if (active_r != {N_VIDS_P {1'sb0}}) begin
							ridx_r <= 1'sb0;
							st_r <= 4'd4;
						end
					end
				end
				4'd1: begin
					chk_ix_r <= scan_ix_r;
					chk_v_r <= 1'b1;
					if (scan_ix_r != sv2v_cast_FC713(N_VIDS_P - 1))
						scan_ix_r <= scan_ix_r + sv2v_cast_FC713_signed(1);
					if (chk_v_r) begin
						if (active_r[chk_ix_r] && (q_vid_w == op_vid_r)) begin
							found_v_r <= 1'b1;
							found_ix_r <= chk_ix_r;
							found_cnt_r <= q_cnt_w;
						end
						if (!active_r[chk_ix_r] && !free_v_r) begin
							free_v_r <= 1'b1;
							free_ix_r <= chk_ix_r;
						end
					end
					if (scan_done_w)
						st_r <= 4'd2;
				end
				4'd2:
					if (op_join_r) begin
						if (found_v_r)
							st_r <= 4'd0;
						else if (free_v_r) begin
							active_r[free_ix_r] <= 1'b1;
							ev_code_r <= EV_NEW_C;
							ev_vid_r <= {4'd0, op_vid_r};
							st_r <= 4'd3;
						end
						else begin
							user_err_o <= 1'b1;
							st_r <= 4'd0;
						end
					end
					else if (found_v_r && (found_cnt_r == CNT_ONE_C)) begin
						active_r[found_ix_r] <= 1'b0;
						ev_code_r <= EV_LV_C;
						ev_vid_r <= {4'd0, op_vid_r};
						st_r <= 4'd3;
					end
					else if (found_v_r)
						st_r <= 4'd0;
					else begin
						user_err_o <= 1'b1;
						st_r <= 4'd0;
					end
				4'd3:
					if (vlan_ev_ready_i)
						st_r <= 4'd0;
				4'd4:
					if (active_r[ridx_r])
						st_r <= 4'd5;
					else if (ridx_r == sv2v_cast_FC713(N_VIDS_P - 1))
						st_r <= 4'd0;
					else
						ridx_r <= ridx_r + sv2v_cast_FC713_signed(1);
				4'd5: st_r <= 4'd6;
				4'd6: begin
					ev_code_r <= EV_JOININ_C;
					ev_vid_r <= {4'd0, q_vid_w};
					st_r <= 4'd7;
				end
				4'd7:
					if (vlan_ev_ready_i) begin
						if (ridx_r == sv2v_cast_FC713(N_VIDS_P - 1))
							st_r <= 4'd0;
						else begin
							ridx_r <= ridx_r + sv2v_cast_FC713_signed(1);
							st_r <= 4'd4;
						end
					end
				default: st_r <= 4'd0;
			endcase
		end
	end
	assign user_ready_o = st_r == 4'd0;
	assign vlan_ev_valid_o = (st_r == 4'd3) || (st_r == 4'd7);
	assign vlan_ev_event_o = ev_code_r;
	assign vlan_ev_vid_o = ev_vid_r;
	assign vid_active_o = active_r;
	initial _sv2v_0 = 0;
endmodule
`default_nettype wire
`default_nettype none
module KL_mrp_strip (
	clk_i,
	rst_n,
	in_valid_i,
	in_data_i,
	in_last_i,
	out_valid_o,
	out_data_o,
	out_last_o,
	out_msrp_o,
	out_ready_i,
	drop_count_o
);
	parameter [31:0] QUEUE_BYTES_P = 2048;
	localparam [31:0] AW_C = $clog2(QUEUE_BYTES_P);
	input wire clk_i;
	input wire rst_n;
	input wire in_valid_i;
	input wire [7:0] in_data_i;
	input wire in_last_i;
	output wire out_valid_o;
	output wire [7:0] out_data_o;
	output wire out_last_o;
	output wire out_msrp_o;
	input wire out_ready_i;
	output reg [15:0] drop_count_o;
	localparam [15:0] ET_MSRP_C = 16'h22ea;
	reg [9:0] ram_r [0:QUEUE_BYTES_P - 1];
	reg [9:0] ram_q_r;
	reg [AW_C:0] wr_cmt_r;
	reg [AW_C:0] wr_tent_r;
	reg [AW_C:0] rd_ptr_r;
	reg [3:0] hdr_idx_r;
	reg [15:0] et_r;
	reg drop_r;
	wire msrp_w;
	wire body_w;
	wire full_w;
	assign msrp_w = et_r == ET_MSRP_C;
	assign body_w = in_valid_i && (hdr_idx_r == 4'd14);
	function automatic [((AW_C + 0) >= 0 ? AW_C + 1 : 1 - (AW_C + 0)) - 1:0] sv2v_cast_1F363;
		input reg [((AW_C + 0) >= 0 ? AW_C + 1 : 1 - (AW_C + 0)) - 1:0] inp;
		sv2v_cast_1F363 = inp;
	endfunction
	assign full_w = (wr_tent_r - rd_ptr_r) == sv2v_cast_1F363(QUEUE_BYTES_P);
	function automatic signed [((AW_C + 0) >= 0 ? AW_C + 1 : 1 - (AW_C + 0)) - 1:0] sv2v_cast_1F363_signed;
		input reg signed [((AW_C + 0) >= 0 ? AW_C + 1 : 1 - (AW_C + 0)) - 1:0] inp;
		sv2v_cast_1F363_signed = inp;
	endfunction
	always @(posedge clk_i) begin : wr_side
		if (!rst_n) begin
			wr_cmt_r <= 1'sb0;
			wr_tent_r <= 1'sb0;
			hdr_idx_r <= 4'd0;
			et_r <= 16'd0;
			drop_r <= 1'b0;
			drop_count_o <= 16'd0;
		end
		else if (in_valid_i) begin
			if (hdr_idx_r == 4'd12)
				et_r[15:8] <= in_data_i;
			if (hdr_idx_r == 4'd13)
				et_r[7:0] <= in_data_i;
			if (hdr_idx_r != 4'd14)
				hdr_idx_r <= hdr_idx_r + 4'd1;
			if (body_w && !drop_r) begin
				if (full_w) begin
					wr_tent_r <= wr_cmt_r;
					drop_r <= 1'b1;
					if (drop_count_o != 16'hffff)
						drop_count_o <= drop_count_o + 16'd1;
				end
				else begin
					ram_r[wr_tent_r[AW_C - 1:0]] <= {msrp_w, in_last_i, in_data_i};
					if (in_last_i) begin
						wr_cmt_r <= wr_tent_r + sv2v_cast_1F363_signed(1);
						wr_tent_r <= wr_tent_r + sv2v_cast_1F363_signed(1);
					end
					else
						wr_tent_r <= wr_tent_r + sv2v_cast_1F363_signed(1);
				end
			end
			if (in_last_i) begin
				hdr_idx_r <= 4'd0;
				drop_r <= 1'b0;
			end
		end
	end
	reg out_vld_r;
	reg [9:0] out_ent_r;
	reg skid_vld_r;
	reg [9:0] skid_ent_r;
	reg fetch_r;
	wire avail_w;
	wire space_w;
	wire pop_w;
	assign avail_w = rd_ptr_r != wr_cmt_r;
	assign pop_w = out_vld_r && out_ready_i;
	assign space_w = (!(out_vld_r && skid_vld_r) && !(skid_vld_r && fetch_r)) && !((out_vld_r && fetch_r) && !out_ready_i);
	always @(posedge clk_i) begin : rd_side
		if (!rst_n) begin
			rd_ptr_r <= 1'sb0;
			out_vld_r <= 1'b0;
			out_ent_r <= 10'd0;
			skid_vld_r <= 1'b0;
			skid_ent_r <= 10'd0;
			fetch_r <= 1'b0;
			ram_q_r <= 10'd0;
		end
		else begin
			if (avail_w && space_w) begin
				ram_q_r <= ram_r[rd_ptr_r[AW_C - 1:0]];
				rd_ptr_r <= rd_ptr_r + sv2v_cast_1F363_signed(1);
				fetch_r <= 1'b1;
			end
			else
				fetch_r <= 1'b0;
			if (pop_w) begin
				if (skid_vld_r) begin
					out_ent_r <= skid_ent_r;
					skid_vld_r <= 1'b0;
					if (fetch_r) begin
						skid_ent_r <= ram_q_r;
						skid_vld_r <= 1'b1;
					end
				end
				else if (fetch_r)
					out_ent_r <= ram_q_r;
				else
					out_vld_r <= 1'b0;
			end
			else if (fetch_r) begin
				if (!out_vld_r) begin
					out_ent_r <= ram_q_r;
					out_vld_r <= 1'b1;
				end
				else begin
					skid_ent_r <= ram_q_r;
					skid_vld_r <= 1'b1;
				end
			end
		end
	end
	assign out_valid_o = out_vld_r;
	assign out_msrp_o = out_ent_r[9];
	assign out_last_o = out_ent_r[8];
	assign out_data_o = out_ent_r[7:0];
endmodule
`default_nettype wire
`default_nettype none
module protocol_processor_top (
	clk_i,
	rst_n,
	entity_id_i,
	entity_model_id_i,
	own_mac_i,
	talker_sources_i,
	talker_caps_i,
	listener_sinks_i,
	listener_caps_i,
	current_cfg_i,
	identify_index_i,
	entity_enable_i,
	link_up_i,
	gm_change_i,
	gm_id_i,
	gptp_domain_i,
	p2p_i,
	cfg_rank_i,
	cfg_acc_lat_ns_i,
	port_rate_bps_i,
	cfg_tspec_max_frame_i,
	cfg_src_en_i,
	cfg_src_iface_i,
	cfg_stream_id_i,
	rx_valid_i,
	rx_data_i,
	rx_last_i,
	tx_valid_o,
	tx_sof_o,
	tx_data_o,
	tx_eof_o,
	tx_ready_i,
	desc_mem_req_valid_o,
	desc_mem_req_ready_i,
	desc_mem_req_addr_o,
	desc_mem_req_beats_o,
	desc_mem_rsp_valid_i,
	desc_mem_rsp_ready_o,
	desc_mem_rsp_data_i,
	desc_mem_rsp_last_i,
	desc_mem_rsp_err_i,
	resp_mem_req_valid_o,
	resp_mem_req_ready_i,
	resp_mem_req_addr_o,
	resp_mem_req_beats_o,
	resp_mem_rsp_valid_i,
	resp_mem_rsp_ready_o,
	resp_mem_rsp_data_i,
	resp_mem_rsp_last_i,
	resp_mem_rsp_err_i,
	resp_mem_wr_valid_o,
	resp_mem_wr_ready_i,
	resp_mem_wr_addr_o,
	resp_mem_wr_data_o,
	resp_mem_wr_strb_o,
	resp_mem_wr_done_i,
	resp_mem_wr_err_i,
	aecp_txn_valid_o,
	aecp_txn_o,
	aecp_txn_ready_i,
	aecp_rxs_rd_slot_i,
	aecp_rxs_rd_addr_i,
	aecp_rxs_rd_en_i,
	aecp_rxs_rd_data_o,
	aecp_rxs_slot_len_o,
	aecp_rxs_free_i,
	aecp_rxs_free_slot_i,
	ctr_req_o,
	ctr_desc_type_o,
	ctr_desc_index_o,
	ctr_word_o,
	ctr_data_i,
	ctr_wait_i,
	ctr_change_i,
	ctr_change_desc_type_i,
	ctr_change_desc_index_i,
	amap_req_o,
	amap_desc_type_o,
	amap_desc_index_o,
	amap_map_index_o,
	amap_sel_o,
	amap_rec_o,
	amap_data_i,
	amap_wait_i,
	amap_edit_req_o,
	amap_edit_phase_o,
	amap_edit_remove_o,
	amap_edit_desc_type_o,
	amap_edit_desc_index_o,
	amap_edit_count_o,
	amap_edit_rec_o,
	amap_edit_record_o,
	amap_edit_value_o,
	amap_edit_data_i,
	amap_edit_wait_i,
	gsi_req_o,
	gsi_kind_o,
	gsi_desc_type_o,
	gsi_desc_index_o,
	gsi_sel_o,
	gsi_ord_o,
	gsi_prop_fmt_o,
	gsi_data_i,
	gsi_wait_i,
	gsi_avb_chg_i,
	gsi_asp_chg_i,
	restore_go_i,
	restore_busy_o,
	restore_done_o,
	restore_fail_o,
	restore_blank_o,
	nvm_alarm_o,
	nvm_unflushed_o,
	nvm_dev_req_o,
	nvm_dev_gnt_i,
	nvm_dev_op_o,
	nvm_dev_region_o,
	nvm_dev_offset_o,
	nvm_dev_len_o,
	nvm_dev_wvalid_o,
	nvm_dev_wready_i,
	nvm_dev_wdata_o,
	nvm_dev_rvalid_i,
	nvm_dev_rdata_i,
	nvm_dev_rready_o,
	nvm_dev_busy_i,
	nvm_dev_done_i,
	nvm_dev_err_i,
	host_req_valid_i,
	host_we_i,
	host_addr_i,
	host_wdata_i,
	host_rdata_o,
	host_rvalid_o,
	host_err_o,
	svc_valid_i,
	svc_ready_o,
	svc_op_i,
	svc_index_i,
	svc_stream_id_i,
	svc_da_i,
	svc_vid_i,
	svc_max_frame_i,
	svc_lstn_state_i,
	svc_rsp_valid_o,
	svc_rsp_status_o,
	svc_rsp_data_o,
	srp_class_a_prio_o,
	srp_class_a_vid_o,
	srp_domain_adopted_o,
	srp_domain_change_o,
	srp_tk_decl_state_o,
	srp_lstn_reg_state_o,
	srp_active_o,
	srp_sr_admitted_o,
	srp_granted_slope_bps_o,
	srp_src_fail_code_o,
	srp_src_fail_bridge_o,
	srp_sum_slope_bps_o,
	srp_over_limit_o,
	srp_tk_reg_state_o,
	srp_lstn_decl_state_o,
	srp_acc_latency_o,
	srp_snk_fail_code_o,
	acmp_declaring_o,
	acmp_bound_o,
	acmp_bound_eid_o,
	acmp_bound_sid_o,
	acmp_bound_dmac_o,
	acmp_bound_vlan_o,
	adp_next_avail_index_o,
	maap_req_valid_o,
	maap_req_ready_i,
	maap_req_release_o,
	maap_req_src_o,
	maap_rsp_valid_i,
	maap_rsp_ok_i,
	maap_rsp_da_i,
	maap_conflict_valid_i,
	maap_conflict_src_i,
	maap_conflict_ack_o,
	cfg_maap_internal_i,
	cfg_maap_count_i,
	cfg_maap_seed_offset_i,
	cfg_maap_seed_valid_i,
	maap_addr_o,
	maap_addr_valid_o,
	maap_state_o,
	maap_conflicts_o,
	maap_defends_o,
	aecp_cur_config_o,
	aecp_identify_o,
	aecp_clk_src_index_o,
	aecp_strm_started_o,
	aecp_pt_offset_o,
	aecp_pt_offset_v_o,
	aecp_fmt_in_o,
	aecp_fmt_in_v_o,
	aecp_fmt_out_o,
	aecp_fmt_out_v_o,
	aecp_dyn_dirty_o,
	aecp_nvm_stb_o,
	aecp_nvm_mark_o,
	aecp_lock_held_o,
	dbg_now_ms_o
);
	reg _sv2v_0;
	parameter [31:0] N_STREAM_IN_P = 8;
	parameter [31:0] N_STREAM_OUT_P = 8;
	parameter [31:0] N_AUDIO_UNIT_P = 1;
	parameter [31:0] N_CLK_DOMAIN_P = 1;
	parameter [31:0] N_CONTROL_P = 1;
	parameter [31:0] RX_SLOTS_P = 4;
	parameter [31:0] RX_SLOT_BYTES_P = 576;
	parameter [31:0] TX_STD_SLOTS_P = 4;
	parameter [31:0] TX_OVERSIZE_BYTES_P = 1600;
	parameter [31:0] CLK_HZ_P = 100000000;
	parameter [31:0] TIM_DIV_US_P = CLK_HZ_P / 32'd1000000;
	parameter [31:0] TIM_DIV_MS_P = 1000;
	parameter TROM_HEX_P = "ltn_rom.hex";
	parameter UCODE_HEX_P = "ucode.hex";
	parameter [31:0] DESC_BASE_P = 32'h20000000;
	parameter [31:0] DESC_LINE_BYTES_P = 576;
	parameter [31:0] DESC_IDX_ENTRIES_P = 32;
	parameter [31:0] DESC_NAME_ENTRIES_P = 32;
	parameter [31:0] DESC_MEM_TMO_CYC_P = 4096;
	parameter [31:0] REG_TL_TIMEOUT_MS_P = 300000;
	parameter [31:0] LOCK_TIMEOUT_MS_P = 60000;
	parameter [31:0] RESP_BASE_P = 32'h20100000;
	localparam [31:0] pp_pkg_PP_CA_POOL_C = 4;
	localparam [31:0] pp_pkg_PP_N_CTRL_C = 16;
	localparam [31:0] pp_pkg_PP_N_IF_C = 1;
	localparam [31:0] pp_pkg_PP_MAAP_SLOTS_C = 2;
	localparam [31:0] pp_pkg_PP_SINGLETON_SLOTS_C = 5;
	localparam [31:0] pp_pkg_PP_SRP_CAD_SLOTS_C = 7;
	function automatic [415:0] pp_pkg_pp_timer_map;
		input reg [31:0] n_if;
		input reg [31:0] si;
		input reg [31:0] so;
		input reg [31:0] n_ctrl;
		input reg [31:0] ca_pool;
		reg [415:0] m;
		begin
			m[415-:32] = 32'd0;
			m[383-:32] = m[415-:32] + n_if;
			m[351-:32] = m[383-:32] + si;
			m[319-:32] = m[351-:32] + si;
			m[287-:32] = m[319-:32] + so;
			m[255-:32] = m[287-:32] + ((32'd2 * n_ctrl) * n_if);
			m[223-:32] = m[255-:32] + ca_pool;
			m[191-:32] = m[223-:32] + pp_pkg_PP_SINGLETON_SLOTS_C;
			m[159-:32] = m[191-:32] + pp_pkg_PP_MAAP_SLOTS_C;
			m[127-:32] = m[159-:32];
			m[95-:32] = m[127-:32] + pp_pkg_PP_SRP_CAD_SLOTS_C;
			m[63-:32] = m[95-:32] + so;
			m[31-:32] = m[127-:32] + (((pp_pkg_PP_SRP_CAD_SLOTS_C + si) + so) * n_if);
			pp_pkg_pp_timer_map = m;
		end
	endfunction
	localparam [415:0] TMR_MAP_C = pp_pkg_pp_timer_map(pp_pkg_PP_N_IF_C, N_STREAM_IN_P, N_STREAM_OUT_P, pp_pkg_PP_N_CTRL_C, pp_pkg_PP_CA_POOL_C);
	localparam [31:0] TMR_SLOTS_C = TMR_MAP_C[31-:32];
	localparam [31:0] TMR_AW_C = $clog2(TMR_SLOTS_C);
	localparam [31:0] RXS_W_C = (RX_SLOTS_P > 1 ? $clog2(RX_SLOTS_P) : 1);
	localparam [31:0] SINK_IDX_W_C = (N_STREAM_IN_P > 1 ? $clog2(N_STREAM_IN_P) : 1);
	localparam [31:0] SRC_IDX_W_C = (N_STREAM_OUT_P > 1 ? $clog2(N_STREAM_OUT_P) : 1);
	localparam [31:0] RXA_W_C = $clog2(RX_SLOT_BYTES_P);
	localparam [31:0] RXL_W_C = $clog2(RX_SLOT_BYTES_P + 1);
	localparam [31:0] TXS_W_C = $clog2(TX_STD_SLOTS_P + 1);
	localparam [31:0] TXA_W_C = $clog2(TX_OVERSIZE_BYTES_P + 1);
	input wire clk_i;
	input wire rst_n;
	input wire [63:0] entity_id_i;
	input wire [63:0] entity_model_id_i;
	input wire [47:0] own_mac_i;
	input wire [15:0] talker_sources_i;
	input wire [15:0] talker_caps_i;
	input wire [15:0] listener_sinks_i;
	input wire [15:0] listener_caps_i;
	input wire [15:0] current_cfg_i;
	input wire [15:0] identify_index_i;
	input wire entity_enable_i;
	input wire link_up_i;
	input wire gm_change_i;
	input wire [63:0] gm_id_i;
	input wire [7:0] gptp_domain_i;
	input wire p2p_i;
	input wire cfg_rank_i;
	input wire [31:0] cfg_acc_lat_ns_i;
	input wire [31:0] port_rate_bps_i;
	input wire [15:0] cfg_tspec_max_frame_i;
	input wire [N_STREAM_OUT_P - 1:0] cfg_src_en_i;
	input wire [(N_STREAM_OUT_P * 2) - 1:0] cfg_src_iface_i;
	input wire [(N_STREAM_OUT_P * 64) - 1:0] cfg_stream_id_i;
	input wire rx_valid_i;
	input wire [7:0] rx_data_i;
	input wire rx_last_i;
	output reg tx_valid_o;
	output reg tx_sof_o;
	output reg [7:0] tx_data_o;
	output reg tx_eof_o;
	input wire tx_ready_i;
	output wire desc_mem_req_valid_o;
	input wire desc_mem_req_ready_i;
	output wire [31:0] desc_mem_req_addr_o;
	output wire [8:0] desc_mem_req_beats_o;
	input wire desc_mem_rsp_valid_i;
	output wire desc_mem_rsp_ready_o;
	input wire [63:0] desc_mem_rsp_data_i;
	input wire desc_mem_rsp_last_i;
	input wire desc_mem_rsp_err_i;
	output wire resp_mem_req_valid_o;
	input wire resp_mem_req_ready_i;
	output wire [31:0] resp_mem_req_addr_o;
	output wire [8:0] resp_mem_req_beats_o;
	input wire resp_mem_rsp_valid_i;
	output wire resp_mem_rsp_ready_o;
	input wire [63:0] resp_mem_rsp_data_i;
	input wire resp_mem_rsp_last_i;
	input wire resp_mem_rsp_err_i;
	output wire resp_mem_wr_valid_o;
	input wire resp_mem_wr_ready_i;
	output wire [31:0] resp_mem_wr_addr_o;
	output wire [63:0] resp_mem_wr_data_o;
	output wire [7:0] resp_mem_wr_strb_o;
	input wire resp_mem_wr_done_i;
	input wire resp_mem_wr_err_i;
	output wire aecp_txn_valid_o;
	localparam [31:0] pp_pkg_PP_TXN_W_C = 393;
	output wire [392:0] aecp_txn_o;
	input wire aecp_txn_ready_i;
	input wire [RXS_W_C - 1:0] aecp_rxs_rd_slot_i;
	input wire [RXA_W_C - 1:0] aecp_rxs_rd_addr_i;
	input wire aecp_rxs_rd_en_i;
	output wire [7:0] aecp_rxs_rd_data_o;
	output wire [RXL_W_C - 1:0] aecp_rxs_slot_len_o;
	input wire aecp_rxs_free_i;
	input wire [RXS_W_C - 1:0] aecp_rxs_free_slot_i;
	output wire ctr_req_o;
	output wire [15:0] ctr_desc_type_o;
	output wire [15:0] ctr_desc_index_o;
	output wire [5:0] ctr_word_o;
	input wire [31:0] ctr_data_i;
	input wire ctr_wait_i;
	input wire ctr_change_i;
	input wire [15:0] ctr_change_desc_type_i;
	input wire [15:0] ctr_change_desc_index_i;
	output wire amap_req_o;
	output wire [15:0] amap_desc_type_o;
	output wire [15:0] amap_desc_index_o;
	output wire [15:0] amap_map_index_o;
	output wire [1:0] amap_sel_o;
	output wire [7:0] amap_rec_o;
	input wire [63:0] amap_data_i;
	input wire amap_wait_i;
	output wire amap_edit_req_o;
	output wire [2:0] amap_edit_phase_o;
	output wire amap_edit_remove_o;
	output wire [15:0] amap_edit_desc_type_o;
	output wire [15:0] amap_edit_desc_index_o;
	output wire [15:0] amap_edit_count_o;
	output wire [7:0] amap_edit_rec_o;
	output wire [63:0] amap_edit_record_o;
	output wire [63:0] amap_edit_value_o;
	input wire [63:0] amap_edit_data_i;
	input wire amap_edit_wait_i;
	output wire gsi_req_o;
	output wire [1:0] gsi_kind_o;
	output wire [15:0] gsi_desc_type_o;
	output wire [15:0] gsi_desc_index_o;
	output wire [3:0] gsi_sel_o;
	output wire [7:0] gsi_ord_o;
	output wire [63:0] gsi_prop_fmt_o;
	input wire [63:0] gsi_data_i;
	input wire gsi_wait_i;
	input wire gsi_avb_chg_i;
	input wire gsi_asp_chg_i;
	input wire restore_go_i;
	output wire restore_busy_o;
	output wire restore_done_o;
	output wire restore_fail_o;
	output wire restore_blank_o;
	output wire nvm_alarm_o;
	output wire [N_STREAM_IN_P - 1:0] nvm_unflushed_o;
	output wire nvm_dev_req_o;
	input wire nvm_dev_gnt_i;
	output wire [1:0] nvm_dev_op_o;
	output wire [7:0] nvm_dev_region_o;
	output wire [15:0] nvm_dev_offset_o;
	output wire [15:0] nvm_dev_len_o;
	output wire nvm_dev_wvalid_o;
	input wire nvm_dev_wready_i;
	output wire [7:0] nvm_dev_wdata_o;
	input wire nvm_dev_rvalid_i;
	input wire [7:0] nvm_dev_rdata_i;
	output wire nvm_dev_rready_o;
	input wire nvm_dev_busy_i;
	input wire nvm_dev_done_i;
	input wire nvm_dev_err_i;
	input wire host_req_valid_i;
	input wire host_we_i;
	input wire [19:0] host_addr_i;
	input wire [31:0] host_wdata_i;
	output wire [31:0] host_rdata_o;
	output wire host_rvalid_o;
	output wire host_err_o;
	input wire svc_valid_i;
	output wire svc_ready_o;
	input wire [2:0] svc_op_i;
	input wire [7:0] svc_index_i;
	input wire [63:0] svc_stream_id_i;
	input wire [47:0] svc_da_i;
	input wire [11:0] svc_vid_i;
	input wire [15:0] svc_max_frame_i;
	input wire [1:0] svc_lstn_state_i;
	output reg svc_rsp_valid_o;
	output reg [1:0] svc_rsp_status_o;
	output reg [31:0] svc_rsp_data_o;
	output wire [2:0] srp_class_a_prio_o;
	output wire [11:0] srp_class_a_vid_o;
	output wire srp_domain_adopted_o;
	output wire srp_domain_change_o;
	output wire [(N_STREAM_OUT_P * 2) - 1:0] srp_tk_decl_state_o;
	output wire [(N_STREAM_OUT_P * 2) - 1:0] srp_lstn_reg_state_o;
	output wire [N_STREAM_OUT_P - 1:0] srp_active_o;
	output wire [N_STREAM_OUT_P - 1:0] srp_sr_admitted_o;
	output wire [(N_STREAM_OUT_P * 32) - 1:0] srp_granted_slope_bps_o;
	output wire [(N_STREAM_OUT_P * 8) - 1:0] srp_src_fail_code_o;
	output wire [(N_STREAM_OUT_P * 64) - 1:0] srp_src_fail_bridge_o;
	output wire [31:0] srp_sum_slope_bps_o;
	output wire srp_over_limit_o;
	output wire [(N_STREAM_IN_P * 2) - 1:0] srp_tk_reg_state_o;
	output wire [(N_STREAM_IN_P * 2) - 1:0] srp_lstn_decl_state_o;
	output wire [(N_STREAM_IN_P * 32) - 1:0] srp_acc_latency_o;
	output wire [(N_STREAM_IN_P * 8) - 1:0] srp_snk_fail_code_o;
	output wire [N_STREAM_OUT_P - 1:0] acmp_declaring_o;
	output wire [N_STREAM_IN_P - 1:0] acmp_bound_o;
	output wire [(N_STREAM_IN_P * 64) - 1:0] acmp_bound_eid_o;
	output wire [(N_STREAM_IN_P * 64) - 1:0] acmp_bound_sid_o;
	output wire [(N_STREAM_IN_P * 48) - 1:0] acmp_bound_dmac_o;
	output wire [(N_STREAM_IN_P * 12) - 1:0] acmp_bound_vlan_o;
	output wire [31:0] adp_next_avail_index_o;
	output wire maap_req_valid_o;
	input wire maap_req_ready_i;
	output wire maap_req_release_o;
	output wire [SRC_IDX_W_C - 1:0] maap_req_src_o;
	input wire maap_rsp_valid_i;
	input wire maap_rsp_ok_i;
	input wire [47:0] maap_rsp_da_i;
	input wire maap_conflict_valid_i;
	input wire [SRC_IDX_W_C - 1:0] maap_conflict_src_i;
	output wire maap_conflict_ack_o;
	input wire cfg_maap_internal_i;
	input wire [7:0] cfg_maap_count_i;
	input wire [15:0] cfg_maap_seed_offset_i;
	input wire cfg_maap_seed_valid_i;
	output wire [47:0] maap_addr_o;
	output wire maap_addr_valid_o;
	output wire [1:0] maap_state_o;
	output wire [7:0] maap_conflicts_o;
	output wire [7:0] maap_defends_o;
	output wire [15:0] aecp_cur_config_o;
	output wire [7:0] aecp_identify_o;
	output wire [15:0] aecp_clk_src_index_o;
	output wire [N_STREAM_IN_P - 1:0] aecp_strm_started_o;
	output wire [(N_STREAM_OUT_P * 32) - 1:0] aecp_pt_offset_o;
	output wire [N_STREAM_OUT_P - 1:0] aecp_pt_offset_v_o;
	output wire [(N_STREAM_IN_P * 64) - 1:0] aecp_fmt_in_o;
	output wire [N_STREAM_IN_P - 1:0] aecp_fmt_in_v_o;
	output wire [(N_STREAM_OUT_P * 64) - 1:0] aecp_fmt_out_o;
	output wire [N_STREAM_OUT_P - 1:0] aecp_fmt_out_v_o;
	output wire aecp_dyn_dirty_o;
	output wire aecp_nvm_stb_o;
	output wire [7:0] aecp_nvm_mark_o;
	output wire aecp_lock_held_o;
	output wire [31:0] dbg_now_ms_o;
	localparam [31:0] TMR_ADP_ADV_BASE_C = TMR_MAP_C[415-:32];
	localparam [31:0] TMR_ADP_NOADP_BASE_C = TMR_MAP_C[383-:32];
	localparam [31:0] TMR_LSTN_BASE_C = TMR_MAP_C[351-:32];
	localparam [31:0] TMR_TKR_BASE_C = TMR_MAP_C[319-:32];
	localparam [31:0] TMR_MAAP_BASE_C = TMR_MAP_C[191-:32];
	localparam [31:0] TMR_SRP_CAD_BASE_C = TMR_MAP_C[127-:32];
	localparam [31:0] TMR_SRP_TK_BASE_C = TMR_MAP_C[95-:32];
	localparam [31:0] TMR_SRP_LS_BASE_C = TMR_MAP_C[63-:32];
	localparam [7:0] pp_pkg_PP_OWN_SRP_CAD_C = 8'h80;
	localparam [7:0] SRP_CAD_OWNER_C = pp_pkg_PP_OWN_SRP_CAD_C;
	localparam [7:0] pp_pkg_PP_OWN_SRP_TK_C = 8'h40;
	localparam [7:0] SRP_TK_OWNER_C = pp_pkg_PP_OWN_SRP_TK_C;
	localparam [7:0] pp_pkg_PP_OWN_SRP_LS_C = 8'h60;
	localparam [7:0] SRP_LS_OWNER_C = pp_pkg_PP_OWN_SRP_LS_C;
	localparam [31:0] OWN_ADP_END_C = TMR_MAP_C[351-:32];
	localparam [7:0] pp_pkg_PP_OWN_LSTN_C = 8'h20;
	function automatic [31:0] sv2v_cast_32;
		input reg [31:0] inp;
		sv2v_cast_32 = inp;
	endfunction
	localparam [31:0] OWN_LSTN_END_C = sv2v_cast_32(pp_pkg_PP_OWN_LSTN_C) + N_STREAM_IN_P;
	localparam [31:0] OWN_SRPTK_END_C = sv2v_cast_32(pp_pkg_PP_OWN_SRP_TK_C) + N_STREAM_OUT_P;
	localparam [7:0] pp_pkg_PP_OWN_TKR_C = 8'h50;
	localparam [31:0] OWN_TKR_END_C = sv2v_cast_32(pp_pkg_PP_OWN_TKR_C) + N_STREAM_OUT_P;
	localparam [31:0] OWN_SRPLS_END_C = sv2v_cast_32(pp_pkg_PP_OWN_SRP_LS_C) + N_STREAM_IN_P;
	localparam [31:0] OWN_SRPCAD_END_C = sv2v_cast_32(pp_pkg_PP_OWN_SRP_CAD_C) + pp_pkg_PP_SRP_CAD_SLOTS_C;
	localparam [7:0] pp_pkg_PP_OWN_MAAP_C = 8'h90;
	localparam [31:0] OWN_MAAP_END_C = sv2v_cast_32(pp_pkg_PP_OWN_MAAP_C) + pp_pkg_PP_MAAP_SLOTS_C;
	generate
		if (TMR_SLOTS_C > (32'd1 << TMR_AW_C)) begin : gen_g_tmr_aw
			initial $display("Error [elaboration] $VALIDATION_STORAGE/reviews/r247-520-r1/protocol-processor/hdl/top/protocol_processor_top.sv:692:5 - protocol_processor_top.gen_g_tmr_aw\n msg: ", "F08.4: TMR_AW_C=%0d cannot index P-TIMER-SLOTS=%0d", TMR_AW_C, TMR_SLOTS_C);
		end
		if ((TMR_MAP_C[63-:32] + N_STREAM_IN_P) > TMR_SLOTS_C) begin : gen_g_tmr_fit
			initial $display("Error [elaboration] $VALIDATION_STORAGE/reviews/r247-520-r1/protocol-processor/hdl/top/protocol_processor_top.sv:696:5 - protocol_processor_top.gen_g_tmr_fit\n msg: ", "F08.4: slot map ends at %0d but P-TIMER-SLOTS=%0d", TMR_MAP_C[63-:32] + N_STREAM_IN_P, TMR_SLOTS_C);
		end
		if (((((((((TMR_ADP_NOADP_BASE_C < (TMR_ADP_ADV_BASE_C + pp_pkg_PP_N_IF_C)) || (TMR_LSTN_BASE_C < (TMR_ADP_NOADP_BASE_C + N_STREAM_IN_P))) || (TMR_TKR_BASE_C < (TMR_LSTN_BASE_C + N_STREAM_IN_P))) || (TMR_MAP_C[287-:32] < (TMR_TKR_BASE_C + N_STREAM_OUT_P))) || (TMR_MAAP_BASE_C < (TMR_MAP_C[223-:32] + pp_pkg_PP_SINGLETON_SLOTS_C))) || (TMR_MAP_C[159-:32] < (TMR_MAAP_BASE_C + pp_pkg_PP_MAAP_SLOTS_C))) || (TMR_SRP_CAD_BASE_C < TMR_MAP_C[159-:32])) || (TMR_SRP_TK_BASE_C < (TMR_SRP_CAD_BASE_C + pp_pkg_PP_SRP_CAD_SLOTS_C))) || (TMR_SRP_LS_BASE_C < (TMR_SRP_TK_BASE_C + N_STREAM_OUT_P))) begin : gen_g_tmr_overlap
			initial $display("Error [elaboration] $VALIDATION_STORAGE/reviews/r247-520-r1/protocol-processor/hdl/top/protocol_processor_top.sv:709:5 - protocol_processor_top.gen_g_tmr_overlap\n msg: ", "F08.4: timer-slot groups OVERLAP at SI=%0d SO=%0d", N_STREAM_IN_P, N_STREAM_OUT_P);
		end
	endgenerate
	localparam [7:0] pp_pkg_PP_OWN_LOCK_C = 8'hb0;
	localparam [7:0] pp_pkg_PP_OWN_NTFY_C = 8'ha0;
	generate
		if ((((((((((OWN_ADP_END_C > sv2v_cast_32(pp_pkg_PP_OWN_LSTN_C)) || (OWN_LSTN_END_C > sv2v_cast_32(pp_pkg_PP_OWN_SRP_TK_C))) || (OWN_SRPTK_END_C > sv2v_cast_32(pp_pkg_PP_OWN_TKR_C))) || (OWN_TKR_END_C > sv2v_cast_32(pp_pkg_PP_OWN_SRP_LS_C))) || (OWN_SRPLS_END_C > sv2v_cast_32(pp_pkg_PP_OWN_SRP_CAD_C))) || (OWN_SRPCAD_END_C > sv2v_cast_32(pp_pkg_PP_OWN_MAAP_C))) || (OWN_MAAP_END_C > sv2v_cast_32(pp_pkg_PP_OWN_NTFY_C))) || ((sv2v_cast_32(pp_pkg_PP_OWN_NTFY_C) + pp_pkg_PP_N_CTRL_C) > sv2v_cast_32(pp_pkg_PP_OWN_LOCK_C))) || ((sv2v_cast_32(pp_pkg_PP_OWN_LOCK_C) + 32'd1) > 32'h000000c0)) || (OWN_MAAP_END_C > 32'd256)) begin : gen_g_owner_overlap
			initial $display("Error [elaboration] $VALIDATION_STORAGE/reviews/r247-520-r1/protocol-processor/hdl/top/protocol_processor_top.sv:722:5 - protocol_processor_top.gen_g_owner_overlap\n msg: ", "F08.4: owner tags OVERLAP at SI=%0d SO=%0d (8-bit expiry bus)", N_STREAM_IN_P, N_STREAM_OUT_P);
		end
	endgenerate
	localparam [15:0] BUDGET_ADP_MS_C = 16'd4000;
	localparam [15:0] BUDGET_ACMP_MS_C = 16'd50;
	localparam [15:0] BUDGET_AECP_MS_C = 16'd100;
	localparam [31:0] LANE_AECP_SOL_C = 0;
	localparam [31:0] LANE_AECP_UNS_C = 1;
	localparam [31:0] LANE_ACMP_C = 2;
	localparam [31:0] LANE_ADP_C = 3;
	localparam [31:0] LANE_SRP_C = 4;
	localparam [31:0] LANE_TKRSP_C = 5;
	localparam [31:0] LANE_MAAP_C = 6;
	localparam [31:0] LANE_ORIG_C = 7;
	localparam [31:0] LANE_N_C = 8;
	wire tick_ms_w;
	wire [31:0] now_ms_w;
	reg tmr_arm_valid_w;
	reg tmr_arm_cancel_w;
	reg [TMR_AW_C - 1:0] tmr_arm_slot_w;
	localparam [31:0] pp_pkg_PP_TIMER_OWNER_W_C = 8;
	reg [7:0] tmr_arm_owner_w;
	reg [31:0] tmr_arm_deadline_w;
	wire exp_valid_w;
	wire [TMR_AW_C - 1:0] exp_slot_w;
	wire [7:0] exp_owner_w;
	KL_pp_timer_service #(
		.CLK_HZ_P(CLK_HZ_P),
		.SLOTS_P(TMR_SLOTS_C),
		.DIV_US_P(TIM_DIV_US_P),
		.DIV_MS_P(TIM_DIV_MS_P)
	) u_timer(
		.clk_i(clk_i),
		.rst_n(rst_n),
		.tick_ms_o(tick_ms_w),
		.now_ms_o(now_ms_w),
		.arm_valid_i(tmr_arm_valid_w),
		.arm_cancel_i(tmr_arm_cancel_w),
		.arm_slot_i(tmr_arm_slot_w),
		.arm_owner_i(tmr_arm_owner_w),
		.arm_deadline_ms_i(tmr_arm_deadline_w),
		.exp_valid_o(exp_valid_w),
		.exp_slot_o(exp_slot_w),
		.exp_owner_o(exp_owner_w)
	);
	assign dbg_now_ms_o = now_ms_w;
	wire [2:0] srp_class_a_prio_w;
	assign srp_class_a_prio_o = srp_class_a_prio_w;
	wire [11:0] srp_class_a_vid_w;
	assign srp_class_a_vid_o = srp_class_a_vid_w;
	wire srp_domain_adopted_w;
	assign srp_domain_adopted_o = srp_domain_adopted_w;
	wire srp_evt_domain_change_w;
	assign srp_domain_change_o = srp_evt_domain_change_w;
	wire [(N_STREAM_OUT_P * 2) - 1:0] srp_tk_decl_state_w;
	assign srp_tk_decl_state_o = srp_tk_decl_state_w;
	wire [(N_STREAM_OUT_P * 2) - 1:0] srp_lstn_reg_state_w;
	assign srp_lstn_reg_state_o = srp_lstn_reg_state_w;
	wire [N_STREAM_OUT_P - 1:0] srp_active_w;
	assign srp_active_o = srp_active_w;
	wire [N_STREAM_OUT_P - 1:0] srp_sr_admitted_w;
	assign srp_sr_admitted_o = srp_sr_admitted_w;
	wire [(N_STREAM_OUT_P * 32) - 1:0] srp_granted_slope_w;
	assign srp_granted_slope_bps_o = srp_granted_slope_w;
	wire [(N_STREAM_OUT_P * 8) - 1:0] srp_src_fail_code_nc_w;
	assign srp_src_fail_code_o = srp_src_fail_code_nc_w;
	wire [(N_STREAM_OUT_P * 64) - 1:0] srp_src_fail_bridge_nc_w;
	assign srp_src_fail_bridge_o = srp_src_fail_bridge_nc_w;
	wire [31:0] srp_sum_slope_w;
	assign srp_sum_slope_bps_o = srp_sum_slope_w;
	wire srp_over_limit_w;
	assign srp_over_limit_o = srp_over_limit_w;
	wire [(N_STREAM_IN_P * 2) - 1:0] srp_tk_reg_state_w;
	assign srp_tk_reg_state_o = srp_tk_reg_state_w;
	wire [(N_STREAM_IN_P * 2) - 1:0] srp_lstn_decl_state_w;
	assign srp_lstn_decl_state_o = srp_lstn_decl_state_w;
	wire [(N_STREAM_IN_P * 32) - 1:0] srp_acc_latency_w;
	assign srp_acc_latency_o = srp_acc_latency_w;
	wire [(N_STREAM_IN_P * 8) - 1:0] srp_snk_fail_code_w;
	assign srp_snk_fail_code_o = srp_snk_fail_code_w;
	wire [N_STREAM_OUT_P - 1:0] tkr_declaring_w;
	assign acmp_declaring_o = tkr_declaring_w;
	reg [N_STREAM_IN_P - 1:0] bound_hold_r;
	reg [N_STREAM_IN_P - 1:0] bound_r;
	wire lstn_dbg_busy_nc_w;
	always @(posedge clk_i) begin : bound_debounce
		if (!rst_n)
			bound_hold_r <= 1'sb0;
		else if (!lstn_dbg_busy_nc_w)
			bound_hold_r <= bound_r;
		else
			bound_hold_r <= bound_hold_r | bound_r;
	end
	assign acmp_bound_o = bound_hold_r;
	reg [(N_STREAM_IN_P * 64) - 1:0] bound_eid_r;
	assign acmp_bound_eid_o = bound_eid_r;
	reg [(N_STREAM_IN_P * 64) - 1:0] bound_sid_r;
	assign acmp_bound_sid_o = bound_sid_r;
	reg [(N_STREAM_IN_P * 48) - 1:0] bound_dmac_r;
	assign acmp_bound_dmac_o = bound_dmac_r;
	reg [(N_STREAM_IN_P * 12) - 1:0] bound_vlan_r;
	assign acmp_bound_vlan_o = bound_vlan_r;
	wire [31:0] adp_dbg_aidx_nc_w;
	assign adp_next_avail_index_o = adp_dbg_aidx_nc_w;
	reg prng_req_w;
	reg [2:0] prng_kind_w;
	wire prng_busy_w;
	wire prng_valid_w;
	wire [15:0] prng_ms_w;
	wire [63:0] prng_lfsr_nc_w;
	wire prng_seeded_w;
	KL_pp_prng u_prng(
		.clk_i(clk_i),
		.rst_n(rst_n),
		.entity_id_i(entity_id_i),
		.link_up_i(link_up_i),
		.draw_req_i(prng_req_w),
		.draw_kind_i(prng_kind_w),
		.draw_busy_o(prng_busy_w),
		.draw_valid_o(prng_valid_w),
		.draw_ms_o(prng_ms_w),
		.dbg_lfsr_o(prng_lfsr_nc_w),
		.dbg_seeded_o(prng_seeded_w)
	);
	reg sb_adm_req_w;
	wire sb_gnt_w;
	reg [3:0] sb_adm_class_w;
	reg [15:0] sb_adm_key_w;
	wire [2:0] sb_id_w;
	wire sb_rel_valid_w;
	wire [2:0] sb_rel_id_w;
	wire sb_kill_ack_nc_w;
	wire [7:0] sb_holds_w;
	wire sb_full_w;
	wire sb_barrier_w;
	wire acmp_sb_grant_w;
	wire aecp_sb_grant_w;
	reg acmp_sb_active_r;
	reg aecp_sb_active_r;
	reg acmp_sb_done_pending_r;
	reg aecp_sb_done_pending_r;
	reg sb_prefer_aecp_r;
	reg [2:0] acmp_sb_id_r;
	reg [2:0] aecp_sb_id_r;
	reg [RXS_W_C - 1:0] acmp_sb_slot_r;
	reg [RXS_W_C - 1:0] aecp_sb_slot_r;
	wire aecp_eng_ready_w;
	KL_pp_scoreboard #(.MAX_HOLDS_P(8)) u_scoreboard(
		.clk_i(clk_i),
		.rst_n(rst_n),
		.adm_req_i(sb_adm_req_w),
		.adm_class_i(sb_adm_class_w),
		.adm_key_i(sb_adm_key_w),
		.adm_gnt_o(sb_gnt_w),
		.adm_id_o(sb_id_w),
		.rel_valid_i(sb_rel_valid_w),
		.rel_id_i(sb_rel_id_w),
		.kill_valid_i(1'b0),
		.kill_id_i(3'd0),
		.kill_resp_queued_i(1'b0),
		.kill_ack_o(sb_kill_ack_nc_w),
		.holds_o(sb_holds_w),
		.full_o(sb_full_w),
		.barrier_pend_o(sb_barrier_w)
	);
	wire trc_wr_valid_w;
	wire [127:0] trc_wr_data_w;
	wire [15:0] trc_wr_count_w;
	wire trc_rd_en_w;
	wire [7:0] trc_rd_addr_w;
	wire [1:0] trc_rd_lane_w;
	wire [31:0] trc_rd_data_w;
	KL_pp_trace_ring #(
		.RECORDS_P(256),
		.RECORD_W_P(128)
	) u_trace(
		.clk_i(clk_i),
		.rst_n(rst_n),
		.wr_valid_i(trc_wr_valid_w),
		.wr_data_i(trc_wr_data_w),
		.wr_count_o(trc_wr_count_w),
		.rd_en_i(trc_rd_en_w),
		.rd_addr_i(trc_rd_addr_w),
		.rd_lane_i(trc_rd_lane_w),
		.rd_data_o(trc_rd_data_w)
	);
	wire org_iss_ready_w;
	wire org_iss_gnt_w;
	wire [15:0] org_iss_seq_w;
	wire [3:0] org_iss_id_w;
	wire org_rt_valid_w;
	wire org_fail_valid_w;
	wire [3:0] org_rt_owner_w;
	wire [3:0] org_rt_id_nc_w;
	wire [3:0] org_fail_owner_w;
	wire [3:0] org_fail_id_nc_w;
	wire org_send_valid_w;
	wire org_resend_valid_w;
	wire [2:0] org_send_slot_w;
	wire [2:0] org_resend_slot_w;
	wire org_hold_valid_w;
	wire org_release_valid_w;
	wire [2:0] org_hold_slot_w;
	wire [2:0] org_release_slot_w;
	wire [7:0] org_withdraw_slot_mask_w;
	wire org_arm_valid_w;
	wire org_arm_cancel_w;
	wire [TMR_AW_C - 1:0] org_arm_slot_w;
	wire [7:0] org_arm_owner_w;
	wire [31:0] org_arm_deadline_w;
	wire [7:0] org_rsp_ign_nc_w;
	wire [3:0] org_busy_nc_w;
	wire ntfy_ca_cancel_valid_w;
	wire [3:0] ntfy_ca_cancel_owner_w;
	wire ca_txs_alloc_req_w;
	wire ca_txs_gnt_w;
	wire [TXS_W_C - 1:0] ca_txs_gnt_slot_w;
	wire [TXS_W_C - 1:0] ca_txs_wr_slot_w;
	wire [TXA_W_C - 1:0] ca_txs_wr_addr_w;
	wire [TXA_W_C - 1:0] ca_txs_wr_len_w;
	wire ca_txs_wr_valid_w;
	wire ca_txs_wr_commit_w;
	wire ca_txs_abort_w;
	wire [7:0] ca_txs_wr_data_w;
	wire ca_iss_valid_w;
	wire [3:0] ca_iss_owner_w;
	wire [2:0] ca_iss_slot_w;
	wire [111:0] ca_iss_key_w;
	wire [15:0] ca_iss_timeout_w;
	wire [TMR_AW_C - 1:0] ca_iss_tmr_slot_w;
	wire ca_issued_nc_w;
	wire [3:0] ca_issued_owner_nc_w;
	wire ca_cancel_release_valid_w;
	wire [TXS_W_C - 1:0] ca_cancel_release_slot_w;
	wire [7:0] arb_gnt_w;
	reg [(8 * TXS_W_C) - 1:0] laneq_org_r;
	wire [63:0] v_hdr_ctlr_eid_w;
	wire [3:0] v_hdr_msg_type_w;
	wire [15:0] v_hdr_opcode_w;
	wire [2:0] v_hdr_protocol_w;
	wire [15:0] v_hdr_seq_w;
	wire [47:0] v_hdr_src_mac_w;
	wire [63:0] v_hdr_target_eid_w;
	wire v_hdr_valid_w;
	KL_pp_originator #(
		.CA_POOL_P(pp_pkg_PP_CA_POOL_C),
		.PROBE_SLOTS_P(0),
		.INFLIGHT_P(pp_pkg_PP_CA_POOL_C),
		.KEY_W_P(112),
		.TMR_SLOTS_P(TMR_SLOTS_C)
	) u_originator(
		.clk_i(clk_i),
		.rst_n(rst_n),
		.iss_valid_i(ca_iss_valid_w),
		.iss_owner_i(ca_iss_owner_w),
		.iss_tx_slot_i(ca_iss_slot_w),
		.iss_key_i(ca_iss_key_w),
		.iss_tmr_slot_i(ca_iss_tmr_slot_w),
		.iss_timeout_ms_i(ca_iss_timeout_w),
		.iss_ready_o(org_iss_ready_w),
		.iss_gnt_o(org_iss_gnt_w),
		.iss_seq_o(org_iss_seq_w),
		.iss_id_o(org_iss_id_w),
		.cancel_valid_i(ntfy_ca_cancel_valid_w),
		.cancel_owner_i(ntfy_ca_cancel_owner_w),
		.rsp_valid_i((((v_hdr_valid_w && (v_hdr_protocol_w == 3'd2)) && (v_hdr_msg_type_w == 4'd1)) && (v_hdr_opcode_w == 16'h0003)) && (v_hdr_ctlr_eid_w == entity_id_i)),
		.rsp_seq_i(v_hdr_seq_w),
		.rsp_key_i({v_hdr_target_eid_w, v_hdr_src_mac_w}),
		.rt_valid_o(org_rt_valid_w),
		.rt_owner_o(org_rt_owner_w),
		.rt_id_o(org_rt_id_nc_w),
		.fail_valid_o(org_fail_valid_w),
		.fail_owner_o(org_fail_owner_w),
		.fail_id_o(org_fail_id_nc_w),
		.send_valid_o(org_send_valid_w),
		.send_slot_o(org_send_slot_w),
		.resend_valid_o(org_resend_valid_w),
		.resend_slot_o(org_resend_slot_w),
		.send_accept_valid_i(arb_gnt_w[LANE_ORIG_C]),
		.send_accept_slot_i(laneq_org_r[0+:TXS_W_C]),
		.hold_valid_o(org_hold_valid_w),
		.hold_slot_o(org_hold_slot_w),
		.release_valid_o(org_release_valid_w),
		.release_slot_o(org_release_slot_w),
		.withdraw_slot_mask_o(org_withdraw_slot_mask_w),
		.tmr_arm_valid_o(org_arm_valid_w),
		.tmr_arm_cancel_o(org_arm_cancel_w),
		.tmr_arm_slot_o(org_arm_slot_w),
		.tmr_arm_owner_o(org_arm_owner_w),
		.tmr_arm_deadline_ms_o(org_arm_deadline_w),
		.now_ms_i(now_ms_w),
		.exp_valid_i(exp_valid_w),
		.exp_slot_i(exp_slot_w),
		.exp_owner_i(exp_owner_w),
		.rsp_ign_cnt_o(org_rsp_ign_nc_w),
		.inflight_busy_o(org_busy_nc_w)
	);
	wire [63:0] ntfy_ca_eid_w;
	wire [47:0] ntfy_ca_mac_w;
	wire [3:0] ntfy_ca_owner_w;
	wire ntfy_ca_ready_w;
	wire ntfy_ca_valid_w;
	KL_aecp_ca_originator #(
		.TMR_SLOTS_P(TMR_SLOTS_C),
		.TMR_CA_BASE_P(TMR_MAP_C[255-:32]),
		.TX_STD_SLOTS_P(TX_STD_SLOTS_P),
		.TX_OVERSIZE_BYTES_P(TX_OVERSIZE_BYTES_P)
	) u_ca_builder(
		.clk_i(clk_i),
		.rst_n(rst_n),
		.entity_id_i(entity_id_i),
		.own_mac_i(own_mac_i),
		.req_valid_i(ntfy_ca_valid_w),
		.req_owner_i(ntfy_ca_owner_w),
		.req_ctlr_eid_i(ntfy_ca_eid_w),
		.req_mac_i(ntfy_ca_mac_w),
		.req_ready_o(ntfy_ca_ready_w),
		.cancel_valid_i(ntfy_ca_cancel_valid_w),
		.cancel_owner_i(ntfy_ca_cancel_owner_w),
		.cancel_release_valid_o(ca_cancel_release_valid_w),
		.cancel_release_slot_o(ca_cancel_release_slot_w),
		.issued_valid_o(ca_issued_nc_w),
		.issued_owner_o(ca_issued_owner_nc_w),
		.txs_alloc_req_o(ca_txs_alloc_req_w),
		.txs_alloc_gnt_i(ca_txs_gnt_w),
		.txs_alloc_slot_i(ca_txs_gnt_slot_w),
		.txs_wr_slot_o(ca_txs_wr_slot_w),
		.txs_wr_addr_o(ca_txs_wr_addr_w),
		.txs_wr_valid_o(ca_txs_wr_valid_w),
		.txs_wr_data_o(ca_txs_wr_data_w),
		.txs_wr_commit_o(ca_txs_wr_commit_w),
		.txs_wr_len_o(ca_txs_wr_len_w),
		.txs_abort_o(ca_txs_abort_w),
		.iss_valid_o(ca_iss_valid_w),
		.iss_owner_o(ca_iss_owner_w),
		.iss_tx_slot_o(ca_iss_slot_w),
		.iss_key_o(ca_iss_key_w),
		.iss_tmr_slot_o(ca_iss_tmr_slot_w),
		.iss_timeout_ms_o(ca_iss_timeout_w),
		.iss_ready_i(org_iss_ready_w),
		.iss_gnt_i(org_iss_gnt_w),
		.iss_seq_i(org_iss_seq_w),
		.iss_id_i(org_iss_id_w)
	);
	wire v_mrp_valid_w;
	wire v_mrp_last_w;
	wire [7:0] v_mrp_data_w;
	wire v_alloc_req_w;
	wire v_alloc_gnt_w;
	wire [RXS_W_C - 1:0] v_alloc_slot_w;
	wire v_wr_valid_w;
	wire v_wr_last_w;
	wire v_wr_abort_w;
	wire v_wr_commit_w;
	wire [7:0] v_wr_data_w;
	wire [4:0] v_hdr_status_w;
	wire [10:0] v_hdr_cdl_w;
	wire v_hdr_u_w;
	wire v_hdr_cr_w;
	wire [63:0] v_hdr_operands_w;
	wire [2:0] v_hdr_rx_slot_w;
	wire [15:0] cnt_rx_da_w;
	wire [15:0] cnt_rx_ethertype_w;
	wire [15:0] cnt_rx_subtype_w;
	wire [15:0] cnt_rx_version_w;
	wire [15:0] cnt_rx_length_w;
	KL_pp_rx_validator #(
		.SLOTS_P(RX_SLOTS_P),
		.BYTES_P(RX_SLOT_BYTES_P)
	) u_rx_validator(
		.clk_i(clk_i),
		.rst_n(rst_n),
		.rx_valid_i(rx_valid_i),
		.rx_data_i(rx_data_i),
		.rx_last_i(rx_last_i),
		.own_mac_i(own_mac_i),
		.mrp_valid_o(v_mrp_valid_w),
		.mrp_data_o(v_mrp_data_w),
		.mrp_last_o(v_mrp_last_w),
		.alloc_req_o(v_alloc_req_w),
		.alloc_gnt_i(v_alloc_gnt_w),
		.alloc_slot_i(v_alloc_slot_w),
		.wr_valid_o(v_wr_valid_w),
		.wr_data_o(v_wr_data_w),
		.wr_last_o(v_wr_last_w),
		.wr_abort_o(v_wr_abort_w),
		.wr_commit_o(v_wr_commit_w),
		.hdr_valid_o(v_hdr_valid_w),
		.hdr_protocol_o(v_hdr_protocol_w),
		.hdr_msg_type_o(v_hdr_msg_type_w),
		.hdr_status_o(v_hdr_status_w),
		.hdr_cdl_o(v_hdr_cdl_w),
		.hdr_src_mac_o(v_hdr_src_mac_w),
		.hdr_controller_eid_o(v_hdr_ctlr_eid_w),
		.hdr_target_eid_o(v_hdr_target_eid_w),
		.hdr_sequence_id_o(v_hdr_seq_w),
		.hdr_u_o(v_hdr_u_w),
		.hdr_cr_o(v_hdr_cr_w),
		.hdr_opcode_o(v_hdr_opcode_w),
		.hdr_operands_o(v_hdr_operands_w),
		.hdr_rx_slot_o(v_hdr_rx_slot_w),
		.rx_da_count_o(cnt_rx_da_w),
		.rx_ethertype_count_o(cnt_rx_ethertype_w),
		.rx_subtype_count_o(cnt_rx_subtype_w),
		.rx_version_count_o(cnt_rx_version_w),
		.rx_length_count_o(cnt_rx_length_w)
	);
	localparam [31:0] RXF_ADP_C = 0;
	localparam [31:0] RXF_LSTN_C = 1;
	localparam [31:0] RXF_TKR_C = 2;
	localparam [31:0] RXF_AECP_C = 3;
	localparam [31:0] RXF_UCPU_C = 4;
	localparam [31:0] RXF_MAAP_C = 5;
	localparam [31:0] RXF_N_C = 6;
	reg [5:0] rxf_vld_r;
	reg [(RXF_N_C * RXS_W_C) - 1:0] rxf_slot_r;
	reg [15:0] rxf_drop_r;
	reg rxf_free_w;
	reg [RXS_W_C - 1:0] rxf_free_slot_w;
	reg [2:0] rxf_pick_ix_w;
	wire [5:0] rxf_req_w;
	wire [(RXF_N_C * RXS_W_C) - 1:0] rxf_req_slot_w;
	wire adp_rxs_free_w;
	wire lstn_rxs_free_w;
	wire tkr_rxs_free_w;
	wire aecp_rxs_free_w;
	wire [RXS_W_C - 1:0] adp_rxs_free_slot_w;
	wire [RXS_W_C - 1:0] lstn_rxs_free_slot_w;
	wire [RXS_W_C - 1:0] tkr_rxs_free_slot_w;
	wire [RXS_W_C - 1:0] aecp_rxs_free_slot_w;
	wire maapeng_rxs_free_w;
	wire [2:0] maapeng_rxs_free_slot_w;
	assign rxf_req_w = {maapeng_rxs_free_w, aecp_rxs_free_w, aecp_rxs_free_i, tkr_rxs_free_w, lstn_rxs_free_w, adp_rxs_free_w};
	assign rxf_req_slot_w = {maapeng_rxs_free_slot_w[RXS_W_C - 1:0], aecp_rxs_free_slot_w, aecp_rxs_free_slot_i, tkr_rxs_free_slot_w, lstn_rxs_free_slot_w, adp_rxs_free_slot_w};
	function automatic [2:0] sv2v_cast_3;
		input reg [2:0] inp;
		sv2v_cast_3 = inp;
	endfunction
	always @(*) begin : rxf_pick
		if (_sv2v_0)
			;
		rxf_free_w = 1'b0;
		rxf_pick_ix_w = 3'd0;
		rxf_free_slot_w = 1'sb0;
		begin : sv2v_autoblock_1
			reg [31:0] i;
			for (i = 0; i < RXF_N_C; i = i + 1)
				if (!rxf_free_w && rxf_vld_r[i]) begin
					rxf_free_w = 1'b1;
					rxf_pick_ix_w = sv2v_cast_3(i);
					rxf_free_slot_w = rxf_slot_r[i * RXS_W_C+:RXS_W_C];
				end
		end
	end
	always @(posedge clk_i) begin : rxf_queue
		if (!rst_n) begin
			rxf_vld_r <= 1'sb0;
			rxf_slot_r <= 1'sb0;
			rxf_drop_r <= 16'd0;
		end
		else begin
			if (rxf_free_w)
				rxf_vld_r[rxf_pick_ix_w] <= 1'b0;
			begin : sv2v_autoblock_2
				reg [31:0] i;
				for (i = 0; i < RXF_N_C; i = i + 1)
					if (rxf_req_w[i]) begin
						if (rxf_vld_r[i] && !(rxf_free_w && (rxf_pick_ix_w == sv2v_cast_3(i)))) begin
							if (rxf_drop_r != 16'hffff)
								rxf_drop_r <= rxf_drop_r + 16'd1;
						end
						else begin
							rxf_vld_r[i] <= 1'b1;
							rxf_slot_r[i * RXS_W_C+:RXS_W_C] <= rxf_req_slot_w[i * RXS_W_C+:RXS_W_C];
						end
					end
			end
		end
	end
	localparam [31:0] RXP_ADP_C = 0;
	localparam [31:0] RXP_LSTN_C = 1;
	localparam [31:0] RXP_TKR_C = 2;
	localparam [31:0] RXP_AECP_C = 3;
	localparam [31:0] RXP_STEER_C = 4;
	localparam [31:0] RXP_UCPU_C = 5;
	localparam [31:0] RXP_N_C = 6;
	wire [5:0] rxp_alloc_gnt_w;
	wire [(RXP_N_C * RXS_W_C) - 1:0] rxp_alloc_slot_w;
	wire [(RXP_N_C * RXS_W_C) - 1:0] rxp_rd_slot_w;
	wire [(RXP_N_C * RXA_W_C) - 1:0] rxp_rd_addr_w;
	wire [5:0] rxp_rd_en_w;
	wire [47:0] rxp_rd_data_w;
	wire [(RXP_N_C * RXL_W_C) - 1:0] rxp_slot_len_w;
	wire [(RXP_N_C * $clog2(RX_SLOTS_P + 1)) - 1:0] rxp_slots_free_w;
	wire [95:0] rxp_overrun_w;
	genvar _gv_g_1;
	generate
		for (_gv_g_1 = 0; _gv_g_1 < RXP_N_C; _gv_g_1 = _gv_g_1 + 1) begin : g_rx_pool
			localparam g = _gv_g_1;
			KL_pp_rx_slots #(
				.SLOTS_P(RX_SLOTS_P),
				.BYTES_P(RX_SLOT_BYTES_P)
			) u_rx_slots(
				.clk_i(clk_i),
				.rst_n(rst_n),
				.alloc_req_i(v_alloc_req_w),
				.alloc_gnt_o(rxp_alloc_gnt_w[g]),
				.alloc_slot_o(rxp_alloc_slot_w[g * RXS_W_C+:RXS_W_C]),
				.wr_valid_i(v_wr_valid_w),
				.wr_data_i(v_wr_data_w),
				.wr_last_i(v_wr_last_w),
				.wr_abort_i(v_wr_abort_w),
				.wr_commit_i(v_wr_commit_w),
				.rd_slot_i(rxp_rd_slot_w[g * RXS_W_C+:RXS_W_C]),
				.rd_addr_i(rxp_rd_addr_w[g * RXA_W_C+:RXA_W_C]),
				.rd_en_i(rxp_rd_en_w[g]),
				.rd_data_o(rxp_rd_data_w[g * 8+:8]),
				.slot_len_o(rxp_slot_len_w[g * RXL_W_C+:RXL_W_C]),
				.free_i(rxf_free_w),
				.free_slot_i(rxf_free_slot_w),
				.slots_free_o(rxp_slots_free_w[g * $clog2(RX_SLOTS_P + 1)+:$clog2(RX_SLOTS_P + 1)]),
				.rx_overrun_count_o(rxp_overrun_w[g * 16+:16])
			);
		end
	endgenerate
	assign v_alloc_gnt_w = rxp_alloc_gnt_w[RXP_ADP_C];
	assign v_alloc_slot_w = rxp_alloc_slot_w[RXP_ADP_C * RXS_W_C+:RXS_W_C];
	assign aecp_rxs_rd_data_o = rxp_rd_data_w[24+:8];
	assign aecp_rxs_slot_len_o = rxp_slot_len_w[RXP_AECP_C * RXL_W_C+:RXL_W_C];
	assign rxp_rd_slot_w[RXP_AECP_C * RXS_W_C+:RXS_W_C] = aecp_rxs_rd_slot_i;
	assign rxp_rd_addr_w[RXP_AECP_C * RXA_W_C+:RXA_W_C] = aecp_rxs_rd_addr_i;
	assign rxp_rd_en_w[RXP_AECP_C] = aecp_rxs_rd_en_i;
	reg hdr_vld_r;
	reg [2:0] hdr_protocol_r;
	reg [3:0] hdr_msg_type_r;
	reg [4:0] hdr_status_r;
	reg [10:0] hdr_cdl_r;
	reg [47:0] hdr_src_mac_r;
	reg [63:0] hdr_ctlr_eid_r;
	reg [63:0] hdr_target_eid_r;
	reg [15:0] hdr_seq_r;
	reg [15:0] hdr_opcode_r;
	reg hdr_u_r;
	reg hdr_cr_r;
	reg [63:0] hdr_operands_r;
	reg [2:0] hdr_rx_slot_r;
	reg [15:0] hdr_drop_r;
	wire nrm_rx_ready_w;
	always @(posedge clk_i) begin : hdr_latch
		if (!rst_n) begin
			hdr_vld_r <= 1'b0;
			hdr_protocol_r <= 3'd0;
			hdr_msg_type_r <= 4'd0;
			hdr_status_r <= 5'd0;
			hdr_cdl_r <= 11'd0;
			hdr_src_mac_r <= 48'd0;
			hdr_ctlr_eid_r <= 64'd0;
			hdr_target_eid_r <= 64'd0;
			hdr_seq_r <= 16'd0;
			hdr_opcode_r <= 16'd0;
			hdr_u_r <= 1'b0;
			hdr_cr_r <= 1'b0;
			hdr_operands_r <= 64'd0;
			hdr_rx_slot_r <= 3'd0;
			hdr_drop_r <= 16'd0;
		end
		else begin
			if (hdr_vld_r && nrm_rx_ready_w)
				hdr_vld_r <= 1'b0;
			if (v_hdr_valid_w) begin
				if (hdr_vld_r && !nrm_rx_ready_w) begin
					if (hdr_drop_r != 16'hffff)
						hdr_drop_r <= hdr_drop_r + 16'd1;
				end
				else begin
					hdr_vld_r <= 1'b1;
					hdr_protocol_r <= v_hdr_protocol_w;
					hdr_msg_type_r <= v_hdr_msg_type_w;
					hdr_status_r <= v_hdr_status_w;
					hdr_cdl_r <= v_hdr_cdl_w;
					hdr_src_mac_r <= v_hdr_src_mac_w;
					hdr_ctlr_eid_r <= v_hdr_ctlr_eid_w;
					hdr_target_eid_r <= v_hdr_target_eid_w;
					hdr_seq_r <= v_hdr_seq_w;
					hdr_opcode_r <= v_hdr_opcode_w;
					hdr_u_r <= v_hdr_u_w;
					hdr_cr_r <= v_hdr_cr_w;
					hdr_operands_r <= v_hdr_operands_w;
					hdr_rx_slot_r <= v_hdr_rx_slot_w;
				end
			end
		end
	end
	wire hz_valid_nc_w;
	wire [2:0] hz_protocol_w;
	wire [15:0] hz_opcode_w;
	reg [3:0] hz_class_w;
	reg [15:0] hz_key_w;
	localparam [15:0] HZ_OP_ADD_AUDIO_MAP_C = 16'h002c;
	localparam [15:0] HZ_OP_REMOVE_AUDIO_MAP_C = 16'h002d;
	always @(*) begin : hz_stub
		if (_sv2v_0)
			;
		(* full_case, parallel_case *)
		case (hz_protocol_w)
			3'd1: hz_class_w = 4'd2;
			3'd2:
				if ((hz_opcode_w == HZ_OP_ADD_AUDIO_MAP_C) || (hz_opcode_w == HZ_OP_REMOVE_AUDIO_MAP_C))
					hz_class_w = 4'd3;
				else
					hz_class_w = 4'd0;
			default: hz_class_w = 4'd0;
		endcase
		hz_key_w = {13'd0, hz_protocol_w};
	end
	wire nrm_txn_valid_w;
	wire [392:0] nrm_txn_w;
	wire nrm_txn_ready_w;
	wire nrm_tmr_ready_nc_w;
	wire nrm_self_ready_nc_w;
	wire nrm_mgmt_ready_nc_w;
	KL_pp_normalizer u_normalizer(
		.clk_i(clk_i),
		.rst_n(rst_n),
		.now_ms_i(now_ms_w),
		.budget_adp_ms_i(BUDGET_ADP_MS_C),
		.budget_acmp_ms_i(BUDGET_ACMP_MS_C),
		.budget_aecp_ms_i(BUDGET_AECP_MS_C),
		.rx_valid_i(hdr_vld_r),
		.rx_ready_o(nrm_rx_ready_w),
		.rx_if_index_i(2'd0),
		.rx_protocol_i(hdr_protocol_r),
		.rx_msg_type_i(hdr_msg_type_r),
		.rx_status_i(hdr_status_r),
		.rx_cdl_i(hdr_cdl_r),
		.rx_src_mac_i(hdr_src_mac_r),
		.rx_controller_eid_i(hdr_ctlr_eid_r),
		.rx_target_eid_i(hdr_target_eid_r),
		.rx_sequence_id_i(hdr_seq_r),
		.rx_u_i(hdr_u_r),
		.rx_cr_i(hdr_cr_r),
		.rx_opcode_i(hdr_opcode_r),
		.rx_operands_i(hdr_operands_r),
		.rx_slot_i(hdr_rx_slot_r),
		.hz_valid_o(hz_valid_nc_w),
		.hz_protocol_o(hz_protocol_w),
		.hz_opcode_o(hz_opcode_w),
		.hz_class_i(hz_class_w),
		.hz_key_i(hz_key_w),
		.tmr_valid_i(1'b0),
		.tmr_txn_i({pp_pkg_PP_TXN_W_C {1'b0}}),
		.tmr_ready_o(nrm_tmr_ready_nc_w),
		.self_valid_i(1'b0),
		.self_txn_i({pp_pkg_PP_TXN_W_C {1'b0}}),
		.self_ready_o(nrm_self_ready_nc_w),
		.mgmt_valid_i(1'b0),
		.mgmt_txn_i({pp_pkg_PP_TXN_W_C {1'b0}}),
		.mgmt_ready_o(nrm_mgmt_ready_nc_w),
		.txn_valid_o(nrm_txn_valid_w),
		.txn_o(nrm_txn_w),
		.txn_ready_i(nrm_txn_ready_w)
	);
	wire adp_txn_valid_w;
	wire acmp_txn_valid_w;
	wire [392:0] adp_txn_w;
	wire [392:0] acmp_txn_w;
	wire adp_txn_ready_w;
	wire acmp_txn_ready_w;
	wire aecp_txn_valid_w;
	wire aecp_txn_ready_w;
	wire [392:0] aecp_txn_w;
	wire maap_txn_valid_w;
	wire maap_txn_ready_w;
	wire [392:0] maap_txn_w;
	wire [7:0] disp_adp_level_w;
	wire [7:0] disp_acmp_level_w;
	wire [7:0] disp_aecp_level_w;
	wire [7:0] disp_maap_level_nc_w;
	wire [15:0] disp_adp_stall_w;
	wire [15:0] disp_acmp_stall_w;
	wire [15:0] disp_aecp_stall_w;
	wire [15:0] disp_maap_stall_nc_w;
	KL_pp_dispatch u_dispatch(
		.clk_i(clk_i),
		.rst_n(rst_n),
		.enq_valid_i(nrm_txn_valid_w),
		.enq_txn_i(nrm_txn_w),
		.enq_ready_o(nrm_txn_ready_w),
		.adp_txn_valid_o(adp_txn_valid_w),
		.adp_txn_o(adp_txn_w),
		.adp_txn_ready_i(adp_txn_ready_w),
		.acmp_txn_valid_o(acmp_txn_valid_w),
		.acmp_txn_o(acmp_txn_w),
		.acmp_txn_ready_i(acmp_txn_ready_w),
		.aecp_txn_valid_o(aecp_txn_valid_w),
		.aecp_txn_o(aecp_txn_w),
		.aecp_txn_ready_i(aecp_txn_ready_w),
		.maap_txn_valid_o(maap_txn_valid_w),
		.maap_txn_o(maap_txn_w),
		.maap_txn_ready_i(maap_txn_ready_w),
		.adp_level_o(disp_adp_level_w),
		.acmp_level_o(disp_acmp_level_w),
		.aecp_level_o(disp_aecp_level_w),
		.maap_level_o(disp_maap_level_nc_w),
		.adp_stall_count_o(disp_adp_stall_w),
		.acmp_stall_count_o(disp_acmp_stall_w),
		.aecp_stall_count_o(disp_aecp_stall_w),
		.maap_stall_count_o(disp_maap_stall_nc_w)
	);
	assign aecp_txn_valid_o = aecp_txn_valid_w && aecp_sb_grant_w;
	assign aecp_txn_o = aecp_txn_w;
	wire [392:0] acmp_head_w;
	reg [392:0] steer_txn_w;
	wire acmp_is_tkr_w;
	wire lstn_txn_ready_w;
	wire tkr_txn_ready_w;
	reg [1:0] pf_st_r;
	reg [3:0] pf_idx_r;
	reg [63:0] pf_eid_r;
	wire pf_ready_w;
	function automatic [392:0] sv2v_cast_393;
		input reg [392:0] inp;
		sv2v_cast_393 = inp;
	endfunction
	assign acmp_head_w = sv2v_cast_393(acmp_txn_w);
	assign acmp_is_tkr_w = (((acmp_head_w[353-:4] == 4'd0) || (acmp_head_w[353-:4] == 4'd2)) || (acmp_head_w[353-:4] == 4'd4)) || (acmp_head_w[353-:4] == 4'd12);
	assign pf_ready_w = pf_st_r == 2'd2;
	assign acmp_txn_ready_w = (acmp_sb_grant_w && pf_ready_w) && (acmp_is_tkr_w ? tkr_txn_ready_w : lstn_txn_ready_w);
	assign rxp_rd_slot_w[RXP_STEER_C * RXS_W_C+:RXS_W_C] = acmp_head_w[56 + RXS_W_C:57];
	function automatic [RXA_W_C - 1:0] sv2v_cast_3BB6D;
		input reg [RXA_W_C - 1:0] inp;
		sv2v_cast_3BB6D = inp;
	endfunction
	assign rxp_rd_addr_w[RXP_STEER_C * RXA_W_C+:RXA_W_C] = sv2v_cast_3BB6D((acmp_is_tkr_w ? 32'd20 : 32'd28) + sv2v_cast_32(pf_idx_r));
	assign rxp_rd_en_w[RXP_STEER_C] = (pf_st_r == 2'd1) && (pf_idx_r < 4'd8);
	localparam [2:0] pp_pkg_PP_SLOT_NULL_C = 3'd7;
	always @(posedge clk_i) begin : steer_prefetch
		if (!rst_n) begin
			pf_st_r <= 2'd0;
			pf_idx_r <= 4'd0;
			pf_eid_r <= 64'd0;
		end
		else
			(* full_case, parallel_case *)
			case (pf_st_r)
				2'd0:
					if (acmp_txn_valid_w) begin
						if (acmp_head_w[59-:3] == pp_pkg_PP_SLOT_NULL_C) begin
							pf_eid_r <= acmp_head_w[221-:64];
							pf_st_r <= 2'd2;
						end
						else begin
							pf_idx_r <= 4'd0;
							pf_st_r <= 2'd1;
						end
					end
				2'd1: begin
					pf_idx_r <= pf_idx_r + 4'd1;
					if (pf_idx_r != 4'd0)
						pf_eid_r <= {pf_eid_r[55:0], rxp_rd_data_w[32+:8]};
					if (pf_idx_r == 4'd8)
						pf_st_r <= 2'd2;
				end
				2'd2:
					if (acmp_txn_valid_w && acmp_txn_ready_w)
						pf_st_r <= 2'd0;
				default: pf_st_r <= 2'd0;
			endcase
	end
	always @(*) begin : steer_head
		if (_sv2v_0)
			;
		steer_txn_w = acmp_head_w;
		steer_txn_w[221-:64] = pf_eid_r;
	end
	wire lstn_disc_arm_w;
	wire lstn_disc_disarm_w;
	wire [63:0] lstn_disc_eid_w;
	wire [SINK_IDX_W_C - 1:0] lstn_act_sink_w;
	wire [47:0] lstn_act_settle_da_w;
	wire [63:0] lstn_act_settle_sid_w;
	wire [11:0] lstn_act_settle_vlan_w;
	wire lstn_act_settle_w;
	always @(posedge clk_i) begin : binding_view
		if (!rst_n) begin
			bound_r <= 1'sb0;
			bound_eid_r <= 1'sb0;
			bound_sid_r <= 1'sb0;
			bound_dmac_r <= 1'sb0;
			bound_vlan_r <= 1'sb0;
		end
		else begin
			if (lstn_disc_arm_w) begin
				bound_r[lstn_act_sink_w] <= 1'b1;
				bound_eid_r[lstn_act_sink_w * 64+:64] <= lstn_disc_eid_w;
			end
			if (lstn_act_settle_w) begin
				bound_sid_r[lstn_act_sink_w * 64+:64] <= lstn_act_settle_sid_w;
				bound_dmac_r[lstn_act_sink_w * 48+:48] <= lstn_act_settle_da_w;
				bound_vlan_r[lstn_act_sink_w * 12+:12] <= lstn_act_settle_vlan_w;
			end
			if (lstn_disc_disarm_w) begin
				bound_r[lstn_act_sink_w] <= 1'b0;
				bound_sid_r[lstn_act_sink_w * 64+:64] <= 64'd0;
				bound_dmac_r[lstn_act_sink_w * 48+:48] <= 48'd0;
				bound_vlan_r[lstn_act_sink_w * 12+:12] <= 12'd0;
			end
		end
	end
	wire adp_prng_req_w;
	wire [2:0] adp_prng_kind_w;
	wire adp_prng_busy_w;
	wire adp_prng_valid_w;
	wire adp_arm_valid_w;
	wire adp_arm_cancel_w;
	wire [TMR_AW_C - 1:0] adp_arm_slot_w;
	wire [7:0] adp_arm_owner_w;
	wire [31:0] adp_arm_deadline_w;
	wire adp_txs_alloc_req_w;
	wire adp_txs_oversize_nc_w;
	wire [TXS_W_C - 1:0] adp_txs_wr_slot_w;
	wire [TXA_W_C - 1:0] adp_txs_wr_addr_w;
	wire [TXA_W_C - 1:0] adp_txs_wr_len_w;
	wire adp_txs_wr_valid_w;
	wire adp_txs_wr_commit_w;
	wire [7:0] adp_txs_wr_data_w;
	wire adp_txreq_valid_w;
	wire [TXS_W_C - 1:0] adp_txreq_slot_w;
	wire [0:0] adp_txreq_if_nc_w;
	wire adp_evt_valid_w;
	wire adp_evt_departed_w;
	wire [SINK_IDX_W_C - 1:0] adp_evt_sink_w;
	wire [0:0] adp_gm_tick_nc_w;
	wire [1:0] adp_dbg_adv_state_w;
	wire [N_STREAM_IN_P - 1:0] adp_dbg_tkdisc_nc_w;
	wire adp_txs_gnt_w;
	wire [TXS_W_C - 1:0] adp_txs_gnt_slot_w;
	KL_adp_engine #(
		.N_IF_P(1),
		.N_SINK_P(N_STREAM_IN_P),
		.TMR_SLOTS_P(TMR_SLOTS_C),
		.TMR_SLOT_ADV_BASE_P(TMR_ADP_ADV_BASE_C),
		.TMR_SLOT_NOADP_BASE_P(TMR_ADP_NOADP_BASE_C),
		.RX_SLOTS_P(RX_SLOTS_P),
		.RX_BYTES_P(RX_SLOT_BYTES_P),
		.TX_STD_SLOTS_P(TX_STD_SLOTS_P),
		.TX_OVERSIZE_BYTES_P(TX_OVERSIZE_BYTES_P)
	) u_adp(
		.clk_i(clk_i),
		.rst_n(rst_n),
		.entity_enable_i(entity_enable_i),
		.link_up_i(link_up_i),
		.gm_change_i(gm_change_i),
		.gm_id_i(gm_id_i),
		.gptp_domain_i(gptp_domain_i),
		.entity_id_i(entity_id_i),
		.entity_model_id_i(entity_model_id_i),
		.own_mac_i(own_mac_i),
		.talker_sources_i(talker_sources_i),
		.talker_caps_i(talker_caps_i),
		.listener_sinks_i(listener_sinks_i),
		.listener_caps_i(listener_caps_i),
		.current_cfg_i(current_cfg_i),
		.identify_index_i(identify_index_i),
		.txn_valid_i(adp_txn_valid_w),
		.txn_i(adp_txn_w),
		.txn_ready_o(adp_txn_ready_w),
		.rxs_rd_slot_o(rxp_rd_slot_w[RXP_ADP_C * RXS_W_C+:RXS_W_C]),
		.rxs_rd_addr_o(rxp_rd_addr_w[RXP_ADP_C * RXA_W_C+:RXA_W_C]),
		.rxs_rd_en_o(rxp_rd_en_w[RXP_ADP_C]),
		.rxs_rd_data_i(rxp_rd_data_w[0+:8]),
		.rxs_free_o(adp_rxs_free_w),
		.rxs_free_slot_o(adp_rxs_free_slot_w),
		.prng_draw_req_o(adp_prng_req_w),
		.prng_draw_kind_o(adp_prng_kind_w),
		.prng_draw_busy_i(adp_prng_busy_w),
		.prng_draw_valid_i(adp_prng_valid_w),
		.prng_draw_ms_i(prng_ms_w),
		.now_ms_i(now_ms_w),
		.tmr_arm_valid_o(adp_arm_valid_w),
		.tmr_arm_cancel_o(adp_arm_cancel_w),
		.tmr_arm_slot_o(adp_arm_slot_w),
		.tmr_arm_owner_o(adp_arm_owner_w),
		.tmr_arm_deadline_ms_o(adp_arm_deadline_w),
		.tmr_exp_valid_i(exp_valid_w),
		.tmr_exp_slot_i(exp_slot_w),
		.tmr_exp_owner_i(exp_owner_w),
		.txs_alloc_req_o(adp_txs_alloc_req_w),
		.txs_oversize_o(adp_txs_oversize_nc_w),
		.txs_alloc_gnt_i(adp_txs_gnt_w),
		.txs_alloc_slot_i(adp_txs_gnt_slot_w),
		.txs_wr_slot_o(adp_txs_wr_slot_w),
		.txs_wr_addr_o(adp_txs_wr_addr_w),
		.txs_wr_valid_o(adp_txs_wr_valid_w),
		.txs_wr_data_o(adp_txs_wr_data_w),
		.txs_wr_commit_o(adp_txs_wr_commit_w),
		.txs_wr_len_o(adp_txs_wr_len_w),
		.txreq_valid_o(adp_txreq_valid_w),
		.txreq_slot_o(adp_txreq_slot_w),
		.txreq_if_o(adp_txreq_if_nc_w),
		.bound_i(bound_r),
		.bound_talker_eid_i(bound_eid_r),
		.evt_valid_o(adp_evt_valid_w),
		.evt_departed_o(adp_evt_departed_w),
		.evt_sink_o(adp_evt_sink_w),
		.gm_changed_tick_o(adp_gm_tick_nc_w),
		.dbg_adv_state_o(adp_dbg_adv_state_w),
		.dbg_avail_index_o(adp_dbg_aidx_nc_w),
		.dbg_tk_discovered_o(adp_dbg_tkdisc_nc_w)
	);
	wire lstn_evt_tk_valid_w;
	wire lstn_evt_tk_ready_w;
	reg [1:0] lstn_evt_tk_kind_w;
	wire lstn_evt_tk_failed_w;
	wire [15:0] lstn_evt_tk_sink_w;
	wire pre_valid_w;
	wire pre_ready_w;
	wire [15:0] pre_sink_w;
	wire [15:0] pre_talker_uid_w;
	wire [63:0] pre_talker_eid_w;
	wire [63:0] pre_ctlr_eid_w;
	wire pre_sw_w;
	wire pre_started_w;
	wire lstn_arm_valid_w;
	wire lstn_arm_cancel_w;
	wire [TMR_AW_C - 1:0] lstn_arm_slot_w;
	wire [7:0] lstn_arm_owner_w;
	wire [31:0] lstn_arm_deadline_w;
	wire lstn_draw_req_w;
	wire [2:0] lstn_draw_kind_w;
	wire lstn_draw_busy_w;
	wire lstn_draw_valid_w;
	wire lstn_txs_alloc_req_w;
	wire lstn_txs_oversize_nc_w;
	wire [TXS_W_C - 1:0] lstn_txs_wr_slot_w;
	wire [TXA_W_C - 1:0] lstn_txs_wr_addr_w;
	wire [TXA_W_C - 1:0] lstn_txs_wr_len_w;
	wire lstn_txs_wr_valid_w;
	wire lstn_txs_wr_commit_w;
	wire [7:0] lstn_txs_wr_data_w;
	wire lstn_txreq_valid_w;
	wire [TXS_W_C - 1:0] lstn_txreq_slot_w;
	wire lstn_act_teardown_w;
	wire lstn_act_nvm_nc_w;
	wire lstn_act_nvm_set_nc_w;
	wire lstn_act_notify_nc_w;
	wire lstn_recwr_w;
	wire [SINK_IDX_W_C - 1:0] lstn_recwr_sink_w;
	localparam [31:0] pp_acmp_pkg_ACMP_REC_W_C = 384;
	wire [383:0] lstn_recwr_rec_w;
	wire lstn_txs_gnt_w;
	wire [TXS_W_C - 1:0] lstn_txs_gnt_slot_w;
	wire strm_set_valid_w;
	wire strm_set_val_w;
	wire strm_set_ready_w;
	wire strm_set_error_w;
	wire [15:0] strm_set_index_w;
	wire [15:0] lstn_strq_drop_w;
	wire lstn_act_strt_chg_w;
	wire lstn_act_strt_cmd_chg_w;
	wire [63:0] ntfy_lock_ctlr_w;
	wire ntfy_lock_held_w;
	KL_pp_acmp_listener #(
		.N_SINKS_P(N_STREAM_IN_P),
		.TROM_HEX_P(TROM_HEX_P),
		.RX_SLOTS_P(RX_SLOTS_P),
		.RX_SLOT_BYTES_P(RX_SLOT_BYTES_P),
		.TX_STD_SLOTS_P(TX_STD_SLOTS_P),
		.TX_OVERSIZE_BYTES_P(TX_OVERSIZE_BYTES_P),
		.TMR_SLOT_AW_P(TMR_AW_C),
		.TMR_BASE_SLOT_P(TMR_LSTN_BASE_C),
		.TMR_OWNER_BASE_P(32),
		.STRM_TIMEOUT_CYC_P(DESC_MEM_TMO_CYC_P)
	) u_listener(
		.clk_i(clk_i),
		.rst_n(rst_n),
		.entity_id_i(entity_id_i),
		.txn_valid_i(((acmp_txn_valid_w && acmp_sb_grant_w) && pf_ready_w) && !acmp_is_tkr_w),
		.txn_i(steer_txn_w),
		.txn_ready_o(lstn_txn_ready_w),
		.evt_tk_valid_i(lstn_evt_tk_valid_w),
		.evt_tk_kind_i(lstn_evt_tk_kind_w),
		.evt_tk_failed_i(lstn_evt_tk_failed_w),
		.evt_tk_sink_i(lstn_evt_tk_sink_w),
		.evt_tk_ready_o(lstn_evt_tk_ready_w),
		.pre_valid_i(pre_valid_w),
		.pre_sink_i(pre_sink_w),
		.pre_talker_eid_i(pre_talker_eid_w),
		.pre_talker_uid_i(pre_talker_uid_w),
		.pre_ctlr_eid_i(pre_ctlr_eid_w),
		.pre_sw_i(pre_sw_w),
		.pre_started_i(pre_started_w),
		.strm_set_valid_i(strm_set_valid_w),
		.strm_set_sink_i(strm_set_index_w),
		.strm_set_val_i(strm_set_val_w),
		.strm_set_ready_o(strm_set_ready_w),
		.strm_set_error_o(strm_set_error_w),
		.strm_started_o(aecp_strm_started_o),
		.dbg_strq_drop_o(lstn_strq_drop_w),
		.act_strt_chg_o(lstn_act_strt_chg_w),
		.act_strt_cmd_chg_o(lstn_act_strt_cmd_chg_w),
		.pre_ready_o(pre_ready_w),
		.now_ms_i(now_ms_w),
		.tmr_arm_valid_o(lstn_arm_valid_w),
		.tmr_arm_cancel_o(lstn_arm_cancel_w),
		.tmr_arm_slot_o(lstn_arm_slot_w),
		.tmr_arm_owner_o(lstn_arm_owner_w),
		.tmr_arm_deadline_ms_o(lstn_arm_deadline_w),
		.tmr_exp_valid_i(exp_valid_w),
		.tmr_exp_slot_i(exp_slot_w),
		.tmr_exp_owner_i(exp_owner_w),
		.draw_req_o(lstn_draw_req_w),
		.draw_kind_o(lstn_draw_kind_w),
		.draw_busy_i(lstn_draw_busy_w),
		.draw_valid_i(lstn_draw_valid_w),
		.draw_ms_i(prng_ms_w),
		.rxs_rd_slot_o(rxp_rd_slot_w[RXP_LSTN_C * RXS_W_C+:RXS_W_C]),
		.rxs_rd_addr_o(rxp_rd_addr_w[RXP_LSTN_C * RXA_W_C+:RXA_W_C]),
		.rxs_rd_en_o(rxp_rd_en_w[RXP_LSTN_C]),
		.rxs_rd_data_i(rxp_rd_data_w[8+:8]),
		.rxs_free_o(lstn_rxs_free_w),
		.rxs_free_slot_o(lstn_rxs_free_slot_w),
		.txs_alloc_req_o(lstn_txs_alloc_req_w),
		.txs_oversize_o(lstn_txs_oversize_nc_w),
		.txs_alloc_gnt_i(lstn_txs_gnt_w),
		.txs_alloc_slot_i(lstn_txs_gnt_slot_w),
		.txs_wr_slot_o(lstn_txs_wr_slot_w),
		.txs_wr_addr_o(lstn_txs_wr_addr_w),
		.txs_wr_valid_o(lstn_txs_wr_valid_w),
		.txs_wr_data_o(lstn_txs_wr_data_w),
		.txs_wr_commit_o(lstn_txs_wr_commit_w),
		.txs_wr_len_o(lstn_txs_wr_len_w),
		.txreq_valid_o(lstn_txreq_valid_w),
		.txreq_slot_o(lstn_txreq_slot_w),
		.lock_held_i(ntfy_lock_held_w),
		.lock_ctlr_i(ntfy_lock_ctlr_w),
		.act_settle_o(lstn_act_settle_w),
		.act_settle_sid_o(lstn_act_settle_sid_w),
		.act_settle_da_o(lstn_act_settle_da_w),
		.act_settle_vlan_o(lstn_act_settle_vlan_w),
		.act_teardown_o(lstn_act_teardown_w),
		.act_disc_arm_o(lstn_disc_arm_w),
		.act_disc_talker_eid_o(lstn_disc_eid_w),
		.act_disc_disarm_o(lstn_disc_disarm_w),
		.act_nvm_o(lstn_act_nvm_nc_w),
		.act_nvm_set_o(lstn_act_nvm_set_nc_w),
		.act_notify_o(lstn_act_notify_nc_w),
		.act_sink_o(lstn_act_sink_w),
		.dbg_busy_o(lstn_dbg_busy_nc_w),
		.dbg_recwr_o(lstn_recwr_w),
		.dbg_recwr_sink_o(lstn_recwr_sink_w),
		.dbg_recwr_rec_o(lstn_recwr_rec_w)
	);
	wire tkr_resp_valid_w;
	wire [3:0] tkr_resp_msg_type_w;
	wire [4:0] tkr_resp_status_w;
	wire [63:0] tkr_resp_sid_w;
	wire [63:0] tkr_resp_ctlr_w;
	wire [63:0] tkr_resp_tkeid_w;
	wire [63:0] tkr_resp_lseid_w;
	wire [15:0] tkr_resp_tkuid_w;
	wire [15:0] tkr_resp_lsuid_w;
	wire [15:0] tkr_resp_cc_w;
	wire [15:0] tkr_resp_seq_w;
	wire [15:0] tkr_resp_flags_w;
	wire [15:0] tkr_resp_vlan_w;
	wire [47:0] tkr_resp_da_w;
	wire [1:0] tkr_resp_if_nc_w;
	wire tkr_gate_open_w;
	wire tkr_gate_close_w;
	wire [SRC_IDX_W_C - 1:0] tkr_gate_src_w;
	wire [63:0] tkr_gate_sid_w;
	wire [47:0] tkr_gate_da_w;
	wire [11:0] tkr_gate_vlan_w;
	wire tkr_arm_valid_w;
	wire tkr_arm_cancel_w;
	wire [TMR_AW_C - 1:0] tkr_arm_slot_w;
	wire [7:0] tkr_arm_owner_w;
	wire [31:0] tkr_arm_deadline_w;
	wire tkr_draw_req_w;
	wire [2:0] tkr_draw_kind_w;
	wire tkr_draw_busy_w;
	wire tkr_draw_valid_w;
	wire tkr_maap_req_valid_w;
	wire tkr_maap_req_ready_w;
	wire tkr_maap_req_release_w;
	wire [SRC_IDX_W_C - 1:0] tkr_maap_req_src_w;
	wire tkr_maap_rsp_valid_w;
	wire tkr_maap_rsp_ok_w;
	wire [47:0] tkr_maap_rsp_da_w;
	wire tkr_maap_confl_valid_w;
	wire [SRC_IDX_W_C - 1:0] tkr_maap_confl_src_w;
	wire tkr_maap_confl_ack_w;
	wire [(N_STREAM_IN_P * 64) - 1:0] srp_snk_fail_bridge_nc_w;
	KL_acmp_talker #(
		.N_STREAM_OUT_P(N_STREAM_OUT_P),
		.RX_SLOTS_P(RX_SLOTS_P),
		.RX_SLOT_BYTES_P(RX_SLOT_BYTES_P),
		.TMR_SLOTS_P(TMR_SLOTS_C),
		.TMR_SLOT_BASE_P(TMR_TKR_BASE_C),
		.TMR_OWNER_BASE_P(32'h00000050)
	) u_talker(
		.clk_i(clk_i),
		.rst_n(rst_n),
		.own_entity_id_i(entity_id_i),
		.cfg_src_en_i(cfg_src_en_i),
		.cfg_src_iface_i(cfg_src_iface_i),
		.cfg_stream_id_i(cfg_stream_id_i),
		.srp_lsn_reg_state_i(srp_lstn_reg_state_w),
		.srp_class_vid_i(srp_class_a_vid_w),
		.srp_pcp_change_i(srp_evt_domain_change_w),
		.txn_valid_i(((acmp_txn_valid_w && acmp_sb_grant_w) && pf_ready_w) && acmp_is_tkr_w),
		.txn_i(steer_txn_w),
		.txn_ready_o(tkr_txn_ready_w),
		.rxs_rd_slot_o(rxp_rd_slot_w[RXP_TKR_C * RXS_W_C+:RXS_W_C]),
		.rxs_rd_addr_o(rxp_rd_addr_w[RXP_TKR_C * RXA_W_C+:RXA_W_C]),
		.rxs_rd_en_o(rxp_rd_en_w[RXP_TKR_C]),
		.rxs_rd_data_i(rxp_rd_data_w[16+:8]),
		.rxs_slot_len_i(rxp_slot_len_w[RXP_TKR_C * RXL_W_C+:RXL_W_C]),
		.rxs_free_o(tkr_rxs_free_w),
		.rxs_free_slot_o(tkr_rxs_free_slot_w),
		.resp_valid_o(tkr_resp_valid_w),
		.resp_msg_type_o(tkr_resp_msg_type_w),
		.resp_status_o(tkr_resp_status_w),
		.resp_stream_id_o(tkr_resp_sid_w),
		.resp_controller_eid_o(tkr_resp_ctlr_w),
		.resp_talker_eid_o(tkr_resp_tkeid_w),
		.resp_listener_eid_o(tkr_resp_lseid_w),
		.resp_talker_uid_o(tkr_resp_tkuid_w),
		.resp_listener_uid_o(tkr_resp_lsuid_w),
		.resp_dest_mac_o(tkr_resp_da_w),
		.resp_conn_count_o(tkr_resp_cc_w),
		.resp_seq_id_o(tkr_resp_seq_w),
		.resp_flags_o(tkr_resp_flags_w),
		.resp_vlan_id_o(tkr_resp_vlan_w),
		.resp_if_index_o(tkr_resp_if_nc_w),
		.maap_req_valid_o(tkr_maap_req_valid_w),
		.maap_req_ready_i(tkr_maap_req_ready_w),
		.maap_req_release_o(tkr_maap_req_release_w),
		.maap_req_src_o(tkr_maap_req_src_w),
		.maap_rsp_valid_i(tkr_maap_rsp_valid_w),
		.maap_rsp_ok_i(tkr_maap_rsp_ok_w),
		.maap_rsp_da_i(tkr_maap_rsp_da_w),
		.maap_conflict_valid_i(tkr_maap_confl_valid_w),
		.maap_conflict_src_i(tkr_maap_confl_src_w),
		.maap_conflict_ack_o(tkr_maap_confl_ack_w),
		.declaring_o(tkr_declaring_w),
		.gate_open_o(tkr_gate_open_w),
		.gate_close_o(tkr_gate_close_w),
		.gate_src_o(tkr_gate_src_w),
		.gate_stream_id_o(tkr_gate_sid_w),
		.gate_da_o(tkr_gate_da_w),
		.gate_vlan_o(tkr_gate_vlan_w),
		.now_ms_i(now_ms_w),
		.tmr_arm_valid_o(tkr_arm_valid_w),
		.tmr_arm_cancel_o(tkr_arm_cancel_w),
		.tmr_arm_slot_o(tkr_arm_slot_w),
		.tmr_arm_owner_o(tkr_arm_owner_w),
		.tmr_arm_deadline_ms_o(tkr_arm_deadline_w),
		.tmr_exp_valid_i(exp_valid_w),
		.tmr_exp_slot_i(exp_slot_w),
		.tmr_exp_owner_i(exp_owner_w),
		.prng_draw_req_o(tkr_draw_req_w),
		.prng_draw_kind_o(tkr_draw_kind_w),
		.prng_draw_busy_i(tkr_draw_busy_w),
		.prng_draw_valid_i(tkr_draw_valid_w),
		.prng_draw_ms_i(prng_ms_w)
	);
	wire maapeng_prng_req_w;
	wire [2:0] maapeng_prng_kind_w;
	wire maapeng_prng_busy_w;
	wire maapeng_prng_valid_w;
	wire maapeng_arm_valid_w;
	wire maapeng_arm_cancel_w;
	wire [TMR_AW_C - 1:0] maapeng_arm_slot_w;
	wire [7:0] maapeng_arm_owner_w;
	wire [31:0] maapeng_arm_deadline_w;
	wire maapeng_txs_alloc_req_w;
	wire maapeng_txs_oversize_nc_w;
	wire maapeng_txs_gnt_w;
	wire [TXS_W_C - 1:0] maapeng_txs_gnt_slot_w;
	wire [TXS_W_C - 1:0] maapeng_txs_wr_slot_w;
	wire [TXA_W_C - 1:0] maapeng_txs_wr_addr_w;
	wire [TXA_W_C - 1:0] maapeng_txs_wr_len_w;
	wire maapeng_txs_wr_valid_w;
	wire maapeng_txs_wr_commit_w;
	wire [7:0] maapeng_txs_wr_data_w;
	wire maapeng_txreq_valid_w;
	wire maapeng_txreq_ready_w;
	wire [TXS_W_C - 1:0] maapeng_txreq_slot_w;
	wire maapeng_alloc_valid_w;
	wire maapeng_alloc_ready_w;
	wire maapeng_rsp_valid_w;
	wire maapeng_rsp_ok_w;
	wire [47:0] maapeng_rsp_da_w;
	wire maapeng_confl_valid_w;
	wire [SRC_IDX_W_C - 1:0] maapeng_confl_src_w;
	wire maapeng_confl_ack_w;
	KL_pp_maap #(
		.N_SRC_P(N_STREAM_OUT_P),
		.RX_SLOTS_P(RX_SLOTS_P),
		.TMR_SLOTS_P(TMR_SLOTS_C),
		.TMR_SLOT_BASE_P(TMR_MAAP_BASE_C),
		.TMR_OWNER_BASE_P(pp_pkg_PP_OWN_MAAP_C),
		.TX_STD_SLOTS_P(TX_STD_SLOTS_P),
		.TX_OVERSIZE_BYTES_P(TX_OVERSIZE_BYTES_P)
	) u_maap(
		.clk_i(clk_i),
		.rst_n(rst_n),
		.cfg_en_i(cfg_maap_internal_i),
		.cfg_count_i(cfg_maap_count_i),
		.cfg_seed_offset_i(cfg_maap_seed_offset_i),
		.cfg_seed_valid_i(cfg_maap_seed_valid_i),
		.own_mac_i(own_mac_i),
		.link_up_i(link_up_i),
		.txn_valid_i(maap_txn_valid_w),
		.txn_i(maap_txn_w),
		.txn_ready_o(maap_txn_ready_w),
		.rxs_free_o(maapeng_rxs_free_w),
		.rxs_free_slot_o(maapeng_rxs_free_slot_w),
		.prng_draw_req_o(maapeng_prng_req_w),
		.prng_draw_kind_o(maapeng_prng_kind_w),
		.prng_draw_busy_i(maapeng_prng_busy_w),
		.prng_draw_valid_i(maapeng_prng_valid_w),
		.prng_draw_ms_i(prng_ms_w),
		.now_ms_i(now_ms_w),
		.tmr_arm_valid_o(maapeng_arm_valid_w),
		.tmr_arm_cancel_o(maapeng_arm_cancel_w),
		.tmr_arm_slot_o(maapeng_arm_slot_w),
		.tmr_arm_owner_o(maapeng_arm_owner_w),
		.tmr_arm_deadline_ms_o(maapeng_arm_deadline_w),
		.tmr_exp_valid_i(exp_valid_w),
		.tmr_exp_slot_i(exp_slot_w),
		.tmr_exp_owner_i(exp_owner_w),
		.txs_alloc_req_o(maapeng_txs_alloc_req_w),
		.txs_oversize_o(maapeng_txs_oversize_nc_w),
		.txs_alloc_gnt_i(maapeng_txs_gnt_w),
		.txs_alloc_slot_i(maapeng_txs_gnt_slot_w),
		.txs_wr_slot_o(maapeng_txs_wr_slot_w),
		.txs_wr_addr_o(maapeng_txs_wr_addr_w),
		.txs_wr_valid_o(maapeng_txs_wr_valid_w),
		.txs_wr_data_o(maapeng_txs_wr_data_w),
		.txs_wr_commit_o(maapeng_txs_wr_commit_w),
		.txs_wr_len_o(maapeng_txs_wr_len_w),
		.txreq_valid_o(maapeng_txreq_valid_w),
		.txreq_slot_o(maapeng_txreq_slot_w),
		.txreq_ready_i(maapeng_txreq_ready_w),
		.alloc_req_valid_i(maapeng_alloc_valid_w),
		.alloc_req_ready_o(maapeng_alloc_ready_w),
		.alloc_req_release_i(tkr_maap_req_release_w),
		.alloc_req_src_i(tkr_maap_req_src_w),
		.alloc_rsp_valid_o(maapeng_rsp_valid_w),
		.alloc_rsp_ok_o(maapeng_rsp_ok_w),
		.alloc_rsp_da_o(maapeng_rsp_da_w),
		.conflict_valid_o(maapeng_confl_valid_w),
		.conflict_src_o(maapeng_confl_src_w),
		.conflict_ack_i(maapeng_confl_ack_w),
		.addr_o(maap_addr_o),
		.addr_valid_o(maap_addr_valid_o),
		.state_o(maap_state_o),
		.conflicts_o(maap_conflicts_o),
		.defends_o(maap_defends_o)
	);
	assign tkr_maap_req_ready_w = (cfg_maap_internal_i ? maapeng_alloc_ready_w : maap_req_ready_i);
	assign tkr_maap_rsp_valid_w = (cfg_maap_internal_i ? maapeng_rsp_valid_w : maap_rsp_valid_i);
	assign tkr_maap_rsp_ok_w = (cfg_maap_internal_i ? maapeng_rsp_ok_w : maap_rsp_ok_i);
	assign tkr_maap_rsp_da_w = (cfg_maap_internal_i ? maapeng_rsp_da_w : maap_rsp_da_i);
	assign tkr_maap_confl_valid_w = (cfg_maap_internal_i ? maapeng_confl_valid_w : maap_conflict_valid_i);
	assign tkr_maap_confl_src_w = (cfg_maap_internal_i ? maapeng_confl_src_w : maap_conflict_src_i);
	assign maapeng_alloc_valid_w = (cfg_maap_internal_i ? tkr_maap_req_valid_w : 1'b0);
	assign maapeng_confl_ack_w = (cfg_maap_internal_i ? tkr_maap_confl_ack_w : 1'b0);
	assign maap_req_valid_o = (cfg_maap_internal_i ? 1'b0 : tkr_maap_req_valid_w);
	assign maap_req_release_o = tkr_maap_req_release_w;
	assign maap_req_src_o = tkr_maap_req_src_w;
	assign maap_conflict_ack_o = (cfg_maap_internal_i ? 1'b0 : tkr_maap_confl_ack_w);
	wire mrp_valid_w;
	wire mrp_last_w;
	wire mrp_msrp_w;
	wire mrp_ready_w;
	wire [7:0] mrp_data_w;
	wire [15:0] mrp_drop_w;
	KL_mrp_strip u_mrp_strip(
		.clk_i(clk_i),
		.rst_n(rst_n),
		.in_valid_i(v_mrp_valid_w),
		.in_data_i(v_mrp_data_w),
		.in_last_i(v_mrp_last_w),
		.out_valid_o(mrp_valid_w),
		.out_data_o(mrp_data_w),
		.out_last_o(mrp_last_w),
		.out_msrp_o(mrp_msrp_w),
		.out_ready_i(mrp_ready_w),
		.drop_count_o(mrp_drop_w)
	);
	reg srp_req_valid_w;
	wire srp_req_ready_w;
	wire [2:0] srp_req_op_w;
	wire [7:0] srp_req_index_w;
	wire [63:0] srp_req_sid_w;
	wire [47:0] srp_req_da_w;
	wire [11:0] srp_req_vid_w;
	wire [15:0] srp_req_mfs_w;
	wire [1:0] srp_req_lstn_w;
	wire srp_rsp_valid_w;
	wire [1:0] srp_rsp_status_w;
	wire [31:0] srp_rsp_data_w;
	wire srp_txs_alloc_req_w;
	wire srp_txs_oversize_nc_w;
	wire [TXS_W_C - 1:0] srp_txs_wr_slot_w;
	wire [TXA_W_C - 1:0] srp_txs_wr_addr_w;
	wire [TXA_W_C - 1:0] srp_txs_wr_len_w;
	wire srp_txs_wr_valid_w;
	wire srp_txs_wr_commit_w;
	wire [7:0] srp_txs_wr_data_w;
	wire srp_txreq_valid_w;
	wire [TXS_W_C - 1:0] srp_txreq_slot_w;
	wire srp_txreq_ready_w;
	wire srp_arm_valid_w;
	wire srp_arm_cancel_w;
	wire [TMR_AW_C - 1:0] srp_arm_slot_w;
	wire [7:0] srp_arm_owner_w;
	wire [31:0] srp_arm_deadline_w;
	wire srp_draw_req_w;
	wire [2:0] srp_draw_kind_w;
	wire srp_draw_busy_w;
	wire srp_draw_valid_w;
	wire [N_STREAM_IN_P - 1:0] srp_evt_tk_reg_w;
	wire [N_STREAM_IN_P - 1:0] srp_evt_tk_unreg_w;
	wire [N_STREAM_OUT_P - 1:0] srp_lstn_reg_change_w;
	wire [3:0] srp_dbg_vid_active_w;
	wire srp_dbg_vlan_err_nc_w;
	wire srp_dbg_adm_round_nc_w;
	wire srp_dbg_pdu_done_nc_w;
	wire srp_dbg_pdu_ok_nc_w;
	wire srp_dbg_pdu_malformed_nc_w;
	wire srp_txs_gnt_w;
	wire [TXS_W_C - 1:0] srp_txs_gnt_slot_w;
	KL_srp_top #(
		.N_SOURCES_P(N_STREAM_OUT_P),
		.N_SINKS_P(N_STREAM_IN_P),
		.TX_STD_BYTES_P(576),
		.TX_OVERSIZE_BYTES_P(TX_OVERSIZE_BYTES_P),
		.SLOT_AW_P(TMR_AW_C),
		.CAD_SLOT_BASE_P(TMR_SRP_CAD_BASE_C),
		.CAD_OWNER_BASE_P(SRP_CAD_OWNER_C),
		.TK_SLOT_BASE_P(TMR_SRP_TK_BASE_C),
		.TK_OWNER_BASE_P(SRP_TK_OWNER_C),
		.LS_SLOT_BASE_P(TMR_SRP_LS_BASE_C),
		.LS_OWNER_BASE_P(SRP_LS_OWNER_C)
	) u_srp(
		.clk_i(clk_i),
		.rst_n(rst_n),
		.own_mac_i(own_mac_i),
		.link_up_i(link_up_i),
		.p2p_i(p2p_i),
		.cfg_rank_i(cfg_rank_i),
		.cfg_acc_lat_ns_i(cfg_acc_lat_ns_i),
		.port_rate_bps_i(port_rate_bps_i),
		.mrp_valid_i(mrp_valid_w),
		.mrp_data_i(mrp_data_w),
		.mrp_last_i(mrp_last_w),
		.mrp_msrp_i(mrp_msrp_w),
		.mrp_ready_o(mrp_ready_w),
		.req_valid_i(srp_req_valid_w),
		.req_ready_o(srp_req_ready_w),
		.req_op_i(srp_req_op_w),
		.req_index_i(srp_req_index_w),
		.req_stream_id_i(srp_req_sid_w),
		.req_da_i(srp_req_da_w),
		.req_vid_i(srp_req_vid_w),
		.req_max_frame_i(srp_req_mfs_w),
		.req_max_interval_i(16'd1),
		.req_lstn_state_i(srp_req_lstn_w),
		.rsp_valid_o(srp_rsp_valid_w),
		.rsp_status_o(srp_rsp_status_w),
		.rsp_data_o(srp_rsp_data_w),
		.alloc_req_o(srp_txs_alloc_req_w),
		.oversize_o(srp_txs_oversize_nc_w),
		.alloc_slot_i(srp_txs_gnt_slot_w),
		.alloc_gnt_i(srp_txs_gnt_w),
		.wr_slot_o(srp_txs_wr_slot_w),
		.wr_addr_o(srp_txs_wr_addr_w),
		.wr_valid_o(srp_txs_wr_valid_w),
		.wr_data_o(srp_txs_wr_data_w),
		.wr_commit_o(srp_txs_wr_commit_w),
		.wr_len_o(srp_txs_wr_len_w),
		.txreq_valid_o(srp_txreq_valid_w),
		.txreq_slot_o(srp_txreq_slot_w),
		.txreq_ready_i(srp_txreq_ready_w),
		.now_ms_i(now_ms_w),
		.arm_valid_o(srp_arm_valid_w),
		.arm_cancel_o(srp_arm_cancel_w),
		.arm_slot_o(srp_arm_slot_w),
		.arm_owner_o(srp_arm_owner_w),
		.arm_deadline_ms_o(srp_arm_deadline_w),
		.exp_valid_i(exp_valid_w),
		.exp_slot_i(exp_slot_w),
		.draw_req_o(srp_draw_req_w),
		.draw_kind_o(srp_draw_kind_w),
		.draw_busy_i(srp_draw_busy_w),
		.draw_valid_i(srp_draw_valid_w),
		.draw_ms_i(prng_ms_w),
		.evt_tk_registered_o(srp_evt_tk_reg_w),
		.evt_tk_unregistered_o(srp_evt_tk_unreg_w),
		.lstn_reg_change_o(srp_lstn_reg_change_w),
		.evt_domain_change_o(srp_evt_domain_change_w),
		.class_a_prio_o(srp_class_a_prio_w),
		.class_a_vid_o(srp_class_a_vid_w),
		.domain_adopted_o(srp_domain_adopted_w),
		.tk_decl_state_o(srp_tk_decl_state_w),
		.lstn_reg_state_o(srp_lstn_reg_state_w),
		.active_o(srp_active_w),
		.src_fail_code_o(srp_src_fail_code_nc_w),
		.src_fail_bridge_o(srp_src_fail_bridge_nc_w),
		.tk_reg_state_o(srp_tk_reg_state_w),
		.lstn_decl_state_o(srp_lstn_decl_state_w),
		.acc_latency_o(srp_acc_latency_w),
		.snk_fail_code_o(srp_snk_fail_code_w),
		.snk_fail_bridge_o(srp_snk_fail_bridge_nc_w),
		.granted_slope_bps_o(srp_granted_slope_w),
		.sr_admitted_o(srp_sr_admitted_w),
		.sum_slope_bps_o(srp_sum_slope_w),
		.over_limit_o(srp_over_limit_w),
		.dbg_vid_active_o(srp_dbg_vid_active_w),
		.dbg_vlan_err_o(srp_dbg_vlan_err_nc_w),
		.dbg_adm_round_o(srp_dbg_adm_round_nc_w),
		.dbg_pdu_done_o(srp_dbg_pdu_done_nc_w),
		.dbg_pdu_ok_o(srp_dbg_pdu_ok_nc_w),
		.dbg_pdu_malformed_o(srp_dbg_pdu_malformed_nc_w)
	);
	reg [153:0] st_tk_r;
	reg [153:0] st_ls_r;
	reg [153:0] st_svc_r;
	reg [153:0] inflight_r;
	reg st_tk_vld_r;
	reg st_ls_vld_r;
	reg st_svc_vld_r;
	reg inflight_vld_r;
	reg [15:0] svc_drop_r;
	assign svc_ready_o = !st_svc_vld_r;
	function automatic [7:0] sv2v_cast_8;
		input reg [7:0] inp;
		sv2v_cast_8 = inp;
	endfunction
	always @(posedge clk_i) begin : srp_svc_adapter
		if (!rst_n) begin
			st_tk_r <= 1'sb0;
			st_tk_vld_r <= 1'b0;
			st_ls_r <= 1'sb0;
			st_ls_vld_r <= 1'b0;
			st_svc_r <= 1'sb0;
			st_svc_vld_r <= 1'b0;
			inflight_r <= 1'sb0;
			inflight_vld_r <= 1'b0;
			srp_req_valid_w <= 1'b0;
			svc_drop_r <= 16'd0;
			svc_rsp_valid_o <= 1'b0;
			svc_rsp_status_o <= 2'd0;
			svc_rsp_data_o <= 32'd0;
		end
		else begin
			svc_rsp_valid_o <= 1'b0;
			if (tkr_gate_open_w || tkr_gate_close_w) begin
				if (st_tk_vld_r) begin
					if (svc_drop_r != 16'hffff)
						svc_drop_r <= svc_drop_r + 16'd1;
				end
				else begin
					st_tk_vld_r <= 1'b1;
					st_tk_r <= {1'b0, (tkr_gate_open_w ? 3'd0 : 3'd1), sv2v_cast_8(tkr_gate_src_w), tkr_gate_sid_w, tkr_gate_da_w, tkr_gate_vlan_w, cfg_tspec_max_frame_i, 2'd0};
				end
			end
			if (lstn_act_settle_w || lstn_act_teardown_w) begin
				if (st_ls_vld_r) begin
					if (svc_drop_r != 16'hffff)
						svc_drop_r <= svc_drop_r + 16'd1;
				end
				else begin
					st_ls_vld_r <= 1'b1;
					st_ls_r <= {1'b0, (lstn_act_settle_w ? 3'd2 : 3'd3), sv2v_cast_8(lstn_act_sink_w), lstn_act_settle_sid_w, lstn_act_settle_da_w, lstn_act_settle_vlan_w, 18'h00002};
				end
			end
			if (svc_valid_i && !st_svc_vld_r) begin
				st_svc_vld_r <= 1'b1;
				st_svc_r <= {1'b1, svc_op_i, svc_index_i, svc_stream_id_i, svc_da_i, svc_vid_i, svc_max_frame_i, svc_lstn_state_i};
			end
			if (!inflight_vld_r) begin
				if (st_tk_vld_r) begin
					inflight_r <= st_tk_r;
					inflight_vld_r <= 1'b1;
					st_tk_vld_r <= 1'b0;
					srp_req_valid_w <= 1'b1;
				end
				else if (st_ls_vld_r) begin
					inflight_r <= st_ls_r;
					inflight_vld_r <= 1'b1;
					st_ls_vld_r <= 1'b0;
					srp_req_valid_w <= 1'b1;
				end
				else if (st_svc_vld_r) begin
					inflight_r <= st_svc_r;
					inflight_vld_r <= 1'b1;
					st_svc_vld_r <= 1'b0;
					srp_req_valid_w <= 1'b1;
				end
			end
			else begin
				if (srp_req_valid_w && srp_req_ready_w)
					srp_req_valid_w <= 1'b0;
				if (srp_rsp_valid_w) begin
					inflight_vld_r <= 1'b0;
					if (inflight_r[153]) begin
						svc_rsp_valid_o <= 1'b1;
						svc_rsp_status_o <= srp_rsp_status_w;
						svc_rsp_data_o <= srp_rsp_data_w;
					end
				end
			end
		end
	end
	assign srp_req_op_w = inflight_r[152-:3];
	assign srp_req_index_w = inflight_r[149-:8];
	assign srp_req_sid_w = inflight_r[141-:64];
	assign srp_req_da_w = inflight_r[77-:48];
	assign srp_req_vid_w = inflight_r[29-:12];
	assign srp_req_mfs_w = inflight_r[17-:16];
	assign srp_req_lstn_w = inflight_r[1-:2];
	wire nvm_req_w;
	wire nvm_we_w;
	wire nvm_wvalid_w;
	wire nvm_wready_w;
	wire [7:0] nvm_record_id_w;
	wire [7:0] nvm_wdata_w;
	wire [7:0] nvm_rdata_w;
	wire nvm_rvalid_w;
	wire nvm_rready_w;
	wire nvm_busy_w;
	wire nvm_done_w;
	wire nvm_err_w;
	wire [N_STREAM_IN_P - 1:0] nvm_dbg_valid_nc_w;
	wire [N_STREAM_IN_P - 1:0] nvm_dbg_touched_nc_w;
	KL_acmp_nvm_shadow #(.N_SINKS_P(N_STREAM_IN_P)) u_nvm_shadow(
		.clk_i(clk_i),
		.rst_n(rst_n),
		.tick_i(tick_ms_w),
		.restore_go_i(restore_go_i),
		.restore_busy_o(restore_busy_o),
		.restore_done_o(restore_done_o),
		.restore_fail_o(restore_fail_o),
		.restore_blank_o(restore_blank_o),
		.alarm_o(nvm_alarm_o),
		.cap_wr_i(lstn_recwr_w),
		.cap_sink_i(lstn_recwr_sink_w),
		.cap_rec_i(lstn_recwr_rec_w),
		.pre_valid_o(pre_valid_w),
		.pre_sink_o(pre_sink_w),
		.pre_talker_eid_o(pre_talker_eid_w),
		.pre_talker_uid_o(pre_talker_uid_w),
		.pre_ctlr_eid_o(pre_ctlr_eid_w),
		.pre_sw_o(pre_sw_w),
		.pre_started_o(pre_started_w),
		.pre_ready_i(pre_ready_w),
		.nvm_req_o(nvm_req_w),
		.nvm_we_o(nvm_we_w),
		.nvm_record_id_o(nvm_record_id_w),
		.nvm_wvalid_o(nvm_wvalid_w),
		.nvm_wready_i(nvm_wready_w),
		.nvm_wdata_o(nvm_wdata_w),
		.nvm_rvalid_i(nvm_rvalid_w),
		.nvm_rready_o(nvm_rready_w),
		.nvm_rdata_i(nvm_rdata_w),
		.nvm_busy_i(nvm_busy_w),
		.nvm_done_i(nvm_done_w),
		.nvm_err_i(nvm_err_w),
		.dbg_dirty_o(nvm_unflushed_o),
		.dbg_valid_o(nvm_dbg_valid_nc_w),
		.dbg_touched_o(nvm_dbg_touched_nc_w)
	);
	KL_pp_nvm_port u_nvm_port(
		.clk_i(clk_i),
		.rst_n(rst_n),
		.nvm_req_i(nvm_req_w),
		.nvm_we_i(nvm_we_w),
		.nvm_record_id_i(nvm_record_id_w),
		.nvm_wvalid_i(nvm_wvalid_w),
		.nvm_wready_o(nvm_wready_w),
		.nvm_wdata_i(nvm_wdata_w),
		.nvm_rvalid_o(nvm_rvalid_w),
		.nvm_rready_i(nvm_rready_w),
		.nvm_rdata_o(nvm_rdata_w),
		.nvm_busy_o(nvm_busy_w),
		.nvm_done_o(nvm_done_w),
		.nvm_err_o(nvm_err_w),
		.dev_req_o(nvm_dev_req_o),
		.dev_gnt_i(nvm_dev_gnt_i),
		.dev_op_o(nvm_dev_op_o),
		.dev_region_o(nvm_dev_region_o),
		.dev_offset_o(nvm_dev_offset_o),
		.dev_len_o(nvm_dev_len_o),
		.dev_wvalid_o(nvm_dev_wvalid_o),
		.dev_wready_i(nvm_dev_wready_i),
		.dev_wdata_o(nvm_dev_wdata_o),
		.dev_rvalid_i(nvm_dev_rvalid_i),
		.dev_rdata_i(nvm_dev_rdata_i),
		.dev_rready_o(nvm_dev_rready_o),
		.dev_busy_i(nvm_dev_busy_i),
		.dev_done_i(nvm_dev_done_i),
		.dev_err_i(nvm_dev_err_i)
	);
	localparam [31:0] ARM_N_C = 8;
	localparam [31:0] ARM_W_C = ((1 + TMR_AW_C) + pp_pkg_PP_TIMER_OWNER_W_C) + 32;
	wire [7:0] armq_in_vld_w;
	wire [(ARM_N_C * ARM_W_C) - 1:0] armq_in_w;
	reg [(32 * ARM_W_C) - 1:0] armq_r;
	reg [23:0] armq_cnt_r;
	reg [15:0] arm_drop_r;
	wire ntfy_arm_valid_w;
	wire ntfy_mon_arm_valid_w;
	assign armq_in_vld_w = {ntfy_mon_arm_valid_w, ntfy_arm_valid_w, maapeng_arm_valid_w, org_arm_valid_w, srp_arm_valid_w, adp_arm_valid_w, tkr_arm_valid_w, lstn_arm_valid_w};
	assign armq_in_w[0+:ARM_W_C] = {lstn_arm_cancel_w, lstn_arm_slot_w, lstn_arm_owner_w, lstn_arm_deadline_w};
	assign armq_in_w[ARM_W_C+:ARM_W_C] = {tkr_arm_cancel_w, tkr_arm_slot_w, tkr_arm_owner_w, tkr_arm_deadline_w};
	assign armq_in_w[2 * ARM_W_C+:ARM_W_C] = {adp_arm_cancel_w, adp_arm_slot_w, adp_arm_owner_w, adp_arm_deadline_w};
	assign armq_in_w[3 * ARM_W_C+:ARM_W_C] = {srp_arm_cancel_w, srp_arm_slot_w, srp_arm_owner_w, srp_arm_deadline_w};
	assign armq_in_w[4 * ARM_W_C+:ARM_W_C] = {org_arm_cancel_w, org_arm_slot_w, org_arm_owner_w, org_arm_deadline_w};
	assign armq_in_w[5 * ARM_W_C+:ARM_W_C] = {maapeng_arm_cancel_w, maapeng_arm_slot_w, maapeng_arm_owner_w, maapeng_arm_deadline_w};
	wire ntfy_arm_cancel_w;
	wire [31:0] ntfy_arm_deadline_w;
	wire [7:0] ntfy_arm_owner_w;
	wire [TMR_AW_C - 1:0] ntfy_arm_slot_w;
	assign armq_in_w[6 * ARM_W_C+:ARM_W_C] = {ntfy_arm_cancel_w, ntfy_arm_slot_w, ntfy_arm_owner_w, ntfy_arm_deadline_w};
	wire ntfy_mon_arm_cancel_w;
	wire [31:0] ntfy_mon_arm_deadline_w;
	wire [7:0] ntfy_mon_arm_owner_w;
	wire [TMR_AW_C - 1:0] ntfy_mon_arm_slot_w;
	assign armq_in_w[7 * ARM_W_C+:ARM_W_C] = {ntfy_mon_arm_cancel_w, ntfy_mon_arm_slot_w, ntfy_mon_arm_owner_w, ntfy_mon_arm_deadline_w};
	reg [7:0] armq_pop_w;
	reg [23:0] armq_mid_w;
	reg [7:0] armq_push_ok_w;
	always @(*) begin : arm_drain_pick
		if (_sv2v_0)
			;
		armq_pop_w = 1'sb0;
		begin : sv2v_autoblock_3
			reg [31:0] i;
			for (i = 0; i < ARM_N_C; i = i + 1)
				if ((armq_pop_w == {8 {1'sb0}}) && (armq_cnt_r[i * 3+:3] != 3'd0))
					armq_pop_w[i] = 1'b1;
		end
		begin : sv2v_autoblock_4
			reg [31:0] i;
			for (i = 0; i < ARM_N_C; i = i + 1)
				begin
					armq_mid_w[i * 3+:3] = armq_cnt_r[i * 3+:3] - (armq_pop_w[i] ? 3'd1 : 3'd0);
					armq_push_ok_w[i] = armq_in_vld_w[i] && (armq_mid_w[i * 3+:3] != 3'd4);
				end
		end
	end
	function automatic [1:0] sv2v_cast_2;
		input reg [1:0] inp;
		sv2v_cast_2 = inp;
	endfunction
	always @(posedge clk_i) begin : arm_mux
		if (!rst_n) begin
			armq_r <= 1'sb0;
			armq_cnt_r <= 1'sb0;
			arm_drop_r <= 16'd0;
			tmr_arm_valid_w <= 1'b0;
			tmr_arm_cancel_w <= 1'b0;
			tmr_arm_slot_w <= 1'sb0;
			tmr_arm_owner_w <= 1'sb0;
			tmr_arm_deadline_w <= 32'd0;
		end
		else begin
			tmr_arm_valid_w <= 1'b0;
			begin : sv2v_autoblock_5
				reg [31:0] i;
				for (i = 0; i < ARM_N_C; i = i + 1)
					begin
						if (armq_pop_w[i]) begin
							{tmr_arm_cancel_w, tmr_arm_slot_w, tmr_arm_owner_w, tmr_arm_deadline_w} <= armq_r[(i * 4) * ARM_W_C+:ARM_W_C];
							tmr_arm_valid_w <= 1'b1;
							armq_r[(i * 4) * ARM_W_C+:ARM_W_C] <= armq_r[((i * 4) + 1) * ARM_W_C+:ARM_W_C];
							armq_r[((i * 4) + 1) * ARM_W_C+:ARM_W_C] <= armq_r[((i * 4) + 2) * ARM_W_C+:ARM_W_C];
							armq_r[((i * 4) + 2) * ARM_W_C+:ARM_W_C] <= armq_r[((i * 4) + 3) * ARM_W_C+:ARM_W_C];
						end
						begin : sv2v_autoblock_6
							reg [31:0] e;
							for (e = 0; e < 4; e = e + 1)
								if (armq_push_ok_w[i] && (armq_mid_w[(i * 3) + 1-:2] == sv2v_cast_2(e)))
									armq_r[((i * 4) + e) * ARM_W_C+:ARM_W_C] <= armq_in_w[i * ARM_W_C+:ARM_W_C];
						end
						if (armq_in_vld_w[i] && !armq_push_ok_w[i]) begin
							if (arm_drop_r != 16'hffff)
								arm_drop_r <= arm_drop_r + 16'd1;
						end
						armq_cnt_r[i * 3+:3] <= armq_mid_w[i * 3+:3] + (armq_push_ok_w[i] ? 3'd1 : 3'd0);
					end
			end
		end
	end
	localparam [31:0] PRNG_N_C = 6;
	reg [5:0] pr_pend_r;
	reg [17:0] pr_kind_r;
	reg pr_inflight_r;
	reg [2:0] pr_owner_r;
	wire [5:0] pr_req_w;
	wire [17:0] pr_kind_w;
	wire pr_any_pend_w;
	wire pr_busy_shared_w;
	wire ntfy_prng_req_w;
	assign pr_req_w = {ntfy_prng_req_w, maapeng_prng_req_w, srp_draw_req_w, adp_prng_req_w, tkr_draw_req_w, lstn_draw_req_w};
	wire [2:0] ntfy_prng_kind_w;
	assign pr_kind_w = {ntfy_prng_kind_w, maapeng_prng_kind_w, srp_draw_kind_w, adp_prng_kind_w, tkr_draw_kind_w, lstn_draw_kind_w};
	assign pr_any_pend_w = |pr_pend_r;
	assign pr_busy_shared_w = (pr_inflight_r || pr_any_pend_w) || prng_busy_w;
	assign lstn_draw_busy_w = pr_busy_shared_w;
	assign tkr_draw_busy_w = pr_busy_shared_w;
	assign adp_prng_busy_w = pr_busy_shared_w;
	assign srp_draw_busy_w = pr_busy_shared_w;
	assign maapeng_prng_busy_w = pr_busy_shared_w;
	wire ntfy_prng_busy_w;
	assign ntfy_prng_busy_w = pr_busy_shared_w;
	assign lstn_draw_valid_w = (prng_valid_w && pr_inflight_r) && (pr_owner_r == 3'd0);
	assign tkr_draw_valid_w = (prng_valid_w && pr_inflight_r) && (pr_owner_r == 3'd1);
	assign adp_prng_valid_w = (prng_valid_w && pr_inflight_r) && (pr_owner_r == 3'd2);
	assign srp_draw_valid_w = (prng_valid_w && pr_inflight_r) && (pr_owner_r == 3'd3);
	assign maapeng_prng_valid_w = (prng_valid_w && pr_inflight_r) && (pr_owner_r == 3'd4);
	wire ntfy_prng_valid_w;
	assign ntfy_prng_valid_w = (prng_valid_w && pr_inflight_r) && (pr_owner_r == 3'd5);
	always @(posedge clk_i) begin : prng_mux
		if (!rst_n) begin
			pr_pend_r <= 1'sb0;
			pr_kind_r <= 1'sb0;
			pr_inflight_r <= 1'b0;
			pr_owner_r <= 3'd0;
			prng_req_w <= 1'b0;
			prng_kind_w <= 3'd0;
		end
		else begin
			prng_req_w <= 1'b0;
			begin : sv2v_autoblock_7
				reg [31:0] i;
				for (i = 0; i < PRNG_N_C; i = i + 1)
					if (pr_req_w[i] && !(pr_inflight_r && (pr_owner_r == sv2v_cast_3(i)))) begin
						pr_pend_r[i] <= 1'b1;
						pr_kind_r[i * 3+:3] <= pr_kind_w[i * 3+:3];
					end
			end
			if (pr_inflight_r) begin
				if (prng_valid_w)
					pr_inflight_r <= 1'b0;
			end
			else if (!prng_busy_w && !prng_req_w) begin : sv2v_autoblock_8
				reg [31:0] i;
				for (i = 0; i < PRNG_N_C; i = i + 1)
					if (!pr_inflight_r && pr_pend_r[i]) begin
						prng_req_w <= 1'b1;
						prng_kind_w <= pr_kind_r[i * 3+:3];
						pr_owner_r <= sv2v_cast_3(i);
						pr_pend_r[i] <= 1'b0;
						pr_inflight_r <= 1'b1;
					end
			end
		end
	end
	function automatic [287:0] pp_pkg_pp_evr_map;
		input reg [31:0] si;
		input reg [31:0] so;
		reg [287:0] m;
		begin
			m[287-:32] = 32'd0;
			m[255-:32] = m[287-:32] + si;
			m[223-:32] = m[255-:32] + si;
			m[191-:32] = m[223-:32] + 32'd1;
			m[159-:32] = m[191-:32] + 32'd1;
			m[127-:32] = m[159-:32] + 32'd1;
			m[95-:32] = m[127-:32] + so;
			m[63-:32] = m[95-:32] + 32'd1;
			m[31-:32] = m[63-:32] + 32'd1;
			pp_pkg_pp_evr_map = m;
		end
	endfunction
	localparam [287:0] EVR_MAP_C = pp_pkg_pp_evr_map(N_STREAM_IN_P, N_STREAM_OUT_P);
	localparam [31:0] EVR_TKREG_BASE_C = EVR_MAP_C[287-:32];
	localparam [31:0] EVR_TKUNR_BASE_C = EVR_MAP_C[255-:32];
	localparam [31:0] EVR_ADP_DISC_C = EVR_MAP_C[223-:32];
	localparam [31:0] EVR_ADP_DEP_C = EVR_MAP_C[191-:32];
	localparam [31:0] EVR_DOMAIN_C = EVR_MAP_C[159-:32];
	localparam [31:0] EVR_LSNCHG_BASE_C = EVR_MAP_C[127-:32];
	localparam [31:0] EVR_GM_C = EVR_MAP_C[95-:32];
	localparam [31:0] EVR_LINK_C = EVR_MAP_C[63-:32];
	localparam [31:0] EVR_N_SRC_C = EVR_MAP_C[31-:32];
	localparam [31:0] EVR_SRC_W_C = (EVR_N_SRC_C > 1 ? $clog2(EVR_N_SRC_C) : 1);
	reg [EVR_N_SRC_C - 1:0] evr_strobe_w;
	reg [(EVR_N_SRC_C * 16) - 1:0] evr_payload_w;
	wire evr_valid_w;
	wire [EVR_SRC_W_C - 1:0] evr_src_w;
	wire [15:0] evr_pay_w;
	wire evr_lost_w;
	wire evr_ack_w;
	reg link_q_r;
	always @(posedge clk_i) begin : link_edge
		if (!rst_n)
			link_q_r <= 1'b0;
		else
			link_q_r <= link_up_i;
	end
	function automatic [15:0] sv2v_cast_16;
		input reg [15:0] inp;
		sv2v_cast_16 = inp;
	endfunction
	always @(*) begin : evr_sources
		if (_sv2v_0)
			;
		evr_strobe_w = 1'sb0;
		evr_payload_w = 1'sb0;
		begin : sv2v_autoblock_9
			reg [31:0] k;
			for (k = 0; k < N_STREAM_IN_P; k = k + 1)
				begin
					evr_strobe_w[EVR_TKREG_BASE_C + k] = srp_evt_tk_reg_w[k];
					evr_payload_w[(EVR_TKREG_BASE_C + k) * 16+:16] = {srp_tk_reg_state_w[k * 2+:2] == 2'd2, 7'd0, sv2v_cast_8(k)};
					evr_strobe_w[EVR_TKUNR_BASE_C + k] = srp_evt_tk_unreg_w[k];
					evr_payload_w[(EVR_TKUNR_BASE_C + k) * 16+:16] = {8'd0, sv2v_cast_8(k)};
				end
		end
		evr_strobe_w[EVR_ADP_DISC_C] = adp_evt_valid_w && !adp_evt_departed_w;
		evr_payload_w[EVR_ADP_DISC_C * 16+:16] = sv2v_cast_16(adp_evt_sink_w);
		evr_strobe_w[EVR_ADP_DEP_C] = adp_evt_valid_w && adp_evt_departed_w;
		evr_payload_w[EVR_ADP_DEP_C * 16+:16] = sv2v_cast_16(adp_evt_sink_w);
		evr_strobe_w[EVR_DOMAIN_C] = srp_evt_domain_change_w;
		evr_payload_w[EVR_DOMAIN_C * 16+:16] = {4'd0, srp_class_a_vid_w};
		begin : sv2v_autoblock_10
			reg [31:0] k;
			for (k = 0; k < N_STREAM_OUT_P; k = k + 1)
				begin
					evr_strobe_w[EVR_LSNCHG_BASE_C + k] = srp_lstn_reg_change_w[k];
					evr_payload_w[(EVR_LSNCHG_BASE_C + k) * 16+:16] = {8'd0, sv2v_cast_8(k)};
				end
		end
		evr_strobe_w[EVR_GM_C] = gm_change_i;
		evr_payload_w[EVR_GM_C * 16+:16] = 16'd0;
		evr_strobe_w[EVR_LINK_C] = link_up_i != link_q_r;
		evr_payload_w[EVR_LINK_C * 16+:16] = {15'd0, link_up_i};
	end
	wire [EVR_SRC_W_C - 1:0] evr_lost_src_w;
	wire [7:0] evr_lost_cnt_nc_w;
	KL_pp_event_router #(
		.N_SRC_P(EVR_N_SRC_C),
		.PAYLOAD_W_P(16)
	) u_event_router(
		.clk_i(clk_i),
		.rst_n(rst_n),
		.src_strobe_i(evr_strobe_w),
		.src_payload_i(evr_payload_w),
		.evt_valid_o(evr_valid_w),
		.evt_src_o(evr_src_w),
		.evt_payload_o(evr_pay_w),
		.evt_lost_o(evr_lost_w),
		.evt_ack_i(evr_ack_w),
		.lost_src_i(evr_lost_src_w),
		.lost_count_o(evr_lost_cnt_nc_w)
	);
	assign evr_lost_src_w = evr_src_w;
	wire evr_tk_sel_w;
	function automatic [EVR_SRC_W_C - 1:0] sv2v_cast_866B6;
		input reg [EVR_SRC_W_C - 1:0] inp;
		sv2v_cast_866B6 = inp;
	endfunction
	assign evr_tk_sel_w = evr_valid_w && (evr_src_w <= sv2v_cast_866B6(EVR_ADP_DEP_C));
	assign lstn_evt_tk_valid_w = evr_tk_sel_w;
	assign lstn_evt_tk_sink_w = {8'd0, evr_pay_w[7:0]};
	assign lstn_evt_tk_failed_w = evr_pay_w[15];
	localparam [1:0] pp_acmp_pkg_TK_KIND_DEP_C = 2'd1;
	localparam [1:0] pp_acmp_pkg_TK_KIND_DISC_C = 2'd0;
	localparam [1:0] pp_acmp_pkg_TK_KIND_REG_C = 2'd2;
	localparam [1:0] pp_acmp_pkg_TK_KIND_UNREG_C = 2'd3;
	always @(*) begin : evt_kind_map
		if (_sv2v_0)
			;
		if (evr_src_w < sv2v_cast_866B6(EVR_TKUNR_BASE_C))
			lstn_evt_tk_kind_w = pp_acmp_pkg_TK_KIND_REG_C;
		else if (evr_src_w < sv2v_cast_866B6(EVR_ADP_DISC_C))
			lstn_evt_tk_kind_w = pp_acmp_pkg_TK_KIND_UNREG_C;
		else if (evr_src_w == sv2v_cast_866B6(EVR_ADP_DISC_C))
			lstn_evt_tk_kind_w = pp_acmp_pkg_TK_KIND_DISC_C;
		else
			lstn_evt_tk_kind_w = pp_acmp_pkg_TK_KIND_DEP_C;
	end
	assign evr_ack_w = (evr_tk_sel_w ? lstn_evt_tk_ready_w : evr_valid_w);
	assign trc_wr_valid_w = evr_valid_w && evr_ack_w;
	assign trc_wr_data_w = {now_ms_w, sv2v_cast_8(evr_src_w), 7'd0, evr_lost_w, evr_pay_w, 64'd0};
	reg [2:0] tkb_st_r;
	reg tkb_pend_r;
	reg [3:0] tkb_msg_r;
	reg [4:0] tkb_status_r;
	reg [63:0] tkb_sid_r;
	reg [63:0] tkb_ctlr_r;
	reg [63:0] tkb_tkeid_r;
	reg [63:0] tkb_lseid_r;
	reg [15:0] tkb_tkuid_r;
	reg [15:0] tkb_lsuid_r;
	reg [15:0] tkb_cc_r;
	reg [15:0] tkb_seq_r;
	reg [15:0] tkb_flags_r;
	reg [15:0] tkb_vlan_r;
	reg [47:0] tkb_da_r;
	reg [15:0] tkb_drop_r;
	reg [TXS_W_C - 1:0] tkb_slot_r;
	reg [5:0] tkb_bidx_r;
	wire tkb_alloc_req_w;
	wire tkb_gnt_w;
	wire [TXS_W_C - 1:0] tkb_gnt_slot_w;
	reg tkb_lane_valid_r;
	wire tkb_lane_gnt_w;
	wire [447:0] tkb_pdu_w;
	wire [7:0] tkb_pdu_byte_w;
	assign tkb_pdu_w = {12'hfc0, tkb_msg_r, tkb_status_r, 11'd44, tkb_sid_r, tkb_ctlr_r, tkb_tkeid_r, tkb_lseid_r, tkb_tkuid_r, tkb_lsuid_r, tkb_da_r, tkb_cc_r, tkb_seq_r, tkb_flags_r, tkb_vlan_r, 16'h0000};
	assign tkb_pdu_byte_w = tkb_pdu_w[9'd440 - {tkb_bidx_r, 3'b000}+:8];
	assign tkb_alloc_req_w = tkb_st_r == 3'd1;
	always @(posedge clk_i) begin : tkb_engine
		if (!rst_n) begin
			tkb_st_r <= 3'd0;
			tkb_pend_r <= 1'b0;
			tkb_msg_r <= 4'd0;
			tkb_status_r <= 5'd0;
			tkb_sid_r <= 64'd0;
			tkb_ctlr_r <= 64'd0;
			tkb_tkeid_r <= 64'd0;
			tkb_lseid_r <= 64'd0;
			tkb_tkuid_r <= 16'd0;
			tkb_lsuid_r <= 16'd0;
			tkb_cc_r <= 16'd0;
			tkb_seq_r <= 16'd0;
			tkb_flags_r <= 16'd0;
			tkb_vlan_r <= 16'd0;
			tkb_da_r <= 48'd0;
			tkb_drop_r <= 16'd0;
			tkb_slot_r <= 1'sb0;
			tkb_bidx_r <= 6'd0;
			tkb_lane_valid_r <= 1'b0;
		end
		else begin
			if (tkr_resp_valid_w) begin
				if (tkb_pend_r) begin
					if (tkb_drop_r != 16'hffff)
						tkb_drop_r <= tkb_drop_r + 16'd1;
				end
				else begin
					tkb_pend_r <= 1'b1;
					tkb_msg_r <= tkr_resp_msg_type_w;
					tkb_status_r <= tkr_resp_status_w;
					tkb_sid_r <= tkr_resp_sid_w;
					tkb_ctlr_r <= tkr_resp_ctlr_w;
					tkb_tkeid_r <= tkr_resp_tkeid_w;
					tkb_lseid_r <= tkr_resp_lseid_w;
					tkb_tkuid_r <= tkr_resp_tkuid_w;
					tkb_lsuid_r <= tkr_resp_lsuid_w;
					tkb_cc_r <= tkr_resp_cc_w;
					tkb_seq_r <= tkr_resp_seq_w;
					tkb_flags_r <= tkr_resp_flags_w;
					tkb_vlan_r <= tkr_resp_vlan_w;
					tkb_da_r <= tkr_resp_da_w;
				end
			end
			(* full_case, parallel_case *)
			case (tkb_st_r)
				3'd0:
					if (tkb_pend_r)
						tkb_st_r <= 3'd1;
				3'd1:
					if (tkb_gnt_w) begin
						tkb_slot_r <= tkb_gnt_slot_w;
						tkb_bidx_r <= 6'd0;
						tkb_st_r <= 3'd2;
					end
				3'd2:
					if (tkb_bidx_r == 6'd55)
						tkb_st_r <= 3'd3;
					else
						tkb_bidx_r <= tkb_bidx_r + 6'd1;
				3'd3: begin
					tkb_st_r <= 3'd4;
					tkb_lane_valid_r <= 1'b1;
				end
				3'd4:
					if (tkb_lane_gnt_w) begin
						tkb_lane_valid_r <= 1'b0;
						tkb_pend_r <= 1'b0;
						tkb_st_r <= 3'd0;
					end
				default: tkb_st_r <= 3'd0;
			endcase
		end
	end
	wire [RXS_W_C - 1:0] aecp_eng_free_slot_w;
	wire aecp_txs_alloc_req_w;
	wire aecp_txs_oversize_w;
	wire [TXS_W_C - 1:0] aecp_txs_wr_slot_w;
	wire [TXA_W_C - 1:0] aecp_txs_wr_addr_w;
	wire [TXA_W_C - 1:0] aecp_txs_wr_len_w;
	wire aecp_txs_wr_valid_w;
	wire aecp_txs_wr_commit_w;
	wire [7:0] aecp_txs_wr_data_w;
	wire aecp_txreq_valid_w;
	wire aecp_txreq_ready_w;
	wire aecp_txreq_uns_valid_w;
	wire aecp_txreq_uns_ready_w;
	wire [TXS_W_C - 1:0] aecp_txreq_slot_w;
	wire aecp_txs_gnt_w;
	wire [TXS_W_C - 1:0] aecp_txs_gnt_slot_w;
	wire aecp_rgy_req_w;
	wire aecp_rgy_state_w;
	wire aecp_rgy_tl_w;
	wire aecp_rgy_wait_w;
	wire [1:0] aecp_rgy_op_w;
	wire [63:0] aecp_rgy_eid_w;
	wire [63:0] aecp_rgy_data_w;
	wire [47:0] aecp_rgy_mac_w;
	wire uns_valid_w;
	wire uns_done_w;
	wire [3:0] uns_kind_w;
	wire [15:0] uns_dt_w;
	wire [15:0] uns_di_w;
	wire [15:0] uns_seq_w;
	wire [15:0] uns_arg0_w;
	wire [15:0] uns_arg1_w;
	wire uns_amap_remove_w;
	wire ntfy_amap_busy_w;
	wire [15:0] uns_amap_count_w;
	wire [63:0] uns_eid_w;
	wire [47:0] uns_mac_w;
	wire [7:0] ntfy_reg_cnt_nc_w;
	wire [7:0] ntfy_coalesce_nc_w;
	wire [15:0] ntfy_uns_cnt_nc_w;
	reg [N_STREAM_IN_P - 1:0] ntfy_stri_in_w;
	reg [N_STREAM_OUT_P - 1:0] ntfy_stri_out_w;
	assign aecp_lock_held_o = ntfy_lock_held_w;
	always @(*) begin : stri_events
		if (_sv2v_0)
			;
		ntfy_stri_in_w = 1'sb0;
		ntfy_stri_out_w = 1'sb0;
		begin : sv2v_autoblock_11
			reg [31:0] k;
			for (k = 0; k < N_STREAM_IN_P; k = k + 1)
				ntfy_stri_in_w[k] = (((sv2v_cast_32(lstn_act_sink_w) == k) && ((((lstn_disc_arm_w || lstn_disc_disarm_w) || lstn_act_settle_w) || lstn_act_teardown_w) || (lstn_act_strt_chg_w && !lstn_act_strt_cmd_chg_w))) || srp_evt_tk_reg_w[k]) || srp_evt_tk_unreg_w[k];
		end
		begin : sv2v_autoblock_12
			reg [31:0] k;
			for (k = 0; k < N_STREAM_OUT_P; k = k + 1)
				ntfy_stri_out_w[k] = ((sv2v_cast_32(tkr_gate_src_w) == k) && (tkr_gate_open_w || tkr_gate_close_w)) || srp_lstn_reg_change_w[k];
		end
	end
	wire aecp_eff_commit_nc_w;
	wire [3:0] aecp_eff_notify_cls_nc_w;
	wire aecp_eff_notify_stb_nc_w;
	wire [15:0] aecp_eff_notify_type_w;
	wire [15:0] aecp_eff_notify_index_w;
	wire [15:0] aecp_eff_notify_arg0_w;
	wire [15:0] aecp_eff_notify_arg1_w;
	wire [63:0] aecp_eff_notify_excl_w;
	wire aecp_dbg_busy_nc_w;
	wire aecp_dbg_img_valid_w;
	wire [15:0] aecp_dbg_cmd_w;
	wire [15:0] aecp_dbg_resp_w;
	wire [15:0] aecp_dbg_drop_w;
	wire [15:0] aecp_dbg_miss_w;
	wire [3:0] aecp_dbg_fault_w;
	wire [4:0] aecp_dbg_status_w;
	wire [10:0] aecp_dbg_len_w;
	wire [2:0] aecp_dbg_rfault_w;
	wire [15:0] aecp_dbg_rerr_w;
	wire [15:0] aecp_dbg_rlane_w;
	reg [N_STREAM_OUT_P - 1:0] aecp_streaming_w;
	always @(*) begin : streaming_reduce
		if (_sv2v_0)
			;
		begin : sv2v_autoblock_13
			reg [31:0] s;
			for (s = 0; s < N_STREAM_OUT_P; s = s + 1)
				aecp_streaming_w[s] = (srp_tk_decl_state_w[s * 2+:2] == 2'd1) && srp_lstn_reg_state_w[(s * 2) + 1];
		end
	end
	wire [392:0] aecp_head_w;
	wire acmp_sb_candidate_w;
	wire aecp_sb_candidate_w;
	wire sb_pick_acmp_w;
	wire sb_pick_aecp_w;
	wire acmp_sb_accept_w;
	wire aecp_sb_accept_w;
	wire acmp_sb_done_w;
	wire aecp_sb_done_w;
	wire sb_rel_acmp_w;
	wire sb_rel_aecp_w;
	assign aecp_head_w = sv2v_cast_393(aecp_txn_w);
	assign acmp_sb_candidate_w = ((acmp_txn_valid_w && pf_ready_w) && !acmp_sb_active_r) && (acmp_is_tkr_w ? tkr_txn_ready_w : lstn_txn_ready_w);
	assign aecp_sb_candidate_w = (aecp_txn_valid_w && !aecp_sb_active_r) && (aecp_eng_ready_w || aecp_txn_ready_i);
	assign sb_pick_aecp_w = aecp_sb_candidate_w && (!acmp_sb_candidate_w || sb_prefer_aecp_r);
	assign sb_pick_acmp_w = acmp_sb_candidate_w && !sb_pick_aecp_w;
	always @(*) begin : scoreboard_admission_mux
		if (_sv2v_0)
			;
		sb_adm_req_w = sb_pick_acmp_w || sb_pick_aecp_w;
		sb_adm_class_w = 4'd0;
		sb_adm_key_w = 16'd0;
		if (sb_pick_acmp_w) begin
			sb_adm_class_w = acmp_head_w[56-:4];
			sb_adm_key_w = acmp_head_w[52-:16];
		end
		else if (sb_pick_aecp_w) begin
			sb_adm_class_w = aecp_head_w[56-:4];
			sb_adm_key_w = aecp_head_w[52-:16];
		end
	end
	assign acmp_sb_grant_w = sb_pick_acmp_w && sb_gnt_w;
	assign aecp_sb_grant_w = sb_pick_aecp_w && sb_gnt_w;
	assign acmp_sb_accept_w = acmp_sb_grant_w && acmp_sb_candidate_w;
	assign aecp_sb_accept_w = aecp_sb_grant_w && aecp_sb_candidate_w;
	assign aecp_txn_ready_w = aecp_sb_grant_w && (aecp_eng_ready_w || aecp_txn_ready_i);
	assign acmp_sb_done_w = acmp_sb_active_r && ((lstn_rxs_free_w && (lstn_rxs_free_slot_w == acmp_sb_slot_r)) || (tkr_rxs_free_w && (tkr_rxs_free_slot_w == acmp_sb_slot_r)));
	assign aecp_sb_done_w = aecp_sb_active_r && ((aecp_rxs_free_w && (aecp_rxs_free_slot_w == aecp_sb_slot_r)) || (aecp_rxs_free_i && (aecp_rxs_free_slot_i == aecp_sb_slot_r)));
	assign sb_rel_acmp_w = acmp_sb_active_r && (acmp_sb_done_pending_r || acmp_sb_done_w);
	assign sb_rel_aecp_w = (!sb_rel_acmp_w && aecp_sb_active_r) && (aecp_sb_done_pending_r || aecp_sb_done_w);
	assign sb_rel_valid_w = sb_rel_acmp_w || sb_rel_aecp_w;
	assign sb_rel_id_w = (sb_rel_acmp_w ? acmp_sb_id_r : aecp_sb_id_r);
	always @(posedge clk_i) begin : scoreboard_owners
		if (!rst_n) begin
			acmp_sb_active_r <= 1'b0;
			aecp_sb_active_r <= 1'b0;
			acmp_sb_done_pending_r <= 1'b0;
			aecp_sb_done_pending_r <= 1'b0;
			sb_prefer_aecp_r <= 1'b0;
			acmp_sb_id_r <= 3'd0;
			aecp_sb_id_r <= 3'd0;
			acmp_sb_slot_r <= 1'sb0;
			aecp_sb_slot_r <= 1'sb0;
		end
		else begin
			if (acmp_sb_accept_w) begin
				acmp_sb_active_r <= 1'b1;
				acmp_sb_done_pending_r <= 1'b0;
				sb_prefer_aecp_r <= 1'b1;
				acmp_sb_id_r <= sb_id_w;
				acmp_sb_slot_r <= acmp_head_w[56 + RXS_W_C:57];
			end
			else if (acmp_sb_done_w)
				acmp_sb_done_pending_r <= 1'b1;
			if (aecp_sb_accept_w) begin
				aecp_sb_active_r <= 1'b1;
				aecp_sb_done_pending_r <= 1'b0;
				sb_prefer_aecp_r <= 1'b0;
				aecp_sb_id_r <= sb_id_w;
				aecp_sb_slot_r <= aecp_head_w[56 + RXS_W_C:57];
			end
			else if (aecp_sb_done_w)
				aecp_sb_done_pending_r <= 1'b1;
			if (sb_rel_acmp_w) begin
				acmp_sb_active_r <= 1'b0;
				acmp_sb_done_pending_r <= 1'b0;
			end
			if (sb_rel_aecp_w) begin
				aecp_sb_active_r <= 1'b0;
				aecp_sb_done_pending_r <= 1'b0;
			end
		end
	end
	KL_aecp_engine #(
		.UCODE_HEX_P(UCODE_HEX_P),
		.DESC_BASE_P(DESC_BASE_P),
		.RESP_BASE_P(RESP_BASE_P),
		.LINE_BYTES_P(DESC_LINE_BYTES_P),
		.IDX_ENTRIES_P(DESC_IDX_ENTRIES_P),
		.NAME_ENTRIES_P(DESC_NAME_ENTRIES_P),
		.MEM_TIMEOUT_CYC_P(DESC_MEM_TMO_CYC_P),
		.N_STREAM_IN_P(N_STREAM_IN_P),
		.N_STREAM_OUT_P(N_STREAM_OUT_P),
		.N_AUDIO_UNIT_P(N_AUDIO_UNIT_P),
		.N_CLK_DOMAIN_P(N_CLK_DOMAIN_P),
		.N_CONTROL_P(N_CONTROL_P),
		.RX_SLOTS_P(RX_SLOTS_P),
		.RX_SLOT_BYTES_P(RX_SLOT_BYTES_P),
		.TX_STD_SLOTS_P(TX_STD_SLOTS_P),
		.TX_STD_BYTES_P(576),
		.TX_OVERSIZE_BYTES_P(TX_OVERSIZE_BYTES_P)
	) u_aecp(
		.clk_i(clk_i),
		.rst_n(rst_n),
		.entity_id_i(entity_id_i),
		.own_mac_i(own_mac_i),
		.txn_valid_i(aecp_txn_valid_w && aecp_sb_grant_w),
		.txn_i(aecp_txn_w),
		.txn_ready_o(aecp_eng_ready_w),
		.rxs_rd_slot_o(rxp_rd_slot_w[RXP_UCPU_C * RXS_W_C+:RXS_W_C]),
		.rxs_rd_addr_o(rxp_rd_addr_w[RXP_UCPU_C * RXA_W_C+:RXA_W_C]),
		.rxs_rd_en_o(rxp_rd_en_w[RXP_UCPU_C]),
		.rxs_rd_data_i(rxp_rd_data_w[40+:8]),
		.rxs_slot_len_i(rxp_slot_len_w[RXP_UCPU_C * RXL_W_C+:RXL_W_C]),
		.rxs_free_o(aecp_rxs_free_w),
		.rxs_free_slot_o(aecp_eng_free_slot_w),
		.txs_alloc_req_o(aecp_txs_alloc_req_w),
		.txs_oversize_o(aecp_txs_oversize_w),
		.txs_alloc_gnt_i(aecp_txs_gnt_w),
		.txs_alloc_slot_i(aecp_txs_gnt_slot_w),
		.txs_wr_slot_o(aecp_txs_wr_slot_w),
		.txs_wr_addr_o(aecp_txs_wr_addr_w),
		.txs_wr_valid_o(aecp_txs_wr_valid_w),
		.txs_wr_data_o(aecp_txs_wr_data_w),
		.txs_wr_commit_o(aecp_txs_wr_commit_w),
		.txs_wr_len_o(aecp_txs_wr_len_w),
		.txreq_valid_o(aecp_txreq_valid_w),
		.txreq_slot_o(aecp_txreq_slot_w),
		.txreq_ready_i(aecp_txreq_ready_w),
		.rgy_req_o(aecp_rgy_req_w),
		.rgy_state_o(aecp_rgy_state_w),
		.rgy_op_o(aecp_rgy_op_w),
		.rgy_eid_o(aecp_rgy_eid_w),
		.rgy_mac_o(aecp_rgy_mac_w),
		.rgy_tl_o(aecp_rgy_tl_w),
		.rgy_data_i(aecp_rgy_data_w),
		.rgy_wait_i(aecp_rgy_wait_w),
		.uns_valid_i(uns_valid_w),
		.uns_kind_i(uns_kind_w),
		.uns_desc_type_i(uns_dt_w),
		.uns_desc_index_i(uns_di_w),
		.uns_ctlr_eid_i(uns_eid_w),
		.uns_mac_i(uns_mac_w),
		.uns_seq_i(uns_seq_w),
		.uns_amap_remove_i(uns_amap_remove_w),
		.uns_amap_count_i(uns_amap_count_w),
		.uns_arg0_i(uns_arg0_w),
		.uns_arg1_i(uns_arg1_w),
		.amap_notify_busy_i(ntfy_amap_busy_w),
		.uns_done_o(uns_done_w),
		.txreq_uns_valid_o(aecp_txreq_uns_valid_w),
		.txreq_uns_ready_i(aecp_txreq_uns_ready_w),
		.mem_req_valid_o(desc_mem_req_valid_o),
		.mem_req_ready_i(desc_mem_req_ready_i),
		.mem_req_addr_o(desc_mem_req_addr_o),
		.mem_req_beats_o(desc_mem_req_beats_o),
		.mem_rsp_valid_i(desc_mem_rsp_valid_i),
		.mem_rsp_ready_o(desc_mem_rsp_ready_o),
		.mem_rsp_data_i(desc_mem_rsp_data_i),
		.mem_rsp_last_i(desc_mem_rsp_last_i),
		.mem_rsp_err_i(desc_mem_rsp_err_i),
		.rmem_req_valid_o(resp_mem_req_valid_o),
		.rmem_req_ready_i(resp_mem_req_ready_i),
		.rmem_req_addr_o(resp_mem_req_addr_o),
		.rmem_req_beats_o(resp_mem_req_beats_o),
		.rmem_rsp_valid_i(resp_mem_rsp_valid_i),
		.rmem_rsp_ready_o(resp_mem_rsp_ready_o),
		.rmem_rsp_data_i(resp_mem_rsp_data_i),
		.rmem_rsp_last_i(resp_mem_rsp_last_i),
		.rmem_rsp_err_i(resp_mem_rsp_err_i),
		.rmem_wr_valid_o(resp_mem_wr_valid_o),
		.rmem_wr_ready_i(resp_mem_wr_ready_i),
		.rmem_wr_addr_o(resp_mem_wr_addr_o),
		.rmem_wr_data_o(resp_mem_wr_data_o),
		.rmem_wr_strb_o(resp_mem_wr_strb_o),
		.rmem_wr_done_i(resp_mem_wr_done_i),
		.rmem_wr_err_i(resp_mem_wr_err_i),
		.ctr_req_o(ctr_req_o),
		.ctr_desc_type_o(ctr_desc_type_o),
		.ctr_desc_index_o(ctr_desc_index_o),
		.ctr_word_o(ctr_word_o),
		.ctr_data_i(ctr_data_i),
		.ctr_wait_i(ctr_wait_i),
		.amap_req_o(amap_req_o),
		.amap_desc_type_o(amap_desc_type_o),
		.amap_desc_index_o(amap_desc_index_o),
		.amap_map_index_o(amap_map_index_o),
		.amap_sel_o(amap_sel_o),
		.amap_rec_o(amap_rec_o),
		.amap_data_i(amap_data_i),
		.amap_wait_i(amap_wait_i),
		.amap_edit_req_o(amap_edit_req_o),
		.amap_edit_phase_o(amap_edit_phase_o),
		.amap_edit_remove_o(amap_edit_remove_o),
		.amap_edit_desc_type_o(amap_edit_desc_type_o),
		.amap_edit_desc_index_o(amap_edit_desc_index_o),
		.amap_edit_count_o(amap_edit_count_o),
		.amap_edit_rec_o(amap_edit_rec_o),
		.amap_edit_record_o(amap_edit_record_o),
		.amap_edit_value_o(amap_edit_value_o),
		.amap_edit_data_i(amap_edit_data_i),
		.amap_edit_wait_i(amap_edit_wait_i),
		.gsi_req_o(gsi_req_o),
		.gsi_kind_o(gsi_kind_o),
		.gsi_desc_type_o(gsi_desc_type_o),
		.gsi_desc_index_o(gsi_desc_index_o),
		.gsi_sel_o(gsi_sel_o),
		.gsi_ord_o(gsi_ord_o),
		.gsi_prop_fmt_o(gsi_prop_fmt_o),
		.gsi_data_i(gsi_data_i),
		.gsi_wait_i(gsi_wait_i),
		.strm_bound_i(bound_hold_r),
		.strm_started_i(aecp_strm_started_o),
		.strm_streaming_i(aecp_streaming_w),
		.lock_held_i(ntfy_lock_held_w),
		.lock_ctlr_i(ntfy_lock_ctlr_w),
		.eff_commit_o(aecp_eff_commit_nc_w),
		.eff_nvm_mark_o(aecp_nvm_mark_o),
		.eff_nvm_stb_o(aecp_nvm_stb_o),
		.eff_notify_class_o(aecp_eff_notify_cls_nc_w),
		.eff_notify_stb_o(aecp_eff_notify_stb_nc_w),
		.eff_notify_type_o(aecp_eff_notify_type_w),
		.eff_notify_index_o(aecp_eff_notify_index_w),
		.eff_notify_arg0_o(aecp_eff_notify_arg0_w),
		.eff_notify_arg1_o(aecp_eff_notify_arg1_w),
		.eff_notify_excl_eid_o(aecp_eff_notify_excl_w),
		.dbg_busy_o(aecp_dbg_busy_nc_w),
		.dbg_cmd_cnt_o(aecp_dbg_cmd_w),
		.dbg_resp_cnt_o(aecp_dbg_resp_w),
		.dbg_drop_cnt_o(aecp_dbg_drop_w),
		.dbg_status_o(aecp_dbg_status_w),
		.dbg_len_o(aecp_dbg_len_w),
		.dbg_img_valid_o(aecp_dbg_img_valid_w),
		.dbg_img_fault_o(aecp_dbg_fault_w),
		.dbg_locate_miss_o(aecp_dbg_miss_w),
		.dbg_resp_fault_o(aecp_dbg_rfault_w),
		.dbg_resp_err_o(aecp_dbg_rerr_w),
		.dbg_resp_lane_o(aecp_dbg_rlane_w),
		.dyn_cur_config_o(aecp_cur_config_o),
		.dyn_identify_o(aecp_identify_o),
		.dyn_clk_src_index_o(aecp_clk_src_index_o),
		.strm_set_valid_o(strm_set_valid_w),
		.strm_set_index_o(strm_set_index_w),
		.strm_set_val_o(strm_set_val_w),
		.strm_set_ready_i(strm_set_ready_w),
		.strm_set_error_i(strm_set_error_w),
		.dyn_pt_offset_o(aecp_pt_offset_o),
		.dyn_pt_offset_v_o(aecp_pt_offset_v_o),
		.dyn_fmt_in_o(aecp_fmt_in_o),
		.dyn_fmt_in_v_o(aecp_fmt_in_v_o),
		.dyn_fmt_out_o(aecp_fmt_out_o),
		.dyn_fmt_out_v_o(aecp_fmt_out_v_o),
		.dyn_dirty_o(aecp_dyn_dirty_o)
	);
	assign aecp_rxs_free_slot_w = aecp_eng_free_slot_w;
	KL_aecp_notify #(
		.N_CTRL_P(pp_pkg_PP_N_CTRL_C),
		.N_STREAM_IN_P(N_STREAM_IN_P),
		.N_STREAM_OUT_P(N_STREAM_OUT_P),
		.TL_TIMEOUT_MS_P(REG_TL_TIMEOUT_MS_P),
		.LOCK_TIMEOUT_MS_P(LOCK_TIMEOUT_MS_P),
		.TMR_SLOTS_P(TMR_SLOTS_C),
		.TMR_REGMON_BASE_P(TMR_MAP_C[287-:32]),
		.TMR_LOCK_SLOT_P(TMR_MAP_C[223-:32])
	) u_notify(
		.clk_i(clk_i),
		.rst_n(rst_n),
		.rgy_req_i(aecp_rgy_req_w),
		.rgy_state_i(aecp_rgy_state_w),
		.rgy_op_i(aecp_rgy_op_w),
		.rgy_eid_i(aecp_rgy_eid_w),
		.rgy_mac_i(aecp_rgy_mac_w),
		.rgy_tl_i(aecp_rgy_tl_w),
		.rgy_data_o(aecp_rgy_data_w),
		.rgy_wait_o(aecp_rgy_wait_w),
		.ev_stri_in_i(ntfy_stri_in_w),
		.ev_stri_out_i(ntfy_stri_out_w),
		.ev_avb_i(((gm_change_i || srp_evt_domain_change_w) || (link_up_i != link_q_r)) || gsi_avb_chg_i),
		.ev_asp_i(gsi_asp_chg_i),
		.ev_amap_i(aecp_eff_notify_stb_nc_w && (aecp_eff_notify_cls_nc_w == 4'd6)),
		.ev_amap_remove_i(amap_edit_remove_o),
		.ev_amap_type_i(amap_edit_desc_type_o),
		.ev_amap_index_i(amap_edit_desc_index_o),
		.ev_amap_count_i(amap_edit_count_o),
		.ev_amap_excl_eid_i(aecp_rgy_eid_w),
		.ev_ctr_i(ctr_change_i),
		.ev_ctr_type_i(ctr_change_desc_type_i),
		.ev_ctr_index_i(ctr_change_desc_index_i),
		.ev_cmd_i(aecp_eff_notify_stb_nc_w),
		.ev_cmd_class_i(aecp_eff_notify_cls_nc_w),
		.ev_cmd_type_i(aecp_eff_notify_type_w),
		.ev_cmd_index_i(aecp_eff_notify_index_w),
		.ev_cmd_arg0_i(aecp_eff_notify_arg0_w),
		.ev_cmd_arg1_i(aecp_eff_notify_arg1_w),
		.ev_cmd_excl_eid_i(aecp_eff_notify_excl_w),
		.rx_cmd_valid_i((v_hdr_valid_w && ((((((v_hdr_msg_type_w == 4'd0) || (v_hdr_msg_type_w == 4'd2)) || (v_hdr_msg_type_w == 4'd4)) || (v_hdr_msg_type_w == 4'd6)) || (v_hdr_msg_type_w == 4'd8)) || (v_hdr_msg_type_w == 4'd14))) && (((v_hdr_protocol_w == 3'd2) || (v_hdr_protocol_w == 3'd3)) || (v_hdr_protocol_w == 3'd4))),
		.rx_cmd_eid_i(v_hdr_ctlr_eid_w),
		.rx_cmd_mac_i(v_hdr_src_mac_w),
		.prng_draw_req_o(ntfy_prng_req_w),
		.prng_draw_kind_o(ntfy_prng_kind_w),
		.prng_draw_busy_i(ntfy_prng_busy_w),
		.prng_draw_valid_i(ntfy_prng_valid_w),
		.prng_draw_ms_i(prng_ms_w),
		.ca_valid_o(ntfy_ca_valid_w),
		.ca_owner_o(ntfy_ca_owner_w),
		.ca_ctlr_eid_o(ntfy_ca_eid_w),
		.ca_mac_o(ntfy_ca_mac_w),
		.ca_ready_i(ntfy_ca_ready_w),
		.ca_cancel_valid_o(ntfy_ca_cancel_valid_w),
		.ca_cancel_owner_o(ntfy_ca_cancel_owner_w),
		.ca_rsp_valid_i(org_rt_valid_w),
		.ca_rsp_owner_i(org_rt_owner_w),
		.ca_fail_valid_i(org_fail_valid_w),
		.ca_fail_owner_i(org_fail_owner_w),
		.uns_valid_o(uns_valid_w),
		.uns_kind_o(uns_kind_w),
		.uns_desc_type_o(uns_dt_w),
		.uns_desc_index_o(uns_di_w),
		.uns_ctlr_eid_o(uns_eid_w),
		.uns_mac_o(uns_mac_w),
		.uns_seq_o(uns_seq_w),
		.uns_amap_remove_o(uns_amap_remove_w),
		.uns_amap_count_o(uns_amap_count_w),
		.uns_arg0_o(uns_arg0_w),
		.uns_arg1_o(uns_arg1_w),
		.uns_done_i(uns_done_w),
		.amap_busy_o(ntfy_amap_busy_w),
		.lock_held_o(ntfy_lock_held_w),
		.lock_ctlr_o(ntfy_lock_ctlr_w),
		.tmr_arm_valid_o(ntfy_arm_valid_w),
		.tmr_arm_cancel_o(ntfy_arm_cancel_w),
		.tmr_arm_slot_o(ntfy_arm_slot_w),
		.tmr_arm_owner_o(ntfy_arm_owner_w),
		.tmr_arm_deadline_ms_o(ntfy_arm_deadline_w),
		.now_ms_i(now_ms_w),
		.tmr_exp_valid_i(exp_valid_w),
		.tmr_exp_slot_i(exp_slot_w),
		.tmr_exp_owner_i(exp_owner_w),
		.mon_arm_valid_o(ntfy_mon_arm_valid_w),
		.mon_arm_cancel_o(ntfy_mon_arm_cancel_w),
		.mon_arm_slot_o(ntfy_mon_arm_slot_w),
		.mon_arm_owner_o(ntfy_mon_arm_owner_w),
		.mon_arm_deadline_ms_o(ntfy_mon_arm_deadline_w),
		.dbg_reg_cnt_o(ntfy_reg_cnt_nc_w),
		.dbg_uns_cnt_o(ntfy_uns_cnt_nc_w),
		.dbg_coalesce_o(ntfy_coalesce_nc_w)
	);
	localparam [31:0] TXC_ADP_C = 0;
	localparam [31:0] TXC_LSTN_C = 1;
	localparam [31:0] TXC_SRP_C = 2;
	localparam [31:0] TXC_TKB_C = 3;
	localparam [31:0] TXC_AECP_C = 4;
	localparam [31:0] TXC_MAAP_C = 5;
	localparam [31:0] TXC_CA_C = 6;
	localparam [31:0] TXC_N_C = 7;
	wire [6:0] txc_req_w;
	reg [6:0] txc_pend_r;
	reg [2:0] txc_owner_r;
	reg txc_locked_r;
	reg txc_alloc_wait_r;
	reg pool_alloc_req_w;
	wire pool_oversize_w;
	wire pool_alloc_gnt_w;
	wire [TXS_W_C - 1:0] pool_alloc_slot_w;
	reg pool_wr_valid_w;
	reg pool_wr_commit_w;
	reg [TXS_W_C - 1:0] pool_wr_slot_w;
	reg [TXA_W_C - 1:0] pool_wr_addr_w;
	reg [TXA_W_C - 1:0] pool_wr_len_w;
	reg [7:0] pool_wr_data_w;
	wire [6:0] txc_commit_w;
	assign txc_req_w = {ca_txs_alloc_req_w, maapeng_txs_alloc_req_w, aecp_txs_alloc_req_w, tkb_alloc_req_w, srp_txs_alloc_req_w, lstn_txs_alloc_req_w, adp_txs_alloc_req_w};
	assign txc_commit_w = {ca_txs_wr_commit_w, maapeng_txs_wr_commit_w, aecp_txs_wr_commit_w, tkb_st_r == 3'd3, srp_txs_wr_commit_w, lstn_txs_wr_commit_w, adp_txs_wr_commit_w};
	always @(posedge clk_i) begin : txc_arbiter
		if (!rst_n) begin
			txc_pend_r <= 1'sb0;
			txc_owner_r <= 3'd0;
			txc_locked_r <= 1'b0;
			txc_alloc_wait_r <= 1'b0;
		end
		else begin
			begin : sv2v_autoblock_14
				reg [31:0] i;
				for (i = 0; i < TXC_N_C; i = i + 1)
					if (txc_req_w[i])
						txc_pend_r[i] <= 1'b1;
			end
			if (!txc_locked_r) begin
				txc_alloc_wait_r <= 1'b0;
				if (txc_pend_r[TXC_LSTN_C] || txc_req_w[TXC_LSTN_C]) begin
					txc_owner_r <= sv2v_cast_3(TXC_LSTN_C);
					txc_locked_r <= 1'b1;
				end
				else if (txc_pend_r[TXC_TKB_C] || txc_req_w[TXC_TKB_C]) begin
					txc_owner_r <= sv2v_cast_3(TXC_TKB_C);
					txc_locked_r <= 1'b1;
				end
				else if (txc_pend_r[TXC_AECP_C] || txc_req_w[TXC_AECP_C]) begin
					txc_owner_r <= sv2v_cast_3(TXC_AECP_C);
					txc_locked_r <= 1'b1;
				end
				else if (txc_pend_r[TXC_CA_C] || txc_req_w[TXC_CA_C]) begin
					txc_owner_r <= sv2v_cast_3(TXC_CA_C);
					txc_locked_r <= 1'b1;
				end
				else if (txc_pend_r[TXC_SRP_C] || txc_req_w[TXC_SRP_C]) begin
					txc_owner_r <= sv2v_cast_3(TXC_SRP_C);
					txc_locked_r <= 1'b1;
				end
				else if (txc_pend_r[TXC_ADP_C] || txc_req_w[TXC_ADP_C]) begin
					txc_owner_r <= sv2v_cast_3(TXC_ADP_C);
					txc_locked_r <= 1'b1;
				end
				else if (txc_pend_r[TXC_MAAP_C] || txc_req_w[TXC_MAAP_C]) begin
					txc_owner_r <= sv2v_cast_3(TXC_MAAP_C);
					txc_locked_r <= 1'b1;
				end
			end
			else begin
				if (txc_alloc_wait_r)
					txc_alloc_wait_r <= 1'b0;
				else if (pool_alloc_req_w)
					txc_alloc_wait_r <= 1'b1;
				if (pool_alloc_gnt_w)
					txc_pend_r[txc_owner_r] <= 1'b0;
				if (txc_commit_w[txc_owner_r]) begin
					txc_locked_r <= 1'b0;
					txc_alloc_wait_r <= 1'b0;
				end
				if ((txc_owner_r == sv2v_cast_3(TXC_CA_C)) && ca_txs_abort_w) begin
					txc_pend_r[TXC_CA_C] <= 1'b0;
					txc_locked_r <= 1'b0;
					txc_alloc_wait_r <= 1'b0;
				end
			end
		end
	end
	assign pool_oversize_w = (txc_locked_r && (txc_owner_r == sv2v_cast_3(TXC_AECP_C))) && aecp_txs_oversize_w;
	function automatic signed [TXA_W_C - 1:0] sv2v_cast_FE6CB_signed;
		input reg signed [TXA_W_C - 1:0] inp;
		sv2v_cast_FE6CB_signed = inp;
	endfunction
	always @(*) begin : txc_mux
		if (_sv2v_0)
			;
		pool_alloc_req_w = 1'b0;
		pool_wr_valid_w = 1'b0;
		pool_wr_commit_w = 1'b0;
		pool_wr_slot_w = 1'sb0;
		pool_wr_addr_w = 1'sb0;
		pool_wr_data_w = 8'd0;
		pool_wr_len_w = 1'sb0;
		if (txc_locked_r) begin
			(* full_case, parallel_case *)
			case (txc_owner_r)
				sv2v_cast_3(TXC_AECP_C): begin
					pool_alloc_req_w = aecp_txs_alloc_req_w;
					pool_wr_valid_w = aecp_txs_wr_valid_w;
					pool_wr_commit_w = aecp_txs_wr_commit_w;
					pool_wr_slot_w = aecp_txs_wr_slot_w;
					pool_wr_addr_w = aecp_txs_wr_addr_w;
					pool_wr_data_w = aecp_txs_wr_data_w;
					pool_wr_len_w = aecp_txs_wr_len_w;
				end
				sv2v_cast_3(TXC_CA_C): begin
					pool_alloc_req_w = ca_txs_alloc_req_w;
					pool_wr_valid_w = ca_txs_wr_valid_w;
					pool_wr_commit_w = ca_txs_wr_commit_w;
					pool_wr_slot_w = ca_txs_wr_slot_w;
					pool_wr_addr_w = ca_txs_wr_addr_w;
					pool_wr_data_w = ca_txs_wr_data_w;
					pool_wr_len_w = ca_txs_wr_len_w;
				end
				sv2v_cast_3(TXC_ADP_C): begin
					pool_alloc_req_w = adp_txs_alloc_req_w;
					pool_wr_valid_w = adp_txs_wr_valid_w;
					pool_wr_commit_w = adp_txs_wr_commit_w;
					pool_wr_slot_w = adp_txs_wr_slot_w;
					pool_wr_addr_w = adp_txs_wr_addr_w;
					pool_wr_data_w = adp_txs_wr_data_w;
					pool_wr_len_w = adp_txs_wr_len_w;
				end
				sv2v_cast_3(TXC_LSTN_C): begin
					pool_alloc_req_w = lstn_txs_alloc_req_w;
					pool_wr_valid_w = lstn_txs_wr_valid_w;
					pool_wr_commit_w = lstn_txs_wr_commit_w;
					pool_wr_slot_w = lstn_txs_wr_slot_w;
					pool_wr_addr_w = lstn_txs_wr_addr_w;
					pool_wr_data_w = lstn_txs_wr_data_w;
					pool_wr_len_w = lstn_txs_wr_len_w;
				end
				sv2v_cast_3(TXC_SRP_C): begin
					pool_alloc_req_w = srp_txs_alloc_req_w;
					pool_wr_valid_w = srp_txs_wr_valid_w;
					pool_wr_commit_w = srp_txs_wr_commit_w;
					pool_wr_slot_w = srp_txs_wr_slot_w;
					pool_wr_addr_w = srp_txs_wr_addr_w;
					pool_wr_data_w = srp_txs_wr_data_w;
					pool_wr_len_w = srp_txs_wr_len_w;
				end
				sv2v_cast_3(TXC_MAAP_C): begin
					pool_alloc_req_w = maapeng_txs_alloc_req_w;
					pool_wr_valid_w = maapeng_txs_wr_valid_w;
					pool_wr_commit_w = maapeng_txs_wr_commit_w;
					pool_wr_slot_w = maapeng_txs_wr_slot_w;
					pool_wr_addr_w = maapeng_txs_wr_addr_w;
					pool_wr_data_w = maapeng_txs_wr_data_w;
					pool_wr_len_w = maapeng_txs_wr_len_w;
				end
				default: begin
					pool_alloc_req_w = tkb_alloc_req_w;
					pool_wr_valid_w = tkb_st_r == 3'd2;
					pool_wr_commit_w = tkb_st_r == 3'd3;
					pool_wr_slot_w = tkb_slot_r;
					pool_wr_addr_w = {5'd0, tkb_bidx_r};
					pool_wr_data_w = tkb_pdu_byte_w;
					pool_wr_len_w = sv2v_cast_FE6CB_signed(56);
				end
			endcase
			if (txc_alloc_wait_r)
				pool_alloc_req_w = 1'b0;
		end
	end
	assign adp_txs_gnt_w = (txc_locked_r && (txc_owner_r == sv2v_cast_3(TXC_ADP_C))) && pool_alloc_gnt_w;
	assign lstn_txs_gnt_w = (txc_locked_r && (txc_owner_r == sv2v_cast_3(TXC_LSTN_C))) && pool_alloc_gnt_w;
	assign srp_txs_gnt_w = (txc_locked_r && (txc_owner_r == sv2v_cast_3(TXC_SRP_C))) && pool_alloc_gnt_w;
	assign tkb_gnt_w = (txc_locked_r && (txc_owner_r == sv2v_cast_3(TXC_TKB_C))) && pool_alloc_gnt_w;
	assign aecp_txs_gnt_w = (txc_locked_r && (txc_owner_r == sv2v_cast_3(TXC_AECP_C))) && pool_alloc_gnt_w;
	assign maapeng_txs_gnt_w = (txc_locked_r && (txc_owner_r == sv2v_cast_3(TXC_MAAP_C))) && pool_alloc_gnt_w;
	assign ca_txs_gnt_w = (txc_locked_r && (txc_owner_r == sv2v_cast_3(TXC_CA_C))) && pool_alloc_gnt_w;
	assign adp_txs_gnt_slot_w = pool_alloc_slot_w;
	assign lstn_txs_gnt_slot_w = pool_alloc_slot_w;
	assign srp_txs_gnt_slot_w = pool_alloc_slot_w;
	assign tkb_gnt_slot_w = pool_alloc_slot_w;
	assign aecp_txs_gnt_slot_w = pool_alloc_slot_w;
	assign maapeng_txs_gnt_slot_w = pool_alloc_slot_w;
	assign ca_txs_gnt_slot_w = pool_alloc_slot_w;
	wire ser_req_w;
	wire ser_valid_w;
	wire ser_last_w;
	wire ser_ready_w;
	wire [TXS_W_C - 1:0] ser_slot_w;
	wire [7:0] ser_data_w;
	wire [TX_STD_SLOTS_P:0] txs_ready_nc_w;
	wire [$clog2(TX_STD_SLOTS_P + 2) - 1:0] txs_free_w;
	wire txs_release_valid_w;
	wire [TXS_W_C - 1:0] txs_release_slot_w;
	function automatic [TXS_W_C - 1:0] sv2v_cast_53FF9;
		input reg [TXS_W_C - 1:0] inp;
		sv2v_cast_53FF9 = inp;
	endfunction
	KL_pp_release_merge #(.N_SLOTS_P(TX_STD_SLOTS_P + 1)) u_release_merge(
		.clk_i(clk_i),
		.rst_n(rst_n),
		.a_valid_i(org_release_valid_w),
		.a_slot_i(sv2v_cast_53FF9(org_release_slot_w)),
		.b_valid_i(ca_cancel_release_valid_w),
		.b_slot_i(ca_cancel_release_slot_w),
		.release_valid_o(txs_release_valid_w),
		.release_slot_o(txs_release_slot_w)
	);
	KL_pp_tx_slots #(
		.TX_STD_SLOTS_P(TX_STD_SLOTS_P),
		.TX_STD_BYTES_P(576),
		.TX_OVERSIZE_BYTES_P(TX_OVERSIZE_BYTES_P)
	) u_tx_slots(
		.clk_i(clk_i),
		.rst_n(rst_n),
		.alloc_req_i(pool_alloc_req_w),
		.oversize_i(pool_oversize_w),
		.alloc_gnt_o(pool_alloc_gnt_w),
		.alloc_slot_o(pool_alloc_slot_w),
		.wr_slot_i(pool_wr_slot_w),
		.wr_addr_i(pool_wr_addr_w),
		.wr_valid_i(pool_wr_valid_w),
		.wr_data_i(pool_wr_data_w),
		.wr_commit_i(pool_wr_commit_w),
		.wr_len_i(pool_wr_len_w),
		.hold_valid_i(org_hold_valid_w),
		.hold_slot_i(org_hold_slot_w),
		.release_valid_i(txs_release_valid_w),
		.release_slot_i(txs_release_slot_w),
		.ser_req_i(ser_req_w),
		.ser_slot_i(ser_slot_w),
		.ser_valid_o(ser_valid_w),
		.ser_data_o(ser_data_w),
		.ser_last_o(ser_last_w),
		.ser_ready_i(ser_ready_w),
		.slots_ready_o(txs_ready_nc_w),
		.slots_free_o(txs_free_w)
	);
	reg [(8 * TXS_W_C) - 1:0] laneq_adp_r;
	reg [(8 * TXS_W_C) - 1:0] laneq_acmp_r;
	reg [(8 * TXS_W_C) - 1:0] laneq_org_next_w;
	reg [3:0] laneq_adp_cnt_r;
	reg [3:0] laneq_acmp_cnt_r;
	reg [3:0] laneq_org_cnt_r;
	wire [3:0] laneq_adp_mid_w;
	wire [3:0] laneq_acmp_mid_w;
	reg [3:0] laneq_org_next_cnt_w;
	wire laneq_adp_push_w;
	wire laneq_acmp_push_w;
	wire laneq_org_drop_w;
	wire laneq_org_pop_w;
	wire laneq_org_release_head_w;
	wire laneq_org_withdraw_head_w;
	wire [7:0] arb_req_w;
	wire [(LANE_N_C * TXS_W_C) - 1:0] arb_slot_w;
	wire [127:0] arb_gnt_cnt_w;
	assign laneq_adp_mid_w = laneq_adp_cnt_r - (arb_gnt_w[LANE_ADP_C] ? 4'd1 : 4'd0);
	assign laneq_acmp_mid_w = laneq_acmp_cnt_r - (arb_gnt_w[LANE_ACMP_C] ? 4'd1 : 4'd0);
	assign laneq_org_release_head_w = ((laneq_org_cnt_r != 4'd0) && txs_release_valid_w) && (txs_release_slot_w == laneq_org_r[0+:TXS_W_C]);
	assign laneq_org_withdraw_head_w = (laneq_org_cnt_r != 4'd0) && org_withdraw_slot_mask_w[laneq_org_r[0+:TXS_W_C]];
	assign laneq_org_drop_w = (laneq_org_cnt_r != 4'd0) && ((!txs_ready_nc_w[laneq_org_r[0+:TXS_W_C]] || laneq_org_release_head_w) || laneq_org_withdraw_head_w);
	assign laneq_org_pop_w = arb_gnt_w[LANE_ORIG_C] || laneq_org_drop_w;
	assign laneq_adp_push_w = adp_txreq_valid_w && (laneq_adp_mid_w != 4'd8);
	assign laneq_acmp_push_w = lstn_txreq_valid_w && (laneq_acmp_mid_w != 4'd8);
	function automatic [3:0] sv2v_cast_4;
		input reg [3:0] inp;
		sv2v_cast_4 = inp;
	endfunction
	always @(*) begin : originator_queue_next
		if (_sv2v_0)
			;
		laneq_org_next_w = 1'sb0;
		laneq_org_next_cnt_w = 4'd0;
		begin : sv2v_autoblock_15
			reg [31:0] i;
			for (i = 0; i < 8; i = i + 1)
				if ((((sv2v_cast_4(i) < laneq_org_cnt_r) && !((i == 0) && laneq_org_pop_w)) && !(txs_release_valid_w && (laneq_org_r[i * TXS_W_C+:TXS_W_C] == txs_release_slot_w))) && !org_withdraw_slot_mask_w[laneq_org_r[i * TXS_W_C+:TXS_W_C]]) begin
					laneq_org_next_w[laneq_org_next_cnt_w[2:0] * TXS_W_C+:TXS_W_C] = laneq_org_r[i * TXS_W_C+:TXS_W_C];
					laneq_org_next_cnt_w = laneq_org_next_cnt_w + 4'd1;
				end
		end
		if ((org_send_valid_w || org_resend_valid_w) && (laneq_org_next_cnt_w != 4'd8)) begin
			laneq_org_next_w[laneq_org_next_cnt_w[2:0] * TXS_W_C+:TXS_W_C] = (org_resend_valid_w ? org_resend_slot_w : org_send_slot_w);
			laneq_org_next_cnt_w = laneq_org_next_cnt_w + 4'd1;
		end
	end
	always @(posedge clk_i) begin : lane_queues
		if (!rst_n) begin
			laneq_adp_r <= 1'sb0;
			laneq_acmp_r <= 1'sb0;
			laneq_org_r <= 1'sb0;
			laneq_adp_cnt_r <= 4'd0;
			laneq_acmp_cnt_r <= 4'd0;
			laneq_org_cnt_r <= 4'd0;
		end
		else begin
			if (arb_gnt_w[LANE_ADP_C]) begin : sv2v_autoblock_16
				reg [31:0] i;
				for (i = 0; i < 7; i = i + 1)
					laneq_adp_r[i * TXS_W_C+:TXS_W_C] <= laneq_adp_r[(i + 1) * TXS_W_C+:TXS_W_C];
			end
			if (laneq_adp_push_w)
				laneq_adp_r[laneq_adp_mid_w[2:0] * TXS_W_C+:TXS_W_C] <= adp_txreq_slot_w;
			laneq_adp_cnt_r <= laneq_adp_mid_w + (laneq_adp_push_w ? 4'd1 : 4'd0);
			if (arb_gnt_w[LANE_ACMP_C]) begin : sv2v_autoblock_17
				reg [31:0] i;
				for (i = 0; i < 7; i = i + 1)
					laneq_acmp_r[i * TXS_W_C+:TXS_W_C] <= laneq_acmp_r[(i + 1) * TXS_W_C+:TXS_W_C];
			end
			if (laneq_acmp_push_w)
				laneq_acmp_r[laneq_acmp_mid_w[2:0] * TXS_W_C+:TXS_W_C] <= lstn_txreq_slot_w;
			laneq_acmp_cnt_r <= laneq_acmp_mid_w + (laneq_acmp_push_w ? 4'd1 : 4'd0);
			laneq_org_r <= laneq_org_next_w;
			laneq_org_cnt_r <= laneq_org_next_cnt_w;
		end
	end
	assign arb_req_w[LANE_AECP_SOL_C] = aecp_txreq_valid_w;
	assign arb_req_w[LANE_AECP_UNS_C] = aecp_txreq_uns_valid_w;
	assign arb_req_w[LANE_ACMP_C] = laneq_acmp_cnt_r != 4'd0;
	assign arb_req_w[LANE_ADP_C] = laneq_adp_cnt_r != 4'd0;
	assign arb_req_w[LANE_SRP_C] = srp_txreq_valid_w;
	assign arb_req_w[LANE_TKRSP_C] = tkb_lane_valid_r;
	assign arb_req_w[LANE_MAAP_C] = maapeng_txreq_valid_w;
	assign arb_req_w[LANE_ORIG_C] = (((laneq_org_cnt_r != 4'd0) && txs_ready_nc_w[laneq_org_r[0+:TXS_W_C]]) && !laneq_org_release_head_w) && !laneq_org_withdraw_head_w;
	assign arb_slot_w[LANE_AECP_SOL_C * TXS_W_C+:TXS_W_C] = aecp_txreq_slot_w;
	assign arb_slot_w[LANE_AECP_UNS_C * TXS_W_C+:TXS_W_C] = aecp_txreq_slot_w;
	assign arb_slot_w[LANE_ACMP_C * TXS_W_C+:TXS_W_C] = laneq_acmp_r[0+:TXS_W_C];
	assign arb_slot_w[LANE_ADP_C * TXS_W_C+:TXS_W_C] = laneq_adp_r[0+:TXS_W_C];
	assign arb_slot_w[LANE_SRP_C * TXS_W_C+:TXS_W_C] = srp_txreq_slot_w;
	assign arb_slot_w[LANE_TKRSP_C * TXS_W_C+:TXS_W_C] = tkb_slot_r;
	assign arb_slot_w[LANE_MAAP_C * TXS_W_C+:TXS_W_C] = maapeng_txreq_slot_w;
	assign arb_slot_w[LANE_ORIG_C * TXS_W_C+:TXS_W_C] = laneq_org_r[0+:TXS_W_C];
	assign maapeng_txreq_ready_w = arb_gnt_w[LANE_MAAP_C];
	assign srp_txreq_ready_w = arb_gnt_w[LANE_SRP_C];
	assign aecp_txreq_ready_w = arb_gnt_w[LANE_AECP_SOL_C];
	assign aecp_txreq_uns_ready_w = arb_gnt_w[LANE_AECP_UNS_C];
	assign tkb_lane_gnt_w = arb_gnt_w[LANE_TKRSP_C];
	wire arb_tx_valid_w;
	wire arb_tx_sof_w;
	wire arb_tx_eof_w;
	reg arb_tx_ready_w;
	wire [7:0] arb_tx_data_w;
	wire arb_start_abort_w;
	assign arb_start_abort_w = org_withdraw_slot_mask_w[ser_slot_w] || (txs_release_valid_w && (txs_release_slot_w == ser_slot_w));
	KL_pp_tx_arbiter #(
		.N_REQ_P(LANE_N_C),
		.PRIO_MAP_P(16'h76c9),
		.SOLICITED_MASK_P(8'b10100101),
		.TX_STD_SLOTS_P(TX_STD_SLOTS_P)
	) u_tx_arbiter(
		.clk_i(clk_i),
		.rst_n(rst_n),
		.tick_ms_i(tick_ms_w),
		.req_valid_i(arb_req_w),
		.tx_slot_i(arb_slot_w),
		.start_abort_i(arb_start_abort_w),
		.gnt_o(arb_gnt_w),
		.gnt_count_o(arb_gnt_cnt_w),
		.ser_req_o(ser_req_w),
		.ser_slot_o(ser_slot_w),
		.ser_valid_i(ser_valid_w),
		.ser_data_i(ser_data_w),
		.ser_last_i(ser_last_w),
		.ser_ready_o(ser_ready_w),
		.tx_valid_o(arb_tx_valid_w),
		.tx_sof_o(arb_tx_sof_w),
		.tx_data_o(arb_tx_data_w),
		.tx_eof_o(arb_tx_eof_w),
		.tx_ready_i(arb_tx_ready_w)
	);
	reg [1:0] sh_st_r;
	reg sh_need_r;
	reg [3:0] sh_idx_r;
	wire [111:0] sh_hdr_w;
	wire [7:0] sh_byte_w;
	assign sh_hdr_w = {48'h91e0f0010000, own_mac_i, 16'h22f0};
	assign sh_byte_w = sh_hdr_w[7'd104 - {sh_idx_r, 3'b000}+:8];
	always @(posedge clk_i) begin : prepend_shim
		if (!rst_n) begin
			sh_st_r <= 2'd0;
			sh_need_r <= 1'b0;
			sh_idx_r <= 4'd0;
		end
		else begin
			if (|arb_gnt_w)
				sh_need_r <= arb_gnt_w[LANE_ACMP_C] || arb_gnt_w[LANE_TKRSP_C];
			(* full_case, parallel_case *)
			case (sh_st_r)
				2'd0:
					if (arb_tx_valid_w && sh_need_r) begin
						if (tx_ready_i) begin
							sh_idx_r <= 4'd1;
							sh_st_r <= 2'd1;
						end
					end
				2'd1:
					if (tx_ready_i) begin
						if (sh_idx_r == 4'd13)
							sh_st_r <= 2'd2;
						else
							sh_idx_r <= sh_idx_r + 4'd1;
					end
				2'd2:
					if ((arb_tx_valid_w && arb_tx_eof_w) && tx_ready_i) begin
						sh_st_r <= 2'd0;
						sh_idx_r <= 4'd0;
					end
				default: sh_st_r <= 2'd0;
			endcase
		end
	end
	always @(*) begin : shim_stream
		if (_sv2v_0)
			;
		(* full_case, parallel_case *)
		case (sh_st_r)
			2'd0:
				if (arb_tx_valid_w && sh_need_r) begin
					tx_valid_o = 1'b1;
					tx_sof_o = 1'b1;
					tx_data_o = sh_hdr_w[111:104];
					tx_eof_o = 1'b0;
					arb_tx_ready_w = 1'b0;
				end
				else begin
					tx_valid_o = arb_tx_valid_w;
					tx_sof_o = arb_tx_sof_w;
					tx_data_o = arb_tx_data_w;
					tx_eof_o = arb_tx_eof_w;
					arb_tx_ready_w = tx_ready_i;
				end
			2'd1: begin
				tx_valid_o = 1'b1;
				tx_sof_o = 1'b0;
				tx_data_o = sh_byte_w;
				tx_eof_o = 1'b0;
				arb_tx_ready_w = 1'b0;
			end
			2'd2: begin
				tx_valid_o = arb_tx_valid_w;
				tx_sof_o = 1'b0;
				tx_data_o = arb_tx_data_w;
				tx_eof_o = arb_tx_eof_w;
				arb_tx_ready_w = tx_ready_i;
			end
			default: begin
				tx_valid_o = arb_tx_valid_w;
				tx_sof_o = arb_tx_sof_w;
				tx_data_o = arb_tx_data_w;
				tx_eof_o = arb_tx_eof_w;
				arb_tx_ready_w = tx_ready_i;
			end
		endcase
	end
	wire sp_img_req_w;
	wire sp_img_we_nc_w;
	wire [15:0] sp_img_addr_nc_w;
	wire [31:0] sp_img_wdata_nc_w;
	reg sp_img_rvalid_r;
	wire sp_dbg_req_w;
	wire [15:0] sp_dbg_addr_nc_w;
	reg sp_dbg_rvalid_r;
	wire sp_snap_req_w;
	wire [15:0] sp_snap_addr_w;
	reg [31:0] sp_snap_rdata_r;
	reg sp_snap_rvalid_r;
	wire sp_ctrl_req_w;
	wire sp_ctrl_we_w;
	wire [7:0] sp_ctrl_addr_w;
	wire [31:0] sp_ctrl_wdata_w;
	reg [31:0] sp_ctrl_rdata_r;
	reg sp_ctrl_rvalid_r;
	wire sp_trace_req_w;
	wire [15:0] sp_trace_addr_w;
	reg sp_trace_rvalid_r;
	wire sp_fw_req_nc_w;
	wire sp_fw_we_nc_w;
	wire [15:0] sp_fw_addr_nc_w;
	wire [31:0] sp_fw_wdata_nc_w;
	KL_pp_side_port #(.EN_FW_ASSIST_P(1'b0)) u_side_port(
		.clk_i(clk_i),
		.rst_n(rst_n),
		.entity_enable_i(entity_enable_i),
		.req_valid_i(host_req_valid_i),
		.we_i(host_we_i),
		.addr_i(host_addr_i),
		.wdata_i(host_wdata_i),
		.rdata_o(host_rdata_o),
		.rvalid_o(host_rvalid_o),
		.err_o(host_err_o),
		.img_req_o(sp_img_req_w),
		.img_we_o(sp_img_we_nc_w),
		.img_addr_o(sp_img_addr_nc_w),
		.img_wdata_o(sp_img_wdata_nc_w),
		.img_rdata_i(32'd0),
		.img_rvalid_i(sp_img_rvalid_r),
		.dbg_req_o(sp_dbg_req_w),
		.dbg_addr_o(sp_dbg_addr_nc_w),
		.dbg_rdata_i(32'd0),
		.dbg_rvalid_i(sp_dbg_rvalid_r),
		.snap_req_o(sp_snap_req_w),
		.snap_addr_o(sp_snap_addr_w),
		.snap_rdata_i(sp_snap_rdata_r),
		.snap_rvalid_i(sp_snap_rvalid_r),
		.ctrl_req_o(sp_ctrl_req_w),
		.ctrl_we_o(sp_ctrl_we_w),
		.ctrl_addr_o(sp_ctrl_addr_w),
		.ctrl_wdata_o(sp_ctrl_wdata_w),
		.ctrl_rdata_i(sp_ctrl_rdata_r),
		.ctrl_rvalid_i(sp_ctrl_rvalid_r),
		.trace_req_o(sp_trace_req_w),
		.trace_addr_o(sp_trace_addr_w),
		.trace_rdata_i(trc_rd_data_w),
		.trace_rvalid_i(sp_trace_rvalid_r),
		.fw_req_o(sp_fw_req_nc_w),
		.fw_we_o(sp_fw_we_nc_w),
		.fw_addr_o(sp_fw_addr_nc_w),
		.fw_wdata_o(sp_fw_wdata_nc_w),
		.fw_rdata_i(32'd0),
		.fw_rvalid_i(1'b0)
	);
	assign trc_rd_en_w = sp_trace_req_w;
	assign trc_rd_addr_w = sp_trace_addr_w[9:2];
	assign trc_rd_lane_w = sp_trace_addr_w[1:0];
	reg [31:0] ctrl_scratch_r;
	always @(posedge clk_i) begin : side_backends
		if (!rst_n) begin
			sp_img_rvalid_r <= 1'b0;
			sp_dbg_rvalid_r <= 1'b0;
			sp_snap_rvalid_r <= 1'b0;
			sp_snap_rdata_r <= 32'd0;
			sp_ctrl_rvalid_r <= 1'b0;
			sp_ctrl_rdata_r <= 32'd0;
			sp_trace_rvalid_r <= 1'b0;
			ctrl_scratch_r <= 32'd0;
		end
		else begin
			sp_img_rvalid_r <= sp_img_req_w;
			sp_dbg_rvalid_r <= sp_dbg_req_w;
			sp_trace_rvalid_r <= sp_trace_req_w;
			sp_snap_rvalid_r <= sp_snap_req_w;
			sp_ctrl_rvalid_r <= sp_ctrl_req_w;
			if ((sp_ctrl_req_w && sp_ctrl_we_w) && (sp_ctrl_addr_w == 8'd0))
				ctrl_scratch_r <= sp_ctrl_wdata_w;
			(* full_case, parallel_case *)
			case (sp_ctrl_addr_w)
				8'd0: sp_ctrl_rdata_r <= ctrl_scratch_r;
				8'd1: sp_ctrl_rdata_r <= {28'd0, restore_fail_o, restore_done_o, restore_busy_o, entity_enable_i};
				default: sp_ctrl_rdata_r <= 32'd0;
			endcase
			(* full_case, parallel_case *)
			case (sp_snap_addr_w[5:0])
				6'd0: sp_snap_rdata_r <= 32'h4b4c5050;
				6'd1: sp_snap_rdata_r <= {sv2v_cast_8(N_STREAM_IN_P), sv2v_cast_8(N_STREAM_OUT_P), sv2v_cast_8(RX_SLOTS_P), sv2v_cast_8(TX_STD_SLOTS_P)};
				6'd2: sp_snap_rdata_r <= now_ms_w;
				6'd3: sp_snap_rdata_r <= {26'd0, nvm_alarm_o, srp_over_limit_w, srp_domain_adopted_w, prng_seeded_w, link_up_i, entity_enable_i};
				6'd4: sp_snap_rdata_r <= {cnt_rx_da_w, cnt_rx_ethertype_w};
				6'd5: sp_snap_rdata_r <= {cnt_rx_subtype_w, cnt_rx_version_w};
				6'd6: sp_snap_rdata_r <= {cnt_rx_length_w, rxp_overrun_w[0+:16]};
				6'd7: sp_snap_rdata_r <= {disp_adp_level_w, disp_acmp_level_w, disp_aecp_level_w, 8'd0};
				6'd8: sp_snap_rdata_r <= {disp_adp_stall_w, disp_acmp_stall_w};
				6'd9: sp_snap_rdata_r <= {disp_aecp_stall_w, hdr_drop_r};
				6'd10: sp_snap_rdata_r <= {13'd0, srp_class_a_prio_w, 4'd0, srp_class_a_vid_w};
				6'd11: sp_snap_rdata_r <= srp_sum_slope_w;
				6'd12: sp_snap_rdata_r <= {sv2v_cast_8(srp_sr_admitted_w), sv2v_cast_8(srp_active_w), sv2v_cast_16(srp_tk_reg_state_w)};
				6'd13: sp_snap_rdata_r <= {sv2v_cast_16(srp_tk_decl_state_w), sv2v_cast_16(srp_lstn_reg_state_w)};
				6'd14: sp_snap_rdata_r <= {sv2v_cast_16(srp_lstn_decl_state_w), 12'd0, srp_dbg_vid_active_w};
				6'd15: sp_snap_rdata_r <= {sb_holds_w, 6'd0, sb_full_w, sb_barrier_w, trc_wr_count_w};
				6'd16, 6'd17, 6'd18, 6'd19, 6'd20, 6'd21, 6'd22, 6'd23: sp_snap_rdata_r <= srp_acc_latency_w[sp_snap_addr_w[2:0] * 32+:32];
				6'd24: sp_snap_rdata_r <= {arm_drop_r, mrp_drop_w};
				6'd25: sp_snap_rdata_r <= {13'd0, sv2v_cast_16(rxp_slots_free_w[RXP_ADP_C * $clog2(RX_SLOTS_P + 1)+:$clog2(RX_SLOTS_P + 1)]), txs_free_w};
				6'd26: sp_snap_rdata_r <= {arb_gnt_cnt_w[32+:16], arb_gnt_cnt_w[48+:16]};
				6'd27: sp_snap_rdata_r <= {arb_gnt_cnt_w[64+:16], arb_gnt_cnt_w[80+:16]};
				6'd28: sp_snap_rdata_r <= {sv2v_cast_8(bound_r), tkb_drop_r, svc_drop_r[7:0]};
				6'd29: sp_snap_rdata_r <= {rxf_drop_r, 8'd0, srp_snk_fail_code_w[0+:8]};
				6'd30: sp_snap_rdata_r <= srp_granted_slope_w[0+:32];
				6'd31: sp_snap_rdata_r <= {30'd0, adp_dbg_adv_state_w};
				6'd32: sp_snap_rdata_r <= {aecp_dbg_cmd_w, aecp_dbg_resp_w};
				6'd33: sp_snap_rdata_r <= {aecp_dbg_drop_w, aecp_dbg_miss_w};
				6'd34: sp_snap_rdata_r <= {11'd0, aecp_dbg_len_w, aecp_dbg_status_w, aecp_dbg_fault_w, aecp_dbg_img_valid_w};
				6'd35: sp_snap_rdata_r <= {aecp_dbg_rerr_w, aecp_dbg_rlane_w};
				6'd36: sp_snap_rdata_r <= {29'd0, aecp_dbg_rfault_w};
				default: sp_snap_rdata_r <= 32'd0;
			endcase
		end
	end
	initial _sv2v_0 = 0;
endmodule
`default_nettype wire
`default_nettype none
module KL_pp_shadow (
	clk_i,
	rst_n,
	entity_id_i,
	entity_model_id_i,
	station_mac_i,
	talker_sources_i,
	talker_caps_i,
	listener_sinks_i,
	listener_caps_i,
	current_cfg_i,
	identify_index_i,
	cfg_src_en_i,
	cfg_stream_id_i,
	cfg_tspec_max_frame_i,
	cfg_acc_lat_ns_i,
	port_rate_bps_i,
	enable_i,
	restore_go_i,
	link_up_i,
	gm_change_i,
	gm_id_i,
	gptp_domain_i,
	rx_tdata_i,
	rx_tkeep_i,
	rx_tvalid_i,
	rx_tready_i,
	rx_tlast_i,
	ctr_req_o,
	ctr_desc_type_o,
	ctr_desc_index_o,
	ctr_word_o,
	ctr_data_i,
	ctr_wait_i,
	ctr_change_i,
	ctr_change_desc_type_i,
	ctr_change_desc_index_i,
	amap_req_o,
	amap_desc_type_o,
	amap_desc_index_o,
	amap_map_index_o,
	amap_sel_o,
	amap_rec_o,
	amap_data_i,
	amap_wait_i,
	amap_edit_req_o,
	amap_edit_phase_o,
	amap_edit_remove_o,
	amap_edit_desc_type_o,
	amap_edit_desc_index_o,
	amap_edit_count_o,
	amap_edit_rec_o,
	amap_edit_record_o,
	amap_edit_value_o,
	amap_edit_data_i,
	amap_edit_wait_i,
	gsi_req_o,
	gsi_kind_o,
	gsi_desc_type_o,
	gsi_desc_index_o,
	gsi_sel_o,
	gsi_ord_o,
	gsi_prop_fmt_o,
	gsi_data_i,
	gsi_wait_i,
	gsi_avb_chg_i,
	gsi_asp_chg_i,
	host_req_i,
	host_we_i,
	host_addr_i,
	host_wdata_i,
	host_rdata_o,
	host_ack_o,
	host_err_o,
	m_axis_tx_tdata,
	m_axis_tx_tkeep,
	m_axis_tx_tvalid,
	m_axis_tx_tlast,
	m_axis_tx_tready,
	tx_drain_i,
	desc_mem_req_valid_o,
	desc_mem_req_ready_i,
	desc_mem_req_addr_o,
	desc_mem_req_beats_o,
	desc_mem_rsp_valid_i,
	desc_mem_rsp_ready_o,
	desc_mem_rsp_data_i,
	desc_mem_rsp_last_i,
	desc_mem_rsp_err_i,
	resp_mem_req_valid_o,
	resp_mem_req_ready_i,
	resp_mem_req_addr_o,
	resp_mem_req_beats_o,
	resp_mem_rsp_valid_i,
	resp_mem_rsp_ready_o,
	resp_mem_rsp_data_i,
	resp_mem_rsp_last_i,
	resp_mem_rsp_err_i,
	resp_mem_wr_valid_o,
	resp_mem_wr_ready_i,
	resp_mem_wr_addr_o,
	resp_mem_wr_data_o,
	resp_mem_wr_strb_o,
	resp_mem_wr_done_i,
	resp_mem_wr_err_i,
	nvm_mem_req_valid_o,
	nvm_mem_req_ready_i,
	nvm_mem_req_addr_o,
	nvm_mem_req_beats_o,
	nvm_mem_rsp_valid_i,
	nvm_mem_rsp_ready_o,
	nvm_mem_rsp_data_i,
	nvm_mem_rsp_last_i,
	nvm_mem_rsp_err_i,
	nvm_mem_wr_valid_o,
	nvm_mem_wr_ready_i,
	nvm_mem_wr_addr_o,
	nvm_mem_wr_data_o,
	nvm_mem_wr_strb_o,
	nvm_mem_wr_done_i,
	nvm_mem_wr_err_i,
	nvm_csr_sel_i,
	nvm_csr_we_i,
	nvm_csr_addr_i,
	nvm_csr_wdata_i,
	nvm_csr_rdata_o,
	maap_req_valid_o,
	maap_req_ready_i,
	maap_req_release_o,
	maap_req_src_o,
	maap_rsp_valid_i,
	maap_rsp_ok_i,
	maap_rsp_da_i,
	maap_conflict_valid_i,
	maap_conflict_src_i,
	maap_conflict_ack_o,
	cfg_maap_internal_i,
	cfg_maap_count_i,
	cfg_maap_seed_offset_i,
	cfg_maap_seed_valid_i,
	maap_addr_o,
	maap_addr_valid_o,
	maap_state_o,
	maap_conflicts_o,
	maap_defends_o,
	aecp_cur_config_o,
	aecp_identify_o,
	aecp_clk_src_index_o,
	aecp_strm_started_o,
	aecp_pt_offset_o,
	aecp_pt_offset_v_o,
	aecp_fmt_in_o,
	aecp_fmt_in_v_o,
	aecp_fmt_out_o,
	aecp_fmt_out_v_o,
	aecp_dyn_dirty_o,
	aecp_lock_held_o,
	srp_class_a_prio_o,
	srp_class_a_vid_o,
	srp_domain_adopted_o,
	srp_domain_change_o,
	srp_tk_decl_state_o,
	srp_lstn_reg_state_o,
	srp_active_o,
	srp_sr_admitted_o,
	srp_granted_slope_bps_o,
	srp_src_fail_code_o,
	srp_src_fail_bridge_o,
	srp_sum_slope_bps_o,
	srp_over_limit_o,
	srp_tk_reg_state_o,
	srp_lstn_decl_state_o,
	srp_acc_latency_o,
	srp_snk_fail_code_o,
	acmp_declaring_o,
	acmp_bound_o,
	acmp_bound_eid_o,
	acmp_bound_sid_o,
	acmp_bound_dmac_o,
	acmp_bound_vlan_o,
	adp_next_avail_index_o,
	restore_busy_o,
	restore_done_o,
	restore_fail_o,
	nvm_backed_o,
	restore_blank_o,
	nvm_alarm_o,
	nvm_dirty_o,
	nvm_stale_o,
	nvm_pend_o,
	nvm_verdict_o,
	nvm_img_valid_o,
	rx_frames_o,
	rx_drops_o,
	tx_frames_o,
	dbg_now_ms_o
);
	reg _sv2v_0;
	parameter [31:0] TDATA_WIDTH_P = 64;
	parameter [31:0] CLK_HZ_P = 100000000;
	parameter [31:0] N_STREAM_IN_P = 8;
	parameter [31:0] N_STREAM_OUT_P = 8;
	parameter [31:0] RX_FIFO_BYTES_P = 4096;
	parameter [31:0] TIM_DIV_US_P = CLK_HZ_P / 32'd1000000;
	parameter [31:0] TIM_DIV_MS_P = 1000;
	parameter TROM_HEX_P = "ltn_rom.hex";
	parameter UCODE_HEX_P = "ucode.hex";
	parameter [31:0] DESC_BASE_P = 32'h20000000;
	parameter [31:0] DESC_LINE_BYTES_P = 576;
	parameter [31:0] DESC_IDX_ENTRIES_P = 32;
	parameter [31:0] DESC_NAME_ENTRIES_P = 32;
	parameter [31:0] DESC_MEM_TMO_CYC_P = 4096;
	parameter [31:0] RESP_BASE_P = 32'h20100000;
	parameter [31:0] N_SPORT_IN_P = 8;
	parameter [31:0] N_SPORT_OUT_P = 8;
	parameter [31:0] N_AUDIO_UNIT_P = 1;
	parameter [31:0] N_CLK_DOM_P = 1;
	localparam [31:0] SRC_IDX_W_C = (N_STREAM_OUT_P > 32'd1 ? $clog2(N_STREAM_OUT_P) : 32'd1);
	input wire clk_i;
	input wire rst_n;
	input wire [63:0] entity_id_i;
	input wire [63:0] entity_model_id_i;
	input wire [47:0] station_mac_i;
	input wire [15:0] talker_sources_i;
	input wire [15:0] talker_caps_i;
	input wire [15:0] listener_sinks_i;
	input wire [15:0] listener_caps_i;
	input wire [15:0] current_cfg_i;
	input wire [15:0] identify_index_i;
	input wire [N_STREAM_OUT_P - 1:0] cfg_src_en_i;
	input wire [(N_STREAM_OUT_P * 64) - 1:0] cfg_stream_id_i;
	input wire [15:0] cfg_tspec_max_frame_i;
	input wire [31:0] cfg_acc_lat_ns_i;
	input wire [31:0] port_rate_bps_i;
	input wire enable_i;
	input wire restore_go_i;
	input wire link_up_i;
	input wire gm_change_i;
	input wire [63:0] gm_id_i;
	input wire [7:0] gptp_domain_i;
	input wire [TDATA_WIDTH_P - 1:0] rx_tdata_i;
	input wire [(TDATA_WIDTH_P / 8) - 1:0] rx_tkeep_i;
	input wire rx_tvalid_i;
	input wire rx_tready_i;
	input wire rx_tlast_i;
	output wire ctr_req_o;
	output wire [15:0] ctr_desc_type_o;
	output wire [15:0] ctr_desc_index_o;
	output wire [5:0] ctr_word_o;
	input wire [31:0] ctr_data_i;
	input wire ctr_wait_i;
	input wire ctr_change_i;
	input wire [15:0] ctr_change_desc_type_i;
	input wire [15:0] ctr_change_desc_index_i;
	output wire amap_req_o;
	output wire [15:0] amap_desc_type_o;
	output wire [15:0] amap_desc_index_o;
	output wire [15:0] amap_map_index_o;
	output wire [1:0] amap_sel_o;
	output wire [7:0] amap_rec_o;
	input wire [63:0] amap_data_i;
	input wire amap_wait_i;
	output wire amap_edit_req_o;
	output wire [2:0] amap_edit_phase_o;
	output wire amap_edit_remove_o;
	output wire [15:0] amap_edit_desc_type_o;
	output wire [15:0] amap_edit_desc_index_o;
	output wire [15:0] amap_edit_count_o;
	output wire [7:0] amap_edit_rec_o;
	output wire [63:0] amap_edit_record_o;
	output wire [63:0] amap_edit_value_o;
	input wire [63:0] amap_edit_data_i;
	input wire amap_edit_wait_i;
	output wire gsi_req_o;
	output wire [1:0] gsi_kind_o;
	output wire [15:0] gsi_desc_type_o;
	output wire [15:0] gsi_desc_index_o;
	output wire [3:0] gsi_sel_o;
	output wire [7:0] gsi_ord_o;
	output wire [63:0] gsi_prop_fmt_o;
	input wire [63:0] gsi_data_i;
	input wire gsi_wait_i;
	input wire gsi_avb_chg_i;
	input wire gsi_asp_chg_i;
	input wire host_req_i;
	input wire host_we_i;
	input wire [19:0] host_addr_i;
	input wire [31:0] host_wdata_i;
	output reg [31:0] host_rdata_o;
	output reg host_ack_o;
	output reg host_err_o;
	output wire [TDATA_WIDTH_P - 1:0] m_axis_tx_tdata;
	output wire [(TDATA_WIDTH_P / 8) - 1:0] m_axis_tx_tkeep;
	output wire m_axis_tx_tvalid;
	output wire m_axis_tx_tlast;
	input wire m_axis_tx_tready;
	input wire tx_drain_i;
	output wire desc_mem_req_valid_o;
	input wire desc_mem_req_ready_i;
	output wire [31:0] desc_mem_req_addr_o;
	output wire [8:0] desc_mem_req_beats_o;
	input wire desc_mem_rsp_valid_i;
	output wire desc_mem_rsp_ready_o;
	input wire [63:0] desc_mem_rsp_data_i;
	input wire desc_mem_rsp_last_i;
	input wire desc_mem_rsp_err_i;
	output wire resp_mem_req_valid_o;
	input wire resp_mem_req_ready_i;
	output wire [31:0] resp_mem_req_addr_o;
	output wire [8:0] resp_mem_req_beats_o;
	input wire resp_mem_rsp_valid_i;
	output wire resp_mem_rsp_ready_o;
	input wire [63:0] resp_mem_rsp_data_i;
	input wire resp_mem_rsp_last_i;
	input wire resp_mem_rsp_err_i;
	output wire resp_mem_wr_valid_o;
	input wire resp_mem_wr_ready_i;
	output wire [31:0] resp_mem_wr_addr_o;
	output wire [63:0] resp_mem_wr_data_o;
	output wire [7:0] resp_mem_wr_strb_o;
	input wire resp_mem_wr_done_i;
	input wire resp_mem_wr_err_i;
	output wire nvm_mem_req_valid_o;
	input wire nvm_mem_req_ready_i;
	output wire [31:0] nvm_mem_req_addr_o;
	output wire [8:0] nvm_mem_req_beats_o;
	input wire nvm_mem_rsp_valid_i;
	output wire nvm_mem_rsp_ready_o;
	input wire [63:0] nvm_mem_rsp_data_i;
	input wire nvm_mem_rsp_last_i;
	input wire nvm_mem_rsp_err_i;
	output wire nvm_mem_wr_valid_o;
	input wire nvm_mem_wr_ready_i;
	output wire [31:0] nvm_mem_wr_addr_o;
	output wire [63:0] nvm_mem_wr_data_o;
	output wire [7:0] nvm_mem_wr_strb_o;
	input wire nvm_mem_wr_done_i;
	input wire nvm_mem_wr_err_i;
	input wire nvm_csr_sel_i;
	input wire nvm_csr_we_i;
	input wire [5:0] nvm_csr_addr_i;
	input wire [31:0] nvm_csr_wdata_i;
	output wire [31:0] nvm_csr_rdata_o;
	output wire maap_req_valid_o;
	input wire maap_req_ready_i;
	output wire maap_req_release_o;
	output wire [SRC_IDX_W_C - 1:0] maap_req_src_o;
	input wire maap_rsp_valid_i;
	input wire maap_rsp_ok_i;
	input wire [47:0] maap_rsp_da_i;
	input wire maap_conflict_valid_i;
	input wire [SRC_IDX_W_C - 1:0] maap_conflict_src_i;
	output wire maap_conflict_ack_o;
	input wire cfg_maap_internal_i;
	input wire [7:0] cfg_maap_count_i;
	input wire [15:0] cfg_maap_seed_offset_i;
	input wire cfg_maap_seed_valid_i;
	output wire [47:0] maap_addr_o;
	output wire maap_addr_valid_o;
	output wire [1:0] maap_state_o;
	output wire [7:0] maap_conflicts_o;
	output wire [7:0] maap_defends_o;
	output wire [15:0] aecp_cur_config_o;
	output wire [7:0] aecp_identify_o;
	output wire [15:0] aecp_clk_src_index_o;
	output wire [N_STREAM_IN_P - 1:0] aecp_strm_started_o;
	output wire [(N_STREAM_OUT_P * 32) - 1:0] aecp_pt_offset_o;
	output wire [N_STREAM_OUT_P - 1:0] aecp_pt_offset_v_o;
	output wire [(N_STREAM_IN_P * 64) - 1:0] aecp_fmt_in_o;
	output wire [N_STREAM_IN_P - 1:0] aecp_fmt_in_v_o;
	output wire [(N_STREAM_OUT_P * 64) - 1:0] aecp_fmt_out_o;
	output wire [N_STREAM_OUT_P - 1:0] aecp_fmt_out_v_o;
	output wire aecp_dyn_dirty_o;
	output wire aecp_lock_held_o;
	output wire [2:0] srp_class_a_prio_o;
	output wire [11:0] srp_class_a_vid_o;
	output wire srp_domain_adopted_o;
	output wire srp_domain_change_o;
	output wire [(N_STREAM_OUT_P * 2) - 1:0] srp_tk_decl_state_o;
	output wire [(N_STREAM_OUT_P * 2) - 1:0] srp_lstn_reg_state_o;
	output wire [N_STREAM_OUT_P - 1:0] srp_active_o;
	output wire [N_STREAM_OUT_P - 1:0] srp_sr_admitted_o;
	output wire [(N_STREAM_OUT_P * 32) - 1:0] srp_granted_slope_bps_o;
	output wire [(N_STREAM_OUT_P * 8) - 1:0] srp_src_fail_code_o;
	output wire [(N_STREAM_OUT_P * 64) - 1:0] srp_src_fail_bridge_o;
	output wire [31:0] srp_sum_slope_bps_o;
	output wire srp_over_limit_o;
	output wire [(N_STREAM_IN_P * 2) - 1:0] srp_tk_reg_state_o;
	output wire [(N_STREAM_IN_P * 2) - 1:0] srp_lstn_decl_state_o;
	output wire [(N_STREAM_IN_P * 32) - 1:0] srp_acc_latency_o;
	output wire [(N_STREAM_IN_P * 8) - 1:0] srp_snk_fail_code_o;
	output wire [N_STREAM_OUT_P - 1:0] acmp_declaring_o;
	output wire [N_STREAM_IN_P - 1:0] acmp_bound_o;
	output wire [(N_STREAM_IN_P * 64) - 1:0] acmp_bound_eid_o;
	output wire [(N_STREAM_IN_P * 64) - 1:0] acmp_bound_sid_o;
	output wire [(N_STREAM_IN_P * 48) - 1:0] acmp_bound_dmac_o;
	output wire [(N_STREAM_IN_P * 12) - 1:0] acmp_bound_vlan_o;
	output wire [31:0] adp_next_avail_index_o;
	output wire restore_busy_o;
	output wire restore_done_o;
	output wire restore_fail_o;
	output wire nvm_backed_o;
	output wire restore_blank_o;
	output wire nvm_alarm_o;
	output wire nvm_dirty_o;
	output wire nvm_stale_o;
	output wire nvm_pend_o;
	output wire [3:0] nvm_verdict_o;
	output wire nvm_img_valid_o;
	output reg [15:0] rx_frames_o;
	output reg [7:0] rx_drops_o;
	output reg [15:0] tx_frames_o;
	output wire [31:0] dbg_now_ms_o;
	localparam [31:0] KEEP_W_C = TDATA_WIDTH_P / 8;
	localparam [47:0] DA_MSRP_C = 48'h0180c200000e;
	localparam [47:0] DA_MVRP_C = 48'h0180c2000021;
	localparam [15:0] ET_1722_C = 16'h22f0;
	localparam [15:0] ET_MSRP_C = 16'h22ea;
	localparam [15:0] ET_MVRP_C = 16'h88f5;
	wire beat_w;
	assign beat_w = rx_tvalid_i & rx_tready_i;
	wire [47:0] da_num_w;
	wire [15:0] etype_w;
	assign da_num_w = {rx_tdata_i[7:0], rx_tdata_i[15:8], rx_tdata_i[23:16], rx_tdata_i[31:24], rx_tdata_i[39:32], rx_tdata_i[47:40]};
	assign etype_w = {rx_tdata_i[39:32], rx_tdata_i[47:40]};
	reg [1:0] fw_S;
	reg [47:0] da_r;
	reg fw_valid_w;
	reg fw_last_w;
	reg fw_user_w;
	reg [TDATA_WIDTH_P - 1:0] fw_data_w;
	reg [KEEP_W_C - 1:0] fw_keep_w;
	wire fw_ready_w;
	wire accept_w;
	assign accept_w = ((etype_w == ET_1722_C) || ((da_r == DA_MSRP_C) && (etype_w == ET_MSRP_C))) || ((da_r == DA_MVRP_C) && (etype_w == ET_MVRP_C));
	always @(*) begin
		if (_sv2v_0)
			;
		fw_valid_w = 1'b0;
		fw_data_w = rx_tdata_i;
		fw_keep_w = rx_tkeep_i;
		fw_last_w = rx_tlast_i;
		fw_user_w = 1'b0;
		(* full_case, parallel_case *)
		case (fw_S)
			2'd0: begin
				fw_valid_w = beat_w;
				fw_user_w = rx_tlast_i;
			end
			2'd1: begin
				fw_valid_w = beat_w;
				if (!accept_w) begin
					fw_last_w = 1'b1;
					fw_user_w = 1'b1;
				end
			end
			2'd2: fw_valid_w = beat_w;
			default: fw_valid_w = 1'b0;
		endcase
	end
	always @(posedge clk_i or negedge rst_n)
		if (!rst_n) begin
			fw_S <= 2'd0;
			da_r <= 48'd0;
		end
		else if (beat_w)
			(* full_case, parallel_case *)
			case (fw_S)
				2'd0: begin
					da_r <= da_num_w;
					fw_S <= (rx_tlast_i ? 2'd0 : 2'd1);
				end
				2'd1: fw_S <= (rx_tlast_i ? 2'd0 : (accept_w ? 2'd2 : 2'd3));
				2'd2:
					if (rx_tlast_i)
						fw_S <= 2'd0;
				default:
					if (rx_tlast_i)
						fw_S <= 2'd0;
			endcase
	wire drop_evt_w;
	assign drop_evt_w = (fw_valid_w & ~fw_ready_w) & (((fw_S == 2'd0) || (fw_S == 2'd1)) || (fw_S == 2'd2));
	wire [TDATA_WIDTH_P - 1:0] ff_data_w;
	wire [KEEP_W_C - 1:0] ff_keep_w;
	wire ff_valid_w;
	wire ff_last_w;
	wire ff_ready_w;
	localparam sv2v_uu_ctl_fifo_ID_WIDTH = 8;
	localparam [7:0] sv2v_uu_ctl_fifo_ext_s_axis_tid_0 = 1'sb0;
	localparam sv2v_uu_ctl_fifo_DEST_WIDTH = 8;
	localparam [7:0] sv2v_uu_ctl_fifo_ext_s_axis_tdest_0 = 1'sb0;
	axis_fifo #(
		.DEPTH(RX_FIFO_BYTES_P),
		.DATA_WIDTH(TDATA_WIDTH_P),
		.KEEP_ENABLE(1),
		.KEEP_WIDTH(KEEP_W_C),
		.LAST_ENABLE(1),
		.ID_ENABLE(0),
		.DEST_ENABLE(0),
		.USER_ENABLE(1),
		.USER_WIDTH(1),
		.FRAME_FIFO(1),
		.USER_BAD_FRAME_VALUE(1'b1),
		.USER_BAD_FRAME_MASK(1'b1),
		.DROP_BAD_FRAME(1),
		.DROP_OVERSIZE_FRAME(1),
		.DROP_WHEN_FULL(1)
	) ctl_fifo(
		.clk(clk_i),
		.rst(~rst_n),
		.s_axis_tdata(fw_data_w),
		.s_axis_tkeep(fw_keep_w),
		.s_axis_tvalid(fw_valid_w),
		.s_axis_tready(fw_ready_w),
		.s_axis_tlast(fw_last_w),
		.s_axis_tid(sv2v_uu_ctl_fifo_ext_s_axis_tid_0),
		.s_axis_tdest(sv2v_uu_ctl_fifo_ext_s_axis_tdest_0),
		.s_axis_tuser(fw_user_w),
		.m_axis_tdata(ff_data_w),
		.m_axis_tkeep(ff_keep_w),
		.m_axis_tvalid(ff_valid_w),
		.m_axis_tready(ff_ready_w),
		.m_axis_tlast(ff_last_w),
		.m_axis_tid(),
		.m_axis_tdest(),
		.m_axis_tuser(),
		.status_overflow(),
		.status_bad_frame(),
		.status_good_frame(),
		.status_depth(),
		.status_depth_commit(),
		.pause_req(1'b0),
		.pause_ack()
	);
	reg [TDATA_WIDTH_P - 1:0] ser_data_r;
	reg [KEEP_W_C - 1:0] ser_keep_r;
	reg ser_last_r;
	reg ser_busy_r;
	reg [2:0] ser_idx_r;
	reg [2:0] ser_top_w;
	function automatic [2:0] sv2v_cast_3;
		input reg [2:0] inp;
		sv2v_cast_3 = inp;
	endfunction
	always @(*) begin
		if (_sv2v_0)
			;
		ser_top_w = 3'd0;
		begin : sv2v_autoblock_1
			reg [31:0] i;
			for (i = 0; i < KEEP_W_C; i = i + 1)
				if (ser_keep_r[i])
					ser_top_w = sv2v_cast_3(i);
		end
	end
	assign ff_ready_w = ~ser_busy_r;
	wire pp_rx_valid_w;
	wire [7:0] pp_rx_data_w;
	wire pp_rx_last_w;
	assign pp_rx_valid_w = ser_busy_r;
	assign pp_rx_data_w = ser_data_r[8 * ser_idx_r+:8];
	assign pp_rx_last_w = (ser_busy_r & ser_last_r) & (ser_idx_r == ser_top_w);
	always @(posedge clk_i or negedge rst_n)
		if (!rst_n) begin
			ser_busy_r <= 1'b0;
			ser_idx_r <= 3'd0;
			ser_data_r <= 1'sb0;
			ser_keep_r <= 1'sb0;
			ser_last_r <= 1'b0;
		end
		else if (!ser_busy_r) begin
			if (ff_valid_w) begin
				ser_data_r <= ff_data_w;
				ser_keep_r <= ff_keep_w;
				ser_last_r <= ff_last_w;
				ser_idx_r <= 3'd0;
				ser_busy_r <= 1'b1;
			end
		end
		else if (ser_idx_r == ser_top_w)
			ser_busy_r <= 1'b0;
		else
			ser_idx_r <= ser_idx_r + 3'd1;
	wire nvm_req_w;
	wire nvm_gnt_w;
	wire nvm_wvalid_w;
	wire nvm_wready_w;
	wire nvm_rvalid_w;
	wire nvm_rready_w;
	wire nvm_busy_w;
	wire nvm_done_w;
	wire nvm_err_w;
	wire [1:0] nvm_op_w;
	wire [7:0] nvm_region_w;
	wire [7:0] nvm_wdata_w;
	wire [7:0] nvm_rdata_w;
	wire [15:0] nvm_offset_w;
	wire [15:0] nvm_len_w;
	wire nvm_backed_w;
	wire nvm_img_valid_w;
	wire nvm_pend_w;
	wire nvm_alarm_w;
	reg restore_busy_q;
	reg walk_blind_r;
	localparam [7:0] NVM_MARK_MAPS_C = 8'd6;
	localparam [7:0] NVM_MARK_NAMES_C = 8'd7;
	wire [N_STREAM_IN_P - 1:0] nvm_unflushed_w;
	wire aecp_nvm_stb_w;
	wire [7:0] aecp_nvm_mark_w;
	reg aecp_mark_pend_r;
	always @(posedge clk_i or negedge rst_n)
		if (!rst_n)
			aecp_mark_pend_r <= 1'b0;
		else if (aecp_nvm_stb_w && ((aecp_nvm_mark_w == NVM_MARK_MAPS_C) || (aecp_nvm_mark_w == NVM_MARK_NAMES_C)))
			aecp_mark_pend_r <= 1'b1;
	assign nvm_pend_w = (aecp_dyn_dirty_o | (|nvm_unflushed_w)) | aecp_mark_pend_r;
	always @(posedge clk_i or negedge rst_n)
		if (!rst_n) begin
			restore_busy_q <= 1'b0;
			walk_blind_r <= 1'b1;
		end
		else begin
			restore_busy_q <= restore_busy_o;
			if (restore_busy_o && !restore_busy_q)
				walk_blind_r <= ~nvm_img_valid_w;
			else if (restore_busy_o && !nvm_img_valid_w)
				walk_blind_r <= 1'b1;
		end
	KL_nvm_backend #(
		.CLK_HZ_P(CLK_HZ_P),
		.N_STREAM_IN_P(N_STREAM_IN_P),
		.N_STREAM_OUT_P(N_STREAM_OUT_P),
		.N_SPORT_IN_P(N_SPORT_IN_P),
		.N_SPORT_OUT_P(N_SPORT_OUT_P),
		.N_AUDIO_UNIT_P(N_AUDIO_UNIT_P),
		.N_CLK_DOM_P(N_CLK_DOM_P),
		.N_NAME_P(DESC_NAME_ENTRIES_P)
	) u_nvm(
		.clk_i(clk_i),
		.rst_n(rst_n),
		.dev_req_i(nvm_req_w),
		.dev_gnt_o(nvm_gnt_w),
		.dev_op_i(nvm_op_w),
		.dev_region_i(nvm_region_w),
		.dev_offset_i(nvm_offset_w),
		.dev_len_i(nvm_len_w),
		.dev_wvalid_i(nvm_wvalid_w),
		.dev_wready_o(nvm_wready_w),
		.dev_wdata_i(nvm_wdata_w),
		.dev_rvalid_o(nvm_rvalid_w),
		.dev_rdata_o(nvm_rdata_w),
		.dev_rready_i(nvm_rready_w),
		.dev_busy_o(nvm_busy_w),
		.dev_done_o(nvm_done_w),
		.dev_err_o(nvm_err_w),
		.mem_req_valid_o(nvm_mem_req_valid_o),
		.mem_req_ready_i(nvm_mem_req_ready_i),
		.mem_req_addr_o(nvm_mem_req_addr_o),
		.mem_req_beats_o(nvm_mem_req_beats_o),
		.mem_rsp_valid_i(nvm_mem_rsp_valid_i),
		.mem_rsp_ready_o(nvm_mem_rsp_ready_o),
		.mem_rsp_data_i(nvm_mem_rsp_data_i),
		.mem_rsp_last_i(nvm_mem_rsp_last_i),
		.mem_rsp_err_i(nvm_mem_rsp_err_i),
		.mem_wr_valid_o(nvm_mem_wr_valid_o),
		.mem_wr_ready_i(nvm_mem_wr_ready_i),
		.mem_wr_addr_o(nvm_mem_wr_addr_o),
		.mem_wr_data_o(nvm_mem_wr_data_o),
		.mem_wr_strb_o(nvm_mem_wr_strb_o),
		.mem_wr_done_i(nvm_mem_wr_done_i),
		.mem_wr_err_i(nvm_mem_wr_err_i),
		.csr_sel_i(nvm_csr_sel_i),
		.csr_we_i(nvm_csr_we_i),
		.csr_addr_i(nvm_csr_addr_i),
		.csr_wdata_i(nvm_csr_wdata_i),
		.csr_rdata_o(nvm_csr_rdata_o),
		.pend_i(nvm_pend_w),
		.alarm_i(nvm_alarm_w),
		.nvm_backed_o(nvm_backed_w),
		.nvm_dirty_o(nvm_dirty_o),
		.nvm_stale_o(nvm_stale_o),
		.nvm_verdict_o(nvm_verdict_o),
		.img_valid_o(nvm_img_valid_w),
		.nvm_pend_o(nvm_pend_o),
		.nvm_unres_o()
	);
	assign nvm_img_valid_o = nvm_img_valid_w;
	assign nvm_alarm_o = nvm_alarm_w;
	wire pp_tx_valid_w;
	wire pp_tx_eof_w;
	wire [7:0] pp_tx_data_w;
	wire pp_host_rvalid_w;
	wire pp_host_err_w;
	wire [31:0] pp_host_rdata_w;
	wire pp_restore_done_w;
	wire pp_restore_fail_w;
	wire pp_restore_blank_w;
	reg hb_pend_r;
	reg hb_we_r;
	reg [19:0] hb_addr_r;
	reg [31:0] hb_wdata_r;
	wire pp_tx_ready_w;
	localparam [31:0] sv2v_uu_u_pp_N_STREAM_OUT_P = N_STREAM_OUT_P;
	localparam [(sv2v_uu_u_pp_N_STREAM_OUT_P * 2) - 1:0] sv2v_uu_u_pp_ext_cfg_src_iface_i_0 = 1'sb0;
	localparam [31:0] sv2v_uu_u_pp_RX_SLOTS_P = 4;
	localparam [31:0] sv2v_uu_u_pp_RXS_W_C = 2;
	localparam [1:0] sv2v_uu_u_pp_ext_aecp_rxs_rd_slot_i_0 = 1'sb0;
	localparam [31:0] sv2v_uu_u_pp_RX_SLOT_BYTES_P = 576;
	localparam [31:0] sv2v_uu_u_pp_RXA_W_C = 10;
	localparam [9:0] sv2v_uu_u_pp_ext_aecp_rxs_rd_addr_i_0 = 1'sb0;
	localparam [1:0] sv2v_uu_u_pp_ext_aecp_rxs_free_slot_i_0 = 1'sb0;
	localparam [2:0] sv2v_uu_u_pp_ext_svc_op_i_0 = 1'sb0;
	localparam [7:0] sv2v_uu_u_pp_ext_svc_index_i_0 = 1'sb0;
	localparam [63:0] sv2v_uu_u_pp_ext_svc_stream_id_i_0 = 1'sb0;
	localparam [47:0] sv2v_uu_u_pp_ext_svc_da_i_0 = 1'sb0;
	localparam [11:0] sv2v_uu_u_pp_ext_svc_vid_i_0 = 1'sb0;
	localparam [15:0] sv2v_uu_u_pp_ext_svc_max_frame_i_0 = 1'sb0;
	localparam [1:0] sv2v_uu_u_pp_ext_svc_lstn_state_i_0 = 1'sb0;
	protocol_processor_top #(
		.N_STREAM_IN_P(N_STREAM_IN_P),
		.N_STREAM_OUT_P(N_STREAM_OUT_P),
		.CLK_HZ_P(CLK_HZ_P),
		.TIM_DIV_US_P(TIM_DIV_US_P),
		.TIM_DIV_MS_P(TIM_DIV_MS_P),
		.TROM_HEX_P(TROM_HEX_P),
		.UCODE_HEX_P(UCODE_HEX_P),
		.DESC_BASE_P(DESC_BASE_P),
		.DESC_LINE_BYTES_P(DESC_LINE_BYTES_P),
		.DESC_IDX_ENTRIES_P(DESC_IDX_ENTRIES_P),
		.DESC_NAME_ENTRIES_P(DESC_NAME_ENTRIES_P),
		.DESC_MEM_TMO_CYC_P(DESC_MEM_TMO_CYC_P),
		.RESP_BASE_P(RESP_BASE_P)
	) u_pp(
		.clk_i(clk_i),
		.rst_n(rst_n),
		.aecp_cur_config_o(aecp_cur_config_o),
		.aecp_identify_o(aecp_identify_o),
		.aecp_clk_src_index_o(aecp_clk_src_index_o),
		.aecp_strm_started_o(aecp_strm_started_o),
		.aecp_pt_offset_o(aecp_pt_offset_o),
		.aecp_pt_offset_v_o(aecp_pt_offset_v_o),
		.aecp_fmt_in_o(aecp_fmt_in_o),
		.aecp_fmt_in_v_o(aecp_fmt_in_v_o),
		.aecp_fmt_out_o(aecp_fmt_out_o),
		.aecp_fmt_out_v_o(aecp_fmt_out_v_o),
		.aecp_dyn_dirty_o(aecp_dyn_dirty_o),
		.aecp_nvm_stb_o(aecp_nvm_stb_w),
		.aecp_nvm_mark_o(aecp_nvm_mark_w),
		.aecp_lock_held_o(aecp_lock_held_o),
		.entity_id_i(entity_id_i),
		.entity_model_id_i(entity_model_id_i),
		.own_mac_i(station_mac_i),
		.talker_sources_i(talker_sources_i),
		.talker_caps_i(talker_caps_i),
		.listener_sinks_i(listener_sinks_i),
		.listener_caps_i(listener_caps_i),
		.current_cfg_i(current_cfg_i),
		.identify_index_i(identify_index_i),
		.entity_enable_i(enable_i),
		.link_up_i(link_up_i),
		.gm_change_i(gm_change_i),
		.gm_id_i(gm_id_i),
		.gptp_domain_i(gptp_domain_i),
		.p2p_i(1'b1),
		.cfg_rank_i(1'b1),
		.cfg_acc_lat_ns_i(cfg_acc_lat_ns_i),
		.port_rate_bps_i(port_rate_bps_i),
		.cfg_tspec_max_frame_i(cfg_tspec_max_frame_i),
		.cfg_src_en_i(cfg_src_en_i),
		.cfg_src_iface_i(sv2v_uu_u_pp_ext_cfg_src_iface_i_0),
		.cfg_stream_id_i(cfg_stream_id_i),
		.rx_valid_i(pp_rx_valid_w),
		.rx_data_i(pp_rx_data_w),
		.rx_last_i(pp_rx_last_w),
		.tx_valid_o(pp_tx_valid_w),
		.tx_sof_o(),
		.tx_data_o(pp_tx_data_w),
		.tx_eof_o(pp_tx_eof_w),
		.tx_ready_i(pp_tx_ready_w),
		.aecp_txn_valid_o(),
		.aecp_txn_o(),
		.aecp_txn_ready_i(1'b0),
		.aecp_rxs_rd_slot_i(sv2v_uu_u_pp_ext_aecp_rxs_rd_slot_i_0),
		.aecp_rxs_rd_addr_i(sv2v_uu_u_pp_ext_aecp_rxs_rd_addr_i_0),
		.aecp_rxs_rd_en_i(1'b0),
		.aecp_rxs_rd_data_o(),
		.aecp_rxs_slot_len_o(),
		.aecp_rxs_free_i(1'b0),
		.aecp_rxs_free_slot_i(sv2v_uu_u_pp_ext_aecp_rxs_free_slot_i_0),
		.ctr_req_o(ctr_req_o),
		.ctr_desc_type_o(ctr_desc_type_o),
		.ctr_desc_index_o(ctr_desc_index_o),
		.ctr_word_o(ctr_word_o),
		.ctr_data_i(ctr_data_i),
		.ctr_wait_i(ctr_wait_i),
		.ctr_change_i(ctr_change_i),
		.ctr_change_desc_type_i(ctr_change_desc_type_i),
		.ctr_change_desc_index_i(ctr_change_desc_index_i),
		.amap_req_o(amap_req_o),
		.amap_desc_type_o(amap_desc_type_o),
		.amap_desc_index_o(amap_desc_index_o),
		.amap_map_index_o(amap_map_index_o),
		.amap_sel_o(amap_sel_o),
		.amap_rec_o(amap_rec_o),
		.amap_data_i(amap_data_i),
		.amap_wait_i(amap_wait_i),
		.amap_edit_req_o(amap_edit_req_o),
		.amap_edit_phase_o(amap_edit_phase_o),
		.amap_edit_remove_o(amap_edit_remove_o),
		.amap_edit_desc_type_o(amap_edit_desc_type_o),
		.amap_edit_desc_index_o(amap_edit_desc_index_o),
		.amap_edit_count_o(amap_edit_count_o),
		.amap_edit_rec_o(amap_edit_rec_o),
		.amap_edit_record_o(amap_edit_record_o),
		.amap_edit_value_o(amap_edit_value_o),
		.amap_edit_data_i(amap_edit_data_i),
		.amap_edit_wait_i(amap_edit_wait_i),
		.gsi_req_o(gsi_req_o),
		.gsi_kind_o(gsi_kind_o),
		.gsi_desc_type_o(gsi_desc_type_o),
		.gsi_desc_index_o(gsi_desc_index_o),
		.gsi_sel_o(gsi_sel_o),
		.gsi_ord_o(gsi_ord_o),
		.gsi_prop_fmt_o(gsi_prop_fmt_o),
		.gsi_data_i(gsi_data_i),
		.gsi_wait_i(gsi_wait_i),
		.gsi_avb_chg_i(gsi_avb_chg_i),
		.gsi_asp_chg_i(gsi_asp_chg_i),
		.restore_go_i(restore_go_i),
		.restore_busy_o(restore_busy_o),
		.restore_done_o(pp_restore_done_w),
		.restore_fail_o(pp_restore_fail_w),
		.restore_blank_o(pp_restore_blank_w),
		.nvm_alarm_o(nvm_alarm_w),
		.nvm_unflushed_o(nvm_unflushed_w),
		.nvm_dev_req_o(nvm_req_w),
		.nvm_dev_gnt_i(nvm_gnt_w),
		.nvm_dev_op_o(nvm_op_w),
		.nvm_dev_region_o(nvm_region_w),
		.nvm_dev_offset_o(nvm_offset_w),
		.nvm_dev_len_o(nvm_len_w),
		.nvm_dev_wvalid_o(nvm_wvalid_w),
		.nvm_dev_wready_i(nvm_wready_w),
		.nvm_dev_wdata_o(nvm_wdata_w),
		.nvm_dev_rvalid_i(nvm_rvalid_w),
		.nvm_dev_rdata_i(nvm_rdata_w),
		.nvm_dev_rready_o(nvm_rready_w),
		.nvm_dev_busy_i(nvm_busy_w),
		.nvm_dev_done_i(nvm_done_w),
		.nvm_dev_err_i(nvm_err_w),
		.host_req_valid_i(hb_pend_r),
		.host_we_i(hb_we_r),
		.host_addr_i(hb_addr_r),
		.host_wdata_i(hb_wdata_r),
		.host_rdata_o(pp_host_rdata_w),
		.host_rvalid_o(pp_host_rvalid_w),
		.host_err_o(pp_host_err_w),
		.svc_valid_i(1'b0),
		.svc_ready_o(),
		.svc_op_i(sv2v_uu_u_pp_ext_svc_op_i_0),
		.svc_index_i(sv2v_uu_u_pp_ext_svc_index_i_0),
		.svc_stream_id_i(sv2v_uu_u_pp_ext_svc_stream_id_i_0),
		.svc_da_i(sv2v_uu_u_pp_ext_svc_da_i_0),
		.svc_vid_i(sv2v_uu_u_pp_ext_svc_vid_i_0),
		.svc_max_frame_i(sv2v_uu_u_pp_ext_svc_max_frame_i_0),
		.svc_lstn_state_i(sv2v_uu_u_pp_ext_svc_lstn_state_i_0),
		.svc_rsp_valid_o(),
		.svc_rsp_status_o(),
		.svc_rsp_data_o(),
		.srp_class_a_prio_o(srp_class_a_prio_o),
		.srp_class_a_vid_o(srp_class_a_vid_o),
		.srp_domain_adopted_o(srp_domain_adopted_o),
		.srp_domain_change_o(srp_domain_change_o),
		.srp_tk_decl_state_o(srp_tk_decl_state_o),
		.srp_lstn_reg_state_o(srp_lstn_reg_state_o),
		.srp_active_o(srp_active_o),
		.srp_sr_admitted_o(srp_sr_admitted_o),
		.srp_granted_slope_bps_o(srp_granted_slope_bps_o),
		.srp_src_fail_code_o(srp_src_fail_code_o),
		.srp_src_fail_bridge_o(srp_src_fail_bridge_o),
		.srp_sum_slope_bps_o(srp_sum_slope_bps_o),
		.srp_over_limit_o(srp_over_limit_o),
		.srp_tk_reg_state_o(srp_tk_reg_state_o),
		.srp_lstn_decl_state_o(srp_lstn_decl_state_o),
		.srp_acc_latency_o(srp_acc_latency_o),
		.srp_snk_fail_code_o(srp_snk_fail_code_o),
		.acmp_declaring_o(acmp_declaring_o),
		.acmp_bound_o(acmp_bound_o),
		.acmp_bound_eid_o(acmp_bound_eid_o),
		.acmp_bound_sid_o(acmp_bound_sid_o),
		.acmp_bound_dmac_o(acmp_bound_dmac_o),
		.acmp_bound_vlan_o(acmp_bound_vlan_o),
		.adp_next_avail_index_o(adp_next_avail_index_o),
		.desc_mem_req_valid_o(desc_mem_req_valid_o),
		.desc_mem_req_ready_i(desc_mem_req_ready_i),
		.desc_mem_req_addr_o(desc_mem_req_addr_o),
		.desc_mem_req_beats_o(desc_mem_req_beats_o),
		.desc_mem_rsp_valid_i(desc_mem_rsp_valid_i),
		.desc_mem_rsp_ready_o(desc_mem_rsp_ready_o),
		.desc_mem_rsp_data_i(desc_mem_rsp_data_i),
		.desc_mem_rsp_last_i(desc_mem_rsp_last_i),
		.desc_mem_rsp_err_i(desc_mem_rsp_err_i),
		.resp_mem_req_valid_o(resp_mem_req_valid_o),
		.resp_mem_req_ready_i(resp_mem_req_ready_i),
		.resp_mem_req_addr_o(resp_mem_req_addr_o),
		.resp_mem_req_beats_o(resp_mem_req_beats_o),
		.resp_mem_rsp_valid_i(resp_mem_rsp_valid_i),
		.resp_mem_rsp_ready_o(resp_mem_rsp_ready_o),
		.resp_mem_rsp_data_i(resp_mem_rsp_data_i),
		.resp_mem_rsp_last_i(resp_mem_rsp_last_i),
		.resp_mem_rsp_err_i(resp_mem_rsp_err_i),
		.resp_mem_wr_valid_o(resp_mem_wr_valid_o),
		.resp_mem_wr_ready_i(resp_mem_wr_ready_i),
		.resp_mem_wr_addr_o(resp_mem_wr_addr_o),
		.resp_mem_wr_data_o(resp_mem_wr_data_o),
		.resp_mem_wr_strb_o(resp_mem_wr_strb_o),
		.resp_mem_wr_done_i(resp_mem_wr_done_i),
		.resp_mem_wr_err_i(resp_mem_wr_err_i),
		.maap_req_valid_o(maap_req_valid_o),
		.maap_req_ready_i(maap_req_ready_i),
		.maap_req_release_o(maap_req_release_o),
		.maap_req_src_o(maap_req_src_o),
		.maap_rsp_valid_i(maap_rsp_valid_i),
		.maap_rsp_ok_i(maap_rsp_ok_i),
		.maap_rsp_da_i(maap_rsp_da_i),
		.maap_conflict_valid_i(maap_conflict_valid_i),
		.maap_conflict_src_i(maap_conflict_src_i),
		.maap_conflict_ack_o(maap_conflict_ack_o),
		.cfg_maap_internal_i(cfg_maap_internal_i),
		.cfg_maap_count_i(cfg_maap_count_i),
		.cfg_maap_seed_offset_i(cfg_maap_seed_offset_i),
		.cfg_maap_seed_valid_i(cfg_maap_seed_valid_i),
		.maap_addr_o(maap_addr_o),
		.maap_addr_valid_o(maap_addr_valid_o),
		.maap_state_o(maap_state_o),
		.maap_conflicts_o(maap_conflicts_o),
		.maap_defends_o(maap_defends_o),
		.dbg_now_ms_o(dbg_now_ms_o)
	);
	reg [TDATA_WIDTH_P - 1:0] txp_data_r;
	reg [KEEP_W_C - 1:0] txp_keep_r;
	reg txp_valid_r;
	reg txp_last_r;
	reg [2:0] txp_idx_r;
	wire txp_take_w;
	assign txp_take_w = txp_valid_r & (tx_drain_i | m_axis_tx_tready);
	assign pp_tx_ready_w = ~txp_valid_r;
	always @(posedge clk_i or negedge rst_n)
		if (!rst_n) begin
			txp_data_r <= 1'sb0;
			txp_keep_r <= 1'sb0;
			txp_valid_r <= 1'b0;
			txp_last_r <= 1'b0;
			txp_idx_r <= 3'd0;
		end
		else begin
			if (txp_take_w) begin
				txp_valid_r <= 1'b0;
				txp_keep_r <= 1'sb0;
				txp_data_r <= 1'sb0;
			end
			if (pp_tx_valid_w & pp_tx_ready_w) begin
				txp_data_r[8 * txp_idx_r+:8] <= pp_tx_data_w;
				txp_keep_r[txp_idx_r] <= 1'b1;
				if (pp_tx_eof_w || (txp_idx_r == 3'd7)) begin
					txp_valid_r <= 1'b1;
					txp_last_r <= pp_tx_eof_w;
					txp_idx_r <= 3'd0;
				end
				else
					txp_idx_r <= txp_idx_r + 3'd1;
			end
		end
	assign m_axis_tx_tdata = txp_data_r;
	assign m_axis_tx_tkeep = txp_keep_r;
	assign m_axis_tx_tvalid = txp_valid_r & ~tx_drain_i;
	assign m_axis_tx_tlast = txp_last_r;
	always @(posedge clk_i or negedge rst_n)
		if (!rst_n) begin
			hb_pend_r <= 1'b0;
			hb_we_r <= 1'b0;
			hb_addr_r <= 20'd0;
			hb_wdata_r <= 32'd0;
			host_rdata_o <= 32'd0;
			host_ack_o <= 1'b0;
			host_err_o <= 1'b0;
		end
		else begin
			host_ack_o <= 1'b0;
			if (!hb_pend_r) begin
				if (host_req_i) begin
					hb_pend_r <= 1'b1;
					hb_we_r <= host_we_i;
					hb_addr_r <= host_addr_i;
					hb_wdata_r <= host_wdata_i;
				end
			end
			else if (pp_host_rvalid_w) begin
				hb_pend_r <= 1'b0;
				host_rdata_o <= pp_host_rdata_w;
				host_err_o <= pp_host_err_w;
				host_ack_o <= 1'b1;
			end
		end
	always @(posedge clk_i or negedge rst_n)
		if (!rst_n) begin
			rx_frames_o <= 16'd0;
			rx_drops_o <= 8'd0;
			tx_frames_o <= 16'd0;
		end
		else begin
			if (pp_rx_valid_w & pp_rx_last_w)
				rx_frames_o <= rx_frames_o + 16'd1;
			if (drop_evt_w & (rx_drops_o != 8'hff))
				rx_drops_o <= rx_drops_o + 8'd1;
			if ((pp_tx_valid_w & pp_tx_ready_w) & pp_tx_eof_w)
				tx_frames_o <= tx_frames_o + 16'd1;
		end
	assign restore_done_o = pp_restore_done_w;
	assign nvm_backed_o = nvm_backed_w;
	assign restore_blank_o = pp_restore_blank_w;
	assign restore_fail_o = pp_restore_fail_w || (pp_restore_done_w && walk_blind_r);
	initial _sv2v_0 = 0;
endmodule
`default_nettype wire
`default_nettype none
`default_nettype wire
`default_nettype none
module KL_nvm_backend (
	clk_i,
	rst_n,
	dev_req_i,
	dev_gnt_o,
	dev_op_i,
	dev_region_i,
	dev_offset_i,
	dev_len_i,
	dev_wvalid_i,
	dev_wready_o,
	dev_wdata_i,
	dev_rvalid_o,
	dev_rdata_o,
	dev_rready_i,
	dev_busy_o,
	dev_done_o,
	dev_err_o,
	mem_req_valid_o,
	mem_req_ready_i,
	mem_req_addr_o,
	mem_req_beats_o,
	mem_rsp_valid_i,
	mem_rsp_ready_o,
	mem_rsp_data_i,
	mem_rsp_last_i,
	mem_rsp_err_i,
	mem_wr_valid_o,
	mem_wr_ready_i,
	mem_wr_addr_o,
	mem_wr_data_o,
	mem_wr_strb_o,
	mem_wr_done_i,
	mem_wr_err_i,
	csr_sel_i,
	csr_we_i,
	csr_addr_i,
	csr_wdata_i,
	csr_rdata_o,
	pend_i,
	alarm_i,
	nvm_backed_o,
	nvm_dirty_o,
	nvm_stale_o,
	nvm_verdict_o,
	img_valid_o,
	nvm_pend_o,
	nvm_unres_o
);
	reg _sv2v_0;
	parameter [31:0] CLK_HZ_P = 125000000;
	parameter [31:0] N_STREAM_IN_P = 9;
	parameter [31:0] N_STREAM_OUT_P = 9;
	parameter [31:0] N_SPORT_IN_P = 8;
	parameter [31:0] N_SPORT_OUT_P = 8;
	parameter [31:0] N_AUDIO_UNIT_P = 1;
	parameter [31:0] N_CLK_DOM_P = 1;
	parameter [31:0] N_NAME_P = 99;
	parameter [31:0] T_ALIVE_MS_P = 2000;
	parameter [31:0] T_COMMIT_MS_P = 8000;
	parameter [31:0] T_HOLD_MS_P = 50;
	parameter [31:0] CAP_ID_W_P = 16;
	input wire clk_i;
	input wire rst_n;
	input wire dev_req_i;
	output wire dev_gnt_o;
	input wire [1:0] dev_op_i;
	input wire [7:0] dev_region_i;
	input wire [15:0] dev_offset_i;
	input wire [15:0] dev_len_i;
	input wire dev_wvalid_i;
	output wire dev_wready_o;
	input wire [7:0] dev_wdata_i;
	output wire dev_rvalid_o;
	output wire [7:0] dev_rdata_o;
	input wire dev_rready_i;
	output wire dev_busy_o;
	output wire dev_done_o;
	output wire dev_err_o;
	output wire mem_req_valid_o;
	input wire mem_req_ready_i;
	output wire [31:0] mem_req_addr_o;
	output wire [8:0] mem_req_beats_o;
	input wire mem_rsp_valid_i;
	output wire mem_rsp_ready_o;
	input wire [63:0] mem_rsp_data_i;
	input wire mem_rsp_last_i;
	input wire mem_rsp_err_i;
	output wire mem_wr_valid_o;
	input wire mem_wr_ready_i;
	output wire [31:0] mem_wr_addr_o;
	output wire [63:0] mem_wr_data_o;
	output wire [7:0] mem_wr_strb_o;
	input wire mem_wr_done_i;
	input wire mem_wr_err_i;
	input wire csr_sel_i;
	input wire csr_we_i;
	input wire [5:0] csr_addr_i;
	input wire [31:0] csr_wdata_i;
	output reg [31:0] csr_rdata_o;
	input wire pend_i;
	input wire alarm_i;
	output wire nvm_backed_o;
	output wire nvm_dirty_o;
	output wire nvm_stale_o;
	output wire [3:0] nvm_verdict_o;
	output wire img_valid_o;
	output wire nvm_pend_o;
	output wire nvm_unres_o;
	localparam [1:0] OP_READ_C = 2'd0;
	localparam [1:0] OP_WRITE_C = 2'd1;
	localparam [1:0] OP_ERASE_C = 2'd2;
	localparam [31:0] REC_HDR_C = 8;
	localparam [31:0] NAME_C = 64;
	localparam [31:0] ID_CFG_C = 'h0;
	localparam [31:0] ID_SUID_C = 'h1;
	localparam [31:0] ID_RATE_C = 'h2;
	localparam [31:0] ID_CLKS_C = 'ha;
	localparam [31:0] ID_MCR_C = 'h12;
	localparam [31:0] ID_BIND_C = 'h20;
	localparam [31:0] ID_FMTI_C = 'h30;
	localparam [31:0] ID_FMTO_C = 'h40;
	localparam [31:0] ID_PTOF_C = 'h50;
	localparam [31:0] ID_MAPI_C = 'h60;
	localparam [31:0] ID_MAPO_C = 'h70;
	localparam [31:0] ID_NAME_C = 'h80;
	localparam [31:0] SZ_CFG_C = 10;
	localparam [31:0] SZ_SUID_C = 16;
	localparam [31:0] SZ_RATE_C = 12;
	localparam [31:0] SZ_CLKS_C = 10;
	localparam [31:0] SZ_MCR_C = 74;
	localparam [31:0] SZ_BIND_C = 28;
	localparam [31:0] SZ_FMT_C = 16;
	localparam [31:0] SZ_PTOF_C = 12;
	localparam [31:0] SZ_NAME_C = REC_HDR_C + NAME_C;
	localparam [31:0] B_CFG_C = 0;
	localparam [31:0] B_SUID_C = B_CFG_C + SZ_CFG_C;
	localparam [31:0] B_RATE_C = B_SUID_C + SZ_SUID_C;
	localparam [31:0] B_CLKS_C = B_RATE_C + (N_AUDIO_UNIT_P * SZ_RATE_C);
	localparam [31:0] B_MCR_C = B_CLKS_C + (N_CLK_DOM_P * SZ_CLKS_C);
	localparam [31:0] B_BIND_C = B_MCR_C + (N_CLK_DOM_P * SZ_MCR_C);
	localparam [31:0] B_FMTI_C = B_BIND_C + (N_STREAM_IN_P * SZ_BIND_C);
	localparam [31:0] B_FMTO_C = B_FMTI_C + (N_STREAM_IN_P * SZ_FMT_C);
	localparam [31:0] B_PTOF_C = B_FMTO_C + (N_STREAM_OUT_P * SZ_FMT_C);
	localparam [31:0] B_MAPI_C = B_PTOF_C + (N_STREAM_OUT_P * SZ_PTOF_C);
	generate
		if ((((N_STREAM_IN_P < 1) || (N_STREAM_IN_P > 16)) || (N_STREAM_OUT_P < 1)) || (N_STREAM_OUT_P > 16)) begin : g_refuse_streams
			initial $display("Error [elaboration] $VALIDATION_STORAGE/reviews/r247-520-r1/hdl/milan/KL_nvm_backend.sv:280:5 - KL_nvm_backend.g_refuse_streams\n msg: ", "KL_nvm_backend: N_STREAM_IN_P=%0d / N_STREAM_OUT_P=%0d outside 1..16: the BINDING, FORMAT and OFFSET blocks hold sixteen ids each (0x20, 0x30, 0x40, 0x50).", N_STREAM_IN_P, N_STREAM_OUT_P);
		end
		else if ((((N_SPORT_IN_P < 1) || (N_SPORT_IN_P > 16)) || (N_SPORT_OUT_P < 1)) || (N_SPORT_OUT_P > 16)) begin : g_refuse_sports
			initial $display("Error [elaboration] $VALIDATION_STORAGE/reviews/r247-520-r1/hdl/milan/KL_nvm_backend.sv:283:5 - KL_nvm_backend.g_refuse_sports\n msg: ", "KL_nvm_backend: N_SPORT_IN_P=%0d / N_SPORT_OUT_P=%0d outside 1..16: the channel-map blocks hold sixteen ids each (0x60, 0x70) and the tables are indexed by csr_addr_i[3:0].", N_SPORT_IN_P, N_SPORT_OUT_P);
		end
		else if ((((N_AUDIO_UNIT_P < 1) || (N_AUDIO_UNIT_P > 8)) || (N_CLK_DOM_P < 1)) || (N_CLK_DOM_P > 8)) begin : g_refuse_units
			initial $display("Error [elaboration] $VALIDATION_STORAGE/reviews/r247-520-r1/hdl/milan/KL_nvm_backend.sv:286:5 - KL_nvm_backend.g_refuse_units\n msg: ", "KL_nvm_backend: N_AUDIO_UNIT_P=%0d / N_CLK_DOM_P=%0d outside 1..8: the RATE block (0x02) and the CLOCK_SOURCE block (0x0A) hold eight ids each.", N_AUDIO_UNIT_P, N_CLK_DOM_P);
		end
		else if ((N_NAME_P < 1) || (N_NAME_P > 128)) begin : g_refuse_names
			initial $display("Error [elaboration] $VALIDATION_STORAGE/reviews/r247-520-r1/hdl/milan/KL_nvm_backend.sv:289:5 - KL_nvm_backend.g_refuse_names\n msg: ", "KL_nvm_backend: N_NAME_P=%0d outside 1..128: the NAME block is 0x80..0xFF.", N_NAME_P);
		end
		else if (CLK_HZ_P < 1000) begin : g_refuse_clock
			initial $display("Error [elaboration] $VALIDATION_STORAGE/reviews/r247-520-r1/hdl/milan/KL_nvm_backend.sv:292:5 - KL_nvm_backend.g_refuse_clock\n msg: ", "KL_nvm_backend: CLK_HZ_P=%0d is below 1 kHz, so no millisecond tick can be derived for the section 9.4 deadlines.", CLK_HZ_P);
		end
		else if ((((T_ALIVE_MS_P < 1) || (T_ALIVE_MS_P > 65535)) || (T_COMMIT_MS_P < 1)) || (T_COMMIT_MS_P > 65535)) begin : g_refuse_deadlines
			initial $display("Error [elaboration] $VALIDATION_STORAGE/reviews/r247-520-r1/hdl/milan/KL_nvm_backend.sv:295:5 - KL_nvm_backend.g_refuse_deadlines\n msg: ", "KL_nvm_backend: T_ALIVE_MS_P=%0d / T_COMMIT_MS_P=%0d outside 1..65535: the deadline down-counters are sixteen bits wide.", T_ALIVE_MS_P, T_COMMIT_MS_P);
		end
		else if ((T_HOLD_MS_P < 1) || (T_HOLD_MS_P >= T_COMMIT_MS_P)) begin : g_refuse_hold
			initial $display("Error [elaboration] $VALIDATION_STORAGE/reviews/r247-520-r1/hdl/milan/KL_nvm_backend.sv:298:5 - KL_nvm_backend.g_refuse_hold\n msg: ", "KL_nvm_backend: T_HOLD_MS_P=%0d must be at least 1 and below T_COMMIT_MS_P=%0d: the hold bounds a copy, never a flash transaction.", T_HOLD_MS_P, T_COMMIT_MS_P);
		end
		else if ((CAP_ID_W_P < 2) || (CAP_ID_W_P > 16)) begin : g_refuse_capid
			initial $display("Error [elaboration] $VALIDATION_STORAGE/reviews/r247-520-r1/hdl/milan/KL_nvm_backend.sv:301:5 - KL_nvm_backend.g_refuse_capid\n msg: ", "KL_nvm_backend: CAP_ID_W_P=%0d outside 2..16: the identity rides the acknowledgement word's upper half.", CAP_ID_W_P);
		end
	endgenerate
	localparam [31:0] IDW_C = 9;
	reg [15:0] mapi_pref_r [0:N_SPORT_IN_P - 1];
	reg [15:0] mapi_len_r [0:N_SPORT_IN_P - 1];
	reg [15:0] mapo_pref_r [0:N_SPORT_OUT_P - 1];
	reg [15:0] mapo_len_r [0:N_SPORT_OUT_P - 1];
	localparam [31:0] MAPI_IW_C = (N_SPORT_IN_P > 1 ? $clog2(N_SPORT_IN_P) : 1);
	localparam [31:0] MAPO_IW_C = (N_SPORT_OUT_P > 1 ? $clog2(N_SPORT_OUT_P) : 1);
	reg [17:0] rec_base_w;
	reg [11:0] rec_len_w;
	reg rec_hit_w;
	wire [MAPI_IW_C - 1:0] mapi_idx_w;
	wire [MAPO_IW_C - 1:0] mapo_idx_w;
	wire [17:0] b_mapo_w;
	wire [17:0] b_name_w;
	wire [8:0] region_w;
	assign region_w = {1'b0, dev_region_i};
	function automatic [7:0] sv2v_cast_8;
		input reg [7:0] inp;
		sv2v_cast_8 = inp;
	endfunction
	function automatic [MAPI_IW_C - 1:0] sv2v_cast_049A4;
		input reg [MAPI_IW_C - 1:0] inp;
		sv2v_cast_049A4 = inp;
	endfunction
	assign mapi_idx_w = sv2v_cast_049A4(dev_region_i - sv2v_cast_8(ID_MAPI_C));
	function automatic [MAPO_IW_C - 1:0] sv2v_cast_C3F22;
		input reg [MAPO_IW_C - 1:0] inp;
		sv2v_cast_C3F22 = inp;
	endfunction
	assign mapo_idx_w = sv2v_cast_C3F22(dev_region_i - sv2v_cast_8(ID_MAPO_C));
	function automatic [17:0] sv2v_cast_18;
		input reg [17:0] inp;
		sv2v_cast_18 = inp;
	endfunction
	assign b_mapo_w = (sv2v_cast_18(B_MAPI_C) + sv2v_cast_18(mapi_pref_r[sv2v_cast_049A4(N_SPORT_IN_P - 1)])) + sv2v_cast_18(mapi_len_r[sv2v_cast_049A4(N_SPORT_IN_P - 1)]);
	assign b_name_w = (b_mapo_w + sv2v_cast_18(mapo_pref_r[sv2v_cast_C3F22(N_SPORT_OUT_P - 1)])) + sv2v_cast_18(mapo_len_r[sv2v_cast_C3F22(N_SPORT_OUT_P - 1)]);
	function automatic [8:0] sv2v_cast_8B400;
		input reg [8:0] inp;
		sv2v_cast_8B400 = inp;
	endfunction
	function automatic [11:0] sv2v_cast_12;
		input reg [11:0] inp;
		sv2v_cast_12 = inp;
	endfunction
	always @(*) begin
		if (_sv2v_0)
			;
		rec_base_w = 18'd0;
		rec_len_w = 12'd0;
		rec_hit_w = 1'b0;
		if (region_w == sv2v_cast_8B400(ID_CFG_C)) begin
			rec_base_w = sv2v_cast_18(B_CFG_C);
			rec_len_w = sv2v_cast_12(SZ_CFG_C);
			rec_hit_w = 1'b1;
		end
		else if (region_w == sv2v_cast_8B400(ID_SUID_C)) begin
			rec_base_w = sv2v_cast_18(B_SUID_C);
			rec_len_w = sv2v_cast_12(SZ_SUID_C);
			rec_hit_w = 1'b1;
		end
		else if ((region_w >= sv2v_cast_8B400(ID_RATE_C)) && (region_w < sv2v_cast_8B400(ID_RATE_C + N_AUDIO_UNIT_P))) begin
			rec_base_w = sv2v_cast_18(B_RATE_C) + (sv2v_cast_18(dev_region_i - sv2v_cast_8(ID_RATE_C)) * sv2v_cast_18(SZ_RATE_C));
			rec_len_w = sv2v_cast_12(SZ_RATE_C);
			rec_hit_w = 1'b1;
		end
		else if ((region_w >= sv2v_cast_8B400(ID_CLKS_C)) && (region_w < sv2v_cast_8B400(ID_CLKS_C + N_CLK_DOM_P))) begin
			rec_base_w = sv2v_cast_18(B_CLKS_C) + (sv2v_cast_18(dev_region_i - sv2v_cast_8(ID_CLKS_C)) * sv2v_cast_18(SZ_CLKS_C));
			rec_len_w = sv2v_cast_12(SZ_CLKS_C);
			rec_hit_w = 1'b1;
		end
		else if ((region_w >= sv2v_cast_8B400(ID_MCR_C)) && (region_w < sv2v_cast_8B400(ID_MCR_C + N_CLK_DOM_P))) begin
			rec_base_w = sv2v_cast_18(B_MCR_C) + (sv2v_cast_18(dev_region_i - sv2v_cast_8(ID_MCR_C)) * sv2v_cast_18(SZ_MCR_C));
			rec_len_w = sv2v_cast_12(SZ_MCR_C);
			rec_hit_w = 1'b1;
		end
		else if ((region_w >= sv2v_cast_8B400(ID_BIND_C)) && (region_w < sv2v_cast_8B400(ID_BIND_C + N_STREAM_IN_P))) begin
			rec_base_w = sv2v_cast_18(B_BIND_C) + (sv2v_cast_18(dev_region_i - sv2v_cast_8(ID_BIND_C)) * sv2v_cast_18(SZ_BIND_C));
			rec_len_w = sv2v_cast_12(SZ_BIND_C);
			rec_hit_w = 1'b1;
		end
		else if ((region_w >= sv2v_cast_8B400(ID_FMTI_C)) && (region_w < sv2v_cast_8B400(ID_FMTI_C + N_STREAM_IN_P))) begin
			rec_base_w = sv2v_cast_18(B_FMTI_C) + (sv2v_cast_18(dev_region_i - sv2v_cast_8(ID_FMTI_C)) * sv2v_cast_18(SZ_FMT_C));
			rec_len_w = sv2v_cast_12(SZ_FMT_C);
			rec_hit_w = 1'b1;
		end
		else if ((region_w >= sv2v_cast_8B400(ID_FMTO_C)) && (region_w < sv2v_cast_8B400(ID_FMTO_C + N_STREAM_OUT_P))) begin
			rec_base_w = sv2v_cast_18(B_FMTO_C) + (sv2v_cast_18(dev_region_i - sv2v_cast_8(ID_FMTO_C)) * sv2v_cast_18(SZ_FMT_C));
			rec_len_w = sv2v_cast_12(SZ_FMT_C);
			rec_hit_w = 1'b1;
		end
		else if ((region_w >= sv2v_cast_8B400(ID_PTOF_C)) && (region_w < sv2v_cast_8B400(ID_PTOF_C + N_STREAM_OUT_P))) begin
			rec_base_w = sv2v_cast_18(B_PTOF_C) + (sv2v_cast_18(dev_region_i - sv2v_cast_8(ID_PTOF_C)) * sv2v_cast_18(SZ_PTOF_C));
			rec_len_w = sv2v_cast_12(SZ_PTOF_C);
			rec_hit_w = 1'b1;
		end
		else if ((region_w >= sv2v_cast_8B400(ID_MAPI_C)) && (region_w < sv2v_cast_8B400(ID_MAPI_C + N_SPORT_IN_P))) begin
			rec_base_w = sv2v_cast_18(B_MAPI_C) + sv2v_cast_18(mapi_pref_r[mapi_idx_w]);
			rec_len_w = sv2v_cast_12(mapi_len_r[mapi_idx_w]);
			rec_hit_w = 1'b1;
		end
		else if ((region_w >= sv2v_cast_8B400(ID_MAPO_C)) && (region_w < sv2v_cast_8B400(ID_MAPO_C + N_SPORT_OUT_P))) begin
			rec_base_w = b_mapo_w + sv2v_cast_18(mapo_pref_r[mapo_idx_w]);
			rec_len_w = sv2v_cast_12(mapo_len_r[mapo_idx_w]);
			rec_hit_w = 1'b1;
		end
		else if ((region_w >= sv2v_cast_8B400(ID_NAME_C)) && (region_w < sv2v_cast_8B400(ID_NAME_C + N_NAME_P))) begin
			rec_base_w = b_name_w + (sv2v_cast_18(dev_region_i - sv2v_cast_8(ID_NAME_C)) * sv2v_cast_18(SZ_NAME_C));
			rec_len_w = sv2v_cast_12(SZ_NAME_C);
			rec_hit_w = 1'b1;
		end
	end
	localparam [4:0] R_IMG_BASE_C = 5'd0;
	localparam [4:0] R_IMG_LEN_C = 5'd1;
	localparam [4:0] R_SEQ_C = 5'd2;
	localparam [4:0] R_STAT_C = 5'd3;
	localparam [4:0] R_ACK_C = 5'd4;
	localparam [4:0] R_CAPID_C = 5'd5;
	localparam [4:0] R_OWN0_C = 5'd8;
	localparam [7:0] CAP_TAG_C = 8'hc3;
	localparam [3:0] VD_ERASE_C = 4'd11;
	localparam [3:0] VD_VERIFY_C = 4'd13;
	reg [31:0] img_base_r;
	reg [31:0] img_len_r;
	reg [31:0] seq_r;
	reg [3:0] verdict_r;
	reg img_valid_r;
	reg backed_r;
	reg stale_r;
	reg ever_backed_r;
	wire reg_we_w;
	wire hb_kick_w;
	wire commit_ack_w;
	wire commit_start_w;
	wire img_cfg_w;
	wire img_live_w;
	wire arm_w;
	wire attest_w;
	wire release_w;
	wire reload_w;
	wire rebase_w;
	wire map_we_w;
	wire fail_rep_w;
	wire reload_ok_w;
	wire [CAP_ID_W_P - 1:0] ack_id_w;
	assign reg_we_w = (csr_sel_i & csr_we_i) & ~csr_addr_i[5];
	assign map_we_w = (csr_sel_i & csr_we_i) & csr_addr_i[5];
	assign hb_kick_w = (reg_we_w & (csr_addr_i[4:0] == R_ACK_C)) & csr_wdata_i[0];
	assign commit_ack_w = (reg_we_w & (csr_addr_i[4:0] == R_ACK_C)) & csr_wdata_i[1];
	assign commit_start_w = (reg_we_w & (csr_addr_i[4:0] == R_ACK_C)) & csr_wdata_i[2];
	assign arm_w = (reg_we_w & (csr_addr_i[4:0] == R_ACK_C)) & csr_wdata_i[3];
	assign attest_w = (reg_we_w & (csr_addr_i[4:0] == R_ACK_C)) & csr_wdata_i[4];
	assign release_w = (reg_we_w & (csr_addr_i[4:0] == R_ACK_C)) & csr_wdata_i[5];
	assign reload_w = (reg_we_w & (csr_addr_i[4:0] == R_ACK_C)) & csr_wdata_i[6];
	assign ack_id_w = csr_wdata_i[16+:CAP_ID_W_P];
	assign rebase_w = (reg_we_w & ((csr_addr_i[4:0] == R_IMG_BASE_C) | (csr_addr_i[4:0] == R_IMG_LEN_C))) | map_we_w;
	assign fail_rep_w = ((reg_we_w & (csr_addr_i[4:0] == R_STAT_C)) & (csr_wdata_i[3:0] >= VD_ERASE_C)) & (csr_wdata_i[3:0] <= VD_VERIFY_C);
	assign img_cfg_w = img_len_r != 32'd0;
	assign img_live_w = img_cfg_w & img_valid_r;
	always @(posedge clk_i)
		if (!rst_n) begin
			img_base_r <= 32'd0;
			img_len_r <= 32'd0;
			seq_r <= 32'd0;
			verdict_r <= 4'd0;
			img_valid_r <= 1'b0;
		end
		else if (reg_we_w)
			case (csr_addr_i[4:0])
				R_IMG_BASE_C: begin
					img_base_r <= csr_wdata_i;
					img_valid_r <= 1'b0;
				end
				R_IMG_LEN_C: begin
					img_len_r <= csr_wdata_i;
					img_valid_r <= 1'b0;
				end
				R_SEQ_C: seq_r <= csr_wdata_i;
				R_STAT_C: begin
					verdict_r <= csr_wdata_i[3:0];
					img_valid_r <= csr_wdata_i[4];
				end
				default:
					;
			endcase
	function automatic [31:0] sv2v_cast_32;
		input reg [31:0] inp;
		sv2v_cast_32 = inp;
	endfunction
	always @(posedge clk_i)
		if ((csr_sel_i && csr_we_i) && csr_addr_i[5]) begin
			if (!csr_addr_i[4]) begin
				if (sv2v_cast_32(csr_addr_i[3:0]) < N_SPORT_IN_P) begin
					mapi_pref_r[sv2v_cast_049A4(csr_addr_i[3:0])] <= csr_wdata_i[15:0];
					mapi_len_r[sv2v_cast_049A4(csr_addr_i[3:0])] <= csr_wdata_i[31:16];
				end
			end
			else if (sv2v_cast_32(csr_addr_i[3:0]) < N_SPORT_OUT_P) begin
				mapo_pref_r[sv2v_cast_C3F22(csr_addr_i[3:0])] <= csr_wdata_i[15:0];
				mapo_len_r[sv2v_cast_C3F22(csr_addr_i[3:0])] <= csr_wdata_i[31:16];
			end
		end
	reg commit_busy_r;
	wire dev_busy_w;
	reg cap_open_r;
	reg cap_hold_r;
	reg cap_valid_r;
	reg cap_att_r;
	reg ack_ref_r;
	reg arm_ref_r;
	reg [CAP_ID_W_P - 1:0] cap_id_r;
	localparam [31:0] HOLD_W_C = $clog2(T_HOLD_MS_P + 1);
	reg [HOLD_W_C - 1:0] hold_r;
	reg dirty_live_r;
	reg dirty_cap_r;
	reg pend_r;
	reg [255:0] open_r;
	wire unres_w;
	wire dirty_img_w;
	wire arm_ok_w;
	wire att_ok_w;
	wire ack_ok_w;
	wire close_w;
	wire drop_w;
	wire hold_exp_w;
	wire void_grant_w;
	wire gnt_opmut_w;
	wire rec_close_w;
	reg [7:0] op_region_r;
	reg op_mut_r;
	reg op_full_r;
	reg set_q_r;
	reg ld_ok_r;
	reg ld_pend_r;
	reg rl_ref_r;
	reg ld_acc_r;
	wire inflight_w;
	wire win_live_w;
	wire mut_wait_w;
	reg mut_defer_r;
	wire pend_w;
	assign unres_w = |open_r;
	assign dirty_img_w = dirty_live_r | dirty_cap_r;
	always @(*) begin
		if (_sv2v_0)
			;
		if (csr_addr_i[5]) begin
			if (!csr_addr_i[4])
				csr_rdata_o = {mapi_len_r[sv2v_cast_049A4(csr_addr_i[3:0])], mapi_pref_r[sv2v_cast_049A4(csr_addr_i[3:0])]};
			else
				csr_rdata_o = {mapo_len_r[sv2v_cast_C3F22(csr_addr_i[3:0])], mapo_pref_r[sv2v_cast_C3F22(csr_addr_i[3:0])]};
		end
		else if (csr_addr_i[4:3] == R_OWN0_C[4:3])
			csr_rdata_o = open_r[32 * csr_addr_i[2:0]+:32];
		else
			case (csr_addr_i[4:0])
				R_IMG_BASE_C: csr_rdata_o = img_base_r;
				R_IMG_LEN_C: csr_rdata_o = img_len_r;
				R_SEQ_C: csr_rdata_o = seq_r;
				R_STAT_C: csr_rdata_o = {CAP_TAG_C, unres_w, pend_w, arm_ref_r, ack_ref_r, cap_att_r, cap_valid_r, cap_hold_r, cap_open_r, verdict_r, rl_ref_r, commit_busy_r, nvm_stale_o, dirty_img_w, img_valid_r, backed_r, img_cfg_w, dev_busy_w, ld_pend_r, ld_acc_r, 2'd0};
				R_CAPID_C: csr_rdata_o = sv2v_cast_32(cap_id_r);
				default: csr_rdata_o = 32'd0;
			endcase
	end
	localparam [31:0] MS_DIV_C = (CLK_HZ_P >= 1000 ? CLK_HZ_P / 1000 : 1);
	localparam [31:0] MS_W_C = (MS_DIV_C > 1 ? $clog2(MS_DIV_C) : 1);
	reg [MS_W_C - 1:0] ms_div_r;
	wire ms_tick_w;
	reg [15:0] alive_r;
	reg [15:0] commit_r;
	assign ms_tick_w = ms_div_r == {MS_W_C {1'sb0}};
	function automatic [MS_W_C - 1:0] sv2v_cast_63AC9;
		input reg [MS_W_C - 1:0] inp;
		sv2v_cast_63AC9 = inp;
	endfunction
	always @(posedge clk_i)
		if (!rst_n)
			ms_div_r <= sv2v_cast_63AC9(MS_DIV_C - 1);
		else
			ms_div_r <= (ms_tick_w ? sv2v_cast_63AC9(MS_DIV_C - 1) : ms_div_r - 1'b1);
	wire alive_exp_w;
	wire commit_exp_w;
	wire loss_ev_w;
	wire loss_w;
	wire backed_n_w;
	wire stale_n_w;
	wire comp_n_w;
	wire dirty_live_n_w;
	wire dirty_cap_n_w;
	assign alive_exp_w = (ms_tick_w & (alive_r == 16'd1)) & ~hb_kick_w;
	assign commit_exp_w = ((((commit_busy_r & ms_tick_w) & (commit_r == 16'd1)) & ~commit_start_w) & ~ack_ok_w) & ~release_w;
	assign loss_ev_w = ((alive_exp_w | commit_exp_w) | fail_rep_w) | alarm_i;
	assign loss_w = loss_ev_w & ever_backed_r;
	assign backed_n_w = (loss_ev_w ? 1'b0 : (hb_kick_w ? 1'b1 : backed_r));
	assign comp_n_w = dirty_live_n_w | dirty_cap_n_w;
	assign stale_n_w = (loss_w ? 1'b1 : (backed_n_w & ~comp_n_w ? 1'b0 : stale_r));
	function automatic [15:0] sv2v_cast_16;
		input reg [15:0] inp;
		sv2v_cast_16 = inp;
	endfunction
	always @(posedge clk_i)
		if (!rst_n) begin
			alive_r <= 16'd0;
			commit_r <= 16'd0;
			commit_busy_r <= 1'b0;
			backed_r <= 1'b0;
			stale_r <= 1'b0;
			ever_backed_r <= 1'b0;
		end
		else begin
			if (hb_kick_w) begin
				alive_r <= sv2v_cast_16(T_ALIVE_MS_P);
				ever_backed_r <= 1'b1;
			end
			else if (ms_tick_w && (alive_r != 16'd0))
				alive_r <= alive_r - 16'd1;
			if (commit_start_w) begin
				commit_r <= sv2v_cast_16(T_COMMIT_MS_P);
				commit_busy_r <= 1'b1;
			end
			else if (((ack_ok_w || release_w) || reload_ok_w) || rebase_w)
				commit_busy_r <= 1'b0;
			else if ((commit_busy_r && ms_tick_w) && (commit_r != 16'd0)) begin
				commit_r <= commit_r - 16'd1;
				if (commit_r == 16'd1)
					commit_busy_r <= 1'b0;
			end
			backed_r <= backed_n_w;
			stale_r <= stale_n_w;
		end
	wire void_hard_w;
	assign void_hard_w = reload_ok_w | rebase_w;
	assign arm_ok_w = (((((arm_w & img_cfg_w) & img_valid_r) & ~cap_open_r) & ~void_hard_w) & ~mut_defer_r) & ld_acc_r;
	function automatic signed [HOLD_W_C - 1:0] sv2v_cast_BEA96_signed;
		input reg signed [HOLD_W_C - 1:0] inp;
		sv2v_cast_BEA96_signed = inp;
	endfunction
	assign hold_exp_w = (cap_hold_r & ms_tick_w) & (hold_r == sv2v_cast_BEA96_signed(1));
	assign void_grant_w = (gnt_opmut_w & cap_open_r) & ~cap_att_r;
	assign att_ok_w = ((((attest_w & cap_open_r) & ~cap_att_r) & cap_valid_r) & ~void_grant_w) & ~void_hard_w;
	assign ack_ok_w = ((((commit_ack_w & cap_open_r) & cap_att_r) & cap_valid_r) & (ack_id_w == cap_id_r)) & ~void_hard_w;
	assign close_w = cap_open_r & (((commit_ack_w & (ack_id_w == cap_id_r)) | release_w) | void_hard_w);
	assign drop_w = close_w & ~ack_ok_w;
	assign dirty_live_n_w = (rec_close_w ? 1'b1 : (reload_ok_w ? 1'b0 : (arm_ok_w ? 1'b0 : (drop_w ? dirty_live_r | dirty_cap_r : dirty_live_r))));
	assign dirty_cap_n_w = (reload_ok_w ? 1'b0 : (arm_ok_w ? dirty_live_r : (ack_ok_w | drop_w ? 1'b0 : dirty_cap_r)));
	function automatic [HOLD_W_C - 1:0] sv2v_cast_BEA96;
		input reg [HOLD_W_C - 1:0] inp;
		sv2v_cast_BEA96 = inp;
	endfunction
	always @(posedge clk_i)
		if (!rst_n) begin
			cap_open_r <= 1'b0;
			cap_hold_r <= 1'b0;
			cap_valid_r <= 1'b0;
			cap_att_r <= 1'b0;
			cap_id_r <= 1'sb0;
			hold_r <= 1'sb0;
			ack_ref_r <= 1'b0;
			arm_ref_r <= 1'b0;
			dirty_live_r <= 1'b0;
			dirty_cap_r <= 1'b0;
			pend_r <= 1'b0;
		end
		else begin
			cap_open_r <= (arm_ok_w ? 1'b1 : (close_w ? 1'b0 : cap_open_r));
			cap_hold_r <= (arm_ok_w ? 1'b1 : ((close_w | attest_w) | hold_exp_w ? 1'b0 : cap_hold_r));
			cap_valid_r <= (arm_ok_w ? 1'b1 : (close_w | void_grant_w ? 1'b0 : cap_valid_r));
			cap_att_r <= (arm_ok_w ? 1'b0 : (close_w ? 1'b0 : (att_ok_w ? 1'b1 : cap_att_r)));
			if (arm_ok_w)
				cap_id_r <= cap_id_r + 1'b1;
			if (arm_ok_w)
				hold_r <= sv2v_cast_BEA96(T_HOLD_MS_P);
			else if ((cap_hold_r && ms_tick_w) && (hold_r != {HOLD_W_C {1'sb0}}))
				hold_r <= hold_r - 1'b1;
			if (commit_ack_w)
				ack_ref_r <= ~ack_ok_w;
			else if (arm_ok_w)
				ack_ref_r <= 1'b0;
			if (arm_w)
				arm_ref_r <= ~arm_ok_w;
			dirty_live_r <= dirty_live_n_w;
			dirty_cap_r <= dirty_cap_n_w;
			pend_r <= pend_i;
		end
	assign pend_w = pend_r | unres_w;
	assign nvm_backed_o = backed_r;
	assign nvm_dirty_o = dirty_img_w;
	assign nvm_stale_o = stale_r;
	assign nvm_verdict_o = verdict_r;
	assign img_valid_o = img_valid_r;
	assign nvm_pend_o = pend_w;
	assign nvm_unres_o = unres_w;
	reg [3:0] st_r;
	reg [31:0] addr_r;
	reg [15:0] cnt_r;
	reg [7:0] byte_r;
	reg gnt_r;
	reg done_r;
	reg err_r;
	reg was_write_r;
	wire [15:0] eff_len_w;
	wire [31:0] span_end_w;
	wire span_ok_w;
	reg wc_valid_r;
	reg [28:0] wc_addr_r;
	reg [63:0] wc_data_r;
	wire wc_hit_w;
	assign eff_len_w = ((dev_op_i == OP_ERASE_C) && (dev_len_i == 16'd0) ? sv2v_cast_16(rec_len_w) : dev_len_i);
	assign span_end_w = (sv2v_cast_32(rec_base_w) + sv2v_cast_32(dev_offset_i)) + sv2v_cast_32(eff_len_w);
	assign span_ok_w = (rec_hit_w && (({16'd0, dev_offset_i} + {16'd0, eff_len_w}) <= sv2v_cast_32(rec_len_w))) && (span_end_w <= img_len_r);
	assign wc_hit_w = wc_valid_r && (wc_addr_r == addr_r[31:3]);
	wire mut_req_w;
	wire gnt_now_w;
	assign mut_req_w = (dev_op_i == OP_WRITE_C) || (dev_op_i == OP_ERASE_C);
	assign gnt_now_w = ((st_r == 4'd0) && dev_req_i) && !((cap_hold_r | arm_ok_w) && mut_req_w);
	assign gnt_opmut_w = (((gnt_now_w && mut_req_w) && img_cfg_w) && span_ok_w) && (eff_len_w != 16'd0);
	assign rec_close_w = ((done_r & was_write_r) & op_mut_r) & op_full_r;
	assign mut_wait_w = ((dev_req_i & mut_req_w) & (st_r == 4'd0)) & ~gnt_now_w;
	always @(posedge clk_i)
		if (!rst_n)
			mut_defer_r <= 1'b0;
		else
			mut_defer_r <= mut_wait_w;
	always @(posedge clk_i)
		if (!rst_n) begin
			st_r <= 4'd0;
			addr_r <= 32'd0;
			cnt_r <= 16'd0;
			byte_r <= 8'd0;
			gnt_r <= 1'b0;
			done_r <= 1'b0;
			err_r <= 1'b0;
			was_write_r <= 1'b0;
			wc_valid_r <= 1'b0;
			wc_addr_r <= 29'd0;
			wc_data_r <= 64'd0;
			op_region_r <= 8'd0;
			op_mut_r <= 1'b0;
			op_full_r <= 1'b0;
			set_q_r <= 1'b0;
		end
		else begin
			gnt_r <= 1'b0;
			done_r <= 1'b0;
			err_r <= 1'b0;
			set_q_r <= gnt_opmut_w;
			if (reg_we_w && (csr_addr_i[4:0] == R_IMG_BASE_C))
				wc_valid_r <= 1'b0;
			case (st_r)
				4'd0:
					if (gnt_now_w) begin
						gnt_r <= 1'b1;
						op_region_r <= dev_region_i;
						op_mut_r <= gnt_opmut_w;
						op_full_r <= ((dev_op_i == OP_WRITE_C) && (dev_offset_i == 16'd0)) && (eff_len_w == sv2v_cast_16(rec_len_w));
						addr_r <= (img_base_r + sv2v_cast_32(rec_base_w)) + sv2v_cast_32(dev_offset_i);
						cnt_r <= eff_len_w;
						was_write_r <= dev_op_i == OP_WRITE_C;
						if (!img_cfg_w) begin
							if ((dev_op_i == OP_READ_C) && (dev_len_i != 16'd0))
								st_r <= 4'd1;
							else if ((dev_op_i == OP_WRITE_C) && (dev_len_i != 16'd0))
								st_r <= 4'd8;
							else
								st_r <= 4'd11;
						end
						else if (!span_ok_w)
							st_r <= 4'd12;
						else if (eff_len_w == 16'd0)
							st_r <= 4'd11;
						else
							case (dev_op_i)
								OP_READ_C: st_r <= (img_live_w ? 4'd2 : 4'd1);
								OP_WRITE_C: begin
									st_r <= 4'd5;
									wc_valid_r <= 1'b0;
								end
								default: begin
									st_r <= 4'd9;
									wc_valid_r <= 1'b0;
								end
							endcase
					end
				4'd1:
					if (dev_rready_i) begin
						if (cnt_r <= 16'd1)
							st_r <= 4'd11;
						else
							cnt_r <= cnt_r - 16'd1;
					end
				4'd2:
					if (wc_hit_w) begin
						byte_r <= wc_data_r[63 - (8 * addr_r[2:0])-:8];
						st_r <= 4'd4;
					end
					else if (mem_req_ready_i)
						st_r <= 4'd3;
				4'd3:
					if (mem_rsp_valid_i) begin
						if (mem_rsp_err_i) begin
							wc_valid_r <= 1'b0;
							st_r <= 4'd12;
						end
						else if (mem_rsp_last_i) begin
							wc_valid_r <= 1'b1;
							wc_addr_r <= addr_r[31:3];
							wc_data_r <= mem_rsp_data_i;
							byte_r <= mem_rsp_data_i[63 - (8 * addr_r[2:0])-:8];
							st_r <= 4'd4;
						end
					end
				4'd4:
					if (dev_rready_i) begin
						addr_r <= addr_r + 32'd1;
						if (cnt_r <= 16'd1)
							st_r <= 4'd11;
						else begin
							cnt_r <= cnt_r - 16'd1;
							st_r <= 4'd2;
						end
					end
				4'd5:
					if (dev_wvalid_i) begin
						byte_r <= dev_wdata_i;
						st_r <= 4'd6;
					end
				4'd6:
					if (mem_wr_ready_i) begin
						if (mem_wr_done_i) begin
							if (mem_wr_err_i)
								st_r <= 4'd12;
							else begin
								addr_r <= addr_r + 32'd1;
								if (cnt_r <= 16'd1)
									st_r <= 4'd11;
								else begin
									cnt_r <= cnt_r - 16'd1;
									st_r <= 4'd5;
								end
							end
						end
						else
							st_r <= 4'd7;
					end
				4'd7:
					if (mem_wr_done_i) begin
						if (mem_wr_err_i)
							st_r <= 4'd12;
						else begin
							addr_r <= addr_r + 32'd1;
							if (cnt_r <= 16'd1)
								st_r <= 4'd11;
							else begin
								cnt_r <= cnt_r - 16'd1;
								st_r <= 4'd5;
							end
						end
					end
				4'd8:
					if (dev_wvalid_i) begin
						if (cnt_r <= 16'd1)
							st_r <= 4'd11;
						else
							cnt_r <= cnt_r - 16'd1;
					end
				4'd9:
					if (mem_wr_ready_i) begin
						if (mem_wr_done_i) begin
							if (mem_wr_err_i)
								st_r <= 4'd12;
							else begin
								addr_r <= addr_r + 32'd1;
								if (cnt_r <= 16'd1)
									st_r <= 4'd11;
								else
									cnt_r <= cnt_r - 16'd1;
							end
						end
						else
							st_r <= 4'd10;
					end
				4'd10:
					if (mem_wr_done_i) begin
						if (mem_wr_err_i)
							st_r <= 4'd12;
						else begin
							addr_r <= addr_r + 32'd1;
							if (cnt_r <= 16'd1)
								st_r <= 4'd11;
							else begin
								cnt_r <= cnt_r - 16'd1;
								st_r <= 4'd9;
							end
						end
					end
				4'd11: begin
					done_r <= 1'b1;
					st_r <= 4'd0;
				end
				default: begin
					err_r <= 1'b1;
					st_r <= 4'd0;
				end
			endcase
		end
	assign mem_req_valid_o = (st_r == 4'd2) && !wc_hit_w;
	assign mem_req_addr_o = {addr_r[31:3], 3'b000};
	assign mem_req_beats_o = 9'd1;
	assign mem_rsp_ready_o = st_r == 4'd3;
	assign mem_wr_valid_o = (st_r == 4'd6) || (st_r == 4'd9);
	assign mem_wr_addr_o = {addr_r[31:3], 3'b000};
	assign mem_wr_data_o = (st_r == 4'd9 ? {64 {1'b1}} : {8 {byte_r}});
	assign mem_wr_strb_o = 8'd1 << addr_r[2:0];
	assign dev_busy_w = st_r != 4'd0;
	assign dev_gnt_o = gnt_r;
	assign dev_wready_o = (st_r == 4'd5) || (st_r == 4'd8);
	assign dev_rvalid_o = (st_r == 4'd4) || (st_r == 4'd1);
	assign dev_rdata_o = (st_r == 4'd1 ? 8'hff : byte_r);
	assign dev_busy_o = dev_busy_w;
	assign dev_done_o = done_r;
	assign dev_err_o = err_r;
	function automatic alloc_f;
		input reg [31:0] id;
		alloc_f = (((((((((((id == ID_CFG_C) || (id == ID_SUID_C)) || ((id >= ID_RATE_C) && (id < (ID_RATE_C + N_AUDIO_UNIT_P)))) || ((id >= ID_CLKS_C) && (id < (ID_CLKS_C + N_CLK_DOM_P)))) || ((id >= ID_MCR_C) && (id < (ID_MCR_C + N_CLK_DOM_P)))) || ((id >= ID_BIND_C) && (id < (ID_BIND_C + N_STREAM_IN_P)))) || ((id >= ID_FMTI_C) && (id < (ID_FMTI_C + N_STREAM_IN_P)))) || ((id >= ID_FMTO_C) && (id < (ID_FMTO_C + N_STREAM_OUT_P)))) || ((id >= ID_PTOF_C) && (id < (ID_PTOF_C + N_STREAM_OUT_P)))) || ((id >= ID_MAPI_C) && (id < (ID_MAPI_C + N_SPORT_IN_P)))) || ((id >= ID_MAPO_C) && (id < (ID_MAPO_C + N_SPORT_OUT_P)))) || ((id >= ID_NAME_C) && (id < (ID_NAME_C + N_NAME_P)));
	endfunction
	assign inflight_w = (st_r != 4'd0) & op_mut_r;
	assign reload_ok_w = (reload_w & ld_ok_r) & ld_pend_r;
	assign win_live_w = (gnt_now_w & img_cfg_w) & ~ld_ok_r;
	always @(posedge clk_i)
		if (!rst_n) begin
			ld_ok_r <= 1'b0;
			ld_pend_r <= 1'b1;
			ld_acc_r <= 1'b0;
			rl_ref_r <= 1'b0;
		end
		else begin
			ld_ok_r <= (gnt_opmut_w ? 1'b0 : (rebase_w ? ~inflight_w : ld_ok_r));
			if (reload_ok_w | win_live_w)
				ld_pend_r <= 1'b0;
			if (reload_ok_w)
				ld_acc_r <= 1'b1;
			if (reload_w)
				rl_ref_r <= ~reload_ok_w;
		end
	genvar _gv_gi_1;
	function automatic signed [7:0] sv2v_cast_8_signed;
		input reg signed [7:0] inp;
		sv2v_cast_8_signed = inp;
	endfunction
	generate
		for (_gv_gi_1 = 0; _gv_gi_1 < 256; _gv_gi_1 = _gv_gi_1 + 1) begin : g_own
			localparam gi = _gv_gi_1;
			if (alloc_f(gi)) begin : g_alloc
				wire hit_w;
				wire open_n_w;
				assign hit_w = op_region_r == sv2v_cast_8_signed(gi);
				assign open_n_w = (rebase_w | (set_q_r & hit_w)) | ((~reload_ok_w & open_r[gi]) & ~(rec_close_w & hit_w));
				always @(posedge clk_i)
					if (!rst_n)
						open_r[gi] <= 1'b1;
					else
						open_r[gi] <= open_n_w;
			end
			else begin : g_none
				wire [1:1] sv2v_tmp_0D14C;
				assign sv2v_tmp_0D14C = 1'b0;
				always @(*) open_r[gi] = sv2v_tmp_0D14C;
			end
		end
	endgenerate
	initial _sv2v_0 = 0;
endmodule
`default_nettype wire

module tcam (
	clk,
	q
);
	parameter signed [31:0] N_NAME_P = 235;
	parameter signed [31:0] K = 3;
	input wire clk;
	output reg q;
	generate
		if (N_NAME_P > 128) begin : g1
			initial $display("Error [elaboration] p.sv:3:5 - tcam.g1\n msg: ", "names %0d too many", N_NAME_P);
		end
		if (N_NAME_P > 200) begin : g2
			initial begin
				$display("Fatal [elaboration] p.sv:6:5 - tcam.g2\n msg: ", "fatal names");
				$finish(1);
			end
		end
		if (N_NAME_P > 201) begin : g3
			initial begin
				$display("Fatal [elaboration] p.sv:9:5 - tcam.g3");
				$finish;
			end
		end
		if (N_NAME_P > 202) begin : g4
			initial $display("Error [elaboration] p.sv:12:5 - tcam.g4");
		end
		if (K == 3) begin : g5
			initial $display("Warning [elaboration] p.sv:15:5 - tcam.g5\n msg: ", "just a warning");
			initial $display("Info [elaboration] p.sv:16:5 - tcam.g5\n msg: ", "info");
		end
		if (N_NAME_P > 203) begin : g6
			initial $display("Error [%0t] p.sv:19:13 - tcam.g6.<unnamed_block>\n msg: ", $time, "procedural error");
		end
	endgenerate
	initial if (N_NAME_P > 204) begin
		$display("Fatal [%0t] p.sv:22:25 - tcam.<unnamed_block>.<unnamed_block>\n msg: ", $time, "initial fatal");
		$finish(2);
	end
	always @(posedge clk) q <= ~q;
endmodule

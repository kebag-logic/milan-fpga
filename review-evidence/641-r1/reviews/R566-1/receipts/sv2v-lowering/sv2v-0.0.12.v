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
			$error("names %0d too many", N_NAME_P);
		end
		if (N_NAME_P > 200) begin : g2
			$fatal(1, "fatal names");
		end
		if (N_NAME_P > 201) begin : g3
			$fatal();
		end
		if (N_NAME_P > 202) begin : g4
			$error();
		end
		if (K == 3) begin : g5
			$warning("just a warning");
			$info("info");
		end
		if (N_NAME_P > 203) begin : g6
			initial $error("procedural error");
		end
	endgenerate
	initial if (N_NAME_P > 204)
		$fatal(2, "initial fatal");
	always @(posedge clk) q <= ~q;
endmodule

/* Machine-generated using Migen */
module gmii_capture(
	input sys_clk,
	input pads_rx_dv,
	input [7:0] pads_rx_data,
	input reset,
	output source_valid,
	output source_last,
	output [7:0] source_payload_data
);

wire sys_rst;
wire capture_pads_rx_dv;
wire [7:0] capture_pads_rx_data;
reg rx_dv = 1'd0;
reg [7:0] rx_data = 8'd0;
reg rx_reset = 1'd1;

// synthesis translate_off
reg dummy_s;
initial dummy_s <= 1'd0;
// synthesis translate_on

assign sys_rst = reset;
assign source_valid = (rx_dv & (~rx_reset));
assign source_payload_data = (rx_reset ? 1'd0 : rx_data);
assign source_last = ((~capture_pads_rx_dv) & source_valid);

always @(posedge sys_clk) begin
	rx_dv <= capture_pads_rx_dv;
	rx_data <= capture_pads_rx_data;
	rx_reset <= sys_rst;
	if (sys_rst) begin
	end
end

(* dont_touch = "true" *) LUT2 #(
	.INIT(2'd2)
) LUT2 (
	.I0(pads_rx_dv),
	.I1(reset),
	.O(capture_pads_rx_dv)
);

(* dont_touch = "true" *) LUT2 #(
	.INIT(2'd2)
) LUT2_1 (
	.I0(pads_rx_data[0]),
	.I1(reset),
	.O(capture_pads_rx_data[0])
);

(* dont_touch = "true" *) LUT2 #(
	.INIT(2'd2)
) LUT2_2 (
	.I0(pads_rx_data[1]),
	.I1(reset),
	.O(capture_pads_rx_data[1])
);

(* dont_touch = "true" *) LUT2 #(
	.INIT(2'd2)
) LUT2_3 (
	.I0(pads_rx_data[2]),
	.I1(reset),
	.O(capture_pads_rx_data[2])
);

(* dont_touch = "true" *) LUT2 #(
	.INIT(2'd2)
) LUT2_4 (
	.I0(pads_rx_data[3]),
	.I1(reset),
	.O(capture_pads_rx_data[3])
);

(* dont_touch = "true" *) LUT2 #(
	.INIT(2'd2)
) LUT2_5 (
	.I0(pads_rx_data[4]),
	.I1(reset),
	.O(capture_pads_rx_data[4])
);

(* dont_touch = "true" *) LUT2 #(
	.INIT(2'd2)
) LUT2_6 (
	.I0(pads_rx_data[5]),
	.I1(reset),
	.O(capture_pads_rx_data[5])
);

(* dont_touch = "true" *) LUT2 #(
	.INIT(2'd2)
) LUT2_7 (
	.I0(pads_rx_data[6]),
	.I1(reset),
	.O(capture_pads_rx_data[6])
);

(* dont_touch = "true" *) LUT2 #(
	.INIT(2'd2)
) LUT2_8 (
	.I0(pads_rx_data[7]),
	.I1(reset),
	.O(capture_pads_rx_data[7])
);

endmodule


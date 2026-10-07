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
assign source_last = ((~pads_rx_dv) & source_valid);

always @(posedge sys_clk) begin
	rx_dv <= pads_rx_dv;
	rx_data <= pads_rx_data;
	rx_reset <= sys_rst;
	if (sys_rst) begin
	end
end

endmodule


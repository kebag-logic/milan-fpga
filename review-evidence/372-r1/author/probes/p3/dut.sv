`default_nettype none
module dut (
  input  wire clk,
  input  wire rst_n,
  input  wire a,
  input  wire b,
  output logic y
);
  typedef enum logic [1:0] { IDLE, S_ONE, S_TWO } state_t;
  state_t state;
  always_ff @(posedge clk) begin : fsm
    if (!rst_n) state <= IDLE;
    else if (a) state <= S_ONE;
    else if (b) state <= S_TWO;
    else state <= IDLE;
  end
  assign y = (state == S_ONE);
endmodule
`default_nettype wire

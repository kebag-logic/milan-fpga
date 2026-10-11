module w_base (
  input wire clk_i, input wire rst_n, input wire rx_valid_i,
  input wire [7:0] rx_data_i, input wire rx_sof_i, input wire rx_eof_i, 
  input wire [63:0] local_clock_id_i, input wire local_clock_valid_i,
  output wire bank_we_o, output wire [4:0] bank_addr_o,
  output wire [63:0] bank_wdata_o, output wire ev_valid_o,
  output wire [7:0] ev_code_o, output wire [15:0] ev_seq_o,
  output wire [15:0] drop_cnt_o);
  parser_base u (.clk_i(clk_i), .rst_n(rst_n), .rx_valid_i(rx_valid_i),
    .rx_data_i(rx_data_i), .rx_sof_i(rx_sof_i), .rx_eof_i(rx_eof_i),
    .rx_err_i(1'b0), .local_clock_id_i(local_clock_id_i),
    .local_clock_valid_i(local_clock_valid_i), .bank_we_o(bank_we_o),
    .bank_addr_o(bank_addr_o), .bank_wdata_o(bank_wdata_o),
    .ev_valid_o(ev_valid_o), .ev_code_o(ev_code_o), .ev_seq_o(ev_seq_o),
    .drop_cnt_o(drop_cnt_o));
endmodule

// integration slice: milan_csr TCAM plumbing -> rx_mac_filter
module tcam_csr_wrap (
  input  wire        clk_i,
  input  wire        rst_n,
  input  wire [31:0] wr_addr_i,
  input  wire [31:0] wr_data_i,
  input  wire        wr_p_i,
  input  wire [63:0] s_tdata,
  input  wire [7:0]  s_tkeep,
  input  wire        s_tvalid,
  input  wire        s_tlast,
  output wire        s_tready,
  output wire [63:0] m_tdata,
  output wire        m_tvalid,
  input  wire        m_tready,
  output wire        m_tlast,
  output wire        dropped_o
);
  // mimic the CSR registers + strobe exactly as milan_csr does
  logic [31:0] tcam_klo, tcam_khi, tcam_mlo, tcam_mhi, tcam_act, tcam_ctrl;
  logic [4:0]  tcam_wr_index;
  logic        tcam_wr_valid_r, tcam_wr_p;
  always_ff @(posedge clk_i) begin
    if (!rst_n) begin
      tcam_klo<=0; tcam_khi<=0; tcam_mlo<=0; tcam_mhi<=0; tcam_act<=0;
      tcam_ctrl<=32'h1; tcam_wr_index<=0; tcam_wr_valid_r<=0; tcam_wr_p<=0;
    end else begin
      tcam_wr_p <= 1'b0;
      if (wr_p_i) begin
        case (wr_addr_i)
          32'h704: tcam_klo <= wr_data_i;
          32'h708: tcam_khi <= wr_data_i;
          32'h70C: tcam_mlo <= wr_data_i;
          32'h710: tcam_mhi <= wr_data_i;
          32'h714: tcam_act <= wr_data_i;
          32'h718: if (wr_data_i[16]) begin
            tcam_wr_p <= 1'b1;
            tcam_wr_index <= wr_data_i[4:0];
            tcam_wr_valid_r <= wr_data_i[8];
          end
          default: ;
        endcase
      end
    end
  end
  rx_mac_filter #(.TDATA_WIDTH(64)) f (
    .clk_i(clk_i), .rst_n(rst_n),
    .default_pass_i(tcam_ctrl[0]),
    .tcam_wr_en_i(tcam_wr_p),
    .tcam_wr_index_i(tcam_wr_index[3:0]),
    .tcam_wr_valid_i(tcam_wr_valid_r),
    .tcam_wr_key_i({tcam_khi[15:0], tcam_klo}),
    .tcam_wr_mask_i({tcam_mhi[15:0], tcam_mlo}),
    .tcam_wr_action_i(tcam_act[7:0]),
    .s_tdata(s_tdata), .s_tkeep(s_tkeep), .s_tvalid(s_tvalid),
    .s_tlast(s_tlast), .s_tready(s_tready),
    .m_tdata(m_tdata), .m_tkeep(), .m_tvalid(m_tvalid),
    .m_tlast(m_tlast), .m_tready(m_tready),
    .frame_action_o(), .frame_match_o(), .frame_dropped_o(dropped_o)
  );
endmodule

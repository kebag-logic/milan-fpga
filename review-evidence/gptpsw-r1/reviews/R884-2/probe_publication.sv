`timescale 1ns/1ps
module probe_publication;
  logic sys_clk=0, dp_clk=0, rst_n=0;
  always #5 sys_clk=~sys_clk;
  always #10 dp_clk=~dp_clk;
  logic [95:0] words=0;
  wire [95:0] observed;
  wire landed;
  integer torn=0;
  integer count=0;
  KL_mbx_cdc dut (
    .sys_clk_i(sys_clk), .sys_rst_n(rst_n),
    .dp_clk_i(dp_clk), .dp_rst_n(rst_n),
    .m_pub_gptp_i(words), .d_pub_gptp_o(observed), .d_pub_gptp_p_o(landed)
  );
  always @(negedge dp_clk) if (landed) begin
    count=count+1;
    $display("landed GEN=%0d GM=%016x",observed[95:88],observed[63:0]);
    if (observed[95:88]==2 && observed[63:0]!=64'h2222222222222222) torn=torn+1;
  end
  initial begin
    repeat(4) @(negedge sys_clk);
    rst_n=1;
    // Commit generation 1 while the crossing is idle.
    @(negedge sys_clk); words[31:0]=32'h11111111;
    @(negedge sys_clk); words[63:32]=32'h11111111;
    @(negedge sys_clk); words[95:64]=32'h01000300;
    repeat(3) @(negedge sys_clk);
    // Commit generation 2 while generation 1 is in flight.
    words[31:0]=32'h22222222;
    @(negedge sys_clk); words[63:32]=32'h22222222;
    @(negedge sys_clk); words[95:64]=32'h02000300;
    // Start another publication but do not commit its GEN.
    @(negedge sys_clk); if (!$test$plusargs("CONTROL")) words[31:0]=32'h33333333;
    repeat(60) @(negedge sys_clk);
    $display("publication count=%0d torn=%0d",count,torn);
    if(torn || count!=2) $fatal(1,"GEN-committed publication integrity failed");
    $finish;
  end
endmodule

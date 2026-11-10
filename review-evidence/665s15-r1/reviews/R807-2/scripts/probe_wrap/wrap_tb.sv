// Evaluates the 32x32 layout's ACMP transmit ring decode in both forms over every
// word offset of the window: the bounded form the skeleton emitted before the fix
// and the unbounded form it emits now. Prints the hit counts and the first/last hit.
module wrap_tb;
  import KL_mbx_pkg::*;
  localparam int unsigned AW2_C = MBX_ADDR_W_C + 2;
  initial begin
    int bounded = 0, open = 0, below = 0;
    int first_b = -1, first_o = -1, last_o = -1;
    for (int a = 0; a < (1 << MBX_ADDR_W_C); a++) begin
      logic [AW2_C-1:0] off_w;
      off_w = {a[MBX_ADDR_W_C-1:0], 2'b00};
      if (off_w >= AW2_C'(MBX_CH_ACMP_TX_BASE_C)
          && off_w < AW2_C'(MBX_CH_ACMP_TX_BASE_C + 4 * MBX_CH_ACMP_TX_WORDS_C)) begin
        bounded++; if (first_b < 0) first_b = int'(off_w);
      end
      if (off_w >= AW2_C'(MBX_CH_ACMP_TX_BASE_C)) begin
        open++; if (first_o < 0) first_o = int'(off_w); last_o = int'(off_w);
      end
      if (off_w < AW2_C'(MBX_CH_ACMP_TX_BASE_C)) below++;
    end
    $display("AW2_C=%0d base=0x%0h words=%0d bound_cast=0x%0h", AW2_C, MBX_CH_ACMP_TX_BASE_C,
             MBX_CH_ACMP_TX_WORDS_C, AW2_C'(MBX_CH_ACMP_TX_BASE_C + 4 * MBX_CH_ACMP_TX_WORDS_C));
    $display("bounded_form_hits=%0d first=%0d", bounded, first_b);
    $display("open_form_hits=%0d first=0x%0h last=0x%0h words_below_base=%0d", open, first_o, last_o, below);
    $finish;
  end
endmodule

module lat_tb;
  import KL_media_if_latency_pkg::*;
  // shape: (frame_pairs kept, blend, word bits, bit clock, write clock, write cycles)
  initial begin
    $display("1x1 TDM8 master  %0d", mark_lat_ns(pair_end_bits(close_pair(4,0),32,1), 64'd12288000, 64'd24576000, 1, 64'd50000000));
    $display("8x8 TDM32 master %0d", mark_lat_ns(pair_end_bits(close_pair(4,0),32,1), 64'd49152000, 64'd98304000, 1, 64'd50000000));
    $display("Arty TDM8 blend  %0d", mark_lat_ns(pair_end_bits(close_pair(4,1),32,1), 64'd12288000, 64'd24576000, 1, 64'd50000000));
    $display("Arty I2S         %0d", mark_lat_ns(pair_end_bits(close_pair(1,0),32,1), 64'd3072000, 64'd24576000, 5, 64'd50000000));
    $display("TDM8 slave       %0d", mark_lat_ns(pair_end_bits(close_pair(4,0),32,1), 64'd12288000, 64'd12288000, 1, 64'd50000000));
    $display("synthetic TDM4   %0d", mark_lat_ns(pair_end_bits(close_pair(2,0),32,0), 64'd6144000, 64'd24576000, 1, 64'd50000000));
    $finish;
  end
endmodule

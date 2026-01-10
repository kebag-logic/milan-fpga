/*
 * SPDX-FileCopyrightText: 2025 Cemal Dogan <cemal.dogan@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

class axi_stream_driver #(
  parameter realtime CLK_PERIOD_P = 10,
  parameter TDATA_WIDTH_P = 32,
  parameter TID_WIDTH_P = 1,
  parameter TDEST_WIDTH_P = 1,
  parameter TUSER_WIDTH_P = 1
);


  // Interface to drive
  virtual axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH_P), .TID_WIDTH_P(TID_WIDTH_P), 
                          .TDEST_WIDTH_P(TDEST_WIDTH_P), .TUSER_WIDTH_P(TUSER_WIDTH_P)) axis_if;


  function new ();
    $display("[INFO][AXI_STREAM_DRIVER] : Driver has been created");
  endfunction

  task drive_axi_stream (ref logic [7:0] q[$]);

    int number_of_octets; // How many bytes in one AXI4-Stream Transaction
    int remainder; // How many bytes in the last AXI4-Stream Transaction
    int total_bytes; // How many AXI4-Stream transaction will be made
    int j = 0;

    number_of_octets = ($size(axis_if.tdata)/8) - 1;
    remainder = (q.size() % (number_of_octets + 1));
    total_bytes = $ceil(($itor(q.size()) / $itor(number_of_octets + 1)));
    // Generate the AXI4-Stream transaction
    @(axis_if.cb);

    while(j <= total_bytes-1) begin
      // Assign the protocol values
      if (j == total_bytes - 1) begin // Last transaction - Check the remainder
      axis_if.tlast = 1'd1;
        if (remainder != 0) begin
          for (int z = 0; z < (number_of_octets+1-remainder); z++) begin
            axis_if.tkeep[z] = 1'b0;
          end
          for (int i = number_of_octets; i >= 0; i--) begin
            // Fill with 8'hXX if the data is invalid
            if (i == (number_of_octets - remainder)) axis_if.tdata[i*8+:8] = 8'hXX;
            else axis_if.tdata[i*8+:8] = q.pop_front();
          end
        end
        else begin // In the last AXI4-Stream Transaction, but remainder is ZERO
          for (int i = number_of_octets; i >= 0; i--) begin
            axis_if.tdata[i*8+:8] = q.pop_front();
          end
        end
      end
      else begin // Standard AXI4-Stream tdata assignments
        axis_if.tvalid = 1'd1;
        axis_if.tkeep = {TDATA_WIDTH_P/8{1'b1}};
        for (int i = number_of_octets; i >= 0; i--) begin
          axis_if.tdata[i*8+:8] = q.pop_front();
        end
      end
      wait (axis_if.tready);
      #1ps;
      j++;
      @(axis_if.cb);
    end
    axis_if.tdata = '0;
    axis_if.tkeep = '0;
    axis_if.tvalid = '0;
    axis_if.tlast = '0;
  endtask

endclass
/*
 * SPDX-FileCopyrightText: 2025 Oguz Kahraman <oguz.kahraman@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
*/
/*
------------------------------------------------------------------------------
  File        : KL_counter.sv
  Author      : Cemal Dogan

                cemal.dogan@kebag-logic.com

  Date        : 02/05/2025
  Description : Responsible for generating the delay in seconds
             valid values (0-5sec)

             TODO: For now it is assumed that the clk_i is 100MHz
  
  Company     : Kebag Logic
  Project     : Milan ADP

------------------------------------------------------------------------------
*/

`default_nettype none

module KL_counter
  (
    input wire clk_i,
    input wire rst_n,
    input wire start_i,
    input wire stop_i,
    input wire [2:0] delay_value_i,

    output wire completed_o
  );

  typedef enum bit [2:0] {
    START_S,
    COUNT_S,
    FINISH_S
  } cnter_state_t;

  cnter_state_t cnter_state;
  logic [15:0] high_counter_max;
  logic [15:0] med_counter_max;
  logic [15:0] low_counter_max;

  reg [15:0] high_counter_val_r;
  reg [15:0] med_counter_val_r;
  reg [15:0] low_counter_val_r;

  reg completed_r;

  assign completed_o = completed_r;

  always_ff @(posedge clk_i) begin : counter_logic
    if (!rst_n) begin
      completed_r <= 1'd0;
      high_counter_val_r <= 16'd0;
      med_counter_val_r <= 16'd0;
      low_counter_val_r <= 16'd0;
      cnter_state <= START_S;
    end
    else begin
      case(cnter_state)

        START_S : begin
          if (start_i) cnter_state <= COUNT_S;
        end

        COUNT_S : begin
          if (high_counter_val_r == high_counter_max - 1) begin
            high_counter_val_r <= 16'd0;
            completed_r <= 1'd1;
            cnter_state <= FINISH_S;
          end
          else begin
            if (med_counter_val_r == med_counter_max - 1) begin
              high_counter_val_r <= high_counter_val_r + 16'd1;
              med_counter_val_r <= 16'd0;
            end
            else begin
              if (low_counter_val_r == low_counter_max - 1) begin
                med_counter_val_r <= med_counter_val_r + 16'd1;
                low_counter_val_r <= 16'd0;
              end
              else begin
                low_counter_val_r <= low_counter_val + 16'd1;
              end
            end
          end
          if (stop_i) cnter_state <= FINISH_S;
        end

        FINISH_S : begin
          completed_r <= 1'd0;
          high_counter_val_r <= 16'd0;
          med_counter_val_r <= 16'd0;
          low_counter_val_r <= 16'd0;
          cnter_state <= START_S;
        end
      endcase
    end
  end

  // Assign the counter_max_values
  always_comb begin : max_cnt_values
    case(delay_value_i)
      0: begin // 0-sec
        // give a few nanoseconds to the logic ?
        high_counter_max = 16'd2;
        med_counter_max = 16'd2;
        low_counter_max = 16'd5;
      end
      1: begin // 1-sec
        high_counter_max = 16'd1000;
        med_counter_max = 16'd1000;
        low_counter_max = 16'd100;
      end
      2: begin // 2-sec
        high_counter_max = 16'd1000;
        med_counter_max = 16'd1000;
        low_counter_max = 16'd200;
      end
      3: begin // 3-sec
        high_counter_max = 16'd1000;
        med_counter_max = 16'd1000;
        low_counter_max = 16'd300;
      end
      4: begin // 4-sec
        high_counter_max = 16'd1000;
        med_counter_max = 16'd1000;
        low_counter_max = 16'd400;
      end
      5: begin // 5-sec
        high_counter_max = 16'd1000;
        med_counter_max = 16'd1000;
        low_counter_max = 16'd500;
      end
      default : begin
        high_counter_max = 16'd1000;
        med_counter_max = 16'd1000;
        low_counter_max = 16'd100;
      end
    endcase
  end

endmodule

`default_nettype wire
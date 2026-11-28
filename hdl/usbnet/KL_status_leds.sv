/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
/*
------------------------------------------------------------------------------
  File        : KL_status_leds.sv
  Description : Four status LEDs (#1018), the Arty A7's RGB LEDs LD0 to LD3,
                each on one colour channel at a low PWM duty so they read
                without glare.
                  LD0  Ethernet link up; it goes off for BLINK_OFF_MS_P on a
                       frame in either direction, then stays on for at least
                       BLINK_ON_MS_P before it can blink again, so steady
                       traffic flickers rather than going dark.
                  LD1  the USB 3.0 path works (usb_ok_i, from the USB network
                       path: docs/design/USB_NET_PATH.md).
                  LD2  any input media-locked or output transmit gate open.
                  LD3  internal clock, or the selected source locked.
                state_o is each LED's state before the PWM, for the status
                read-back and for the tests.
  Spec refs   : #1018; #1020 ruling; IEEE 1722.1-2021 7.4.23
  Company     : Kebag Logic
  Project     : Milan AVB endstation
------------------------------------------------------------------------------
*/
//---------------------------------------------------------------------------//
`default_nettype none

module KL_status_leds #(
  parameter int unsigned CLK_HZ_P        = 80_000_000,
  parameter int unsigned PWM_BITS_P      = 8,
  parameter int unsigned DUTY_P          = 16,   //! on clocks per 2^PWM_BITS_P
  parameter int unsigned BLINK_OFF_MS_P  = 40,
  parameter int unsigned BLINK_ON_MS_P   = 60
)(
  input  wire        clk_i,   //! the SoC system clock
  input  wire        rst_ni,   //! synchronous reset, active low
  input  wire        link_up_i,   //! the Ethernet link is up (LD0)
  input  wire        act_i,        //! one pulse per frame, either direction
  input  wire        usb_ok_i,   //! the USB 3.0 path works (LD1)
  input  wire        stream_i, //! fabric LD2 predicate, synchronized to clk_i
  input  wire        clock_i,  //! fabric LD3 predicate, synchronized to clk_i
  output logic [3:0] state_o,   //! LD0 to LD3 as shown, before the PWM
  output logic [3:0] led_o   //! LD0 to LD3 at the PWM duty, to the green pads
);
  localparam int unsigned MS_CYC_C = CLK_HZ_P / 1000;
  localparam int unsigned MS_W_C   = $clog2(BLINK_OFF_MS_P + BLINK_ON_MS_P + 1);

  if (DUTY_P == 0 || DUTY_P >= (1 << PWM_BITS_P) || MS_CYC_C < 2) begin : g_refuse
    $error("KL_status_leds: DUTY_P=%0d must lie inside the PWM period", DUTY_P);
  end

  logic [$clog2(MS_CYC_C)-1:0] div_r;
  logic                        tick_r;
  logic [PWM_BITS_P-1:0]       pwm_r;
  logic [MS_W_C-1:0]           blink_r;   //! ms left in the blink: off first, then the hold

  always_ff @(posedge clk_i) begin : timebase
    if (!rst_ni) begin
      div_r  <= '0;
      tick_r <= 1'b0;
      pwm_r  <= '0;
    end else begin
      pwm_r  <= pwm_r + 1'b1;
      tick_r <= div_r == ($clog2(MS_CYC_C))'(MS_CYC_C - 1);
      div_r  <= (div_r == ($clog2(MS_CYC_C))'(MS_CYC_C - 1)) ? '0 : div_r + 1'b1;
    end
  end : timebase

  always_ff @(posedge clk_i) begin : blink
    if (!rst_ni) begin
      blink_r <= '0;
    end else if (blink_r == '0) begin
      if (act_i && link_up_i) blink_r <= MS_W_C'(BLINK_OFF_MS_P + BLINK_ON_MS_P);
    end else if (tick_r) begin
      blink_r <= blink_r - 1'b1;
    end
  end : blink

  wire off_w = blink_r > MS_W_C'(BLINK_ON_MS_P);

  assign state_o = {clock_i, stream_i, usb_ok_i, link_up_i && !off_w};
  assign led_o   = state_o & {4{pwm_r < PWM_BITS_P'(DUTY_P)}};

endmodule

`default_nettype wire

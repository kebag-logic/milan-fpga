/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : KL_media_nco.sv
  Author      : Kebag Logic

  Date        : 2026-08-10
  Description : The media clock's sample grid, made steerable - the ONE grid
                every channel advances on, in both directions.

                WHY THIS EXISTS. The grid used to be an inline Bresenham
                divider in milan_datapath with the remainder as a localparam:
                exact against the board crystal, and structurally unable to
                follow anything else. A talker whose grid cannot be steered
                cannot be a media clock SINK, which Milan v1.2 7.2.2 makes
                mandatory ("For each supported clock domain, an AAF Media
                Talker shall implement a CRF Media Clock Input"), and a
                listener whose grid cannot be steered drains someone else's
                stream on its own crystal and slips one sample per beat
                period (bench 2026-08-10: one 48 kHz sample every 1.96 s
                through the loopback lane, 10.6 ppm).

                WHAT IT IS. A fractional-N divider of clk_i whose remainder
                carries a signed runtime trim:

                  average period = DIV_C + (REM_C + trim) / DEN_C  clocks
                  DIV_C = CLK_FREQ_HZ_P / FS_HZ_P    (integer part)
                  REM_C = CLK_FREQ_HZ_P % FS_HZ_P    (nominal remainder)
                  DEN_C = FS_HZ_P                    (denominator)

                so d(rate)/rate per trim LSB = -1 / CLK_FREQ_HZ_P, EXACTLY,
                independent of FS_HZ_P. At 100 MHz that is 0.01 ppm per LSB
                and TRIM_MAX_P = 20000 spans +/-200 ppm - the same authority
                KL_mmcm_drp_servo clamps its own output to (U_MAX_P), so the
                two actuators of one media clock have one range.

                SIGN. trim > 0 lengthens the period = SLOWS the grid. The
                servo's u is the opposite convention ("u > 0 = speed up",
                KL_mmcm_drp_servo.sv:604), so the datapath negates on the way
                in. Getting this backwards turns a servo into a runaway, so
                it is stated in both places and pinned by the testbench.

                BIT-EXACT AT trim = 0. With trim tied off, sum_w can never go
                negative, un_w is dead, and the arithmetic reduces term for
                term to the divider this module replaced. That is deliberate:
                clock_source = INTERNAL must keep the free-running grid every
                existing bench number and every existing testbench was
                measured against (USER rule: internal media clock = free-run,
                slips accepted).

                SINGLE-STEP CORRECTION. The elaboration guards below bound
                the accumulator so one +/-DEN_C correction always re-normalises
                it; a trim large enough to need two would silently drop a
                sample, so it is refused at elaboration rather than clamped
                into a lie.

  Company     : Kebag Logic
  Project     : Milan AVTP
------------------------------------------------------------------------------
*/

//! Steerable fractional-N media sample grid. tick_o averages
//! CLK_FREQ_HZ_P / (DIV_C + (REM_C + trim_i)/DEN_C) Hz with one clk_i of
//! jitter and ZERO long-term residual.

`default_nettype none

module KL_media_nco #(
  parameter int unsigned CLK_FREQ_HZ_P = 100_000_000, //! datapath clock (Hz)
  parameter int unsigned FS_HZ_P       = 48_000,      //! nominal sample rate (Hz)
  //! |trim| clamp, in LSB. DERIVED, not mirrored: the largest trim whose
  //! accumulator still re-normalises in one step is FS_HZ_P - (CLK % FS),
  //! and that bound moves with the datapath clock (100 MHz: 32000 LSB,
  //! 50 MHz: 16000 LSB - both +/-319.9 ppm, because the LSB moves with the
  //! clock too). Overriding this with a literal is how a 50 MHz build would
  //! silently drop a sample, so the default is the maximum legal value and
  //! the guards below refuse anything larger.
  parameter int unsigned TRIM_MAX_P    = FS_HZ_P - (CLK_FREQ_HZ_P % FS_HZ_P),
  parameter int unsigned TRIMW_P       = 16,          //! trim_i width (signed)
  //! NCO LSB per ppm. DERIVED: one LSB moves the rate by 1/CLK_FREQ_HZ_P
  //! relative, so a ppm is CLK_FREQ_HZ_P/1e6 LSB (100 at 100 MHz, 50 at
  //! 50 MHz). Used only to rescale the servo's units below.
  parameter int unsigned PPM_LSB_P     = CLK_FREQ_HZ_P / 1_000_000
)(
  input  wire                     clk_i,   //! datapath clock
  input  wire                     rst_n,   //! active-low synchronous reset
  //! signed remainder trim, 0 = nominal. LSB = -1/CLK_FREQ_HZ_P relative
  //! (0.01 ppm at 100 MHz); POSITIVE SLOWS THE GRID. Clamped internally to
  //! +/-TRIM_MAX_P, so a wild input degrades to the clamp, never to a
  //! dropped sample.
  input  wire signed [TRIMW_P-1:0] trim_i,
  //! --- the servo path -----------------------------------------------------
  //! KL_mmcm_drp_servo's u, signed, in 1/16 ppm units (its A_MCSRV_STAT
  //! [31:16] field). Lives HERE rather than in the datapath so the sign and
  //! the rescale are covered by this module's suite: a sign error between the
  //! two conventions is a runaway servo, not a wrong number, and four naked
  //! lines in a 5000-line wrapper had no way to be exercised.
  input  wire signed [15:0]        servo_trim_i,
  //! 1 = follow servo_trim_i (a clock source is selected), 0 = free-run on
  //! trim_i. clock_source = INTERNAL must land here as 0: the USER rule is
  //! "internal media clock = free-run, slips accepted", and it is what keeps
  //! the shipping default bit-for-bit identical to the pre-NCO divider.
  input  wire                      servo_en_i,
  output logic                    tick_o,  //! one-cycle sample strobe
  //! fractional accumulator, for the media-clock testbench and CSR taps: it
  //! is the sub-sample phase of the grid and it is the only way to see the
  //! trim take effect faster than the beat period
  output logic [$clog2(FS_HZ_P)-1:0] phase_o
);

  // ---------------------------------------------------------------------- //
  // Derived sizing                                                          //
  // ---------------------------------------------------------------------- //
  localparam int unsigned DIV_C   = CLK_FREQ_HZ_P / FS_HZ_P;
  localparam int unsigned REM_C   = CLK_FREQ_HZ_P % FS_HZ_P;
  localparam int unsigned DEN_C   = FS_HZ_P;
  localparam int unsigned FRACW_C = $clog2(DEN_C);
  localparam int unsigned CNTW_C  = $clog2(DIV_C + 2);
  //! signed span of sum_w: [ REM_C - TRIM_MAX_P , DEN_C-1 + REM_C + TRIM_MAX_P ]
  localparam int unsigned SUMW_C  = $clog2(2*DEN_C + TRIM_MAX_P + 2) + 1;

  //! The guards that make ONE correction step sufficient. Both are true of
  //! the shipping shape (100 MHz / 48 kHz: REM_C 16000, TRIM_MAX_P 20000).
  if (REM_C + TRIM_MAX_P > DEN_C) begin : gen_guard_hi
    $error("KL_media_nco: REM_C=%0d + TRIM_MAX_P=%0d exceeds DEN_C=%0d, so the accumulator can reach 2*DEN_C and one subtraction no longer re-normalises it - the grid would silently drop a sample. Leave TRIM_MAX_P at its derived default (%0d LSB here) or lower it.",
           REM_C, TRIM_MAX_P, DEN_C, DEN_C - REM_C);
  end
  else if (TRIM_MAX_P >= REM_C + DEN_C) begin : gen_guard_lo
    $error("KL_media_nco: TRIM_MAX_P=%0d can drive the accumulator below -DEN_C=%0d, so one addition no longer re-normalises it. Lower TRIM_MAX_P.",
           TRIM_MAX_P, DEN_C);
  end
  else if (DIV_C < 2) begin : gen_guard_div
    $error("KL_media_nco: CLK_FREQ_HZ_P=%0d / FS_HZ_P=%0d = %0d leaves no room for the borrowed cycle (a trim that shortens the period needs DIV_C >= 2). This grid needs a faster datapath clock.",
           CLK_FREQ_HZ_P, FS_HZ_P, DIV_C);
  end

  // ---------------------------------------------------------------------- //
  // Grid                                                                    //
  // ---------------------------------------------------------------------- //
  logic [CNTW_C-1:0]  cnt_r;
  logic [FRACW_C-1:0] frac_r;

  //! SERVO PATH. The servo's u > 0 means SPEED UP (KL_mmcm_drp_servo.sv:604);
  //! this NCO's trim > 0 LENGTHENS the period, i.e. slows down. Hence the
  //! negation. u is 1/16 ppm and one LSB here is 1/PPM_LSB_P ppm, so the
  //! conversion is -(u * PPM_LSB_P) / 16. The servo clamps u to +-200 ppm
  //! (U_MAX_P), which lands at +-200*PPM_LSB_P LSB - 20000 at 100 MHz, inside
  //! the derived TRIM_MAX_P of 32000, so the two authorities agree by
  //! construction rather than by a comment.
  //! use_dsp="no": PPM_LSB_P is a COMPILE-TIME CONSTANT (100 at 100 MHz), so
  //! this is a constant multiply - two shift-adds in fabric, about a
  //! nanosecond. Vivado inferred a DSP48E1 for it anyway, and a combinational
  //! DSP costs ~5 ns of a 10 ns period on a path that then still has to reach
  //! the accumulator. The repo already uses the opposite hint where a DSP IS
  //! wanted (credit_based_shaper.sv:106), so the attribute is house-idiom
  //! rather than a new dependency.
  (* use_dsp = "no" *)
  wire signed [31:0] servo_lsb_w =
      -(($signed(32'(servo_trim_i)) * $signed(32'(PPM_LSB_P))) >>> 4);

  //! one trim, selected. INTERNAL (servo_en_i = 0) free-runs on trim_i, which
  //! the datapath ties to zero, which is what makes the shipping default
  //! bit-for-bit the divider this module replaced.
  wire signed [31:0] trim_sel_w = servo_en_i ? servo_lsb_w : 32'(trim_i);

  //! clamp AFTER the select, so a wild servo command degrades to the clamp on
  //! exactly the same terms a wild trim_i does - and so the arithmetic below
  //! is always inside the span the elaboration guards proved
  wire signed [SUMW_C-1:0] trim_cl_w =
      (trim_sel_w >  $signed(32'(TRIM_MAX_P)))  ?  SUMW_C'(signed'(TRIM_MAX_P))
    : (trim_sel_w < -$signed(32'(TRIM_MAX_P)))  ? -SUMW_C'(signed'(TRIM_MAX_P))
                                                :  SUMW_C'(trim_sel_w);

  //! REGISTERED, and this is a timing fix, not a style choice. Left
  //! combinational, the conversion above joined the Bresenham arithmetic
  //! below into ONE path: DSP multiply -> select -> 32-bit clamp -> the
  //! accumulator adder -> the overflow/underflow compares -> the terminal
  //! compare -> cnt_r. Vivado measured it at 12.336 ns of a 10 ns period,
  //! 17 logic levels with 10 CARRY4, and it broke timing on all three place
  //! seeds at once (WNS -2.9 to -4.0 ns) - a structural failure, not a
  //! placement lottery.
  //!
  //! Costs nothing to break: servo_trim_i moves at most once per servo tick
  //! (KL_mmcm_drp_servo TICK_CYC_P = 24576 audio cycles, about 1 ms), and the
  //! grid needs a new rate no faster than the loop produces one. One cycle of
  //! latency on a value that updates every ~100,000 cycles is invisible to
  //! the rate, to the phase, and to every check in tb/verilator/media_nco.
  logic signed [SUMW_C-1:0] trim_r;
  always_ff @(posedge clk_i) begin : trim_pipe
    if (!rst_n) trim_r <= '0;
    else        trim_r <= trim_cl_w;
  end : trim_pipe

  //! ONE predicate set decides the borrowed/lent cycle AND the accumulator
  //! wrap, so the two can never disagree (the KL_pcm_tx pace_div discipline)
  wire signed [SUMW_C-1:0] sum_w = SUMW_C'(signed'({1'b0, frac_r}))
                                 + SUMW_C'(signed'(REM_C))
                                 + trim_r;
  wire ov_w = (sum_w >= SUMW_C'(signed'(DEN_C)));   //! grid runs slow: lend a cycle
  wire un_w = (sum_w <  SUMW_C'(signed'(0)));       //! grid runs fast: borrow one

  wire [31:0] end_w = 32'(DIV_C) - 32'd1
                    + (ov_w ? 32'd1 : 32'd0)
                    - (un_w ? 32'd1 : 32'd0);

  always_ff @(posedge clk_i) begin : media_grid
    if (!rst_n) begin
      cnt_r  <= '0;
      frac_r <= '0;
      tick_o <= 1'b0;
    end
    else if (32'(cnt_r) == end_w) begin
      cnt_r  <= '0;
      frac_r <= ov_w ? FRACW_C'(sum_w - SUMW_C'(signed'(DEN_C)))
              : un_w ? FRACW_C'(sum_w + SUMW_C'(signed'(DEN_C)))
                     : FRACW_C'(sum_w);
      tick_o <= 1'b1;
    end
    else begin
      cnt_r  <= cnt_r + 1'b1;
      tick_o <= 1'b0;
    end
  end : media_grid

  assign phase_o = frac_r;

endmodule

`default_nettype wire

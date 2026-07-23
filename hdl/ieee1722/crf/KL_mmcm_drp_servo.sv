/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

//---------------------------------------------------------------------------//
/*
------------------------------------------------------------------------------
  File        : KL_mmcm_drp_servo.sv
  Description : CRF media-clock recovery ACTUATOR - the audio-MMCM servo
                (Milan v1.2 7.3.4 media clock recovery; the clean-clock
                rework retired the playback NCO with trim_o = 0 awaiting
                exactly this block).

                Closes the loop  talker media clock -> our audio MMCM
                when clock_source == 2 (the CRF CLOCK_SOURCE descriptor):

                  error   e = local_rate - crf_rate  (both are "gPTP-ns
                          per 512 ms of media events": KL_crf_rx rate_o
                          measures the TALKER media clock against gPTP
                          over its 256-PDU field-timestamp ring; this
                          block measures OUR audio clock against the
                          same gPTP time over a 2^WIN_LOG2_P-tick local
                          window, so e > 0  <=>  we run slow).
                          1 ppm == 512 units. CRF_DELTA (0x744) is NOT a
                          loop input: it contains the arbitrary
                          talker+transit phase constant; the wire-truth
                          loop quantity is the differential rate.

                  PI      u <- clamp(integ + e>>KP_SHIFT_P), with
                          integ <- integ + e>>KI_SHIFT_P, per window;
                          bounded step (|du| <= SLEW_MAX_P per window)
                          and bounded authority (|u| <= U_MAX_P).

                  step guard (2026-07-23 silicon): a local ptp_now
                          step/slew (GM reboot -> ptp4l stepping the
                          PHC) makes ONE window's local span enormous
                          while crf_rate_i stays healthy; that single
                          window used to wind the integrator straight
                          to the +-200 ppm clamp (trim 0xF380 seen),
                          where it STAYED until an IDLE bounce. Any
                          window with |e| > GUARD_THR_C (2^19 = 1024
                          ppm in the x512 units - legit acquire errors
                          stay < ~211 ppm = base + authority) is now
                          DISCARDED like a win_skip window: no PI, no
                          trim, no lock_cnt change; counted in
                          status_o[15:10]. DISC_MAX_C consecutive
                          discards resync win_start like a CRF relock
                          (PI state kept), so a sustained slew can
                          never wedge the servo.

                  actuator (fine, glitch-free): MMCME2 dynamic fine
                          phase shift, UG472 "Interpolated Fine Phase
                          Shift in Fixed or Dynamic Mode in the MMCM":
                          linear steps of 1/(56*F_VCO) per PSEN
                          operation, PSDONE "always 12 PSCLK cycles"
                          later, "no maximum phase shift ... wraps
                          around round-robin" - a sustained step RATE is
                          therefore a permanent, glitch-free frequency
                          trim of the live audio clock:
                              df/f = -step_rate * (1/(56*F_VCO)).
                          u > 0 (speed up) issues PS DECREMENTS (UG472:
                          "Each increment ADDS to the phase shift", i.e.
                          delays the output = slows it while stepping).
                          Fine PS requires the fractional counters OFF
                          (UG472: "Fractional divide is not allowed in
                          either fixed or dynamic interpolated fine
                          phase-shift mode") - the audio MMCM is integer
                          M=34/D=1/O=43 off the 31.081081 MHz pre-PLL
                          (see milan_soc.py _CRG: 24.576 MHz - 10.6 ppm
                          base, F_VCO = 1056.7568 MHz, step = 16.9 ps).

                  actuator (coarse, DRP): an XAPP888-conformant DRP
                          engine against the documented MMCME2 register
                          map (addresses/fields cited at the localparams
                          below). On every servo activation it READ-
                          verifies the CLKOUT0 divider registers against
                          the expected configuration (reads are
                          non-intrusive; XAPP888 requires reset only
                          "during dynamic reconfiguration"), and - only
                          when auto_repair_i is set and the readback
                          mismatches - REPROGRAMS them with the full
                          documented safe sequence:
                            1. quiesce the fine-PS runner (XAPP888:
                               "Fine-phase shifting is not allowed for
                               the initial configuration or during
                               reconfiguration");
                            2. assert MMCM reset (XAPP888: "must be held
                               in reset during dynamic reconfiguration");
                            3. write PowerReg 0x28 = 0xFFFF (XAPP888
                               Table 14: "must all be set High when
                               performing DRP");
                            4. read-modify-write each ClkReg through the
                               DEN/DWE/DRDY handshake, preserving the
                               RESERVED bits (XAPP888 reference design:
                               "reads the previous value, masks the bits
                               that need to be changed");
                            5. release reset and wait for LOCKED.
                          The relock is a bounded audio-clock outage
                          (same sequencing class as the link-guard GMII
                          CDC reinit); it can never fire on a matching
                          live clock, and never at all while
                          auto_repair_i = 0 (the silicon bring-up
                          default until the bench confirms the readback
                          expectation against the Vivado-programmed
                          attribute encoding).

                WHY NOT DRP-only (the honest granularity math): the
                fractional divide fields (ClkReg2 FRAC[14:12], XAPP888
                Table 2/7) have 1/8 resolution (UG472: "resolution of
                the fractional divide is 1/8"), i.e. >= (1/8)/64 =
                1953 ppm per LSB on CLKFBOUT and (1/8)/43 = 2907 ppm on
                CLKOUT0 here - three orders of magnitude too coarse for
                a +-100 ppm/sub-ppm media servo, and every change costs
                a reset+relock outage. The documented ppm-capable MMCM
                actuator is the fine phase shift; the DRP engine is kept
                for what DRP is actually for (divider reprogramming,
                verified/sequenced), fully implemented and TB-proven.

                States (status_o[2:0]): IDLE (clock_source != 2: no DRP
                access, no PS steps, u = 0), VERIFY, REPAIR, ACQUIRE,
                LOCKED (|e| < LOCK_THR_P for LOCK_WIN_P windows),
                HOLDOVER (CRF unlock: u frozen, stepping continues at
                the held rate), FAULT (repair relock timeout).

                PI micro-sequence (mf51 timing fix): the window update is
                a once-per-512-ms event, so the PI arithmetic runs as a
                7-cycle micro-sequence instead of one combinational cone
                (mf51 evidence: ptp_q_r_reg -> u_cmd_r_reg, 21.9 ns data
                path, 49 logic levels / 39 CARRY4 - the whole span sub +
                NORM + ECLAMP + PI + slew evaluated in ONE clk cycle and
                missed timing on ALL seeds). One arithmetic step per
                stage, ~140 ns added latency = 3e-7 of the window:
                  T0  boundary tick: 64-bit span sub, crf_rate snapshot
                  S1  64-bit - NOM_WIN_NS_P, <<< NORM_SHIFT_P
                  S2  ECLAMP clamp (compares + mux)
                  S3  e = locerr - rate (32-bit sub) -> ew_r
                  S4  integ + e>>KI (32-bit add) | lock-threshold cmp
                  S5  integrator clamp | + e>>KP (32-bit add)
                  S6  output clamp | - u_cmd (32-bit sub)
                  S7  slew select + writeback (u_cmd, integ, lock_cnt)
                The u*GAIN_NUM_P product feeding the PS accumulator is
                registered in its own stage (u_gain_r; u_cmd_r changes
                >= 1 tick before the next accumulate). Bit-for-bit the
                same loop results, k cycles later; the sequence aborts if
                the servo leaves the active states (IDLE then clears
                u/integ anyway).

                Clock domains: clk_i (datapath; also the DRP DCLK -
                DS181 FDCK max 200 MHz), clk_audio_i (tick divider
                only), ps_clk_i (PS runner; DS181 MMCM_FMAX_PSCLK 450
                MHz at -1 - the SoC feeds the 200 MHz idelay clock so
                the sustained-slew ceiling PSCLK/13 * step covers
                (10.6 + 100) ppm with >2x margin). Batches cross
                clk_i -> ps_clk_i through the library cdc_handshake.

  Spec refs   : Milan v1.2 7.3.2-7.3.4; IEEE 1722-2016 Clause 10;
                Xilinx UG472 (v1.13) ch.3 "Interpolated Fine Phase Shift
                / Dynamic Phase Shift Interface in the MMCM",
                "Frequency Synthesis Using Fractional Divide";
                Xilinx XAPP888 (v1.8) Tables 1-15 (DRP register map);
                Xilinx DS181 (v1.27) MMCM switching characteristics.
  Company     : Kebag Logic
  Project     : Milan AVB endstation
------------------------------------------------------------------------------
*/
//---------------------------------------------------------------------------//

`default_nettype none

module KL_mmcm_drp_servo #(
  parameter int unsigned CLK_FREQ_HZ_P    = 50_000_000,   //! clk_i frequency
  //! local media-rate window: TICK_CYC_P audio cycles per tick (24576 @
  //! 24.576 MHz = 1 ms), 2^WIN_LOG2_P ticks per window (512 => 512 ms,
  //! matching the KL_crf_rx 256-PDU rate window 1:1)
  parameter int unsigned TICK_CYC_P       = 24576,
  parameter int unsigned WIN_LOG2_P       = 9,
  parameter longint unsigned NOM_WIN_NS_P = 64'd512_000_000,
  parameter int unsigned NORM_SHIFT_P     = 0,    //! log2(512 ms / window)
  //! PI gains (u and e share units, plant gain ~1 by GAIN_NUM_P design):
  //! integrator halves the error per window, small P term for transient
  parameter int unsigned KI_SHIFT_P       = 1,
  parameter int unsigned KP_SHIFT_P       = 2,
  parameter int signed   U_MAX_P          = 102_400,  //! +-200 ppm (x512)
  parameter int signed   SLEW_MAX_P       = 51_200,   //! +-100 ppm / window
  parameter int signed   LOCK_THR_P       = 1_024,    //! 2 ppm
  parameter int unsigned LOCK_WIN_P       = 4,
  //! u -> PS steps per tick: batch = (u * GAIN_NUM_P) >> 9.
  //! GAIN_NUM_P = round( (56 * F_VCO / 1e9) * tick_ns * 512 / 512 )
  //!            = round( 56 * 1.0567568 * 1.0 )  = 59  (1 ms tick)
  parameter int unsigned GAIN_NUM_P       = 59,
  parameter int unsigned PS_TOUT_CYC_P    = 255,        //! PSDONE watchdog
  parameter int unsigned RELOCK_TOUT_P    = 1 << 17,    //! post-repair LOCKED wait
  //! expected CLKOUT0 divider config for O = 43 (XAPP888 Table 1/2 field
  //! packing; bench-verify against the Vivado attribute encoding before
  //! enabling auto_repair_i - see the bring-up checklist):
  //!   ClkReg1 0x08: PHASE_MUX=0, HIGH_TIME=22 [11:6], LOW_TIME=21 [5:0]
  //!   ClkReg2 0x09: FRAC=0, FRAC_EN=0 (fine-PS mode), FRAC_WF_R=0,
  //!                 MX=00, EDGE=1 (odd divide), NO_COUNT=0, DELAY=0
  //! masks exclude the XAPP888 "RESERVED - retain previous value" bits
  //! (ClkReg1 [12], ClkReg2 [15])
  parameter logic [15:0] CFG_C0R1_P       = 16'h0595,
  parameter logic [15:0] CFG_C0R1_MASK_P  = 16'hEFFF,
  parameter logic [15:0] CFG_C0R2_P       = 16'h0080,
  parameter logic [15:0] CFG_C0R2_MASK_P  = 16'h7FFF
) (
  input  wire         clk_i,          //! datapath clock (= MMCM DCLK domain)
  input  wire         rst_n,          //! active-low reset (clk_i)
  input  wire         clk_audio_i,    //! MMCM CLKOUT0 (the measured clock)
  input  wire         ps_clk_i,       //! MMCM PSCLK domain (SoC: 200 MHz idelay)

  input  wire [63:0]  ptp_now_i,      //! gPTP-synced time (ns, clk_i)
  input  wire [15:0]  clk_src_i,      //! live clock_source_index (2 = CRF)
  input  wire         crf_locked_i,   //! KL_crf_rx locked_o
  input  wire signed [31:0] crf_rate_i, //! KL_crf_rx rate_o (ns / 512 ms)

  input  wire         auto_repair_i,  //! 1 = DRP REPAIR allowed on mismatch
  input  wire         ps_invert_i,    //! flip the PS direction mapping (bench
                                      //! knob, MCSRV_CTRL 0x8FC[0]: 2026-07-23
                                      //! mf51 silicon stepped the WRONG way -
                                      //! rails 25x worse under the servo; the
                                      //! TB model bakes the UG472 sign, so
                                      //! only silicon can settle it)

  //! MMCME2_ADV DRP port (DCLK = clk_i; DS181 FDCK <= 200 MHz)
  output logic [6:0]  drp_addr_o,
  output logic        drp_en_o,       //! 1-cycle DEN (with drp_we_o for writes)
  output logic        drp_we_o,
  output logic [15:0] drp_di_o,
  input  wire  [15:0] drp_do_i,
  input  wire         drp_rdy_i,      //! DRDY completion pulse

  output logic        mmcm_rst_o,     //! MMCME2_ADV RST (held through repair)
  input  wire         mmcm_locked_i,  //! MMCME2_ADV LOCKED (async)

  //! MMCME2_ADV dynamic fine phase shift port (ps_clk_i domain, UG472)
  output logic        ps_en_o,        //! 1-PSCLK-cycle PSEN
  output logic        ps_incdec_o,    //! 1 = increment (delay = slow down)
  input  wire         ps_done_i,      //! PSDONE (12 PSCLK cycles after PSEN)

  output logic [31:0] status_o        //! A_MCSRV_STAT (0x8F8) readback
);

  // ------------------------------------------------------------------ //
  //  XAPP888 (v1.8) Table 15 DRP address map (7 series)                 //
  // ------------------------------------------------------------------ //
  localparam logic [6:0] DADDR_C0R1_C  = 7'h08;  //! CLKOUT0 Register 1
  localparam logic [6:0] DADDR_C0R2_C  = 7'h09;  //! CLKOUT0 Register 2
  localparam logic [6:0] DADDR_POWER_C = 7'h28;  //! Power Register (7 series)
  //! (0x14/0x15 CLKFBOUT, 0x16 DIVCLK, 0x18-0x1A LockReg1-3, 0x4E/0x4F
  //!  FiltReg1-2 exist per Table 15 but are deliberately NOT touched:
  //!  this servo never changes M or D, and XAPP888's lock/filter lookup
  //!  tables only need rewriting when M changes.)
  localparam logic [15:0] POWER_ALL_C  = 16'hFFFF; //! XAPP888 Table 14

  localparam int unsigned WIN_TICKS_C = 1 << WIN_LOG2_P;
  localparam int signed   ECLAMP_C    = 32'sd1 << 20;  //! window-error bound
  //! step guard: |e| beyond this (1024 ppm at 512 units/ppm) is not a
  //! plant error, it is a broken measurement (local PHC step) - discard
  localparam int signed   GUARD_THR_C = 32'sd1 << 19;
  localparam int unsigned DISC_MAX_C  = 4;  //! consecutive discards -> resync

  // ------------------------------------------------------------------ //
  //  Audio-domain tick divider (TICK_CYC_P cycles -> 1 pulse)           //
  // ------------------------------------------------------------------ //
  logic [1:0] arst_sync_r;               //! audio-domain reset sync
  wire        arst_n_w = arst_sync_r[1];
  always_ff @(posedge clk_audio_i) begin : audio_rst_sync
    arst_sync_r <= {arst_sync_r[0], rst_n};
  end : audio_rst_sync

  logic [$clog2(TICK_CYC_P)-1:0] tick_div_r;
  logic                          tick_a_r;
  always_ff @(posedge clk_audio_i) begin : tick_div
    if (!arst_n_w) begin
      tick_div_r <= '0;
      tick_a_r   <= 1'b0;
    end else if (tick_div_r == $bits(tick_div_r)'(TICK_CYC_P - 1)) begin
      tick_div_r <= '0;
      tick_a_r   <= 1'b1;
    end else begin
      tick_div_r <= tick_div_r + 1'b1;
      tick_a_r   <= 1'b0;
    end
  end : tick_div

  wire tick_p_w;
  cdc_pulse u_tick_cdc (
    .src_clk    (clk_audio_i),
    .src_rst_n  (arst_n_w),
    .src_pulse  (tick_a_r),
    .dest_clk   (clk_i),
    .dest_rst_n (rst_n),
    .dest_pulse (tick_p_w)
  );

  // ------------------------------------------------------------------ //
  //  Synchronizers into clk_i                                           //
  // ------------------------------------------------------------------ //
  (* ASYNC_REG = "TRUE" *) logic [1:0] locked_sync_r;
  (* ASYNC_REG = "TRUE" *) logic [1:0] psbusy_sync_r;
  (* ASYNC_REG = "TRUE" *) logic [1:0] psfault_sync_r;
  logic ps_busy_ps_r;                  //! runner busy level (ps_clk domain)
  logic ps_fault_ps_r;                 //! sticky PSDONE-watchdog fault

  always_ff @(posedge clk_i) begin : in_syncs
    if (!rst_n) begin
      locked_sync_r  <= '0;
      psbusy_sync_r  <= '0;
      psfault_sync_r <= '0;
    end else begin
      locked_sync_r  <= {locked_sync_r[0],  mmcm_locked_i};
      psbusy_sync_r  <= {psbusy_sync_r[0],  ps_busy_ps_r};
      psfault_sync_r <= {psfault_sync_r[0], ps_fault_ps_r};
    end
  end : in_syncs

  wire mmcm_locked_s_w = locked_sync_r[1];
  wire ps_busy_s_w     = psbusy_sync_r[1];
  wire ps_fault_s_w    = psfault_sync_r[1];

  // ------------------------------------------------------------------ //
  //  Servo state                                                        //
  // ------------------------------------------------------------------ //
  typedef enum logic [2:0] {
    IDLE_S     = 3'd0,
    VERIFY_S   = 3'd1,
    REPAIR_S   = 3'd2,
    ACQUIRE_S  = 3'd3,
    LOCKED_S   = 3'd4,
    HOLDOVER_S = 3'd5,
    FAULT_S    = 3'd6
  } servo_state_t;

  //! DRP micro-sequence (shared by VERIFY and REPAIR)
  typedef enum logic [3:0] {
    D_IDLE_S, D_RD_EN_S, D_RD_WAIT_S, D_WR_EN_S, D_WR_WAIT_S,
    D_QUIESCE_S, D_RSTON_S, D_PWR_EN_S, D_PWR_WAIT_S, D_RELOCK_S
  } drp_state_t;

  servo_state_t state_r;
  drp_state_t   dstate_r;

  wire servo_sel_w = (clk_src_i == 16'd2);

  //! local window measurement
  logic [WIN_LOG2_P:0]      tick_cnt_r;
  logic [63:0]              win_start_r;
  logic                     win_valid_r;
  logic [1:0]               win_skip_r;   //! PI warm-up (crf ring refill)
  logic signed [31:0]       ew_r;         //! last window error (normalized)
  logic [1:0]               disc_run_r;   //! consecutive guard-discarded windows
  logic [5:0]               disc_cnt_r;   //! saturating discard total (status)

  //! PI
  logic signed [23:0]       integ_r, u_cmd_r;
  logic [$clog2(LOCK_WIN_P+1)-1:0] lock_cnt_r;

  //! PI micro-sequence registers (see header: mf51 one-cycle-cone fix;
  //! one add/sub or one clamp per stage, once per window)
  logic [2:0]               pp_seq_r;     //! 0 = idle, 1..7 = stage
  logic                     pp_run_r;     //! writeback armed (no skip/holdover)
  logic signed [63:0]       pp_d_r;       //! T0: raw window span
  logic signed [63:0]       pp_spann_r;   //! S1: span - nominal, normalized
  logic signed [31:0]       pp_locerr_r;  //! S2: ECLAMP-bounded local error
  logic signed [31:0]       pp_rate_r;    //! T0: crf_rate_i boundary snapshot
  logic signed [31:0]       pp_isum_r;    //! S4: integ + e>>KI (pre-clamp)
  logic                     pp_thr_r;     //! S4: |e| < LOCK_THR_P
  logic signed [23:0]       pp_ig_r;      //! S5: clamped next integrator
  logic signed [31:0]       pp_un_r;      //! S5: ig + e>>KP (pre-clamp)
  logic signed [23:0]       pp_ut_r;      //! S6: clamped PI output
  logic signed [31:0]       pp_du_r;      //! S6: ut - u_cmd (pre-slew)
  logic signed [31:0]       u_gain_r;     //! registered u_cmd * GAIN_NUM_P

  //! PS batch accumulator + handshake
  logic signed [31:0]       acc_r;
  logic                     hs_send_r;
  logic [14:0]              hs_data_r;    //! {incdec, count[13:0]}
  wire                      hs_rcv_w;
  logic                     ps_hold_r;    //! quiesce request (DRP repair)

  //! DRP sequencing
  logic                     drp_pass_r;   //! current reg pair verified equal
  logic                     rd_second_r;  //! 0 = 0x08, 1 = 0x09
  logic                     repairing_r;  //! this pass may write
  logic [15:0]              rd_val_r;
  logic                     verified_r, mismatch_r, drp_fault_r;
  logic [$clog2(RELOCK_TOUT_P+1)-1:0] relock_r;
  logic [3:0]               rst_settle_r;

  wire [15:0] exp_val_w  = rd_second_r ? CFG_C0R2_P      : CFG_C0R1_P;
  wire [15:0] exp_mask_w = rd_second_r ? CFG_C0R2_MASK_P : CFG_C0R1_MASK_P;

  //! ptp_now_i staged once: the live 64-bit gPTP accumulator must not
  //! feed the T0 span subtract combinationally. One cycle of staleness
  //! against the 512 ms window is 2e-6 % - free timing. (The rest of
  //! the old one-cycle PI cone is the micro-sequence above.)
  logic [63:0] ptp_q_r;
  always_ff @(posedge clk_i) begin : ptp_stage_S
    ptp_q_r <= ptp_now_i;
  end

  function automatic logic signed [23:0] clamp_u(input logic signed [31:0] v);
    if (v > 32'(U_MAX_P))       return 24'(U_MAX_P);
    else if (v < -32'(U_MAX_P)) return 24'(-U_MAX_P);
    else                        return 24'(v);
  endfunction

  always_ff @(posedge clk_i) begin : servo_engine
    if (!rst_n) begin
      state_r  <= IDLE_S;   dstate_r <= D_IDLE_S;
      tick_cnt_r <= '0;     win_start_r <= '0;
      win_valid_r <= 1'b0;  win_skip_r <= '0;
      disc_run_r <= '0;     disc_cnt_r <= '0;
      ew_r <= '0;           integ_r <= '0;      u_cmd_r <= '0;
      lock_cnt_r <= '0;     acc_r <= '0;
      hs_send_r <= 1'b0;    hs_data_r <= '0;    ps_hold_r <= 1'b0;
      drp_addr_o <= '0;     drp_en_o <= 1'b0;   drp_we_o <= 1'b0;
      drp_di_o <= '0;       mmcm_rst_o <= 1'b0;
      drp_pass_r <= 1'b0;   rd_second_r <= 1'b0; repairing_r <= 1'b0;
      rd_val_r <= '0;       verified_r <= 1'b0; mismatch_r <= 1'b0;
      drp_fault_r <= 1'b0;  relock_r <= '0;     rst_settle_r <= '0;
      pp_seq_r <= '0;       pp_run_r <= 1'b0;
      pp_d_r <= '0;         pp_spann_r <= '0;   pp_locerr_r <= '0;
      pp_rate_r <= '0;      pp_isum_r <= '0;    pp_thr_r <= 1'b0;
      pp_ig_r <= '0;        pp_un_r <= '0;      pp_ut_r <= '0;
      pp_du_r <= '0;        u_gain_r <= '0;
    end else begin
      drp_en_o <= 1'b0;
      drp_we_o <= 1'b0;
      if (hs_send_r && hs_rcv_w) hs_send_r <= 1'b0;
      //! GAIN stage: registered product keeps the multiplier cone out of
      //! the acc_r adder (u_cmd_r settles >= 1 tick before the next use)
      u_gain_r <= 32'(u_cmd_r) * 32'(GAIN_NUM_P);

      // ---------------- top-level servo FSM ----------------
      unique case (state_r)
        IDLE_S: begin
          u_cmd_r <= '0; integ_r <= '0; acc_r <= '0;
          win_valid_r <= 1'b0; lock_cnt_r <= '0;
          disc_run_r <= '0; disc_cnt_r <= '0;
          verified_r <= 1'b0; mismatch_r <= 1'b0; drp_fault_r <= 1'b0;
          mmcm_rst_o <= 1'b0; ps_hold_r <= 1'b0;
          if (servo_sel_w && crf_locked_i) begin
            state_r     <= VERIFY_S;
            dstate_r    <= D_RD_EN_S;
            rd_second_r <= 1'b0;
            drp_pass_r  <= 1'b1;
            repairing_r <= 1'b0;
          end
        end

        VERIFY_S, REPAIR_S: begin
          if (!servo_sel_w) begin
            //! abort: never leave the MMCM in reset
            mmcm_rst_o <= 1'b0;
            dstate_r   <= D_IDLE_S;
            state_r    <= IDLE_S;
          end
        end

        ACQUIRE_S, LOCKED_S: begin
          if (!servo_sel_w)          state_r <= IDLE_S;
          else if (!crf_locked_i)    state_r <= HOLDOVER_S;
          else if (state_r == ACQUIRE_S && lock_cnt_r >=
                   ($bits(lock_cnt_r))'(LOCK_WIN_P)) state_r <= LOCKED_S;
          else if (state_r == LOCKED_S && lock_cnt_r == '0)
                                     state_r <= ACQUIRE_S;
        end

        HOLDOVER_S: begin
          //! u frozen (stepping continues below) until CRF returns
          if (!servo_sel_w)          state_r <= IDLE_S;
          else if (crf_locked_i) begin
            state_r    <= ACQUIRE_S;
            win_skip_r <= 2'd2;      //! crf_rate ring refills for 512 ms
            lock_cnt_r <= '0;
          end
        end

        FAULT_S: begin
          mmcm_rst_o <= 1'b0;
          if (!servo_sel_w) state_r <= IDLE_S;
        end

        default: state_r <= IDLE_S;
      endcase

      // ---------------- local rate window + PI ----------------
      if (state_r inside {ACQUIRE_S, LOCKED_S, HOLDOVER_S}) begin
        if (tick_p_w) begin
          if (!win_valid_r) begin
            win_start_r <= ptp_q_r;
            win_valid_r <= 1'b1;
            tick_cnt_r  <= '0;
          end else if (tick_cnt_r == (WIN_LOG2_P+1)'(WIN_TICKS_C - 1)) begin
            //! T0: window boundary - snapshot the operands, kick the
            //! micro-sequence (next boundary is a full window away)
            tick_cnt_r  <= '0;
            win_start_r <= ptp_q_r;
            pp_d_r      <= $signed(ptp_q_r - win_start_r);
            pp_rate_r   <= crf_rate_i;
            pp_run_r    <= (win_skip_r == '0) && (state_r != HOLDOVER_S);
            pp_seq_r    <= 3'd1;
            if (win_skip_r != '0)
              win_skip_r <= win_skip_r - 2'd1;
          end else begin
            tick_cnt_r <= tick_cnt_r + 1'b1;
          end

        end

        //! PI micro-sequence: one arithmetic step per cycle (mf51 fix,
        //! see header). ew_r/writebacks land bit-for-bit as the old
        //! single-cycle cone, 3..7 cycles after the boundary tick.
        unique case (pp_seq_r)
          3'd0: ;
          3'd1: begin : pi_norm_S
            pp_spann_r <= (pp_d_r - $signed(NOM_WIN_NS_P)) <<< NORM_SHIFT_P;
            pp_seq_r   <= 3'd2;
          end : pi_norm_S
          3'd2: begin : pi_eclamp_S
            //! window error, clamped (a dead/garbage audio clock must
            //! not wrap the PI)
            pp_locerr_r <= (pp_spann_r >  64'(ECLAMP_C)) ?  ECLAMP_C
                         : (pp_spann_r < -64'(ECLAMP_C)) ? -ECLAMP_C
                         : 32'(pp_spann_r);
            pp_seq_r    <= 3'd3;
          end : pi_eclamp_S
          3'd3: begin : pi_err_S
            ew_r     <= pp_locerr_r - pp_rate_r;
            pp_seq_r <= 3'd4;
          end : pi_err_S
          3'd4: begin : pi_isum_S
            pp_isum_r <= 32'(integ_r) + (ew_r >>> KI_SHIFT_P);
            pp_thr_r  <= (ew_r < LOCK_THR_P) && (ew_r > -LOCK_THR_P);
            //! step guard: an implausible window error (|e| > 1024 ppm
            //! equivalent - a local PHC step, not the plant) is squashed
            //! like a win_skip window: pp_run_r cleared before the S7
            //! writeback, so u_cmd/integ/lock_cnt all hold. DISC_MAX_C
            //! consecutive discards resync the window baseline (CRF-
            //! relock pattern: win_valid_r drops, PI state kept)
            if (pp_run_r &&
                ((ew_r > GUARD_THR_C) || (ew_r < -GUARD_THR_C))) begin
              pp_run_r <= 1'b0;
              if (disc_cnt_r != 6'h3F)
                disc_cnt_r <= disc_cnt_r + 6'd1;
              if (disc_run_r == 2'(DISC_MAX_C - 1)) begin
                win_valid_r <= 1'b0;
                disc_run_r  <= '0;
              end else begin
                disc_run_r <= disc_run_r + 2'd1;
              end
            end
            pp_seq_r  <= 3'd5;
          end : pi_isum_S
          3'd5: begin : pi_pterm_S
            pp_ig_r  <= clamp_u(pp_isum_r);
            pp_un_r  <= 32'(clamp_u(pp_isum_r)) + (ew_r >>> KP_SHIFT_P);
            pp_seq_r <= 3'd6;
          end : pi_pterm_S
          3'd6: begin : pi_uclamp_S
            pp_ut_r  <= clamp_u(pp_un_r);
            pp_du_r  <= 32'(clamp_u(pp_un_r)) - 32'(u_cmd_r);
            pp_seq_r <= 3'd7;
          end : pi_uclamp_S
          3'd7: begin : pi_wb_S
            if (pp_run_r) begin
              disc_run_r <= '0;   //! a committed window ends the streak
              //! bounded step (slew limit)
              if (pp_du_r > 32'(SLEW_MAX_P))
                u_cmd_r <= u_cmd_r + 24'(SLEW_MAX_P);
              else if (pp_du_r < -32'(SLEW_MAX_P))
                u_cmd_r <= u_cmd_r - 24'(SLEW_MAX_P);
              else
                u_cmd_r <= pp_ut_r;
              integ_r <= pp_ig_r;
              //! frequency-lock qualification
              if (pp_thr_r) begin
                if (lock_cnt_r != ($bits(lock_cnt_r))'(LOCK_WIN_P))
                  lock_cnt_r <= lock_cnt_r + 1'b1;
              end else begin
                lock_cnt_r <= '0;
              end
            end
            pp_seq_r <= '0;
          end : pi_wb_S
          default: pp_seq_r <= '0;
        endcase

        //! PS batch accumulation + dispatch (single acc_r update: the
        //! tick add and the batch subtract may land on the same cycle)
        begin : dispatch
          automatic logic signed [31:0] a_v, b_v;
          a_v = acc_r;
          if (tick_p_w && !ps_hold_r)
            a_v = a_v + u_gain_r;
          if (!hs_send_r && !ps_busy_s_w && !ps_hold_r) begin
            b_v = acc_r >>> 9;
            if (b_v > 32'sd16383)  b_v = 32'sd16383;
            if (b_v < -32'sd16383) b_v = -32'sd16383;
            if (b_v != 0) begin
              //! u > 0 = speed up = PS decrement (UG472: increment delays);
              //! ps_invert_i flips the mapping (see the port comment)
              hs_data_r <= (b_v > 0) ? {ps_invert_i,  14'(b_v)}
                                     : {~ps_invert_i, 14'(-b_v)};
              hs_send_r <= 1'b1;
              a_v       = a_v - (b_v <<< 9);
            end
          end
          acc_r <= a_v;
        end : dispatch
      end else begin
        //! micro-sequence abort on leaving the active states (only IDLE
        //! is reachable mid-flight; IDLE clears u/integ every cycle, so
        //! dropping the in-flight update matches the one-cycle original)
        pp_seq_r <= '0;
      end

      // ---------------- DRP micro-sequencer ----------------
      unique case (dstate_r)
        D_IDLE_S: ;

        //! read phase: DEN one cycle, wait DRDY (UG472/DS181 DRP timing)
        D_RD_EN_S: begin
          drp_addr_o <= rd_second_r ? DADDR_C0R2_C : DADDR_C0R1_C;
          drp_en_o   <= 1'b1;
          dstate_r   <= D_RD_WAIT_S;
        end
        D_RD_WAIT_S: if (drp_rdy_i) begin
          rd_val_r <= drp_do_i;
          if ((drp_do_i & exp_mask_w) != (exp_val_w & exp_mask_w))
            drp_pass_r <= 1'b0;
          if (repairing_r) begin
            dstate_r <= D_WR_EN_S;
          end else if (!rd_second_r) begin
            rd_second_r <= 1'b1;
            dstate_r    <= D_RD_EN_S;
          end else if (drp_pass_r &&
                       ((drp_do_i & exp_mask_w) == (exp_val_w & exp_mask_w)))
          begin
            verified_r <= 1'b1;
            dstate_r   <= D_IDLE_S;
            state_r    <= ACQUIRE_S;
            win_valid_r <= 1'b0;
            win_skip_r  <= 2'd1;
          end else begin
            mismatch_r <= 1'b1;
            if (auto_repair_i) begin
              state_r     <= REPAIR_S;
              ps_hold_r   <= 1'b1;
              dstate_r    <= D_QUIESCE_S;
            end else begin
              //! informative only: PS servo runs on the live config
              dstate_r    <= D_IDLE_S;
              state_r     <= ACQUIRE_S;
              win_valid_r <= 1'b0;
              win_skip_r  <= 2'd1;
            end
          end
        end

        //! repair: quiesce fine PS first (XAPP888: no fine-phase shifting
        //! during reconfiguration), then hold RST through all writes
        D_QUIESCE_S: if (!ps_busy_s_w && !hs_send_r) begin
          mmcm_rst_o   <= 1'b1;
          rst_settle_r <= 4'd15;
          dstate_r     <= D_RSTON_S;
        end
        D_RSTON_S: begin
          if (rst_settle_r == '0) dstate_r <= D_PWR_EN_S;
          else                    rst_settle_r <= rst_settle_r - 4'd1;
        end
        D_PWR_EN_S: begin
          drp_addr_o <= DADDR_POWER_C;
          drp_di_o   <= POWER_ALL_C;     //! XAPP888 Table 14
          drp_en_o   <= 1'b1;
          drp_we_o   <= 1'b1;
          dstate_r   <= D_PWR_WAIT_S;
        end
        D_PWR_WAIT_S: if (drp_rdy_i) begin
          rd_second_r <= 1'b0;
          dstate_r    <= D_RD_EN_S;      //! RMW: read 0x08 first
        end
        D_WR_EN_S: begin
          //! merge: keep RESERVED bits from the readback (XAPP888)
          drp_addr_o <= rd_second_r ? DADDR_C0R2_C : DADDR_C0R1_C;
          drp_di_o   <= (rd_val_r & ~exp_mask_w) | (exp_val_w & exp_mask_w);
          drp_en_o   <= 1'b1;
          drp_we_o   <= 1'b1;
          dstate_r   <= D_WR_WAIT_S;
        end
        D_WR_WAIT_S: if (drp_rdy_i) begin
          if (!rd_second_r) begin
            rd_second_r <= 1'b1;
            dstate_r    <= D_RD_EN_S;
          end else begin
            mmcm_rst_o <= 1'b0;          //! release, await relock
            relock_r   <= ($bits(relock_r))'(RELOCK_TOUT_P);
            dstate_r   <= D_RELOCK_S;
          end
        end
        D_RELOCK_S: begin
          if (mmcm_locked_s_w) begin
            verified_r  <= 1'b1;
            ps_hold_r   <= 1'b0;
            dstate_r    <= D_IDLE_S;
            state_r     <= ACQUIRE_S;
            win_valid_r <= 1'b0;
            win_skip_r  <= 2'd1;
          end else if (relock_r == '0) begin
            drp_fault_r <= 1'b1;
            ps_hold_r   <= 1'b0;
            dstate_r    <= D_IDLE_S;
            state_r     <= FAULT_S;
          end else begin
            relock_r <= relock_r - 1'b1;
          end
        end

        default: dstate_r <= D_IDLE_S;
      endcase

      //! entering repair pass: writes follow each read
      if (state_r == REPAIR_S && dstate_r == D_QUIESCE_S)
        repairing_r <= 1'b1;
      if (state_r inside {IDLE_S, ACQUIRE_S})
        repairing_r <= 1'b0;
    end
  end : servo_engine

  // ------------------------------------------------------------------ //
  //  Batch handshake into the PS runner                                 //
  // ------------------------------------------------------------------ //
  logic [1:0] psrst_sync_r;              //! ps_clk-domain reset sync
  wire        psrst_n_w = psrst_sync_r[1];
  always_ff @(posedge ps_clk_i) begin : ps_rst_sync
    psrst_sync_r <= {psrst_sync_r[0], rst_n};
  end : ps_rst_sync

  wire [14:0] ps_cmd_w;
  wire        ps_req_w;
  cdc_handshake #(.WIDTH(15)) u_batch_hs (
    .src_clk    (clk_i),
    .src_rst_n  (rst_n),
    .src_in     (hs_data_r),
    .src_send   (hs_send_r),
    .src_rcv    (hs_rcv_w),
    .dest_clk   (ps_clk_i),
    .dest_rst_n (psrst_n_w),
    .dest_out   (ps_cmd_w),
    .dest_req   (ps_req_w)
  );

  // ------------------------------------------------------------------ //
  //  PS runner (ps_clk_i): PSEN 1 cycle, wait PSDONE (12 PSCLK cycles   //
  //  deterministic per UG472), repeat count times. 1-deep pending slot  //
  //  absorbs the handshake-ack vs busy-sync race.                       //
  // ------------------------------------------------------------------ //
  typedef enum logic [1:0] { P_IDLE_S, P_EN_S, P_WAIT_S } ps_state_t;
  ps_state_t                    pstate_r;
  logic [13:0]                  ps_cnt_r;
  logic                         ps_dir_r;
  logic                         pend_v_r;
  logic [14:0]                  pend_r;
  logic [$clog2(PS_TOUT_CYC_P+1)-1:0] ps_wd_r;

  always_ff @(posedge ps_clk_i) begin : ps_runner
    if (!psrst_n_w) begin
      pstate_r <= P_IDLE_S;
      ps_en_o <= 1'b0; ps_incdec_o <= 1'b0;
      ps_cnt_r <= '0;  ps_dir_r <= 1'b0;
      pend_v_r <= 1'b0; pend_r <= '0;
      ps_busy_ps_r <= 1'b0; ps_fault_ps_r <= 1'b0;
      ps_wd_r <= '0;
    end else begin
      ps_en_o <= 1'b0;
      if (ps_req_w) begin
        pend_v_r <= 1'b1;
        pend_r   <= ps_cmd_w;
      end

      unique case (pstate_r)
        P_IDLE_S: begin
          ps_busy_ps_r <= pend_v_r || ps_req_w;
          if (pend_v_r) begin
            ps_dir_r <= pend_r[14];
            ps_cnt_r <= pend_r[13:0];
            pend_v_r <= ps_req_w;        //! consumed (unless refilled now)
            pstate_r <= P_EN_S;
          end
        end
        P_EN_S: begin
          ps_busy_ps_r <= 1'b1;
          //! UG472: "PSEN must be active for one PSCLK period";
          //! PSINCDEC high = increment = delay the output (slow down)
          ps_en_o     <= 1'b1;
          ps_incdec_o <= ps_dir_r;
          ps_wd_r     <= ($bits(ps_wd_r))'(PS_TOUT_CYC_P);
          pstate_r    <= P_WAIT_S;
        end
        P_WAIT_S: begin
          if (ps_done_i) begin
            if (ps_cnt_r <= 14'd1) pstate_r <= P_IDLE_S;
            else begin
              ps_cnt_r <= ps_cnt_r - 14'd1;
              pstate_r <= P_EN_S;
            end
          end else if (ps_wd_r == '0) begin
            ps_fault_ps_r <= 1'b1;       //! sticky: PSDONE never came
            pstate_r      <= P_IDLE_S;
          end else begin
            ps_wd_r <= ps_wd_r - 1'b1;
          end
        end
        default: pstate_r <= P_IDLE_S;
      endcase
    end
  end : ps_runner

  // ------------------------------------------------------------------ //
  //  Status readback (A_MCSRV_STAT 0x8F8)                               //
  // ------------------------------------------------------------------ //
  wire signed [15:0] trim_w = 16'(u_cmd_r >>> 5);  //! 1/16 ppm units
  assign status_o = {trim_w,                       //! [31:16] signed trim
                     disc_cnt_r,                   //! [15:10] guard discards
                     1'b0,                         //! [9]     reserved
                     drp_fault_r,                  //! [8]
                     ps_fault_s_w,                 //! [7]
                     (ps_busy_s_w | hs_send_r),    //! [6]
                     mmcm_locked_s_w,              //! [5]
                     mismatch_r,                   //! [4]
                     verified_r,                   //! [3]
                     state_r};                     //! [2:0]

endmodule

`default_nettype wire

/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

//---------------------------------------------------------------------------//
/*
------------------------------------------------------------------------------
  File        : KL_ptp_clock_validity.sv
  Description : The one place that decides whether this end station is
                allowed to claim its AVTP presentation times correspond
                to gPTP time. Its single output is the AVTP "tu"
                (timestamp uncertain) bit that EVERY talker in the
                fabric stamps into every Stream Data AVTPDU it emits
                (AAF packetizer, legacy AAF talker, CRF talker).

                WHY IT EXISTS (measured, 2026-07-27). Our Arty streamed
                31 M AAF frames whose presentation times came from a PHC
                216,446 s (60 h) away from the domain, at full rate,
                with tu hard-wired to 0 the whole time. The receiving
                Milan device counted 99.4 % of them LATE or EARLY and
                had no way to defend itself, because the only field that
                exists to warn it - tu - said "the timestamps are fine".
                See docs/findings/REF_LISTENER_TIMESTAMP_SWEEP_0727.md.

                WHAT THE STANDARD ACTUALLY REQUIRES. Not "stop
                streaming": Milan v1.2 5.3.7.3 forbids that outright
                ("it shall be streaming AVTP packets ... STREAMING_WAIT
                shall not be implemented"). Not tv=0 either: IEEE
                1722-2016 7.5 makes tv=1 mandatory for every AAF AVTPDU
                when sp=0, which is our shape. The prescribed behaviour
                is to KEEP STREAMING and RAISE tu - Milan v1.2 4.3.5.2
                ("A Talker PAAD shall set the AVTP tu bit as described
                in [AVTP, Clause 4.4.4.7]"), IEEE 1722-2016 4.4.4.7, and
                Milan v1.2 Annex B.1.1 (on a grandmaster change tu shall
                be 1 for at least 0.25 s).

                THE THREE TERMS, and where each one's evidence lives:

                  * SOFTWARE LEASE (sw_*). Whether the PHC is actually
                    disciplined to the domain is a servo fact: it lives
                    in ptp4l's offset/frequency state and NOTHING in
                    fabric can observe it. That is not merely a wiring
                    gap, it is information-theoretic - see
                    docs/design/PRESENTATION_TIME_WRAP.md: avtp_timestamp
                    is the LOW 32 BITS of an unsigned nanosecond count,
                    so it laps every 4.294967296 s, and once the true
                    offset exceeds one lap the modular difference carries
                    no information about the direction OR the magnitude
                    of the error. A far-off clock produces blocks of
                    100 % LATE and blocks of 100 % EARLY that are
                    indistinguishable from a well-behaved error signal -
                    which is precisely the square wave measured on
                    2026-07-27. No listener-side heuristic, and no
                    fabric-side observation of our own wire, can recover
                    the truth; only the talker's own servo knows. So
                    software publishes it -
                    the established gptp2csr.sh pattern (GM id 0x624/8,
                    pdelay 0x6E4, AS_PATH 0x730/4) - and it publishes it
                    as a LEASE, not a flag: every CLKV_CTRL write
                    reloads a countdown, and when the countdown runs out
                    the claim lapses. A boolean written once at boot is
                    exactly the defect above (the Arty was synchronised
                    once, then drifted 60 h away while still asserting
                    health). Reset state is sync_ok=0 / lease=0, i.e.
                    UNKNOWN == NOT VALID: a build nobody teaches to
                    publish sync state emits tu=1 forever, which is the
                    honest answer, not the convenient one.

                  * FABRIC-OBSERVED PHC STEPS (phc_load_p_i /
                    phc_adj_p_i). A settime or adjtime IS a discontinuity
                    in gPTP time by construction - 1722 4.4.4.7's exact
                    trigger - and unlike sync state it is fully visible
                    here, as the PTP_CMD strobes. No software help
                    needed, no software trust required.

                  * GRANDMASTER CHANGE (gm_id_i). The daemon already
                    publishes gptp_grandmaster_id into ADP_GM_LO/HI for
                    the advertiser; a change in that value is a change
                    of grandmaster. Detecting it here gets Milan Annex
                    B.1.1 for free, with no new software contract.

                The last two arm a holdover of HOLD_QTICK_P quarter-
                seconds (default 2 -> 0.25..0.5 s against a free-running
                prescaler, so the B.1.1 minimum holds for an event at
                any phase).

                tu_ivals_o is the Milan Table 5.4 / Table 5.6
                TIMESTAMP_UNCERTAIN counter for the talker side, in
                Milan's own units: the number of one-second observation
                intervals during which tu was set at least once (Milan
                allows any interval <= 1 s). It exists so software can
                tell "tu never asserted" from "nothing computes tu" -
                the second half of the decorative-ABI fix
                (docs/limitations/RECURRING_DEFECT_PATTERNS.md 1).

                asCAPABLE RIDES THE SAME LEASE (gh #64 J3). 802.1AS-2020
                10.2.5.1: "A Boolean that is TRUE if and only if it is
                determined that this PTP Instance and the PTP Instance at
                the other end of the link attached to this PTP Port can
                interoperate with each other via the IEEE 802.1AS
                protocol" - and the clause adds that the determination is
                MEDIUM-DEPENDENT, i.e. it is the pdelay-exchange verdict
                ptp4l computes and NOTHING in fabric can observe
                (the same information boundary as the sync claim above).
                The old consumer proxied it as |pdelay CSR|, which is
                stale-true forever once the daemon dies and flag-flaps
                when a starved pmc read maps "no answer" to pdelay 0.
                So the daemon publishes its asCapable verdict as
                CLKV_CTRL[2] on the SAME write that renews the lease, and
                as_cap_r obeys the lease law sync_ok_r obeys: latched
                only with a live lease, CLEARED when the lease lapses -
                daemon death answers asCapable=0 by construction, and
                Milan v1.2 Table 5.22 (asCapable is a GET_AVB_INFO push
                trigger) fires exactly one honest edge for it.

  Spec refs   : Milan v1.2 4.3.5.2 (talker shall set tu), 5.3.7.3
                (streaming shall not stop), Annex B.1.1 (0.25 s on GM
                change), Table 5.4 / Table 5.6 (TIMESTAMP_UNCERTAIN =
                observation intervals), Table 5.22 (asCapable push);
                IEEE 802.1AS-2020 10.2.5.1 (asCapable); IEEE 1722-2016
                4.4.4.5 (tv), 4.4.4.7 (tu), 7.5 (AAF tv=1 at sp=0);
                docs/findings/REF_LISTENER_TIMESTAMP_SWEEP_0727.md
  Company     : Kebag Logic
  Project     : Milan AVB endstation
------------------------------------------------------------------------------
*/
//---------------------------------------------------------------------------//

`default_nettype none

module KL_ptp_clock_validity #(
  //! cycles per 250 ms quarter-tick (= CLK_FREQ_HZ / 4). Simulation shapes
  //! override this so a holdover and a lease expiry are reachable.
  parameter int unsigned QTICK_CYC_P  = 25_000_000,
  //! discontinuity holdover in quarter-ticks. 2 => 0.25..0.5 s against the
  //! free-running prescaler, so Milan v1.2 Annex B.1.1's 0.25 s minimum
  //! holds whatever the phase of the event.
  parameter int unsigned HOLD_QTICK_P = 2
) (
  input  wire        clk_i,           //! datapath clock
  input  wire        rst_n,           //! active-low synchronous reset

  //! --- software-published gPTP sync state (CSR CLKV_CTRL 0x778) ---------
  input  wire        sw_wr_p_i,       //! 1-cycle pulse: CLKV_CTRL was written
  input  wire        sw_sync_ok_i,    //! CLKV_CTRL[0] as written
  input  wire        sw_disc_p_i,     //! CLKV_CTRL[1] W1S: software saw a discontinuity
  input  wire        sw_as_cap_i,     //! CLKV_CTRL[2] as written: daemon's 802.1AS-2020
                                      //! 10.2.5.1 asCapable verdict (leased, like [0])
  input  wire [11:0] sw_wdog_q_i,     //! CLKV_CTRL[15:4] lease, quarter-ticks (0 = never trust)

  //! --- discontinuities this fabric can see for itself -------------------
  input  wire        phc_load_p_i,    //! PTP_CMD[0] settime applied (a step)
  input  wire        phc_adj_p_i,     //! PTP_CMD[1] adjtime applied (a step)
  input  wire [63:0] gm_id_i,         //! ADP_GM_LO/HI gptp_grandmaster_id

  //! --- verdict -----------------------------------------------------------
  output wire        ts_uncertain_o,  //! AVTP tu bit for EVERY talker (1 = uncertain)
  output wire        as_capable_o,    //! lease-backed asCapable (GET_AVB_INFO flags[0])
  output wire [31:0] stat_o,          //! CLKV_STAT 0x77C
  output wire [31:0] tu_ivals_o       //! CLKV_TUCNT 0x780 (Milan Table 5.4 counter)
);

  // --------------------------------------------------------------------
  //  250 ms prescaler - the single time base for the lease, the holdover
  //  and the observation interval.
  // --------------------------------------------------------------------
  localparam int unsigned QTICK_MAX_C = (QTICK_CYC_P < 2) ? 2 : QTICK_CYC_P;
  localparam int unsigned QDIV_W_C    = $clog2(QTICK_MAX_C);

  logic [QDIV_W_C-1:0] qdiv_r;
  logic                qtick_w;

  assign qtick_w = (qdiv_r == QDIV_W_C'(QTICK_MAX_C - 1));

  always_ff @(posedge clk_i) begin : p_prescale
    if (!rst_n) qdiv_r <= '0;
    else        qdiv_r <= qtick_w ? '0 : (qdiv_r + QDIV_W_C'(1));
  end

  // --------------------------------------------------------------------
  //  The software lease. Reset = no lease = NOT synchronised.
  //  A write with wdog = 0 is a legal way to say "never trust me": it
  //  arms an already-expired lease instead of an infinite one.
  // --------------------------------------------------------------------
  logic        sync_ok_r;
  logic        as_cap_r;
  logic [11:0] lease_r;
  logic        no_lease_r;

  always_ff @(posedge clk_i) begin : p_lease
    if (!rst_n) begin
      sync_ok_r  <= 1'b0;
      as_cap_r   <= 1'b0;
      lease_r    <= 12'd0;
      no_lease_r <= 1'b1;
    end else if (sw_wr_p_i) begin
      sync_ok_r  <= sw_sync_ok_i & (|sw_wdog_q_i);
      //! asCapable is a claim exactly like sync_ok: only a live lease can
      //! carry it, and every write re-states it (a daemon that renews the
      //! lease with [2] clear is REPORTING asCapable false, not silent)
      as_cap_r   <= sw_as_cap_i & (|sw_wdog_q_i);
      lease_r    <= sw_wdog_q_i;
      no_lease_r <= ~(|sw_wdog_q_i);
    end else if (qtick_w && (lease_r != 12'd0)) begin
      lease_r <= lease_r - 12'd1;
      if (lease_r == 12'd1) begin
        sync_ok_r  <= 1'b0;   //! the claim lapsed - stop asserting health
        as_cap_r   <= 1'b0;   //! ...and asCapable lapses WITH it (J3: a dead
                              //! daemon's last claim must not outlive it)
        no_lease_r <= 1'b1;
      end
    end
  end

  // --------------------------------------------------------------------
  //  Discontinuity holdover: PHC step, or a change of grandmaster, or a
  //  software-reported discontinuity. Milan v1.2 Annex B.1.1.
  // --------------------------------------------------------------------
  localparam int unsigned HOLD_MAX_C = (HOLD_QTICK_P < 1) ? 1 : HOLD_QTICK_P;
  localparam int unsigned HOLD_W_C   = $clog2(HOLD_MAX_C + 1);

  logic [63:0]          gm_r;
  logic [HOLD_W_C-1:0]  hold_r;
  logic                 disc_p_w;
  logic                 hold_w;

  //! gm_r resets to 0 and gm_id_i resets to 0, so the first daemon publish
  //! of a real grandmaster id IS a change and does arm the holdover. That is
  //! correct: before it we did not know who the grandmaster was.
  assign disc_p_w = phc_load_p_i | phc_adj_p_i | sw_disc_p_i | (gm_id_i != gm_r);
  assign hold_w   = (hold_r != '0);

  always_ff @(posedge clk_i) begin : p_hold
    if (!rst_n) begin
      gm_r   <= 64'd0;
      hold_r <= '0;
    end else begin
      gm_r <= gm_id_i;
      if (disc_p_w)                 hold_r <= HOLD_W_C'(HOLD_MAX_C);
      else if (qtick_w && hold_w)   hold_r <= hold_r - HOLD_W_C'(1);
    end
  end

  // --------------------------------------------------------------------
  //  The verdict. NOT a stream gate: Milan v1.2 5.3.7.3 forbids stopping
  //  a Stream Output, so the only honest lever is this bit.
  // --------------------------------------------------------------------
  assign ts_uncertain_o = (~sync_ok_r) | hold_w;

  // --------------------------------------------------------------------
  //  Milan Table 5.4 TIMESTAMP_UNCERTAIN: one increment per one-second
  //  observation interval in which tu was set at least once. 4 quarter-
  //  ticks == 1.000 s, the largest interval Milan allows.
  // --------------------------------------------------------------------
  logic [1:0]  ival_r;
  logic        tu_seen_r;
  logic [31:0] tu_ivals_r;

  always_ff @(posedge clk_i) begin : p_ival
    if (!rst_n) begin
      ival_r     <= 2'd0;
      tu_seen_r  <= 1'b0;
      tu_ivals_r <= 32'd0;
    end else begin
      if (ts_uncertain_o) tu_seen_r <= 1'b1;
      if (qtick_w) begin
        ival_r <= ival_r + 2'd1;
        if (ival_r == 2'd3) begin
          if (tu_seen_r || ts_uncertain_o) tu_ivals_r <= tu_ivals_r + 32'd1;
          tu_seen_r <= 1'b0;   //! start the next interval clean
        end
      end
    end
  end

  assign tu_ivals_o = tu_ivals_r;

  //! the lease-backed asCapable verdict, for the GET_AVB_INFO flags byte
  //! (1722.1-2021 7.4.40.2 flags[0]) and its Table 5.22 push signature
  assign as_capable_o = as_cap_r;

  //! CLKV_STAT: [0] tu now, [1] lease-backed sync claim, [2] no live lease,
  //! [3] inside a discontinuity holdover, [15:4] lease remaining (quarter-
  //! seconds), [16] lease-backed asCapable claim (J3). Read this before
  //! believing a TUCNT of 0.
  assign stat_o = {15'd0, as_cap_r, lease_r, hold_w, no_lease_r, sync_ok_r,
                   ts_uncertain_o};

endmodule

`default_nettype wire

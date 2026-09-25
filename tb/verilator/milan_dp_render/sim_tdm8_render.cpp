// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// sim_tdm8_render - the shipping AX7101 TDM8 render lane, from the dynamic
// AUDIO_MAP command to the DECODED SERIAL OUTPUT (issue #447).
//
// WHY THIS IS ITS OWN BINARY. sim_aclk is the #386 render-law instrument and
// carries its own mutation arm; adding the AECP map face, the CSR diagnostic
// window and a serial decoder to it would enlarge the blast radius of every
// future render-law change for no gain. Same reason the tree already keeps
// sim_aclk separate from sim_nxn.
//
// WHAT IT PROVES, and the one rule that makes it worth anything: NOTHING THE
// DUT PRODUCES IS USED AS AN EXPECTED VALUE.
//
//   * The INJECTION RECORD is built before any traffic is sent. inj[e][s] is
//     the 24-bit word {pdu[11:0], event[3:0], channel[7:0]} of media event
//     ordinal e on stream wire channel s. The AAF feeder transmits FROM that
//     table and never writes back to it.
//   * The ROUTE RECORD is built only from the ADD and REMOVE records this leg
//     issued and the SUCCESS status each returned. GET_AUDIO_MAP and the CSR
//     render-RAM readback are GRADED against it; they do not define it.
//   * The PIN DECODER reads exactly three signals - tdm_bclk_o, tdm_fsync_o
//     and tdm_dout_o - sampled after each half step. It reads no DUT internal,
//     and specifically not the exported frame position or bit-clock enables.
//     A frame counter, an FSYNC toggle and an internal crossbar tap are each
//     insufficient by construction, which is what issue #447 acceptance 5
//     asks for.
//   * Internal taps are TIMESTAMP and COUNTER sources only: the crossbar's
//     valid pulse, the adapter's commit strobe, the serial frame start and
//     adoption instants, and the five lane counters. The m-th post-epoch
//     crossbar pulse is correlated with the m-th decoded frame BY COUNT, never
//     by reading its payload.
//
// THE DECODER'S PHASE: A REAL dsp_a RECEIVER (issue #452). The master launches
// fsync on the bclk FALL, so the pulse is CENTRED on the rise it marks: fsync
// is high across exactly ONE rising edge, with half a bit period of setup and
// of hold, and nothing on the bus moves at a rise. This decoder is therefore
// the McASP one at RDATDLY = 1 - sample fsync on the rise, take slot 0's MSB
// on the rise that FOLLOWS the one where fsync read high, with the TRIGGER
// EDGE EXCLUDED FROM THE COUNTDOWN - which is the same rule the in-tree
// external codec model of this bus presents to the capture direction. Before
// #452 fsync changed ON the rising edge, so this decoder counted TWO rises
// from a transition it read early; the framing instant it produces is the same
// rise either way, and what changed is that the reading is no longer a
// function of which pin arrives first. tb/verilator/tdm_render's golden
// de-serializer models a SLAVE bus and is deliberately NOT reused here; both
// it and KL_tdm_render stay untouched and green on their own bench.
//
// WHAT THE FRAMING COUNTER CAN AND CANNOT SEE. The decoder's free-running
// position advances from BCLK alone. A mutation that shifts DOUT by one bit
// while leaving BCLK and FSYNC alone therefore leaves every framing value
// unchanged: it is graded by the full 24-bit word identity and the 8-bit pad
// check, not by the cadence counter. The cadence counter is kept for the
// clock/frame faults it really does observe (a frame that is not 256 bclks,
// or a decoder that resynchronises against its own count).
//
// WHAT IT DOES NOT CLAIM. This is a digital, zero-delay model. It does not
// establish electrical margin at the pins, and the counter-crossing arm below
// does not claim to demonstrate metastability: the CDC discrimination is done
// by the mutation arm's explicitly modelled bit-arrival skew, whose limits are
// stated there. Physical acceptance stays with #386 acceptance 4 and #117.
//
// THE AXIS RATE HERE IS A MODEL RATE. This leg runs axis_clk at 100 MHz, with
// clk_audio_i = clk_tdm_i = axis_clk x 391/1591 = 24.575739 MHz - the
// SHIPPING audio clock's absolute frequency, so every serial term below (the
// 81.4 ns bit period, the 20.834 us frame, the fsync rate) is the shipping
// one. The shipping AX7101 image clocks axis_clk at 50 MHz (`--milan-clk-freq
// 50e6`, docs/litex/CLOCK_DOMAINS.md `milan`), so a term MEASURED IN AXIS
// CYCLES is twice as long in nanoseconds there as it is here. Axis-cycle
// measurements are therefore printed as cycles first and converted at BOTH
// rates, and docs/design/TIME_SYNC.md publishes the shipping conversion.
//
// THE CLOCK SOURCE. The serial window above runs at INTERNAL, where the
// packet grid and the physical frame grid free-run apart by the divider
// plan's -10.64 ppm. The [CRF] phase selects this shape's CRF CLOCK_SOURCE
// through the REAL command path - a SET_CLOCK_SOURCE on CLOCK_DOMAIN 0 over
// the same AECP face the map commands use - with the AAF stream STILL
// RUNNING, feeds a real CRF stream into the provisioned sink, and grades the
// same pins again once KL_media_grid_align holds the packet grid on the
// physical one. Two claims separate the aligned state from the free-running
// one, and both are the construction contract's own: the lane's skip and
// underrun counters stay at ZERO across the aligned window (at INTERNAL the
// surplus is one counted skip per beat period), and the commit-to-pin
// interval stops sweeping a whole frame. The transition is then made the
// other way, back to INTERNAL, under the same running stream.
//
// WHAT THE MULTI-STREAM BUILD ADDS (-DTDM8R_MULTI_TB). The shipping shape
// carries one listener, so two properties are unobservable on it: the render
// epoch's bind-fall mask is STREAM QUALIFIED, and a legal cluster key with no
// physical projection does not exist. gen_tdm8r_multi_shape.py writes a
// second end-station config (a second listener; the wire-truth cluster
// policy, which makes that listener's clusters honestly virtual) and the same
// builder derives its shape header and entity image. The [MULTI] phase binds
// both listeners and grades the two halves of the qualification against each
// other at the pins.
//
// Modes: no argument runs every phase. --serial-only, --epoch-only and
// --crf-only are the short legs tdm8_render_mutants.py runs, and
// --defect-stopped-clock, --defect-one-sample and --defect-internal-select
// are its three leg-side defect arms. The multi-stream build takes no mode:
// its one phase IS its leg.

#include "../../common/verilator_harness.hpp"
#include "Vmilan_datapath.h"
#include "Vmilan_datapath___024root.h"
#include "verilated.h"

#include <array>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <string>
#include <vector>

namespace {

//! AXI4-Lite handshake guard: cycles a single beat may wait before the BFM
//! gives up rather than hanging the leg.
constexpr int kAxiGuardCycles = 2048;
//! the shipping listener stream: 8 wire channels, 6 events per class-A PDU
constexpr int kChans = 8;
constexpr int kEvents = 6;
constexpr size_t kPayloadBytes = static_cast<size_t>(kChans) * kEvents * 4;
constexpr size_t kFrameBytes = 14 + 24 + kPayloadBytes;
//! six events per PDU at 48 kHz on the 100 MHz MODEL axis clock (the shipping
//! image's axis clock is 50 MHz; see THE AXIS RATE HERE IS A MODEL RATE). On
//! the PHYSICAL grid - the cadence a talker disciplined to the same CRF
//! produces - the fsync period is 512 x 1591/391 cycles, so six of them are
//! 12 500 + 52/391.
constexpr long kPduPeriodCycles = 12500;
constexpr long kPduPhysFracNum = 52;
constexpr long kPduPhysFracDen = 391;
//! the CRF cadence: 96 samples per PDU at 48 kHz is 2 ms, and 2 ms of the
//! 100 MHz axis clock is 200 000 cycles
constexpr long kCrfPduPeriodCycles = 200000;
//! the MODEL axis clock, and the one the shipping AX7101 image runs. Every
//! interval this leg measures in axis cycles is published in cycles and
//! converted at both: ns = cycles x 1e9 / rate.
constexpr double kModelAxisHz = 100e6;
constexpr double kShipAxisHz = 50e6;
constexpr double kModelNsPerAxis = 1e9 / kModelAxisHz;
constexpr double kShipNsPerAxis = 1e9 / kShipAxisHz;
//! one media tick on the packet grid, in axis cycles (100 MHz / 48 kHz)
constexpr double kTickCycles = kModelAxisHz / 48000.0;
//! #386's render setpoint as milan_datapath derives it: one class-A PDU of
//! events plus the two-tick allowance. Stated here as the LAW under test,
//! never read back from the DUT.
constexpr int kRenderSetpointEvt = kEvents + 2;
//! THE PRESERVED PREFILL SNAP, as a derivation rather than a search. The
//! render stage holds every pop until a PDU END finds its queue at or above
//! TARGET = setpoint + one PDU of events, then snaps the read pointer to
//! wptr - TARGET and DROPS the oldest excess. This leg pushes kEvents per
//! PDU, so the first PDU end at or above the target is the third (18 events
//! pushed, 14 kept) and the first event the lane may ever render is ordinal
//! 18 - 14 = 4. Stated here as the LAW under test: a stage that discarded a
//! different count would leave a different ordinal at the head, and T6
//! PREFILL asserts the equality rather than searching for whatever came out.
constexpr int kPrefillTargetEvt = kRenderSetpointEvt + kEvents;
constexpr long kPrefillPdus =
    (kPrefillTargetEvt + kEvents - 1) / kEvents;
constexpr long kFirstEligibleEvent =
    kPrefillPdus * kEvents - kPrefillTargetEvt;
//! registration slack on the band's upper edge: the accept pulse and the pop
//! pulse are each one register behind their events
constexpr long kBandSlackCycles = 64;
//! this shape's CRF CLOCK_SOURCE index. Not trusted: the SET_CLOCK_SOURCE
//! below is graded SUCCESS and the media plane's own registered resolve is
//! then required to read CRF, so a wrong index fails rather than passes.
constexpr uint16_t kCrfClksrcIx = 1;
//! the exact fractional-N product clock plan: clk_audio_i = clk_tdm_i =
//! axis_clk x 391/1591 = 24,575,738.5292 Hz, BCLK_HALF_P = 1
constexpr long kAudNum = 391;
constexpr long kAudDen = 1591;
//! the serial frame: 8 slots x 32 bit clocks
constexpr int kSlots = 8;
constexpr int kSlotBits = 32;
constexpr int kFrameBclks = kSlots * kSlotBits;
//! the crossbar's TDM key lane (milan_datapath CHMAP_RPHYS_TDM_BASE_C / _N_C).
//! Stated here as the LAW under test, never read back from the DUT.
constexpr int kTdmBase = 2;
constexpr int kI2sBase = 0;
constexpr int kI2sN = 2;
//! the permutation the map programs: no fixed point, so an identity
//! projection cannot pass by accident
constexpr std::array<int, kSlots> kPerm = {3, 5, 0, 7, 2, 6, 1, 4};
//! the MULTI-STREAM shape's key geometry, stated as the LAW under test rather
//! than read back from the DUT: STREAM_PORT_INPUT 1's cluster block starts
//! where port 0's ends, and the model declares sixteen keys in all.
constexpr int kMultiPort1Base = 8;
constexpr int kMultiInKeys = 16;
//! which shape THIS build elaborated. A constant rather than a preprocessor
//! branch around the phases, so BOTH sets stay compiled and a change that
//! breaks the one this build does not run is still caught here.
#ifdef TDM8R_MULTI_TB
constexpr bool kMultiShape = true;
#else
constexpr bool kMultiShape = false;
#endif
//! ...and the generated entity image that shape's AECP face serves, named by
//! the Makefile target that produces it, so a missing image prints the
//! command that makes it.
constexpr const char* kAemImage =
    kMultiShape ? "tdm8rm_aemi.bin" : "tdm8r_aemi.bin";

//! One classification-table entry's stream id, whatever width the tap has:
//! Verilator presents a ONE-entry table as a 64-bit scalar and a wider one as
//! an array of 32-bit words, and this leg elaborates both shapes.
inline uint64_t sid_of_entry(uint64_t flat, int s) {
    return (s == 0) ? flat : 0;
}
template <typename T>
inline uint64_t sid_of_entry(const T& flat, int s) {
    return (static_cast<uint64_t>(flat[2 * s + 1]) << 32) | flat[2 * s];
}
//! how far the grading cursor may advance over one decoded frame before the
//! frame is a failure rather than a counted skip
constexpr int kMaxAdvance = 4;
//! the serial geometry in AXIS cycles on the shipping 391/1591 plan, stated
//! once: one bit period, one whole frame, and the frame CDC's own registered
//! depth (the floor no commit closer than that can have met - see
//! measure_the_commit_to_pin_terms).
constexpr double kAxisPerHalf = 0.5;
constexpr double kBitAxis =
    2.0 * static_cast<double>(kAudDen) / static_cast<double>(kAudNum);
constexpr double kFrameAxis =
    512.0 * static_cast<double>(kAudDen) / static_cast<double>(kAudNum);
constexpr double kCdcFloorAxis =
    6.0 * static_cast<double>(kAudDen) / static_cast<double>(kAudNum);

//! One decoded serial frame: the eight 32-bit slot words, exactly as the pins
//! delivered them, and the harness time of slot 0's MSB sampling edge.
struct DecodedFrame {
    std::array<uint32_t, kSlots> slot{};
    long half_step = 0;                 //! of slot 0's MSB sampling edge
    std::array<long, kSlots> msb_half{};//! ...and of every slot's MSB edge
    uint64_t frames_at = 0;             //! lane counters at publication
    uint64_t unders_at = 0;
    uint64_t skips_at = 0;
};

class TdmRenderHarness {
 public:
    int run(int argc, char** argv);

 private:
    Vmilan_datapath* dut = nullptr;
    milan::tb::Checker check{"tdm8_render"};

    bool serial_only = false;
    bool epoch_only = false;
    bool crf_only = false;
    bool defect_stopped_clock = false;
    bool defect_one_sample = false;
    //! the [CRF] phase's own defect arm: the command path is exercised in
    //! full, but it NAMES INTERNAL. Everything else about the phase is
    //! unchanged - the CRF stream is still fed, the sink still locks - so
    //! what fails is exactly the set of claims that depend on the SELECTION
    //! having happened, which is what makes those claims evidence.
    bool defect_internal_select = false;

    // ---------------------------------------------------------------- //
    //  The fractional-N product clock, and the freeze this leg needs    //
    // ---------------------------------------------------------------- //
    long acc = 0;
    int  aud = 0;
    long axis_cycle = 0;
    long half_step = 0;
    bool tdm_frozen = false;            //! hold clk_tdm_i static

    void half() {
        if (!tdm_frozen) {
            acc += kAudNum;
            if (acc >= kAudDen) { acc -= kAudDen; aud ^= 1; }
        }
        dut->clk_audio_i = aud;
        dut->clk_tdm_i   = aud;
        ++half_step;
    }

    //! The two memory models are driven and advanced in the LOW phase, the
    //! ordering every other milan_dp leg uses: the model presents its inputs,
    //! the low eval settles, and only then does it read the DUT's registered
    //! valid/ready back. Advancing them on the rising edge instead reads the
    //! outputs the DUT is registering at that very edge, and a valid/ready
    //! handshake graded half a cycle out deadlocks the descriptor burst - the
    //! store then never validates the image and every map command comes back
    //! NO_SUCH_DESCRIPTOR, which looks exactly like a broken responder.
    void lo() {
        dut->axis_clk = 0; dut->gtx_clk = 0;
        desc_drive(); resp_drive();
        half(); dut->eval();
        desc_edge(); resp_edge();
        observe();
    }
    void hi() {
        dut->axis_clk = 1; dut->gtx_clk = 1;
        half(); dut->eval();
        ++axis_cycle;
        observe_axis();
        observe();
        sniff_probe();
        drp_respond();
    }

    //! The minimal DRP responder the media-clock servo needs once CRF is
    //! selected: DRDY a few cycles after DEN, data 0. With auto_repair off a
    //! VERIFY mismatch is informative-only and the servo proceeds, which is
    //! all this leg needs of it - the MMCM's real ClkReg contents are
    //! tb/verilator/mmcm_servo's subject, not this one's.
    int drp_lat = 0;
    void drp_respond() {
        dut->i_mmcm_drp_rdy = 0;
        if (drp_lat > 0 && --drp_lat == 0) dut->i_mmcm_drp_rdy = 1;
        if (dut->o_mmcm_drp_en) drp_lat = 3;
        dut->i_mmcm_drp_do = 0;
    }

    // ---------------------------------------------------------------- //
    //  The two processor memory faces. The AECP uCPU serves the entity  //
    //  model from main memory and lays its responses out in a second    //
    //  region; both are ordered models with no DDR timing claim. The    //
    //  descriptor image is the one the BUILD ships, generated from this //
    //  config by the same two tools sw/litex loads at PP_DESC_BASE_P,   //
    //  so the map face this leg drives is the one a board would serve.  //
    // ---------------------------------------------------------------- //
    static constexpr uint32_t kDescBase = 0x20000000u;
    static constexpr uint32_t kRespBase = 0x20100000u;
    std::vector<uint8_t> desc_img;
    long desc_requests = 0;             //! bursts the AECP store asked for
    bool desc_busy = false;
    uint32_t desc_addr = 0;
    unsigned desc_left = 0;
    unsigned desc_wait = 0;
    std::array<uint8_t, 592> resp_mem{};
    bool mem_busy = false;
    uint32_t mem_addr = 0;
    unsigned mem_left = 0;
    bool mem_done = false;

    void desc_drive() {
        uint64_t data = 0;
        for (unsigned i = 0; i < 8; ++i) {
            const size_t off = static_cast<size_t>(desc_addr - kDescBase) + i;
            data = (data << 8) | (off < desc_img.size() ? desc_img[off] : 0);
        }
        dut->i_desc_mem_req_ready = !desc_busy;
        dut->i_desc_mem_rsp_valid = desc_busy && desc_wait == 0;
        dut->i_desc_mem_rsp_data = data;
        dut->i_desc_mem_rsp_last = desc_busy && desc_left == 1;
        dut->i_desc_mem_rsp_err = 0;
    }
    void desc_edge() {
        if (!desc_busy && dut->o_desc_mem_req_valid) {
            ++desc_requests;
            desc_addr = dut->o_desc_mem_req_addr;
            desc_left = dut->o_desc_mem_req_beats;
            desc_busy = desc_left != 0;
            desc_wait = 12;
        } else if (desc_busy && desc_wait) {
            --desc_wait;
        } else if (desc_busy && dut->o_desc_mem_rsp_ready) {
            desc_addr += 8;
            if (--desc_left == 0) desc_busy = false;
        }
    }
    void resp_drive() {
        uint64_t data = 0;
        for (unsigned i = 0; i < 8; ++i) {
            const size_t off = static_cast<size_t>(mem_addr - kRespBase) + i;
            data = (data << 8) | (off < resp_mem.size() ? resp_mem[off] : 0);
        }
        dut->i_resp_mem_req_ready = !mem_busy;
        dut->i_resp_mem_rsp_valid = mem_busy;
        dut->i_resp_mem_rsp_data = data;
        dut->i_resp_mem_rsp_last = mem_busy && mem_left == 1;
        dut->i_resp_mem_rsp_err = 0;
        dut->i_resp_mem_wr_ready = !mem_done;
        dut->i_resp_mem_wr_done = mem_done;
        dut->i_resp_mem_wr_err = 0;
    }
    void resp_edge() {
        if (mem_busy && dut->o_resp_mem_rsp_ready) {
            mem_addr += 8;
            if (--mem_left == 0) mem_busy = false;
        } else if (!mem_busy && dut->o_resp_mem_req_valid) {
            mem_addr = dut->o_resp_mem_req_addr;
            mem_left = dut->o_resp_mem_req_beats;
            mem_busy = mem_left != 0;
        }
        if (mem_done) {
            mem_done = false;
        } else if (dut->o_resp_mem_wr_valid) {
            for (unsigned i = 0; i < 8; ++i) {
                const size_t off =
                    static_cast<size_t>(dut->o_resp_mem_wr_addr - kRespBase) + i;
                if (off < resp_mem.size() && (dut->o_resp_mem_wr_strb & (1u << i)))
                    resp_mem[off] =
                        static_cast<uint8_t>(dut->o_resp_mem_wr_data >> (56 - 8 * i));
            }
            mem_done = true;
        }
    }
    bool load_descriptor_image(const char* path);
    void step() { lo(); hi(); }
    void steps(long n) { while (n--) step(); }

    // ---------------------------------------------------------------- //
    //  THE PIN DECODER. Three pins, nothing else.                      //
    // ---------------------------------------------------------------- //
    int  p_bclk = 0;
    int  p_fsync = 0;
    bool armed = false;
    int  pend = 0;
    bool framed = false;
    int  q = 0;                          //! free-running bit position
    long rises = 0;                      //! bclk rises since reset release
    long rises_at_last_fsync = -1;
    long rises_at_first_fsync = -1;      //! ...of the FIRST one, so the gap
                                         //! between a re-arm and the boundary
                                         //! that ends the invalid interval is
                                         //! a pin observation
    long fsync_rises = 0;
    std::array<uint32_t, kSlots> word{};
    std::array<long, kSlots> msb_half{};
    long frame_msb_half = 0;
    std::vector<DecodedFrame> decoded;
    long framing_faults = 0;             //! q != 0 at a one-rise expiry
    long gap_faults = 0;                 //! fsync-to-fsync != 256 bclk rises
    bool collect = false;                //! publish frames into `decoded`

    void observe() {
        const int b = dut->tdm_bclk_o;
        const int f = dut->tdm_fsync_o;
        const int d = dut->tdm_dout_o;
        if (!(b && !p_bclk)) { p_bclk = b; return; }
        p_bclk = b;
        ++rises;
        observe_late(f, d);
        // THE COUNTDOWN EXCLUDES ITS OWN TRIGGER EDGE. fsync is high across
        // exactly one rise and slot 0's MSB is on the NEXT one, so the delay
        // is set on the rise that reads fsync high and expires on the rise
        // after it - decrementing on the trigger edge itself would put the
        // first decoded MSB one rise early, which this bus does not deliver.
        if (f && !p_fsync && armed) {
            if (rises_at_last_fsync >= 0 && rises - rises_at_last_fsync != kFrameBclks)
                ++gap_faults;
            rises_at_last_fsync = rises;
            if (fsync_rises == 0) rises_at_first_fsync = rises;
            ++fsync_rises;
            pend = 1;
        } else if (pend > 0 && --pend == 0) {
            if (framed && q != 0) ++framing_faults;
            q = 0;
            framed = true;
        }
        if (!f) armed = true;
        p_fsync = f;
        if (!framed) return;
        const int slot = q / kSlotBits;
        const int bit = q % kSlotBits;
        if (bit == 0) msb_half[static_cast<size_t>(slot)] = half_step;
        if (slot == 0 && bit == 0) frame_msb_half = half_step;
        word[static_cast<size_t>(slot)] =
            (word[static_cast<size_t>(slot)] << 1) | static_cast<uint32_t>(d);
        if (slot == kSlots - 1 && bit == kSlotBits - 1 && collect) {
            DecodedFrame fr;
            fr.slot = word;
            fr.msb_half = msb_half;
            fr.half_step = frame_msb_half;
            fr.frames_at = lane_frames();
            fr.unders_at = lane_unders();
            fr.skips_at = lane_skips();
            decoded.push_back(fr);
        }
        if (++q == kFrameBclks) q = 0;
    }

    // ---------------------------------------------------------------- //
    //  THE NEGATIVE-CONTROL DECODER (issue #452). The SAME three pins,  //
    //  one difference: it attributes the pulse to the rise where fsync  //
    //  reads LOW again rather than to the one where it reads HIGH. On   //
    //  the OLD bus, whose fsync changed ON the rising edge, that was    //
    //  one of the two readings an unconstrained pin skew could hand a   //
    //  receiver - and it was the RIGHT one. On a bus that launches      //
    //  fsync on the fall it is one rise late, so every word it recovers //
    //  is the injected one shifted up one place and it reproduces no    //
    //  media event at all. Put the RTL edge back on the rise and this   //
    //  decoder becomes the correct one, which is how its two checks     //
    //  below discriminate between the two buses instead of passing on   //
    //  either.                                                          //
    // ---------------------------------------------------------------- //
    int  late_p_fsync = 0;
    bool late_armed = false;
    int  late_pend = 0;
    bool late_framed = false;
    int  late_q = 0;
    std::array<uint32_t, kSlots> late_word{};
    std::vector<std::array<uint32_t, kSlots>> late_frames;

    void observe_late(int f, int d) {
        if (!f && late_p_fsync && late_armed) {
            late_pend = 1;
        } else if (late_pend > 0 && --late_pend == 0) {
            late_q = 0;
            late_framed = true;
        }
        if (f) late_armed = true;        //! a pulse must be SEEN before its fall
        late_p_fsync = f;
        if (!late_framed) return;
        const size_t slot = static_cast<size_t>(late_q / kSlotBits);
        late_word[slot] = (late_word[slot] << 1) | static_cast<uint32_t>(d);
        if (late_q == kFrameBclks - 1 && collect) late_frames.push_back(late_word);
        if (++late_q == kFrameBclks) late_q = 0;
    }

    void decoder_reset() {
        armed = false; pend = 0; framed = false; q = 0;
        rises = 0; rises_at_last_fsync = -1; rises_at_first_fsync = -1;
        fsync_rises = 0;
        framing_faults = 0; gap_faults = 0;
        word.fill(0); msb_half.fill(0);
        decoded.clear();
        late_armed = false; late_pend = 0; late_framed = false; late_q = 0;
        late_word.fill(0); late_frames.clear();
        p_bclk = dut->tdm_bclk_o;
        p_fsync = dut->tdm_fsync_o;
        late_p_fsync = dut->tdm_fsync_o;
    }

    // ---------------------------------------------------------------- //
    //  Internal taps: timestamps and counters ONLY                     //
    // ---------------------------------------------------------------- //
    uint64_t lane_frames() const { return dut->rootp->milan_datapath__DOT__tdmr_frames_w; }
    uint64_t lane_unders() const { return dut->rootp->milan_datapath__DOT__tdmr_underruns_w; }
    uint64_t lane_skips()  const { return dut->rootp->milan_datapath__DOT__tdmr_skips_w; }
    uint64_t lane_over()   const { return dut->rootp->milan_datapath__DOT__tdmr_overruns_w; }
    uint64_t lane_epochs() const { return dut->rootp->milan_datapath__DOT__tdmr_epochs_w; }
    //! the classification table's stream id for entry `s`
    uint64_t table_sid(int s) const {
        return sid_of_entry(dut->rootp->milan_datapath__DOT__strtbl_sid_w, s);
    }

    std::vector<long> phys_valid_cycle;  //! axis cycle of each crossbar pulse
    std::vector<long> commit_cycle;      //! axis cycle of each frame commit
    long adopt_events = 0;
    int  adopt_prev = 0;
    //! T28's counter-sanity record: every sampled frames_o, against the pin
    //! decoder's own count of observed frame boundaries. The baseline is taken
    //! when the decoder re-arms, so the two are counting the same interval.
    uint64_t frames_seen_max = 0;
    uint64_t frames_base = 0;
    long counter_regressions = 0;
    long counter_impossible = 0;
    long counter_worst_lead = 0;

    // ---------------------------------------------------------------- //
    //  THE #386 LAW INSTRUMENT, the one sim_aclk uses, kept here so the  //
    //  setpoint law is observed in the SAME run that decodes the pins.   //
    //  Records are kept by the PDU's own 12-bit wire id; the accept      //
    //  pulse carries no id, so accepts are matched to injections in      //
    //  order, which the depacketizer keeps and this leg never breaks.    //
    // ---------------------------------------------------------------- //
    static constexpr size_t kIdSpace = 4096;
    std::vector<int> sent_ids;              //! wire ids, in injection order
    size_t accepts_seen = 0;
    std::array<long, kIdSpace> accept_at{}; //! axis cycle of the accept pulse
    std::array<int, kIdSpace> fill_at{};    //! the stage's fill at that instant
    std::array<long, kIdSpace> pop_at{};    //! ...and of its event 0's pop
    long recentre_pulses = 0;               //! render_recentre_p_w edges
    long src_recentre_pulses = 0;           //! the clock-source trigger's own
    //! ...and, for the multi-stream arm, the two per-stream observations that
    //! stop "the second stream is live" from being an assumption: how many
    //! PDUs the monitor ACCEPTED for each stream, and how many events the
    //! render stage POPPED for each.
    std::array<long, 2> accepts_by_stream{};
    std::array<long, 2> pops_by_stream{};

    void law_reset() {
        sent_ids.clear();
        accepts_seen = 0;
        accept_at.fill(-1);
        fill_at.fill(-1);
        pop_at.fill(-1);
    }

    void observe_law() {
        if (dut->rootp->milan_datapath__DOT__avtprx_accept_p) {
            const size_t s = static_cast<size_t>(
                dut->rootp->milan_datapath__DOT__avtprx_idx) & 1u;
            ++accepts_by_stream[s];
        }
        for (size_t s = 0; s < pops_by_stream.size(); s++)
            if ((dut->rootp->milan_datapath__DOT__rsp_pop_p_w >> s) & 1)
                ++pops_by_stream[s];
        if (dut->rootp->milan_datapath__DOT__avtprx_accept_p &&
            accepts_seen < sent_ids.size()) {
            const size_t id = static_cast<size_t>(sent_ids[accepts_seen++]);
            accept_at[id] = axis_cycle;
            fill_at[id] =
                static_cast<int>(dut->rootp->milan_datapath__DOT__rsp_fill_w & 0xFF);
        }
        if (dut->rootp->milan_datapath__DOT__rsp_pop_p_w & 1) {
            const uint64_t d = dut->rootp->milan_datapath__DOT__rsp_tdata_w;
            const uint32_t s0 = (static_cast<uint32_t>(d & 0xFF) << 16) |
                                (static_cast<uint32_t>((d >> 8) & 0xFF) << 8) |
                                static_cast<uint32_t>((d >> 16) & 0xFF);
            const size_t id = (s0 >> 12) & 0xFFF;
            if (((s0 >> 8) & 0xF) == 0 && pop_at[id] < 0)
                pop_at[id] = axis_cycle;
        }
        if (dut->rootp->milan_datapath__DOT__render_recentre_p_w) ++recentre_pulses;
        if (dut->rootp->milan_datapath__DOT__src_recentre_p_r) ++src_recentre_pulses;
    }

    void observe_axis() {
        observe_law();
        observe_epoch();
        observe_commit_watch();
        if (dut->rootp->milan_datapath__DOT__chmap_phys_v_w)
            phys_valid_cycle.push_back(axis_cycle);
        if (dut->rootp->milan_datapath__DOT__tdmr_commit_p_w)
            commit_cycle.push_back(axis_cycle);
        const int a = dut->rootp->milan_datapath__DOT__tdmr_adopt_p_w;
        if (a && !adopt_prev) ++adopt_events;
        adopt_prev = a;
        const uint64_t fr = lane_frames();
        if (fr < frames_seen_max) ++counter_regressions;
        else frames_seen_max = fr;
        // The counter increments at frame starts; the decoder counts fsync
        // rises, one bit period apart, so over the SAME interval the two can
        // differ only by a frame plus the crossing's own registration. A
        // sampled value ahead of what the pins can justify is a value the
        // counter never held - the discrimination the gray crossing exists
        // for, read without trusting the counter to grade itself.
        const long lead = static_cast<long>(fr - frames_base) - fsync_rises;
        if (lead > counter_worst_lead) counter_worst_lead = lead;
        if (lead > 3) ++counter_impossible;
    }

    //! The stream-qualified epoch's two observations, accumulated every cycle
    //! rather than sampled: which streams the bind table actually dropped, and
    //! whether the adapter's commit gate EVER fell. A "the lane kept running"
    //! verdict read from one end-of-window sample would miss a gate that
    //! closed and reopened inside it.
    uint32_t bind_falls_seen = 0;
    long commit_gate_closed_cycles = 0;

    void observe_epoch() {
        bind_falls_seen |= static_cast<uint32_t>(
            dut->rootp->milan_datapath__DOT__strtbl_bind_fall_w);
        if (!dut->rootp->milan_datapath__DOT__tdmr_commit_en_w)
            ++commit_gate_closed_cycles;
    }

    void epoch_watch_reset() {
        bind_falls_seen = 0;
        commit_gate_closed_cycles = 0;
    }

    //! T21's window, watched PER CYCLE rather than sampled by a step loop:
    //! from the instant it is armed until the lane's epoch counter moves,
    //! every frame commit strobe is counted. The window closes on the epoch
    //! COUNTER, which is the same clk_i view of the reopening the producer
    //! itself gets (the counter and the acknowledgement cross with the same
    //! latency), so "before the epoch reopened" means the same thing to this
    //! observer and to the gateware.
    //!
    //! The crossbar's own pulses are counted beside them, because "no commit
    //! was made" means nothing in a window where the adapter was never asked
    //! to make one: the window has to contain WORK.
    bool commit_watch_armed = false;
    bool commit_watch_closed = false;
    uint64_t commit_watch_base = 0;
    long commits_before_reopen = 0;
    long phys_offers_in_window = 0;

    void arm_the_commit_watch() {
        commit_watch_armed = true;
        commit_watch_closed = false;
        commit_watch_base = lane_epochs();
        commits_before_reopen = 0;
        phys_offers_in_window = 0;
    }

    void observe_commit_watch() {
        if (!commit_watch_armed) return;
        if (lane_epochs() != commit_watch_base) {
            commit_watch_armed = false;
            commit_watch_closed = true;
            return;
        }
        if (dut->rootp->milan_datapath__DOT__chmap_phys_v_w)
            ++phys_offers_in_window;
        if (dut->rootp->milan_datapath__DOT__tdmr_commit_p_w)
            ++commits_before_reopen;
    }

    void taps_reset() {
        phys_valid_cycle.clear();
        commit_cycle.clear();
        adopt_events = 0;
        frames_seen_max = lane_frames();
        frames_base = lane_frames();
        counter_regressions = 0;
        counter_impossible = 0;
        counter_worst_lead = 0;
    }

    // ---------------------------------------------------------------- //
    //  AXI4-Lite BFM                                                   //
    // ---------------------------------------------------------------- //
    void axi_write(uint16_t a, uint32_t d) {
        dut->s_axi_awaddr = a; dut->s_axi_awvalid = 1;
        dut->s_axi_wdata = d;  dut->s_axi_wstrb = 0xF; dut->s_axi_wvalid = 1;
        dut->s_axi_bready = 1;
        for (int g = 0; g < kAxiGuardCycles; g++) {
            lo(); const bool acc_w = dut->s_axi_awready && dut->s_axi_wready; hi();
            if (acc_w) break;
        }
        dut->s_axi_awvalid = 0; dut->s_axi_wvalid = 0;
        for (int g = 0; g < kAxiGuardCycles; g++) {
            lo(); const bool bv = dut->s_axi_bvalid; hi(); if (bv) break;
        }
        dut->s_axi_bready = 0;
    }
    uint32_t axi_read(uint16_t a) {
        dut->s_axi_araddr = a; dut->s_axi_arvalid = 1; dut->s_axi_rready = 1;
        for (int g = 0; g < kAxiGuardCycles; g++) {
            lo(); const bool ar = dut->s_axi_arready; hi(); if (ar) break;
        }
        dut->s_axi_arvalid = 0;
        uint32_t d = 0;
        for (int g = 0; g < kAxiGuardCycles; g++) {
            lo(); const bool rv = dut->s_axi_rvalid; if (rv) d = dut->s_axi_rdata; hi();
            if (rv) break;
        }
        dut->s_axi_rready = 0;
        return d;
    }

    // ---------------------------------------------------------------- //
    //  MAC ingress                                                     //
    // ---------------------------------------------------------------- //
    void inject(const uint8_t* f, size_t len) {
        std::vector<uint64_t> beats;
        for (size_t bt = 0; bt < (len + 7) / 8; bt++) {
            uint64_t v = 0;
            for (int j = 0; j < 8; j++)
                if (bt * 8 + j < len)
                    v |= static_cast<uint64_t>(f[bt * 8 + j]) << (8 * j);
            beats.push_back(v);
        }
        size_t idx = 0;
        for (int c = 0; c < 1500 && idx < beats.size() + 8; c++) {
            if (idx < beats.size()) {
                dut->s_axis_mac_rx_tdata  = beats[idx];
                dut->s_axis_mac_rx_tkeep  = 0xFF;
                dut->s_axis_mac_rx_tvalid = 1;
                dut->s_axis_mac_rx_tlast  = (idx == beats.size() - 1);
            } else {
                dut->s_axis_mac_rx_tvalid = 0; dut->s_axis_mac_rx_tlast = 0;
            }
            lo();
            const bool in_acc = dut->s_axis_mac_rx_tvalid && dut->s_axis_mac_rx_tready;
            hi();
            if (in_acc || idx >= beats.size()) idx++;
        }
        dut->s_axis_mac_rx_tvalid = 0; dut->s_axis_mac_rx_tlast = 0;
    }

    // ---------------------------------------------------------------- //
    //  THE IMMUTABLE INJECTION RECORD                                  //
    // ---------------------------------------------------------------- //
    //! inj[e][s]: the 24-bit word of media event ordinal e on wire channel s.
    //! Built before any traffic and never written again.
    std::vector<std::array<uint32_t, kChans>> inj;
    long injected_events = 0;            //! how many ordinals have been sent

    void build_injection_record(long pdus) {
        inj.clear();
        inj.reserve(static_cast<size_t>(pdus) * kEvents);
        for (long p = 0; p < pdus; p++)
            for (int k = 0; k < kEvents; k++) {
                std::array<uint32_t, kChans> ev{};
                for (int c = 0; c < kChans; c++)
                    ev[static_cast<size_t>(c)] =
                        (static_cast<uint32_t>(p & 0xFFF) << 12) |
                        (static_cast<uint32_t>(k & 0xF) << 8) |
                        static_cast<uint32_t>(c & 0xFF);
                inj.push_back(ev);
            }
        injected_events = 0;
        law_reset();
    }

    bool feed_on = false;
    long next_pdu_at = 0;
    uint8_t wire_seq = 0;
    long pdu_cursor = 0;
    //! the SECOND stream, on the multi-stream shape only: its own cadence,
    //! its own wire sequence and its own event cursor
    bool feed1_on = false;
    long next_pdu1_at = 0;
    uint8_t wire_seq1 = 0;
    long injected1_events = 0;

    //! stream 1's sample word. The same {pdu, event} identity as stream 0's,
    //! with the channel field marked 0x80 | c - a value NO stream-0 sample
    //! can hold, because the record's channel field is 0..7. That is what
    //! makes "this slot is fed from stream 1" readable at the pins without a
    //! second ordinal oracle.
    static uint32_t stream1_word(long event, int chan) {
        return (static_cast<uint32_t>((event / kEvents) & 0xFFF) << 12) |
               (static_cast<uint32_t>(event % kEvents) << 8) |
               (0x80u | static_cast<uint32_t>(chan & 0x7F));
    }

    void send_pdu(int stream = 0) {
        uint8_t f[kFrameBytes]; memset(f, 0, sizeof f);
        memcpy(f, kStreamDmac[stream], 6);
        const uint8_t src[6] = {
            0x02, 0x00, 0x00, 0x00, 0x00, 0x02};
        memcpy(f + 6, src, 6);
        f[12] = 0x22; f[13] = 0xF0;
        f[14] = 0x02;                               // AAF
        f[15] = 0x81;                               // sv, tv
        f[16] = (stream == 0) ? wire_seq++ : wire_seq1++;
        memcpy(f + 18, kSid[stream], 8);
        f[26] = 0x00; f[27] = 0x00; f[28] = 0x10; f[29] = 0x00;
        f[30] = 0x02;                               // INT32
        f[31] = static_cast<uint8_t>(0x05 << 4);    // 48 kHz
        f[32] = static_cast<uint8_t>(kChans);
        f[33] = 32;
        f[34] = static_cast<uint8_t>(kPayloadBytes >> 8);
        f[35] = static_cast<uint8_t>(kPayloadBytes & 0xFF);
        const long base = (stream == 0) ? injected_events : injected1_events;
        for (int k = 0; k < kEvents; k++) {
            const size_t e = static_cast<size_t>(base) + static_cast<size_t>(k);
            if (stream == 0 && e >= inj.size()) break;
            for (int c = 0; c < kChans; c++) {
                uint32_t v = (stream == 0)
                           ? inj[e][static_cast<size_t>(c)]
                           : stream1_word(static_cast<long>(e), c);
                // the ONE arm that deliberately puts a different word on the
                // wire than the record holds (N4): the record keeps the
                // intended value, so the identity check is the thing that has
                // to notice
                if (defect_one_sample && c == 3 && e == corrupt_at)
                    v ^= 0x000010u;
                const size_t o = 38 + 4 * (static_cast<size_t>(k) * kChans + c);
                f[o]     = static_cast<uint8_t>(v >> 16);
                f[o + 1] = static_cast<uint8_t>(v >> 8);
                f[o + 2] = static_cast<uint8_t>(v);
                f[o + 3] = 0;
            }
        }
        if (stream == 0) {
            //! the #386 law instrument follows stream 0's accepts in order;
            //! it is read only by the single-stream [CRF] phase
            sent_ids.push_back(
                static_cast<int>(injected_events / kEvents) & 0xFFF);
            injected_events += kEvents;
            ++pdu_cursor;
        } else {
            injected1_events += kEvents;
        }
        inject(f, kFrameBytes);
    }
    long corrupt_at = 1 << 30;

    //! the AAF cadence: an integer period plus a fraction. 0 is the PACKET
    //! grid (the INTERNAL case, where the two grids free-run apart); 52/391 is
    //! the PHYSICAL one, the cadence a talker disciplined to the same CRF
    //! produces and the one the aligned packet grid follows.
    long pdu_frac_num = 0;
    long pdu_frac_acc = 0;
    void advance_pdu_slot() {
        next_pdu_at += kPduPeriodCycles;
        pdu_frac_acc += pdu_frac_num;
        if (pdu_frac_acc >= kPduPhysFracDen) {
            pdu_frac_acc -= kPduPhysFracDen;
            next_pdu_at += 1;
        }
    }

    // ---------------------------------------------------------------- //
    //  THE CRF MEDIA CLOCK INPUT stream, at its 2 ms cadence. Timestamps  //
    //  advance at the NOMINAL 48 kHz rate, so the servo reads the audio   //
    //  clock's honest deviation rather than one this leg invented.        //
    // ---------------------------------------------------------------- //
    bool crf_on = false;
    long crf_next_at = 0;
    uint64_t crf_ts = 1000000000ULL;
    uint8_t crf_wire_seq = 0;

    void send_crf() {
        uint8_t f[64]; memset(f, 0, sizeof f);
        const uint8_t dmac[6] = {
            0x91, 0xE0, 0xF0, 0x00, 0x2A, 0x03};
        memcpy(f, dmac, 6);
        const uint8_t src[6] = {
            0x02, 0x00, 0x00, 0x00, 0x00, 0x02};
        memcpy(f + 6, src, 6);
        f[12] = 0x22; f[13] = 0xF0;
        f[14] = 0x04;                               // CRF subtype
        f[15] = 0x80;                               // sv
        f[16] = crf_wire_seq++;
        f[17] = 0x01;                               // CRF_AUDIO_SAMPLE
        const uint8_t sid[8] = {
            0x02, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00, 0x01};
        memcpy(f + 18, sid, 8);
        f[26] = 0x00; f[27] = 0x00; f[28] = 0xBB; f[29] = 0x80;  // pull0|48000
        f[30] = 0x00; f[31] = 0x08;                 // crf_data_length 8
        f[32] = 0x00; f[33] = 96;                   // timestamp_interval
        for (int i = 0; i < 8; i++)
            f[34 + i] = static_cast<uint8_t>(crf_ts >> (8 * (7 - i)));
        crf_ts += 2000000ULL;
        inject(f, 64);
    }

    void run_fed(long n) {
        const long stop = axis_cycle + n;
        while (axis_cycle < stop) {
            if (crf_on && axis_cycle >= crf_next_at) {
                send_crf();
                crf_next_at += kCrfPduPeriodCycles;
            } else if (feed_on && axis_cycle >= next_pdu_at &&
                       static_cast<size_t>(injected_events) + kEvents <= inj.size()) {
                send_pdu(0);
                advance_pdu_slot();
            } else if (feed1_on && axis_cycle >= next_pdu1_at) {
                send_pdu(1);
                next_pdu1_at += kPduPeriodCycles;
            } else {
                step();
            }
        }
    }

    // ---------------------------------------------------------------- //
    //  THE ROUTE RECORD - issued commands only                         //
    // ---------------------------------------------------------------- //
    //! route[co] = the stream wire channel feeding global cluster key co, and
    //! route_stream[co] = the STREAM INDEX it names; -1 for a cluster with no
    //! mapping. Written only from an ADD/REMOVE this leg issued that returned
    //! SUCCESS. The stream is a separate dimension from the channel because a
    //! mapping carries both, and on a multi-stream shape a lane key may name
    //! a stream whose ordinals the stream-0 injection record does not hold.
    std::array<int, kSlots> route{};
    std::array<int, kSlots> route_stream{};

    void route_reset() { route.fill(-1); route_stream.fill(-1); }
    //! serial slot k is fed by the cluster whose key is k (PBASE 0), so its
    //! source channel is route[k]
    int src_of_slot(int k) const { return route[static_cast<size_t>(k)]; }
    int stream_of_slot(int k) const {
        return route_stream[static_cast<size_t>(k)];
    }

    // ---------------------------------------------------------------- //
    //  AECP command face                                               //
    // ---------------------------------------------------------------- //
    static constexpr uint16_t kCmdGetAudioMap = 43;
    static constexpr uint16_t kCmdAddMappings = 44;
    static constexpr uint16_t kCmdRemoveMappings = 45;
    static constexpr uint16_t kDescStreamPortIn = 0x000E;
    uint16_t aecp_seq = 0x4470;
    //! print the raw answer of a map command that neither succeeded nor
    //! earned the documented BAD_ARGUMENTS refusal, so an unexpected status
    //! is diagnosable from the log alone
    bool trace_map_cmd = true;

    std::vector<uint8_t> aecp_request(uint16_t cmd, uint16_t sq,
                                      const std::vector<uint8_t>& pl) {
        const size_t flen = (38 + pl.size() < 60) ? 60 : 38 + pl.size();
        std::vector<uint8_t> f(flen, 0);
        const uint8_t cmac[6] = {
            0x68, 0x05, 0xCA, 0x95, 0xB2, 0xD1};
        memcpy(f.data() + 6, cmac, 6);
        f[12] = 0x22; f[13] = 0xF0; f[14] = 0xFB; f[15] = 0x00;
        const uint16_t cdl = static_cast<uint16_t>(12 + pl.size());
        f[16] = static_cast<uint8_t>((cdl >> 8) & 0x7);
        f[17] = static_cast<uint8_t>(cdl);
        const uint8_t teid[8] = {
            0x02, 0x00, 0x00, 0xFF, 0xFE, 0x00, 0x00, 0x01};
        memcpy(f.data() + 18, teid, 8);
        const uint8_t ceid[8] = {
            0x68, 0x05, 0xCA, 0xFF, 0xFE, 0x95, 0xB2, 0xD1};
        memcpy(f.data() + 26, ceid, 8);
        f[34] = static_cast<uint8_t>(sq >> 8); f[35] = static_cast<uint8_t>(sq);
        f[36] = static_cast<uint8_t>((cmd >> 8) & 0x7F);
        f[37] = static_cast<uint8_t>(cmd);
        for (size_t i = 0; i < pl.size(); i++) f[38 + i] = pl[i];
        return f;
    }

    std::vector<uint8_t> await_aecp(int cyc = 200000) {
        std::vector<uint8_t> cur, resp;
        dut->m_axis_mac_tx_tready = 1;
        for (int c = 0; c < cyc && resp.empty(); c++) {
            lo();
            if (dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready) {
                for (int l = 0; l < 8; l++)
                    if ((dut->m_axis_mac_tx_tkeep >> l) & 1)
                        cur.push_back(static_cast<uint8_t>(dut->m_axis_mac_tx_tdata >> (8 * l)));
                if (dut->m_axis_mac_tx_tlast) {
                    const bool is_aecp = cur.size() > 37 && cur[12] == 0x22 &&
                                         cur[13] == 0xF0 && cur[14] == 0xFB;
                    const bool solicited = is_aecp && (cur[15] & 0xF) == 1 &&
                                           (cur[36] & 0x80) == 0;
                    if (solicited) resp = cur;
                    cur.clear();
                }
            }
            hi();
        }
        return resp;
    }

    std::vector<uint8_t> aecp_xact(uint16_t cmd, const std::vector<uint8_t>& pl) {
        const std::vector<uint8_t> f = aecp_request(cmd, aecp_seq++, pl);
        inject(f.data(), f.size());
        return await_aecp();
    }

    static long aecp_status(const std::vector<uint8_t>& b) {
        return b.size() > 16 ? (b[16] >> 3) & 0x1F : -1;
    }

    //! One ADD or REMOVE of n {stream_channel, cluster_offset} rows on a
    //! STREAM_PORT_INPUT, each naming `stream`. Returns the AEM status.
    long map_cmd(uint16_t cmd, const std::vector<std::pair<int, int>>& rows,
                 int port = 0, int stream = 0) {
        std::vector<uint8_t> pl = {
            static_cast<uint8_t>(kDescStreamPortIn >> 8),
            static_cast<uint8_t>(kDescStreamPortIn),
            static_cast<uint8_t>(port >> 8), static_cast<uint8_t>(port),
            0x00, static_cast<uint8_t>(rows.size()), 0x00, 0x00};
        for (const auto& r : rows) {
            const uint8_t row[8] = {
                0, static_cast<uint8_t>(stream),
                0, static_cast<uint8_t>(r.first),
                                    0, static_cast<uint8_t>(r.second), 0, 0};
            pl.insert(pl.end(), row, row + 8);
        }
        const auto resp = aecp_xact(cmd, pl);
        const long st = aecp_status(resp);
        if (st != 0 && st != 7 && trace_map_cmd) {
            std::printf("  [i]    map command %u returned status %ld, %zu "
                        "bytes:", cmd, st, resp.size());
            for (size_t i = 0; i < resp.size() && i < 56; i++)
                std::printf(" %02X", resp[i]);
            std::printf("\n");
        }
        //! the route record models the SERIAL SLOTS, which are fed by global
        //! cluster keys 0..7 - STREAM_PORT_INPUT 0's own block. A mapping on
        //! another port reaches no slot, so recording it here would make the
        //! oracle describe a lane that does not exist.
        if (st == 0 && port == 0) {
            for (const auto& r : rows) {
                if (r.second < 0 || r.second >= kSlots) continue;
                const bool add = (cmd == kCmdAddMappings);
                route[static_cast<size_t>(r.second)] = add ? r.first : -1;
                route_stream[static_cast<size_t>(r.second)] = add ? stream : -1;
            }
        }
        return st;
    }

    //! The GET_AUDIO_MAP page, as {stream_index, stream_channel,
    //! cluster_offset} rows.
    std::vector<std::array<int, 3>> get_audio_map(int port = 0, int page = 0,
                                                  long* number_of_maps = nullptr) {
        const std::vector<uint8_t> pl = {
            static_cast<uint8_t>(kDescStreamPortIn >> 8),
            static_cast<uint8_t>(kDescStreamPortIn),
            static_cast<uint8_t>(port >> 8), static_cast<uint8_t>(port),
            static_cast<uint8_t>(page >> 8), static_cast<uint8_t>(page),
            0x00, 0x00};
        const auto r = aecp_xact(kCmdGetAudioMap, pl);
        std::vector<std::array<int, 3>> rows;
        if (aecp_status(r) != 0 || r.size() < 50) return rows;
        if (number_of_maps != nullptr)
            *number_of_maps = (static_cast<long>(r[44]) << 8) | r[45];
        const unsigned n = (static_cast<unsigned>(r[46]) << 8) | r[47];
        if (r.size() < 50 + 8 * n) return rows;
        for (unsigned i = 0; i < n; i++) {
            const size_t o = 50 + 8 * i;
            rows.push_back({static_cast<int>((r[o] << 8) | r[o + 1]),
                            static_cast<int>((r[o + 2] << 8) | r[o + 3]),
                            static_cast<int>((r[o + 4] << 8) | r[o + 5])});
        }
        return rows;
    }

    // ---------------------------------------------------------------- //
    //  CSR crossbar window                                             //
    // ---------------------------------------------------------------- //
    static constexpr uint16_t kChmapCtrl = 0x900;
    static constexpr uint16_t kChmapSel  = 0x904;
    static constexpr uint16_t kChmapWord = 0x908;
    static constexpr uint16_t kChmapSnap = 0x910;
    static constexpr uint16_t kChmapLoop = 0x914;

    //! the render RAM word at a PHYSICAL render key. The 0x904 selector is a
    //! PHYSICAL key on the readback side and a GLOBAL CLUSTER key on the
    //! 0x908 write side; on every shape shipped so far the two coincided, and
    //! on this one they differ by the lane base. That asymmetry is preserved
    //! from source, documented in the register map, and pinned by T10.
    uint32_t render_ram(int phys_key) {
        axi_write(kChmapSel, static_cast<uint32_t>(phys_key));
        axi_write(kChmapSnap, 1);
        for (int g = 0; g < 64; g++) {
            const uint32_t sv = axi_read(kChmapSnap);
            if ((sv & 1) == 0) break;
        }
        const uint32_t v = axi_read(kChmapLoop);
        if (((v >> 26) & 1) == 0) return 0xFFFFFFFFu;
        return v & 0xFF;
    }

    //! one CSR 0x908 write, addressed by GLOBAL CLUSTER key
    void csr_map_write(int cluster_key, uint32_t word16) {
        const uint32_t ctrl = axi_read(kChmapCtrl);
        axi_write(kChmapCtrl, ctrl | 1u);
        axi_write(kChmapSel, static_cast<uint32_t>(cluster_key));
        axi_write(kChmapWord, word16);
        axi_write(kChmapCtrl, ctrl);
        steps(16);
    }

    // ---------------------------------------------------------------- //
    //  ACMP: the bind ladder and the unbind                            //
    // ---------------------------------------------------------------- //
    std::vector<uint8_t> sniff_fr;
    uint16_t probe_seq = 0;
    bool probe_seen = false;

    void sniff_probe() {
        if (!(dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready)) return;
        for (int l = 0; l < 8; l++)
            if ((dut->m_axis_mac_tx_tkeep >> l) & 1)
                sniff_fr.push_back(static_cast<uint8_t>(dut->m_axis_mac_tx_tdata >> (8 * l)));
        if (!dut->m_axis_mac_tx_tlast) return;
        if (sniff_fr.size() >= 64 && sniff_fr[12] == 0x22 && sniff_fr[13] == 0xF0 &&
            sniff_fr[14] == 0xFC && (sniff_fr[15] & 0xF) == 0x0) {
            probe_seq = static_cast<uint16_t>((sniff_fr[62] << 8) | sniff_fr[63]);
            probe_seen = true;
        }
        sniff_fr.clear();
    }

    //! The two AAF stream identities this leg binds: listener k takes the
    //! talker's stream k. Stream 1 exists only on the multi-stream shape, and
    //! its DMAC and stream id are BOTH distinct, so nothing about the second
    //! stream can be mistaken for the first at the classifier or the filter.
    static constexpr uint8_t kSid[2][8] = {
        {0x02, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00},
        {0x02, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00, 0x02}};
    static constexpr uint8_t kStreamDmac[2][6] = {
        {0x91, 0xE0, 0xF0, 0x00, 0x2A, 0x02},
        {0x91, 0xE0, 0xF0, 0x00, 0x2A, 0x04}};

    //! the fixed ACMP identities, written into every command and answer
    static void acmp_head(uint8_t* f, uint8_t msg_type, int listener,
                          int talker) {
        const uint8_t mc[6] = {
            0x91, 0xE0, 0xF0, 0x01, 0x00, 0x00};
        memcpy(f, mc, 6);
        f[12] = 0x22; f[13] = 0xF0; f[14] = 0xFC; f[15] = msg_type;
        f[16] = 0x00; f[17] = 44;
        for (int i = 26; i < 34; i++) f[i] = static_cast<uint8_t>(i);
        const uint8_t tk[8] = {
            0x02, 0x00, 0x00, 0xFF, 0xFE, 0x00, 0x00, 0x02};
        memcpy(f + 34, tk, 8);
        const uint8_t ls[8] = {
            0x02, 0x00, 0x00, 0xFF, 0xFE, 0x00, 0x00, 0x01};
        memcpy(f + 42, ls, 8);
        f[51] = static_cast<uint8_t>(talker);      // talker_unique_id
        f[53] = static_cast<uint8_t>(listener);    // listener_unique_id
    }

    void acmp_connect_rx(uint16_t seq, int listener = 0, int talker = 0) {
        uint8_t f[72]; memset(f, 0, sizeof f);
        acmp_head(f, 0x06, listener, talker);
        const uint8_t csrc[6] = {
            0x68, 0x05, 0xCA, 0x95, 0xB2, 0xD1};
        memcpy(f + 6, csrc, 6);
        f[62] = static_cast<uint8_t>(seq >> 8); f[63] = static_cast<uint8_t>(seq);
        inject(f, 70);
    }

    void acmp_play_talker_response(int listener = 0, int talker = 0) {
        uint8_t f[72]; memset(f, 0, sizeof f);
        acmp_head(f, 0x01, listener, talker);
        const uint8_t tsrc[6] = {
            0x02, 0x00, 0x00, 0x00, 0x00, 0x02};
        memcpy(f + 6, tsrc, 6);
        memcpy(f + 18, kSid[talker], 8);
        memcpy(f + 54, kStreamDmac[talker], 6);
        f[62] = static_cast<uint8_t>(probe_seq >> 8);
        f[63] = static_cast<uint8_t>(probe_seq & 0xFF);
        inject(f, 70);
    }

    //! DISCONNECT_RX alone drops the bind: the record's enable falls without
    //! a talker answer, which is exactly the qualified bind fall the render
    //! epoch watches for.
    void acmp_disconnect_rx(uint16_t seq, int listener = 0, int talker = 0) {
        uint8_t f[72]; memset(f, 0, sizeof f);
        acmp_head(f, 0x08, listener, talker);
        const uint8_t csrc[6] = {
            0x68, 0x05, 0xCA, 0x95, 0xB2, 0xD1};
        memcpy(f + 6, csrc, 6);
        memcpy(f + 18, kSid[talker], 8);
        f[62] = static_cast<uint8_t>(seq >> 8); f[63] = static_cast<uint8_t>(seq);
        inject(f, 70);
    }

    void bring_out_of_reset();
    void bind_listener_zero();
    void run_the_bind_ladder(int listener, int talker, uint16_t seq,
                             const char* tag);
    void phase_map();
    void phase_multistream();
    void prove_an_unrelated_stream_loss_leaves_the_lane_running();
    void prove_a_stale_stream_repoint_is_bounded(int slot, int chan);
    void prove_the_lane_renders_a_second_stream(int slot, int chan);
    void prove_a_rendered_stream_loss_closes_the_epoch(int slot, int chan);
    void prove_the_nonphysical_key_mirrors_without_reaching_a_pin();
    void phase_serial();
    void phase_csr();
    void phase_reset();
    void phase_bind_loss();
    void phase_crf();
    long set_clock_source(uint16_t index);
    long get_clock_source();
    void provision_the_crf_sink();
    void select_crf_under_the_running_stream();
    void prove_the_setpoint_law_still_holds(long first_id, long last_id,
                                            const char* tag);
    void deselect_back_to_internal(uint64_t epochs_before);

    //! THE GRADING RULE. Every published frame is matched against the
    //! injection record at some advance a in 0..kMaxAdvance; the smallest a
    //! that matches wins. a == 0 on a later frame is a REPEAT and needs a
    //! counted underrun; a > 1 is a SKIP of a-1 events and needs a-1 COUNTED
    //! skips - which may already be PENDING, because the counter increments
    //! when a prefetched frame is overwritten and that is BEFORE the decoded
    //! frame whose ordinal jump exposes it.
    struct Grade {
        long frames = 0;
        long repeats = 0;
        long skipped = 0;
        long identity_failures = 0;
        long pad_failures = 0;
        long channel_field_failures = 0;
        long coherence_failures = 0;
        long distinct_failures = 0;
        long uncounted_repeats = 0;
        long uncounted_skips = 0;
        long pending_skips = 0;
        long cursor = 0;
        //! the advance each decoded frame took, so a later measurement can
        //! walk the COMMIT cursor beside the event cursor
        std::vector<long> advances;
    };
    Grade grade_frames(long first_event, const char* tag);

    //! Where in the IMMUTABLE injection record one decoded frame sits, or -1
    //! when no ordinal matches it. Searched, never assumed: the preserved
    //! prefill snap and the epoch admission decide which event renders first,
    //! and a slot fed from another stream carries its own ordinal and takes
    //! no part in the match.
    long find_the_ordinal(const DecodedFrame& fr) const {
        return find_the_ordinal_raw(fr.slot, /*slip=*/false);
    }

    //! ...over a raw slot array, so the negative-control decoder is graded by
    //! the same search. `slip` grades against the injected words shifted UP
    //! one place, which is what a reading one rise late recovers: the 24-bit
    //! field of a slot window started one bclk late is (injected << 1), the
    //! carried-in bit landing below it among the eight pad bits.
    long find_the_ordinal_raw(const std::array<uint32_t, kSlots>& slot,
                              bool slip) const {
        for (size_t e = 0; e + 1 < inj.size(); e++) {
            bool all = true;
            for (int k = 0; k < kSlots && all; k++) {
                if (stream_of_slot(k) > 0) continue;
                const int s = src_of_slot(k);
                uint32_t want = (s < 0) ? 0u : inj[e][static_cast<size_t>(s)];
                if (slip) want = (want << 1) & 0xFFFFFFu;
                if ((slot[static_cast<size_t>(k)] >> 8) != want) all = false;
            }
            if (all) return static_cast<long>(e);
        }
        return -1;
    }

    //! WHICH COMMIT PRODUCED THE FIRST DECODED FRAME is not a guess. The
    //! frame CDC cannot deliver a committed frame to the serial side faster
    //! than its own registered depth, and slot 0 carries one bit period of
    //! serial position on top, so the newest commit that old is a floor no
    //! closer commit can have met. Returns its index in `commit_cycle`, or -1
    //! when the window opened before any commit could qualify.
    long seat_the_commit_cursor(long pin0_half) const {
        const double pin0 = static_cast<double>(pin0_half) * kAxisPerHalf;
        long cursor = -1;
        for (size_t j = 0; j < commit_cycle.size(); j++)
            if (static_cast<double>(commit_cycle[j])
                    <= pin0 - kCdcFloorAxis - kBitAxis)
                cursor = static_cast<long>(j);
        return cursor;
    }

    //! One decoded window's verdict, so the INTERNAL and CRF windows are
    //! graded by ONE instrument and their numbers are comparable.
    struct Window {
        Grade g;
        uint64_t skips = 0;             //! counted over the window
        uint64_t unders = 0;
        uint64_t epochs = 0;
        long phi_min = 0;               //! commit-to-pin, axis cycles
        long phi_max = 0;
        long phi_n = 0;
        //! ...and its WALK: the first and last correlated measurements and
        //! the harness time between them, which is what turns a spread into
        //! a RATE the divider plan can be compared against
        long phi_first = 0;
        long phi_last = 0;
        long t_first = 0;
        long t_last = 0;
        double walk_ppm = 0.0;
        long start = -1;                //! the first decoded ordinal
    };
    Window decode_and_grade_a_window(long cycles, const char* tag);
    void report_a_window(const Window& w, const char* tag);
    void prove_the_aligned_window_is_the_acceptance_state(const Window& intr,
                                                          const Window& crf);

    //! The arms phase_serial and the two epoch phases run, each named for what
    //! it proves rather than for the order it happens to sit in.
    void prove_the_first_rendered_event_is_the_derived_one();
    void prove_the_late_attribution_reading_is_one_bit_late();
    void grade_the_decoded_window(long first_event, uint64_t skips_before,
                                  uint64_t unders_before);
    void measure_the_bank_term(long* walk_min, long* walk_max);
    void measure_the_commit_to_pin_terms(const Grade& g);
    void publish_the_measured_terms(long walk_min, long walk_max, long tmin,
                                    long tmax, double bit_axis);
    void prove_each_slot_sits_at_its_own_position(double bit_axis);
    void prove_the_lane_counters_are_coherent(uint64_t skips_before,
                                              uint64_t unders_before);
    void prove_the_surplus_is_drop_oldest();
    void prove_a_removal_silences_only_its_own_slots();
    void prove_a_stopped_clock_reset_reopens_one_epoch(
            const std::array<uint32_t, kSlots>& pre_epoch,
            uint64_t epochs_before);
    void prove_a_hard_reset_interrupts_and_rearms(const char* tag,
                                                  bool at_frame_wrap);
    void prove_a_reset_inside_an_outstanding_round_trip();
    void prove_two_bind_falls_in_one_round_trip_count_twice();
    void prove_the_lane_recovers_after_a_reset();
    void prove_the_graceful_flush_left_the_frame_in_flight_whole();
    void prove_a_rebind_carries_only_post_rebind_audio(uint64_t epochs_before,
                                                       long events_at_loss);

    //! how many serial slots the route record currently feeds. An oracle over
    //! an empty route would match every ordinal trivially, so every arm that
    //! grades identity states this first.
    int routed_slots() const {
        int n = 0;
        for (int k = 0; k < kSlots; k++) if (route[static_cast<size_t>(k)] >= 0) ++n;
        return n;
    }
};

// ====================================================================== //

bool TdmRenderHarness::load_descriptor_image(const char* path) {
    std::FILE* f = std::fopen(path, "rb");
    if (f == nullptr) return false;
    uint8_t buf[4096];
    size_t n = 0;
    while ((n = std::fread(buf, 1, sizeof buf, f)) > 0)
        desc_img.insert(desc_img.end(), buf, buf + n);
    std::fclose(f);
    return !desc_img.empty();
}

void TdmRenderHarness::bring_out_of_reset() {
    dut->axis_resetn = 0; dut->gtx_resetn = 0;
    dut->m_axis_mac_tx_tready = 1;
    dut->i_mac_speed = 0b10; dut->i_link_up = 1; dut->i_full_duplex = 1;
    steps(64);
    dut->axis_resetn = 1; dut->gtx_resetn = 1;
    steps(256);
}

void TdmRenderHarness::bind_listener_zero() {
    constexpr uint16_t kAdpCtrl = 0x600;
    constexpr uint16_t kAdpEidLo = 0x604;
    constexpr uint16_t kAdpEidHi = 0x608;
    constexpr uint16_t kAcmplState = 0x6A4;
    // THE STATION MAC IS LEFT AT ITS RESET ZERO, on purpose. This leg
    // addresses AECP commands to the station's own unicast address, and the
    // RX address filter answers "is this the station" against exactly that
    // register; a bench that programmed a group address there and then sent a
    // unicast command to it would be filtered out, and silence from a filter
    // looks the same as silence from a broken responder. Every other frame
    // this leg sends is multicast.
    axi_write(kAdpEidHi, 0x020000FF);
    axi_write(kAdpEidLo, 0xFE000001);
    axi_write(kAdpCtrl, 0x00001F01);
    steps(2000);
    run_the_bind_ladder(0, 0, 0x1122, "T1 BIND");
    check.dec("T1 BIND: listener 0 bound (0x6A4[3], the class-D record)",
              (axi_read(kAcmplState) >> 3) & 1, 1);
}

//! The sim_main ACMP ladder for ONE listener: BIND_RX, the harvested
//! PROBE_TX, a played CONNECT_TX_RESPONSE. The probe's sequence id is taken
//! off the egress rather than assumed, so a listener that never asked is a
//! failure here and not a silent non-bind two hundred lines later.
void TdmRenderHarness::run_the_bind_ladder(int listener, int talker,
                                           uint16_t seq, const char* tag) {
    char what[160];
    probe_seen = false;
    acmp_connect_rx(seq, listener, talker);
    for (int c = 0; c < 4000 && !probe_seen; c++) step();
    std::snprintf(what, sizeof what,
                  "%s: listener %d launched a PROBE_TX at the named talker",
                  tag, listener);
    check.dec(what, probe_seen ? 1 : 0, 1);
    acmp_play_talker_response(listener, talker);
    steps(3000);
}

TdmRenderHarness::Grade TdmRenderHarness::grade_frames(long first_event,
                                                       const char* tag) {
    Grade g;
    g.cursor = first_event;
    long skips_accounted = 0;
    const uint64_t skips0 = decoded.empty() ? 0 : decoded.front().skips_at;
    uint64_t unders_prev = decoded.empty() ? 0 : decoded.front().unders_at;
    bool first = true;
    for (const DecodedFrame& fr : decoded) {
        // THE STRUCTURAL CHECKS COME FIRST, and they are counted before the
        // ordinal search rather than after it: they must be INDEPENDENT of
        // the identity oracle, or a frame the oracle cannot place would
        // silently take its padding and its per-slot structure with it. A
        // data line shifted by one bit is exactly that case - it moves no
        // clock, so the framing counter cannot see it, and what does see it
        // is the padding and the full-word grading.
        bool pad_ok = true;
        bool chan_ok = true;
        bool coherent = true;
        std::array<uint32_t, kSlots> data{};
        for (int k = 0; k < kSlots; k++) {
            const uint32_t raw = fr.slot[static_cast<size_t>(k)];
            data[static_cast<size_t>(k)] = raw >> 8;          // 24 data bits
            if ((raw & 0xFFu) != 0) pad_ok = false;           // 8 pad bits
        }
        {
            uint32_t sid = 0;
            bool have_sid = false;
            std::array<uint32_t, kSlots> seen0{};
            int n0 = 0;
            for (int k = 0; k < kSlots; k++) {
                const int s = src_of_slot(k);
                if (s < 0) continue;
                const uint32_t v = data[static_cast<size_t>(k)];
                //! the channel field is graded for EVERY routed slot, and a
                //! slot fed from another stream carries that stream's own
                //! channel marking - which is the whole point of grading it
                const uint32_t want_chan =
                    (stream_of_slot(k) == 0) ? static_cast<uint32_t>(s)
                                             : (0x80u | static_cast<uint32_t>(s));
                if ((v & 0xFFu) != want_chan) chan_ok = false;
                //! ...but only slots fed from THIS record's stream share one
                //! media event identity, so the coherence and distinctness
                //! terms are over those
                if (stream_of_slot(k) != 0) continue;
                if (!have_sid) { sid = v >> 8; have_sid = true; }
                else if ((v >> 8) != sid) coherent = false;
                for (int j = 0; j < n0; j++)
                    if (seen0[static_cast<size_t>(j)] == v) ++g.distinct_failures;
                seen0[static_cast<size_t>(n0++)] = v;
            }
            if (!pad_ok) ++g.pad_failures;
            if (!chan_ok) ++g.channel_field_failures;
            if (!coherent) ++g.coherence_failures;
        }
        long advance = -1;
        for (int a = 0; a <= kMaxAdvance; a++) {
            const size_t e = static_cast<size_t>(g.cursor + a);
            if (e >= inj.size()) break;
            bool all = true;
            for (int k = 0; k < kSlots && all; k++) {
                //! a slot fed from another stream has its own ordinal, so it
                //! takes no part in THIS record's match; its structure is
                //! graded above and its stream is proved at the pins by the
                //! multi-stream arm
                if (stream_of_slot(k) > 0) continue;
                const int s = src_of_slot(k);
                const uint32_t want = (s < 0) ? 0u
                                    : inj[e][static_cast<size_t>(s)];
                if (data[static_cast<size_t>(k)] != want) all = false;
            }
            if (all) { advance = a; break; }
        }
        if (advance < 0) {
            ++g.identity_failures;
            if (g.identity_failures <= 4) {
                std::printf("  [i]    %s frame %ld: no injection ordinal in "
                            "[%ld, %ld] matches", tag, g.frames, g.cursor,
                            g.cursor + kMaxAdvance);
                for (int k = 0; k < kSlots; k++)
                    std::printf(" s%d=%06X(src %d)", k,
                                data[static_cast<size_t>(k)], src_of_slot(k));
                std::printf("\n");
            }
            g.advances.push_back(1);        // assume the nominal advance
            ++g.frames;
            continue;
        }
        g.advances.push_back(first ? 0 : advance);

        const long pending = static_cast<long>(fr.skips_at - skips0) - skips_accounted;
        if (advance == 0 && !first) {
            ++g.repeats;
            if (fr.unders_at != unders_prev + 1) ++g.uncounted_repeats;
        } else if (advance > 1) {
            const long lost = advance - 1;
            g.skipped += lost;
            if (pending < lost) ++g.uncounted_skips;
            else skips_accounted += lost;
        }
        g.pending_skips = static_cast<long>(fr.skips_at - skips0) - skips_accounted;
        unders_prev = fr.unders_at;
        g.cursor += advance;
        ++g.frames;
        first = false;
    }
    return g;
}

// ====================================================================== //
//  Phases                                                                //
// ====================================================================== //

void TdmRenderHarness::phase_map() {
    std::printf("\n[MAP] the dynamic AUDIO_MAP command path and its projection\n");
    bind_listener_zero();
    route_reset();
    // The AECP store must actually have READ the entity image, or a refusal
    // below would be a stalled model rather than a verdict.
    check.that("the AECP descriptor store fetched the entity image",
               desc_requests > 0);
    std::printf("  [i]    %ld descriptor burst(s) served from the %zu-byte "
                "generated image\n", desc_requests, desc_img.size());

    // T2 ADD: eight records, a permutation with no fixed point
    std::vector<std::pair<int, int>> rows;
    for (int co = 0; co < kSlots; co++)
        rows.emplace_back(kPerm[static_cast<size_t>(co)], co);
    check.dec("T2 ADD: eight permuted mappings accepted",
              static_cast<uint64_t>(map_cmd(kCmdAddMappings, rows)), 0);

    // T3 GET: the requested semantic mapping comes back
    long nmaps = -1;
    const auto page = get_audio_map(0, 0, &nmaps);
    check.dec("T3 GET: the page carries all eight mappings", page.size(), kSlots);
    check.dec("T3 GET: number_of_maps is 1", static_cast<uint64_t>(nmaps), 1);
    long agree = 0;
    for (const auto& r : page)
        if (r[0] == 0 && r[2] >= 0 && r[2] < kSlots &&
            r[1] == src_of_slot(r[2]))
            ++agree;
    check.dec("T3 GET: every row agrees with the issued route record",
              static_cast<uint64_t>(agree), page.size());

    // T4 PROJECTION: the render RAM, read at PHYSICAL keys
    long projected = 0;
    for (int k = 0; k < kSlots; k++) {
        const uint32_t w = render_ram(kTdmBase + k);
        const uint32_t want = 0x80u | static_cast<uint32_t>(src_of_slot(k) & 0x3F);
        if (w == want) ++projected;
        else std::printf("  [i]    T4 physical key %d holds %02X, expected %02X\n",
                         kTdmBase + k, w, want);
    }
    check.dec("T4 PROJECTION: physical keys 2..9 hold the routed sources",
              static_cast<uint64_t>(projected), kSlots);
    long dac_clear = 0;
    for (int k = 0; k < kI2sN; k++)
        if (render_ram(kI2sBase + k) == 0) ++dac_clear;
    check.dec("T4 PROJECTION: nothing reached the pruned DAC lane keys",
              static_cast<uint64_t>(dac_clear), kI2sN);

    // T9 the two refusals, each named for its own defect class
    check.dec("T9 CLUSTER-BOUND: cluster_offset 8 past this port's 8 clusters "
              "is BAD_ARGUMENTS",
              static_cast<uint64_t>(map_cmd(kCmdAddMappings, {{0, kSlots}})), 7);
    check.dec("T9 STREAM-CHANNEL: stream_channel 8 outside the format is "
              "BAD_ARGUMENTS",
              static_cast<uint64_t>(map_cmd(kCmdAddMappings, {{kChans, 0}})), 7);
    long unchanged = 0;
    for (int k = 0; k < kSlots; k++)
        if (render_ram(kTdmBase + k) ==
            (0x80u | static_cast<uint32_t>(src_of_slot(k) & 0x3F))) ++unchanged;
    check.dec("T9: the render RAM is bit-identical after both refusals",
              static_cast<uint64_t>(unchanged), kSlots);
}

void TdmRenderHarness::phase_serial() {
    std::printf("\n[SERIAL] the pins, decoded, against the injection record\n");
    build_injection_record(400);
    feed_on = true;
    next_pdu_at = axis_cycle + 64;
    pdu_cursor = 0;
    if (defect_stopped_clock) {
        std::printf("  [i]    DEFECT ARM: clk_tdm_i held static through the "
                    "serial window\n");
        tdm_frozen = true;
    }
    // PREFILL AND LOCK, WITH THE DECODER ALREADY OPEN. The setpoint's own
    // 18-to-14 snap happens here, and the first ELIGIBLE event is decided by
    // it, not by the first injection: the window below opens before the snap,
    // so the first event that ever reaches the pins is observed rather than
    // searched for, and it is graded against the derived ordinal.
    decoder_reset();
    taps_reset();
    collect = true;
    run_fed(10 * kPduPeriodCycles);
    collect = false;
    prove_the_first_rendered_event_is_the_derived_one();
    run_fed(50 * kPduPeriodCycles);
    decoder_reset();
    taps_reset();
    collect = true;
    const long first_event = injected_events;
    const uint64_t skips_before = lane_skips();
    const uint64_t unders_before = lane_unders();
    run_fed(140 * kPduPeriodCycles);
    collect = false;

    check.that("T5 FRAMING: consecutive fsync rises are exactly 256 bclk rises "
               "apart", gap_faults == 0 && fsync_rises > 4);
    check.that("T5 FRAMING: the free-running position is 0 at every one-rise "
               "expiry", framing_faults == 0);
    check.that("T5 FRAMING: the window decoded whole frames", !decoded.empty());
    prove_the_late_attribution_reading_is_one_bit_late();
    // An oracle over an EMPTY route matches every ordinal trivially, so the
    // route the grading stands on is stated before anything is graded.
    check.dec("T6 PRECONDITION: every serial slot is routed, so no frame can "
              "match trivially", static_cast<uint64_t>(routed_slots()), kSlots);
    if (decoded.empty()) {
        std::printf("  [i]    T5: no frame decoded - fsync rises %ld, bclk "
                    "rises %ld\n", fsync_rises, rises);
        return;
    }

    grade_the_decoded_window(first_event, skips_before, unders_before);
}

//! T5 NEGATIVE CONTROL (issue #452): the OLD bus's other reading, graded on
//! the SAME window and the SAME three pins. A check that would pass whichever
//! edge fsync launches on is worth nothing, so this one is stated as the two
//! halves of "one bit late": the late-attribution decoder reproduces NO
//! injected media event, and every frame it does produce is an injected one
//! shifted up a place. Move the RTL edge back onto the rise and this decoder
//! is the correct one - both halves then fail, by name.
void TdmRenderHarness::prove_the_late_attribution_reading_is_one_bit_late() {
    long plain = 0;
    long slipped = 0;
    for (const auto& w : late_frames) {
        if (find_the_ordinal_raw(w, /*slip=*/false) >= 0) ++plain;
        if (find_the_ordinal_raw(w, /*slip=*/true) >= 0) ++slipped;
    }
    check.that("T5 NEGATIVE CONTROL: the late-attribution decoder framed and "
               "decoded whole frames", late_frames.size() > 4);
    check.dec("T5 NEGATIVE CONTROL: it reproduces NO injected media event",
              static_cast<uint64_t>(plain), 0);
    check.dec("T5 NEGATIVE CONTROL: every frame it decodes is an injected one "
              "read ONE BIT LATE", static_cast<uint64_t>(slipped),
              static_cast<uint64_t>(late_frames.size()));
}

//! T6 PREFILL: the FIRST event this lane ever renders, DERIVED and then
//! observed. The window this runs on opened before the prefill snap, so the
//! lane is watched from digital silence through its first audio frame. The
//! expected ordinal is kFirstEligibleEvent, computed from the preserved
//! prefill rule and this leg's own feed rate; the only law allowed to move it
//! is drop-oldest, which counts every frame it overwrites, so the ordinal is
//! corrected by the lane's OWN counted skips and the remainder is an equality.
void TdmRenderHarness::prove_the_first_rendered_event_is_the_derived_one() {
    check.that("T6 PREFILL: the window opened at prefill decoded whole frames",
               decoded.size() > 4);
    long first_nz = -1;
    for (size_t i = 0; i < decoded.size() && first_nz < 0; i++)
        for (int k = 0; k < kSlots; k++)
            if (decoded[i].slot[static_cast<size_t>(k)] != 0) {
                first_nz = static_cast<long>(i);
                break;
            }
    check.that("T6 PREFILL: the lane rendered digital silence before its "
               "first eligible event, and then rendered one", first_nz > 0);
    if (first_nz <= 0) return;
    const DecodedFrame& fr = decoded[static_cast<size_t>(first_nz)];
    const long ordinal = find_the_ordinal(fr);
    const long skips = static_cast<long>(fr.skips_at - decoded.front().skips_at);
    std::printf("  [i]    T6 PREFILL: silence for %ld frame(s), then ordinal "
                "%ld with %ld counted skip(s); derived first eligible ordinal "
                "%ld (%ld events pushed at the snap, %d kept)\n",
                first_nz, ordinal, skips, kFirstEligibleEvent,
                kPrefillPdus * kEvents, kPrefillTargetEvt);
    check.that("T6 PREFILL: the first rendered frame is an injected media "
               "event", ordinal >= 0);
    if (ordinal < 0) return;
    check.dec("T6 PREFILL: the first event the lane renders is the one the "
              "preserved prefill snap leaves at the head, plus its own "
              "counted skips",
              static_cast<uint64_t>(ordinal - skips),
              static_cast<uint64_t>(kFirstEligibleEvent));
}

//! The decoded window, graded against the immutable injection record: the
//! first eligible ordinal, the per-frame identity, padding and structure, the
//! order rules, and the arms that follow from them.
void TdmRenderHarness::grade_the_decoded_window(long first_event,
                                                uint64_t skips_before,
                                                uint64_t unders_before) {
    // WHERE THIS WINDOW STARTS. This window opens in mid-stream, long after
    // the prefill snap T6 PREFILL derived and graded, so its first ordinal is
    // whichever event the lane had reached - SEARCHED for in the injection
    // record rather than assumed, with the grading then requiring every later
    // frame to follow from it by a permitted advance. The DERIVED claim about
    // the first eligible event is the one above; this is the cursor for the
    // identity and order grading below.
    const DecodedFrame& f0 = decoded.front();
    const long start = find_the_ordinal(f0);
    check.that("T6 IDENTITY: the first decoded frame is an injected media "
               "event", start >= 0);
    if (start < 0) {
        std::printf("  [i]    T6: first decoded frame slots:");
        for (int k = 0; k < kSlots; k++)
            std::printf(" %08X", f0.slot[static_cast<size_t>(k)]);
        std::printf("\n");
    } else {
        check.that("T6 WINDOW: the first ordinal of this mid-stream window is "
                   "one the feed had already injected when it opened",
                   start <= first_event);
    }
    std::printf("  [i]    first decoded ordinal %ld; %ld events had been "
                "injected when collection opened\n", start, first_event);

    // The window is graded even when the first frame did not resolve to an
    // ordinal: falling back to the injection cursor keeps the per-frame
    // identity, padding and structural counts reportable, so a defect says
    // WHICH property it broke instead of stopping the phase at the door.
    const Grade g = grade_frames(start >= 0 ? start : first_event, "T6");
    check.dec("T6 IDENTITY: every decoded frame is a complete 24-bit match "
              "against the injection record",
              static_cast<uint64_t>(g.identity_failures), 0);
    check.dec("T6 PADDING: the eight pad bits of every slot are zero",
              static_cast<uint64_t>(g.pad_failures), 0);
    check.dec("T6 STRUCTURAL: each slot's channel field is its routed source",
              static_cast<uint64_t>(g.channel_field_failures), 0);
    check.dec("T6 STRUCTURAL: the eight slots carry one media event's identity",
              static_cast<uint64_t>(g.coherence_failures), 0);
    check.dec("T6 STRUCTURAL: the eight slots are distinct samples",
              static_cast<uint64_t>(g.distinct_failures), 0);
    check.dec("T6 ORDER: every repeat is a counted underrun",
              static_cast<uint64_t>(g.uncounted_repeats), 0);
    check.dec("T6 ORDER: every skipped event is covered by a counted skip",
              static_cast<uint64_t>(g.uncounted_skips), 0);
    std::printf("  [i]    %ld frames graded, %ld repeat(s), %ld skipped "
                "event(s), %ld counted skip(s) still pending adoption\n",
                g.frames, g.repeats, g.skipped, g.pending_skips);

    prove_the_lane_counters_are_coherent(skips_before, unders_before);
    measure_the_commit_to_pin_terms(g);
    prove_the_surplus_is_drop_oldest();
    prove_a_removal_silences_only_its_own_slots();
    feed_on = false;
    tdm_frozen = false;
}

//! T28 COUNTER SANITY: the gray counter crossing, read from the PINS' own
//! view of how many frames were delivered rather than from the counter
//! grading itself. `skips_before` and `unders_before` are the lane's values
//! when the window opened, printed so a later reader can place the deltas.
void TdmRenderHarness::prove_the_lane_counters_are_coherent(
        uint64_t skips_before, uint64_t unders_before) {
    check.dec("T28 COUNTERS: no sampled frame count went backwards",
              static_cast<uint64_t>(counter_regressions), 0);
    check.dec("T28 COUNTERS: no sampled frame count ran ahead of the frames "
              "the pins delivered",
              static_cast<uint64_t>(counter_impossible), 0);
    std::printf("  [i]    worst observed frames_o lead over decoded frame "
                "boundaries: %ld\n", counter_worst_lead);
    check.that("T28 COUNTERS: overruns did not move (drop-oldest keeps the "
               "CDC near empty)", lane_over() == 0);
    check.that("T28 COUNTERS: the lane counted at least as many frames as the "
               "pins delivered", lane_frames() >= static_cast<uint64_t>(fsync_rises) - 2);
    std::printf("  [i]    lane counters: frames %llu underruns %llu skips %llu "
                "overruns %llu epochs %llu (skips before the window %llu, "
                "underruns before %llu)\n",
                static_cast<unsigned long long>(lane_frames()),
                static_cast<unsigned long long>(lane_unders()),
                static_cast<unsigned long long>(lane_skips()),
                static_cast<unsigned long long>(lane_over()),
                static_cast<unsigned long long>(lane_epochs()),
                static_cast<unsigned long long>(skips_before),
                static_cast<unsigned long long>(unders_before));
}

//! T7 BANK TERM: how long the adapter takes to walk the crossbar's TDM key
//! window into the serializer's bank and commit it, measured between two
//! registered events in `axis_clk` - the crossbar's valid pulse and the frame
//! commit strobe - and never modelled.
void TdmRenderHarness::measure_the_bank_term(long* walk_min, long* walk_max) {
    *walk_min = 1 << 30;
    *walk_max = 0;
    const size_t n = (commit_cycle.size() < phys_valid_cycle.size())
                   ? commit_cycle.size() : phys_valid_cycle.size();
    for (size_t i = 0; i < n; i++) {
        const long d = commit_cycle[i] - phys_valid_cycle[i];
        if (d < 0 || d > 64) continue;              // an unpaired edge
        if (d < *walk_min) *walk_min = d;
        if (d > *walk_max) *walk_max = d;
    }
    check.that("T7 BANK TERM: the adapter's commit follows its crossbar pulse "
               "by a fixed number of cycles",
               *walk_max >= *walk_min && *walk_min >= 1 && *walk_max <= 32);
    //! AXIS CYCLES FIRST. The bank walk is an axis_clk interval, so its
    //! nanosecond value belongs to the clock that is running: this leg's
    //! model 100 MHz, and the shipping image's 50 MHz `milan` clock.
    std::printf("  [i]    T7 bank walk and commit: %ld..%ld axis cycles "
                "(%.1f..%.1f ns at this leg's %.0f MHz model axis clock; "
                "%.1f..%.1f ns at the shipping %.0f MHz milan clock) over "
                "%zu pairs\n",
                *walk_min, *walk_max,
                kModelNsPerAxis * static_cast<double>(*walk_min),
                kModelNsPerAxis * static_cast<double>(*walk_max),
                kModelAxisHz / 1e6,
                kShipNsPerAxis * static_cast<double>(*walk_min),
                kShipNsPerAxis * static_cast<double>(*walk_max),
                kShipAxisHz / 1e6, n);
}

void TdmRenderHarness::measure_the_commit_to_pin_terms(const Grade& g) {
    // T7 LATENCY - measured from REGISTERED events, never from a model.
    // The m-th crossbar valid pulse is correlated with the m-th decoded
    // frame BY COUNT; its payload is never read.
    if (!commit_cycle.empty() && !phys_valid_cycle.empty()) {
        long walk_min = 0;
        long walk_max = 0;
        measure_the_bank_term(&walk_min, &walk_max);
        // ...and the whole commit-to-pin interval, measured between two
        // REGISTERED events: the adapter's frame commit and the receiver's
        // sampling edge of that frame's slot 0 MSB. The commit that produced
        // a frame is the newest one that landed before its adoption, which is
        // drop-oldest's own rule, so the cursor is SEATED once that way (the
        // CDC's registered depth: the write pointer's gray value crosses two
        // flops and sets the empty flag - 3 read edges - the prefetch read
        // enable is one more, the FIFO's registered read data and the
        // fetch-valid flag one more, and the load of the double buffer one
        // more) and then walked by the grading's own advances, because
        // drop-oldest consumes exactly one commit per adoption plus one per
        // counted skip. Counted events, never a guessed alignment.
        long cursor = seat_the_commit_cursor(decoded.front().half_step);
        long tmin = 1 << 30;
    long tmax = -(1 << 30);
    long span_n = 0;
        long tail_unpaired = 0;
        long bad_interval = 0;
        for (size_t i = 0; i < decoded.size() && i < g.advances.size(); i++) {
            cursor += g.advances[i];
            if (cursor < 0 || cursor >= static_cast<long>(commit_cycle.size())) {
                ++tail_unpaired;            // the window ended, not a defect
                continue;
            }
            const double pin_axis = static_cast<double>(decoded[i].half_step) * kAxisPerHalf;
            const long d = static_cast<long>(pin_axis)
                         - commit_cycle[static_cast<size_t>(cursor)];
            if (d < 0 || d > 8000) { ++bad_interval; continue; }
            if (d < tmin) tmin = d;
            if (d > tmax) tmax = d;
            ++span_n;
        }
        if (span_n > 16) {
            // one serial frame is 256 bit periods = 512 clk_tdm cycles =
            // 512 x 1591/391 axis cycles (kFrameAxis), and one bit period is
            // two of them (kBitAxis)
            const double frame_axis = kFrameAxis;
            const double bit_axis = kBitAxis;
            check.that("T7 LATENCY: the commit-to-pin interval spreads by at "
                       "most one serial frame, so the delay does not ratchet",
                       static_cast<double>(tmax - tmin) <= frame_axis * 1.05);
            check.dec("T7 LATENCY: every decoded frame inside the window "
                      "paired with the commit that produced it",
                      static_cast<uint64_t>(bad_interval), 0);
            check.that("T7 LATENCY: the commit that produced a frame is at "
                       "least the CDC's own registered depth before its pin "
                       "edge", static_cast<double>(tmin) >= kCdcFloorAxis);
            std::printf("  [i]    T7 frame commit to slot 0 MSB sampling edge: "
                        "%ld..%ld axis cycles (%.3f..%.3f us) over %ld frames, "
                        "%ld past the window's end; one frame = %.3f us, one "
                        "bit period = %.4f us, CDC floor = %.1f cycles\n",
                        tmin, tmax, static_cast<double>(tmin) / 100.0,
                        static_cast<double>(tmax) / 100.0, span_n,
                        tail_unpaired, frame_axis / 100.0, bit_axis / 100.0,
                        kCdcFloorAxis);
            publish_the_measured_terms(walk_min, walk_max, tmin, tmax,
                                       bit_axis);
            prove_each_slot_sits_at_its_own_position(bit_axis);
        } else {
            check.fail("T7 LATENCY: too few correlated frames to measure the "
                       "commit-to-pin interval");
        }
    } else {
        check.fail("T7 LATENCY: no commit or crossbar pulse was observed");
    }
}

//! THE PUBLISHED TERMS, derived from the measurements above: the bank walk is
//! walk_min..walk_max, and the CDC-plus-adopt wait phi is what is left after
//! slot 0's own serial position is removed.
//!
//! WHICH CLOCK EACH TERM BELONGS TO. The bank walk is whole axis cycles and
//! doubles in nanoseconds on the shipping 50 MHz milan clock. phi is almost
//! all SERIAL time - the CDC's own read-side registers and the wait for the
//! next frame start, both in clk_tdm_i, whose absolute rate here IS the
//! shipping one - plus exactly ONE axis-domain register, the FIFO write
//! pointer the commit strobe advances. So phi as shipped is this measurement
//! plus that one cycle again. docs/design/TIME_SYNC.md publishes both.
void TdmRenderHarness::publish_the_measured_terms(long walk_min, long walk_max,
                                                  long tmin, long tmax,
                                                  double bit_axis) {
    const double phi_min_axis = static_cast<double>(tmin) - bit_axis;
    const double phi_max_axis = static_cast<double>(tmax) - bit_axis;
    std::printf("  [i]    T7 published terms, measured: bank walk and commit "
                "%ld..%ld axis cycles = %.1f..%.1f ns at the model axis "
                "clock, %.1f..%.1f ns at the shipping milan clock; adopt wait "
                "phi %.3f..%.3f us (the measured interval less slot 0's one "
                "bit period of serial position) = 1 axis cycle + %.3f..%.3f "
                "us of serial-domain wait, so %.3f..%.3f us on the shipping "
                "image; slot k adds %.4f us\n",
                walk_min, walk_max,
                kModelNsPerAxis * static_cast<double>(walk_min),
                kModelNsPerAxis * static_cast<double>(walk_max),
                kShipNsPerAxis * static_cast<double>(walk_min),
                kShipNsPerAxis * static_cast<double>(walk_max),
                phi_min_axis * kModelNsPerAxis / 1000.0,
                phi_max_axis * kModelNsPerAxis / 1000.0,
                (phi_min_axis - 1.0) * kModelNsPerAxis / 1000.0,
                (phi_max_axis - 1.0) * kModelNsPerAxis / 1000.0,
                ((phi_min_axis - 1.0) * kModelNsPerAxis + kShipNsPerAxis)
                    / 1000.0,
                ((phi_max_axis - 1.0) * kModelNsPerAxis + kShipNsPerAxis)
                    / 1000.0,
                32.0 * bit_axis / 100.0);
}

//! T7 SLOT POSITION: slot k's MSB must sit exactly 32k bit periods after
//! slot 0's, on every decoded frame. That is what makes "slot k" a
//! POSITION on the wire rather than a label in the bank.
void TdmRenderHarness::prove_each_slot_sits_at_its_own_position(
        double bit_axis) {
    long slot_pos_faults = 0;
    for (const DecodedFrame& fr : decoded) {
        for (int k = 1; k < kSlots; k++) {
            const double got =
                static_cast<double>(fr.msb_half[static_cast<size_t>(k)]
                                    - fr.msb_half[0]) * kAxisPerHalf;
            const double want = 32.0 * static_cast<double>(k) * bit_axis;
            if (got < want - 2.0 || got > want + 2.0) ++slot_pos_faults;
        }
    }
    check.dec("T7 SLOT POSITION: slot k's MSB sits exactly 32k bit periods "
              "after slot 0's, on every decoded frame",
              static_cast<uint64_t>(slot_pos_faults), 0);
}

void TdmRenderHarness::prove_the_surplus_is_drop_oldest() {
    // T14 SKIP LAW: hold the serial clock for several frame intervals while
    // the producer keeps committing, so the surplus is forced in bounded time
    // instead of waiting out the 1.96 s free-run beat. Drop-OLDEST keeps
    // prefetching the freshest committed frame, counts each overwritten one
    // and leaves the CDC near empty; drop-NEWEST would fill it, drop commits
    // as overruns and let the commit-to-pin delay ratchet upward.
    {
        const uint64_t skips0 = lane_skips();
        const uint64_t over0 = lane_over();
        feed_on = true;
        next_pdu_at = axis_cycle + 64;
        run_fed(10 * kPduPeriodCycles);
        tdm_frozen = true;
        // Two and a half frame intervals: enough that two producer commits
        // land inside one frame interval, and inside the CDC's four entries
        // so nothing is lost as an OVERRUN. A hold longer than the CDC is
        // depth-limited whatever the surplus policy is - the consumer cannot
        // drain a clock that is not running - so it would discriminate
        // nothing; that limit is recorded in docs/CHANNEL_MAP_64.md.
        run_fed(5200);
        tdm_frozen = false;
        run_fed(10 * kPduPeriodCycles);
        check.that("T14 SKIP LAW: the forced surplus was COUNTED as skips",
                   lane_skips() >= skips0 + 1);
        check.dec("T14 SKIP LAW: the CDC never filled, so no commit was "
                  "dropped as an overrun",
                  static_cast<uint64_t>(lane_over() - over0), 0);
        std::printf("  [i]    T14: skips %llu -> %llu, overruns %llu -> %llu "
                    "across a two-and-a-half-frame serial-clock hold\n",
                    static_cast<unsigned long long>(skips0),
                    static_cast<unsigned long long>(lane_skips()),
                    static_cast<unsigned long long>(over0),
                    static_cast<unsigned long long>(lane_over()));
        // ...and the delay is back inside the band it held before the hold,
        // which is what "does not ratchet" means at the pins
        decoder_reset();
        taps_reset();
        collect = true;
        run_fed(30 * kPduPeriodCycles);
        collect = false;
        if (!decoded.empty() && !commit_cycle.empty()) {
            const long cur = seat_the_commit_cursor(decoded.front().half_step);
            long worst = 0;
            if (cur >= 0) {
                const double pin_axis =
                    static_cast<double>(decoded.front().half_step) * kAxisPerHalf;
                worst = static_cast<long>(pin_axis)
                      - commit_cycle[static_cast<size_t>(cur)];
            }
            check.that("T14 SKIP LAW: the commit-to-pin delay after the hold "
                       "is still inside one frame, so it did not ratchet",
                       cur >= 0 && static_cast<double>(worst)
                                   <= kFrameAxis + kCdcFloorAxis + kBitAxis);
            std::printf("  [i]    T14: commit-to-pin after the hold = %ld axis "
                        "cycles (%.3f us)\n", worst,
                        static_cast<double>(worst) / 100.0);
        } else {
            check.fail("T14 SKIP LAW: nothing decoded after the serial-clock "
                       "hold");
        }
        feed_on = false;
    }

}

void TdmRenderHarness::prove_a_removal_silences_only_its_own_slots() {
    // T8 REMOVE: two of the eight, and nothing else moves
    const int drop_a = 2;
    const int drop_b = 5;
    check.dec("T8 REMOVE: two mappings removed",
              static_cast<uint64_t>(map_cmd(kCmdRemoveMappings,
                                            {{kPerm[drop_a], drop_a},
                                             {kPerm[drop_b], drop_b}})), 0);
    check.dec("T8 REMOVE: their physical keys read disabled",
              render_ram(kTdmBase + drop_a) | render_ram(kTdmBase + drop_b), 0);
    const auto page2 = get_audio_map(0, 0);
    long still = 0;
    for (const auto& r : page2)
        if (r[2] == drop_a || r[2] == drop_b) ++still;
    check.dec("T8 REMOVE: GET no longer reports them",
              static_cast<uint64_t>(still), 0);
    long dac_after = 0;
    for (int k = 0; k < kI2sN; k++)
        if (render_ram(kI2sBase + k) == 0) ++dac_after;
    check.dec("T8 REMOVE: no removal aliased the pruned DAC lane",
              static_cast<uint64_t>(dac_after), kI2sN);
    // the removed slots must now render digital silence while the rest are
    // still graded against the record
    decoder_reset();
    taps_reset();
    collect = true;
    run_fed(40 * kPduPeriodCycles);
    collect = false;
    long silent = 0;
    for (const DecodedFrame& fr : decoded) {
        if ((fr.slot[static_cast<size_t>(drop_a)] == 0) &&
            (fr.slot[static_cast<size_t>(drop_b)] == 0)) ++silent;
    }
    check.that("T8 REMOVE: the two removed slots carry 24'h000000 in every "
               "decoded frame",
               !decoded.empty() && silent == static_cast<long>(decoded.size()));
    if (!decoded.empty()) {
        const long start2 = find_the_ordinal(decoded.front());
        check.that("T8 REMOVE: the six surviving slots still grade against the "
                   "injection record", start2 >= 0);
        if (start2 >= 0) {
            const Grade g2 = grade_frames(start2, "T8");
            check.dec("T8 REMOVE: identity holds for the surviving slots",
                      static_cast<uint64_t>(g2.identity_failures), 0);
        }
    }
    // put the two mappings back for the later phases
    map_cmd(kCmdAddMappings, {{kPerm[drop_a], drop_a}, {kPerm[drop_b], drop_b}});
}

void TdmRenderHarness::phase_csr() {
    std::printf("\n[CSR] the diagnostic write window, by CLUSTER key\n");
    // T10: the 0x908 write arm addresses by GLOBAL CLUSTER key and projects
    // through the generated table; the 0x910/0x914 readback addresses by
    // PHYSICAL key with no projection. On this shape the two differ by the
    // lane base, which is the asymmetry the register map documents.
    const int cluster = 4;
    const int phys = kTdmBase + cluster;
    const uint32_t before = render_ram(phys);
    csr_map_write(cluster, 0x8006u);      // en, src 0, stream 0, channel 6
    const uint32_t after = render_ram(phys);
    check.hex("T10 CSR: a write by CLUSTER key lands at the PROJECTED "
              "physical key", after, 0x86u);
    check.that("T10 CSR: the readback selector is the PHYSICAL key, so the "
               "two sides differ by the lane base",
               before != after || kTdmBase == 0);
    // restore the AECP-owned route
    csr_map_write(cluster,
                  0x8000u | static_cast<uint32_t>(src_of_slot(cluster) & 0x7));
    check.hex("T10 CSR: the route is restored", render_ram(phys),
              0x80u | static_cast<uint32_t>(src_of_slot(cluster) & 0x3F));

    // T11: the OUT-OF-RANGE cluster key, named for what it is. On THIS shape
    // every declared key is projected, so a key with no projection is one PAST
    // the declared block - which is a different defect class from a legal
    // cluster whose RPHYS entry is invalid, and the two must not be graded as
    // one. The nonphysical IN-RANGE key needs a shape that has one; it is
    // graded, on both observations, by the multi-stream leg's M6.
    const int out_of_range = kSlots;      // key 8: the declared block is 0..7
    std::array<uint32_t, 16> ram_before{};
    for (int k = 0; k < kI2sN + kSlots; k++)
        ram_before[static_cast<size_t>(k)] = render_ram(k);
    csr_map_write(out_of_range, 0x8001u);
    long ram_same = 0;
    for (int k = 0; k < kI2sN + kSlots; k++)
        if (render_ram(k) == ram_before[static_cast<size_t>(k)]) ++ram_same;
    check.dec("T11 OUT OF RANGE: a cluster key past this model's declared keys "
              "changes no render RAM word",
              static_cast<uint64_t>(ram_same), kI2sN + kSlots);
    const auto page = get_audio_map(0, 0);
    long rows_out_of_block = 0;
    for (const auto& r : page)
        if (r[2] >= kSlots) ++rows_out_of_block;
    check.dec("T11 OUT OF RANGE: no mapping outside this port's declared "
              "cluster block appears in the GET page",
              static_cast<uint64_t>(rows_out_of_block), 0);
    std::printf("  [i]    T11: a suppressed CSR write is a CSR behaviour; no "
                "AECP status is asserted for it. The in-range PROJECTED mirror "
                "is T11b below; the in-range NONPHYSICAL one is the "
                "multi-stream leg's M6.\n");

    // T11b: the PRESERVED behaviour the suppression must not have changed.
    // An unlocked CSR write at an IN-RANGE cluster key writes the AECP
    // protocol store whatever its physical projection says; only the crossbar
    // write is gated by the projection. Here the key IS projected, so both
    // effects are visible and are checked independently - and it is a
    // PHYSICAL key, which is why it cannot stand in for the nonphysical case.
    const int mirror_key = 6;
    csr_map_write(mirror_key, 0x8007u);   // stream 0, channel 7
    check.hex("T11b MIRROR: the in-range PROJECTED CSR write reached the "
              "render RAM", render_ram(kTdmBase + mirror_key), 0x87u);
    const auto page_b = get_audio_map(0, 0);
    long mirrored = 0;
    for (const auto& r : page_b)
        if (r[2] == mirror_key && r[1] == 7 && r[0] == 0) ++mirrored;
    check.dec("T11b MIRROR: the same write is visible in the AECP protocol "
              "store through GET_AUDIO_MAP",
              static_cast<uint64_t>(mirrored), 1);
    // restore
    csr_map_write(mirror_key,
                  0x8000u | static_cast<uint32_t>(src_of_slot(mirror_key) & 0x7));
    map_cmd(kCmdAddMappings, {{src_of_slot(mirror_key), mirror_key}});
}

void TdmRenderHarness::phase_reset() {
    std::printf("\n[RESET] the four-phase render epoch over reset and a "
                "stopped serial clock\n");
    // Warm the lane: pointers away from zero, a recognisable pre-reset epoch
    // in the active and prefetched banks.
    build_injection_record(400);
    feed_on = true;
    next_pdu_at = axis_cycle + 64;
    run_fed(60 * kPduPeriodCycles);
    decoder_reset();
    collect = true;
    run_fed(20 * kPduPeriodCycles);
    collect = false;
    check.that("T18 WARM: the lane was serializing real audio before the reset",
               !decoded.empty());
    std::array<uint32_t, kSlots> pre_epoch{};
    if (!decoded.empty()) pre_epoch = decoded.back().slot;
    const uint64_t epochs_before = lane_epochs();

    prove_a_stopped_clock_reset_reopens_one_epoch(pre_epoch, epochs_before);
    //! the two placements C2's validation list names, and the one it already
    //! had: a reset inside the frame, a reset ON the frame wrap, and a reset
    //! while a round trip is outstanding
    prove_a_hard_reset_interrupts_and_rearms("T22", false);
    prove_a_hard_reset_interrupts_and_rearms("T20", true);
    prove_a_reset_inside_an_outstanding_round_trip();
    prove_the_lane_recovers_after_a_reset();
}

//! T18 and T21/T22: the four-phase epoch over a reset the SERIAL SIDE NEVER
//! SEES AS AN EDGE. The clock is stopped first, the datapath reset is asserted
//! and released entirely while it is stopped, and what reopens the lane when
//! the clock returns is the producer's RETAINED request, not a pulse.
void TdmRenderHarness::prove_a_stopped_clock_reset_reopens_one_epoch(
        const std::array<uint32_t, kSlots>& pre_epoch, uint64_t epochs_before) {
    // THE FEED KEEPS RUNNING ACROSS THE ASSERTION AND THE RELEASE. The
    // producer therefore has a live crossbar walk to commit at every media
    // tick throughout, before the reset, under it and after it, so what stops
    // a commit reaching the pins is the epoch and not an absence of traffic.
    // T21 below counts the commits in the release-to-reopen window at the
    // commit strobe, so a commit that carried no audible sample still counts.
    feed_on = true;
    next_pdu_at = axis_cycle + 64;
    tdm_frozen = true;
    run_fed(200);
    const int dout_frozen = dut->tdm_dout_o;
    const uint64_t frames_frozen = lane_frames();
    // A STOPPED CLOCK DELIVERS NOTHING, and that is the property to state -
    // not that the pin is low. The serial reset is SYNCHRONOUS, so with
    // clk_tdm_i stopped it cannot take effect at all: nothing shifts, the pin
    // holds whatever level it was last launched at, and no frame is counted,
    // which is what makes a stopped clock unreadable as delivered audio. The
    // statement is made BEFORE the reset, because a reset zeroes the
    // destination side of the counter export and would answer it trivially.
    run_fed(4000);
    check.dec("T18 STOPPED CLOCK: nothing shifts while clk_tdm_i is stopped, "
              "so the serial pin holds its last launched level",
              static_cast<uint64_t>(dut->tdm_dout_o),
              static_cast<uint64_t>(dout_frozen));
    check.that("T18 STOPPED CLOCK: no serial frame is counted while the clock "
               "is stopped", lane_frames() == frames_frozen);
    dut->axis_resetn = 0;
    run_fed(400);
    // The reset is RELEASED while the clock is still stopped, so the serial
    // domain never observes it as an edge at all. What it does observe, when
    // its clock returns, is the producer's RETAINED epoch request - the whole
    // reason the handshake is a level and not a pulse.
    dut->axis_resetn = 1;
    //! ...and once the counter export has re-synchronised after the reset -
    //! its clk_i side is zeroed by rst_n while the serial side, which never
    //! saw the reset, still holds the real count - the commit watch is armed.
    //! T21's window is then the DUT's own, from here to the counted
    //! reopening, rather than a step count this loop happened to choose. The
    //! serial clock stays STOPPED for a dozen media ticks inside it, which is
    //! what gives the window its content: the crossbar keeps offering the
    //! adapter a walk on every media tick while the epoch is closed and
    //! cannot reopen.
    run_fed(400);
    arm_the_commit_watch();
    run_fed(2 * kPduPeriodCycles);
    tdm_frozen = false;
    run_fed(4000);
    check.dec("T18 RESET: once the serial clock returns, the retained request "
              "flushes the lane and the pin is driven low",
              static_cast<uint64_t>(dut->tdm_dout_o), 0);
    decoder_reset();
    collect = true;
    run_fed(6000);
    collect = false;
    feed_on = false;
    long nonzero = 0;
    for (const DecodedFrame& fr : decoded)
        for (int k = 0; k < kSlots; k++)
            if (fr.slot[static_cast<size_t>(k)] != 0) ++nonzero;
    check.dec("T18 RESET: every frame decoded after the clock returns is all "
              "zero until the epoch reopens",
              static_cast<uint64_t>(nonzero), 0);
    long pre_epoch_seen = 0;
    for (const DecodedFrame& fr : decoded)
        for (int k = 0; k < kSlots; k++)
            if (fr.slot[static_cast<size_t>(k)] != 0 &&
                fr.slot[static_cast<size_t>(k)] == pre_epoch[static_cast<size_t>(k)])
                ++pre_epoch_seen;
    check.dec("T18 RESET: no pre-reset sample survives the stopped-clock reset",
              static_cast<uint64_t>(pre_epoch_seen), 0);
    //! EXACTLY ONE. One epoch event is one round trip and one counted
    //! reopening: a lane that re-requested at its own reopening would still
    //! satisfy "the counter advanced", and that is the defect this equality
    //! exists to refuse.
    check.dec("T18 RESET: the reset epoch reopened EXACTLY once", lane_epochs(),
              epochs_before + 1);
    std::printf("  [i]    epochs %llu -> %llu across the stopped-clock reset\n",
                static_cast<unsigned long long>(epochs_before),
                static_cast<unsigned long long>(lane_epochs()));
    check.dec("T18 RESET: the FIFO write side admitted nothing before the "
              "round trip completed", static_cast<uint64_t>(lane_over()), 0);

    // T21: the commits the running feed placed before, during and after the
    // release may not be ADMITTED from a closed epoch. Counted at the frame
    // commit strobe over the DUT's own window - the release to the counted
    // reopening - so the claim is about the gate and not about whether the
    // frames would have carried audible samples.
    check.that("T21 COMMIT AROUND RELEASE: the window really closed on a "
               "counted reopening, so it is a window", commit_watch_closed);
    check.that("T21 COMMIT AROUND RELEASE: the crossbar offered the adapter a "
               "walk inside that window, so a zero below is a refusal and not "
               "an absence of work", phys_offers_in_window > 4);
    check.dec("T21 COMMIT AROUND RELEASE: the adapter committed no frame "
              "between the reset release and the epoch reopening",
              static_cast<uint64_t>(commits_before_reopen), 0);
    std::printf("  [i]    T21: %ld crossbar offer(s) and %ld commit(s) between "
                "the reset release and the counted reopening\n",
                phys_offers_in_window, commits_before_reopen);
    check.dec("T21 COMMIT AROUND RELEASE: ...and nothing it might have "
              "committed reached the pins", static_cast<uint64_t>(nonzero), 0);
}

//! T22 and T20: A HARD RESET INTERRUPTS THE FRAME IN FLIGHT, wherever it
//! lands. The distinction from a graceful epoch flush - which completes the
//! frame WHOLE - is what this arm carries, and both placements C2's validation
//! list names are exercised: one inside the frame and one ON the wrap. Graded
//! from the PINS: the interval after the release is invalid, it is bounded by
//! one frame, the boundary that ends it carries the frame cadence back, and
//! what follows is digital silence rather than stale audio.
void TdmRenderHarness::prove_a_hard_reset_interrupts_and_rearms(
        const char* tag, bool at_frame_wrap) {
    char what[200];
    if (at_frame_wrap) {
        //! land the reset ON the wrap: step to the fsync rise the PINS show
        //! and assert immediately, so the frame it interrupts is the one that
        //! has just begun
        int prev = dut->tdm_fsync_o;
        for (int c = 0; c < 40000; c++) {
            step();
            const int f = dut->tdm_fsync_o;
            if (f && !prev) break;
            prev = f;
        }
        //! ...and then on to the RISE that pulse marks. Since #452 fsync is
        //! launched on the bclk fall, half a bit period AHEAD of the rise a
        //! receiver reads it on, so the pin transition above is not yet the
        //! frame boundary - the rise the decoder counts as the wrap is the
        //! next one, and landing the reset between the two would place it 255
        //! rises into the PREVIOUS frame rather than on the wrap.
        for (int c = 0; c < 40000 && rises != rises_at_last_fsync; c++) step();
    } else {
        steps(8);
    }
    const long into = (rises_at_last_fsync >= 0) ? rises - rises_at_last_fsync
                                                 : -1;
    dut->axis_resetn = 0;
    steps(600);
    dut->axis_resetn = 1;
    decoder_reset();
    collect = true;
    steps(12000);
    collect = false;
    std::snprintf(what, sizeof what,
                  "%s HARD RESET: the reset landed where this arm placed it "
                  "(%s)", tag, at_frame_wrap ? "on the frame wrap"
                                             : "inside the frame");
    check.that(what, at_frame_wrap ? (into >= 0 && into <= 4)
                                   : (into > 4 && into < kFrameBclks));
    //! THE BOUND IS ONE FRAME PLUS ONE RISE (#452). bclk parks LOW and fsync
    //! parks HIGH across the reset, so the first rise after the release
    //! carries the first frame's sync as a LEVEL the decoder was reset into
    //! rather than as an edge - and a level is never an edge here, the same
    //! rule the slave suite's armed detector has always applied to a 50%-duty
    //! frame sync. The decoder therefore arms on the fall that follows that
    //! rise and takes the NEXT frame's edge, one whole frame and that one rise
    //! after the release. A decoder that never re-armed, or a bus whose
    //! cadence did not come back, still fails this.
    std::snprintf(what, sizeof what,
                  "%s HARD RESET: a fresh frame boundary ends the interrupted "
                  "interval, and it comes within one frame of bclk plus the "
                  "rise the reset-parked level spans", tag);
    check.that(what, rises_at_first_fsync >= 0
                     && rises_at_first_fsync <= kFrameBclks + 1);
    std::snprintf(what, sizeof what,
                  "%s HARD RESET: the frame cadence after the release is 256 "
                  "bclk rises again, from the pins alone", tag);
    check.that(what, fsync_rises >= 3 && gap_faults == 0
                     && framing_faults == 0);
    long nonzero = 0;
    for (const DecodedFrame& fr : decoded)
        for (int k = 0; k < kSlots; k++)
            if (fr.slot[static_cast<size_t>(k)] != 0) ++nonzero;
    std::snprintf(what, sizeof what,
                  "%s HARD RESET: every frame decoded after that boundary is "
                  "digital silence, not the interrupted frame's audio", tag);
    check.dec(what, static_cast<uint64_t>(nonzero), 0);
    std::printf("  [i]    %s: the reset landed %ld bclk rise(s) into the "
                "frame; the decoder re-armed, saw its first boundary %ld bclk "
                "rise(s) later and %ld in all, and decoded %zu frame(s)\n",
                tag, into, rises_at_first_fsync, fsync_rises, decoded.size());
}

//! T19: A RESET WHILE THE ROUND TRIP IS OUTSTANDING (C2's validation list).
//! The serial clock is stopped first, so the round trip the first reset
//! starts CANNOT complete; the second reset then lands inside it. What the
//! lane owes afterwards is one epoch, not two, and no commit before it.
void TdmRenderHarness::prove_a_reset_inside_an_outstanding_round_trip() {
    tdm_frozen = true;
    steps(200);
    const uint64_t epochs_before = lane_epochs();
    dut->axis_resetn = 0;
    steps(300);
    dut->axis_resetn = 1;
    steps(300);
    //! the round trip is outstanding and cannot be acknowledged: the serial
    //! clock is stopped, so the counter cannot move. Asserted, not assumed.
    check.dec("T19 RESET IN FLIGHT: the first round trip is still outstanding "
              "with the serial clock stopped", lane_epochs(), epochs_before);
    dut->axis_resetn = 0;
    steps(300);
    dut->axis_resetn = 1;
    //! the counter export's clk_i side is zeroed by rst_n and re-synchronises
    //! from the serial side, which never saw either reset; the watch is armed
    //! after that, so its window closes on the REOPENING and not on a
    //! resynchronising counter
    steps(400);
    check.dec("T19 RESET IN FLIGHT: ...and still outstanding after the second "
              "reset lands inside it", lane_epochs(), epochs_before);
    arm_the_commit_watch();
    steps(2 * static_cast<long>(kPduPeriodCycles));
    tdm_frozen = false;
    steps(20000);
    check.dec("T19 RESET IN FLIGHT: the two nested resets reopened the epoch "
              "EXACTLY once", lane_epochs(), epochs_before + 1);
    check.that("T19 RESET IN FLIGHT: the crossbar offered the adapter a walk "
               "while that round trip was outstanding",
               phys_offers_in_window > 4);
    check.dec("T19 RESET IN FLIGHT: no frame was committed before that "
              "reopening", static_cast<uint64_t>(commits_before_reopen), 0);
    check.dec("T19 RESET IN FLIGHT: and none was admitted into a full CDC "
              "either", static_cast<uint64_t>(lane_over()), 0);
    std::printf("  [i]    T19: %ld crossbar offer(s) and %ld commit(s) while "
                "the round trip was outstanding; epochs %llu -> %llu\n",
                phys_offers_in_window, commits_before_reopen,
                static_cast<unsigned long long>(epochs_before),
                static_cast<unsigned long long>(lane_epochs()));
}

//! ...and the lane comes back: rebind, remap, and the first nonzero frame is a
//! POST-reset injected event.
void TdmRenderHarness::prove_the_lane_recovers_after_a_reset() {
    // ...and the lane comes back: rebind, remap, and the first nonzero frame
    // is a post-reset injected event.
    const uint64_t epochs_before = lane_epochs();
    bind_listener_zero();
    route_reset();
    std::vector<std::pair<int, int>> rows;
    for (int co = 0; co < kSlots; co++)
        rows.emplace_back(kPerm[static_cast<size_t>(co)], co);
    check.dec("T18 RECOVERY: the map is programmable again after the reset",
              static_cast<uint64_t>(map_cmd(kCmdAddMappings, rows)), 0);
    build_injection_record(200);
    feed_on = true;
    next_pdu_at = axis_cycle + 64;
    run_fed(60 * kPduPeriodCycles);
    decoder_reset();
    collect = true;
    run_fed(40 * kPduPeriodCycles);
    collect = false;
    const long recovered =
        decoded.empty() ? -1 : find_the_ordinal(decoded.front());
    check.that("T18 RECOVERY: complete fresh frames decode after the epoch "
               "reopens", recovered >= 0);
    //! a rebind and a remap are not epoch events - only a bind FALL on a
    //! stream this lane renders is - so the recovery reopens nothing
    check.dec("T18 RECOVERY: the rebind and remap counted no further "
              "reopening", lane_epochs(), epochs_before);
    feed_on = false;
}

void TdmRenderHarness::phase_bind_loss() {
    std::printf("\n[BIND] the render epoch over a bind loss and a rebind\n");
    // A distinct sample epoch before the loss, so a surviving sample is
    // recognisable rather than merely plausible.
    build_injection_record(400);
    feed_on = true;
    next_pdu_at = axis_cycle + 64;
    run_fed(60 * kPduPeriodCycles);
    decoder_reset();
    collect = true;
    run_fed(20 * kPduPeriodCycles);
    collect = false;
    check.that("T23 WARM: the lane carried pre-loss audio", !decoded.empty());
    std::vector<std::array<uint32_t, kSlots>> pre_loss;
    for (const DecodedFrame& fr : decoded) pre_loss.push_back(fr.slot);
    const uint64_t epochs_before = lane_epochs();
    const long events_at_loss = injected_events;

    // THE WINDOW OPENS BEFORE THE BIND FALLS, so it STRADDLES the flush: the
    // last frame the pins carry and the first silent one are both inside it.
    // Opening it after the disconnect (as this arm used to) leaves the
    // boundary outside the window, and the flush boundary is then ungraded -
    // which is what T27 below grades. The loss and silence checks are
    // unaffected: they skip every frame before the first all-zero one.
    decoder_reset();
    collect = true;
    run_fed(4 * kPduPeriodCycles);
    // Drop the bind with every mapping in place, and WITHOUT resetting.
    acmp_disconnect_rx(0x2233);
    steps(40000);
    collect = false;
    feed_on = false;
    long carried = 0;
    long frames_after_boundary = 0;
    bool boundary_passed = false;
    for (const DecodedFrame& fr : decoded) {
        bool all_zero = true;
        for (int k = 0; k < kSlots; k++)
            if (fr.slot[static_cast<size_t>(k)] != 0) all_zero = false;
        if (all_zero) { boundary_passed = true; }
        if (!boundary_passed) continue;
        ++frames_after_boundary;
        if (all_zero) continue;
        for (const auto& old : pre_loss)
            for (int k = 0; k < kSlots; k++)
                if (fr.slot[static_cast<size_t>(k)] != 0 &&
                    fr.slot[static_cast<size_t>(k)] == old[static_cast<size_t>(k)])
                    ++carried;
    }
    check.that("T23 BIND LOSS: the lane reached digital silence after the "
               "boundary", boundary_passed);
    check.dec("T23 BIND LOSS: no frame after the boundary carries a pre-loss "
              "sample in any slot", static_cast<uint64_t>(carried), 0);
    //! ONE bind fall, ONE reopening. The serial side reopens as soon as the
    //! request clears - the audio waits for freshness, the reopening does not
    //! - so the count is exact by the time this window has run.
    check.dec("T23 BIND LOSS: the one bind fall reopened the epoch EXACTLY "
              "once", lane_epochs(), epochs_before + 1);
    check.dec("T23 BIND LOSS: the adapter commit gate is closed while the "
              "epoch is",
              static_cast<uint64_t>(dut->rootp->milan_datapath__DOT__tdmr_commit_en_w),
              0);
    prove_the_graceful_flush_left_the_frame_in_flight_whole();

    prove_a_rebind_carries_only_post_rebind_audio(epochs_before, events_at_loss);
}

//! T27: THE GRACEFUL FLUSH BOUNDARY ITSELF, which the loss and silence checks
//! above cannot see. They classify each decoded frame as all-zero or not and
//! skip everything before the first all-zero one, so a frame that is part
//! pre-loss audio and part zeros - the artifact a flush that cut the frame in
//! flight would put on the wire - is neither counted nor failed by them.
//!
//! The contract the module banner and docs/CHANNEL_MAP_64.md 3.1 state is that
//! a HARD RESET interrupts the frame in flight while the GRACEFUL FLUSH zeroes
//! the active frame at FRAME STARTS ONLY, so the last frame the pins carry
//! before digital silence completes WHOLE. This arm grades exactly that, from
//! the pins and the immutable injection record: the frame immediately before
//! the boundary must carry audio in EVERY routed slot and all of those slots
//! must hold ONE media event's identity. A flush that zeroed the active frame
//! off a frame start leaves the slots after the cut at zero, so that frame
//! matches no ordinal at all and this fails by name. The hard reset's own
//! interrupted interval is T20's and T22's and is deliberately untouched here.
void TdmRenderHarness::prove_the_graceful_flush_left_the_frame_in_flight_whole() {
    const int routed = routed_slots();
    check.that("T27 FLUSH BOUNDARY: the window is graded over a non-empty "
               "route, so a whole frame is a claim about real slots",
               routed > 0);
    //! the boundary is the FIRST all-zero frame: the flush reached the
    //! serializer there, and the frame before it is the last one on the wire
    long boundary = -1;
    for (size_t i = 0; i < decoded.size() && boundary < 0; i++) {
        bool all_zero = true;
        for (int k = 0; k < kSlots; k++)
            if (decoded[i].slot[static_cast<size_t>(k)] != 0) all_zero = false;
        if (all_zero) boundary = static_cast<long>(i);
    }
    const bool graded = check.that("T27 FLUSH BOUNDARY: the window holds audio "
                                   "and then digital silence, so there IS a "
                                   "last non-silent frame", boundary > 0);
    if (!graded || routed <= 0) return;

    const DecodedFrame& last = decoded[static_cast<size_t>(boundary) - 1];
    long torn_slots = 0;
    for (int k = 0; k < kSlots; k++)
        if (route[static_cast<size_t>(k)] >= 0 &&
            last.slot[static_cast<size_t>(k)] == 0) ++torn_slots;
    check.dec("T27 FLUSH BOUNDARY: the last frame before digital silence is a "
              "COMPLETE frame - no routed slot was zeroed by the flush",
              static_cast<uint64_t>(torn_slots), 0);
    const long ordinal = find_the_ordinal(last);
    check.that("T27 FLUSH BOUNDARY: ...and every routed slot of it carries ONE "
               "media event's identity", ordinal >= 0);
    std::printf("  [i]    T27: boundary at decoded frame %ld of %zu; the last "
                "non-silent frame is ordinal %ld with %d routed slot(s), %ld "
                "of them zeroed\n", boundary, decoded.size(), ordinal, routed,
                torn_slots);
}

//! T26 and T23: a map write inside the CLOSED epoch may not reach a slot, and
//! the first nonzero frame after the rebind must be a POST-rebind event routed
//! by the NEW map.
void TdmRenderHarness::prove_a_rebind_carries_only_post_rebind_audio(
        uint64_t epochs_before, long events_at_loss) {
    // T26: rewrite the map while the bind is down. The re-seeded crossbar
    // value must not reach a slot, and the first nonzero frame after the
    // rebind must be a POST-rebind event routed by the NEW map.
    std::vector<std::pair<int, int>> newrows;
    for (int co = 0; co < kSlots; co++)
        newrows.emplace_back((kPerm[static_cast<size_t>(co)] + 1) % kChans, co);
    map_cmd(kCmdAddMappings, newrows);
    decoder_reset();
    collect = true;
    steps(20000);
    collect = false;
    long leaked = 0;
    for (const DecodedFrame& fr : decoded)
        for (int k = 0; k < kSlots; k++)
            if (fr.slot[static_cast<size_t>(k)] != 0) ++leaked;
    check.dec("T26 MAP WRITE IN A CLOSED EPOCH: the re-seeded crossbar value "
              "never reaches a slot", static_cast<uint64_t>(leaked), 0);

    // Restore the bind and a disjoint injection epoch.
    run_the_bind_ladder(0, 0, 0x3344, "T23 REBIND");
    build_injection_record(200);
    injected_events = 0;
    feed_on = true;
    next_pdu_at = axis_cycle + 64;
    run_fed(60 * kPduPeriodCycles);
    decoder_reset();
    collect = true;
    run_fed(40 * kPduPeriodCycles);
    collect = false;
    check.that("T23 REBIND: the lane serializes again after the rebind",
               !decoded.empty());
    const long post = decoded.empty() ? -1 : find_the_ordinal(decoded.front());
    check.that("T23 REBIND: the first nonzero frame after the rebind is a "
               "post-rebind injected event routed by the NEW map", post >= 0);
    if (post >= 0) {
        const Grade g = grade_frames(post, "T23");
        check.dec("T23 REBIND: identity and order hold after the rebind",
                  static_cast<uint64_t>(g.identity_failures), 0);
        check.dec("T23 REBIND: every repeat is still a counted underrun",
                  static_cast<uint64_t>(g.uncounted_repeats), 0);
        check.dec("T23 REBIND: every skipped event is still covered by a "
                  "counted skip", static_cast<uint64_t>(g.uncounted_skips), 0);
    }
    check.dec("T28 EPOCHS: the loss and its recovery counted EXACTLY one "
              "reopening between them", lane_epochs(), epochs_before + 1);
    std::printf("  [i]    events injected before the loss: %ld; epochs %llu -> "
                "%llu\n", events_at_loss,
                static_cast<unsigned long long>(epochs_before),
                static_cast<unsigned long long>(lane_epochs()));
    feed_on = false;
    prove_two_bind_falls_in_one_round_trip_count_twice();
}

//! T25: TWO BIND FALLS INSIDE ONE ROUND TRIP ARE TWO COUNTED REOPENINGS.
//! The serial clock is held, so the round trip the first fall starts cannot
//! be acknowledged and everything below happens INSIDE it - which is asserted
//! from the counter rather than assumed. A producer that raised its request
//! straight onto the outstanding handshake would have the second fall cleared
//! by the first one's acknowledgement and count one reopening for two events.
void TdmRenderHarness::prove_two_bind_falls_in_one_round_trip_count_twice() {
    const uint64_t epochs_before = lane_epochs();
    tdm_frozen = true;
    steps(200);
    acmp_disconnect_rx(0x2266);                     // the first bind fall
    steps(2000);
    check.dec("T25 DOUBLE EVENT: the first fall's round trip is outstanding "
              "with the serial clock stopped", lane_epochs(), epochs_before);
    check.dec("T25 DOUBLE EVENT: ...and it closed the adapter's commit gate",
              static_cast<uint64_t>(
                  dut->rootp->milan_datapath__DOT__tdmr_commit_en_w), 0);
    run_the_bind_ladder(0, 0, 0x4455, "T25 REBIND");
    acmp_disconnect_rx(0x2277);                     // the second, inside it
    steps(2000);
    check.dec("T25 DOUBLE EVENT: the second bind fall landed inside the same "
              "round trip", lane_epochs(), epochs_before);
    tdm_frozen = false;
    steps(30000);
    check.dec("T25 DOUBLE EVENT: two bind falls inside one round trip are TWO "
              "counted reopenings, not one", lane_epochs(), epochs_before + 2);
    std::printf("  [i]    T25: epochs %llu -> %llu across two bind falls "
                "inside one round trip\n",
                static_cast<unsigned long long>(epochs_before),
                static_cast<unsigned long long>(lane_epochs()));
}

// ====================================================================== //
//  [CRF] the clock source, changed under the running stream               //
// ====================================================================== //

//! One decoded window, graded by the SAME instrument whichever clock source
//! is selected, so the INTERNAL and CRF numbers are comparable rather than
//! merely both printed.
TdmRenderHarness::Window TdmRenderHarness::decode_and_grade_a_window(
        long cycles, const char* tag) {
    Window w;
    decoder_reset();
    taps_reset();
    const uint64_t skips0 = lane_skips();
    const uint64_t unders0 = lane_unders();
    const uint64_t epochs0 = lane_epochs();
    collect = true;
    run_fed(cycles);
    collect = false;
    w.skips = lane_skips() - skips0;
    w.unders = lane_unders() - unders0;
    w.epochs = lane_epochs() - epochs0;
    if (decoded.empty()) return w;
    const DecodedFrame& f0 = decoded.front();
    w.start = find_the_ordinal(f0);
    w.g = grade_frames(w.start >= 0 ? w.start : 0, tag);
    // ...and the commit-to-pin interval over the same frames, seated on the
    // CDC floor and walked by the grading's own advances
    long cursor = seat_the_commit_cursor(f0.half_step);
    w.phi_min = 1 << 30;
    w.phi_max = -(1 << 30);
    //! phi is bounded by one serial frame BY CONSTRUCTION - the frame is
    //! adopted at the first frame start the CDC floor allows - so when the
    //! walk reaches a frame boundary the measurement steps by exactly one
    //! frame and the adoption moves to the neighbouring frame start. That
    //! step is the BEAT, not a discontinuity in the underlying rate, so the
    //! sequence is unwrapped before the rate is taken. Without it a window
    //! that happens to straddle a beat reports a rate of thousands of ppm.
    long unwrap = 0;
    long prev = 0;
    for (size_t i = 0; i < decoded.size() && i < w.g.advances.size(); i++) {
        cursor += w.g.advances[i];
        if (cursor < 0 || cursor >= static_cast<long>(commit_cycle.size()))
            continue;
        const double pin_axis =
            static_cast<double>(decoded[i].half_step) * kAxisPerHalf;
        const long d = static_cast<long>(pin_axis)
                     - commit_cycle[static_cast<size_t>(cursor)];
        if (d < 0 || d > 8000) continue;
        if (d < w.phi_min) w.phi_min = d;
        if (d > w.phi_max) w.phi_max = d;
        if (w.phi_n > 0) {
            while (d + unwrap - prev > static_cast<long>(kFrameAxis / 2.0))
                unwrap -= static_cast<long>(kFrameAxis);
            while (d + unwrap - prev < -static_cast<long>(kFrameAxis / 2.0))
                unwrap += static_cast<long>(kFrameAxis);
        }
        prev = d + unwrap;
        if (w.phi_n == 0) { w.phi_first = prev; w.t_first = static_cast<long>(pin_axis); }
        w.phi_last = prev;
        w.t_last = static_cast<long>(pin_axis);
        ++w.phi_n;
    }
    //! a window that correlated nothing reports zeros rather than the
    //! sentinels, so the printed record cannot be read as a measurement; the
    //! arms that need one check `phi_n` themselves
    if (w.phi_n == 0) { w.phi_min = 0; w.phi_max = 0; }
    // THE WALK, in ppm of the harness clock. phi is the wait from a frame's
    // commit to its slot-0 sampling edge, so a commit grid that runs FASTER
    // than the frame grid lengthens the wait by exactly their rate
    // difference: this number IS the two grids' relative rate, measured at
    // the pins, with no model in it.
    if (w.phi_n > 2 && w.t_last > w.t_first)
        w.walk_ppm = 1e6 * static_cast<double>(w.phi_last - w.phi_first)
                   / static_cast<double>(w.t_last - w.t_first);
    return w;
}

void TdmRenderHarness::report_a_window(const Window& w, const char* tag) {
    std::printf("  [i]    %s: %ld frames decoded from ordinal %ld, %ld "
                "repeat(s), %ld skipped event(s); lane deltas skips %llu "
                "underruns %llu epochs %llu; commit-to-pin %ld..%ld axis "
                "cycles (%.3f..%.3f us) over %ld frames, spread %ld of one "
                "frame = %.0f\n",
                tag, w.g.frames, w.start, w.g.repeats, w.g.skipped,
                static_cast<unsigned long long>(w.skips),
                static_cast<unsigned long long>(w.unders),
                static_cast<unsigned long long>(w.epochs),
                w.phi_min, w.phi_max, static_cast<double>(w.phi_min) / 100.0,
                static_cast<double>(w.phi_max) / 100.0, w.phi_n,
                w.phi_max - w.phi_min, kFrameAxis);
    //! ...and the walk that spread came from, with the beat period it
    //! implies: one whole frame of phi is one counted skip, so the two grids
    //! cost the lane one media event every frame / (rate x frame rate).
    const double beat_s = (w.walk_ppm == 0.0) ? 0.0
                        : kFrameAxis / (std::fabs(w.walk_ppm) * 1e-6) / 100e6;
    std::printf("  [i]    %s: the commit-to-pin interval WALKS at %+.4f ppm "
                "over %ld axis cycles, which is one whole frame of phi - one "
                "counted skip - every %.4f s\n",
                tag, w.walk_ppm, w.t_last - w.t_first, beat_s);
}

//! SET_CLOCK_SOURCE on CLOCK_DOMAIN 0, over the SAME AECP face this leg's map
//! commands use. This is the production control path, not a poke at the
//! store: the command is parsed, range checked against the model's declared
//! CLOCK_SOURCE count and committed by the processor, and the media plane
//! resolves it. Returns the AEM status.
long TdmRenderHarness::set_clock_source(uint16_t index) {
    const std::vector<uint8_t> pl = {
        0x00, 0x24,                                     // CLOCK_DOMAIN
        0x00, 0x00,                                     // descriptor index 0
        static_cast<uint8_t>(index >> 8), static_cast<uint8_t>(index),
        0x00, 0x00};
    const auto r = aecp_xact(0x0016, pl);
    steps(16);
    return aecp_status(r);
}

//! ...and GET_CLOCK_SOURCE, so the selection is read back over the same face
//! rather than only observed inside the fabric. Returns the index, or -1.
long TdmRenderHarness::get_clock_source() {
    const std::vector<uint8_t> pl = {0x00, 0x24, 0x00, 0x00};
    const auto r = aecp_xact(0x0017, pl);
    if (aecp_status(r) != 0 || r.size() < 46) return -1;
    return (static_cast<long>(r[42]) << 8) | r[43];
}

//! The CRF Media Clock Input sink, provisioned over the CSR pair exactly as
//! the shipping bench lever does. The station MAC is deliberately NOT touched
//! here: this leg addresses AECP to the station's own reset-zero unicast
//! address (see bind_listener_zero), the CRF sink keys on STREAM ID alone,
//! and the CRF PDUs arrive on a multicast stream address the RX filter
//! already passes.
void TdmRenderHarness::provision_the_crf_sink() {
    constexpr uint16_t kCrfCtrl = 0x738;
    constexpr uint16_t kCrfSidLo = 0x73C;
    constexpr uint16_t kCrfSidHi = 0x740;
    dut->i_mmcm_locked = 1;
    axi_write(kCrfSidLo, 0x00020001);
    axi_write(kCrfSidHi, 0x02000000);
    axi_write(kCrfCtrl, 0x1);
    crf_next_at = axis_cycle;
    crf_on = true;
    run_fed(2000000);                       // 8 clean PDUs at the 2 ms cadence
    check.dec("T30 CRF: the Media Clock Input sink locked on the fed stream",
              static_cast<uint64_t>(axi_read(kCrfCtrl) >> 31), 1);
}

//! The LIVE transition: the AAF stream never stops, so the stage sees exactly
//! the sub-tick phase step a moved grid shows it, which is the case a
//! restarted feed never reaches.
void TdmRenderHarness::select_crf_under_the_running_stream() {
    const uint16_t ix = defect_internal_select ? 0 : kCrfClksrcIx;
    if (defect_internal_select)
        std::printf("  [i]    DEFECT ARM: the selection names INTERNAL, not "
                    "this shape's CRF source\n");
    check.dec("T30 CRF: SET_CLOCK_SOURCE(CRF) over the real AECP face answers "
              "SUCCESS", static_cast<uint64_t>(set_clock_source(ix)), 0);
    check.dec("T30 CRF: GET_CLOCK_SOURCE reads the CRF index back",
              static_cast<uint64_t>(get_clock_source()), kCrfClksrcIx);
    check.dec("T30 CRF: the media plane's one registered resolve reads CRF",
              static_cast<uint64_t>(
                  dut->rootp->milan_datapath__DOT__crf_clk_selected_r), 1);
    check.dec("T30 CRF: the NCO servo gate rose with it",
              static_cast<uint64_t>(
                  dut->rootp->milan_datapath__DOT__mnco_servo_en_w), 1);
    //! from here the talker's cadence is the PHYSICAL grid's, the one the
    //! packet grid is about to be held on
    pdu_frac_num = kPduPhysFracNum;
    pdu_frac_acc = 0;
}

//! THE CONTRAST THAT MAKES THE CRF WINDOW EVIDENCE. The construction contract
//! states the aligned state exactly: at INTERNAL the producer leads the frame
//! grid by the divider plan and each beat costs one counted skip, and under
//! CRF the grids are held together so both counters stay at ZERO. The
//! commit-to-pin interval says the same thing the other way: free-running it
//! sweeps a whole frame, aligned it stops sweeping.
void TdmRenderHarness::prove_the_aligned_window_is_the_acceptance_state(
        const Window& intr, const Window& crf) {
    check.dec("T30 CRF: every decoded frame under CRF is a complete 24-bit "
              "match against the injection record",
              static_cast<uint64_t>(crf.g.identity_failures), 0);
    check.dec("T30 CRF: the eight pad bits of every slot are zero under CRF",
              static_cast<uint64_t>(crf.g.pad_failures), 0);
    check.dec("T30 CRF: each slot's channel field is its routed source under "
              "CRF", static_cast<uint64_t>(crf.g.channel_field_failures), 0);
    check.dec("T30 CRF: the eight slots carry one media event's identity under "
              "CRF", static_cast<uint64_t>(crf.g.coherence_failures), 0);
    check.dec("T30 CRF: the eight slots are distinct samples under CRF",
              static_cast<uint64_t>(crf.g.distinct_failures), 0);
    check.dec("T30 CRF: every repeat is a counted underrun under CRF",
              static_cast<uint64_t>(crf.g.uncounted_repeats), 0);
    check.dec("T30 CRF: every skipped event is covered by a counted skip under "
              "CRF", static_cast<uint64_t>(crf.g.uncounted_skips), 0);
    check.that("T30 CRF: the aligned window decoded whole frames",
               crf.g.frames > 200 && crf.start >= 0);
    // the acceptance state itself
    check.dec("T30 CRF ALIGNED: the aligned window costs the lane NO counted "
              "skip", crf.skips, 0);
    check.dec("T30 CRF ALIGNED: ...and NO underrun",  crf.unders, 0);
    check.dec("T30 CRF ALIGNED: a clock-source change is not a bind fall, so "
              "no render epoch closed", crf.epochs, 0);
    check.dec("T30 CRF ALIGNED: the align loop is engaged on the physical "
              "frame marker",
              static_cast<uint64_t>(
                  dut->rootp->milan_datapath__DOT__mga_engaged_w), 1);
    // THE DISCRIMINATION, and why it is a RATE and not a skip count. The
    // divider plan's surplus is one counted skip per 1.9582 s BEAT PERIOD, and
    // a window that long is not affordable here - so what separates the two
    // states inside a 37 ms window is the WALK the skip eventually comes from.
    // At INTERNAL the commit grid (the NCO's exact 48 kHz) leads the frame
    // grid (clk_tdm / 512 = 47,999.4893 Hz) by the plan's +10.6393 ppm and phi
    // lengthens at exactly that rate; under CRF the aligner holds the packet
    // grid ON the physical one and the walk stops. Both are measured at the
    // pins, in the same window length, by the same instrument.
    //! the closed form: commits arrive every kTickCycles and frames start
    //! every kFrameAxis, so each commit waits (kFrameAxis - kTickCycles)
    //! longer than the one before it - the divider plan's 10.6393 ppm, with
    //! the sign phi walks in.
    const double plan_ppm = 1e6 * (kFrameAxis - kTickCycles) / kTickCycles;
    check.that("T30 INTERNAL: the free-running commit-to-pin interval walks, "
               "and at the divider plan's own rate",
               intr.phi_n > 200 &&
               std::fabs(intr.walk_ppm - plan_ppm) < 2.0);
    check.that("T30 CRF ALIGNED: the walk STOPPED once the grids were held "
               "together, which is what the aligner buys the lane",
               crf.phi_n > 200 && std::fabs(crf.walk_ppm) < 2.0);
    check.that("T30 CRF ALIGNED: ...and the two rates are a real separation, "
               "not two numbers inside one band",
               std::fabs(intr.walk_ppm - crf.walk_ppm) > 4.0);
    std::printf("  [i]    T30: the divider plan's closed form is %+.4f ppm; "
                "measured %+.4f ppm at INTERNAL and %+.4f ppm under CRF\n",
                plan_ppm, intr.walk_ppm, crf.walk_ppm);
}

//! #386's law, measured in THIS run rather than cited from another: the fill
//! at accept is the 8-event setpoint and the first event's delay is inside
//! (SETPOINT, SETPOINT + 1] media ticks.
void TdmRenderHarness::prove_the_setpoint_law_still_holds(long first_id,
                                                          long last_id,
                                                          const char* tag) {
    const double lo = kRenderSetpointEvt * kTickCycles;
    const double hi = (kRenderSetpointEvt + 1) * kTickCycles
                    + static_cast<double>(kBandSlackCycles);
    long n = 0;
    long in_band = 0;
    long fill_ok = 0;
    long dmin = 0;
    long dmax = 0;
    for (long id = first_id; id < last_id && id < static_cast<long>(kIdSpace);
         id++) {
        const size_t i = static_cast<size_t>(id);
        if (accept_at[i] < 0 || pop_at[i] < 0) continue;
        const long d = pop_at[i] - accept_at[i];
        if (n == 0 || d < dmin) dmin = d;
        if (n == 0 || d > dmax) dmax = d;
        if (static_cast<double>(d) > lo && static_cast<double>(d) <= hi)
            ++in_band;
        if (fill_at[i] == kRenderSetpointEvt) ++fill_ok;
        ++n;
    }
    std::printf("  [i]    %s: %ld PDUs, first-event delay %ld..%ld cycles = "
                "%.3f..%.3f media ticks; the law is %d < d/T <= %d (+%ld "
                "cycles of registration slack)\n",
                tag, n, dmin, dmax, static_cast<double>(dmin) / kTickCycles,
                static_cast<double>(dmax) / kTickCycles, kRenderSetpointEvt,
                kRenderSetpointEvt + 1, kBandSlackCycles);
    char what[160];
    std::snprintf(what, sizeof what,
                  "%s: PDUs measured for the #386 law in this window", tag);
    check.that(what, n >= 100);
    std::snprintf(what, sizeof what,
                  "%s: the fill at accept is the 8-event setpoint for every "
                  "PDU", tag);
    check.dec(what, static_cast<uint64_t>(fill_ok), static_cast<uint64_t>(n));
    std::snprintf(what, sizeof what,
                  "%s: every PDU's first event is inside the law band", tag);
    check.dec(what, static_cast<uint64_t>(in_band), static_cast<uint64_t>(n));
}

//! ...and the transition the OTHER way, still under the running stream. The
//! deselect is the same law: one settled-grid recentre, and the lane keeps
//! rendering the record.
void TdmRenderHarness::deselect_back_to_internal(uint64_t epochs_before) {
    const long src0 = src_recentre_pulses;
    const uint32_t rc0 = dut->rootp->milan_datapath__DOT__rsp_recentres_w;
    check.dec("T31 DESELECT: SET_CLOCK_SOURCE(INTERNAL) answers SUCCESS",
              static_cast<uint64_t>(set_clock_source(0)), 0);
    check.dec("T31 DESELECT: the registered resolve falls back to INTERNAL",
              static_cast<uint64_t>(
                  dut->rootp->milan_datapath__DOT__crf_clk_selected_r), 0);
    pdu_frac_num = 0;
    pdu_frac_acc = 0;
    crf_on = false;
    //! the dwell at INTERNAL is the same 2048 media ticks from the change
    run_fed(6000000);
    check.dec("T31 DESELECT: the deselect fired the settled-grid trigger ONCE",
              static_cast<uint64_t>(src_recentre_pulses - src0), 1);
    check.dec("T31 DESELECT: ...and the stage executed exactly one recentre",
              static_cast<uint64_t>(
                  dut->rootp->milan_datapath__DOT__rsp_recentres_w - rc0), 1);
    const Window back = decode_and_grade_a_window(40 * kPduPeriodCycles,
                                                  "T31");
    report_a_window(back, "T31 back at INTERNAL");
    check.that("T31 DESELECT: the lane is still serializing the record after "
               "the deselect", back.start >= 0 && back.g.frames > 100);
    check.dec("T31 DESELECT: identity holds across the second live transition",
              static_cast<uint64_t>(back.g.identity_failures), 0);
    check.dec("T31 DESELECT: no render epoch closed across either transition",
              lane_epochs(), epochs_before);
}

void TdmRenderHarness::phase_crf() {
    std::printf("\n[CRF] the CRF clock source selected under the running "
                "stream, and the same pins decoded again\n");
    build_injection_record(2400);
    feed_on = true;
    pdu_frac_num = 0;
    pdu_frac_acc = 0;
    next_pdu_at = axis_cycle + 64;
    run_fed(40 * kPduPeriodCycles);         // prefill, lock, epoch admission
    const uint64_t epochs_before = lane_epochs();

    // the FREE-RUNNING reference, on the same pins and the same oracle
    const long int_first = injected_events / kEvents;
    const Window intr = decode_and_grade_a_window(300 * kPduPeriodCycles,
                                                  "T30 INTERNAL");
    report_a_window(intr, "T30 INTERNAL");
    prove_the_setpoint_law_still_holds(int_first + 4,
                                       injected_events / kEvents - 4,
                                       "T30 INTERNAL LAW");

    provision_the_crf_sink();
    const long src0 = src_recentre_pulses;
    const long pulses0 = recentre_pulses;
    const uint32_t rc0 = dut->rootp->milan_datapath__DOT__rsp_recentres_w;
    select_crf_under_the_running_stream();
    //! the aligner engages within a frame and its error rests inside the
    //! trigger's band once the proportional peak has passed; the dwell is
    //! 2048 media ticks (43 ms), so 12 M cycles cover the pull-in
    run_fed(12000000);
    check.dec("T30 CRF: the selection under the running stream fired the "
              "settled-grid trigger ONCE",
              static_cast<uint64_t>(src_recentre_pulses - src0), 1);
    check.dec("T30 CRF: ...as exactly one render recentre pulse",
              static_cast<uint64_t>(recentre_pulses - pulses0), 1);
    check.dec("T30 CRF: ...and the stage executed exactly one recentre",
              static_cast<uint64_t>(
                  dut->rootp->milan_datapath__DOT__rsp_recentres_w - rc0), 1);

    const long crf_first = injected_events / kEvents;
    const Window crf = decode_and_grade_a_window(300 * kPduPeriodCycles,
                                                 "T30 CRF");
    report_a_window(crf, "T30 CRF aligned");
    prove_the_aligned_window_is_the_acceptance_state(intr, crf);
    prove_the_setpoint_law_still_holds(crf_first + 4,
                                       injected_events / kEvents - 4,
                                       "T30 CRF LAW");
    check.dec("T30 CRF: no second recentre followed the settled one",
              static_cast<uint64_t>(src_recentre_pulses - src0), 1);

    deselect_back_to_internal(epochs_before);
    //! ...and the margin the whole phase stands on, checked rather than
    //! assumed: a feed that ran out of record would decode repeats and every
    //! window above would be grading a stream that had stopped.
    std::printf("  [i]    T31: %ld of the record's %zu events were injected\n",
                injected_events, inj.size());
    check.that("T31: the injection record OUTLASTED the phase, so no window "
               "graded a feed that had stopped",
               static_cast<size_t>(injected_events) + kEvents <= inj.size());
    feed_on = false;
}

// ====================================================================== //
//  [MULTI] the stream-qualified render epoch, and the legal cluster key   //
//  with no pin. Both need a shape with more than one listener stream,     //
//  which is what gen_tdm8r_multi_shape.py writes and this build           //
//  elaborates: STREAM_PORT_INPUT 0's eight clusters are the TDM slots,    //
//  STREAM_PORT_INPUT 1's eight are honestly NONPHYSICAL.                  //
// ====================================================================== //

//! THE QUALIFICATION, half one: a bind fall on a stream this lane does NOT
//! render must leave the lane alone. Graded at the pins and at the gate, and
//! - the part that stops this from passing vacuously - the fall is required
//! to have actually FIRED on that stream.
void TdmRenderHarness::prove_an_unrelated_stream_loss_leaves_the_lane_running() {
    const uint64_t epochs_before = lane_epochs();
    epoch_watch_reset();
    acmp_disconnect_rx(0x2244, 1, 1);
    feed1_on = false;                   // its talker is gone with its bind
    const Window w = decode_and_grade_a_window(60 * kPduPeriodCycles, "M3");
    report_a_window(w, "M3 after the UNRELATED stream's loss");
    check.that("M3 UNRELATED LOSS: the bind fall really fired on stream 1, so "
               "this arm is not passing on an event that never happened",
               (bind_falls_seen & 0x2) != 0);
    check.dec("M3 UNRELATED LOSS: ...and it did NOT fire on stream 0, which "
              "the lane does render",
              static_cast<uint64_t>(bind_falls_seen & 0x1), 0);
    check.dec("M3 UNRELATED LOSS: stream 0 is still bound",
              static_cast<uint64_t>(
                  dut->rootp->milan_datapath__DOT__strtbl_en_w & 0x1), 1);
    check.dec("M3 UNRELATED LOSS: stream 1 is not",
              static_cast<uint64_t>(
                  dut->rootp->milan_datapath__DOT__strtbl_en_w & 0x2), 0);
    check.dec("M3 UNRELATED LOSS: the adapter's commit gate never closed, not "
              "for one cycle",
              static_cast<uint64_t>(commit_gate_closed_cycles), 0);
    check.dec("M3 UNRELATED LOSS: no render epoch closed", lane_epochs(),
              epochs_before);
    long silent = 0;
    for (const DecodedFrame& fr : decoded) {
        bool all_zero = true;
        for (int k = 0; k < kSlots; k++)
            if (fr.slot[static_cast<size_t>(k)] != 0) all_zero = false;
        if (all_zero) ++silent;
    }
    check.dec("M3 UNRELATED LOSS: not one decoded frame fell to digital "
              "silence", static_cast<uint64_t>(silent), 0);
    check.that("M3 UNRELATED LOSS: the lane kept rendering the record",
               w.start >= 0 && w.g.frames > 100);
    check.dec("M3 UNRELATED LOSS: identity holds through the unrelated loss",
              static_cast<uint64_t>(w.g.identity_failures), 0);
    check.dec("M3 UNRELATED LOSS: ...and so does the per-slot structure",
              static_cast<uint64_t>(w.g.channel_field_failures
                                    + w.g.pad_failures), 0);
}

//! M7: THE CORNER BETWEEN THE TWO HALVES. A map write points a lane key at a
//! stream whose bind fell WHILE THE LANE DID NOT RENDER IT. No epoch is owed
//! and none is raised - the qualified fall is the only thing that closes one,
//! and at the fall that stream was not in the lane's set - so the slot is
//! served by the crossbar's RETAINED per-{stream, channel} latch until that
//! stream pops again. This arm visits that corner and states the BOUND rather
//! than assuming it is silence: one constant sample of THAT stream's own
//! audio, never another stream's, never a torn or moving value, on that slot
//! alone, and self-clearing at the first pop (which is M4's half, on its own
//! lane key). The retention is KL_chan_map_render's documented behaviour, one
//! stage above this lane and shared with every other destination; the lane
//! neither creates it nor can see it, and docs/CHANNEL_MAP_64.md 3.1 records
//! it as the bounded case it is.
void TdmRenderHarness::prove_a_stale_stream_repoint_is_bounded(int slot,
                                                               int chan) {
    const uint64_t epochs_before = lane_epochs();
    const int was = src_of_slot(slot);
    epoch_watch_reset();
    check.dec("M7 STALE REPOINT: stream 1 is unbound before the re-point, so "
              "its bind fall is already behind us",
              static_cast<uint64_t>(
                  dut->rootp->milan_datapath__DOT__strtbl_en_w & 0x2), 0);
    check.dec("M7 STALE REPOINT: the stream-0 mapping is removed from the "
              "lane key",
              static_cast<uint64_t>(
                  map_cmd(kCmdRemoveMappings, {{was, slot}}, 0, 0)), 0);
    check.dec("M7 STALE REPOINT: ...and the key is re-pointed at the stream "
              "that is no longer delivering",
              static_cast<uint64_t>(
                  map_cmd(kCmdAddMappings, {{chan, slot}}, 0, 1)), 0);
    //! the re-point takes effect at the crossbar's next media tick, so the
    //! frame straddling it is neither mapping's; the window opens after that
    //! boundary rather than carrying an ungraded frame inside it (M4's rule)
    run_fed(10 * kPduPeriodCycles);
    const Window w = decode_and_grade_a_window(30 * kPduPeriodCycles, "M7");
    report_a_window(w, "M7 with one lane key on a stream that stopped");
    check.dec("M7 STALE REPOINT: the re-point raised no epoch, because no "
               "qualified bind fall happened", lane_epochs(), epochs_before);
    check.dec("M7 STALE REPOINT: ...and the adapter's commit gate never "
              "closed", static_cast<uint64_t>(commit_gate_closed_cycles), 0);
    long moving = 0;
    long wrong_stream = 0;
    uint32_t held = 0;
    bool have_held = false;
    for (const DecodedFrame& fr : decoded) {
        const uint32_t v = fr.slot[static_cast<size_t>(slot)] >> 8;
        if (!have_held) { held = v; have_held = true; }
        else if (v != held) ++moving;
        if (v != 0 && (v & 0xFFu) != (0x80u | static_cast<uint32_t>(chan)))
            ++wrong_stream;
    }
    check.dec("M7 STALE REPOINT: the re-pointed slot holds ONE value in every "
              "decoded frame - a bounded DC re-seed, not moving audio",
              static_cast<uint64_t>(moving), 0);
    check.dec("M7 STALE REPOINT: and that value is digital silence or that "
              "stream's own retained sample, never another stream's",
              static_cast<uint64_t>(wrong_stream), 0);
    check.dec("M7 STALE REPOINT: the other seven slots keep grading against "
              "the stream-0 record",
              static_cast<uint64_t>(w.g.identity_failures), 0);
    std::printf("  [i]    M7: lane key %d re-pointed at stream 1 channel %d "
                "while that stream is down holds %06X in all %zu decoded "
                "frames (%s)\n", slot, chan, held, decoded.size(),
                held == 0 ? "digital silence"
                          : "the crossbar's retained sample of that stream");
    // restore the stream-0 claim this key had, so the next arm starts where
    // it expects to
    check.dec("M7 STALE REPOINT: the key is returned to stream 0",
              static_cast<uint64_t>(
                  map_cmd(kCmdRemoveMappings, {{chan, slot}}, 0, 1)), 0);
    check.dec("M7 STALE REPOINT: ...and its original mapping restored",
              static_cast<uint64_t>(
                  map_cmd(kCmdAddMappings, {{was, slot}}, 0, 0)), 0);
    run_fed(10 * kPduPeriodCycles);
}

//! ...and the routing that makes half two mean anything: one lane key is
//! moved to the OTHER stream through the real map command, and that stream's
//! audio has to appear in that slot at the pins.
void TdmRenderHarness::prove_the_lane_renders_a_second_stream(int slot,
                                                              int chan) {
    run_the_bind_ladder(1, 1, 0x3355, "M4 REBIND");
    feed1_on = true;
    next_pdu1_at = axis_cycle + 128;
    //! A cluster already claimed by a different mapping is not silently
    //! re-pointed: 1722.1-2021 7.4.44 makes ADD_AUDIO_MAPPINGS on a mapped
    //! cluster an error unless it repeats the mapping, so the stream-0 one is
    //! REMOVED first. That refusal is itself worth pinning here, because it
    //! is what stops a controller moving a slot to another stream by halves.
    check.dec("M4 SECOND STREAM: re-pointing a CLAIMED cluster without "
              "removing it first is BAD_ARGUMENTS",
              static_cast<uint64_t>(
                  map_cmd(kCmdAddMappings, {{chan, slot}}, 0, 1)), 7);
    check.dec("M4 SECOND STREAM: the stream-0 mapping is removed from the "
              "lane key",
              static_cast<uint64_t>(
                  map_cmd(kCmdRemoveMappings,
                          {{kPerm[static_cast<size_t>(slot)], slot}}, 0, 0)), 0);
    check.dec("M4 SECOND STREAM: ...and the key is remapped to stream 1 "
              "through ADD_AUDIO_MAPPINGS",
              static_cast<uint64_t>(
                  map_cmd(kCmdAddMappings, {{chan, slot}}, 0, 1)), 0);
    check.dec("M4 SECOND STREAM: the lane's stream mask now names both "
              "streams",
              static_cast<uint64_t>(
                  dut->rootp->milan_datapath__DOT__tdmr_lane_streams_w), 0x3);
    //! the remap takes effect at the crossbar's next media tick, so the frame
    //! straddling it is neither the old mapping's nor the new one's. The
    //! window opens AFTER that boundary rather than being allowed to carry an
    //! ungraded frame inside it.
    run_fed(10 * kPduPeriodCycles);
    const Window w = decode_and_grade_a_window(60 * kPduPeriodCycles, "M4");
    report_a_window(w, "M4 with one slot fed from stream 1");
    long wrong_stream = 0;
    long nonzero = 0;
    for (const DecodedFrame& fr : decoded) {
        const uint32_t v = fr.slot[static_cast<size_t>(slot)] >> 8;
        if ((v & 0xFFu) != (0x80u | static_cast<uint32_t>(chan))) ++wrong_stream;
        if (v != 0) ++nonzero;
    }
    check.that("M4 SECOND STREAM: the remapped slot carries real audio",
               nonzero > 100);
    check.dec("M4 SECOND STREAM: every frame's remapped slot carries STREAM "
              "1's channel marking, which no stream-0 sample can hold",
              static_cast<uint64_t>(wrong_stream), 0);
    check.dec("M4 SECOND STREAM: the other seven slots still match the "
              "stream-0 record",
              static_cast<uint64_t>(w.g.identity_failures), 0);
    check.dec("M4 SECOND STREAM: ...and every slot's channel field is its own "
              "stream's", static_cast<uint64_t>(w.g.channel_field_failures), 0);
}

//! THE QUALIFICATION, half two: the same bind fall, on a stream the lane now
//! DOES render, must close the epoch, flush to digital silence and reopen on
//! a fresh post-flush event.
void TdmRenderHarness::prove_a_rendered_stream_loss_closes_the_epoch(int slot,
                                                                     int chan) {
    const uint64_t epochs_before = lane_epochs();
    epoch_watch_reset();
    std::vector<std::array<uint32_t, kSlots>> pre_loss;
    for (const DecodedFrame& fr : decoded) pre_loss.push_back(fr.slot);
    acmp_disconnect_rx(0x2255, 1, 1);
    decoder_reset();
    collect = true;
    run_fed(60000);
    collect = false;
    feed1_on = false;
    check.that("M5 RENDERED LOSS: the bind fall fired on stream 1",
               (bind_falls_seen & 0x2) != 0);
    check.that("M5 RENDERED LOSS: the adapter's commit gate CLOSED, which the "
               "unrelated loss never did", commit_gate_closed_cycles > 0);
    bool boundary = false;
    long carried = 0;
    for (const DecodedFrame& fr : decoded) {
        bool all_zero = true;
        for (int k = 0; k < kSlots; k++)
            if (fr.slot[static_cast<size_t>(k)] != 0) all_zero = false;
        if (all_zero) { boundary = true; continue; }
        if (!boundary) continue;
        for (const auto& old : pre_loss)
            for (int k = 0; k < kSlots; k++)
                if (fr.slot[static_cast<size_t>(k)] != 0 &&
                    fr.slot[static_cast<size_t>(k)] == old[static_cast<size_t>(k)])
                    ++carried;
    }
    check.that("M5 RENDERED LOSS: the lane reached digital silence", boundary);
    check.dec("M5 RENDERED LOSS: no frame after the boundary carries a "
              "pre-loss sample in any slot", static_cast<uint64_t>(carried), 0);
    //! #443: stream 1 is flushed while stream 0 still runs. These unequal
    //! states catch a CSR selector that silently aliases every index to 0.
    axi_write(0x800, 1);
    const uint32_t second = axi_read(0x8DC);
    check.dec("RENDER-CSR-MULTI: flushed listener 1 has empty prefill",
              second & 0xFFFF, 0x100);
    check.dec("RENDER-CSR-MULTI: listener 1 retains the global rail count",
              second >> 16, dut->rootp->milan_datapath__DOT__rsp_rails_w);
    axi_write(0x800, 0);
    const uint32_t first = axi_read(0x8DC);
    check.that("RENDER-CSR-MULTI: listener 0 still has queued events",
               (first & 0xFF) != 0);
    check.dec("RENDER-CSR-MULTI: listener 0 is not in prefill",
              (first >> 8) & 1, 0);
    axi_write(0x800, 2);
    check.dec("RENDER-CSR-MULTI: first absent index reads zero",
              axi_read(0x8DC), 0);
    axi_write(0x800, 0);
    // ...and the freshness gate: the lane reopens only once BOTH rendered
    // streams have popped a post-flush event, so the rebind alone is not
    // enough and the feed has to be back too
    run_the_bind_ladder(1, 1, 0x3366, "M5 REOPEN");
    feed1_on = true;
    next_pdu1_at = axis_cycle + 128;
    run_fed(40 * kPduPeriodCycles);
    check.dec("M5 REOPEN: the one rendered-stream loss reopened the epoch "
              "EXACTLY once", lane_epochs(), epochs_before + 1);
    check.dec("M5 REOPEN: the adapter's commit gate is open again",
              static_cast<uint64_t>(
                  dut->rootp->milan_datapath__DOT__tdmr_commit_en_w), 1);
    const Window w = decode_and_grade_a_window(40 * kPduPeriodCycles, "M5");
    report_a_window(w, "M5 after the reopen");
    check.that("M5 REOPEN: the lane serializes the record again",
               w.start >= 0 && w.g.frames > 100);
    check.dec("M5 REOPEN: identity holds after the rendered-stream recovery",
              static_cast<uint64_t>(w.g.identity_failures), 0);
    long wrong_stream = 0;
    for (const DecodedFrame& fr : decoded)
        if ((((fr.slot[static_cast<size_t>(slot)] >> 8)) & 0xFFu)
                != (0x80u | static_cast<uint32_t>(chan)))
            ++wrong_stream;
    check.dec("M5 REOPEN: the stream-1 slot is still fed from stream 1",
              static_cast<uint64_t>(wrong_stream), 0);
}

//! [R152] THE NONPHYSICAL IN-RANGE KEY, graded apart from the out-of-range
//! one and apart from a physical one. Three CSR writes, three different
//! answers, and the two observations - the render RAM and the AECP protocol
//! store through GET_AUDIO_MAP - taken SEPARATELY for each:
//!
//!   key 3   PHYSICAL:     reaches the render RAM AND the store
//!   key 9   NONPHYSICAL:  reaches the store ONLY. It is a legal declared
//!                         cluster of STREAM_PORT_INPUT 1 with no physical
//!                         projection, so the crossbar write is suppressed
//!                         at the projection gate while the store mirror,
//!                         which the projection does not gate, still happens.
//!   key 16  OUT OF RANGE: reaches neither.
void TdmRenderHarness::prove_the_nonphysical_key_mirrors_without_reaching_a_pin() {
    std::printf("  [i]    M6: the three cluster-key classes, each graded on "
                "BOTH observations\n");
    std::array<uint32_t, kI2sN + kSlots> ram_before{};
    for (int k = 0; k < kI2sN + kSlots; k++)
        ram_before[static_cast<size_t>(k)] = render_ram(k);

    // ---- the NONPHYSICAL in-range key
    const int nonphys_offset = 1;                     // port 1, cluster 1
    const int nonphys_key = kMultiPort1Base + nonphys_offset;
    csr_map_write(nonphys_key, 0x8000u | 0x0005u);    // stream 0, channel 5
    long ram_same = 0;
    for (int k = 0; k < kI2sN + kSlots; k++)
        if (render_ram(k) == ram_before[static_cast<size_t>(k)]) ++ram_same;
    check.dec("M6 NONPHYSICAL: a legal in-range cluster key with no physical "
              "projection changes NO render RAM word",
              static_cast<uint64_t>(ram_same), kI2sN + kSlots);
    long mirrored = 0;
    for (const auto& r : get_audio_map(1, 0))
        if (r[2] == nonphys_offset && r[1] == 5 && r[0] == 0) ++mirrored;
    check.dec("M6 NONPHYSICAL: ...and the SAME write is still mirrored into "
              "the AECP protocol store, read back through GET_AUDIO_MAP",
              static_cast<uint64_t>(mirrored), 1);

    // ---- the OUT-OF-RANGE key: a different defect class, and it must NOT
    //      reach the store either
    csr_map_write(kMultiInKeys, 0x8000u | 0x0004u);
    long ram_same2 = 0;
    for (int k = 0; k < kI2sN + kSlots; k++)
        if (render_ram(k) == ram_before[static_cast<size_t>(k)]) ++ram_same2;
    check.dec("M6 OUT OF RANGE: a key past the model's declared cluster keys "
              "changes no render RAM word",
              static_cast<uint64_t>(ram_same2), kI2sN + kSlots);
    long rows_out = 0;
    for (const auto& r : get_audio_map(0, 0))
        if (r[1] == 4 && r[2] >= kSlots) ++rows_out;
    for (const auto& r : get_audio_map(1, 0))
        if (r[1] == 4 && r[2] >= kSlots) ++rows_out;
    check.dec("M6 OUT OF RANGE: ...and nothing appears in either port's "
              "GET_AUDIO_MAP page, so the store refused it too",
              static_cast<uint64_t>(rows_out), 0);

    // ---- the PHYSICAL control: both observations MOVE, so the two zeros
    //      above are a suppression and not a dead CSR path
    const int phys_cluster = 3;
    csr_map_write(phys_cluster, 0x8000u | 0x0006u);   // stream 0, channel 6
    check.hex("M6 PHYSICAL: an in-range PROJECTED key reaches the render RAM",
              render_ram(kTdmBase + phys_cluster), 0x86u);
    long phys_mirror = 0;
    for (const auto& r : get_audio_map(0, 0))
        if (r[2] == phys_cluster && r[1] == 6 && r[0] == 0) ++phys_mirror;
    check.dec("M6 PHYSICAL: ...and the protocol store as well",
              static_cast<uint64_t>(phys_mirror), 1);
}

void TdmRenderHarness::phase_multistream() {
    std::printf("\n[MULTI] the stream-qualified render epoch on a two-stream "
                "shape, and a legal cluster key with no pin\n");
    constexpr uint16_t kAdpCtrl = 0x600;
    constexpr uint16_t kAdpEidLo = 0x604;
    constexpr uint16_t kAdpEidHi = 0x608;
    axi_write(kAdpEidHi, 0x020000FF);
    axi_write(kAdpEidLo, 0xFE000001);
    axi_write(kAdpCtrl, 0x00001F01);
    steps(2000);
    //! STREAM 1'S LISTENER CONTEXT. Stream 0's current format reaches the RX
    //! monitor through the legacy fmt0 path; every stream above it is served
    //! from the per-stream LCTX, which the 0x800 window provisions - the same
    //! face the NxN legs use. A CTRL commit with NO staged stream id leaves
    //! the table entry to the ACMP alias (the idx-0 alias protection), so
    //! this provisions the FORMAT and nothing else. The words are the entity's
    //! own declared listener format: AAF, INT32, 48 kHz, 32-bit.
    constexpr uint16_t kStrmSel = 0x800;
    constexpr uint16_t kSwCtrl = 0x810;
    constexpr uint16_t kSwFmtLo = 0x824;
    constexpr uint16_t kSwFmtHi = 0x828;
    axi_write(kStrmSel, 0x001);
    axi_write(kSwFmtLo, 0x02006000);
    axi_write(kSwFmtHi, 0x02050220);
    axi_write(kSwCtrl, 0x1);
    check.hex("M1 CONTEXT: stream 1's listener format reads back out of the "
              "LCTX", axi_read(kSwFmtHi), 0x02050220);
    run_the_bind_ladder(0, 0, 0x1122, "M1 BIND");
    run_the_bind_ladder(1, 1, 0x1133, "M1 BIND");
    check.dec("M1 BIND: both listener streams are bound",
              static_cast<uint64_t>(
                  dut->rootp->milan_datapath__DOT__strtbl_en_w & 0x3), 0x3);
    {
        //! the classifier's own view of what was bound: two entries, two
        //! DIFFERENT stream ids, each the one its ACMP answer carried. The
        //! tap is a flat vector of 32-bit words, so an entry is two of them.
        const uint64_t sid0 = table_sid(0);
        const uint64_t sid1 = table_sid(1);
        std::printf("  [i]    M1: the stream table holds %016llX and "
                    "%016llX\n",
                    static_cast<unsigned long long>(sid0),
                    static_cast<unsigned long long>(sid1));
        check.that("M1 BIND: the two entries carry DIFFERENT stream ids, so "
                   "the two streams are really two", sid0 != sid1);
    }
    check.that("M1: the AECP descriptor store fetched this shape's entity "
               "image", desc_requests > 0);

    route_reset();
    std::vector<std::pair<int, int>> rows;
    for (int co = 0; co < kSlots; co++)
        rows.emplace_back(kPerm[static_cast<size_t>(co)], co);
    check.dec("M1 MAP: eight permuted stream-0 mappings accepted on "
              "STREAM_PORT_INPUT 0",
              static_cast<uint64_t>(map_cmd(kCmdAddMappings, rows, 0, 0)), 0);
    long projected = 0;
    for (int k = 0; k < kSlots; k++)
        if (render_ram(kTdmBase + k) ==
            (0x80u | static_cast<uint32_t>(src_of_slot(k) & 0x3F))) ++projected;
    check.dec("M1 MAP: physical keys 2..9 hold the routed sources on this "
              "shape too", static_cast<uint64_t>(projected), kSlots);
    check.dec("M1 MAP: the lane's stream mask names stream 0 ALONE",
              static_cast<uint64_t>(
                  dut->rootp->milan_datapath__DOT__tdmr_lane_streams_w), 0x1);

    build_injection_record(1200);
    feed_on = true;
    feed1_on = true;
    next_pdu_at = axis_cycle + 64;
    next_pdu1_at = axis_cycle + 128;
    run_fed(60 * kPduPeriodCycles);
    const Window warm = decode_and_grade_a_window(40 * kPduPeriodCycles, "M2");
    report_a_window(warm, "M2 both streams live");
    check.that("M2 WARM: the lane is serializing stream 0 with stream 1 live "
               "beside it", warm.start >= 0 && warm.g.frames > 100);
    check.dec("M2 WARM: identity holds with a second stream running",
              static_cast<uint64_t>(warm.g.identity_failures), 0);
    //! ...and stream 1 is not merely bound: its PDUs are ACCEPTED and its
    //! events are POPPED by the render stage. Without this the whole
    //! qualification below could be graded against a stream that was never
    //! delivering anything.
    std::printf("  [i]    M2: PDUs accepted per stream %ld / %ld; render-stage "
                "pops per stream %ld / %ld\n",
                accepts_by_stream[0], accepts_by_stream[1],
                pops_by_stream[0], pops_by_stream[1]);
    check.that("M2 WARM: stream 1's PDUs are ACCEPTED by the monitor",
               accepts_by_stream[1] > 50);
    check.that("M2 WARM: ...and its events are popped by the render stage",
               pops_by_stream[1] > 500);

    prove_an_unrelated_stream_loss_leaves_the_lane_running();
    prove_a_stale_stream_repoint_is_bounded(5, 4);
    const int lane1_slot = 7;
    const int lane1_chan = 2;
    prove_the_lane_renders_a_second_stream(lane1_slot, lane1_chan);
    prove_a_rendered_stream_loss_closes_the_epoch(lane1_slot, lane1_chan);
    feed_on = false;
    feed1_on = false;
    prove_the_nonphysical_key_mirrors_without_reaching_a_pin();
}

int TdmRenderHarness::run(int argc, char** argv) {
    for (int i = 1; i < argc; i++) {
        const std::string a = argv[i];
        if (a == "--serial-only") serial_only = true;
        else if (a == "--epoch-only") epoch_only = true;
        else if (a == "--crf-only") crf_only = true;
        else if (a == "--defect-stopped-clock") { defect_stopped_clock = true; serial_only = true; }
        else if (a == "--defect-one-sample") { defect_one_sample = true; serial_only = true; corrupt_at = 400; }
        else if (a == "--defect-internal-select") { defect_internal_select = true; crf_only = true; }
    }
    const milan::tb::Model<Vmilan_datapath> model;
    dut = model.get();
    // THE ENTITY MODEL IS THE ONE THE BUILD SHIPS. The AECP uCPU serves
    // READ_DESCRIPTOR from main memory and validates the image header before
    // it enables the entity, so a leg that leaves this face unanswered gets
    // no AECP response at all - which is a stalled harness, not a verdict.
    char image_check[96];
    std::snprintf(image_check, sizeof image_check,
                  "the generated entity image is on disk (make %s)",
                  kAemImage);
    if (!check.that(image_check, load_descriptor_image(kAemImage)))
        return check.report();
    law_reset();
    route_reset();
    bring_out_of_reset();

    if (kMultiShape) {
        // The MULTI-STREAM build runs the one phase its shape exists for. The
        // shipping-shape phases are not repeated there: they would prove the
        // same things a second time on a shape no board flashes.
        phase_multistream();
        return check.report();
    }
    phase_map();
    if (crf_only) {
        phase_crf();
        return check.report();
    }
    if (!epoch_only) phase_serial();
    if (!serial_only) {
        phase_crf();
        phase_csr();
        phase_reset();
        phase_bind_loss();
    }
    return check.report();
}

}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    TdmRenderHarness harness;
    return harness.run(argc, argv);
}

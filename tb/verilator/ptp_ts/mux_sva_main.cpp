// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// Self-checking harness for hdl/common/axis_mux_rr_2in_1out.sv with its bound
// SVA checker (tb/common/sva/, issue #372). The ptp_ts Makefile builds it
// twice, at TDATA_WIDTH 8 and 64, and passes that width in as
// AXIS_MUX_TDATA_WIDTH. The product module is compiled unmodified.
//
// Three things are graded, and none of them reads the checker's internals:
//
//   1. A SCOREBOARD: every beat a source hands over leaves the mux once,
//      unchanged, in that source's order, never inside the other source's
//      packet; nothing leaves that was not handed over; and when both sources
//      offer back-to-back packets the output alternates between them.
//   2. WITNESSES: every checker instance must be elaborated (its DPI scope
//      exists), and every property must report non-vacuous passes. Where the
//      antecedent is visible on the ports, the count must EQUAL the count
//      this harness took from the ports itself; where it involves the mux's
//      internal state, the port-visible events that imply it are a floor.
//   3. The assertions themselves stop the simulation on a violation.
//
// The AXI4-Stream source rules on s0/s1 are THIS harness's obligations
// (u_s0_stimulus, u_s1_stimulus hold it to them). The negative campaign,
// sva_campaign.py, breaks one on purpose with +stimulus_fault=, and runs
// mutated copies of the mux with +verilator+error+limit+ raised so that
// every assertion failing at the first failing edge is reported; the
// harness then stops at the end of that edge and exits 3.
//
// Plusargs: +scenario=<name> runs one scenario (default: all, in order);
// +stimulus_fault=<s0|s1>_<drop_tvalid|flip_tdata|flip_tkeep|flip_tlast>;
// +seed=<n> replays the random scenario; +grade_witnesses grades the
// witnesses after one scenario too (the campaign's unused-path control).
// Exit: 0 pass, 1 a graded check failed, 2 bad plusarg, 3 an assertion
// stopped the run (campaign mode).

#include <verilated.h>

#include "Vaxis_mux_rr_2in_1out.h"
#include "Vaxis_mux_rr_2in_1out__Dpi.h"
#include "../../common/verilator_harness.hpp"

#include <array>
#include <charconv>
#include <cstdint>
#include <cstdio>
#include <deque>
#include <map>
#include <random>
#include <set>
#include <string>
#include <string_view>
#include <type_traits>
#include <utility>
#include <vector>

#ifndef AXIS_MUX_TDATA_WIDTH
#error "build with -DAXIS_MUX_TDATA_WIDTH=<the -GTDATA_WIDTH the model was verilated with>"
#endif

namespace {

using Mux = Vaxis_mux_rr_2in_1out;
using DataWord = std::remove_reference_t<decltype(std::declval<Mux&>().s0_tdata)>;
using KeepWord = std::remove_reference_t<decltype(std::declval<Mux&>().s0_tkeep)>;

constexpr unsigned kTdataWidth = AXIS_MUX_TDATA_WIDTH;
static_assert(kTdataWidth == 8 || kTdataWidth == 64, "this harness drives the 8- and 64-bit shapes");
static_assert(sizeof(DataWord) * 8 == kTdataWidth, "AXIS_MUX_TDATA_WIDTH disagrees with the model");
constexpr unsigned kTkeepWidth = kTdataWidth / 8;
constexpr std::uint64_t kDataMask = kTdataWidth == 64 ? ~std::uint64_t{0}
                                                      : (std::uint64_t{1} << kTdataWidth) - 1;
constexpr std::uint64_t kKeepMask = (std::uint64_t{1} << kTkeepWidth) - 1;
//! TDATA's top bit names the source, so a beat of one source can never pass
//! for a beat of the other.
constexpr unsigned kSourceBit = kTdataWidth - 1;
constexpr std::uint64_t kPoisonStride = 0x9E37'79B9'7F4A'7C15;
constexpr unsigned kSources = 2;
//! Differs per width, so the two builds do not replay identical traffic.
constexpr std::uint64_t kDefaultSeed = 3720 + kTdataWidth;
//! Simulation time per clock, in the 1 ps precision of the mux's
//! `timescale. Both evaluations of a cycle happen at one timestamp and
//! time advances after the rising edge, so every edge lands on a whole
//! nanosecond and the [time] an assertion prints is 1000 * cycle:
//! [6000] is the rising edge that ends cycle 6.
constexpr std::uint64_t kCycleTicks = 1000;
constexpr int kExitAssertionStop = 3;
constexpr int kExitUsage = 2;

//! What a clock edge can carry on one AXI4-Stream interface.
struct Beat {
    std::uint64_t data = 0;
    std::uint64_t keep = 0;
    bool last = false;
};

bool same_beat(const Beat& a, const Beat& b) {
    return a.data == b.data && a.keep == b.keep && a.last == b.last;
}

unsigned source_of(const Beat& beat) {
    return static_cast<unsigned>((beat.data >> kSourceBit) & 1U);
}

//! The TKEEP of a packet's last beat: a low-aligned partial tail on the
//! 64-bit shape, the single byte on the 8-bit one.
std::uint64_t last_keep(unsigned serial) {
    const unsigned bytes = 1 + serial % kTkeepWidth;
    return (std::uint64_t{1} << bytes) - 1;
}

//! Packet `serial` of `source`, `length` beats long. Contents are a pure
//! function of those three numbers and never zero, so the scoreboard needs
//! nothing from the DUT to know what a beat should be.
std::vector<Beat> packet_beats(unsigned source, unsigned serial, unsigned length) {
    std::vector<Beat> beats;
    for (unsigned index = 0; index < length; ++index) {
        const std::uint64_t body = kTdataWidth == 64
            ? (std::uint64_t{serial} << 32) | (std::uint64_t{index} << 16) | 0xA5U
            : 1U + (serial * 37U + index * 11U) % 127U;
        Beat beat;
        beat.data = (std::uint64_t{source} << kSourceBit) | body;
        beat.last = index + 1 == length;
        beat.keep = beat.last ? last_keep(serial) : kKeepMask;
        beats.push_back(beat);
    }
    return beats;
}

//! What an input shows while its TVALID is low: arbitrary and changing
//! every cycle, which AXI4-Stream allows. A DUT that forwarded or accepted
//! it would put a beat on the output that no source handed over.
Beat poison_beat(unsigned source, std::uint64_t cycle) {
    Beat beat;
    beat.data = (~(cycle * kPoisonStride) ^ source) & kDataMask;
    beat.keep = cycle & kKeepMask;
    beat.last = (cycle & 1U) != 0;
    return beat;
}

//! The four stimulus faults the negative campaign can inject, one at a time.
enum class FaultKind { none, drop_tvalid, flip_tdata, flip_tkeep, flip_tlast };

struct StimulusFault {
    unsigned source = 0;
    FaultKind kind = FaultKind::none;
};

//! One input port of the mux, seen from the source that drives it.
struct SourcePins {
    CData& tvalid;
    CData& tready;
    DataWord& tdata;
    KeepWord& tkeep;
    CData& tlast;
};

//! A compliant AXI4-Stream source: it presents one beat at a time and holds
//! TVALID, TDATA, TKEEP and TLAST until the edge that takes it; between beats
//! it may idle, showing poison. On reset it drops TVALID, abandons the rest
//! of a packet it has started, and re-offers one it has not.
class StreamSource {
 public:
    StreamSource(unsigned index, SourcePins pins) : index_(index), pins_(pins) {}

    //! Queue a packet; `gaps[i]` idle cycles precede beat i.
    void add_packet(unsigned length, std::vector<unsigned> gaps) {
        Planned planned;
        planned.beats = packet_beats(index_, next_serial_++, length);
        planned.gaps = std::move(gaps);
        planned.gaps.resize(length, 0);
        const bool was_empty = queue_.empty();
        queue_.push_back(std::move(planned));
        if (was_empty) {
            gap_left_ = queue_.front().gaps[0];
        }
    }

    void arm_fault(FaultKind kind) { fault_ = kind; }
    bool fault_injected() const { return fault_done_; }

    //! Drive the pins for the coming edge.
    void drive(std::uint64_t cycle) {
        const bool ready_to_offer = !queue_.empty() && gap_left_ == 0 && holdoff_ == 0;
        const bool offer = ready_to_offer && !withdrawn_;
        //! A withdrawn beat keeps its payload: that fault breaks TVALID alone.
        Beat beat = ready_to_offer ? queue_.front().beats[beat_] : poison_beat(index_, cycle);
        if (offer && corrupt_) {
            beat = corrupted(beat);
        }
        pins_.tvalid = offer ? 1 : 0;
        pins_.tdata = static_cast<DataWord>(beat.data & kDataMask);
        pins_.tkeep = static_cast<KeepWord>(beat.keep & kKeepMask);
        pins_.tlast = beat.last ? 1 : 0;
    }

    bool taken() const { return pins_.tvalid != 0 && pins_.tready != 0; }
    bool stalled() const { return pins_.tvalid != 0 && pins_.tready == 0; }
    Beat presented() const { return Beat{pins_.tdata, pins_.tkeep, pins_.tlast != 0}; }
    std::size_t beat_index() const { return beat_; }

    //! Advance after the edge: next beat on a handshake, the armed fault on
    //! the first stall, and one idle cycle off any gap being served.
    void after_edge(bool handshake, bool stalled, std::uint64_t cycle) {
        withdrawn_ = false;
        corrupt_ = false;
        if (holdoff_ > 0) {
            --holdoff_;
        } else if (gap_left_ > 0) {
            --gap_left_;
        } else if (handshake) {
            next_beat();
        } else if (stalled && fault_ != FaultKind::none && !fault_done_) {
            inject(cycle);
        }
    }

    //! Called for every edge that samples reset, before driving it: TVALID
    //! drops, a started packet is abandoned (its accepted prefix is all the
    //! output will ever see of it), an unstarted one is re-offered, and
    //! TVALID also stays low at the first edge after release (IHI0051A).
    void on_reset() {
        if (!queue_.empty() && beat_ > 0) {
            queue_.pop_front();
        }
        beat_ = 0;
        gap_left_ = queue_.empty() ? 0 : queue_.front().gaps[0];
        holdoff_ = 2;
        withdrawn_ = false;
        corrupt_ = false;
    }

    bool done() const { return queue_.empty(); }

 private:
    struct Planned {
        std::vector<Beat> beats;
        std::vector<unsigned> gaps;
    };

    void next_beat() {
        ++beat_;
        if (beat_ == queue_.front().beats.size()) {
            queue_.pop_front();
            beat_ = 0;
        }
        gap_left_ = queue_.empty() ? 0 : queue_.front().gaps[beat_];
    }

    void inject(std::uint64_t cycle) {
        fault_done_ = true;
        if (fault_ == FaultKind::drop_tvalid) {
            withdrawn_ = true;
        } else {
            corrupt_ = true;
        }
        std::printf("stimulus fault injected: s%u, after the stall sampled at cycle %llu\n",
                    index_, static_cast<unsigned long long>(cycle));
    }

    Beat corrupted(Beat beat) const {
        if (fault_ == FaultKind::flip_tdata) {
            beat.data ^= 1U;
        } else if (fault_ == FaultKind::flip_tkeep) {
            beat.keep ^= 1U;
        } else if (fault_ == FaultKind::flip_tlast) {
            beat.last = !beat.last;
        }
        return beat;
    }

    unsigned index_;
    SourcePins pins_;
    std::deque<Planned> queue_;
    unsigned next_serial_ = 0;
    std::size_t beat_ = 0;
    unsigned gap_left_ = 0;
    unsigned holdoff_ = 0;
    FaultKind fault_ = FaultKind::none;
    bool fault_done_ = false;
    bool withdrawn_ = false;
    bool corrupt_ = false;
};

//! How the sink paces m_tready.
struct SinkPlan {
    unsigned stall_at_beat = 0;      //!< stall the beat with this 1-based index in each packet (0: never)
    bool stall_last_beat = false;    //!< stall every packet's TLAST beat
    unsigned stall_cycles = 0;       //!< how long each stall lasts
    unsigned ready_percent = 100;    //!< random TREADY otherwise; 100 is always ready
};

//! The sink behind m. It may look at the beat on offer before deciding
//! TREADY for the same edge, which AXI4-Stream allows (TREADY may depend on
//! TVALID); the harness settles the model again after it decides.
class Sink {
 public:
    explicit Sink(CData& tready) : tready_(tready) {}

    void set_plan(const SinkPlan& plan) {
        plan_ = plan;
        stall_left_ = 0;
        stalled_this_beat_ = false;
    }

    //! TREADY while the beat on offer settles; decide() may then lower it.
    void open() { tready_ = 1; }

    //! Decide TREADY for this edge from the beat on offer.
    void decide(bool m_tvalid, bool m_tlast, std::mt19937_64& rng) {
        const bool pick = m_tvalid && !stalled_this_beat_ && plan_.stall_cycles > 0
            && ((plan_.stall_last_beat && m_tlast) || (plan_.stall_at_beat != 0
                && beat_in_packet_ + 1 == plan_.stall_at_beat));
        if (pick) {
            stall_left_ = plan_.stall_cycles;
            stalled_this_beat_ = true;
        }
        bool ready = true;
        if (stall_left_ > 0) {
            --stall_left_;
            ready = false;
        } else if (plan_.ready_percent < 100) {
            ready = rng() % 100 < plan_.ready_percent;
        }
        tready_ = ready ? 1 : 0;
    }

    void after_edge(bool transfer, bool last) {
        if (transfer) {
            stalled_this_beat_ = false;
            beat_in_packet_ = last ? 0 : beat_in_packet_ + 1;
        }
    }

    void on_reset() {
        beat_in_packet_ = 0;
        stalled_this_beat_ = false;
        stall_left_ = 0;
    }

 private:
    CData& tready_;
    SinkPlan plan_;
    unsigned stall_left_ = 0;
    unsigned beat_in_packet_ = 0;
    bool stalled_this_beat_ = false;
};

//! Grades what leaves m against what s0 and s1 handed over, and nothing
//! else: it never reads the checker or the mux's state.
class Scoreboard {
 public:
    explicit Scoreboard(milan::tb::Checker& check) : check_(check) {}

    void accepted(unsigned source, const Beat& beat) { pending_[source].push_back(beat); }

    void delivered(const Beat& beat, std::uint64_t cycle) {
        const unsigned source = source_of(beat);
        if (!open_packet_) {
            open_packet_ = true;
            open_source_ = source;
            open_intact_ = true;
        } else if (source != open_source_) {
            fail_beat("a beat of the other source inside an open packet", beat, cycle);
        }
        if (pending_[source].empty()) {
            fail_beat("a beat that no source handed over", beat, cycle);
        } else if (!same_beat(pending_[source].front(), beat)) {
            fail_beat("a beat that differs from the one handed over", beat, cycle);
            pending_[source].pop_front();
        } else {
            pending_[source].pop_front();
        }
        if (beat.last) {
            check_.that("an output packet leaves the mux intact and in its source's order",
                        open_intact_);
            order_.push_back(open_source_);
            open_packet_ = false;
        }
    }

    //! Reset sampled: an open output packet may end here without TLAST, but
    //! a mux with no storage must not be holding any accepted beat.
    void on_reset() {
        open_packet_ = false;
        check_.that("no accepted beat is still inside the mux when reset arrives",
                    pending_[0].empty() && pending_[1].empty());
        pending_[0].clear();
        pending_[1].clear();
    }

    //! End of a scenario: everything handed over has left, as whole packets.
    void close(const char* scenario) {
        char what[160];
        std::snprintf(what, sizeof what, "%s: every accepted beat left the mux", scenario);
        check_.that(what, pending_[0].empty() && pending_[1].empty());
        std::snprintf(what, sizeof what, "%s: no output packet is left open", scenario);
        check_.that(what, !open_packet_);
    }

    std::vector<unsigned> take_order() { return std::exchange(order_, {}); }

 private:
    void fail_beat(const char* what, const Beat& beat, std::uint64_t cycle) {
        char message[200];
        std::snprintf(message, sizeof message, "%s (cycle %llu, data 0x%llx keep 0x%llx last %d)", what,
                      static_cast<unsigned long long>(cycle), static_cast<unsigned long long>(beat.data),
                      static_cast<unsigned long long>(beat.keep), beat.last ? 1 : 0);
        check_.fail(message);
        open_intact_ = false;
    }

    milan::tb::Checker& check_;
    std::array<std::deque<Beat>, kSources> pending_;
    std::vector<unsigned> order_;
    bool open_packet_ = false;
    unsigned open_source_ = 0;
    bool open_intact_ = true;
};

//! What one (checker instance, property) pair reported through its pass
//! action. Only the calls flagged non-vacuous are kept: a pass action runs at
//! every passing edge, so the number of calls counts edges, not checks.
struct WitnessTally {
    std::uint64_t nonvacuous = 0;
};

//! The ledger the DPI callback writes into. svPutUserData files it under each
//! checker scope the harness expects, so the callback reaches it through the
//! scope that called, and no state lives at file scope.
class WitnessLedger {
 public:
    //! The identity the ledger is filed under; only its address is used.
    static void* user_data_key() {
        static char key = 0;
        return &key;
    }

    void record(const char* scope, const char* rule, bool nonvacuous) {
        WitnessTally& tally = tallies_[std::string(scope) + "." + rule];
        if (nonvacuous) {
            ++tally.nonvacuous;
        }
    }

    const std::map<std::string, WitnessTally>& tallies() const { return tallies_; }

 private:
    std::map<std::string, WitnessTally> tallies_;
};

}  // namespace

//! Called by every checker property's pass action (tb/common/sva/). A scope
//! the harness did not register has no ledger, and that is a harness defect.
void axis_sva_witness(const char* rule_name, svBit nonvacuous) {
    const svScope scope = svGetScope();
    auto* ledger = static_cast<WitnessLedger*>(svGetUserData(scope, WitnessLedger::user_data_key()));
    if (ledger == nullptr) {
        vl_fatal(__FILE__, __LINE__, "", "axis_sva_witness: a checker scope the harness never registered");
        return;
    }
    ledger->record(svGetNameFromScope(scope), rule_name, nonvacuous != 0);
}

namespace {

//! Where the bind puts the checker, and the per-interface instances in it.
constexpr std::string_view kCheckerScope = "TOP.axis_mux_rr_2in_1out.u_sva";
constexpr std::array<std::string_view, 3> kInterfaceScopes = {".u_s0_stimulus", ".u_s1_stimulus",
                                                              ".u_m_dut"};
constexpr std::array<std::string_view, 4> kHandshakeRules = {
    "ap_tvalid_held_until_handshake", "ap_tdata_stable_until_handshake",
    "ap_tkeep_stable_until_handshake", "ap_tlast_stable_until_handshake"};

//! Thrown by tick() once an assertion has failed: the campaign raises the
//! error limit so that every assertion failing at that edge is reported,
//! and the run stops there.
struct AssertionStop {
    std::uint64_t cycle;
};

//! The harness's own count, from the ports alone, of what each property
//! must have seen. An attempt is counted at the edge that completes it, and
//! reset is handled the way `disable iff (!rst_n)` handles it.
struct PortCounts {
    std::array<std::uint64_t, 3> stall_attempts{};  //!< s0, s1, m: a stall, rst_n high there and next edge
    std::uint64_t running_edges = 0;          //!< edges sampling rst_n high
    std::uint64_t reset_attempts = 0;         //!< edges sampling reset that another edge follows
    std::uint64_t tlast_handshakes = 0;       //!< s0/s1 TLAST handshakes, rst_n high there and next edge
    std::uint64_t mid_packet_handshakes = 0;  //!< the same for the other handshakes: each keeps an owner
    std::uint64_t packet_starts = 0;          //!< first-beat handshakes on s0/s1: each needed a grant
    std::uint64_t granted_edges = 0;          //!< edges where s0 or s1 saw TREADY
    std::uint64_t valid_edges = 0;            //!< edges where m showed TVALID
    std::uint64_t transfers = 0;              //!< handshakes on m
};

//! The previous edge, as much of it as PortCounts needs.
struct PreviousEdge {
    std::array<bool, 3> stalled{};
    bool in_reset = false;
    bool tlast_handshake = false;
    bool mid_packet_handshake = false;
};

//! What one edge carried, as the sources and the sink need to hear it.
struct EdgeSample {
    std::array<bool, kSources> taken{};
    std::array<bool, kSources> stalled{};
    bool transfer = false;
    bool m_last = false;
};

//! How a witness count must relate to the harness's own count.
enum class Bound { exact, floor, present };

struct WitnessExpectation {
    std::string key;
    std::uint64_t harness;
    Bound bound;
};

class MuxSvaHarness;

struct Scenario {
    std::string_view name;
    void (MuxSvaHarness::*run)();
};

//! Parse `+name=value`; empty when the plusarg is absent.
std::string plusarg(const char* name_equals) {
    const std::string match(Verilated::commandArgsPlusMatch(name_equals));
    const std::size_t eq = match.find('=');
    return eq == std::string::npos ? std::string{} : match.substr(eq + 1);
}

bool parse_fault(const std::string& text, StimulusFault& fault) {
    constexpr std::array<std::pair<std::string_view, FaultKind>, 4> kKinds = {{
        {"drop_tvalid", FaultKind::drop_tvalid}, {"flip_tdata", FaultKind::flip_tdata},
        {"flip_tkeep", FaultKind::flip_tkeep}, {"flip_tlast", FaultKind::flip_tlast}}};
    if (text.size() < 4 || text[0] != 's' || (text[1] != '0' && text[1] != '1') || text[2] != '_') {
        return false;
    }
    for (const auto& [name, kind] : kKinds) {
        if (std::string_view(text).substr(3) == name) {
            fault.source = static_cast<unsigned>(text[1] - '0');
            fault.kind = kind;
            return true;
        }
    }
    return false;
}

class MuxSvaHarness {
 public:
    MuxSvaHarness()
        : top_(model_.get()),
          check_(kTdataWidth == 8 ? "ptp_ts mux sva w8" : "ptp_ts mux sva w64"),
          sources_{{StreamSource{0, SourcePins{top_->s0_tvalid, top_->s0_tready, top_->s0_tdata,
                                                top_->s0_tkeep, top_->s0_tlast}},
                    StreamSource{1, SourcePins{top_->s1_tvalid, top_->s1_tready, top_->s1_tdata,
                                                top_->s1_tkeep, top_->s1_tlast}}}},
          sink_(top_->m_tready),
          scoreboard_(check_) {}

    int run() {
        if (const int usage = parse_plusargs(); usage != 0) {
            return usage;
        }
        rng_.seed(seed_);
        std::printf("axis_mux_rr_2in_1out with its bound checker: TDATA_WIDTH=%u seed=%llu "
                    "(+seed=<n> replays random_mix) scenario=%s stimulus_fault=%s\n",
                    kTdataWidth, static_cast<unsigned long long>(seed_),
                    only_scenario_.empty() ? "all" : only_scenario_.c_str(),
                    fault_name_.empty() ? "none" : fault_name_.c_str());
        register_checker_scopes();
        if (fault_.kind != FaultKind::none) {
            sources_[fault_.source].arm_fault(fault_.kind);
        }
        try {
            run_scenarios();
        } catch (const AssertionStop& stop) {
            std::printf("SVA-STOP: an assertion failed at the edge ending cycle %llu (the %%Error "
                        "lines above name it); the run stops at that edge\n",
                        static_cast<unsigned long long>(stop.cycle));
            return kExitAssertionStop;
        }
        if (fault_.kind != FaultKind::none) {
            check_.that("the requested stimulus fault was injected",
                        sources_[fault_.source].fault_injected());
        }
        if (only_scenario_.empty() || Verilated::commandArgsPlusMatch("grade_witnesses")[0] != '\0') {
            grade_witnesses();
        } else {
            std::printf("witness grading needs every scenario (+scenario= selected one; "
                        "+grade_witnesses grades it anyway)\n");
        }
        return check_.report();
    }

 private:
    static std::array<Scenario, 8> scenarios() {
        return {{{"single_beats", &MuxSvaHarness::scenario_single_beats},
                 {"multi_beats", &MuxSvaHarness::scenario_multi_beats},
                 {"valid_gaps", &MuxSvaHarness::scenario_valid_gaps},
                 {"simultaneous_offers", &MuxSvaHarness::scenario_simultaneous_offers},
                 {"backpressure_mid_packet", &MuxSvaHarness::scenario_backpressure_mid_packet},
                 {"backpressure_last_beat", &MuxSvaHarness::scenario_backpressure_last_beat},
                 {"reset_while_stalled", &MuxSvaHarness::scenario_reset_while_stalled},
                 {"random_mix", &MuxSvaHarness::scenario_random_mix}}};
    }

    int parse_plusargs() {
        only_scenario_ = plusarg("scenario=");
        bool known = only_scenario_.empty();
        for (const Scenario& scenario : scenarios()) {
            known = known || scenario.name == only_scenario_;
        }
        if (!known) {
            std::printf("unknown +scenario=%s\n", only_scenario_.c_str());
            return kExitUsage;
        }
        fault_name_ = plusarg("stimulus_fault=");
        if (!fault_name_.empty() && !parse_fault(fault_name_, fault_)) {
            std::printf("unknown +stimulus_fault=%s (want s0_ or s1_ then drop_tvalid, flip_tdata, "
                        "flip_tkeep or flip_tlast)\n", fault_name_.c_str());
            return kExitUsage;
        }
        const std::string seed = plusarg("seed=");
        if (!seed.empty()) {
            const auto [end, error] = std::from_chars(seed.data(), seed.data() + seed.size(), seed_);
            if (error != std::errc{} || end != seed.data() + seed.size()) {
                std::printf("unreadable +seed=%s\n", seed.c_str());
                return kExitUsage;
            }
        }
        return 0;
    }

    //! A checker instance that is not elaborated has no DPI scope: the bind
    //! is missing or mistyped, or --no-assert compiled every call out.
    void register_checker_scopes() {
        for (std::string_view suffix : {std::string_view{}, kInterfaceScopes[0], kInterfaceScopes[1],
                                        kInterfaceScopes[2]}) {
            const std::string name = std::string(kCheckerScope) + std::string(suffix);
            const svScope scope = svGetScopeFromName(name.c_str());
            check_.that(("checker instance " + name + " is elaborated with its assertions").c_str(),
                        scope != nullptr);
            if (scope != nullptr) {
                svPutUserData(scope, WitnessLedger::user_data_key(), &ledger_);
            }
        }
    }

    void run_scenarios() {
        reset_for(4);
        for (const Scenario& scenario : scenarios()) {
            if (aborted_ || (!only_scenario_.empty() && scenario.name != only_scenario_)) {
                continue;
            }
            std::printf("scenario %s from cycle %llu\n", scenario.name.data(),
                        static_cast<unsigned long long>(cycle_));
            (this->*scenario.run)();
            scoreboard_.close(scenario.name.data());
        }
    }

    // ---- clocking -------------------------------------------------------------

    //! One clock: drive, settle, let the sink decide, sample the edge, clock
    //! it, then let the sources and the sink react to what the edge took.
    void tick() {
        top_->rst_n = reset_asserted_ ? 0 : 1;
        for (StreamSource& source : sources_) {
            if (reset_asserted_) {
                source.on_reset();
            }
            source.drive(cycle_);
        }
        sink_.open();
        top_->clk = 0;
        top_->eval();
        sink_.decide(top_->m_tvalid != 0, top_->m_tlast != 0, rng_);
        top_->eval();
        const EdgeSample sample = observe();
        top_->clk = 1;
        top_->eval();
        Verilated::threadContextp()->timeInc(kCycleTicks);
        for (unsigned index = 0; index < kSources; ++index) {
            sources_[index].after_edge(sample.taken[index], sample.stalled[index], cycle_);
        }
        sink_.after_edge(sample.transfer, sample.m_last);
        ++cycle_;
        if (Verilated::threadContextp()->errorCount() > 0) {
            throw AssertionStop{cycle_ - 1};
        }
    }

    EdgeSample observe() {
        EdgeSample sample;
        for (unsigned index = 0; index < kSources; ++index) {
            sample.taken[index] = sources_[index].taken();
            sample.stalled[index] = sources_[index].stalled();
        }
        sample.transfer = top_->m_tvalid != 0 && top_->m_tready != 0;
        sample.m_last = top_->m_tlast != 0;
        const bool running = top_->rst_n != 0;
        count_properties(sample, running);
        grade_handshakes(sample, running);
        m_stall_run_ = top_->m_tvalid != 0 && top_->m_tready == 0 ? m_stall_run_ + 1 : 0;
        return sample;
    }

    void count_properties(const EdgeSample& sample, bool running) {
        const std::array<bool, 3> stalled = {sample.stalled[0], sample.stalled[1],
                                             top_->m_tvalid != 0 && top_->m_tready == 0};
        for (std::size_t index = 0; index < stalled.size(); ++index) {
            counts_.stall_attempts[index] += previous_.stalled[index] && running ? 1 : 0;
            previous_.stalled[index] = running && stalled[index];
        }
        counts_.running_edges += running ? 1 : 0;
        counts_.reset_attempts += previous_.in_reset ? 1 : 0;
        previous_.in_reset = !running;
        bool tlast_handshake = false;
        bool mid_packet_handshake = false;
        for (unsigned index = 0; index < kSources; ++index) {
            if (sample.taken[index]) {
                const bool last = sources_[index].presented().last;
                tlast_handshake = tlast_handshake || last;
                mid_packet_handshake = mid_packet_handshake || !last;
                counts_.packet_starts += running && sources_[index].beat_index() == 0 ? 1 : 0;
            }
        }
        counts_.tlast_handshakes += previous_.tlast_handshake && running ? 1 : 0;
        counts_.mid_packet_handshakes += previous_.mid_packet_handshake && running ? 1 : 0;
        previous_.tlast_handshake = running && tlast_handshake;
        previous_.mid_packet_handshake = running && mid_packet_handshake;
        counts_.granted_edges += running && (top_->s0_tready != 0 || top_->s1_tready != 0) ? 1 : 0;
        counts_.valid_edges += running && top_->m_tvalid != 0 ? 1 : 0;
        counts_.transfers += running && sample.transfer ? 1 : 0;
    }

    void grade_handshakes(const EdgeSample& sample, bool running) {
        if (!running) {
            handshake_in_reset_ = handshake_in_reset_ || sample.transfer || sample.taken[0]
                || sample.taken[1];
            return;
        }
        for (unsigned index = 0; index < kSources; ++index) {
            if (sample.taken[index]) {
                scoreboard_.accepted(index, sources_[index].presented());
            }
        }
        if (sample.transfer) {
            scoreboard_.delivered(Beat{top_->m_tdata, top_->m_tkeep, top_->m_tlast != 0}, cycle_);
        }
    }

    void reset_for(unsigned edges) {
        scoreboard_.on_reset();
        sink_.on_reset();
        handshake_in_reset_ = false;
        reset_asserted_ = true;
        for (unsigned edge = 0; edge < edges; ++edge) {
            tick();
        }
        reset_asserted_ = false;
        check_.that("no handshake at an edge that samples reset", !handshake_in_reset_);
    }

    //! Clock until `condition` holds; a watchdog in DUT cycles, never in host
    //! time, fails the run and abandons the remaining scenarios.
    template <class Condition>
    void run_until(const char* what, std::uint64_t budget_cycles, Condition condition) {
        const std::uint64_t start = cycle_;
        while (!aborted_ && !condition()) {
            if (cycle_ - start >= budget_cycles) {
                check_.fail((std::string(what) + ": not reached within "
                             + std::to_string(budget_cycles) + " cycles").c_str());
                aborted_ = true;
                return;
            }
            tick();
        }
    }

    //! Clock until both sources have handed everything over, then let the
    //! mux return to IDLE.
    void drain(const char* what, std::uint64_t budget_cycles) {
        run_until(what, budget_cycles, [this] { return sources_[0].done() && sources_[1].done(); });
        for (unsigned settle = 0; settle < 4 && !aborted_; ++settle) {
            tick();
        }
    }

    // ---- scenarios --------------------------------------------------------------

    void scenario_single_beats() {
        sink_.set_plan(SinkPlan{});
        for (unsigned packet = 0; packet < 4; ++packet) {
            sources_[0].add_packet(1, {});
        }
        drain("single_beats, s0 alone", 200);
        for (unsigned packet = 0; packet < 4; ++packet) {
            sources_[1].add_packet(1, {});
        }
        drain("single_beats, s1 alone", 200);
    }

    void scenario_multi_beats() {
        sink_.set_plan(SinkPlan{});
        for (unsigned length : {2U, 5U, 8U}) {
            sources_[0].add_packet(length, {});
        }
        drain("multi_beats, s0 alone", 200);
        for (unsigned length : {3U, 6U}) {
            sources_[1].add_packet(length, {});
        }
        drain("multi_beats, s1 alone", 200);
    }

    void scenario_valid_gaps() {
        sink_.set_plan(SinkPlan{});
        sources_[0].add_packet(4, {0, 2, 1, 3});
        sources_[0].add_packet(3, {1, 0, 2});
        sources_[1].add_packet(5, {2, 1, 0, 3, 1});
        sources_[1].add_packet(2, {0, 4});
        drain("valid_gaps", 400);
    }

    //! Both sources offer back-to-back packets from the same edge: a round
    //! robin must hand the output over after every packet.
    void scenario_simultaneous_offers() {
        sink_.set_plan(SinkPlan{});
        scoreboard_.take_order();
        constexpr unsigned kPacketsEach = 6;
        for (unsigned packet = 0; packet < kPacketsEach; ++packet) {
            sources_[0].add_packet(1 + packet % 4, {});
            sources_[1].add_packet(1 + (packet + 2) % 4, {});
        }
        drain("simultaneous_offers", 400);
        const std::vector<unsigned> order = scoreboard_.take_order();
        bool alternates = order.size() == 2 * kPacketsEach;
        for (std::size_t index = 1; index < order.size(); ++index) {
            alternates = alternates && order[index] != order[index - 1];
        }
        check_.that("simultaneous_offers: saturated sources alternate packet by packet", alternates);
    }

    void scenario_backpressure_mid_packet() {
        SinkPlan plan;
        plan.stall_at_beat = 3;
        plan.stall_cycles = 4;
        sink_.set_plan(plan);
        for (unsigned packet = 0; packet < 2; ++packet) {
            sources_[0].add_packet(6, {});
            sources_[1].add_packet(6, {});
        }
        drain("backpressure_mid_packet", 400);
    }

    void scenario_backpressure_last_beat() {
        SinkPlan plan;
        plan.stall_last_beat = true;
        plan.stall_cycles = 5;
        sink_.set_plan(plan);
        for (unsigned length : {1U, 4U}) {
            sources_[0].add_packet(length, {});
            sources_[1].add_packet(length, {});
        }
        drain("backpressure_last_beat", 400);
    }

    //! Reset lands while the owner is stalled - on a middle beat, then on
    //! its TLAST beat - and the other source is waiting; traffic resumes.
    void scenario_reset_while_stalled() {
        SinkPlan hold_middle;
        hold_middle.stall_at_beat = 3;
        hold_middle.stall_cycles = 50;
        sink_.set_plan(hold_middle);
        sources_[0].add_packet(6, {});
        sources_[1].add_packet(4, {});
        run_until("reset_while_stalled, stall on a middle beat", 100, [this] { return m_stall_run_ >= 3; });
        reset_for(3);
        sink_.set_plan(SinkPlan{});
        sources_[0].add_packet(3, {});
        drain("reset_while_stalled, resume after the middle-beat reset", 200);

        SinkPlan hold_last;
        hold_last.stall_last_beat = true;
        hold_last.stall_cycles = 50;
        sink_.set_plan(hold_last);
        sources_[1].add_packet(3, {});
        sources_[0].add_packet(2, {});
        run_until("reset_while_stalled, stall on a TLAST beat", 100, [this] { return m_stall_run_ >= 2; });
        reset_for(2);
        sink_.set_plan(SinkPlan{});
        sources_[1].add_packet(2, {});
        drain("reset_while_stalled, resume after the TLAST reset", 200);
    }

    //! Seeded traffic: random lengths, gaps and TREADY on both sources, and
    //! one reset at a random edge in the middle of it.
    void scenario_random_mix() {
        SinkPlan plan;
        plan.ready_percent = 70;
        sink_.set_plan(plan);
        for (StreamSource& source : sources_) {
            for (unsigned packet = 0; packet < 40; ++packet) {
                const unsigned length = 1 + static_cast<unsigned>(rng_() % 8);
                std::vector<unsigned> gaps(length);
                for (unsigned& gap : gaps) {
                    gap = rng_() % 10 < 6 ? 0 : 1 + static_cast<unsigned>(rng_() % 3);
                }
                source.add_packet(length, std::move(gaps));
            }
        }
        const std::uint64_t reset_at = cycle_ + 40 + rng_() % 160;
        run_until("random_mix, to its reset", 1000, [this, reset_at] { return cycle_ >= reset_at; });
        reset_for(1 + static_cast<unsigned>(rng_() % 3));
        drain("random_mix", 4000);
    }

    // ---- witnesses ----------------------------------------------------------------

    std::vector<WitnessExpectation> witness_expectations() const {
        const std::string root(kCheckerScope);
        std::vector<WitnessExpectation> expected;
        for (std::size_t index = 0; index < kInterfaceScopes.size(); ++index) {
            for (std::string_view rule : kHandshakeRules) {
                expected.push_back({root + std::string(kInterfaceScopes[index]) + "." + std::string(rule),
                                    counts_.stall_attempts[index], Bound::exact});
            }
        }
        expected.push_back({root + ".ap_state_legal", counts_.running_edges, Bound::exact});
        expected.push_back({root + ".ap_reset_releases_owner", counts_.reset_attempts, Bound::exact});
        expected.push_back({root + ".ap_owner_released_after_tlast", counts_.tlast_handshakes, Bound::exact});
        expected.push_back({root + ".ap_owner_held_until_tlast_handshake", counts_.mid_packet_handshakes,
                            Bound::floor});
        expected.push_back({root + ".ap_grant_only_to_requester", counts_.packet_starts, Bound::floor});
        expected.push_back({root + ".ai_grants_mutually_exclusive", counts_.granted_edges, Bound::present});
        expected.push_back({root + ".ai_ready_only_for_owner_and_ready_sink", counts_.granted_edges,
                            Bound::present});
        expected.push_back({root + ".ai_tvalid_forwarded", counts_.valid_edges, Bound::present});
        expected.push_back({root + ".ai_payload_forwarded_on_transfer", counts_.transfers, Bound::present});
        return expected;
    }

    //! Every property must have passed non-vacuously, as often as the ports
    //! say it had to (exact), at least that often (floor: the antecedent
    //! also covers internal state), or at all (present: an immediate
    //! assertion re-evaluates whenever an input moves, not once per edge).
    void grade_witnesses() {
        const std::map<std::string, WitnessTally>& tallies = ledger_.tallies();
        std::set<std::string> expected_keys;
        for (const WitnessExpectation& expectation : witness_expectations()) {
            expected_keys.insert(expectation.key);
            const auto found = tallies.find(expectation.key);
            const std::uint64_t seen = found == tallies.end() ? 0 : found->second.nonvacuous;
            bool ok = expectation.harness > 0 && seen > 0;
            if (expectation.bound == Bound::exact) {
                ok = ok && seen == expectation.harness;
            } else if (expectation.bound == Bound::floor) {
                ok = ok && seen >= expectation.harness;
            }
            const char* relation = expectation.bound == Bound::exact ? "equal"
                                   : expectation.bound == Bound::floor ? "at least" : "both above zero";
            std::printf("witness %-78s nonvacuous=%llu harness=%llu (%s)\n", expectation.key.c_str(),
                        static_cast<unsigned long long>(seen),
                        static_cast<unsigned long long>(expectation.harness), relation);
            check_.that(("witness " + expectation.key).c_str(), ok);
        }
        for (const auto& [key, tally] : tallies) {
            if (expected_keys.count(key) == 0) {
                check_.fail(("a witness this harness does not expect: " + key).c_str());
            }
        }
    }

    const milan::tb::Model<Mux> model_;
    Mux* top_;
    milan::tb::Checker check_;
    std::array<StreamSource, kSources> sources_;
    Sink sink_;
    Scoreboard scoreboard_;
    WitnessLedger ledger_;
    PortCounts counts_;
    PreviousEdge previous_;
    std::mt19937_64 rng_;
    std::uint64_t seed_ = kDefaultSeed;
    std::uint64_t cycle_ = 0;
    std::string only_scenario_;
    std::string fault_name_;
    StimulusFault fault_;
    bool reset_asserted_ = false;
    bool handshake_in_reset_ = false;
    bool aborted_ = false;
    unsigned m_stall_run_ = 0;
};

}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    MuxSvaHarness harness;
    return harness.run();
}

// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// test_plat_sinks.cpp - each Stream Input's current format in its
// receive-monitor context (#946; plat/ctrl_plat.c's receive-monitor formats,
// plat/ctrl_plat_csr.c), on the host: ctrl_plat.c's boot and composition on the mailbox model, the saved-state
// flash model and the CSR window of plat_bus.hpp, at the generated shape it is built
// for (PLAT_TEST_SHAPE).
//
// The window is read as the datapath decodes it (REGISTER_MAP.md, 0x800
// window): a write to the selection names {dir, idx}, and with dir 0 the
// FMT_LO and FMT_HI writes land in listener context idx's words 2 and 3. The
// receive monitor judges every PDU of a stream above 0 against those words,
// and a PDU not in them counts UNSUPPORTED_FORMAT and is discarded (Milan v1.2
// Table 5.6, 4.4.2.2; KL_avtp_rx_monitor_ctx), so each AAF input above 0 must
// hold its current format whenever a stream of its binding can arrive. Every
// case watches each mailbox access for it (Coherence): while an input's binding
// has a stream published, its context holds the input's current format, from
// the access that publishes it, the first a PDU of that stream can follow; and
// no SET_STREAM_FORMAT answered SUCCESS leaves before its context holds it.
//
//   S1  at READY every AAF STREAM_INPUT above 0 holds its current format,
//       written after the face's acknowledged commit and before ADP starts;
//       input 0 (the publication carries its format) and the CRF input are
//       never selected; the selection another writer left is written back
//   S2  SET_STREAM_FORMAT of an unbound input above 0 moves its context alone
//       to the new format, after that change's acknowledged commit; bound, the
//       input refuses it (STREAM_IS_RUNNING) and no context is written
//   S3  a commit the datapath never acknowledges writes no context
//   S4  a SET_STREAM_FORMAT whose commit is not acknowledged waits, IN_PROGRESS,
//       and writes nothing; once acknowledged it is done again, answered
//       SUCCESS, and its format reaches the input's context before that answer
//   S5  a change of another kind (SET_NAME, a STREAM_OUTPUT's format, one that
//       waited) writes no context, and nor does a pass with no change
//   S6  a SET_STREAM_FORMAT waits; its input is bound and its stream published
//       meanwhile; acknowledged, the change is not done again: the input keeps
//       its format and context, and the command is answered ENTITY_MISBEHAVING
//       at the wait's bound (IEEE 1722.1-2021 7.4.9, aecp.h applied). Unbound,
//       the same change is taken and a rebind publishes its stream on it
//   S7  as S6, acknowledged while the input is bound and its probe unanswered
//   S8  as S6, never acknowledged within the wait: the timeout keeps the format
//       in force, the late acknowledgement moves no context, and the refusal
//       ends with the wait (another input's change is taken)
//   S9  bound and unbound again while the change waits: acknowledged, it is
//       done again, its context written before its SUCCESS, and a rebind
//       publishes its stream on the new format
//   S10 SET_CONFIGURATION writes every context at its format in force; one that
//       waits while an input is bound meanwhile is not done again
//   S11 at an input's index, with that input bound and its stream published, a
//       change of another type (STREAM_OUTPUT n's SET_STREAM_FORMAT, which waits)
//       or of another kind (SET_NAME of input n) is taken and writes no context
//   S12 STREAM_INPUT 0 narrowed to one channel, the mappings naming its
//       channels removed first, is kept across a power cut: the boot's restore
//       takes it while the datapath's map store still holds its reset set, whose
//       rows the narrowed format would leave unmapped (REQUIREMENTS.md, the
//       persisted inventory; Milan v1.2 5.3.8.1, 5.3.13). At 1x1/1if that set
//       maps input 0's channels; at 8x8/1if it maps none. The far model keeps
//       the store and judges the verdict from it, as the datapath does
//   S13 every STREAM_INPUT's saved binding is restored at power-on; its
//       talker declares the stream's Talker Advertise (or Failed) before it
//       is discovered and probed, and is then quiet; once the probe is
//       answered the input declares its Listener Ready (Asking Failed) in
//       THE TRANSMIT's next MRPDU, within a JoinTime, and GET_STREAM_INFO
//       shows REGISTERING (and REGISTERING_FAILED) (#969; Milan v1.2 5.3.8.5,
//       5.5.3.5.18 step 4, Tables 5.9, 5.10)
//   S14 as S13 after BIND_RX while bound: each input is re-bound to another
//       stream, whose Talker has been declared all along

#include <gtest/gtest.h>

#include <algorithm>
#include <cstdint>
#include <cstdio>
#include <map>
#include <string>
#include <vector>

#include "acmp_fake.hpp"
#include "fw_gtest.hpp"
#include "plat_bus.hpp"

#include "ctrl_plat.h"
#include "ctrl_plat_policy_gen.h"
extern "C" {
#include "host/nvm_fmodel.h"
}
#include "mbx_hal.h"
#include "mbx_model.h"
// the store's headers carry no extern "C", and its shape header asserts in C11's spelling
#define _Static_assert static_assert
extern "C" {
#include "nvm_store.h"
}
#undef _Static_assert

FW_TALLY_LABEL("ctrl split platform sink formats (host model, " PLAT_TEST_SHAPE ")");

#ifndef PLAT_SINKS_MIN
#error "PLAT_SINKS_MIN, the AAF inputs above 0 the shape holds, comes from the arm (plat_arms.arm_platsinks)"
#endif

namespace {

using plat_bus::bus;
using plat_bus::kCsr;

constexpr std::uint16_t kStreamInput = 5u;          // IEEE 1722.1-2021 Table 7-1
constexpr unsigned kFormatAt = 74u;                  // a STREAM_INPUT's current_format (7.2.6)
constexpr unsigned kFormatsAt = 82u;                 // its formats_offset, then number_of_formats
constexpr unsigned kInterfaceAt = 126u;              // its avb_interface_index
constexpr std::uint8_t kAaf = 0x02u;                 // IEEE 1722-2016 Table 6
constexpr std::uint32_t kOtherSelection = 0x103u;    // talker 3, as MAAP's destination writes leave it
constexpr std::uint64_t kTwoChannels = 0x0205022000806000ull;  // AAF PCM32 48 kHz 2ch, in the Base family
// IEEE 1722.1-2021 Table 7-126
constexpr unsigned kSuccess = 0u;
constexpr unsigned kInProgress = 9u;
constexpr unsigned kEntityMisbehaving = 10u;
constexpr unsigned kStreamIsRunning = 12u;
// IEEE 1722.1-2021 Table 7-125
constexpr std::uint16_t kSetConfiguration = 0x0006u;
constexpr std::uint16_t kSetStreamFormat = 0x0008u;

// One mailbox access, with the CSR accesses before it.
struct Mbx {
    std::size_t plat;   // bus().log.size() when it was made
    bool write;
    std::uint32_t offset;
    std::uint32_t value;
};

mbx_model fabric;
std::vector<Mbx> mailbox;

struct Far {
    bool ack = true;
    std::vector<std::size_t> commits;   // mailbox.size() at each F_COMMIT
    // The datapath's map store, kept when `store` is set (S12): the configuration's reset set from power-on, moved
    // only by the EDIT window's committed records, as milan_datapath.sv's transaction server keeps it; each beat
    // accepted. SET_STREAM_FORMAT's verdict is then the datapath's from that store (its sfv_verdict_w): bit 0
    // supported, which this model takes as so (the family decode is the datapath's), and bit 1 every channel the
    // store's rows reference for the stream still in the proposal (its channels_per_frame, bits 31:22). Unset, the
    // verdict is 3 and every window but GSI's is silent.
    bool store = false;
    bool seeded = false;
    std::map<std::pair<unsigned, unsigned>, std::vector<aecp_mapping>> live;   // port (type, index): its rows
    void power_on() {
        live.clear();
        seeded = false;
    }
    // the store's reset set, the generated maps' defaults, once the image has composed them
    void seed() {
        if (seeded) return;
        const aecp_config& cfg = ctrl_plat.aecp.core.cfg;
        for (std::size_t k = 0; k < cfg.map_count; ++k) {
            const aecp_map& m = cfg.maps[k];
            live[{m.type, m.index}].assign(m.defaults, m.defaults + m.default_count);
        }
        seeded = true;
    }
    std::uint64_t verdict(const std::uint32_t* r) {
        if (!store) return 3u;
        seed();
        const unsigned type = r[0] & 0xffffu, index = r[0] >> 16;
        const unsigned channels = static_cast<unsigned>(r[2] >> 22) & 0x3ffu;
        const unsigned port = type == kStreamInput ? 14u : 15u;   // STREAM_PORT_INPUT, STREAM_PORT_OUTPUT
        unsigned need = 0;
        for (const auto& [key, rows] : live) {
            for (const aecp_mapping& m : rows) {
                if (key.first == port && m.stream == index) need = std::max(need, m.channel + 1u);
            }
        }
        return 1u | (need <= channels ? 2u : 0u);
    }
    std::uint64_t edit(const std::uint32_t* r) {
        seed();
        const aecp_mapping m{static_cast<std::uint16_t>(r[3] >> 16), static_cast<std::uint16_t>(r[3]),
                             static_cast<std::uint16_t>(r[2] >> 16), static_cast<std::uint16_t>(r[2])};
        auto& rows = live[{r[0] & 0xffffu, r[0] >> 16}];
        if ((r[1] & 7u) == 5u) {   // a committed record
            const auto at = std::find_if(rows.begin(), rows.end(), [&](const aecp_mapping& x) {
                return x.stream == m.stream && x.channel == m.channel && x.cluster == m.cluster &&
                       x.cluster_channel == m.cluster_channel;
            });
            if (((r[1] >> 4) & 1u) != 0u && at != rows.end()) rows.erase(at);
            if (((r[1] >> 4) & 1u) == 0u && at == rows.end()) rows.push_back(m);
        }
        return 1u;
    }
    // SET_STREAM_FORMAT's verdict (GSI kind 0, selector 15) as above; the other GET_STREAM_INFO words are 0
    static mbx_model_reply answer(void* p, unsigned, unsigned w, const std::uint32_t* r, std::uint64_t* data) {
        auto& f = *static_cast<Far*>(p);
        *data = 0;
        if (w == MBX_WIN_EDIT && f.store) {
            *data = f.edit(r);
            return MBX_MODEL_ANSWER;
        }
        if (w != MBX_WIN_GSI || (r[1] & 3u) != 0u) return MBX_MODEL_SILENT;
        if (((r[1] >> 4) & 15u) == 15u) *data = f.verdict(r);
        return MBX_MODEL_ANSWER;
    }
    static bool commit(void* p, unsigned, const std::uint32_t*) {
        auto& f = *static_cast<Far*>(p);
        f.commits.push_back(mailbox.size());
        return f.ack;
    }
};

const ctrl_plat_policy kPolicy = CTRL_PLAT_POLICY_INIT;
const ctrl_plat_stream kStreams[CTRL_SRP_SOURCES] = CTRL_PLAT_STREAMS_INIT;

// The listener contexts' format words as the window decodes the writes from bus log position `from` on: each
// context's {FMT_HI, FMT_LO}, the log position of its last format write, the listener selections in order, and
// whether each format pair was followed by the selection's write back to `restore`.
struct Window {
    std::map<unsigned, std::uint32_t> lo, hi;
    std::map<unsigned, std::size_t> at;
    std::vector<unsigned> selected;
    bool restored = true;
    std::uint64_t format(unsigned n) const {
        return static_cast<std::uint64_t>(hi.at(n)) << 32 | lo.at(n);
    }
    bool holds(unsigned n) const { return lo.count(n) != 0u && hi.count(n) != 0u; }
};

Window window(std::size_t from, std::uint32_t restore) {
    Window w;
    std::uint32_t sel = restore;
    bool owed = false;
    for (std::size_t k = from; k < bus().log.size(); ++k) {
        const auto& a = bus().log[k];
        if (!a.write || a.address < kCsr || a.address >= kCsr + 0x10000u) continue;
        const auto offset = static_cast<std::uint32_t>(a.address - kCsr);
        const unsigned idx = sel & 0xFu;
        const bool listener = (sel & 0x100u) == 0u;
        if (offset == CTRL_PLAT_CSR_STRM_SEL) {
            if (owed) w.restored = w.restored && a.value == restore;
            owed = false;
            sel = a.value;
            if ((sel & 0x100u) == 0u) w.selected.push_back(sel & 0xFu);
        } else if (offset == CTRL_PLAT_CSR_STRMW_FMT_LO && listener) {
            w.lo[idx] = a.value;
            w.at[idx] = k;
            owed = true;
        } else if (offset == CTRL_PLAT_CSR_STRMW_FMT_HI && listener) {
            w.hi[idx] = a.value;
            w.at[idx] = k;
            owed = true;
        }
    }
    w.restored = w.restored && !owed;
    return w;
}

std::uint64_t be(const std::uint8_t* p, unsigned n) {
    std::uint64_t v = 0;
    for (unsigned k = 0; k < n; ++k) v = v << 8 | p[k];
    return v;
}

// The current configuration's AAF STREAM_INPUTs above 0 on interface 0, which each have a receive-monitor
// context, by index: their current formats.
std::map<unsigned, std::uint64_t> context_formats() {
    std::map<unsigned, std::uint64_t> out;
    const aecp_model* model = ctrl_plat.aecp.core.cfg.model;
    for (std::size_t k = 0; k < model->count; ++k) {
        const aecp_descriptor& d = model->descriptors[k];
        if (d.type == kStreamInput && d.configuration == ctrl_plat.aecp.core.configuration && d.index != 0u &&
            d.length >= kInterfaceAt + 2u && d.value[kFormatAt] == kAaf && be(d.value + kInterfaceAt, 2) == 0u) {
            out[d.index] = be(d.value + kFormatAt, 8);
        }
    }
    return out;
}

// What the formats are for, watched at every mailbox access once on: the listener contexts' words, decoded from
// the bus log as the window takes them from the boot on, against each input's current format whenever ACMP has
// its binding's stream published (from the access that publishes it, the first a PDU of it can follow, a
// boundary), and against each SET_STREAM_FORMAT of such an input answered SUCCESS when that answer leaves.
struct Coherence {
    bool on = false;
    std::size_t upto = 0;
    std::uint32_t sel = kOtherSelection;
    std::map<unsigned, std::uint32_t> lo, hi;
    std::map<unsigned, std::uint64_t> stream;   // each context's stream as last published
    unsigned checks = 0, stale = 0, boundaries = 0, answers = 0, early = 0;
    std::string first;                          // the first stale observation
    bool holds(unsigned n) const { return lo.count(n) != 0u && hi.count(n) != 0u; }
    std::uint64_t words(unsigned n) const {
        return holds(n) ? static_cast<std::uint64_t>(hi.at(n)) << 32 | lo.at(n) : 0u;
    }
    void feed() {
        for (; upto < bus().log.size(); ++upto) {
            const auto& a = bus().log[upto];
            if (!a.write || a.address < kCsr || a.address >= kCsr + 0x10000u) continue;
            const auto offset = static_cast<std::uint32_t>(a.address - kCsr);
            if (offset == CTRL_PLAT_CSR_STRM_SEL) {
                sel = a.value;
            } else if ((sel & 0x100u) == 0u && offset == CTRL_PLAT_CSR_STRMW_FMT_LO) {
                lo[sel & 0xFu] = a.value;
            } else if ((sel & 0x100u) == 0u && offset == CTRL_PLAT_CSR_STRMW_FMT_HI) {
                hi[sel & 0xFu] = a.value;
            }
        }
    }
    void observe() {
        if (!on) return;
        feed();
        for (const auto& [n, format] : context_formats()) {
            const acmp_sink& s = ctrl_plat.app.acmp.acmp.sinks[n];
            const std::uint64_t sid = s.published_bound ? s.published_stream : 0u;
            if (sid != 0u) {
                ++checks;
                if (stream[n] == 0u) ++boundaries;
                if (words(n) != format && stale++ == 0u) {
                    char text[96];
                    std::snprintf(text, sizeof text, "input %u: current %016llx, context %016llx", n,
                                  static_cast<unsigned long long>(format),
                                  static_cast<unsigned long long>(words(n)));
                    first = text;
                }
            }
            stream[n] = sid;
        }
    }
    void sent(const mbx_model_tx* t) {
        if (!on || t == nullptr || t->len < 50u || t->bytes[14] != 0xfbu || (t->bytes[15] & 0xfu) != 1u ||
            be(t->bytes + 36, 2) != kSetStreamFormat || (be(t->bytes + 16, 2) >> 11) != kSuccess ||
            be(t->bytes + 38, 2) != kStreamInput) {
            return;
        }
        feed();
        const auto n = static_cast<unsigned>(be(t->bytes + 40, 2));
        if (context_formats().count(n) == 0u) return;
        ++answers;
        if (words(n) != be(t->bytes + 42, 8)) ++early;
    }
};
Coherence seen;

}  // namespace

// mbx_hal.h on the model, every access in the shared order
extern "C" std::uint32_t mbx_hal_read32(std::uint32_t offset) {
    seen.observe();
    const std::uint32_t value = mbx_model_read(&fabric, offset);
    mailbox.push_back({bus().log.size(), false, offset, value});
    return value;
}

extern "C" void mbx_hal_write32(std::uint32_t offset, std::uint32_t value) {
    seen.observe();
    mailbox.push_back({bus().log.size(), true, offset, value});
    const std::uint32_t sent = fabric.tx_sent;
    mbx_model_write(&fabric, offset, value, 0xFu);
    for (std::uint32_t k = sent; k < fabric.tx_sent; ++k) seen.sent(mbx_model_tx_frame(&fabric, k));
}

extern "C" void mbx_hal_wait(void) {}

namespace {

struct Sinks : ::testing::Test {
    Far far{};
    mbx_model_far side{&far, Far::answer, Far::commit};
    ctrl_plat_env env{};
    nvm_flash flash{};

    void SetUp() override {
        bus().reset();
        bus().csr[CTRL_PLAT_CSR_STRM_SEL] = kOtherSelection;
        seen = Coherence{};
        mailbox.clear();
        mbx_model_reset(&fabric);
        mbx_model_far_bind(&fabric, &side);
        for (unsigned i = 0; i < MBX_N_IF; ++i) mbx_model_set_link(&fabric, i, true);
        nvm_fmodel_blank();
        nvm_fmodel_power_on();
        nvm_fmodel_window(NVM_SLOT_A, NVM_SLOT_B + NVM_SLOT_BYTES);
        nvm_fmodel_times(1000, 100);
        flash = {nvm_fmodel_port.read, nvm_fmodel_port.program, nvm_fmodel_port.erase, nvm_fmodel_port.busy,
                 nvm_fmodel_port.now_us, nvm_fmodel_port.ctx};
        env.flash = &flash;
        env.csr = kCsr;
        env.uart = plat_bus::kUartRegs;
        env.policy = &kPolicy;
        env.streams = kStreams;
        env.aaf_outputs = CTRL_PLAT_AAF_OUTPUTS;
        env.crf_output = CTRL_PLAT_CRF_OUTPUT;
        env.link_rate_bps = CTRL_PLAT_LINK_BPS;
        ctrl_plat_generated_image(&env);
    }
    // SRP keeps its one instance as its timer's owner (srp_mbx.h), so each case destroys it
    void TearDown() override {
        seen.on = false;
        srp_mbx_destroy(&ctrl_plat.srp);
        mbx_model_far_bind(&fabric, nullptr);
    }
    // The current configuration's STREAM_INPUTs, by index: the descriptor's current format and interface.
    struct Input {
        std::uint64_t format;
        unsigned interface;
    };
    std::map<unsigned, Input> inputs() const {
        std::map<unsigned, Input> out;
        const aecp_model* model = ctrl_plat.aecp.core.cfg.model;
        for (std::size_t n = 0; n < model->count; ++n) {
            const aecp_descriptor& d = model->descriptors[n];
            if (d.type == kStreamInput && d.configuration == ctrl_plat.aecp.core.configuration &&
                d.length >= kInterfaceAt + 2u) {
                out[d.index] = {be(d.value + kFormatAt, 8), static_cast<unsigned>(be(d.value + kInterfaceAt, 2))};
            }
        }
        return out;
    }
    // The AAF inputs above 0 on interface 0, which each have a receive-monitor context of their own.
    std::vector<unsigned> contexts() const {
        std::vector<unsigned> out;
        for (const auto& [n, in] : inputs()) {
            if (n != 0u && (in.format >> 56) == kAaf && in.interface == 0u) out.push_back(n);
        }
        return out;
    }
    // Whether the CSR access at bus log position p follows an acknowledged commit with no mailbox write
    // between: the last mailbox write before it is an F_COMMIT the face made, and a read after that commit,
    // its acknowledgement's, precedes p too (mbx_face_commit).
    bool after_acknowledged_commit(std::size_t p) const {
        std::size_t last = mailbox.size();
        for (std::size_t k = 0; k < mailbox.size() && mailbox[k].plat <= p; ++k) {
            if (mailbox[k].write) last = k;
        }
        if (last == mailbox.size()) return false;
        bool commit = false;
        for (const std::size_t c : far.commits) commit = commit || c == last + 1u;
        return commit && last + 1u < mailbox.size() && !mailbox[last + 1u].write && mailbox[last + 1u].plat <= p;
    }
    // The bus log position after the face's first publication with F_CTRL.READY set (the open's,
    // aecp_face_open) was committed and acknowledged: its READY write, then an F_COMMIT, then the read that
    // found it taken; SIZE_MAX for none.
    std::size_t ready_published() const {
        const std::uint32_t ctrl = MBX_FACE_BASE + MBX_FACE_REG_F_CTRL;
        const std::uint32_t commit = MBX_FACE_BASE + MBX_FACE_REG_F_COMMIT;
        std::size_t k = 0;
        while (k < mailbox.size() && !(mailbox[k].write && mailbox[k].offset == ctrl &&
                                       ((mailbox[k].value >> MBX_F_CTRL_READY_LSB) & 1u) != 0u)) {
            ++k;
        }
        while (k < mailbox.size() && !(mailbox[k].write && mailbox[k].offset == commit)) ++k;
        while (k < mailbox.size() && mailbox[k].write) ++k;
        return k < mailbox.size() ? mailbox[k].plat : SIZE_MAX;
    }
    // The bus log position at the first write to TMR_CMD arming interface 0's ADP slot (ADP starts).
    std::size_t adp_start() const {
        for (const auto& a : mailbox) {
            const std::uint32_t slot = (a.value >> MBX_TMR_CMD_SLOT_LSB) & ((1u << MBX_TMR_CMD_SLOT_WIDTH) - 1u);
            const std::uint32_t op = (a.value >> MBX_TMR_CMD_OP_LSB) & ((1u << MBX_TMR_CMD_OP_WIDTH) - 1u);
            if (a.write && a.offset == MBX_REG_TMR_CMD && slot == CTRL_APP_ADP_FIRST_SLOT && op == MBX_TMR_OP_ARM) {
                return a.plat;
            }
        }
        return bus().log.size();
    }
    void steps(unsigned n) {
        for (unsigned k = 0; k < n; ++k) ctrl_plat_step();
    }
    // An AEM command (IEEE 1722.1-2021 9.2.1.2) to the entity, as the datapath delivers it.
    bool send(std::uint16_t cmd, const std::vector<std::uint8_t>& payload, std::uint16_t seq) {
        std::vector<std::uint8_t> f(38, 0);
        const auto put = [&](std::size_t at, std::uint64_t v, unsigned bytes) {
            for (unsigned k = 0; k < bytes; ++k) f[at + k] = static_cast<std::uint8_t>(v >> (8u * (bytes - 1u - k)));
        };
        put(0, ctrl_plat.config.entity->mac, 6);
        put(6, 0x020000000081ull, 6);
        put(12, 0x22f0u, 2);
        f[14] = 0xfbu;                   // AECP, AEM_COMMAND
        put(16, 12u + payload.size(), 2);  // control_data_length: controller, sequence, command and the payload
        put(18, ctrl_plat.config.entity->entity_id, 8);
        put(26, 0x1020304050607080ull, 8);
        put(34, seq, 2);
        put(36, cmd, 2);
        f.insert(f.end(), payload.begin(), payload.end());
        return mbx_model_rx(&fabric, f.data(), f.size(), 0);
    }
    // The statuses of the entity's AEM responses to `cmd` with `seq`, in the order they left.
    std::vector<int> statuses(std::uint16_t cmd, std::uint16_t seq) const {
        std::vector<int> out;
        for (std::uint32_t k = 0; k < fabric.tx_sent; ++k) {
            const auto* t = mbx_model_tx_frame(&fabric, k);
            if (t != nullptr && t->len >= 38u && t->bytes[14] == 0xfbu && (t->bytes[15] & 0xfu) == 1u &&
                be(t->bytes + 34, 2) == seq && be(t->bytes + 36, 2) == cmd) {
                out.push_back(static_cast<int>(be(t->bytes + 16, 2) >> 11));
            }
        }
        return out;
    }
    // Step until the command's final (not IN_PROGRESS) response has left: its status, or -1 within the turns.
    int final_status(std::uint16_t cmd, std::uint16_t seq, unsigned turns = 400u) {
        for (unsigned turn = 0; turn < turns; ++turn) {
            ctrl_plat_step();
            for (const int status : statuses(cmd, seq)) {
                if (status != static_cast<int>(kInProgress)) return status;
            }
        }
        return -1;
    }
    // SET_STREAM_FORMAT's payload (IEEE 1722.1-2021 7.4.9.1) for descriptor {type, n}
    static std::vector<std::uint8_t> format_payload(std::uint16_t type, unsigned n, std::uint64_t format) {
        std::vector<std::uint8_t> payload(12, 0);
        for (unsigned k = 0; k < 2; ++k) payload[k] = static_cast<std::uint8_t>(type >> (8u * (1u - k)));
        for (unsigned k = 0; k < 2; ++k) payload[2 + k] = static_cast<std::uint8_t>(n >> (8u * (1u - k)));
        for (unsigned k = 0; k < 8; ++k) payload[4 + k] = static_cast<std::uint8_t>(format >> (8u * (7u - k)));
        return payload;
    }
    // SET_STREAM_FORMAT of descriptor {type, n}: its final status
    int set_format(std::uint16_t type, unsigned n, std::uint64_t format, std::uint16_t seq) {
        return send(kSetStreamFormat, format_payload(type, n, format), seq) ? final_status(kSetStreamFormat, seq) : -1;
    }
    int set_format(unsigned n, std::uint64_t format, std::uint16_t seq) { return set_format(kStreamInput, n, format, seq); }
    // SET_CONFIGURATION (7.4.7.1) of the configuration in force
    bool set_configuration(std::uint16_t seq) {
        std::vector<std::uint8_t> payload(4, 0);
        payload[2] = static_cast<std::uint8_t>(ctrl_plat.aecp.core.configuration >> 8);
        payload[3] = static_cast<std::uint8_t>(ctrl_plat.aecp.core.configuration);
        return send(kSetConfiguration, payload, seq);
    }
    // The boot to READY, then every mailbox access watched (Coherence).
    bool ready() {
        if (ctrl_plat_boot(&env) != CTRL_PLAT_READY) return false;
        seen.on = true;
        return true;
    }
    // A command `cmd` sent, its commit held: true once its one response, IN_PROGRESS, has left and the change waits.
    bool held(std::uint16_t cmd, std::uint16_t seq) {
        for (unsigned turn = 0; turn < 200u && statuses(cmd, seq).empty(); ++turn) ctrl_plat_step();
        const auto s = statuses(cmd, seq);
        return s.size() == 1u && s.front() == static_cast<int>(kInProgress) && ctrl_plat.aecp.core.waiting;
    }
    bool hold_format(unsigned n, std::uint64_t to, std::uint16_t seq) {
        far.ack = false;
        return send(kSetStreamFormat, format_payload(kStreamInput, n, to), seq) && held(kSetStreamFormat, seq);
    }
    // The datapath acknowledges the commit it held.
    void acknowledge() {
        far.ack = true;
        mbx_model_face_ack(&fabric, 0);
    }
    // A waiting command's final status at the wait's bound (AECP_WAIT_MS after it, the clock not moved since),
    // or -2 if one left before it.
    int at_bound(std::uint16_t cmd, std::uint16_t seq) {
        steps(20);
        for (const int status : statuses(cmd, seq)) {
            if (status != static_cast<int>(kInProgress)) return -2;
        }
        mbx_model_advance_ms(&fabric, AECP_WAIT_MS);
        return final_status(cmd, seq);
    }
    // A controller's ACMP command `msg` (IEEE 1722.1-2021 8.2.1) to the entity's listener n, as the datapath
    // delivers it.
    bool acmp(std::uint8_t msg, unsigned n, std::uint16_t talker_uid = 0u) {
        acmp_test::Pdu c;
        c.msg = msg;
        c.controller = acmp_test::kCtl1;
        c.talker = acmp_test::kTkA;
        c.talker_uid = talker_uid;
        c.listener = ctrl_plat.config.entity->entity_id;
        c.listener_uid = static_cast<std::uint16_t>(n);
        const auto frame = acmp_test::acmpdu(c);
        return mbx_model_rx(&fabric, frame.data(), frame.size(), 0);
    }
    static acmp_sink_view sink(unsigned n) {
        acmp_sink_view v{};
        (void)acmp_view(&ctrl_plat.app.acmp.acmp, n, &v);
        return v;
    }
    // BIND_RX (true) or UNBIND_RX of listener n, stepped until taken.
    bool bind(unsigned n, bool bound) {
        if (!acmp(bound ? spec::MSG_BIND_RX_COMMAND : spec::MSG_UNBIND_RX_COMMAND, n)) return false;
        for (unsigned turn = 0; turn < 400u && sink(n).bound != bound; ++turn) ctrl_plat_step();
        steps(20);  // the responses and a bind's probe leave, one owed frame a pass
        return sink(n).bound == bound;
    }
    // The talker's answer to the newest PROBE_TX_COMMAND of listener n sent from frame `since` on (Milan v1.2
    // 5.5.3.5.3), stepped until the binding settles with its stream.
    bool answer_probe(unsigned n, std::uint32_t since, unsigned variant = 0u) {
        for (std::uint32_t k = fabric.tx_sent; k-- > since;) {
            const auto* tx = mbx_model_tx_frame(&fabric, k);
            if (tx == nullptr || tx->len < 70u || tx->bytes[14] != 0xfcu ||
                (tx->bytes[15] & 15u) != spec::MSG_PROBE_TX_COMMAND || be(tx->bytes + 52, 2) != n) {
                continue;
            }
            acmp_test::Pdu r;
            r.msg = spec::MSG_PROBE_TX_RESPONSE;
            r.controller = acmp_test::kCtl1;
            r.talker = be(tx->bytes + 34, 8);
            r.talker_uid = static_cast<std::uint16_t>(be(tx->bytes + 50, 2));
            r.listener = ctrl_plat.config.entity->entity_id;
            r.listener_uid = static_cast<std::uint16_t>(n);
            r.seq = static_cast<std::uint16_t>(be(tx->bytes + 62, 2));
            r.stream_id = acmp_test::kSid + variant;
            r.dest_mac = acmp_test::kDa + variant;
            r.vlan = 2u;
            const auto frame = acmp_test::acmpdu(r);
            if (!mbx_model_rx(&fabric, frame.data(), frame.size(), 0)) return false;
            for (unsigned turn = 0; turn < 400u && !sink(n).settled; ++turn) ctrl_plat_step();
            return sink(n).settled && sink(n).stream.stream_id == acmp_test::kSid + variant;
        }
        return false;
    }
    // While watched, every published stream's context held its input's current format, and no SET_STREAM_FORMAT's
    // SUCCESS left before its context held it.
    static void coherent(const char* label) {
        EXPECT_EQ(seen.stale, 0u) << label << " a published stream's context holds its input's current format ("
                                  << seen.first << ")";
        EXPECT_EQ(seen.early, 0u) << label << " no SET_STREAM_FORMAT's SUCCESS leaves before its context holds it";
    }
    // Every context written since `from` holds the format in force, and every context was written.
    void every_context_in_force(std::size_t from, const char* what) {
        const auto all = inputs();
        const Window w = window(from, kOtherSelection);
        for (const unsigned n : contexts()) {
            if (!w.holds(n)) {
                ADD_FAILURE() << what << " rewrites every context at its format in force: input " << n << " holds none";
                continue;
            }
            EXPECT_EQ(w.format(n), all.at(n).format) << what << " rewrites every context at its format in force: input "
                                                     << n;
        }
        EXPECT_EQ(w.lo.size(), contexts().size()) << what << " writes no other context";
        EXPECT_TRUE(w.restored) << what << ": the selection another writer left is written back";
    }
};

TEST_F(Sinks, S1EveryAafInputAboveZeroHoldsItsFormatAtReady) {
    ASSERT_EQ(ctrl_plat_boot(&env), CTRL_PLAT_READY) << "S1 the boot reaches its ready state";
    const auto all = inputs();
    const auto want = contexts();
    EXPECT_GE(want.size(), static_cast<std::size_t>(PLAT_SINKS_MIN))
        << "S1 the shape holds its AAF inputs above 0 (" PLAT_TEST_SHAPE ")";
    ASSERT_FALSE(far.commits.empty()) << "S1 the face is committed before AECP opens";
    const std::size_t adp = adp_start();
    const std::size_t ready = ready_published();
    ASSERT_NE(ready, SIZE_MAX) << "S1 the face publishes READY and it is acknowledged";
    const Window w = window(0, kOtherSelection);
    for (const unsigned n : want) {
        if (!w.holds(n)) {
            ADD_FAILURE() << "S1 every AAF input above 0 holds its current format: input " << n << " holds none";
            continue;
        }
        EXPECT_EQ(w.format(n), all.at(n).format) << "S1 every AAF input above 0 holds its current format: input " << n;
        EXPECT_GE(w.at.at(n), ready) << "S1 written after the open's acknowledged publication: input " << n;
        EXPECT_LT(w.at.at(n), adp) << "S1 written before ADP starts: input " << n;
    }
    // a context is judged on its input's current format's subtype (ctrl_plat_csr_sink_context), so each format such
    // an input advertises (IEEE 1722.1-2021 7.2.6, formats_offset and number_of_formats) is AAF, and a change to any
    // of them keeps its context
    const aecp_model* model = ctrl_plat.aecp.core.cfg.model;
    for (std::size_t k = 0; k < model->count; ++k) {
        const aecp_descriptor& d = model->descriptors[k];
        if (d.type != kStreamInput || d.configuration != ctrl_plat.aecp.core.configuration ||
            std::find(want.begin(), want.end(), d.index) == want.end()) {
            continue;
        }
        const auto start = static_cast<std::size_t>(be(d.value + kFormatsAt, 2));
        const auto count = static_cast<std::size_t>(be(d.value + kFormatsAt + 2u, 2));
        ASSERT_LE(start + 8u * count, static_cast<std::size_t>(d.length)) << "S1 input " << d.index << "'s formats fit";
        for (std::size_t f = 0; f < count; ++f) {
            EXPECT_EQ(d.value[start + 8u * f], kAaf) << "S1 every format input " << d.index << " advertises is AAF";
        }
    }
    for (const unsigned n : w.selected) {
        EXPECT_NE(n, 0u) << "S1 input 0 is never selected (the publication carries its format)";
        EXPECT_TRUE(all.count(n) == 0u || (all.at(n).format >> 56) == kAaf)
            << "S1 the CRF input has no receive-monitor context: input " << n;
    }
    for (const auto& [n, word] : w.lo) {
        (void)word;
        EXPECT_NE(std::find(want.begin(), want.end(), n), want.end()) << "S1 no other listener context is written: "
                                                                       << n;
    }
    EXPECT_TRUE(w.restored) << "S1 the selection another writer left is written back";
    EXPECT_EQ(bus().word(CTRL_PLAT_CSR_STRM_SEL), kOtherSelection) << "S1 the selection another writer left is kept";
}

TEST_F(Sinks, S2SetStreamFormatMovesOnlyThatContextAndABoundInputRefuses) {
    ASSERT_TRUE(ready());
    const auto want = contexts();
    if (want.empty()) {
        // no AAF input above 0 at this shape: input 0's SET_STREAM_FORMAT, its first, is a change the face
        // publishes (the override is set), and it writes no context
        const std::size_t from = bus().log.size();
        const std::size_t commits = far.commits.size();
        EXPECT_EQ(set_format(0u, inputs().at(0).format, 0x0201u), static_cast<int>(kSuccess))
            << "S2 SET_STREAM_FORMAT of input 0 is accepted";
        EXPECT_GT(far.commits.size(), commits) << "S2 input 0's change is published";
        EXPECT_TRUE(window(from, kOtherSelection).selected.empty()) << "S2 input 0's change writes no context";
        return;
    }
    const unsigned n = want.back();
    const std::uint64_t was = inputs().at(n).format;
    ASSERT_NE(was, kTwoChannels);
    std::size_t from = bus().log.size();
    ASSERT_EQ(set_format(n, kTwoChannels, 0x0201u), static_cast<int>(kSuccess))
        << "S2 SET_STREAM_FORMAT of an unbound input is accepted";
    Window w = window(from, kOtherSelection);
    ASSERT_TRUE(w.holds(n)) << "S2 SET_STREAM_FORMAT's new format reaches input " << n << "'s context";
    EXPECT_EQ(w.format(n), kTwoChannels) << "S2 SET_STREAM_FORMAT's new format reaches input " << n << "'s context";
    EXPECT_EQ(w.lo.size(), 1u) << "S2 that input's context alone is written";
    EXPECT_TRUE(after_acknowledged_commit(w.at.at(n))) << "S2 written after the change's acknowledged commit";
    EXPECT_TRUE(w.restored) << "S2 the selection another writer left is written back";
    // a controller binds input n, as the datapath delivers it; the input then refuses a format
    acmp_test::Pdu bind;
    bind.msg = spec::MSG_BIND_RX_COMMAND;
    bind.controller = acmp_test::kCtl1;
    bind.talker = acmp_test::kTkA;
    bind.listener = ctrl_plat.config.entity->entity_id;
    bind.listener_uid = static_cast<std::uint16_t>(n);
    const auto frame = acmp_test::acmpdu(bind);
    ASSERT_TRUE(mbx_model_rx(&fabric, frame.data(), frame.size(), 0)) << "S2 the bind reaches the mailbox";
    acmp_sink_view sink{};
    for (unsigned turn = 0; turn < 400u && !sink.bound; ++turn) {
        ctrl_plat_step();
        ASSERT_TRUE(acmp_view(&ctrl_plat.app.acmp.acmp, static_cast<uint16_t>(n), &sink));
    }
    ASSERT_TRUE(sink.bound) << "S2 the bind is taken";
    from = bus().log.size();
    EXPECT_EQ(set_format(n, was, 0x0202u), static_cast<int>(kStreamIsRunning))
        << "S2 a bound input refuses SET_STREAM_FORMAT";
    EXPECT_TRUE(window(from, kOtherSelection).selected.empty()) << "S2 a refused change writes no context";
    coherent("S2");
}

TEST_F(Sinks, S3AnUnacknowledgedCommitWritesNoContext) {
    far.ack = false;
    EXPECT_EQ(ctrl_plat_boot(&env), CTRL_PLAT_AECP) << "S3 no acknowledgement, no AECP";
    EXPECT_FALSE(far.commits.empty()) << "S3 the face was offered";
    EXPECT_TRUE(window(0, kOtherSelection).selected.empty()) << "S3 a commit never acknowledged writes no context";
}

TEST_F(Sinks, S4AChangeWaitingForItsAcknowledgementIsWrittenOnceInForce) {
    ASSERT_TRUE(ready());
    const auto want = contexts();
    const unsigned n = want.empty() ? 0u : want.back();
    const std::uint64_t to = want.empty() ? inputs().at(0).format : kTwoChannels;
    const std::size_t from = bus().log.size();
    far.ack = false;
    ASSERT_TRUE(send(kSetStreamFormat, format_payload(kStreamInput, n, to), 0x0301u))
        << "S4 the command reaches the mailbox";
    for (unsigned turn = 0; turn < 200u && statuses(0x0008u, 0x0301u).empty(); ++turn) ctrl_plat_step();
    steps(50);
    const auto first = statuses(0x0008u, 0x0301u);
    ASSERT_FALSE(first.empty()) << "S4 the change waits, IN_PROGRESS";
    EXPECT_EQ(first.front(), static_cast<int>(kInProgress)) << "S4 the change waits, IN_PROGRESS (" << first.size()
                                                             << " responses, last " << first.back() << ")";
    EXPECT_TRUE(window(from, kOtherSelection).selected.empty())
        << "S4 a change waiting for its acknowledgement writes no context";
    const std::size_t acked = bus().log.size();
    far.ack = true;
    mbx_model_face_ack(&fabric, 0);
    EXPECT_EQ(final_status(0x0008u, 0x0301u), static_cast<int>(kSuccess))
        << "S4 once acknowledged the change is done again and answered SUCCESS";
    steps(20);
    const Window w = window(acked, kOtherSelection);
    if (want.empty()) {
        EXPECT_TRUE(w.selected.empty()) << "S4 input 0's change writes no context";
        return;
    }
    ASSERT_TRUE(w.holds(n)) << "S4 the change done again reaches input " << n << "'s context";
    EXPECT_EQ(w.format(n), to) << "S4 the change done again reaches input " << n << "'s context";
    EXPECT_EQ(w.lo.size(), 1u) << "S4 that input's context alone is written";
    // written after `acked`, the acknowledgement of the change's own commit, and before its SUCCESS left
    EXPECT_EQ(seen.answers, 1u) << "S4 its SUCCESS leaves once its context holds it";
    EXPECT_TRUE(w.restored) << "S4 the selection another writer left is written back";
    coherent("S4");
}

TEST_F(Sinks, S5AChangeOfAnotherKindWritesNoContext) {
    ASSERT_TRUE(ready());
    // SET_NAME (IEEE 1722.1-2021 7.4.17.1) of the ENTITY's name: a persisted setting, which the face commits
    std::vector<std::uint8_t> name(72, 0);
    name[8] = 'S';
    name[9] = '5';
    std::size_t from = bus().log.size();
    std::size_t commits = far.commits.size();
    ASSERT_TRUE(send(0x0010u, name, 0x0401u)) << "S5 SET_NAME reaches the mailbox";
    EXPECT_EQ(final_status(0x0010u, 0x0401u), static_cast<int>(kSuccess)) << "S5 SET_NAME is accepted";
    steps(20);
    EXPECT_GT(far.commits.size(), commits) << "S5 SET_NAME's setting is committed";
    EXPECT_TRUE(window(from, kOtherSelection).selected.empty()) << "S5 SET_NAME writes no context";
    // STREAM_OUTPUT 0's SET_STREAM_FORMAT, its first, so a change the face publishes; its commit held, it waits
    // and is done again once acknowledged
    const aecp_descriptor* out = nullptr;
    const aecp_model* model = ctrl_plat.aecp.core.cfg.model;
    for (std::size_t k = 0; k < model->count; ++k) {
        const aecp_descriptor& d = model->descriptors[k];
        if (d.type == 6u && d.index == 0u && d.configuration == ctrl_plat.aecp.core.configuration) out = &d;
    }
    ASSERT_NE(out, nullptr) << "S5 the image holds STREAM_OUTPUT 0";
    from = bus().log.size();
    commits = far.commits.size();
    far.ack = false;
    ASSERT_TRUE(send(kSetStreamFormat, format_payload(6u, 0u, be(out->value + kFormatAt, 8)), 0x0402u))
        << "S5 a STREAM_OUTPUT's SET_STREAM_FORMAT reaches the mailbox";
    ASSERT_TRUE(held(kSetStreamFormat, 0x0402u)) << "S5 a STREAM_OUTPUT's SET_STREAM_FORMAT waits, IN_PROGRESS";
    acknowledge();
    EXPECT_EQ(final_status(kSetStreamFormat, 0x0402u), static_cast<int>(kSuccess))
        << "S5 a STREAM_OUTPUT's SET_STREAM_FORMAT is done again and accepted";
    steps(20);
    EXPECT_GT(far.commits.size(), commits) << "S5 the output's format is committed";
    EXPECT_TRUE(window(from, kOtherSelection).selected.empty())
        << "S5 a STREAM_OUTPUT's SET_STREAM_FORMAT writes no context";
    // passes with no change, the clock moved past every module's timers
    from = bus().log.size();
    steps(50);
    mbx_model_advance_ms(&fabric, 2000u);
    steps(50);
    EXPECT_TRUE(window(from, kOtherSelection).selected.empty()) << "S5 a pass with no change writes no context";
    coherent("S5");
}

// The cases below bind an input whose change waits: at a shape with no AAF input above 0 there is none to bind.
#define SINKS_CONTEXT_OR_RETURN(label)                                                                          \
    const auto want = contexts();                                                                                \
    if (want.empty()) {                                                                                          \
        EXPECT_TRUE(window(0, kOtherSelection).selected.empty()) << label " no input has a context at this shape"; \
        return;                                                                                                  \
    }

TEST_F(Sinks, S6AWaitingChangeIsNotDoneAgainOntoAnInputBoundAndSettledMeanwhile) {
    ASSERT_TRUE(ready());
    SINKS_CONTEXT_OR_RETURN("S6")
    const unsigned n = want.back();
    const std::uint64_t was = inputs().at(n).format;
    ASSERT_NE(was, kTwoChannels);
    const std::size_t from = bus().log.size();
    ASSERT_TRUE(hold_format(n, kTwoChannels, 0x0601u)) << "S6 the change waits, IN_PROGRESS";
    EXPECT_EQ(inputs().at(n).format, was) << "S6 the waiting change is undone";
    std::uint32_t since = fabric.tx_sent;
    ASSERT_TRUE(bind(n, true)) << "S6 the bind is taken while the change waits";
    ASSERT_TRUE(answer_probe(n, since)) << "S6 the probe is answered and the binding settles with its stream";
    acknowledge();
    EXPECT_EQ(at_bound(kSetStreamFormat, 0x0601u), static_cast<int>(kEntityMisbehaving))
        << "S6 a change whose input was bound meanwhile is answered ENTITY_MISBEHAVING at the wait's bound";
    EXPECT_EQ(inputs().at(n).format, was) << "S6 the input keeps its format";
    const Window w = window(from, kOtherSelection);
    EXPECT_TRUE(!w.holds(n) || w.format(n) == was) << "S6 the input's context keeps its format";
    EXPECT_TRUE(sink(n).settled) << "S6 the binding stays settled";
    EXPECT_GT(seen.checks, 0u) << "S6 watched while its stream is published";
    // unbound, the same change is taken, and a rebind publishes its stream on it
    ASSERT_TRUE(bind(n, false)) << "S6 the unbind is taken";
    ASSERT_EQ(set_format(n, kTwoChannels, 0x0602u), static_cast<int>(kSuccess)) << "S6 unbound, the change is taken";
    since = fabric.tx_sent;
    ASSERT_TRUE(bind(n, true)) << "S6 the rebind is taken";
    ASSERT_TRUE(answer_probe(n, since)) << "S6 the rebind settles with its stream";
    EXPECT_EQ(seen.words(n), kTwoChannels) << "S6 the rebind's stream is published on the new format";
    EXPECT_EQ(seen.boundaries, 2u) << "S6 both streams are published while watched";
    coherent("S6");
}

TEST_F(Sinks, S7AWaitingChangeIsNotDoneAgainOntoAnInputBoundWithItsProbeUnanswered) {
    ASSERT_TRUE(ready());
    SINKS_CONTEXT_OR_RETURN("S7")
    const unsigned n = want.back();
    const std::uint64_t was = inputs().at(n).format;
    ASSERT_TRUE(hold_format(n, kTwoChannels, 0x0701u)) << "S7 the change waits, IN_PROGRESS";
    const std::uint32_t since = fabric.tx_sent;
    ASSERT_TRUE(bind(n, true)) << "S7 the bind is taken while the change waits";
    acknowledge();
    steps(20);
    ASSERT_TRUE(answer_probe(n, since)) << "S7 the probe answered after the acknowledgement settles the binding";
    EXPECT_EQ(at_bound(kSetStreamFormat, 0x0701u), static_cast<int>(kEntityMisbehaving))
        << "S7 a change whose input is bound, its probe unanswered, is answered ENTITY_MISBEHAVING at the wait's bound";
    EXPECT_EQ(inputs().at(n).format, was) << "S7 the input keeps its format";
    EXPECT_EQ(seen.words(n), was) << "S7 the input's context keeps its format";
    EXPECT_EQ(seen.boundaries, 1u) << "S7 its stream is published while watched";
    coherent("S7");
}

TEST_F(Sinks, S8AChangeNeverAcknowledgedInItsWaitKeepsTheFormatInForce) {
    ASSERT_TRUE(ready());
    SINKS_CONTEXT_OR_RETURN("S8")
    const unsigned n = want.back();
    const std::uint64_t was = inputs().at(n).format;
    ASSERT_TRUE(hold_format(n, kTwoChannels, 0x0801u)) << "S8 the change waits, IN_PROGRESS";
    const std::uint32_t since = fabric.tx_sent;
    ASSERT_TRUE(bind(n, true)) << "S8 the bind is taken while the change waits";
    ASSERT_TRUE(answer_probe(n, since)) << "S8 the probe is answered and the binding settles with its stream";
    EXPECT_EQ(at_bound(kSetStreamFormat, 0x0801u), static_cast<int>(kEntityMisbehaving))
        << "S8 a change never acknowledged within its wait is answered ENTITY_MISBEHAVING at the wait's bound";
    EXPECT_EQ(inputs().at(n).format, was) << "S8 the input keeps its format";
    const std::size_t late = bus().log.size();
    acknowledge();
    steps(50);
    const Window w = window(late, kOtherSelection);
    EXPECT_TRUE(!w.holds(n) || w.format(n) == was) << "S8 the late acknowledgement moves no context";
    EXPECT_EQ(seen.words(n), was) << "S8 the input's context keeps its format";
    // the refusal ends with the wait: another input's change is taken
    const unsigned m = want.front();
    if (m != n) {
        const std::size_t from = bus().log.size();
        EXPECT_EQ(set_format(m, kTwoChannels, 0x0802u), static_cast<int>(kSuccess))
            << "S8 the refusal ends with the wait: another input's change is taken";
        const Window other = window(from, kOtherSelection);
        EXPECT_TRUE(other.holds(m) && other.format(m) == kTwoChannels)
            << "S8 the refusal ends with the wait: another input's change reaches its context";
    }
    EXPECT_EQ(seen.boundaries, 1u) << "S8 its stream is published while watched";
    coherent("S8");
}

TEST_F(Sinks, S9AChangeWhoseInputIsUnboundAgainIsDoneAgainBeforeARebind) {
    ASSERT_TRUE(ready());
    SINKS_CONTEXT_OR_RETURN("S9")
    const unsigned n = want.back();
    ASSERT_TRUE(hold_format(n, kTwoChannels, 0x0901u)) << "S9 the change waits, IN_PROGRESS";
    std::uint32_t since = fabric.tx_sent;
    ASSERT_TRUE(bind(n, true)) << "S9 the bind is taken while the change waits";
    ASSERT_TRUE(answer_probe(n, since)) << "S9 the probe is answered and the binding settles with its stream";
    ASSERT_TRUE(bind(n, false)) << "S9 the unbind is taken while the change waits";
    acknowledge();
    EXPECT_EQ(final_status(kSetStreamFormat, 0x0901u), static_cast<int>(kSuccess))
        << "S9 unbound again before its acknowledgement, the change is done again and answered SUCCESS";
    EXPECT_EQ(inputs().at(n).format, kTwoChannels) << "S9 the input takes the new format";
    EXPECT_EQ(seen.words(n), kTwoChannels) << "S9 the change done again reaches input " << n << "'s context";
    EXPECT_EQ(seen.answers, 1u) << "S9 its SUCCESS leaves once its context holds it";
    since = fabric.tx_sent;
    ASSERT_TRUE(bind(n, true)) << "S9 the rebind is taken";
    ASSERT_TRUE(answer_probe(n, since)) << "S9 the rebind settles with its stream";
    EXPECT_EQ(seen.boundaries, 2u) << "S9 both streams are published while watched";
    coherent("S9");
}

TEST_F(Sinks, S10SetConfigurationWritesEveryContextAndOneWaitingIsNotDoneAgainOntoABoundInput) {
    ASSERT_TRUE(ready());
    SINKS_CONTEXT_OR_RETURN("S10")
    const unsigned n = want.back();
    // its first, so a change: its commit held, it waits, and an input is bound meanwhile
    far.ack = false;
    ASSERT_TRUE(set_configuration(0x0a01u)) << "S10 SET_CONFIGURATION reaches the mailbox";
    ASSERT_TRUE(held(kSetConfiguration, 0x0a01u)) << "S10 SET_CONFIGURATION waits, IN_PROGRESS";
    const std::uint32_t since = fabric.tx_sent;
    ASSERT_TRUE(bind(n, true)) << "S10 the bind is taken while the change waits";
    ASSERT_TRUE(answer_probe(n, since)) << "S10 the probe is answered and the binding settles with its stream";
    acknowledge();
    EXPECT_EQ(at_bound(kSetConfiguration, 0x0a01u), static_cast<int>(kEntityMisbehaving))
        << "S10 a SET_CONFIGURATION whose input was bound meanwhile is answered ENTITY_MISBEHAVING at the wait's bound";
    // unbound, it is taken: every context at its format in force
    ASSERT_TRUE(bind(n, false)) << "S10 the unbind is taken";
    const std::size_t from = bus().log.size();
    ASSERT_TRUE(set_configuration(0x0a02u)) << "S10 SET_CONFIGURATION reaches the mailbox";
    EXPECT_EQ(final_status(kSetConfiguration, 0x0a02u), static_cast<int>(kSuccess))
        << "S10 SET_CONFIGURATION is accepted";
    every_context_in_force(from, "S10 SET_CONFIGURATION");
    coherent("S10");
}

TEST_F(Sinks, S11AChangeOfAnotherTypeOrKindAtAContextsIndexIsTakenAndWritesNoContext) {
    ASSERT_TRUE(ready());
    SINKS_CONTEXT_OR_RETURN("S11")
    const unsigned n = want.back();
    const aecp_descriptor* out = nullptr;
    const aecp_model* model = ctrl_plat.aecp.core.cfg.model;
    for (std::size_t k = 0; k < model->count; ++k) {
        const aecp_descriptor& d = model->descriptors[k];
        if (d.type == 6u && d.index == n && d.configuration == ctrl_plat.aecp.core.configuration) out = &d;
    }
    ASSERT_NE(out, nullptr) << "S11 the image holds STREAM_OUTPUT " << n;
    const std::uint32_t since = fabric.tx_sent;
    ASSERT_TRUE(bind(n, true)) << "S11 input " << n << " is bound";
    ASSERT_TRUE(answer_probe(n, since)) << "S11 input " << n << "'s binding settles with its stream";
    // STREAM_OUTPUT n's SET_STREAM_FORMAT, its first, so a change: its commit held, it waits, and is acknowledged
    std::size_t from = bus().log.size();
    far.ack = false;
    ASSERT_TRUE(send(kSetStreamFormat, format_payload(6u, n, be(out->value + kFormatAt, 8)), 0x0b01u))
        << "S11 output " << n << "'s SET_STREAM_FORMAT reaches the mailbox";
    ASSERT_TRUE(held(kSetStreamFormat, 0x0b01u)) << "S11 output " << n << "'s SET_STREAM_FORMAT waits, IN_PROGRESS";
    acknowledge();
    EXPECT_EQ(final_status(kSetStreamFormat, 0x0b01u), static_cast<int>(kSuccess))
        << "S11 output " << n << "'s SET_STREAM_FORMAT is taken while input " << n << " is bound";
    steps(20);
    EXPECT_TRUE(window(from, kOtherSelection).selected.empty())
        << "S11 output " << n << "'s format change writes no context";
    // SET_NAME (IEEE 1722.1-2021 7.4.17.1) of STREAM_INPUT n itself: descriptor_type, descriptor_index, name_index,
    // configuration_index, then the name
    std::vector<std::uint8_t> name(72, 0);
    name[1] = static_cast<std::uint8_t>(kStreamInput);
    name[3] = static_cast<std::uint8_t>(n);
    name[8] = 'S';
    from = bus().log.size();
    ASSERT_TRUE(send(0x0010u, name, 0x0b02u)) << "S11 SET_NAME of input " << n << " reaches the mailbox";
    EXPECT_EQ(final_status(0x0010u, 0x0b02u), static_cast<int>(kSuccess))
        << "S11 SET_NAME of bound input " << n << " is taken";
    steps(20);
    EXPECT_TRUE(window(from, kOtherSelection).selected.empty()) << "S11 SET_NAME of input " << n << " writes no context";
    EXPECT_TRUE(sink(n).settled) << "S11 input " << n << "'s binding stays settled";
    EXPECT_GT(seen.checks, 0u) << "S11 watched while its stream is published";
    coherent("S11");
}

// The rows of STREAM_PORT_INPUT maps in force that name stream `n`, by port index.
std::map<unsigned, std::vector<aecp_mapping>> input_rows(unsigned n) {
    std::map<unsigned, std::vector<aecp_mapping>> out;
    const aecp_config& cfg = ctrl_plat.aecp.core.cfg;
    for (std::size_t k = 0; k < cfg.map_count; ++k) {
        const aecp_map& m = cfg.maps[k];
        if (m.type != 14u || m.configuration != ctrl_plat.aecp.core.configuration) continue;
        for (std::size_t r = 0; r < m.count; ++r) {
            if (m.rows[r].stream == n) out[m.index].push_back(m.rows[r]);
        }
    }
    return out;
}

TEST_F(Sinks, S12ANarrowedInputFormatIsKeptAcrossAPowerCut) {
    far.store = true;
    ASSERT_TRUE(ready());
    // a controller narrows STREAM_INPUT 0 to one channel of its family, removing first the mappings that name its
    // channels, which the narrowed format would leave unmapped (Milan v1.2 5.4.2.7)
    const std::uint64_t wide = inputs().at(0).format;
    const std::uint64_t narrow = (wide & ~(0x3ffull << 22)) | (1ull << 22);
    ASSERT_NE(narrow, wide) << "S12 input 0's format is wider than one channel";
    std::uint16_t seq = 0x0c01u;
    for (const auto& [port, rows] : input_rows(0)) {
        std::vector<std::uint8_t> payload(8 + 8 * rows.size(), 0);
        payload[1] = 14u;   // STREAM_PORT_INPUT
        payload[2] = static_cast<std::uint8_t>(port >> 8);
        payload[3] = static_cast<std::uint8_t>(port);
        payload[5] = static_cast<std::uint8_t>(rows.size());
        for (std::size_t k = 0; k < rows.size(); ++k) {
            const std::uint16_t w[4] = {rows[k].stream, rows[k].channel, rows[k].cluster, rows[k].cluster_channel};
            for (unsigned q = 0; q < 4; ++q) {
                payload[8 + 8 * k + 2 * q] = static_cast<std::uint8_t>(w[q] >> 8);
                payload[9 + 8 * k + 2 * q] = static_cast<std::uint8_t>(w[q]);
            }
        }
        ASSERT_TRUE(send(0x002du, payload, seq)) << "S12 REMOVE_AUDIO_MAPPINGS reaches the mailbox";
        ASSERT_EQ(final_status(0x002du, seq), static_cast<int>(kSuccess))
            << "S12 input 0's mappings at input port " << port << " are removed";
        ++seq;
        mbx_model_advance_ms(&fabric, AECP_PACE_MS);
    }
    ASSERT_TRUE(input_rows(0).empty()) << "S12 no mapping names input 0's channels";
    ASSERT_EQ(set_format(0, narrow, seq), static_cast<int>(kSuccess)) << "S12 input 0 is narrowed to one channel";
    ASSERT_EQ(inputs().at(0).format, narrow);
    // the saved state written back by the store's service on the loop's tick: both clocks 10 ms a pass
    const unsigned commits = nvm_store_status()->commits_ok;
    for (unsigned k = 0; k < 3000u && (nvm_store_status()->commits_ok == commits ||
                                       ctrl_plat.state.pending_count != 0u ||
                                       nvm_store_status()->phase != NVM_P_IDLE); ++k) {
        mbx_model_advance_ms(&fabric, 10u);
        nvm_fmodel_advance_us(10000u);
        ctrl_plat_step();
        ctrl_plat_step();
    }
    ASSERT_GT(nvm_store_status()->commits_ok, commits) << "S12 the change is written back";
    ASSERT_EQ(ctrl_plat.state.pending_count, 0u) << "S12 no record is still owed";
    // the cut: the fabric, the CPU and its memory from power-on; the flash keeps its contents, and the datapath's
    // map store holds its reset set again
    seen.on = false;
    srp_mbx_destroy(&ctrl_plat.srp);
    bus().reset();
    bus().csr[CTRL_PLAT_CSR_STRM_SEL] = kOtherSelection;
    mailbox.clear();
    mbx_model_reset(&fabric);
    mbx_model_far_bind(&fabric, &side);
    for (unsigned i = 0; i < MBX_N_IF; ++i) mbx_model_set_link(&fabric, i, true);
    nvm_fmodel_power_on();
    far.power_on();
    ASSERT_TRUE(ready()) << "S12 the boot after the cut reaches READY";
    EXPECT_EQ(inputs().at(0).format, narrow) << "S12 input 0's narrowed format is restored after the cut";
    EXPECT_TRUE(input_rows(0).empty()) << "S12 the mappings removed before the cut stay removed";
}

// ---- #969: a Talker registered before its input's binding settles -------------------------------------------------
// The talker's MSRP Talker Advertise (Failed: failure code 1) of stream v, JoinIn, to interface 0 (IEEE 802.1Q-2018
// 35.2.2.8, 10.8): StreamID kSid + v, destination kDa + v, VID 2, as answer_probe's PROBE_TX_RESPONSE carries them.
std::vector<std::uint8_t> talker_declaration(unsigned v, bool failed) {
    std::vector<std::uint8_t> value(failed ? 34u : 25u, 0);
    const auto put = [&](std::size_t at, std::uint64_t x, unsigned bytes) {
        for (unsigned k = 0; k < bytes; ++k) value[at + k] = static_cast<std::uint8_t>(x >> (8u * (bytes - 1u - k)));
    };
    put(0, acmp_test::kSid + v, 8);
    put(8, acmp_test::kDa + v, 6);
    put(14, 2u, 2);
    put(16, 224u, 2);
    put(18, 1u, 2);
    value[20] = 0x60u;
    if (failed) value[33] = 1u;
    std::vector<std::uint8_t> f = {0x01, 0x80, 0xc2, 0x00, 0x00, 0x0e, 0x02, 0x03, 0x04, 0x01, 0x02, 0x03, 0x22, 0xea,
                                   0x00, static_cast<std::uint8_t>(failed ? 2u : 1u),
                                   static_cast<std::uint8_t>(value.size())};
    const unsigned list = 2u + static_cast<unsigned>(value.size()) + 1u + 2u;
    f.push_back(static_cast<std::uint8_t>(list >> 8));
    f.push_back(static_cast<std::uint8_t>(list));
    f.push_back(0x00);
    f.push_back(0x01);  // no LeaveAll, one value
    f.insert(f.end(), value.begin(), value.end());
    f.push_back(36u);  // JoinIn
    f.insert(f.end(), {0, 0, 0, 0});
    return f;
}

// The Listener declaration of StreamID `sid` in MSRP frame `t`: 2 Ready, 1 Asking Failed, 0 none or withdrawn (a
// Message's type, attribute length and list length; a Listener vector's values, their events three to a byte and
// their declarations four to one, IEEE 802.1Q-2018 10.8, 35.2.2).
unsigned listener_of(const mbx_model_tx* t, std::uint64_t sid) {
    const std::uint8_t* end = t->bytes + t->len;
    for (const std::uint8_t* p = t->bytes + 15; p + 4 <= end && p[0] != 0; p += 4 + be(p + 2, 2)) {
        const std::uint8_t* last = p + 4 + be(p + 2, 2);
        for (const std::uint8_t* q = p + 4; p[0] == 3u && q + 2 <= last && be(q, 2) != 0u;) {
            const unsigned count = static_cast<unsigned>(be(q, 2) % 8192u);
            for (unsigned v = 0; v < count; ++v) {
                const unsigned packed = q[10 + v / 3];
                const unsigned event = v % 3 == 0 ? packed / 36 : v % 3 == 1 ? packed / 6 % 6 : packed % 6;
                const unsigned declaration = q[10 + (count + 2) / 3 + v / 4] >> (6 - 2 * (v % 4)) & 3u;
                if (be(q + 2, 8) + v == sid) return event == 5u ? 0u : declaration;
            }
            q += 10 + (count + 2) / 3 + (count + 3) / 4;
        }
    }
    return 0u;
}

struct Early : Sinks {
    static constexpr std::uint16_t kGetStreamInfo = 0x000fu;   // IEEE 1722.1-2021 Table 7-125
    static constexpr unsigned kJoinMs = CTRL_LOOP_JOIN_CS * 10u;
    // `ms` milliseconds pass, a pass a millisecond
    void pass(unsigned ms) {
        for (unsigned k = 0; k < ms; ++k) {
            mbx_model_advance_ms(&fabric, 1);
            ctrl_plat_step();
        }
    }
    // The first MSRP MRPDU the entity sent from frame `from` on, or nullptr
    static const mbx_model_tx* first_msrp(std::uint32_t from) {
        for (std::uint32_t k = from; k < fabric.tx_sent; ++k) {
            const auto* t = mbx_model_tx_frame(&fabric, k);
            if (t != nullptr && t->channel == MBX_CH_SRP && be(t->bytes + 12, 2) == 0x22eau) return t;
        }
        return nullptr;
    }
    // Whether the entity's MSRP MRPDUs from frame `from` on, by `by` ms, declare `sid`'s Listener as `kind`
    static bool declared_by(std::uint32_t from, std::uint64_t sid, unsigned kind, std::uint32_t by) {
        for (std::uint32_t k = from; k < fabric.tx_sent; ++k) {
            const auto* t = mbx_model_tx_frame(&fabric, k);
            if (t != nullptr && t->channel == MBX_CH_SRP && be(t->bytes + 12, 2) == 0x22eau && t->now_ms <= by &&
                listener_of(t, sid) == kind) {
                return true;
            }
        }
        return false;
    }
    // GET_STREAM_INFO of STREAM_INPUT n (IEEE 1722.1-2021 7.4.16): its SUCCESS response's flags and flags_ex
    bool stream_info(unsigned n, std::uint16_t seq, std::uint32_t* flags, std::uint32_t* flags_ex) {
        std::vector<std::uint8_t> payload(4, 0);
        payload[1] = static_cast<std::uint8_t>(kStreamInput);
        payload[3] = static_cast<std::uint8_t>(n);
        if (!send(kGetStreamInfo, payload, seq) || final_status(kGetStreamInfo, seq) != static_cast<int>(kSuccess)) {
            return false;
        }
        for (std::uint32_t k = fabric.tx_sent; k-- > 0;) {
            const auto* t = mbx_model_tx_frame(&fabric, k);
            if (t != nullptr && t->len >= 38u + 52u && t->bytes[14] == 0xfbu && be(t->bytes + 34, 2) == seq &&
                be(t->bytes + 36, 2) == kGetStreamInfo) {
                *flags = static_cast<std::uint32_t>(be(t->bytes + 42, 4));
                *flags_ex = static_cast<std::uint32_t>(be(t->bytes + 86, 4));
                return true;
            }
        }
        return false;
    }
    // The talker's answer to listener n's outstanding probe (PRB_W_RESP or PRB_W_RESP2) with stream v, then until
    // the binding reaches SRP: the time the answer met, the frame count when SRP took the binding, and whether it
    // settled and was delivered. What was owed before (a BIND_RX while bound owes its withdrawal) may leave first.
    bool answer_outstanding(unsigned n, unsigned v, std::uint32_t* from, std::uint32_t* at) {
        *at = fabric.now_ms;
        const srp_sink& s = ctrl_plat.srp.ifs[0].sinks[n];
        const auto taken = [&] { return s.bound && be(s.stream_id.bytes, 8) == acmp_test::kSid + v; };
        if (!answer_probe(n, 0u, v)) return false;
        for (unsigned turn = 0; turn < 400u && !taken(); ++turn) ctrl_plat_step();
        *from = fabric.tx_sent;
        return taken();
    }
    // Input n, its probe answered with stream v at `at`, SRP taking the binding at frame `from`: its Listener `kind`
    // (2 Ready, 1 Asking Failed) in THE TRANSMIT's next MRPDU, within a JoinTime of the answer, and GET_STREAM_INFO's
    // REGISTERING (flags_ex bit 31) and REGISTERING_FAILED (flags bit 25) (Milan v1.2 Tables 5.9, 5.10).
    void expect_declares(unsigned n, unsigned v, std::uint32_t from, std::uint32_t at, bool failed,
                         const std::string& what, std::uint16_t seq) {
        const unsigned kind = failed ? 1u : 2u;
        const auto* first = first_msrp(from);
        ASSERT_NE(first, nullptr) << what << ": an MRPDU follows the probe's answer, input " << n;
        EXPECT_EQ(listener_of(first, acmp_test::kSid + v), kind)
            << what << ": the Listener is declared in THE TRANSMIT's next MRPDU, input " << n;
        EXPECT_TRUE(declared_by(from, acmp_test::kSid + v, kind, at + kJoinMs))
            << what << ": the Listener is declared within a JoinTime of the probe's answer, input " << n;
        std::uint32_t flags = 0, flags_ex = 0;
        ASSERT_TRUE(stream_info(n, seq, &flags, &flags_ex)) << what << ": GET_STREAM_INFO of input " << n;
        EXPECT_EQ(flags_ex & 1u, 1u) << what << ": GET_STREAM_INFO shows REGISTERING, input " << n;
        EXPECT_EQ((flags & 0x40u) != 0u, failed)
            << what << ": GET_STREAM_INFO's REGISTERING_FAILED follows the kind registered, input " << n;
    }
    // Every listener answered as soon as its probe is outstanding, each with its own stream, then each judged
    void answer_every_probe(const std::vector<unsigned>& all, unsigned offset, bool failed, const std::string& what,
                            std::uint16_t seq) {
        std::map<unsigned, std::pair<std::uint32_t, std::uint32_t>> answered;
        for (unsigned ms = 0; ms < 6000u && answered.size() < all.size(); ++ms) {
            for (const unsigned n : all) {
                const auto state = sink(n).state;
                if (answered.count(n) == 0u && (state == ACMP_PRB_W_RESP || state == ACMP_PRB_W_RESP2)) {
                    std::uint32_t from = 0, at = 0;
                    ASSERT_TRUE(answer_outstanding(n, n + offset, &from, &at))
                        << what << ": input " << n << "'s probe is answered and its binding reaches SRP";
                    answered[n] = {from, at};
                    pass(6);
                }
            }
            pass(1);
        }
        ASSERT_EQ(answered.size(), all.size()) << what << ": every input probes";
        pass(kJoinMs + 10u);
        for (const unsigned n : all) {
            expect_declares(n, n + offset, answered[n].first, answered[n].second, failed, what,
                            static_cast<std::uint16_t>(seq + n));
        }
    }
    std::vector<unsigned> every_input() const {
        std::vector<unsigned> out;
        for (const auto& [n, in] : inputs()) {
            if (in.interface == 0u) out.push_back(n);
        }
        return out;
    }
};

TEST_F(Early, S13ASavedBindingRestoredAtPowerOnDeclaresATalkerRegisteredBeforeItSettled) {
    for (const bool failed : {false, true}) {
        const char* what = failed ? "S13 a Talker Failed registered before the restored binding settled"
                                  : "S13 a Talker Advertise registered before the restored binding settled";
        for (unsigned i = 0; i < MBX_N_IF; ++i) mbx_model_set_gm(&fabric, i, acmp_test::kGm0, 0);
        ASSERT_TRUE(ready());
        const auto all = every_input();
        ASSERT_FALSE(all.empty());
        for (const unsigned n : all) {
            const std::uint32_t since = fabric.tx_sent;
            ASSERT_TRUE(bind(n, true)) << what << ": input " << n << " is bound";
            ASSERT_TRUE(answer_probe(n, since, n)) << what << ": input " << n << " settles";
            pass(12);  // the ACMP channel's bucket refills (mbx_model.h, MBX_CH_ACMP_RATE_REFILL_MS)
        }
        // the saved state written back by the store's service on the loop's tick, both clocks 10 ms a pass (S12)
        const unsigned commits = nvm_store_status()->commits_ok;
        for (unsigned k = 0; k < 3000u && (nvm_store_status()->commits_ok == commits ||
                                           ctrl_plat.state.pending_count != 0u ||
                                           nvm_store_status()->phase != NVM_P_IDLE); ++k) {
            mbx_model_advance_ms(&fabric, 10u);
            nvm_fmodel_advance_us(10000u);
            ctrl_plat_step();
            ctrl_plat_step();
        }
        ASSERT_EQ(ctrl_plat.state.pending_count, 0u) << what << ": the bindings are saved";
        // the power cut, as S12's: the flash keeps its contents
        seen.on = false;
        srp_mbx_destroy(&ctrl_plat.srp);
        bus().reset();
        bus().csr[CTRL_PLAT_CSR_STRM_SEL] = kOtherSelection;
        mailbox.clear();
        mbx_model_reset(&fabric);
        mbx_model_far_bind(&fabric, &side);
        for (unsigned i = 0; i < MBX_N_IF; ++i) {
            mbx_model_set_link(&fabric, i, true);
            mbx_model_set_gm(&fabric, i, acmp_test::kGm0, 0);
        }
        nvm_fmodel_power_on();
        far.power_on();
        ASSERT_TRUE(ready()) << what << ": the boot after the cut reaches READY";
        for (const unsigned n : all) {
            ASSERT_TRUE(sink(n).bound) << what << ": input " << n << "'s binding is restored";
            ASSERT_FALSE(sink(n).settled) << what << ": input " << n << " probes again";
        }
        pass(400);
        // the talker declares every stream, then is quiet: no LeaveAll, no declaration again
        for (const unsigned n : all) {
            const auto f = talker_declaration(n, failed);
            ASSERT_TRUE(mbx_model_rx(&fabric, f.data(), f.size(), 0)) << what << ": the Talker reaches the mailbox";
            pass(2);
        }
        pass(1000);
        // the talker is discovered (Milan v1.2 5.6.4), so every restored binding probes it
        const auto avail = acmp_test::adpdu(acmp_test::Adp{});
        ASSERT_TRUE(mbx_model_rx(&fabric, avail.data(), avail.size(), 0)) << what << ": ENTITY_AVAILABLE";
        answer_every_probe(all, 0u, failed, what, failed ? 0x0d40u : 0x0d00u);
        TearDown();
        SetUp();
    }
}

TEST_F(Early, S14ABindWhileBoundToAStreamDeclaredAllAlongIsDeclaredWithinOneTransmit) {
    ASSERT_TRUE(ready());
    const auto all = every_input();
    ASSERT_FALSE(all.empty());
    const unsigned other = 0x40u;  // the streams the inputs are re-bound to: kSid + 0x40 + n
    for (const unsigned n : all) {
        const std::uint32_t since = fabric.tx_sent;
        ASSERT_TRUE(bind(n, true)) << "S14 input " << n << " is bound";
        ASSERT_TRUE(answer_probe(n, since, n)) << "S14 input " << n << " settles";
        pass(12);  // the ACMP channel's bucket refills (mbx_model.h, MBX_CH_ACMP_RATE_REFILL_MS)
        const auto f = talker_declaration(n, false);
        ASSERT_TRUE(mbx_model_rx(&fabric, f.data(), f.size(), 0));
        pass(kJoinMs + 10u);
        ASSERT_EQ(ctrl_plat.srp.ifs[0].sinks[n].declared, 2u) << "S14 input " << n << " declares its first stream";
    }
    // every other stream's Talker is declared, and stays so, while the inputs are bound to their first
    for (const unsigned n : all) {
        const auto f = talker_declaration(n + other, false);
        ASSERT_TRUE(mbx_model_rx(&fabric, f.data(), f.size(), 0));
        pass(2);
    }
    pass(1000);
    for (const unsigned n : all) {
        ASSERT_TRUE(acmp(spec::MSG_BIND_RX_COMMAND, n, 1u)) << "S14 BIND_RX of input " << n << " while bound";
        pass(6);
    }
    answer_every_probe(all, other, false, "S14 a BIND_RX while bound to a stream declared all along", 0x0e00u);
}

}  // namespace

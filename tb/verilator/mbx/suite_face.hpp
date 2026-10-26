// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// suite_face.hpp - the face block's checks (contract 2.3; #665), members of
// mbx_tb::Suite (suite.hpp), run on the RTL through both bus adapters and on
// the host model.
//
// The face block carries what the processor wrapper's other faces carried:
// the settings the firmware writes (F), published by a commit handshake, and
// four request and answer windows (R), each answered by the datapath. Every
// value leaves with its qualifier, so each check here is one of the
// contract's sentences: a setting holds from its commit until the
// acknowledgement and a write that would move it is refused; a request holds
// from its GO until the answer carrying its tag or its wait bound; an answer
// under another tag, or with no request open, is discarded; each event is
// coalesced and never loses the last state. The bench's datapath side
// (face_ack, win_answer, win_expire, face_event) is the harness's.

#ifndef MBX_SUITE_FACE_HPP
#define MBX_SUITE_FACE_HPP

namespace mbx_tb {

//! Register `reg` of interface i's face block, and of its source s's or sink k's entry.
inline std::uint32_t face_reg(std::uint32_t i, std::uint32_t reg) { return MBX_FACE_BASE + MBX_FACE_STRIDE * i + reg; }
inline std::uint32_t face_src_reg(std::uint32_t i, std::uint32_t s, std::uint32_t reg) {
    return face_reg(i, MBX_FACE_SOURCE_BASE + MBX_FACE_SOURCE_STRIDE * s + reg);
}
inline std::uint32_t face_snk_reg(std::uint32_t i, std::uint32_t k, std::uint32_t reg) {
    return face_reg(i, MBX_FACE_SINK_BASE + MBX_FACE_SINK_STRIDE * k + reg);
}
//! The interface blocks the window holds: the contract's interfaces, then
//! blocks of interfaces no build of it has.
inline constexpr std::uint32_t kFaceBlocks = 4;
static_assert(MBX_FACE_BASE + kFaceBlocks * MBX_FACE_STRIDE <= MBX_WINDOW_BYTES,
              "the suite writes the face block of every interface index inside the window");

//! One register the firmware writes: its offset inside an interface's block (an
//! entry's register at its entry's offset) and the union of its fields.
struct FaceWord {
    std::uint32_t off;
    std::uint32_t mask;
};

inline std::uint32_t face_ones(std::uint32_t lsb, std::uint32_t width) {
    return (width >= 32u ? 0xFFFFFFFFu : ((1u << width) - 1u)) << lsb;
}

//! Every setting register, request register and entry register, with its fields.
inline std::vector<FaceWord> face_words() {
    std::vector<FaceWord> out;
    auto add = [&](std::uint32_t off, std::uint32_t mask) {
        for (FaceWord& w : out) {
            if (w.off == off) {
                w.mask |= mask;
                return;
            }
        }
        out.push_back(FaceWord{off, mask});
    };
    for (const FaceField& f : setting_fields()) {
        add(f.reg, face_ones(f.lsb, f.width));
    }
    for (unsigned w = 0; w < kWindows; ++w) {
        for (const FaceField& f : window_fields(w)) {
            if (f.width == 64u) {
                add(f.reg, 0xFFFFFFFFu);
                add(f.hi, 0xFFFFFFFFu);
            } else {
                add(f.reg, face_ones(f.lsb, f.width));
            }
        }
    }
    for (std::uint32_t s = 0; s < MBX_N_PUB_SOURCES; ++s) {
        const std::uint32_t e = MBX_FACE_SOURCE_BASE + MBX_FACE_SOURCE_STRIDE * s;
        add(e + MBX_FACE_SRC_REG_F_PT_OFFSET, 0xFFFFFFFFu);
        add(e + MBX_FACE_SRC_REG_F_FMT_OUT_LO, 0xFFFFFFFFu);
        add(e + MBX_FACE_SRC_REG_F_FMT_OUT_HI, 0xFFFFFFFFu);
        add(e + MBX_FACE_SRC_REG_F_SRC_VALID, face_ones(MBX_F_SRC_VALID_PT_OFFSET_LSB, MBX_F_SRC_VALID_PT_OFFSET_WIDTH) |
                                                  face_ones(MBX_F_SRC_VALID_FMT_OUT_LSB, MBX_F_SRC_VALID_FMT_OUT_WIDTH));
    }
    for (std::uint32_t k = 0; k < MBX_N_PUB_SINKS; ++k) {
        const std::uint32_t e = MBX_FACE_SINK_BASE + MBX_FACE_SINK_STRIDE * k;
        add(e + MBX_FACE_SNK_REG_F_FMT_IN_LO, 0xFFFFFFFFu);
        add(e + MBX_FACE_SNK_REG_F_FMT_IN_HI, 0xFFFFFFFFu);
        add(e + MBX_FACE_SNK_REG_F_SNK_VALID, face_ones(MBX_F_SNK_VALID_FMT_IN_LSB, MBX_F_SNK_VALID_FMT_IN_WIDTH));
    }
    return out;
}

//! Whether a write to `off` inside an interface's block is held by the commit
//! (a setting, an entry register or F_COMMIT) rather than by a window.
inline bool face_held_by_commit(std::uint32_t off) {
    for (unsigned w = 0; w < kWindows; ++w) {
        for (const FaceField& f : window_fields(w)) {
            if (f.reg == off || (f.width == 64u && f.hi == off)) {
                return false;
            }
        }
    }
    return true;
}

//! The window whose request register `off` is, or kWindows.
inline unsigned face_window_of(std::uint32_t off) {
    for (unsigned w = 0; w < kWindows; ++w) {
        for (const FaceField& f : window_fields(w)) {
            if (f.reg == off || (f.width == 64u && f.hi == off)) {
                return w;
            }
        }
    }
    return kWindows;
}

//! The status word of window w on interface i, as the host reads it.
inline std::uint32_t win_status(std::uint32_t busy, std::uint32_t done, std::uint32_t timeout, std::uint32_t tag) {
    return (busy << MBX_CTR_STATUS_BUSY_LSB) | (done << MBX_CTR_STATUS_DONE_LSB) |
           (timeout << MBX_CTR_STATUS_TIMEOUT_LSB) | (tag << MBX_CTR_STATUS_TAG_LSB);
}

//! The value fill_face writes into word `off` of interface i for seed t.
inline std::uint32_t face_value(std::uint32_t i, std::uint32_t off, std::uint32_t t) {
    return 0x9E3779B9u * (off + 0x40u * i + t + 1u) ^ (off << 7);
}

template <class Bench, class Check>
std::vector<std::uint32_t> Suite<Bench, Check>::face_regs_now() {
    std::vector<std::uint32_t> out;
    for (std::uint32_t i = 0; i < MBX_N_IF; ++i) {
        for (const FaceWord& w : face_words()) {
            out.push_back(rd(face_reg(i, w.off)));
        }
        out.push_back(rd(face_reg(i, MBX_FACE_REG_F_STATUS)));
        for (unsigned w = 0; w < kWindows; ++w) {
            out.push_back(rd(face_reg(i, kWindowRegs[w].status)));
            out.push_back(rd(face_reg(i, kWindowRegs[w].data_lo)));
            out.push_back(rd(face_reg(i, kWindowRegs[w].data_hi)));
        }
    }
    return out;
}

template <class Bench, class Check>
std::vector<FaceView> Suite<Bench, Check>::face_views() {
    std::vector<FaceView> out;
    for (std::uint32_t i = 0; i < MBX_N_IF; ++i) {
        out.push_back(b_.face(i));
    }
    return out;
}

template <class Bench, class Check>
FaceView Suite<Bench, Check>::face_zero() {
    FaceView v;
    v.setting.assign(setting_fields().size(), 0u);
    v.pt_offset.assign(MBX_N_PUB_SOURCES, 0u);
    v.fmt_out.assign(MBX_N_PUB_SOURCES, 0u);
    v.fmt_in.assign(MBX_N_PUB_SINKS, 0u);
    for (unsigned w = 0; w < kWindows; ++w) {
        v.fields[w].assign(window_fields(w).size(), 0u);
    }
    return v;
}

template <class Bench, class Check>
void Suite<Bench, Check>::fill_face(std::uint32_t seed) {
    for (std::uint32_t i = 0; i < MBX_N_IF; ++i) {
        for (const FaceWord& w : face_words()) {
            wr(face_reg(i, w.off), face_value(i, w.off, seed));
        }
    }
}

//! The view the face block shows after fill_face(seed), its windows idle and
//! no commit waiting: each field from the word the suite wrote.
template <class Bench, class Check>
FaceView Suite<Bench, Check>::face_expected(std::uint32_t i, std::uint32_t seed) {
    auto word = [&](std::uint32_t off) {
        for (const FaceWord& w : face_words()) {
            if (w.off == off) {
                return face_value(i, off, seed) & w.mask;
            }
        }
        return 0u;
    };
    auto src = [&](unsigned s, std::uint32_t reg) { return word(MBX_FACE_SOURCE_BASE + MBX_FACE_SOURCE_STRIDE * s + reg); };
    auto snk = [&](unsigned k, std::uint32_t reg) { return word(MBX_FACE_SINK_BASE + MBX_FACE_SINK_STRIDE * k + reg); };
    const std::uint32_t idle[kWindows] = {};
    return face_from_words(0u, word, src, snk, idle, idle, [&](unsigned, std::uint32_t reg) { return word(reg); });
}

template <class Bench, class Check>
void Suite<Bench, Check>::check_face() {
    bool zero = true;
    for (std::uint32_t w : face_regs_now()) {
        zero = zero && w == 0u;
    }
    ck_.that("F0 every face register of every interface reads 0 after reset, every status and answer included", zero);
    bool idle = true;
    for (const FaceView& v : face_views()) {
        idle = idle && same_face(v, face_zero());
    }
    ck_.that("F0 and the datapath sees no commit, every setting 0, every window idle with tag 0 and fields 0", idle);
    check_face_masks();
    check_face_outputs();
    check_face_commit();
    for (unsigned w = 0; w < kWindows; ++w) {
        check_face_window(w);
    }
    check_face_out_of_window();
    check_face_events();
    check_face_counter_events();
    check_face_reset();
}

// every register keeps its own fields and every bit of them, at its own
// interface and entry.
template <class Bench, class Check>
void Suite<Bench, Check>::check_face_masks() {
    bool masked = true;
    for (std::uint32_t i = 0; i < MBX_N_IF; ++i) {
        for (const FaceWord& w : face_words()) {
            wr(face_reg(i, w.off), 0xFFFFFFFFu);
            masked = masked && rd(face_reg(i, w.off)) == w.mask;
        }
    }
    ck_.that("F1 each setting, request and entry register keeps its own fields only, per interface and entry", masked);
    fill_face(0x31u);
    bool own = true;
    for (std::uint32_t i = 0; i < MBX_N_IF; ++i) {
        for (const FaceWord& w : face_words()) {
            own = own && rd(face_reg(i, w.off)) == (face_value(i, w.off, 0x31u) & w.mask);
        }
    }
    ck_.that("F1 each reads back what was written to it, and only that", own);
    ck_.dec("F1 no setting or request write is refused while nothing is held", rd(MBX_REG_BUS_ERR), 0);
}

// each field reaches its own port, of its own interface, entry and window.
template <class Bench, class Check>
void Suite<Bench, Check>::check_face_outputs() {
    bool fields = true;
    for (std::uint32_t i = 0; i < MBX_N_IF; ++i) {
        fields = fields && same_face(b_.face(i), face_expected(i, 0x31u));
    }
    ck_.that("F2 every setting, entry and request field reaches the datapath on its own port, for its own interface",
             fields);
    for (std::uint32_t i = 0; i < MBX_N_IF; ++i) {
        for (const FaceWord& w : face_words()) {
            wr(face_reg(i, w.off), 0u);
        }
    }
    // one field at a time: it moves its own port only, of its own interface
    bool single = true;
    const std::size_t n = setting_fields().size();
    for (std::uint32_t i = 0; i < MBX_N_IF; ++i) {
        for (std::size_t f = 0; f < n; ++f) {
            const FaceField& at = setting_fields()[f];
            wr(face_reg(i, at.reg), face_ones(at.lsb, at.width));
            const std::vector<FaceView> v = face_views();
            for (std::uint32_t j = 0; j < MBX_N_IF; ++j) {
                for (std::size_t g = 0; g < n; ++g) {
                    const std::uint64_t want = (j == i && g == f) ? face_ones(0, setting_fields()[g].width) : 0u;
                    single = single && v[j].setting.at(g) == want;
                }
            }
            wr(face_reg(i, at.reg), 0u);
        }
        for (unsigned w = 0; w < kWindows; ++w) {
            const std::vector<FaceField>& wf = window_fields(w);
            for (std::size_t f = 0; f < wf.size(); ++f) {
                const std::uint64_t ones = wf[f].width == 64u ? ~std::uint64_t{0} : face_ones(0, wf[f].width);
                if (wf[f].width == 64u) {
                    wr(face_reg(i, wf[f].reg), 0xFFFFFFFFu);
                    wr(face_reg(i, wf[f].hi), 0xFFFFFFFFu);
                } else {
                    wr(face_reg(i, wf[f].reg), face_ones(wf[f].lsb, wf[f].width));
                }
                const std::vector<FaceView> v = face_views();
                for (std::uint32_t j = 0; j < MBX_N_IF; ++j) {
                    for (unsigned x = 0; x < kWindows; ++x) {
                        for (std::size_t g = 0; g < window_fields(x).size(); ++g) {
                            single = single && v[j].fields[x].at(g) == ((j == i && x == w && g == f) ? ones : 0u);
                        }
                    }
                }
                wr(face_reg(i, wf[f].reg), 0u);
                if (wf[f].width == 64u) {
                    wr(face_reg(i, wf[f].hi), 0u);
                }
            }
        }
        for (std::uint32_t s = 0; s < MBX_N_PUB_SOURCES; ++s) {
            wr(face_src_reg(i, s, MBX_FACE_SRC_REG_F_PT_OFFSET), 0xC0000000u | s);
            wr(face_src_reg(i, s, MBX_FACE_SRC_REG_F_FMT_OUT_HI), 0xF0000000u | s);
            wr(face_src_reg(i, s, MBX_FACE_SRC_REG_F_SRC_VALID), 1u << MBX_F_SRC_VALID_PT_OFFSET_LSB);
            std::vector<FaceView> v = face_views();
            for (std::uint32_t j = 0; j < MBX_N_IF; ++j) {
                for (std::uint32_t r = 0; r < MBX_N_PUB_SOURCES; ++r) {
                    const bool me = j == i && r == s;
                    single = single && v[j].pt_offset.at(r) == (me ? (0xC0000000u | s) : 0u) &&
                             v[j].fmt_out.at(r) == (me ? (std::uint64_t{0xF0000000u | s} << 32) : 0u);
                }
                single = single && v[j].pt_offset_v == (j == i ? 1u << s : 0u) && v[j].fmt_out_v == 0u;
            }
            wr(face_src_reg(i, s, MBX_FACE_SRC_REG_F_SRC_VALID), 1u << MBX_F_SRC_VALID_FMT_OUT_LSB);
            v = face_views();
            for (std::uint32_t j = 0; j < MBX_N_IF; ++j) {
                single = single && v[j].fmt_out_v == (j == i ? 1u << s : 0u) && v[j].pt_offset_v == 0u;
            }
            wr(face_src_reg(i, s, MBX_FACE_SRC_REG_F_PT_OFFSET), 0u);
            wr(face_src_reg(i, s, MBX_FACE_SRC_REG_F_FMT_OUT_HI), 0u);
            wr(face_src_reg(i, s, MBX_FACE_SRC_REG_F_SRC_VALID), 0u);
        }
        for (std::uint32_t k = 0; k < MBX_N_PUB_SINKS; ++k) {
            wr(face_snk_reg(i, k, MBX_FACE_SNK_REG_F_FMT_IN_LO), 0x0A000000u | k);
            wr(face_snk_reg(i, k, MBX_FACE_SNK_REG_F_SNK_VALID), 1u << MBX_F_SNK_VALID_FMT_IN_LSB);
            const std::vector<FaceView> v = face_views();
            for (std::uint32_t j = 0; j < MBX_N_IF; ++j) {
                for (std::uint32_t r = 0; r < MBX_N_PUB_SINKS; ++r) {
                    single = single && v[j].fmt_in.at(r) == ((j == i && r == k) ? (0x0A000000u | k) : 0u);
                }
                single = single && v[j].fmt_in_v == (j == i ? 1u << k : 0u);
            }
            wr(face_snk_reg(i, k, MBX_FACE_SNK_REG_F_FMT_IN_LO), 0u);
            wr(face_snk_reg(i, k, MBX_FACE_SNK_REG_F_SNK_VALID), 0u);
        }
    }
    ck_.that("F2 each setting field, each request field and each source's and sink's value moves its own port only",
             single);
}

// a commit holds every setting until its acknowledgement, and a write that
// would move one meanwhile is refused.
template <class Bench, class Check>
void Suite<Bench, Check>::check_face_commit() {
    fill_face(0x52u);
    const std::uint32_t i = MBX_N_IF - 1u;
    const std::uint32_t err0 = rd(MBX_REG_BUS_ERR);
    ck_.dec("F3 no commit waits before F_COMMIT", b_.face(i).send, 0);
    wr(face_reg(i, MBX_FACE_REG_F_COMMIT), 0u);
    ck_.that("F3 F_COMMIT written with GO clear commits nothing",
             b_.face(i).send == 0u && rd(face_reg(i, MBX_FACE_REG_F_STATUS)) == 0u);
    wr(face_reg(i, MBX_FACE_REG_F_COMMIT), 1u << MBX_F_COMMIT_GO_LSB);
    bool others = true;
    for (std::uint32_t j = 0; j + 1u < MBX_N_IF; ++j) {
        others = others && b_.face(j).send == 0u;
    }
    ck_.that("F3 GO raises fw_send_o and F_STATUS.BUSY on its own interface only",
             b_.face(i).send == 1u && rd(face_reg(i, MBX_FACE_REG_F_STATUS)) == (1u << MBX_F_STATUS_BUSY_LSB) && others);
    const FaceView held = b_.face(i);
    const std::vector<std::uint32_t> words = face_regs_now();
    std::uint32_t refused = 0;
    for (const FaceWord& w : face_words()) {
        if (face_held_by_commit(w.off)) {
            wr(face_reg(i, w.off), ~face_value(i, w.off, 0x52u));
            ++refused;
        }
    }
    wr(face_reg(i, MBX_FACE_REG_F_COMMIT), 1u << MBX_F_COMMIT_GO_LSB);
    ++refused;
    ck_.dec("F3 every setting and entry write, and a second commit, is refused while BUSY and counted",
            rd(MBX_REG_BUS_ERR), err0 + refused);
    ck_.that("F3 and the settings, their read-back and their ports, held while BUSY",
             face_regs_now() == words && same_face(b_.face(i), held));
    bool requests = true;
    for (unsigned w = 0; w < kWindows; ++w) {
        const FaceField& f = window_fields(w).front();
        wr(face_reg(i, f.reg), face_value(i, f.reg, 0x77u));
        requests = requests && rd(face_reg(i, f.reg)) == (face_value(i, f.reg, 0x77u) & face_words_mask(f.reg));
        wr(face_reg(i, f.reg), face_value(i, f.reg, 0x52u));
    }
    ck_.that("F3 a window's request registers are not held by a commit", requests);
    if (MBX_N_IF > 1u) {
        b_.face_ack(0);
        ck_.dec("F3 another interface's acknowledgement is not this commit's", b_.face(i).send, 1);
    }
    b_.face_ack(i);
    ck_.that("F3 the acknowledgement drops fw_send_o and BUSY",
             b_.face(i).send == 0u && rd(face_reg(i, MBX_FACE_REG_F_STATUS)) == 0u);
    wr(face_reg(i, MBX_FACE_REG_F_ENTITY), 0x00AB0123u);
    ck_.hex("F3 and the settings take writes again", rd(face_reg(i, MBX_FACE_REG_F_ENTITY)),
            0x00AB0123u & face_words_mask(MBX_FACE_REG_F_ENTITY));
    b_.face_ack(i);
    wr(face_reg(i, MBX_FACE_REG_F_COMMIT), 1u << MBX_F_COMMIT_GO_LSB);
    ck_.dec("F3 an acknowledgement with no commit waiting is not taken for the next", b_.face(i).send, 1);
    b_.face_ack(i);
    ck_.dec("F3 the next commit is acknowledged by its own", b_.face(i).send, 0);
}

template <class Bench, class Check>
std::uint32_t Suite<Bench, Check>::face_words_mask(std::uint32_t off) {
    for (const FaceWord& w : face_words()) {
        if (w.off == off) {
            return w.mask;
        }
    }
    return 0u;
}

// window w's request holds from its GO until the answer carrying its
// tag; an answer under another tag, or with no request open, is discarded; the
// wait bound closes it unanswered; nothing it does moves another window.
template <class Bench, class Check>
void Suite<Bench, Check>::check_face_window(unsigned w) {
    static const char* const names[kWindows] = {"CTR", "AMAP", "EDIT", "GSI"};
    const std::string name = names[w];
    const std::uint32_t i = MBX_N_IF - 1u;
    const WindowRegs& r = kWindowRegs[w];
    const bool one_word = r.data_hi == r.data_lo;
    auto status = [&] { return rd(face_reg(i, r.status)); };
    auto data = [&] {
        return one_word ? std::uint64_t{rd(face_reg(i, r.data_lo))}
                        : (std::uint64_t{rd(face_reg(i, r.data_hi))} << 32) | rd(face_reg(i, r.data_lo));
    };
    auto label = [&](const char* what) { return std::string("F4 ") + name + " " + what; };
    fill_face(0x60u + w);
    const FaceView before = b_.face(i);
    const std::uint32_t err0 = rd(MBX_REG_BUS_ERR);
    ck_.that(label("idle: STATUS 0, no request on its port").c_str(), status() == 0u && before.req[w] == 0u);
    wr(face_reg(i, r.go), 1u << MBX_CTR_CMD_GO_LSB);
    FaceView open = b_.face(i);
    bool alone = true;
    for (unsigned x = 0; x < kWindows; ++x) {
        alone = alone && open.req[x] == (x == w ? 1u : 0u);
    }
    ck_.that(label("GO opens the request: BUSY with tag 1, req and tag on its ports, no other window's").c_str(),
             status() == win_status(1, 0, 0, 1) && open.tag[w] == 1u && alone);
    std::uint32_t refused = 0;
    for (const FaceWord& fw : face_words()) {
        if (face_window_of(fw.off) == w) {
            wr(face_reg(i, fw.off), ~face_value(i, fw.off, 0x60u + w));
            ++refused;
        }
    }
    wr(face_reg(i, r.go), 1u << MBX_CTR_CMD_GO_LSB);
    ++refused;
    ck_.dec(label("a request write and a second GO while BUSY are refused and counted").c_str(), rd(MBX_REG_BUS_ERR),
            err0 + refused);
    ck_.that(label("and the request's fields hold on their ports and in their read-back").c_str(),
             b_.face(i).fields[w] == before.fields[w] && status() == win_status(1, 0, 0, 1));
    const std::uint64_t answer = 0x8765432100000000ull | (0x1000u * w + 0x2A5u);
    b_.win_answer(w, i, 2u, answer);
    ck_.that(label("an answer under another tag is discarded: still BUSY, no DATA").c_str(),
             status() == win_status(1, 0, 0, 1) && data() == 0u && b_.face(i).req[w] == 1u);
    if (MBX_N_IF > 1u) {
        b_.win_answer(w, 0u, 1u, answer);
        ck_.that(label("another interface's answer is not this request's").c_str(), status() == win_status(1, 0, 0, 1));
    }
    b_.win_answer(w, i, 1u, answer);
    const std::uint64_t got = one_word ? static_cast<std::uint32_t>(answer) : answer;
    ck_.that(label("the answer under its tag closes it: DONE, the answer in DATA, the request off its port").c_str(),
             status() == win_status(0, 1, 0, 1) && data() == got && b_.face(i).req[w] == 0u);
    b_.win_answer(w, i, 1u, 0x0123u);
    ck_.hex(label("an answer with no request open is discarded").c_str(), data(), got);
    wr(face_reg(i, r.go), 1u << MBX_CTR_CMD_GO_LSB);
    ck_.that(label("the next GO takes tag 2 and clears DONE").c_str(),
             status() == win_status(1, 0, 0, 2) && b_.face(i).tag[w] == 2u);
    b_.win_expire(w, i);
    ck_.that(label("unanswered past its wait bound it closes with TIMEOUT, the last answer kept").c_str(),
             status() == win_status(0, 0, 1, 2) && data() == got && b_.face(i).req[w] == 0u);
    b_.win_answer(w, i, 2u, 0x4444u);
    ck_.that(label("a late answer to the request that timed out is discarded").c_str(),
             status() == win_status(0, 0, 1, 2) && data() == got);
    wr(face_reg(i, r.go), 1u << MBX_CTR_CMD_GO_LSB);
    b_.win_answer(w, i, 2u, 0x5555u);
    ck_.that(label("and so is that late answer under the next request").c_str(), status() == win_status(1, 0, 0, 3));
    b_.win_answer(w, i, 3u, 0x6666u);
    ck_.hex(label("which takes its own").c_str(), data(), 0x6666u);
    wr(face_reg(i, r.go), 0u);
    ck_.dec(label("CMD written with GO clear opens nothing").c_str(), status(), win_status(0, 1, 0, 3));
    ck_.dec(label("and the window refused nothing while it was idle").c_str(), rd(MBX_REG_BUS_ERR), err0 + refused);
}

// outside the registers: a hole, an interface the build lacks, a status
// or an answer take no write; a partial strobe is refused.
template <class Bench, class Check>
void Suite<Bench, Check>::check_face_out_of_window() {
    fill_face(0x47u);
    const std::vector<std::uint32_t> words = face_regs_now();
    const std::vector<FaceView> views = face_views();
    const std::uint32_t err0 = rd(MBX_REG_BUS_ERR);
    auto named = [&](std::uint32_t i, std::uint32_t off) {
        if (i >= MBX_N_IF) {
            return false;
        }
        if (off == MBX_FACE_REG_F_COMMIT || off == MBX_FACE_REG_F_STATUS) {
            return true;
        }
        for (const WindowRegs& r : kWindowRegs) {
            if (off == r.go || off == r.status || off == r.data_lo || off == r.data_hi) {
                return true;
            }
        }
        for (const FaceWord& w : face_words()) {
            if (w.off == off) {
                return true;
            }
        }
        return false;
    };
    bool holes = true;
    for (std::uint32_t i = 0; i < kFaceBlocks; ++i) {
        for (std::uint32_t off = 0; off < MBX_FACE_STRIDE; off += 4u) {
            if (!named(i, off)) {
                wr(face_reg(i, off), 0xFFFFFFFFu);
                holes = holes && rd(face_reg(i, off)) == 0u;
            }
        }
    }
    ck_.that("F7 every hole of every face block, and every word of an interface the build lacks, reads 0 after a "
             "write",
             holes);
    for (std::uint32_t i = 0; i < MBX_N_IF; ++i) {
        wr(face_reg(i, MBX_FACE_REG_F_STATUS), 0xFFFFFFFFu);
        for (const WindowRegs& r : kWindowRegs) {
            wr(face_reg(i, r.status), 0xFFFFFFFFu);
            wr(face_reg(i, r.data_lo), 0xFFFFFFFFu);
            wr(face_reg(i, r.data_hi), 0xFFFFFFFFu);
        }
    }
    bool kept = face_regs_now() == words;
    const std::vector<FaceView> after = face_views();
    for (std::uint32_t i = 0; i < MBX_N_IF; ++i) {
        kept = kept && same_face(after[i], views[i]);
    }
    ck_.that("F7 and none of those writes, nor one to a status or an answer, moved a register or a port", kept);
    ck_.dec("F7 a write outside the registers is not a refusal", rd(MBX_REG_BUS_ERR), err0);
    b_.write(face_reg(0, MBX_FACE_REG_F_ENTITY), 0u, 0x3);
    b_.write(face_reg(0, MBX_FACE_REG_CTR_CMD), 1u, 0x1);
    b_.write(face_reg(0, MBX_FACE_REG_F_COMMIT), 1u, 0x7);
    ck_.that("F7 a write with a partial strobe moves no setting, opens no request and commits nothing",
             face_regs_now() == words && same_face(b_.face(0), views[0]));
    ck_.dec("F7 and counts in BUS_ERR", rd(MBX_REG_BUS_ERR), err0 + 3u);
}

// the counted face events, each coalesced into one record that carries
// every pulse, in their priority after the tick.
template <class Bench, class Check>
void Suite<Bench, Check>::check_face_events() {
    const std::uint32_t i = MBX_N_IF - 1u;
    const std::uint32_t types[3] = {MBX_EV_TYPE_AMAP_LIVE_WRITE, MBX_EV_TYPE_AVB_INFO_CHANGED,
                                    MBX_EV_TYPE_AS_PATH_CHANGED};
    const std::uint32_t count_lsb[3] = {MBX_EV_AMAP_LIVE_WRITE_W1_COUNT_LSB, MBX_EV_AVB_INFO_CHANGED_W1_COUNT_LSB,
                                        MBX_EV_AS_PATH_CHANGED_W1_COUNT_LSB};
    const std::uint32_t count_width[3] = {MBX_EV_AMAP_LIVE_WRITE_W1_COUNT_WIDTH, MBX_EV_AVB_INFO_CHANGED_W1_COUNT_WIDTH,
                                          MBX_EV_AS_PATH_CHANGED_W1_COUNT_WIDTH};
    const unsigned kinds[3] = {3u, 1u, 2u};
    for (unsigned k = 0; k < 3u; ++k) {
        b_.face_event(kinds[k], i);
        b_.idle(8);
        const std::vector<std::uint32_t> e = take_event();
        ck_.that("F8 one face event posts its record, on its interface, with COUNT 1 and NOW_MS",
                 ev_type(e) == types[k] && e.size() == 4 &&
                     field(e[0], MBX_EVREC_W0_IF_LSB, MBX_EVREC_W0_IF_WIDTH) == i &&
                     field(e[1], count_lsb[k], count_width[k]) == 1u &&
                     e[3] == rd(MBX_REG_NOW_MS));
        b_.idle(4);
    }
    ck_.that("F8 and nothing more", take_event().empty());
    fill_event_ring_with_expiries();
    for (unsigned k = 0; k < 3u; ++k) {
        for (unsigned n = 0; n < 2u + k; ++n) {
            b_.face_event(kinds[k], i);
            b_.idle(2);
        }
    }
    std::vector<std::uint32_t> order;
    std::uint32_t counts[3] = {};
    for (std::vector<std::uint32_t> x = take_event(); !x.empty(); x = take_event()) {
        for (unsigned k = 0; k < 3u; ++k) {
            if (ev_type(x) == types[k]) {
                order.push_back(types[k]);
                counts[k] += field(x[1], count_lsb[k], count_width[k]);
            }
        }
        b_.idle(8);
    }
    ck_.that("F8 pulses while the ring was full post one record each, the map write first, then AVB_INFO, then "
             "AS_PATH",
             order == std::vector<std::uint32_t>(types, types + 3));
    ck_.that("F8 each carrying every pulse it coalesced", counts[0] == 2u && counts[1] == 3u && counts[2] == 4u);
}

// COUNTERS_CHANGED: one pending bit per served descriptor, ALL for any
// other, and at most one record per descriptor in each holdoff epoch, a change
// meanwhile waiting for the next.
template <class Bench, class Check>
void Suite<Bench, Check>::check_face_counter_events() {
    const std::uint32_t i = MBX_N_IF - 1u;
    auto ctr = [&](const std::vector<std::uint32_t>& e, std::uint32_t& type, std::uint32_t& index) {
        type = field(e[1], MBX_EV_COUNTERS_CHANGED_W1_TYPE_LSB, MBX_EV_COUNTERS_CHANGED_W1_TYPE_WIDTH);
        index = field(e[1], MBX_EV_COUNTERS_CHANGED_W1_INDEX_LSB, MBX_EV_COUNTERS_CHANGED_W1_INDEX_WIDTH);
        return field(e[2], MBX_EV_COUNTERS_CHANGED_W2_ALL_LSB, MBX_EV_COUNTERS_CHANGED_W2_ALL_WIDTH);
    };
    // start an epoch: everything posted before now is in an earlier one
    b_.ms(MBX_CTRCHG_HOLDOFF_MS);
    b_.face_event(0, i, MBX_CTRCHG_STREAM_INPUT_TYPE, 3);
    b_.idle(8);
    std::vector<std::uint32_t> e = take_event();
    std::uint32_t type = 0;
    std::uint32_t index = 0;
    std::uint32_t all = e.size() == 4 ? ctr(e, type, index) : 9u;
    ck_.that("F9 a counter change posts COUNTERS_CHANGED with its descriptor, on its interface",
             ev_type(e) == MBX_EV_TYPE_COUNTERS_CHANGED && type == MBX_CTRCHG_STREAM_INPUT_TYPE && index == 3u &&
                 all == 0u && field(e[0], MBX_EVREC_W0_IF_LSB, MBX_EVREC_W0_IF_WIDTH) == i);
    b_.face_event(0, i, MBX_CTRCHG_STREAM_INPUT_TYPE, 3);
    b_.face_event(0, i, MBX_CTRCHG_STREAM_INPUT_TYPE, 3);
    b_.face_event(0, i, MBX_CTRCHG_STREAM_OUTPUT_TYPE, MBX_CTRCHG_STREAM_OUTPUT_COUNT - 1u);
    b_.idle(8);
    e = take_event();
    all = e.size() == 4 ? ctr(e, type, index) : 9u;
    ck_.that("F9 another descriptor posts at once; the first, posted in this epoch, waits",
             ev_type(e) == MBX_EV_TYPE_COUNTERS_CHANGED && type == MBX_CTRCHG_STREAM_OUTPUT_TYPE &&
                 index == MBX_CTRCHG_STREAM_OUTPUT_COUNT - 1u && all == 0u);
    b_.idle(8);
    ck_.that("F9 and nothing else posts in this epoch", take_event().empty());
    b_.ms(MBX_CTRCHG_HOLDOFF_MS);
    b_.idle(8);
    e = take_event();
    all = e.size() == 4 ? ctr(e, type, index) : 9u;
    ck_.that("F9 the next epoch posts the descriptor that changed meanwhile, once, its changes coalesced",
             ev_type(e) == MBX_EV_TYPE_COUNTERS_CHANGED && type == MBX_CTRCHG_STREAM_INPUT_TYPE && index == 3u &&
                 all == 0u);
    b_.idle(8);
    ck_.that("F9 and no more", take_event().empty());
    b_.ms(MBX_CTRCHG_HOLDOFF_MS);
    b_.face_event(0, i, 0x0042u, 0);
    b_.face_event(0, i, MBX_CTRCHG_STREAM_INPUT_TYPE, MBX_CTRCHG_STREAM_INPUT_COUNT);
    b_.face_event(0, i, MBX_CTRCHG_AVB_INTERFACE_TYPE, 0);
    b_.face_event(0, i, MBX_CTRCHG_CLOCK_DOMAIN_TYPE, 0);
    b_.idle(8);
    std::vector<std::uint32_t> seen;
    std::uint32_t alls = 0;
    for (std::vector<std::uint32_t> x = take_event(); !x.empty(); x = take_event()) {
        if (ev_type(x) == MBX_EV_TYPE_COUNTERS_CHANGED) {
            alls += ctr(x, type, index);
            seen.push_back(type);
        }
        b_.idle(8);
    }
    ck_.that("F9 an unknown descriptor posts a record with ALL, and the AVB_INTERFACE and the CLOCK_DOMAIN their own, "
             "as they arrive",
             seen == std::vector<std::uint32_t>{0u, MBX_CTRCHG_AVB_INTERFACE_TYPE, MBX_CTRCHG_CLOCK_DOMAIN_TYPE} &&
                 alls == 1u);
    b_.ms(MBX_CTRCHG_HOLDOFF_MS);
    b_.idle(8);
    e = take_event();
    all = e.size() == 4 ? ctr(e, type, index) : 9u;
    ck_.that("F9 an index past its family, in the same epoch, is the ALL bit again: it posts once in the next",
             ev_type(e) == MBX_EV_TYPE_COUNTERS_CHANGED && all == 1u && type == 0u && index == 0u &&
                 take_event().empty());
}

// a reset clears the whole block, every port, every open request and
// every pending face event.
template <class Bench, class Check>
void Suite<Bench, Check>::check_face_reset() {
    fill_face(0x5Au);
    const std::uint32_t i = MBX_N_IF - 1u;
    wr(face_reg(i, MBX_FACE_REG_F_COMMIT), 1u << MBX_F_COMMIT_GO_LSB);
    wr(face_reg(i, MBX_FACE_REG_GSI_CMD), 1u << MBX_CTR_CMD_GO_LSB);
    fill_event_ring_with_expiries();
    b_.face_event(3u, i);
    b_.face_event(0u, i, MBX_CTRCHG_STREAM_INPUT_TYPE, 1);
    restart();
    bool zero = true;
    for (std::uint32_t w : face_regs_now()) {
        zero = zero && w == 0u;
    }
    for (const FaceView& v : face_views()) {
        zero = zero && same_face(v, face_zero());
    }
    b_.ms(2);
    ck_.that("F10 a reset clears every face register, port, open request and commit, and every pending face event",
             zero && take_event().empty());
}

// The RTL's own timing (the cycle-by-cycle bench only): the wait bound to the
// cycle, an answer taken only on its pulse, and a commit held for as long as
// the acknowledgement takes.
template <class Bench, class Check>
void Suite<Bench, Check>::check_face_timing() {
    const std::uint32_t i = MBX_N_IF - 1u;
    for (unsigned w = 0; w < kWindows; ++w) {
        const WindowRegs& r = kWindowRegs[w];
        const std::string name = w == kWinCtr ? "CTR" : w == kWinAmap ? "AMAP" : w == kWinEdit ? "EDIT" : "GSI";
        // every clock the request is open, counted from the clock the GO lands,
        // and the clocks it is still open once the GO's bus access returns
        unsigned open = 0;
        b_.on_clock = [&] { open += b_.face(i).req[w]; };
        wr(face_reg(i, r.go), 1u << MBX_CTR_CMD_GO_LSB);
        unsigned held = 0;
        while (b_.face(i).req[w] != 0u && held < 4u * kWaitCycles[w]) {
            b_.idle(1);
            ++held;
        }
        b_.on_clock = nullptr;
        ck_.dec(("T0 " + name + " an unanswered request holds for exactly its wait bound, in clocks").c_str(), open,
                kWaitCycles[w]);
        ck_.dec(("T0 " + name + " then closes with TIMEOUT").c_str(), rd(face_reg(i, r.status)),
                win_status(0, 0, 1, b_.face(i).tag[w]));
        wr(face_reg(i, r.go), 1u << MBX_CTR_CMD_GO_LSB);
        std::uint32_t tag = b_.face(i).tag[w];
        // a request that never opened leaves held 0: the timing check has
        // failed, and the bench stays bounded
        b_.idle(held == 0u ? 0u : held - 1u);
        b_.win_answer(w, i, tag, 0xA0u + w);
        ck_.dec(("T0 " + name + " an answer on the last cycle of the bound is taken").c_str(), rd(face_reg(i, r.status)),
                win_status(0, 1, 0, tag));
        wr(face_reg(i, r.go), 1u << MBX_CTR_CMD_GO_LSB);
        tag = b_.face(i).tag[w];
        b_.idle(held);
        b_.win_answer(w, i, tag, 0xB0u + w);
        ck_.that(("T0 " + name + " one cycle later the request has timed out and the answer is discarded").c_str(),
                 rd(face_reg(i, r.status)) == win_status(0, 0, 1, tag) && rd(face_reg(i, r.data_lo)) == 0xA0u + w);
        wr(face_reg(i, r.go), 1u << MBX_CTR_CMD_GO_LSB);
        tag = b_.face(i).tag[w];
        b_.win_data(w, i, tag, 0xC0u + w);
        b_.idle(8);
        ck_.dec(("T1 " + name + " answer data and tag without the pulse close nothing").c_str(),
                rd(face_reg(i, r.status)), win_status(1, 0, 0, tag));
        b_.win_answer(w, i, tag, 0xD0u + w);
        ck_.hex(("T1 " + name + " the pulse takes the data it carries").c_str(), rd(face_reg(i, r.data_lo)), 0xD0u + w);
    }
    wr(face_reg(i, MBX_FACE_REG_F_ENTITY), 0x00250007u);
    wr(face_reg(i, MBX_FACE_REG_F_COMMIT), 1u << MBX_F_COMMIT_GO_LSB);
    bool held = true;
    for (unsigned c = 0; c < 200u; ++c) {
        b_.idle(1);
        held = held && b_.face(i).send == 1u && b_.face(i).setting.at(1) == 0x0007u && b_.face(i).setting.at(2) == 0x25u;
    }
    ck_.that("T2 a commit holds fw_send_o and its settings for as long as the acknowledgement takes", held);
    b_.face_ack(i);
    ck_.dec("T2 and drops fw_send_o on the cycle after it", b_.face(i).send, 0);
}

}  // namespace mbx_tb

#endif  // MBX_SUITE_FACE_HPP

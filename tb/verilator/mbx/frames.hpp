// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// frames.hpp - wire frames for the mailbox suite, written from the clauses
// (IEEE 1722.1-2021 Figures 6-1, 8-1 and 9-1; IEEE 1722-2016 Figure B.4;
// IEEE 802.1Q-2018 10.8), never from the RTL or the contract's filter table.
// The filter's byte offsets are then checked against these frames, so a
// contract offset that disagrees with the clause fails here.

#ifndef MBX_FRAMES_HPP
#define MBX_FRAMES_HPP

#include <cstdint>
#include <vector>

#include "mbx_contract.h"

namespace mbx_tb {

//! One frame the TX merge sent: its bytes, interface and channel.
struct TxFrame {
    std::vector<std::uint8_t> bytes;
    unsigned iface = 0;
    unsigned channel = 0;
};

//! What the publication block drives into one interface's datapath (lane
//! F-INT): each field as KL_mbx's pub_*_o ports carry it on the RTL, and as
//! mbx_model_pub_view() reports it on the host model.
struct PubView {
    std::uint32_t da_gate = 0;       //!< DA_GATE.OPEN, bit s source s
    std::uint32_t licence = 0;       //!< LICENCE.ACTIVE, bit s source s
    std::uint32_t idle_slope_bps = 0;  //!< IDLE_SLOPE.BPS
    std::uint32_t vid = 0;           //!< SR_DOMAIN.VID
    std::uint32_t priority = 0;      //!< SR_DOMAIN.PRIORITY
    std::uint32_t adopted = 0;       //!< SR_DOMAIN.ADOPTED
    std::uint32_t talker_decl = 0;   //!< TALKER_DECL.DECLARED, bit s source s
    std::uint32_t bound = 0;         //!< bit k: sink k's BINDING.BOUND
    std::uint32_t started = 0;       //!< bit k: sink k's BINDING.STARTED
    std::vector<std::uint64_t> sid;  //!< the stream_id the datapath takes for sink k: 0 while its SID_VALID is clear
};

inline bool same_pub(const PubView& a, const PubView& b) {
    return a.da_gate == b.da_gate && a.licence == b.licence && a.idle_slope_bps == b.idle_slope_bps &&
           a.vid == b.vid && a.priority == b.priority && a.adopted == b.adopted && a.talker_decl == b.talker_decl &&
           a.bound == b.bound && a.started == b.started && a.sid == b.sid;
}

//! One field of a face register: the register's offset inside an interface's
//! face block, the field's place, and for a 64-bit value the offset of its
//! high word (`reg` then holds the low one).
struct FaceField {
    std::uint32_t reg;
    std::uint32_t lsb;
    std::uint32_t width;
    std::uint32_t hi = 0;
};

//! The face block's windows, in the contract's order.
inline constexpr unsigned kWindows = 4;
enum : unsigned { kWinCtr = 0, kWinAmap = 1, kWinEdit = 2, kWinGsi = 3 };

//! A window's GO, status and data registers (data_hi == data_lo: one word).
struct WindowRegs {
    std::uint32_t go;
    std::uint32_t status;
    std::uint32_t data_lo;
    std::uint32_t data_hi;
};
inline const WindowRegs kWindowRegs[kWindows] = {
    {MBX_FACE_REG_CTR_CMD, MBX_FACE_REG_CTR_STATUS, MBX_FACE_REG_CTR_DATA, MBX_FACE_REG_CTR_DATA},
    {MBX_FACE_REG_AMAP_CMD, MBX_FACE_REG_AMAP_STATUS, MBX_FACE_REG_AMAP_DATA_LO, MBX_FACE_REG_AMAP_DATA_HI},
    {MBX_FACE_REG_EDIT_CMD, MBX_FACE_REG_EDIT_STATUS, MBX_FACE_REG_EDIT_DATA_LO, MBX_FACE_REG_EDIT_DATA_HI},
    {MBX_FACE_REG_GSI_CMD, MBX_FACE_REG_GSI_STATUS, MBX_FACE_REG_GSI_DATA_LO, MBX_FACE_REG_GSI_DATA_HI},
};
inline constexpr std::uint32_t kWaitCycles[kWindows] = {MBX_WIN_CTR_WAIT_CYCLES, MBX_WIN_AMAP_WAIT_CYCLES,
                                                        MBX_WIN_EDIT_WAIT_CYCLES, MBX_WIN_GSI_WAIT_CYCLES};

//! Every setting field, in the order KL_mbx declares its fw_*_o ports.
inline const std::vector<FaceField>& setting_fields() {
    static const std::vector<FaceField> v = {
        {MBX_FACE_REG_F_CTRL, MBX_F_CTRL_READY_LSB, MBX_F_CTRL_READY_WIDTH},
        {MBX_FACE_REG_F_ENTITY, MBX_F_ENTITY_CUR_CONFIG_LSB, MBX_F_ENTITY_CUR_CONFIG_WIDTH},
        {MBX_FACE_REG_F_ENTITY, MBX_F_ENTITY_IDENTIFY_LSB, MBX_F_ENTITY_IDENTIFY_WIDTH},
        {MBX_FACE_REG_F_CLOCK, MBX_F_CLOCK_SOURCE_INDEX_LSB, MBX_F_CLOCK_SOURCE_INDEX_WIDTH},
        {MBX_FACE_REG_F_AECP, MBX_F_AECP_LOCK_HELD_LSB, MBX_F_AECP_LOCK_HELD_WIDTH},
        {MBX_FACE_REG_F_AECP, MBX_F_AECP_DYN_DIRTY_LSB, MBX_F_AECP_DYN_DIRTY_WIDTH},
        {MBX_FACE_REG_F_RESTORE, MBX_F_RESTORE_BUSY_LSB, MBX_F_RESTORE_BUSY_WIDTH},
        {MBX_FACE_REG_F_RESTORE, MBX_F_RESTORE_DONE_LSB, MBX_F_RESTORE_DONE_WIDTH},
        {MBX_FACE_REG_F_RESTORE, MBX_F_RESTORE_FAIL_LSB, MBX_F_RESTORE_FAIL_WIDTH},
        {MBX_FACE_REG_F_RESTORE, MBX_F_RESTORE_BLANK_LSB, MBX_F_RESTORE_BLANK_WIDTH},
        {MBX_FACE_REG_F_RESTORE, MBX_F_RESTORE_CLOSED_LSB, MBX_F_RESTORE_CLOSED_WIDTH},
        {MBX_FACE_REG_F_RESTORE, MBX_F_RESTORE_RB_LSB, MBX_F_RESTORE_RB_WIDTH},
        {MBX_FACE_REG_F_RESTORE, MBX_F_RESTORE_RS_CAUSE_LSB, MBX_F_RESTORE_RS_CAUSE_WIDTH},
        {MBX_FACE_REG_F_RESTORE, MBX_F_RESTORE_CAUSE_LSB, MBX_F_RESTORE_CAUSE_WIDTH},
        {MBX_FACE_REG_F_NVM, MBX_F_NVM_BACKED_LSB, MBX_F_NVM_BACKED_WIDTH},
        {MBX_FACE_REG_F_NVM, MBX_F_NVM_ALARM_LSB, MBX_F_NVM_ALARM_WIDTH},
        {MBX_FACE_REG_F_NVM, MBX_F_NVM_DIRTY_LSB, MBX_F_NVM_DIRTY_WIDTH},
        {MBX_FACE_REG_F_NVM, MBX_F_NVM_STALE_LSB, MBX_F_NVM_STALE_WIDTH},
        {MBX_FACE_REG_F_NVM, MBX_F_NVM_PEND_LSB, MBX_F_NVM_PEND_WIDTH},
        {MBX_FACE_REG_F_NVM, MBX_F_NVM_IMG_VALID_LSB, MBX_F_NVM_IMG_VALID_WIDTH},
        {MBX_FACE_REG_F_NVM, MBX_F_NVM_VERDICT_LSB, MBX_F_NVM_VERDICT_WIDTH},
    };
    return v;
}

//! Window w's request fields, in the order KL_mbx declares their ports.
inline const std::vector<FaceField>& window_fields(unsigned w) {
    static const std::vector<FaceField> v[kWindows] = {
        {{MBX_FACE_REG_CTR_REQ, MBX_CTR_REQ_TYPE_LSB, MBX_CTR_REQ_TYPE_WIDTH},
         {MBX_FACE_REG_CTR_REQ, MBX_CTR_REQ_INDEX_LSB, MBX_CTR_REQ_INDEX_WIDTH},
         {MBX_FACE_REG_CTR_WORD, MBX_CTR_WORD_WORD_LSB, MBX_CTR_WORD_WORD_WIDTH}},
        {{MBX_FACE_REG_AMAP_REQ, MBX_AMAP_REQ_TYPE_LSB, MBX_AMAP_REQ_TYPE_WIDTH},
         {MBX_FACE_REG_AMAP_REQ, MBX_AMAP_REQ_INDEX_LSB, MBX_AMAP_REQ_INDEX_WIDTH},
         {MBX_FACE_REG_AMAP_PAGE, MBX_AMAP_PAGE_MAP_INDEX_LSB, MBX_AMAP_PAGE_MAP_INDEX_WIDTH},
         {MBX_FACE_REG_AMAP_PAGE, MBX_AMAP_PAGE_SEL_LSB, MBX_AMAP_PAGE_SEL_WIDTH},
         {MBX_FACE_REG_AMAP_PAGE, MBX_AMAP_PAGE_REC_LSB, MBX_AMAP_PAGE_REC_WIDTH}},
        {{MBX_FACE_REG_EDIT_REQ, MBX_EDIT_REQ_TYPE_LSB, MBX_EDIT_REQ_TYPE_WIDTH},
         {MBX_FACE_REG_EDIT_REQ, MBX_EDIT_REQ_INDEX_LSB, MBX_EDIT_REQ_INDEX_WIDTH},
         {MBX_FACE_REG_EDIT_BEAT, MBX_EDIT_BEAT_PHASE_LSB, MBX_EDIT_BEAT_PHASE_WIDTH},
         {MBX_FACE_REG_EDIT_BEAT, MBX_EDIT_BEAT_REMOVE_LSB, MBX_EDIT_BEAT_REMOVE_WIDTH},
         {MBX_FACE_REG_EDIT_BEAT, MBX_EDIT_BEAT_REC_LSB, MBX_EDIT_BEAT_REC_WIDTH},
         {MBX_FACE_REG_EDIT_BEAT, MBX_EDIT_BEAT_COUNT_LSB, MBX_EDIT_BEAT_COUNT_WIDTH},
         {MBX_FACE_REG_EDIT_RECORD_LO, 0, 64, MBX_FACE_REG_EDIT_RECORD_HI},
         {MBX_FACE_REG_EDIT_VALUE_LO, 0, 64, MBX_FACE_REG_EDIT_VALUE_HI}},
        {{MBX_FACE_REG_GSI_REQ, MBX_GSI_REQ_TYPE_LSB, MBX_GSI_REQ_TYPE_WIDTH},
         {MBX_FACE_REG_GSI_REQ, MBX_GSI_REQ_INDEX_LSB, MBX_GSI_REQ_INDEX_WIDTH},
         {MBX_FACE_REG_GSI_SEL, MBX_GSI_SEL_KIND_LSB, MBX_GSI_SEL_KIND_WIDTH},
         {MBX_FACE_REG_GSI_SEL, MBX_GSI_SEL_SEL_LSB, MBX_GSI_SEL_SEL_WIDTH},
         {MBX_FACE_REG_GSI_SEL, MBX_GSI_SEL_ORD_LSB, MBX_GSI_SEL_ORD_WIDTH},
         {MBX_FACE_REG_GSI_PROP_LO, 0, 64, MBX_FACE_REG_GSI_PROP_HI}},
    };
    return v[w];
}

//! What the face block drives into one interface's datapath (contract 2.3):
//! each value as KL_mbx's fw_*_o and window ports carry it on the RTL, and as
//! mbx_model_face_view() reports it on the host model.
struct FaceView {
    std::uint32_t send = 0;                     //!< fw_send_o: a commit waits for its acknowledgement
    std::vector<std::uint64_t> setting;         //!< every setting field, in setting_fields() order
    std::vector<std::uint64_t> pt_offset;       //!< per source: F_PT_OFFSET.NS
    std::vector<std::uint64_t> fmt_out;         //!< per source: F_FMT_OUT_HI:F_FMT_OUT_LO
    std::vector<std::uint64_t> fmt_in;          //!< per sink: F_FMT_IN_HI:F_FMT_IN_LO
    std::uint32_t pt_offset_v = 0;              //!< bit s: F_SRC_VALID.PT_OFFSET of source s
    std::uint32_t fmt_out_v = 0;                //!< bit s: F_SRC_VALID.FMT_OUT of source s
    std::uint32_t fmt_in_v = 0;                 //!< bit k: F_SNK_VALID.FMT_IN of sink k
    std::uint32_t req[kWindows] = {};           //!< <window>_req_o
    std::uint32_t tag[kWindows] = {};           //!< <window>_tag_o
    std::vector<std::uint64_t> fields[kWindows];   //!< each request field, in window_fields() order
};

inline bool same_face(const FaceView& a, const FaceView& b) {
    bool same = a.send == b.send && a.setting == b.setting && a.pt_offset == b.pt_offset && a.fmt_out == b.fmt_out &&
                a.fmt_in == b.fmt_in && a.pt_offset_v == b.pt_offset_v && a.fmt_out_v == b.fmt_out_v &&
                a.fmt_in_v == b.fmt_in_v;
    for (unsigned w = 0; w < kWindows; ++w) {
        same = same && a.req[w] == b.req[w] && a.tag[w] == b.tag[w] && a.fields[w] == b.fields[w];
    }
    return same;
}

//! A FaceView from the register words a model holds: word(reg) is setting
//! register reg's word, src(s, reg) and snk(k, reg) an entry's.
template <class Word, class Src, class Snk, class Req>
FaceView face_from_words(std::uint32_t send, Word word, Src src, Snk snk, const std::uint32_t* req,
                         const std::uint32_t* tag, Req request) {
    auto take = [](std::uint32_t w, std::uint32_t lsb, std::uint32_t width) -> std::uint64_t {
        return width >= 32u ? w : ((w >> lsb) & ((1u << width) - 1u));
    };
    FaceView v;
    v.send = send;
    for (const FaceField& f : setting_fields()) {
        v.setting.push_back(take(word(f.reg), f.lsb, f.width));
    }
    for (unsigned s = 0; s < MBX_N_PUB_SOURCES; ++s) {
        v.pt_offset.push_back(src(s, MBX_FACE_SRC_REG_F_PT_OFFSET));
        v.fmt_out.push_back((std::uint64_t{src(s, MBX_FACE_SRC_REG_F_FMT_OUT_HI)} << 32) |
                            src(s, MBX_FACE_SRC_REG_F_FMT_OUT_LO));
        const std::uint32_t valid = src(s, MBX_FACE_SRC_REG_F_SRC_VALID);
        v.pt_offset_v |= static_cast<std::uint32_t>(take(valid, MBX_F_SRC_VALID_PT_OFFSET_LSB, 1)) << s;
        v.fmt_out_v |= static_cast<std::uint32_t>(take(valid, MBX_F_SRC_VALID_FMT_OUT_LSB, 1)) << s;
    }
    for (unsigned k = 0; k < MBX_N_PUB_SINKS; ++k) {
        v.fmt_in.push_back((std::uint64_t{snk(k, MBX_FACE_SNK_REG_F_FMT_IN_HI)} << 32) |
                           snk(k, MBX_FACE_SNK_REG_F_FMT_IN_LO));
        v.fmt_in_v |= static_cast<std::uint32_t>(take(snk(k, MBX_FACE_SNK_REG_F_SNK_VALID),
                                                      MBX_F_SNK_VALID_FMT_IN_LSB, 1)) << k;
    }
    for (unsigned w = 0; w < kWindows; ++w) {
        v.req[w] = req[w];
        v.tag[w] = tag[w];
        for (const FaceField& f : window_fields(w)) {
            v.fields[w].push_back(f.width == 64u ? (std::uint64_t{request(w, f.hi)} << 32) | request(w, f.reg)
                                                 : take(request(w, f.reg), f.lsb, f.width));
        }
    }
    return v;
}

constexpr std::uint16_t kEtherAvtp = 0x22F0;   // IEEE 1722-2016 Table 5
constexpr std::uint16_t kEtherMsrp = 0x22EA;   // IEEE 802.1Q-2018 Table 10-2
constexpr std::uint16_t kEtherMvrp = 0x88F5;   // IEEE 802.1Q-2018 Table 10-2
constexpr std::uint16_t kEtherVlan = 0x8100;   // IEEE 802.1Q-2018 Table 9-1
constexpr std::uint16_t kEtherPtp = 0x88F7;    // IEEE 802.1AS-2020 11.3.4: not a control EtherType here
constexpr std::uint8_t kSubAaf = 0x02;          // IEEE 1722-2016 Table 6
constexpr std::uint8_t kSubCrf = 0x04;          // IEEE 1722-2016 Table 6
constexpr std::uint8_t kSubAdp = 0xFA;          // IEEE 1722.1-2021 6.2.2.1
constexpr std::uint8_t kSubAecp = 0xFB;         // IEEE 1722.1-2021 9.2.2.1.1
constexpr std::uint8_t kSubAcmp = 0xFC;         // IEEE 1722.1-2021 8.2.2.1
constexpr std::uint8_t kSubReserved = 0xFD;     // IEEE 1722-2016 Table 6: reserved, no format assigned
constexpr std::uint8_t kSubMaap = 0xFE;         // IEEE 1722-2016 B.2.1
constexpr std::uint64_t kSrcMac = 0x0011223344A5ull;
constexpr std::uint64_t kAdpAcmpMac = 0x91E0F0010000ull;   // IEEE 1722.1-2021 Table B.1: ADP and ACMP
constexpr std::uint64_t kIdentifyMac = 0x91E0F0010001ull;  // IEEE 1722.1-2021 Table B.1: identification
constexpr std::uint64_t kMaapMac = 0x91E0F000FF00ull;      // IEEE 1722-2016 Table B.10
constexpr std::uint64_t kMsrpMac = 0x0180C200000Eull;      // IEEE 802.1Q-2018 35.2.2.1 (Table 8-1)
constexpr std::uint64_t kMvrpMac = 0x0180C2000021ull;      // IEEE 802.1Q-2018 Table 10-1
constexpr std::uint64_t kStreamMac = 0x91E0F000FE01ull;    // IEEE 1722-2016 Table B.9: a static stream address
//! The unicast MAC the suite gives interface 0 (OWN_MAC); interface i takes
//! kOwnMac + i, so each interface's is its own.
constexpr std::uint64_t kOwnMac = 0x001B92000001ull;
//! A unicast MAC no interface owns: traffic a switch floods.
constexpr std::uint64_t kForeignMac = 0x001B92000099ull;

inline void put_be(std::vector<std::uint8_t>& f, std::size_t at, std::uint64_t v, unsigned n) {
    for (unsigned i = 0; i < n; ++i) {
        f[at + i] = static_cast<std::uint8_t>(v >> (8u * (n - 1u - i)));
    }
}

//! An untagged Ethernet header with `len` frame bytes in all.
inline std::vector<std::uint8_t> eth(std::uint64_t dst, std::uint16_t ethertype, std::size_t len) {
    std::vector<std::uint8_t> f(len, 0);
    put_be(f, 0, dst, 6);
    put_be(f, 6, kSrcMac, 6);
    put_be(f, 12, ethertype, 2);
    return f;
}

//! An ADPDU (Figure 6-1): entity_id at wire byte 18, control_data_length 56.
//! `len` other than 82 truncates or zero-pads the 82-byte frame.
inline std::vector<std::uint8_t> adpdu(std::uint8_t message_type, std::uint64_t entity_id,
                                       std::size_t len = 82) {
    auto f = eth(0x91E0F0010000ull, kEtherAvtp, 82);
    f[14] = kSubAdp;
    f[15] = message_type & 0x0Fu;
    put_be(f, 16, 56, 2);
    put_be(f, 18, entity_id, 8);
    f.resize(len, 0);
    return f;
}

//! An ACMPDU (Figure 8-1): talker_entity_id at 34, listener_entity_id at 42.
inline std::vector<std::uint8_t> acmpdu(std::uint8_t message_type, std::uint64_t talker,
                                        std::uint64_t listener) {
    auto f = eth(0x91E0F0010000ull, kEtherAvtp, 70);
    f[14] = kSubAcmp;
    f[15] = message_type & 0x0Fu;
    put_be(f, 16, 44, 2);
    put_be(f, 34, talker, 8);
    put_be(f, 42, listener, 8);
    return f;
}

//! An AECPDU (Figure 9-1): target_entity_id at 18, an AEM_COMMAND unicast
//! to interface 0's own MAC.
inline std::vector<std::uint8_t> aecpdu(std::uint64_t target, std::size_t len = 64) {
    auto f = eth(kOwnMac, kEtherAvtp, len);
    f[14] = kSubAecp;
    put_be(f, 18, target, 8);
    return f;
}

//! An AECPDU of any message_type (Table 9-1), both identities and its
//! destination: target_entity_id at 18, controller_entity_id at 26,
//! sequence_id at 34, and for an AEM PDU the command_type at 36 (7.4).
inline std::vector<std::uint8_t> aecp(std::uint8_t message_type, std::uint64_t target, std::uint64_t controller,
                                      std::uint64_t dst = kOwnMac, std::uint16_t command_type = 0) {
    auto f = eth(dst, kEtherAvtp, 64);
    f[14] = kSubAecp;
    f[15] = message_type & 0x0Fu;
    put_be(f, 16, 12, 2);
    put_be(f, 18, target, 8);
    put_be(f, 26, controller, 8);
    put_be(f, 34, 0x0102, 2);
    put_be(f, 36, command_type, 2);
    return f;
}

//! The CONTROLLER_AVAILABLE command type (IEEE 1722.1-2021 7.4.4, Table
//! 7-140; Milan v1.2 5.4.5.3 sends it to a registered controller as a
//! liveness probe).
constexpr std::uint16_t kControllerAvailable = 0x0003;

//! The frame with an 802.1Q C-tag (TPID 0x8100, then PCP 3 and VID 2, the SR
//! class A tag) inserted after the source address (802.1Q-2018 9.3).
inline std::vector<std::uint8_t> tagged(const std::vector<std::uint8_t>& untagged) {
    std::vector<std::uint8_t> f(untagged.begin(), untagged.begin() + 12);
    const std::uint8_t tag[] = {0x81, 0x00, 0x60, 0x02};
    f.insert(f.end(), tag, tag + 4);
    f.insert(f.end(), untagged.begin() + 12, untagged.end());
    return f;
}

//! The frame with its destination MAC replaced.
inline std::vector<std::uint8_t> to(std::vector<std::uint8_t> f, std::uint64_t dst) {
    put_be(f, 0, dst, 6);
    return f;
}

//! The frame with its EtherType replaced.
inline std::vector<std::uint8_t> with_ethertype(std::vector<std::uint8_t> f, std::uint16_t ethertype) {
    put_be(f, 12, ethertype, 2);
    return f;
}

//! The frame with byte 14 (the AVTP subtype; ProtocolVersion in an MRPDU) replaced.
inline std::vector<std::uint8_t> with_subtype(std::vector<std::uint8_t> f, std::uint8_t subtype) {
    f[14] = subtype;
    return f;
}

//! An AVTP stream data PDU (AAF or CRF) of `len` bytes to a stream address.
inline std::vector<std::uint8_t> stream_pdu(std::uint8_t subtype, std::uint64_t dst = kStreamMac,
                                            std::size_t len = 80) {
    auto f = eth(dst, kEtherAvtp, len);
    f[14] = subtype;
    f[15] = 0x81;   // sv set, version 0, mr 0, tv 1
    return f;
}

//! A MAAP PDU (Figure B.4): requested_start_address at 26, requested_count at 32.
inline std::vector<std::uint8_t> maap(std::uint8_t message_type, std::uint64_t start, std::uint16_t count) {
    auto f = eth(0x91E0F000FF00ull, kEtherAvtp, 42);
    f[14] = kSubMaap;
    f[15] = message_type & 0x0Fu;
    put_be(f, 26, start, 6);
    put_be(f, 32, count, 2);
    return f;
}

//! An MRPDU frame: ProtocolVersion 0 at byte 14, then `body` (802.1Q 10.8).
inline std::vector<std::uint8_t> mrp(std::uint16_t ethertype, const std::vector<std::uint8_t>& body) {
    auto f = eth(ethertype == kEtherMsrp ? 0x0180C200000Eull : 0x0180C2000021ull, ethertype, 15 + body.size());
    for (std::size_t i = 0; i < body.size(); ++i) {
        f[15 + i] = body[i];
    }
    return f;
}

}  // namespace mbx_tb

#endif  // MBX_FRAMES_HPP

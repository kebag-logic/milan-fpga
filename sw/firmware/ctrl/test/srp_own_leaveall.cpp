// SPDX-License-Identifier: CERN-OHL-W-2.0
// lwSRP #20 at the board: a Listener withdrawn just after the board's own LeaveAll is sent as Lv.
// Two stations share one link here. The board is this firmware's SRP adapter on the mailbox model. The peer is an
// lwSRP MSRP participant standing for the talker side, its Registrar Milan's (IN / rLv! -> MT, Milan v1.2 4.2.7.2.2),
// with an allocation pool of its own. The peer declares the Domain and a Talker Advertise for every input's stream;
// the board binds every input, so it declares each Listener Ready and its own LeaveAll MRPDUs carry each Join.
// - A withdrawal: 5 to 200 ms after the board's LeaveAll MRPDU that carried an input's Listener Join, the input is
//   unbound. The board sends that Listener's Lv within 240 ms of the unbinding (joinTime's maximum, Milan v1.2
//   Table 4.3), the peer deregisters it on that Lv, and every input still bound stays registered.
// - No withdrawal: across the board's LeaveAlls and the peer's, every Listener stays registered at the peer, with no
//   Leave indication (IEEE 802.1Q-2018 10.8 NOTE 2: a LeaveAll precedes the messages of its MRPDU).
// Run at 8x8/1if, every input, and at 1x1/1if (test_ctrl_firmware.py).
#include "srp_fixture.hpp"
#include <array>
#include <cstdio>
FW_TALLY_LABEL("ctrl SRP own LeaveAll");
namespace {
constexpr unsigned kLvBoundMs = 240;     // Milan v1.2 Table 4.3: joinTime at most 240 ms
constexpr unsigned kEvJoinIn = 1, kEvJoinMt = 3, kEvLv = 5;   // IEEE 802.1Q-2018 10.8.2.5

// Input k's stream, its Talker's destination and VID 2 (locally administered).
msrp_stream_id stream(unsigned k) { return {{0x02,0x00,0x00,0x00,0x00,0x10,0x00,static_cast<uint8_t>(k)}}; }
std::array<uint8_t,6> destination(unsigned k) { return {0x91,0xe0,0xf0,0x00,0xfe,static_cast<uint8_t>(k)}; }
int input_of(const uint8_t *id) {
    for (unsigned k=0;k<CTRL_SRP_SINKS;++k) if (std::memcmp(stream(k).bytes,id,8)==0) return static_cast<int>(k);
    return -1;
}

// What the peer's Registrar did with each input's Listener.
struct PeerRecord {
    uint32_t registered = 0;                  // bit k: input k's Listener registered Ready
    std::array<unsigned,CTRL_SRP_SINKS> leaves{};
    std::array<uint32_t,CTRL_SRP_SINKS> left_ms{};
    const mbx_model *clock = nullptr;
} peer_record;
void peer_joined(mrp_app *, uint8_t, uint8_t type, const void *value, bool) {
    const auto *v = static_cast<const uint8_t *>(value);
    const int k = type==MSRP_ATTR_TYPE_LISTENER ? input_of(v) : -1;
    if (k>=0 && v[8]==MSRP_LISTENER_DECL_READY) peer_record.registered |= 1u<<k;
}
void peer_left(mrp_app *, uint8_t, uint8_t type, const void *value) {
    const int k = type==MSRP_ATTR_TYPE_LISTENER ? input_of(static_cast<const uint8_t *>(value)) : -1;
    if (k<0) return;
    peer_record.registered &= ~(1u<<k);
    ++peer_record.leaves[k];
    peer_record.left_ms[k] = peer_record.clock->now_ms;
}

// One of the board's MSRP frames, read from IEEE 802.1Q-2018 10.8.1.2 and 35.2.2 apart from both lwSRP parsers.
struct BoardFrame {
    uint32_t ms = 0;
    bool leave_all = false;                   // any vector's LeaveAllEvent is LeaveAll
    std::array<int,CTRL_SRP_SINKS> listener{};  // each input's Listener AttributeEvent, or -1
};
BoardFrame read_board(const mbx_model_tx *f) {
    BoardFrame b; b.ms = f->now_ms; b.listener.fill(-1);
    const uint8_t *p = f->bytes+14; const unsigned len = f->len-14u;
    unsigned off = 1;
    while (off+2<=len && (p[off] || p[off+1])) {
        const unsigned type = p[off], width = p[off+1];
        const unsigned end = off+4+wire_be16(p+off+2);   // AttributeListLength (35.2.2.6)
        off += 4;
        while (off+2<=end && (p[off] || p[off+1])) {
            const unsigned vh = wire_be16(p+off), n = vh&8191u;
            off += 2;
            b.leave_all = b.leave_all || (vh>>13)==1u;
            for (unsigned v=0;v<n && type==MSRP_ATTR_TYPE_LISTENER;++v) {
                const unsigned packed = p[off+width+v/3];
                const unsigned ev = v%3==0 ? packed/36 : v%3==1 ? (packed/6)%6 : packed%6;
                uint8_t id[8]; std::memcpy(id,p+off,8);
                wire_put_be(id+6,wire_be16(id+6)+v,2);    // 35.2.2.8: the UniqueID counts the vector
                const int k = input_of(id);
                if (k>=0) b.listener[k] = static_cast<int>(ev);
            }
            off += width+(n+2)/3+(type==MSRP_ATTR_TYPE_LISTENER ? (n+3)/4 : 0);
        }
        off = end;
    }
    return b;
}

class OwnLeaveAll : public Srp {
protected:
    ctrl_pool peer_pool{};
    alignas(std::max_align_t) uint8_t peer_arena[SRP_POOL_ARENA_BYTES]{};
    mrp_app *peer = nullptr;
    uint32_t delivered = 0;                   // the board's next frame for the peer
    std::vector<BoardFrame> board;            // the board's MSRP frames, in order
    unsigned peer_leave_alls = 0;
    std::array<uint8_t,1514> peer_frame{};

    // Every call into the peer allocates and frees from the peer's own pool.
    template<class Fn> void as_peer(Fn fn) {
        shlan_port_bind_pool(&peer_pool); fn(); shlan_port_bind_pool(&pool);
    }
    void start_peer(uint32_t leave_all_cs) {
        peer_record = PeerRecord{}; peer_record.clock = &model;
        ASSERT_TRUE(ctrl_pool_init(&peer_pool,peer_arena,sizeof(peer_arena),srp_pool_classes,SRP_POOL_N_CLASSES));
        as_peer([&] {
            msrp_ctx none{};
            mrp_app *prototype = msrp_app_create(1,&none);
            ASSERT_NE(prototype,nullptr);
            mrp_app_ops ops = *prototype->ops;
            msrp_app_destroy(prototype);
            ASSERT_TRUE(ops.milan_rapid_leave) << "the firmware's lwSRP is built for Milan";
            ops.join_ind = peer_joined; ops.leave_ind = peer_left;
            ops.map_join = nullptr; ops.map_leave = nullptr; ops.ctx = nullptr;   // an end station
            peer = mrp_app_create(&ops,1);
            ASSERT_NE(peer,nullptr);
            // JoinTime 200 ms and LeaveTime 5 s (Milan v1.2 Table 4.3); a point-to-point link
            ASSERT_EQ(mrp_port_configure(peer,0,20,500,leave_all_cs,0x5eedu,true),0);
            const msrp_domain domain{6,3,2};
            ASSERT_EQ(mrp_mad_join(peer,0,MSRP_ATTR_TYPE_DOMAIN,&domain,true),0);
            for (unsigned k=0;k<CTRL_SRP_SINKS;++k) {
                msrp_talker_adv t{};
                t.stream_id = stream(k);
                const auto da = destination(k);
                std::memcpy(t.dest_mac,da.data(),6);
                t.vlan_id = 2; t.max_frame_size = 224; t.max_interval_frames = 1; t.priority_and_rank = 0x60;
                ASSERT_EQ(msrp_declare_talker(peer,0,&t,true),0);
            }
        });
    }
    void TearDown() override {
        if (peer) as_peer([&] { mrp_app_destroy(peer); });
        peer = nullptr;
        EXPECT_EQ(ctrl_pool_in_use(&peer_pool),0u);
        Srp::TearDown();
    }
    static int peer_send(void *ctx, uint8_t, const uint8_t *pdu, size_t len) {
        auto *t = static_cast<OwnLeaveAll *>(ctx);
        std::vector<uint8_t> f(14+len);
        wire_put_be(f.data(),0x0180c200000eull,6);
        wire_put_be(f.data()+6,0x020304010203ull,6);
        wire_put_be(f.data()+12,0x22ea,2);
        std::memcpy(f.data()+14,pdu,len);
        // A frame the SRP channel's bucket holds is committed by its next refill (mbx_model_rx).
        (void)mbx_model_rx(&t->model,f.data(),f.size(),0);
        return 0;
    }
    // One millisecond on the link: the board runs, its MSRP frames reach the peer, the peer's reach the board.
    void step() {
        mbx_model_advance_ms(&model,1); settle();
        for (; delivered<model.tx_sent; ++delivered) {
            const auto *f = mbx_model_tx_frame(&model,delivered);
            ASSERT_NE(f,nullptr) << "the board's frame left the capture before the peer read it";
            if (wire_be16(f->bytes+12)!=0x22ea) continue;
            board.push_back(read_board(f));
            as_peer([&] { EXPECT_EQ(mrp_rx(peer,0,f->bytes+14,f->len-14u),0); });
        }
        as_peer([&] {
            const int sent = mrp_transmit(peer,0,peer_frame.data()+14,peer_frame.size()-14,peer_send,this);
            EXPECT_GE(sent,0);
            if (sent==1 && peer_frame[14+5]>>5==1u) ++peer_leave_alls;   // its first vector flags LeaveAll
        });
        settle();
    }
    void run_until(uint32_t ms) { while (model.now_ms<ms && !HasFatalFailure()) step(); }
    void bind(unsigned k) {
        const auto sid = stream(k); const auto da = destination(k);
        ASSERT_TRUE(srp_mbx_bind(&adapter,0,k,&sid,da.data(),2));
    }
    // The ACMP side retries a refused unbinding (srp_mbx.h); returns when the adapter took it.
    void unbind(unsigned k) {
        for (unsigned n=0;n<100u && !srp_mbx_bind(&adapter,0,k,nullptr,nullptr,0);++n) step();
        ASSERT_FALSE(adapter.ifs[0].sinks[k].bound);
    }
    // Every input bound and registered Ready at the peer.
    void bind_every_input() {
        settle();
        for (unsigned k=0;k<CTRL_SRP_SINKS;++k) bind(k);
        const uint32_t all = CTRL_SRP_SINKS>=32u ? ~0u : (1u<<CTRL_SRP_SINKS)-1u;
        const uint32_t limit = model.now_ms+2000u;
        while (peer_record.registered!=all && model.now_ms<limit && !HasFatalFailure()) step();
        ASSERT_EQ(peer_record.registered,all) << "every input's Listener registered Ready at the peer";
    }
    // The time of the board's next LeaveAll MRPDU after `from` that carries input k's Listener Join.
    uint32_t own_leave_all_with(unsigned k, size_t from) {
        const uint32_t limit = model.now_ms+16000u;   // 10.7.4.3: a leavealltimer draw is under 15 s
        for (size_t n=from;;++n) {
            while (n>=board.size()) {
                if (model.now_ms>=limit || HasFatalFailure()) {
                    ADD_FAILURE() << "no own LeaveAll carrying input " << k << "'s Listener Join";
                    return 0;
                }
                step();
            }
            const int ev = board[n].listener[k];
            if (board[n].leave_all && (ev==static_cast<int>(kEvJoinIn) || ev==static_cast<int>(kEvJoinMt))) {
                return board[n].ms;
            }
        }
    }
};

// A withdrawal `offset` ms after the board's own LeaveAll MRPDU that carried the Listener's Join, input by input.
class OwnLeaveAllWithdrawal : public OwnLeaveAll, public ::testing::WithParamInterface<unsigned> {};

TEST_P(OwnLeaveAllWithdrawal, TheLvGoesOutWithinJoinTimeOnEveryInput) {
    const unsigned offset = GetParam();
    // The peer's LeaveAllTime is long, so the board's leavealltimer runs out first: every LeaveAll is the board's own.
    start_peer(3000);
    bind_every_input();
    for (unsigned k=0;k<CTRL_SRP_SINKS && !HasFatalFailure();++k) {
        const uint32_t leave_all = own_leave_all_with(k,board.size());
        run_until(leave_all+offset);
        const uint32_t asked = model.now_ms;
        unbind(k);
        const size_t from = board.size();
        uint32_t lv = 0; bool sent = false;
        while (!sent && model.now_ms<asked+kLvBoundMs+50u && !HasFatalFailure()) {
            step();
            for (size_t n=from;n<board.size() && !sent;++n) {
                if (board[n].listener[k]==static_cast<int>(kEvLv)) { sent = true; lv = board[n].ms; }
            }
        }
        EXPECT_TRUE(sent) << "input " << k << ": no Lv within " << kLvBoundMs << " ms of a withdrawal " << offset
                          << " ms after the board's LeaveAll";
        if (sent) {
            EXPECT_LE(lv-asked,kLvBoundMs) << "input " << k << ", offset " << offset;
        }
        std::printf("OWN-LA input=%u offset_ms=%u leaveall_ms=%u withdrawn_ms=%u lv_ms=%s%u peer_left_ms=%u\n",
                    k,offset,leave_all,asked,sent ? "" : "none>",sent ? lv : asked+kLvBoundMs+50u,
                    peer_record.left_ms[k]);
        EXPECT_EQ(peer_record.leaves[k],sent ? 1u : 0u) << "input " << k << ": the peer deregisters on the Lv";
        EXPECT_EQ(peer_record.registered>>k & 1u,0u) << "input " << k << " withdrawn at the peer";
        for (unsigned j=k+1;j<CTRL_SRP_SINKS;++j) {
            EXPECT_EQ(peer_record.registered>>j & 1u,1u) << "input " << j << " stays registered";
            EXPECT_EQ(peer_record.leaves[j],0u) << "input " << j << " stays registered";
        }
    }
    // Withdrawn means withdrawn: no input re-declares after its Lv.
    run_until(model.now_ms+2000u);
    for (unsigned k=0;k<CTRL_SRP_SINKS;++k) {
        EXPECT_EQ(peer_record.leaves[k],1u) << "input " << k;
    }
    EXPECT_EQ(peer_record.registered,0u);
}

// 5 to 200 ms in 5 ms steps, the qualification's 129 ms, and either side of the board's 190 ms join timer.
std::vector<unsigned> offsets() {
    std::vector<unsigned> o;
    for (unsigned ms=5;ms<=200;ms+=5) o.push_back(ms);
    for (unsigned ms : {129u,189u,191u}) o.push_back(ms);
    return o;
}
INSTANTIATE_TEST_SUITE_P(FiveTo200Ms, OwnLeaveAllWithdrawal, ::testing::ValuesIn(offsets()));

TEST_F(OwnLeaveAll, EveryListenerStaysRegisteredAcrossBothStationsLeaveAlls) {
    // Both stations' LeaveAllTime is 10 s, so each sends LeaveAlls of its own (the other's restarts its timer).
    start_peer(1000);
    bind_every_input();
    const size_t from = board.size();
    run_until(model.now_ms+90000u);
    unsigned own = 0;
    const uint32_t all = CTRL_SRP_SINKS>=32u ? ~0u : (1u<<CTRL_SRP_SINKS)-1u;
    for (size_t n=from;n<board.size();++n) {
        if (!board[n].leave_all) continue;
        ++own;
        for (unsigned k=0;k<CTRL_SRP_SINKS;++k) {
            const int ev = board[n].listener[k];
            EXPECT_TRUE(ev==static_cast<int>(kEvJoinIn) || ev==static_cast<int>(kEvJoinMt))
                << "input " << k << ": the board's LeaveAll at " << board[n].ms << " ms re-declares the Listener";
        }
    }
    std::printf("OWN-LA held inputs=%u span_ms=%u board_frames=%zu board_leavealls=%u peer_leavealls=%u\n",
                CTRL_SRP_SINKS,model.now_ms,board.size()-from,own,peer_leave_alls);
    EXPECT_GE(own,3u) << "the board's own LeaveAlls";
    EXPECT_GE(peer_leave_alls,2u) << "the peer's own LeaveAlls";
    EXPECT_EQ(peer_record.registered,all);
    for (unsigned k=0;k<CTRL_SRP_SINKS;++k) EXPECT_EQ(peer_record.leaves[k],0u) << "input " << k;
    for (const auto &f : board) {
        for (unsigned k=0;k<CTRL_SRP_SINKS;++k) EXPECT_NE(f.listener[k],static_cast<int>(kEvLv)) << "input " << k;
    }
}
} // namespace

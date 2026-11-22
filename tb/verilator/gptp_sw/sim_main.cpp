// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// sim_main.cpp - gPTP in firmware locks to modelled peers over the mailbox and the timestamp units (#884, #665 F6).
//
// THE FIRMWARE is the split image's gPTP: the end station ports and their adapter (sw/firmware/ctrl/gptp), the loop
// and the mailbox driver, on the host mailbox model at two interfaces (contract 2.5: the gptp channel with its
// ingress trailer, the TIMESTAMP event, the narrowed gPTP publication). THE FABRIC is tb_gptp_sw.sv, once an
// interface (Milan v1.2 8.3.4: one end station an AVB interface, so one PHC and one timestamp unit a MAC; #884's
// ruling of 2026-11-21, item 5): the PHC the firmware's servo steers, the launch observer on the MAC's transmit
// stream, the timestamp unit and the split's control tap, whose bytes the mailbox model takes. THE PEERS are this
// file's own model, written apart from the firmware: each an ideal clock of its own rate and phase, a 300 ns link,
// and Milan v1.2 Table 4.1's intervals.
//
// Runs (argv selects; all by default):
//   slave   each interface's peer is a grandmaster (priority1 100) of its own, on its own clock: interface 0's
//           1000 s ahead of its PHC and 40 ppm fast, interface 1's 500 s ahead and 25 ppm slow. Each port must step
//           once and lock its own PHC to its own grandmaster, with no bridge between them (8.3.4). Then the
//           published snapshot: the words the datapath takes are the snapshot's, the AECP owner's GET_AVB_INFO and
//           GET_AS_PATH answers are the snapshot's, and the AVB_INFO and AS_PATH changes were raised (ruling 7).
//           Then a Pdelay_Req cut short by its last eight octets must be refused, not answered: the trailer is not
//           the message's. Last, interface 1's grandmaster falls silent, and the grandmaster its port takes on its
//           announce receipt timeout, a tick's work, must be published.
// In every run, no pass leaves a port's change for a later one (the adapter publishes from its callbacks).
//   master  each peer is a slave (priority1 250) with a servo of its own; each port is grandmaster, and each peer
//           must lock to its own PHC through the firmware's Sync, Follow_Up and Pdelay answers.
//   flood   interface 0's grandmaster also sends bursts of 32 Pdelay_Req back to back, past the gptp channel's
//           admission (burst 16): the port keeps its lock, the mailbox refuses the excess, and every event message
//           it admits reached the firmware with its own stamp (ruling 2).
// Every offset is read from outside: each PHC's own counter against its peer's model clock at the same instant.
//
// Each check prints its words; the tally is the record. Exit 0 = PASS.

#include <array>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <deque>
#include <iterator>
#include <string>
#include <vector>

#include "Vtb_gptp_sw.h"
#include "verilated.h"

extern "C" {
#include "ctrl_loop.h"
#include "gptp_mbx.h"
#include "mbx_model.h"
}

namespace {

int checks = 0;
int failures = 0;
void check(bool ok, const std::string &what, double got = 0, double exp = 0)
{
	checks++;
	if (!ok) {
		failures++;
		std::printf("  [FAIL] %s got=%.3f exp=%.3f\n", what.c_str(), got, exp);
	}
}

using Bytes = std::vector<uint8_t>;
constexpr uint64_t kPs = 1000;        // ps a ns
constexpr int64_t kLinkNs = 300;      // each link's one-way delay
constexpr unsigned kIf = MBX_N_IF;
constexpr uint16_t kCutSeq = 0x6666;  // the cut Pdelay_Req's sequenceId (run slave)
static_assert(kIf == 2, "the closed loop runs two interfaces (make generates the two-interface contract)");

void be(Bytes &f, size_t at, uint64_t v, unsigned n)
{
	for (unsigned i = 0; i < n; i++)
		f[at + i] = uint8_t(v >> (8 * (n - 1 - i)));
}
uint64_t rd(const Bytes &f, size_t at, unsigned n)
{
	uint64_t v = 0;
	for (unsigned i = 0; i < n; i++)
		v = (v << 8) | f[at + i];
	return v;
}
void ts10(Bytes &f, size_t at, uint64_t ns)
{
	be(f, at, ns / 1000000000ull, 6);
	be(f, at + 6, ns % 1000000000ull, 4);
}
uint64_t ts10_get(const Bytes &f, size_t at)
{
	return rd(f, at, 6) * 1000000000ull + rd(f, at + 6, 4);
}

// ---- the bench's packed ports: bits [lsb +: n] of a Verilator port, of any width
template <class T> void put(T &w, unsigned lsb, unsigned n, uint64_t v)
{
	const uint64_t mask = (n >= 64 ? ~0ull : ((1ull << n) - 1)) << lsb;
	w = T((uint64_t(w) & ~mask) | ((v << lsb) & mask));
}
template <class T> uint64_t get(const T &w, unsigned lsb, unsigned n)
{
	return (uint64_t(w) >> lsb) & (n >= 64 ? ~0ull : ((1ull << n) - 1));
}
template <std::size_t W> void put(VlWide<W> &w, unsigned lsb, unsigned n, uint64_t v)
{
	for (unsigned k = 0; k < n; k++) {
		const unsigned b = lsb + k;
		w[b / 32] = (w[b / 32] & ~(1u << (b % 32))) | (uint32_t((v >> k) & 1u) << (b % 32));
	}
}
template <std::size_t W> uint64_t get(const VlWide<W> &w, unsigned lsb, unsigned n)
{
	uint64_t v = 0;
	for (unsigned k = 0; k < n; k++) {
		const unsigned b = lsb + k;
		v |= uint64_t((w[b / 32] >> (b % 32)) & 1u) << k;
	}
	return v;
}

// ---- the peer: an independent model of a one-port 802.1AS time-aware system -------------------------------------
struct Peer {
	bool gm;                       // grandmaster (priority1 100), or a slave (250)
	long double ppm;      // its clock: base_ns + t * (1 + ppm 1e-6 + trim)
	long double base_ns;
	long double trim = 0;          // its own servo's rate correction (the slave)
	long double t_base = 0;
	uint64_t clock_id = 0x02AABBFFFE000001ull;
	uint16_t sync_seq = 0;
	uint16_t ann_seq = 0;
	uint16_t preq_seq = 0;
	long double next_sync = 0;
	long double next_ann = 0;
	long double next_preq = 0;
	// its own Pdelay as initiator
	uint16_t req_seq = 0;
	long double t1 = 0;
	long double t4 = 0;
	long double t2 = 0;
	long double t3 = 0;
	bool have_resp = false;
	std::vector<double> delays;
	// as a slave: the master's Sync waiting for its Follow_Up
	bool sync_wait = false;
	uint16_t sync_wait_seq = 0;
	long double sync_rx = 0;
	long double integ = 0;
	std::vector<double> slave_offsets;   // its measured offset from the master, each pair
	unsigned cut_answers = 0;            // Pdelay_Resp to the cut request (run slave), none expected

	long double at(long double t_ns) const { return base_ns + (t_ns - t_base) * (1.0L + ppm * 1e-6L + trim); }
	void rebase(long double t_ns)
	{
		base_ns = at(t_ns);
		t_base = t_ns;
	}
	Bytes msg(unsigned type, unsigned ptp_len, uint16_t seq, uint8_t control, int8_t logi) const
	{
		Bytes f(14 + ptp_len, 0);
		be(f, 0, 0x0180C200000Eull, 6);
		be(f, 6, 0x02AABB000001ull, 6);
		be(f, 12, 0x88F7, 2);
		f[14] = uint8_t(0x10 | type);
		f[15] = 0x12;
		be(f, 16, ptp_len, 2);
		be(f, 34, clock_id, 8);
		be(f, 42, 1, 2);
		be(f, 44, seq, 2);
		f[46] = control;
		f[47] = uint8_t(logi);
		return f;
	}
};

struct Pending { long double t_ns; Bytes f; };   // a frame on a link, arriving at t_ns of the bench

// one interface's fabric drive, peer and link
struct Lane {
	std::deque<int> gmii;                  // octets on the MAC's transmit stream; -1: no octet (the gap)
	Bytes rx_frame;
	size_t rx_at = 0;
	bool rx_busy = false;
	Bytes tap_bytes;                       // the frame the control tap is handing out
	std::deque<Pending> to_dut;            // the peer's frames, by arrival
	std::deque<Pending> to_peer;           // the firmware's frames, by arrival at the peer
	int adjust_hold = 0;
	Peer peer;
	bool peer_on = false;
	long double peer_free_ns = 0;
	bool flood = false;                    // the grandmaster's Pdelay_Req bursts (run flood)
	long double next_flood = 0;
	uint16_t flood_seq = 0x8000;
	// the mailbox's verdicts on what the tap handed it
	unsigned admitted_event = 0;           // event messages (majorSdoId 1, messageType 0 to 3) committed at once
	unsigned refused = 0;                  // frames the gptp channel refused or held (its admission, #917)
	std::vector<unsigned> handed;          // event messages the tap handed out: 1 each
	unsigned notices[8] = {};              // the AECP owner's change notices, by event bit
};

struct Bench {
	Vtb_gptp_sw t;
	uint64_t now_ps = 0;
	uint64_t next_dp = 0;   // the next rising edge of each clock
	uint64_t next_eth = 0;
	uint64_t eth_until_ps = 0;
	// firmware
	struct mbx_model model {};
	struct ctrl_loop loop {};
	struct gptp_mbx g {};
	unsigned tx_seen = 0;
	unsigned late = 0;   // passes that left a published port's change for a later one (no poll, #884)
	std::array<Lane, kIf> lane;
	unsigned ms = 0;

	long double ns() const { return (long double)now_ps / kPs; }
	uint64_t phc(unsigned i) { return get(t.phc_ns_o, 64 * i, 64); }

	// ---- the PHC HAL: each interface's CSR PTP block, as the firmware's servo drives it (REQ-PTP-02, 03)
	static void adjfine(void *ctx, unsigned i, int32_t addend) { put(static_cast<Bench *>(ctx)->t.phc_adj_i, 32 * i, 32, uint32_t(addend)); }
	static void step(void *ctx, unsigned i, int64_t delta)
	{
		Bench *b = static_cast<Bench *>(ctx);
		put(b->t.phc_offset_i, 64 * i, 64, uint64_t(delta));
		b->lane[i].adjust_hold = 1;
	}
	// ---- the AECP owner's change notice (ctrl_app_aecp_changed's events)
	static void changed(void *ctx, unsigned i, unsigned events)
	{
		Bench *b = static_cast<Bench *>(ctx);
		for (unsigned k = 0; k < 8; k++)
			if (events & (1u << k))
				b->lane[i].notices[k]++;
	}

	void edge_dp()
	{
		for (unsigned i = 0; i < kIf; i++) {
			Lane &l = lane[i];
			// the receive tap: one beat of eight octets a clock while a frame is being taken
			if (!l.rx_busy && !l.to_dut.empty() && l.to_dut.front().t_ns <= ns()) {
				l.rx_frame = l.to_dut.front().f;
				l.to_dut.pop_front();
				l.rx_at = 0;
				l.rx_busy = true;
			}
			if (l.rx_busy) {
				uint64_t d = 0;
				unsigned keep = 0;
				for (unsigned k = 0; k < 8 && l.rx_at + k < l.rx_frame.size(); k++) {
					d |= uint64_t(l.rx_frame[l.rx_at + k]) << (8 * k);
					keep |= 1u << k;
				}
				put(t.rx_tdata_i, 64 * i, 64, d);
				put(t.rx_tkeep_i, 8 * i, 8, keep);
				put(t.rx_tvalid_i, i, 1, 1);
				put(t.rx_tlast_i, i, 1, l.rx_at + 8 >= l.rx_frame.size());
			} else {
				put(t.rx_tvalid_i, i, 1, 0);
				put(t.rx_tlast_i, i, 1, 0);
			}
			put(t.phc_adjust_i, i, 1, l.adjust_hold > 0);
			put(t.s_rx_ready_i, i, 1, 1);
		}
		// the control taps' bytes are taken on this edge
		t.eval();
		bool took[kIf];
		uint8_t byte[kIf];
		bool last[kIf];
		for (unsigned i = 0; i < kIf; i++) {
			took[i] = get(t.s_rx_valid_o, i, 1);
			byte[i] = uint8_t(get(t.s_rx_data_o, 8 * i, 8));
			last[i] = get(t.s_rx_last_o, i, 1);
		}
		t.dp_clk_i = 1;
		t.eval();
		t.dp_clk_i = 0;
		t.eval();
		for (unsigned i = 0; i < kIf; i++) {
			Lane &l = lane[i];
			if (l.adjust_hold > 0)
				l.adjust_hold--;
			if (l.rx_busy) {
				l.rx_at += 8;
				if (l.rx_at >= l.rx_frame.size())
					l.rx_busy = false;
			}
			if (took[i]) {
				l.tap_bytes.push_back(byte[i]);
				if (last[i]) {
					// the record the gptp ring takes: the frame and its trailer, as the tap handed them out
					const Bytes &f = l.tap_bytes;
					const bool event = f.size() > 23 && rd(f, 12, 2) == 0x88F7 && (f[14] >> 4) == 1 && (f[14] & 0xF) <= 3;
					if (event)
						l.handed.push_back(1);
					if (mbx_model_rx(&model, f.data(), f.size(), i))
						l.admitted_event += event;
					else
						l.refused++;
					l.tap_bytes.clear();
				}
			}
			// the egress record FIFO, drained into the mailbox's TIMESTAMP events
			put(t.ts_take_i, i, 1, 0);
			if (get(t.ts_valid_o, i, 1)) {
				const uint64_t hi = get(t.ts_data_o, 86 * i + 64, 22);
				const uint64_t ns_v = get(t.ts_data_o, 86 * i, 64);
				mbx_model_timestamp(&model, i, (hi >> 21) & 1u, (hi >> 20) & 1u, uint8_t((hi >> 16) & 0xFu),
						    uint16_t(hi & 0xFFFFu), ns_v);
				put(t.ts_take_i, i, 1, 1);
			}
		}
	}
	void edge_eth()
	{
		for (unsigned i = 0; i < kIf; i++) {
			Lane &l = lane[i];
			if (!l.gmii.empty() && l.gmii.front() >= 0) {
				put(t.gmii_tvalid_i, i, 1, 1);
				put(t.gmii_tdata_i, 8 * i, 8, uint8_t(l.gmii.front()));
			} else {
				put(t.gmii_tvalid_i, i, 1, 0);
			}
			if (!l.gmii.empty())
				l.gmii.pop_front();
		}
		t.eth_clk_i = 1;
		t.eval();
		t.eth_clk_i = 0;
		t.eval();
	}
	// one frame of the firmware onto interface i's GMII stream: preamble, delimiter, octets, FCS, inter-frame gap
	void launch(unsigned i, const Bytes &f)
	{
		Lane &l = lane[i];
		// octet 0 is presented on the (queued + 8)th eth edge from the next one: the observer's reference octet
		long double sof = (long double)next_eth / kPs + 8.0L * (l.gmii.size() + 8);
		for (int k = 0; k < 7; k++)
			l.gmii.push_back(0x55);
		l.gmii.push_back(0xD5);
		for (uint8_t b : f)
			l.gmii.push_back(b);
		for (size_t pad = f.size(); pad < 60; pad++)
			l.gmii.push_back(0);
		for (int k = 0; k < 4; k++)
			l.gmii.push_back(0xA5);
		for (int k = 0; k < 12; k++)
			l.gmii.push_back(-1);
		l.to_peer.push_back({sof + kLinkNs, f});
		eth_until_ps = now_ps + uint64_t(8000.0L * (l.gmii.size() + 64));
	}
	bool gmii_busy() const
	{
		for (const Lane &l : lane)
			if (!l.gmii.empty())
				return true;
		return false;
	}

	void run_until(long double t_end_ns)
	{
		while (ns() < t_end_ns) {
			uint64_t nxt = next_dp;
			// the eth clock runs through each frame and its crossings, and for the first 200 us (the seal)
			bool eth = now_ps < eth_until_ps || gmii_busy() || now_ps < 200000000ull;
			if (eth && next_eth < nxt)
				nxt = next_eth;
			now_ps = nxt;
			if (now_ps == next_dp) {
				for (unsigned i = 0; i < kIf; i++)
					peer_tick(i);   // each peer acts at its own instants, on the bench's clock
				edge_dp();
				next_dp += 20 * kPs;
			}
			if (eth && now_ps == next_eth) {
				edge_eth();
				next_eth += 8 * kPs;
			} else if (!eth) {
				next_eth = now_ps - (now_ps % (8 * kPs)) + 8 * kPs;
			}
			service();
		}
	}

	// the firmware's loop, every 50 us; NOW_MS every millisecond
	uint64_t next_service_ps = 0;
	uint64_t next_ms_ps = 0;
	void service()
	{
		if (link_at_ps && now_ps >= link_at_ps) {
			link_at_ps = 0;
			for (unsigned i = 0; i < kIf; i++)
				mbx_model_set_link(&model, i, true);
		}
		if (now_ps >= next_ms_ps) {
			next_ms_ps += 1000000000ull;
			mbx_model_advance_ms(&model, 1);
			ms++;
		}
		if (now_ps < next_service_ps)
			return;
		next_service_ps = now_ps + 50000000ull;
		for (int k = 0; k < 16; k++) {
			const unsigned work = ctrl_loop_service(&loop);
			// each callback publishes the port it ran (gptp_mbx.c), so no pass leaves a change of a port that
			// has published for a later one; a port's first state waits for the first centisecond
			for (unsigned i = 0; i < kIf; i++)
				late += gptp_port_pub_dirty(&g.port[i]) && gptp_mbx_snapshot(&g, i) != nullptr ? 1u : 0u;
			if (work == 0)
				break;
		}
		// the firmware's frames, from the mailbox's transmit merge to each interface's wire
		while (tx_seen < model.tx_sent) {
			const struct mbx_model_tx *tx = mbx_model_tx_frame(&model, tx_seen++);
			if (tx->interface < kIf)
				launch(tx->interface, Bytes(tx->bytes, tx->bytes + tx->len));
		}
	}

	// ---- each peer's behaviour -------------------------------------------------------------------------------
	// a peer's link: its frames leave one after another at 1 Gb/s (8 ns an octet, preamble and gap included), and
	// each event message carries its real departure (a grandmaster's egress stamp)
	long double peer_depart(unsigned i, long double want_ns, size_t len)
	{
		Lane &l = lane[i];
		long double d = want_ns > l.peer_free_ns ? want_ns : l.peer_free_ns;
		l.peer_free_ns = d + 8.0L * (len + 8 + 4 + 12);
		return d;
	}
	// a peer's frames reach its tap in arrival order, whatever order they were sent in
	void send_peer(unsigned i, long double depart_ns, Bytes f)
	{
		Pending p{depart_ns + kLinkNs, std::move(f)};
		auto &q = lane[i].to_dut;
		auto at = q.end();
		while (at != q.begin() && std::prev(at)->t_ns > p.t_ns)
			--at;
		q.insert(at, std::move(p));
	}
	void peer_tick(unsigned i)
	{
		Lane &l = lane[i];
		Peer &peer = l.peer;
		const long double t = ns();
		// frames of the firmware arriving at the peer
		while (!l.to_peer.empty() && l.to_peer.front().t_ns <= t) {
			Pending p = l.to_peer.front();
			l.to_peer.pop_front();
			if (l.peer_on)
				peer_rx(i, p.t_ns, p.f);
		}
		if (!l.peer_on)
			return;
		if (t >= peer.next_preq) {
			peer.next_preq += 1e9L;
			peer.req_seq = ++peer.preq_seq;
			long double d = peer_depart(i, t, 68);
			peer.t1 = peer.at(d);
			peer.have_resp = false;
			send_peer(i, d, peer.msg(0x2, 54, peer.req_seq, 5, 0));
		}
		if (l.flood && t >= l.next_flood) {
			// a burst of Pdelay_Req back to back, past the gptp channel's admission (burst 16)
			l.next_flood += 200e6L;
			for (unsigned k = 0; k < 32; k++)
				send_peer(i, peer_depart(i, t, 68), peer.msg(0x2, 54, l.flood_seq++, 5, 0));
		}
		if (t >= peer.next_ann) {
			peer.next_ann += 1e9L;
			Bytes a = peer.msg(0xB, 76, ++peer.ann_seq, 5, 0);
			a[48 + 13] = peer.gm ? 100 : 250;
			a[48 + 14] = 248;
			a[48 + 15] = 0x22;
			be(a, 48 + 16, 0x436A, 2);
			a[48 + 18] = 248;
			be(a, 48 + 19, peer.clock_id, 8);
			a[48 + 29] = 0xA0;
			be(a, 78, 0x0008, 2);
			be(a, 80, 8, 2);
			be(a, 82, peer.clock_id, 8);
			send_peer(i, peer_depart(i, t, a.size()), a);
		}
		if (peer.gm && t >= peer.next_sync) {
			peer.next_sync += 125e6L;
			Bytes s = peer.msg(0x0, 44, ++peer.sync_seq, 0, -3);
			s[20] = 0x02;
			long double d = peer_depart(i, t, 60);
			const uint64_t origin = uint64_t(peer.at(d));   // the two-step Sync's egress stamp
			send_peer(i, d, s);
			Bytes fu = peer.msg(0x8, 76, peer.sync_seq, 2, -3);
			ts10(fu, 48, origin);
			be(fu, 58, 0x0003, 2);
			be(fu, 60, 28, 2);
			fu[62] = 0x00;
			fu[63] = 0x80;
			fu[64] = 0xC2;
			fu[67] = 1;
			send_peer(i, peer_depart(i, t + 100000.0L, fu.size()), fu);
		}
	}
	void peer_rx(unsigned i, long double t_arr, const Bytes &f)
	{
		Peer &peer = lane[i].peer;
		if (f.size() < 48 || rd(f, 12, 2) != 0x88F7)
			return;
		unsigned type = f[14] & 0xF;
		uint16_t seq = uint16_t(rd(f, 44, 2));
		long double c_arr = peer.at(t_arr);
		if (type == 0x2) {   // the firmware's Pdelay_Req: answer as a responder, 20 us of turnaround
			Bytes r = peer.msg(0x3, 54, seq, 5, 0x7F);
			r[20] = 0x02;
			ts10(r, 48, uint64_t(c_arr));
			std::copy(f.begin() + 34, f.begin() + 44, r.begin() + 58);
			long double depart = peer_depart(i, t_arr + 20000.0L, 68);
			send_peer(i, depart, r);
			Bytes fu = peer.msg(0xA, 54, seq, 5, 0x7F);
			ts10(fu, 48, uint64_t(peer.at(depart)));
			std::copy(f.begin() + 34, f.begin() + 44, fu.begin() + 58);
			send_peer(i, peer_depart(i, depart + 50000.0L, 68), fu);
		} else if (type == 0x3 && seq == kCutSeq) {
			peer.cut_answers++;
		} else if (type == 0x3 && seq == peer.req_seq) {
			peer.t4 = c_arr;
			peer.t2 = (long double)ts10_get(f, 48);
			peer.have_resp = true;
		} else if (type == 0xA && seq == peer.req_seq && peer.have_resp) {
			peer.t3 = (long double)ts10_get(f, 48);
			peer.delays.push_back(double(((peer.t4 - peer.t1) - (peer.t3 - peer.t2)) / 2));
		} else if (type == 0x0 && !peer.gm) {
			peer.sync_wait = true;
			peer.sync_wait_seq = seq;
			peer.sync_rx = c_arr;
		} else if (type == 0x8 && !peer.gm && peer.sync_wait && seq == peer.sync_wait_seq) {
			peer.sync_wait = false;
			long double pd = peer.delays.empty() ? 0 : peer.delays.back();
			long double offset = peer.sync_rx - ((long double)ts10_get(f, 48) + pd);   // the slave's offset
			peer.slave_offsets.push_back(double(offset));
			// the peer's own servo (independent of the firmware's): a step over 20 us, else a PI on its rate,
			// both gains per 125 ms pair: half the offset, a tenth into the integral
			peer.rebase(t_arr);
			if (std::fabs(double(offset)) > 20000.0) {
				peer.base_ns -= offset;
			} else {
				peer.integ += 0.1L * offset / 125e6L;
				peer.trim = -(0.5L * offset / 125e6L) - peer.integ;
			}
		}
	}

	// interface i's peer: a grandmaster or a slave, its clock's rate and its phase at t = 0
	void peer(unsigned i, bool gm, long double ppm, long double base_ns, uint64_t clock_id)
	{
		Lane &l = lane[i];
		l.peer = Peer{};
		l.peer.gm = gm;
		l.peer.ppm = ppm;
		l.peer.base_ns = base_ns;
		l.peer.clock_id = clock_id;
		l.peer_on = true;
	}
	void start()
	{
		t.dp_rst_n = 0;
		t.eth_rst_n = 0;
		for (int k = 0; k < 8; k++) {
			t.dp_clk_i = 1;
			t.eth_clk_i = 1;
			t.eval();
			t.dp_clk_i = 0;
			t.eth_clk_i = 0;
			t.eval();
		}
		t.dp_rst_n = 1;
		t.eth_rst_n = 1;
		mbx_model_reset(&model);
		mbx_model_bind(&model, nullptr, nullptr);
		ctrl_loop_init(&loop);
		struct gptp_config cfg[kIf] = {};
		std::array<uint64_t, kIf> macs{};
		for (unsigned i = 0; i < kIf; i++) {
			macs[i] = 0x001B92000001ull + i;
			cfg[i].clock_id = 0x001B92FFFE000001ull + i;
			for (unsigned b = 0; b < 6; b++)
				cfg[i].mac[b] = uint8_t(macs[i] >> (8 * (5 - b)));
			cfg[i].priority1 = 248;
			cfg[i].priority2 = 248;
			cfg[i].phc_clk_hz = 50000000u;
		}
		struct gptp_mbx_phc phc = {this, adjfine, step};
		struct gptp_mbx_aecp aecp = {this, changed};
		if (!gptp_mbx_attach(&g, &loop, cfg, &phc) || !ctrl_loop_open(&loop, 0x001B92FFFE000001ull, macs.data()))
			std::printf("  [FAIL] the firmware did not open\n");
		gptp_mbx_notify(&g, &aecp);
		link_at_ps = 1000000000ull;   // the links come up 1 ms after reset, the timestamp units sealed by then
	}
	uint64_t link_at_ps = 0;
	// interface i's PHC against its peer's clock now, ns: positive when the PHC is ahead
	double offset_now(unsigned i) { return double((long double)phc(i) - lane[i].peer.at(ns())); }
};

// a run's trace: (s, offset ns) of interface i, and its lock time (the last sample past 100 ns) and worst after it
struct Lock {
	double lock = 0;
	double worst = 0;
};
Lock lock_of(const std::vector<std::pair<double, double>> &trace)
{
	Lock r;
	for (auto &p : trace)
		if (std::fabs(p.second) > 100.0)
			r.lock = p.first;
	for (auto &p : trace)
		if (p.first > r.lock)
			r.worst = std::fmax(r.worst, std::fabs(p.second));
	return r;
}

// a field of a published word, by the contract's place
uint32_t field(uint32_t w, unsigned lsb, unsigned width)
{
	return (w >> lsb) & (width >= 32u ? ~0u : (1u << width) - 1u);
}

// interface i's published words as its datapath holds them: the GPTP_* words of the last GEN that moved
void published(const struct mbx_model &m, unsigned i, uint32_t w[MBX_PUB_GPTP_WORDS])
{
	struct mbx_model_pub v;
	mbx_model_pub_view(&m, i, &v);
	std::memcpy(w, v.gptp, sizeof v.gptp);
}

void run_slave()
{
	Bench b;
	const uint64_t gm[kIf] = {0x02AABBFFFE000001ull, 0x02AACCFFFE000002ull};
	b.peer(0, true, 40.0L, 1'000'000'000'000.0L, gm[0]);
	b.peer(1, true, -25.0L, 500'000'000'000.0L, gm[1]);
	b.start();
	std::vector<std::pair<double, double>> trace[kIf];
	for (int k = 1; k <= 100; k++) {
		b.run_until(k * 100e6L);   // every 100 ms
		for (unsigned i = 0; i < kIf; i++)
			trace[i].push_back({k * 0.1, b.offset_now(i)});
	}
	// interface 1's peer sends a Pdelay_Req cut short by its last eight octets: with the trailer its record is as
	// long as a whole one's, so only the adapter's taking the trailer off refuses it (IEEE 802.1AS-2020 11.4.5)
	const uint32_t bad0 = b.g.port[1].ctr.rx_bad;
	Bytes cut = b.lane[1].peer.msg(0x2, 54, kCutSeq, 5, 0);
	cut.resize(cut.size() - 8u);
	b.send_peer(1, b.peer_depart(1, b.ns(), cut.size()), cut);
	b.run_until(10.05e9L);
	check(b.g.port[1].ctr.rx_bad == bad0 + 1u && b.lane[1].peer.cut_answers == 0,
	      "SLAVE if1 a Pdelay_Req cut short by its last eight octets is refused, not answered",
	      double(b.g.port[1].ctr.rx_bad - bad0), 1);
	for (unsigned i = 0; i < kIf; i++) {
		const Lock l = lock_of(trace[i]);
		const struct gptp_port &p = b.g.port[i];
		const std::string at = "SLAVE if" + std::to_string(i) + " ";
		std::printf("[ SLAVE if%u ] role %d, asCapable %d, GM %016llx, steps %u, lock (PHC within 100 ns of its GM) "
			    "%.1f s, then worst |offset| %.1f ns; pdelay %d ns\n", i, int(gptp_port_role(&p)), int(p.pub.as_capable),
			    static_cast<unsigned long long>(p.pub.gm_id), p.ctr.steps, l.lock, l.worst, p.pub.pdelay_ns);
		for (size_t s = 0; s < trace[i].size(); s += 20)
			std::printf("    t=%4.1f s  PHC%u - GM%u = %14.1f ns\n", trace[i][s].first, i, i, trace[i][s].second);
		check(gptp_port_role(&p) == GPTP_ROLE_SLAVE, at + "the port is its grandmaster's slave");
		check(p.pub.gm_id == gm[i], at + "the published grandmaster is its own peer, not the other interface's");
		check(l.lock <= 8.0, at + "the PHC is within 100 ns of its grandmaster by 8 s", l.lock, 8.0);
		check(l.worst < 100.0, at + "and stays within 100 ns (NFR-TIME-01: 1 us)", l.worst, 100.0);
		check(std::abs(p.pub.pdelay_ns - kLinkNs) <= 25, at + "the measured link delay is its link's", p.pub.pdelay_ns,
		      double(kLinkNs));
		check(p.ctr.steps == 1, at + "one step, then slew", p.ctr.steps, 1);
		double pd = b.lane[i].peer.delays.empty() ? -1e9 : b.lane[i].peer.delays.back();
		check(std::fabs(pd - kLinkNs) <= 25.0, at + "the peer measures the link through the firmware's answers", pd,
		      double(kLinkNs));
		check(b.g.rx_unstamped == 0, at + "every event message reached its port with its stamp", b.g.rx_unstamped, 0);
		// ---- the published snapshot (#884's ruling item 7)
		const struct gptp_pub *s = gptp_mbx_snapshot(&b.g, i);
		check(s != nullptr && s->gm_id == gm[i], at + "the snapshot holds the grandmaster it published");
		if (s == nullptr)
			continue;
		// decoded by the contract's places, not by the firmware's encoder
		uint32_t have[MBX_PUB_GPTP_WORDS];
		published(b.model, i, have);
		const uint32_t st = have[2];
		const uint64_t pgm = uint64_t(have[1]) << 32 | have[0];
		check(pgm == s->gm_id && field(st, MBX_GPTP_STATE_DOMAIN_LSB, MBX_GPTP_STATE_DOMAIN_WIDTH) == s->domain &&
		      field(st, MBX_GPTP_STATE_AS_CAPABLE_LSB, MBX_GPTP_STATE_AS_CAPABLE_WIDTH) == (s->as_capable ? 1u : 0u) &&
		      field(st, MBX_GPTP_STATE_SYNC_OK_LSB, MBX_GPTP_STATE_SYNC_OK_WIDTH) == (s->sync_ok ? 1u : 0u) &&
		      field(st, MBX_GPTP_STATE_SLEW_LSB, MBX_GPTP_STATE_SLEW_WIDTH) == (s->slew ? 1u : 0u) &&
		      field(st, MBX_GPTP_STATE_DISC_LSB, MBX_GPTP_STATE_DISC_WIDTH) == s->disc &&
		      field(st, MBX_GPTP_STATE_GEN_LSB, MBX_GPTP_STATE_GEN_WIDTH) == b.g.gen[i],
		      at + "the words the datapath takes are the snapshot's, its GEN last", double(have[0]),
		      double(uint32_t(s->gm_id)));
		uint64_t agm = 0;
		uint32_t apd = 0;
		uint8_t adom = 0;
		bool acap = false;
		gptp_mbx_avb(&b.g, i, &agm, &apd, &adom, &acap);
		check(agm == s->gm_id && apd == uint32_t(s->pdelay_ns) && adom == s->domain && acap == s->as_capable,
		      at + "GET_AVB_INFO's gPTP fields are the snapshot's", double(apd), double(s->pdelay_ns));
		uint64_t path[GPTP_PATH_MAX] = {};
		size_t n = 0;
		const bool ok = gptp_mbx_path(&b.g, i, path, GPTP_PATH_MAX, &n);
		check(ok && n == s->path_count && n >= 1 && path[0] == gm[i], at + "GET_AS_PATH is the snapshot's path, its "
		      "grandmaster first", double(n), double(s->path_count));
		check(b.lane[i].notices[1] >= 1 && b.lane[i].notices[2] >= 1,
		      at + "the AVB_INFO and AS_PATH changes were raised to the AECP owner", b.lane[i].notices[1], 1);
	}
	// no bridge between the two end stations (Milan v1.2 8.3.4): each PHC follows its own grandmaster
	const double apart = double((long double)b.phc(1) - (long double)b.phc(0));
	const double gms = double(b.lane[1].peer.at(b.ns()) - b.lane[0].peer.at(b.ns()));
	check(std::fabs(apart - gms) < 200.0, "SLAVE the two PHCs stand apart as their grandmasters do (8.3.4: no bridge)",
	      apart / 1e9, gms / 1e9);
	// interface 1's grandmaster falls silent: its announce receipt timeout (IEEE 802.1AS-2020 10.7.3.2) is a tick's
	// work, with no frame of the peer's to follow it, and the port's new grandmaster must still be published
	b.lane[1].peer_on = false;
	b.run_until(14.5e9L);
	uint32_t w[MBX_PUB_GPTP_WORDS];
	published(b.model, 1, w);
	const uint64_t now_gm = uint64_t(w[1]) << 32 | w[0];
	check(now_gm != gm[1] && now_gm == b.g.port[1].pub.gm_id,
	      "SLAVE if1 its grandmaster silent, the port's next grandmaster is published",
	      double(now_gm & 0xFFFFu), double(b.g.port[1].pub.gm_id & 0xFFFFu));
	check(b.late == 0, "SLAVE the publication follows every port change in the pass that made it", b.late, 0);
}

void run_master()
{
	Bench b;
	b.peer(0, false, -60.0L, 5'000'000.0L, 0x02AABBFFFE000001ull);
	b.peer(1, false, 35.0L, 9'000'000.0L, 0x02AACCFFFE000002ull);
	b.start();
	std::vector<std::pair<double, double>> trace[kIf];
	for (int k = 1; k <= 100; k++) {
		b.run_until(k * 100e6L);
		for (unsigned i = 0; i < kIf; i++)
			trace[i].push_back({k * 0.1, b.offset_now(i)});
	}
	for (unsigned i = 0; i < kIf; i++) {
		const Lock l = lock_of(trace[i]);
		const struct gptp_port &p = b.g.port[i];
		const Peer &peer = b.lane[i].peer;
		const std::string at = "MASTER if" + std::to_string(i) + " ";
		std::printf("[ MASTER if%u ] role %d, asCapable %d, GM %016llx, peer slave pairs %zu, lock (peer within 100 ns "
			    "of the PHC) %.1f s, then worst |offset| %.1f ns; peer's link delay %.1f ns\n", i,
			    int(gptp_port_role(&p)), int(p.pub.as_capable), static_cast<unsigned long long>(p.pub.gm_id),
			    peer.slave_offsets.size(), l.lock, l.worst, peer.delays.empty() ? -1.0 : peer.delays.back());
		for (size_t s = 0; s < trace[i].size(); s += 20)
			std::printf("    t=%4.1f s  PHC%u - peer%u = %14.1f ns\n", trace[i][s].first, i, i, trace[i][s].second);
		check(gptp_port_role(&p) == GPTP_ROLE_MASTER, at + "the port is grandmaster");
		check(p.pub.sync_ok, at + "and publishes the synchronization verdict");
		check(peer.slave_offsets.size() > 50, at + "the peer took the firmware's Sync and Follow_Up pairs",
		      double(peer.slave_offsets.size()), 50);
		check(l.lock <= 8.0, at + "the peer's clock is within 100 ns of its PHC by 8 s", l.lock, 8.0);
		check(l.worst < 100.0, at + "and stays within 100 ns", l.worst, 100.0);
		double pd = peer.delays.empty() ? -1e9 : peer.delays.back();
		check(std::fabs(pd - kLinkNs) <= 25.0, at + "the peer measures the link through the firmware's answers", pd,
		      double(kLinkNs));
	}
	check(b.late == 0, "MASTER the publication follows every port change in the pass that made it", b.late, 0);
}

void run_flood()
{
	Bench b;
	b.peer(0, true, 40.0L, 1'000'000'000'000.0L, 0x02AABBFFFE000001ull);
	b.lane[0].flood = true;
	b.lane[0].next_flood = 2.5e9L;   // after the lock is taken
	b.start();
	std::vector<std::pair<double, double>> trace;
	for (int k = 1; k <= 80; k++) {
		b.run_until(k * 100e6L);
		trace.push_back({k * 0.1, b.offset_now(0)});
	}
	const Lock l = lock_of(trace);
	const Lane &ln = b.lane[0];
	std::printf("[ FLOOD ] 32 Pdelay_Req every 200 ms from 2.5 s: event messages handed out %zu, committed at once %u, "
		    "refused or held frames %u, received stamped %u, unstamped %u, egress records lost %u; lock %.1f s, "
		    "then worst |offset| %.1f ns\n", ln.handed.size(), ln.admitted_event, ln.refused, b.g.rx_stamped,
		    b.g.rx_unstamped,
		    unsigned(get(b.t.ts_drop_o, 0, 16)), l.lock, l.worst);
	// mbx_model_rx's false is a refusal or a hold (#917), the held frame committed at the next refill, so the
	// firmware's own tally is the delivered count: every event message it received carried its stamp, and it
	// received no more than the tap handed out, the channel's refusals the rest
	unsigned handed = 0;
	for (const auto &f : ln.handed)
		handed += f;
	check(ln.refused > 0, "FLOOD the gptp channel refused or held the bursts' excess (its admission, burst 16)",
	      ln.refused, 1);
	check(b.g.rx_unstamped == 0 && b.g.rx_stamped > 0 && b.g.rx_stamped <= handed,
	      "FLOOD every event message the channel delivered reached the firmware with its own stamp",
	      double(b.g.rx_unstamped), 0);
	check(get(b.t.ts_drop_o, 0, 16) == 0, "FLOOD the answers' egress stamps all fit the unit's FIFO",
	      double(get(b.t.ts_drop_o, 0, 16)), 0);
	check(l.lock <= 8.0 && l.worst < 100.0, "FLOOD the port keeps its lock through the flood", l.worst, 100.0);
	check(b.late == 0, "FLOOD the publication follows every port change in the pass that made it", b.late, 0);
}

}  // namespace

int main(int argc, char **argv)
{
	Verilated::commandArgs(argc, argv);
	std::string only = argc > 1 && argv[1][0] != '+' ? argv[1] : "";
	if (only.empty() || only == "slave")
		run_slave();
	if (only.empty() || only == "master")
		run_master();
	if (only.empty() || only == "flood")
		run_flood();
	std::printf("== gptp in firmware, closed loop over the mailbox model and the timestamp units: checks: %d   "
		    "failures: %d ==\n", checks, failures);
	std::printf("RESULT: %s\n", failures ? "FAIL" : "PASS");
	return failures ? 1 : 0;
}

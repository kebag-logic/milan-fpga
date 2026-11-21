// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// sim_main.cpp - gPTP in firmware locks to a modelled peer over the mailbox and the timestamp unit (#884, #665 F6).
//
// THE FIRMWARE is the split image's gPTP: the end station port and its adapter (sw/firmware/ctrl/gptp), the loop
// and the mailbox driver, on the host mailbox model (contract 2.5: the gptp channel, the TIMESTAMP event, the gPTP
// publication). THE FABRIC is tb_gptp_sw.sv: the PHC (timestamp_counter) the firmware's servo steers, the launch
// observer on the MAC's transmit stream and the timestamp unit. THE PEER is this file's own model, written apart
// from the firmware: an ideal clock of its own rate and phase, a 300 ns link, and Milan v1.2 Table 4.1's intervals.
//
// Two runs. `slave`: the peer is the grandmaster (priority1 100), 1000 s ahead of the PHC and 40 ppm fast; the
// firmware must step once and lock its PHC to the peer's clock. `master`: the peer is a slave (priority1 250) with a
// servo of its own; the firmware is grandmaster and the peer must lock to the PHC through the firmware's Sync,
// Follow_Up and Pdelay answers. Every offset is read from outside both: the PHC's own counter against the peer's
// model clock at the same instant of the bench's time.
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
constexpr int64_t kLinkNs = 300;      // the link's one-way delay

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

struct Pending { long double t_ns; Bytes f; };   // a frame the peer sends, arriving at t_ns of the bench

struct Bench {
	Vtb_gptp_sw t;
	uint64_t now_ps = 0;
	uint64_t next_dp = 0;   // the next rising edge of each clock
	uint64_t next_eth = 0;
	bool eth_on = false;
	uint64_t eth_until_ps = 0;
	// firmware
	struct mbx_model model {};
	struct ctrl_loop loop {};
	struct gptp_mbx g {};
	unsigned tx_seen = 0;
	// fabric drive
	std::deque<int> gmii;                  // octets on the MAC's transmit stream; -1: no octet (the gap)
	std::deque<long double> gmii_sof;      // the bench time each frame's octet 0 leaves, ns
	Bytes rx_frame;
	size_t rx_at = 0;
	bool rx_busy = false;
	std::deque<Pending> to_dut;            // the peer's frames, by arrival
	std::deque<Pending> to_peer;           // the firmware's frames, by arrival at the peer
	int adjust_hold = 0;
	Peer peer;
	unsigned ms = 0;

	long double ns() const { return (long double)now_ps / kPs; }

	// ---- the PHC HAL: the CSR's PTP block, as the firmware's servo drives it (REQ-PTP-02, 03)
	static void adjfine(void *ctx, unsigned, int32_t addend) { static_cast<Bench *>(ctx)->t.phc_adj_i = uint32_t(addend); }
	static void step(void *ctx, unsigned, int64_t delta)
	{
		Bench *b = static_cast<Bench *>(ctx);
		b->t.phc_offset_i = uint64_t(delta);
		b->adjust_hold = 1;
	}

	void edge_dp()
	{
		// the receive tap: one beat of eight octets a clock while a frame is being taken
		if (!rx_busy && !to_dut.empty() && to_dut.front().t_ns <= ns()) {
			rx_frame = to_dut.front().f;
			if (std::getenv("GPTP_SW_DEBUG") && rx_frame.size() > 45)
				std::printf("    TAP type %x seq %u due %.1f at %.1f ns, PHC %llu\n", rx_frame[14] & 0xF,
					    unsigned(rd(rx_frame, 44, 2)), double(to_dut.front().t_ns), double(ns()),
					    static_cast<unsigned long long>(t.phc_ns_o));
			to_dut.pop_front();
			rx_at = 0;
			rx_busy = true;
		}
		if (rx_busy) {
			uint64_t d = 0;
			unsigned keep = 0;
			for (unsigned l = 0; l < 8 && rx_at + l < rx_frame.size(); l++) {
				d |= uint64_t(rx_frame[rx_at + l]) << (8 * l);
				keep |= 1u << l;
			}
			t.rx_tdata_i = d;
			t.rx_tkeep_i = keep;
			t.rx_tvalid_i = 1;
			t.rx_tlast_i = rx_at + 8 >= rx_frame.size();
		} else {
			t.rx_tvalid_i = 0;
			t.rx_tlast_i = 0;
		}
		t.phc_adjust_i = adjust_hold > 0;
		t.dp_clk_i = 1;
		t.eval();
		t.dp_clk_i = 0;
		t.eval();
		if (adjust_hold > 0)
			adjust_hold--;
		if (rx_busy) {
			rx_at += 8;
			if (rx_at >= rx_frame.size()) {
				rx_busy = false;
				// the frame reaches the mailbox's gptp ring after the tap has stamped it
				mbx_model_rx(&model, rx_frame.data(), rx_frame.size(), 0);
			}
		}
		// the record FIFO, drained into the mailbox's TIMESTAMP events
		t.ts_take_i = 0;
		if (t.ts_valid_o) {
			const uint32_t hi = t.ts_data_o[2];
			uint64_t ns_v = (uint64_t(t.ts_data_o[1]) << 32) | t.ts_data_o[0];
			mbx_model_timestamp(&model, 0, (hi >> 21) & 1u, (hi >> 20) & 1u, uint8_t((hi >> 16) & 0xFu),
					    uint16_t(hi & 0xFFFFu), ns_v);
			if (std::getenv("GPTP_SW_DEBUG"))
				std::printf("    STAMP %s ok %u type %x seq %u ns %llu at %.1f\n", ((hi >> 21) & 1u) ? "egress" : "ingress",
					    (hi >> 20) & 1u, (hi >> 16) & 0xFu, hi & 0xFFFFu, static_cast<unsigned long long>(ns_v), double(ns()));
			t.ts_take_i = 1;
		}
	}
	void edge_eth()
	{
		if (!gmii.empty() && gmii.front() >= 0) {
			t.gmii_tvalid_i = 1;
			t.gmii_tdata_i = uint8_t(gmii.front());
		} else {
			t.gmii_tvalid_i = 0;
		}
		if (!gmii.empty())
			gmii.pop_front();
		t.eth_clk_i = 1;
		t.eval();
		t.eth_clk_i = 0;
		t.eval();
	}
	// one frame of the firmware onto the GMII stream: preamble, delimiter, octets, FCS, inter-frame gap
	void launch(const Bytes &f)
	{
		// octet 0 is presented on the (queued + 8)th eth edge from the next one: the observer's reference octet
		long double sof = (long double)next_eth / kPs + 8.0L * (gmii.size() + 8);
		for (int i = 0; i < 7; i++)
			gmii.push_back(0x55);
		gmii.push_back(0xD5);
		for (uint8_t b : f)
			gmii.push_back(b);
		for (size_t pad = f.size(); pad < 60; pad++)
			gmii.push_back(0);
		for (int i = 0; i < 4; i++)
			gmii.push_back(0xA5);
		for (int i = 0; i < 12; i++)
			gmii.push_back(-1);
		to_peer.push_back({sof + kLinkNs, f});
		if (std::getenv("GPTP_SW_DEBUG") && f.size() > 45)
			std::printf("    LAUNCH type %x seq %u at %.1f ns (octet 0 at %.1f)\n", f[14] & 0xF, unsigned(rd(f, 44, 2)),
				    double(ns()), double(sof));
		eth_until_ps = now_ps + uint64_t(8000.0L * (gmii.size() + 64));
	}

	void run_until(long double t_end_ns)
	{
		while (ns() < t_end_ns) {
			uint64_t nxt = next_dp;
			// the eth clock runs through each frame and its crossings, and for the first 200 us (the seal)
			bool eth = eth_on || now_ps < eth_until_ps || !gmii.empty() || now_ps < 200000000ull;
			if (eth && next_eth < nxt)
				nxt = next_eth;
			now_ps = nxt;
			if (now_ps == next_dp) {
				peer_tick();   // the peer acts at its own instants, on the bench's clock
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
	unsigned dbg_used = 0;
	void service()
	{
		if (link_at_ps && now_ps >= link_at_ps) {
			link_at_ps = 0;
			mbx_model_set_link(&model, 0, true);
		}
		if (now_ps >= next_ms_ps) {
			next_ms_ps += 1000000000ull;
			mbx_model_advance_ms(&model, 1);
			ms++;
		}
		if (now_ps < next_service_ps)
			return;
		next_service_ps = now_ps + 50000000ull;
		for (int k = 0; k < 16 && ctrl_loop_service(&loop) != 0; k++) {
		}
		// the firmware's frames, from the mailbox's transmit merge to the wire
		if (std::getenv("GPTP_SW_DEBUG") && g.port[0].ctr.sync_used != dbg_used) {
			dbg_used = g.port[0].ctr.sync_used;
			std::printf("    PAIR %u at %.3f s: offset %d trim %d true %.1f\n", dbg_used, double(ns() / 1e9L),
				    g.port[0].pub.offset_ns, g.port[0].srv.trim, offset_now());
		}
		while (tx_seen < model.tx_sent) {
			const struct mbx_model_tx *tx = mbx_model_tx_frame(&model, tx_seen++);
			launch(Bytes(tx->bytes, tx->bytes + tx->len));
		}
	}

	// ---- the peer's behaviour --------------------------------------------------------------------------------
	// the peer's link: its frames leave one after another at 1 Gb/s (8 ns an octet, preamble and gap
	// included), and each event message carries its real departure (a grandmaster's egress stamp)
	long double peer_free_ns = 0;
	long double peer_depart(long double want_ns, size_t len)
	{
		long double d = want_ns > peer_free_ns ? want_ns : peer_free_ns;
		peer_free_ns = d + 8.0L * (len + 8 + 4 + 12);
		return d;
	}
	// the peer's frames reach the tap in arrival order, whatever order they were sent in
	void send_peer(long double depart_ns, Bytes f)
	{
		Pending p{depart_ns + kLinkNs, std::move(f)};
		auto at = to_dut.end();
		while (at != to_dut.begin() && std::prev(at)->t_ns > p.t_ns)
			--at;
		to_dut.insert(at, std::move(p));
	}
	void peer_tick()
	{
		const long double t = ns();
		// frames of the firmware arriving at the peer
		while (!to_peer.empty() && to_peer.front().t_ns <= t) {
			Pending p = to_peer.front();
			to_peer.pop_front();
			peer_rx(p.t_ns, p.f);
		}
		if (t >= peer.next_preq) {
			peer.next_preq += 1e9L;
			peer.req_seq = ++peer.preq_seq;
			long double d = peer_depart(t, 68);
			peer.t1 = peer.at(d);
			peer.have_resp = false;
			send_peer(d, peer.msg(0x2, 54, peer.req_seq, 5, 0));
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
			send_peer(peer_depart(t, a.size()), a);
		}
		if (peer.gm && t >= peer.next_sync) {
			peer.next_sync += 125e6L;
			Bytes s = peer.msg(0x0, 44, ++peer.sync_seq, 0, -3);
			s[20] = 0x02;
			long double d = peer_depart(t, 60);
			const uint64_t origin = uint64_t(peer.at(d));   // the two-step Sync's egress stamp
			send_peer(d, s);
			Bytes fu = peer.msg(0x8, 76, peer.sync_seq, 2, -3);
			ts10(fu, 48, origin);
			be(fu, 58, 0x0003, 2);
			be(fu, 60, 28, 2);
			fu[62] = 0x00;
			fu[63] = 0x80;
			fu[64] = 0xC2;
			fu[67] = 1;
			send_peer(peer_depart(t + 100000.0L, fu.size()), fu);
		}
	}
	void peer_rx(long double t_arr, const Bytes &f)
	{
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
			long double depart = peer_depart(t_arr + 20000.0L, 68);
			send_peer(depart, r);
			Bytes fu = peer.msg(0xA, 54, seq, 5, 0x7F);
			ts10(fu, 48, uint64_t(peer.at(depart)));
			std::copy(f.begin() + 34, f.begin() + 44, fu.begin() + 58);
			send_peer(peer_depart(depart + 50000.0L, 68), fu);
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

	void start(bool gm_peer, long double ppm, long double base_ns)
	{
		peer = Peer{};
		peer.gm = gm_peer;
		peer.ppm = ppm;
		peer.base_ns = base_ns;
		t.dp_rst_n = 0;
		t.eth_rst_n = 0;
		for (int i = 0; i < 8; i++) {
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
		struct gptp_config cfg[MBX_N_IF] = {};
		cfg[0].clock_id = 0x001B92FFFE000001ull;
		cfg[0].mac[0] = 0x00;
		cfg[0].mac[1] = 0x1B;
		cfg[0].mac[2] = 0x92;
		cfg[0].mac[5] = 0x01;
		cfg[0].priority1 = 248;
		cfg[0].priority2 = 248;
		cfg[0].phc_clk_hz = 50000000u;
		static const struct gptp_mbx_phc phc = {nullptr, adjfine, step};
		struct gptp_mbx_phc mine = phc;
		mine.ctx = this;
		if (!gptp_mbx_attach(&g, &loop, cfg, &mine) || !ctrl_loop_open(&loop, 0x001B92FFFE000001ull, std::array<uint64_t, MBX_N_IF>{0x001B92000001ull}.data()))
			std::printf("  [FAIL] the firmware did not open\n");
		link_at_ps = 1000000000ull;   // the link comes up 1 ms after reset, the timestamp unit sealed by then
	}
	uint64_t link_at_ps = 0;
	// the PHC against the peer's clock now, ns: positive when the PHC is ahead
	double offset_now() { return double((long double)t.phc_ns_o - peer.at(ns())); }
};

}  // namespace

int main(int argc, char **argv)
{
	Verilated::commandArgs(argc, argv);

	if (std::getenv("GPTP_SW_DEBUG")) {
		Bench b;
		b.start(true, 40.0L, 1'000'000'000'000.0L);
		b.run_until(4.2e9L);
		std::printf("pd t1 %llu t2 %llu t3 %llu t4 %llu delay %d lost %u done %u\n", static_cast<unsigned long long>(b.g.port[0].pd.t1),
			    static_cast<unsigned long long>(b.g.port[0].pd.t2), static_cast<unsigned long long>(b.g.port[0].pd.t3),
			    static_cast<unsigned long long>(b.g.port[0].pd.t4), b.g.port[0].pd.delay_ns, b.g.port[0].ctr.pd_lost,
			    b.g.port[0].ctr.pd_done);
		return 0;
	}
	// ---- run 1: the firmware's port as slave of a modelled grandmaster
	{
		Bench b;
		b.start(true, 40.0L, 1'000'000'000'000.0L);
		std::vector<std::pair<double, double>> trace;   // (s, offset ns)
		std::vector<std::string> own;   // the port's own view, a line a second
		for (int k = 1; k <= 100; k++) {
			b.run_until(k * 100e6L);   // every 100 ms
			trace.push_back({k * 0.1, b.offset_now()});
			if (k % 10 == 1) {
				char line[200];
				std::snprintf(line, sizeof line, "pairs %u steps %u last offset %d ns trim %d fu_lost %u sync_rx %u ts_lost %u",
					      b.g.port[0].ctr.sync_used, b.g.port[0].ctr.steps, b.g.port[0].pub.offset_ns,
					      b.g.port[0].srv.trim, b.g.port[0].ctr.fu_lost, b.g.port[0].ctr.sync_rx,
					      unsigned(b.t.ts_lost_o));
				own.push_back(line);
			}
		}
		double lock = 0;
		for (auto &p : trace)
			if (std::fabs(p.second) > 100.0)
				lock = p.first;
		double worst = 0;
		for (auto &p : trace)
			if (p.first > lock)
				worst = std::fmax(worst, std::fabs(p.second));
		std::printf("[ SLAVE ] role %d, asCapable %d, GM %016llx, steps %u, lock (PHC within 100 ns of the GM) %.1f s, "
			    "then worst |offset| %.1f ns; pdelay %d ns; ts lost %u\n",
			    int(gptp_port_role(&b.g.port[0])), int(b.g.port[0].pub.as_capable),
			    static_cast<unsigned long long>(b.g.port[0].pub.gm_id), b.g.port[0].ctr.steps, lock, worst,
			    b.g.port[0].pub.pdelay_ns, unsigned(b.t.ts_lost_o));
		for (size_t i = 0; i < trace.size(); i += 10)
			std::printf("    t=%4.1f s  PHC - GM = %14.1f ns   (the port: %s)\n", trace[i].first, trace[i].second,
				    own[i / 10].c_str());
		check(gptp_port_role(&b.g.port[0]) == GPTP_ROLE_SLAVE, "SLAVE the port is the grandmaster's slave");
		check(b.g.port[0].pub.gm_id == b.peer.clock_id, "SLAVE the published grandmaster is the peer");
		check(lock <= 8.0, "SLAVE the PHC is within 100 ns of the grandmaster by 8 s", lock, 8.0);
		check(worst < 100.0, "SLAVE and stays within 100 ns (NFR-TIME-01: 1 us)", worst, 100.0);
		check(std::abs(b.g.port[0].pub.pdelay_ns - kLinkNs) <= 25, "SLAVE the measured link delay is the link's",
		      b.g.port[0].pub.pdelay_ns, double(kLinkNs));
		check(b.g.port[0].ctr.steps == 1, "SLAVE one step, then slew", b.g.port[0].ctr.steps, 1);
		double pd = b.peer.delays.empty() ? -1e9 : b.peer.delays.back();
		check(std::fabs(pd - kLinkNs) <= 25.0, "SLAVE the peer measures the link through the firmware's answers", pd,
		      double(kLinkNs));
	}

	// ---- run 2: the firmware's port as grandmaster of a modelled slave
	{
		Bench b;
		b.start(false, -60.0L, 5'000'000.0L);
		std::vector<std::pair<double, double>> trace;
		for (int k = 1; k <= 100; k++) {
			b.run_until(k * 100e6L);
			trace.push_back({k * 0.1, b.offset_now()});
		}
		double lock = 0;
		for (auto &p : trace)
			if (std::fabs(p.second) > 100.0)
				lock = p.first;
		double worst = 0;
		for (auto &p : trace)
			if (p.first > lock)
				worst = std::fmax(worst, std::fabs(p.second));
		std::printf("[ MASTER ] role %d, asCapable %d, GM %016llx, peer slave pairs %zu, lock (peer within 100 ns "
			    "of the PHC) %.1f s, then worst |offset| %.1f ns; peer's link delay %.1f ns\n",
			    int(gptp_port_role(&b.g.port[0])), int(b.g.port[0].pub.as_capable),
			    static_cast<unsigned long long>(b.g.port[0].pub.gm_id), b.peer.slave_offsets.size(), lock, worst,
			    b.peer.delays.empty() ? -1.0 : b.peer.delays.back());
		for (size_t i = 0; i < trace.size(); i += 10)
			std::printf("    t=%4.1f s  PHC - peer = %14.1f ns\n", trace[i].first, trace[i].second);
		check(gptp_port_role(&b.g.port[0]) == GPTP_ROLE_MASTER, "MASTER the port is grandmaster");
		check(b.g.port[0].pub.sync_ok, "MASTER and publishes the synchronization verdict");
		check(b.peer.slave_offsets.size() > 50, "MASTER the peer took the firmware's Sync and Follow_Up pairs",
		      double(b.peer.slave_offsets.size()), 50);
		check(lock <= 8.0, "MASTER the peer's clock is within 100 ns of the PHC by 8 s", lock, 8.0);
		check(worst < 100.0, "MASTER and stays within 100 ns", worst, 100.0);
		double pd = b.peer.delays.empty() ? -1e9 : b.peer.delays.back();
		check(std::fabs(pd - kLinkNs) <= 25.0, "MASTER the peer measures the link through the firmware's answers", pd,
		      double(kLinkNs));
	}

	std::printf("== gptp in firmware, closed loop over the mailbox model and the timestamp unit: checks: %d   "
		    "failures: %d ==\n", checks, failures);
	std::printf("RESULT: %s\n", failures ? "FAIL" : "PASS");
	return failures ? 1 : 0;
}

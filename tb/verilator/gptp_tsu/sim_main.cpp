// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// sim_main.cpp - the timestamp unit (hdl/ieee8021as/gptp_tsu/KL_gptp_tsu.sv,
// #884, #665 F6) and the split tap's gptp trailer it feeds (KL_ctrl_split),
// self-checking. Every expected stamp is computed here from
// the PHC this bench drives and the fabric plane's published corrections
// (docs/design/GPTP_PLANE.md: 426 ns on GMII, 3770 ns on MII, the board's
// ingress and egress constants), never read back from the unit.
//
// Each check prints its own words; the tally is the record.

#include <cstdint>
#include <cstdio>
#include <deque>
#include <vector>

#include "Vtb_gptp_tsu.h"
#include "verilated.h"

namespace {

int checks = 0;
int failures = 0;

void check(bool ok, const char *what, unsigned long long got = 0, unsigned long long exp = 0)
{
	checks++;
	if (!ok) {
		failures++;
		std::printf("  [FAIL] %s got=%llu exp=%llu\n", what, got, exp);
	}
}

struct Rec {
	bool egress;
	bool ok;
	unsigned type;
	unsigned seq;
	uint64_t ns;
};

Rec decode(const VlWide<3> &w)
{
	// {EGRESS, OK, MSG_TYPE, SEQUENCE_ID, STAMP}, STAMP lowest: 86 bits over three words
	uint64_t ns = (uint64_t(w[1]) << 32) | w[0];
	uint32_t hi = w[2];
	return {bool((hi >> 21) & 1), bool((hi >> 20) & 1), (hi >> 16) & 0xF, hi & 0xFFFF, ns};
}

// a frame the control tap handed toward the mailbox: its bytes and its eight-octet trailer
struct Out {
	std::vector<uint8_t> bytes;
	uint64_t trailer;
};

constexpr uint64_t NO_STAMP = ~0ull;

struct Bench {
	Vtb_gptp_tsu t;
	uint64_t phc = 1'000'000'000'000ull;   // the PHC: 20 ns a cycle, the 50 MHz shape
	uint64_t cyc = 0;
	std::deque<Rec> g, m;
	std::deque<Out> out;                   // frames the tap delivered, in order
	std::vector<uint8_t> cur;              // the bytes of the frame being delivered
	bool drain = true;                     // the mailbox side takes a byte a cycle
	uint64_t m_stamp = 0;                  // the MII unit's ingress stamp at the last frame's last beat
	bool m_event = false;

	void tick()
	{
		t.phc_ns_i = phc;
		t.s_rx_ready_i = drain;
		t.clk_i = 0;
		t.eval();
		bool took = drain && t.s_rx_valid_o;
		uint8_t byte = t.s_rx_data_o;
		bool last = t.s_rx_last_o;
		t.clk_i = 1;
		t.eval();
		if (took) {
			cur.push_back(byte);
			if (last) {
				Out o;
				o.trailer = 0;
				size_t n = cur.size() >= 8 ? cur.size() - 8 : 0;
				for (size_t k = n; k < cur.size(); k++)
					o.trailer = (o.trailer << 8) | cur[k];
				o.bytes.assign(cur.begin(), cur.begin() + long(n));
				out.push_back(o);
				cur.clear();
			}
		}
		// the FIFO heads, taken as soon as offered
		t.g_ts_take_i = 0;
		t.m_ts_take_i = 0;
		t.eval();
		if (t.g_ts_valid_o) {
			g.push_back(decode(t.g_ts_data_o));
			t.g_ts_take_i = 1;
		}
		if (t.m_ts_valid_o) {
			m.push_back(decode(t.m_ts_data_o));
			t.m_ts_take_i = 1;
		}
		phc += 20;
		cyc++;
	}
	void run(unsigned n)
	{
		for (unsigned i = 0; i < n; i++)
			tick();
	}
	void reset()
	{
		t.rst_n = 0;
		t.phc_en_i = 1;
		t.phc_incr_i = 20u << 24;
		t.phc_adj_i = 0;
		t.rx_tvalid_i = 0;
		t.rec_valid_i = 0;
		run(4);
		t.rst_n = 1;
		run(2);
		g.clear();
		m.clear();
		out.clear();
	}
	// a frame's beats on the receive tap, eight octets a beat, little lane order, then idle cycles; returns the
	// PHC at its first beat
	uint64_t beats(const std::vector<uint8_t> &f, unsigned idle)
	{
		uint64_t first = 0;
		for (size_t at = 0; at < f.size(); at += 8) {
			uint64_t d = 0;
			unsigned keep = 0;
			for (unsigned l = 0; l < 8 && at + l < f.size(); l++) {
				d |= uint64_t(f[at + l]) << (8 * l);
				keep |= 1u << l;
			}
			t.rx_tdata_i = d;
			t.rx_tkeep_i = keep;
			t.rx_tvalid_i = 1;
			t.rx_tlast_i = at + 8 >= f.size();
			if (at == 0)
				first = phc;
			if (t.rx_tlast_i) {
				t.eval();
				m_stamp = t.m_rx_stamp_o;
				m_event = t.m_rx_event_o;
			}
			tick();
		}
		t.rx_tvalid_i = 0;
		t.rx_tlast_i = 0;
		run(idle);
		return first;
	}
	// one frame, then long enough for the tap to hand it out whole
	uint64_t frame(const std::vector<uint8_t> &f)
	{
		uint64_t at = beats(f, 4);
		run(unsigned(f.size()) + 40);
		return at;
	}
	// one launch record for both units; returns the PHC on the edge it lands
	uint64_t launch(bool kind, unsigned gen, unsigned type, unsigned seq, unsigned dg, unsigned dm, bool abort)
	{
		t.rec_valid_i = 1;
		t.rec_kind_i = kind;
		t.rec_gen_i = gen;
		t.rec_type_i = type;
		t.rec_seq_i = seq;
		t.rec_delta_g_i = dg;
		t.rec_delta_m_i = dm;
		t.rec_abort_i = abort;
		uint64_t at = phc;
		tick();
		t.rec_valid_i = 0;
		run(4);
		return at;
	}
	void seal() { launch(true, 1, 0, 0, 45, 90, false); }
};

std::vector<uint8_t> gptp(unsigned type, unsigned seq, size_t len = 58, uint64_t da = 0x0180C200000Eull,
			  uint16_t et = 0x88F7, unsigned sdo = 1)
{
	std::vector<uint8_t> f(len, 0);
	for (int i = 0; i < 6; i++)
		f[i] = uint8_t(da >> (8 * (5 - i)));
	f[6] = 0x02;
	f[12] = uint8_t(et >> 8);
	f[13] = uint8_t(et);
	if (len > 15) {
		f[14] = uint8_t((sdo << 4) | type);
		f[15] = 0x12;
	}
	if (len > 45) {
		f[44] = uint8_t(seq >> 8);
		f[45] = uint8_t(seq);
	}
	return f;
}

// a delivered frame's sequenceId (octets 44 and 45)
unsigned seq_of(const Out &o) { return o.bytes.size() > 45 ? (unsigned(o.bytes[44]) << 8) | o.bytes[45] : ~0u; }

}  // namespace

int main(int argc, char **argv)
{
	Verilated::commandArgs(argc, argv);
	Bench b;
	b.reset();

	// ---- ingress: the first beat's PHC, less the board's ingress constant, in the frame's own trailer
	std::vector<uint8_t> sync = gptp(0x0, 0x1234);
	uint64_t at = b.frame(sync);
	check(b.out.size() == 1 && b.out.front().bytes == sync, "I1 a received Sync is delivered whole, its trailer after it",
	      b.out.size(), 1);
	if (!b.out.empty())
		check(b.out.front().trailer == at - 656, "I1 the trailer is the first beat's PHC less INGRESS_LAT (656 ns)",
		      b.out.front().trailer, at - 656);
	check(b.m_event && b.m_stamp == at, "I1 the MII unit (no constant) stamps the first beat's PHC", b.m_stamp, at);
	check(b.g.empty(), "I1 a received frame posts no TIMESTAMP record", b.g.size(), 0);
	b.out.clear();
	std::vector<uint64_t> ats;
	for (unsigned type : {0x2u, 0x3u, 0x1u})
		ats.push_back(b.frame(gptp(type, 7)));
	bool own = b.out.size() == 3;
	for (unsigned i = 0; own && i < 3; i++)
		own = b.out[i].trailer == ats[i] - 656;
	check(own, "I2 Pdelay_Req, Pdelay_Resp and Delay_Req (event messages) each carry their own stamp", b.out.size(), 3);
	b.out.clear();
	b.frame(gptp(0x8, 1));
	b.frame(gptp(0xB, 2, 90));
	b.frame(gptp(0xA, 3));
	bool none = b.out.size() == 3;
	for (const Out &o : b.out)
		none = none && o.trailer == NO_STAMP;
	check(none, "I3 general messages (Follow_Up, Announce, Pdelay_Resp_Follow_Up) carry the no-stamp trailer",
	      b.out.size(), 3);
	b.out.clear();
	b.frame(gptp(0x0, 4, 58, 0x0180C2000021ull));
	check(!b.m_event, "I4 a Sync to another destination is not timed", b.m_event, 0);
	b.frame(gptp(0x0, 5, 58, 0x0180C200000Eull, 0x88B5));   // (0x22EA there is MSRP, the srp channel's)
	check(!b.m_event, "I4 another EtherType at the gPTP address is not timed", b.m_event, 0);
	b.frame(gptp(0x0, 6, 58, 0x0180C200000Eull, 0x8100));
	check(!b.m_event, "I4 a tagged frame is not timed", b.m_event, 0);
	check(b.out.empty(), "I4 and the tap hands none of the three to the gptp channel", b.out.size(), 0);
	b.frame(gptp(0x0, 7, 58, 0x0180C200000Eull, 0x88F7, 0));
	check(!b.m_event && b.out.size() == 1 && b.out.back().trailer == NO_STAMP,
	      "I4 majorSdoId 0 (IEEE 1588, not 802.1AS) is not timed: its record carries the no-stamp trailer",
	      b.out.empty() ? 0 : b.out.back().trailer, NO_STAMP);
	b.out.clear();
	b.frame(gptp(0x0, 8, 16));
	check(b.out.size() == 1 && b.out.back().trailer == NO_STAMP, "I5 a frame of two beats carries no stamp",
	      b.out.empty() ? 0 : b.out.back().trailer, NO_STAMP);
	b.out.clear();

	// ---- a flood (#884's ruling item 2): the mailbox side stalled, frames back to back. Every frame the tap
	// delivers carries its own stamp; a frame it cannot keep is refused whole, stamp and all, and counted.
	unsigned drops0 = b.t.s_rx_drops_o;
	std::vector<uint64_t> flood;
	b.drain = false;
	for (unsigned i = 0; i < 80; i++)
		flood.push_back(b.beats(gptp(0x2, 0x100 + i, 48), 0));
	b.run(8);
	unsigned refused = unsigned(b.t.s_rx_drops_o - drops0);
	b.drain = true;
	b.run(80 * (56 + 4) + 200);
	bool mine = !b.out.empty();
	for (const Out &o : b.out) {
		unsigned k = seq_of(o) - 0x100;
		mine = mine && k < 80 && o.trailer == flood[k] - 656;
	}
	check(mine, "T2 under a flood every delivered frame carries its own stamp", b.out.size(), 64);
	check(b.out.size() == 64 && refused == 16,
	      "T2 the stamp FIFO keeps 64; the 16 past them are refused at the tap and counted", refused, 16);
	b.out.clear();
	// the frame FIFO full first: a frame it drops takes its stamp with it, so the next frame still carries its own
	drops0 = b.t.s_rx_drops_o;
	std::vector<uint64_t> big;
	b.drain = false;
	for (unsigned i = 0; i < 6; i++)
		big.push_back(b.beats(gptp(0x0, 0x200 + i, 1000), 1));
	b.run(8);
	refused = unsigned(b.t.s_rx_drops_o - drops0);
	b.drain = true;
	b.run(6 * 1010 + 200);
	uint64_t after = b.frame(gptp(0x0, 0x2FF));
	mine = b.out.size() >= 2;
	for (const Out &o : b.out) {
		unsigned sq = seq_of(o);
		uint64_t want = sq == 0x2FF ? after : (sq - 0x200 < 6 ? big[sq - 0x200] : 0);
		mine = mine && o.trailer == want - 656;
	}
	check(mine && refused > 0 && b.out.size() + refused == 7,
	      "T3 a frame the frame FIFO drops takes its stamp with it: every delivered frame keeps its own",
	      b.out.size() + refused, 7);
	b.out.clear();
	b.g.clear();
	b.m.clear();

	// ---- egress: sealed first, then the launch's PHC less the derived correction plus EGRESS_LAT
	unsigned toggles = 0, last = b.t.g_seal_req_o;
	for (unsigned i = 0; i < 1200; i++) {
		b.tick();
		toggles += b.t.g_seal_req_o != last;
		last = b.t.g_seal_req_o;
	}
	check(toggles >= 3, "E0 the unit re-offers its seal until the observer echoes", toggles, 3);
	check(b.t.g_seal_gen_o == 1, "E0 the seal names generation 1, never 0", b.t.g_seal_gen_o, 1);
	b.launch(false, 1, 0x0, 9, 45, 90, false);   // the unit's own generation, but no echo yet
	check(b.g.size() == 1 && !b.g.back().ok, "E1 before the echo a launch is a counted loss",
	      b.g.empty() ? 9 : b.g.back().ok, 0);
	b.seal();
	b.g.clear();
	b.m.clear();
	unsigned lost0 = b.t.g_lost_o;
	at = b.launch(false, 1, 0x2, 0x55, 45, 90, false);
	check(b.g.size() == 1, "E2 a launched Pdelay_Req gives one record", b.g.size(), 1);
	if (!b.g.empty()) {
		Rec r = b.g.back();
		check(r.egress && r.ok && r.type == 2 && r.seq == 0x55, "E2 an egress measurement keyed by type and sequenceId");
		check(r.ns == at - 426 + 219, "E2 GMII: the launch's PHC less 426 ns (GPTP_PLANE.md) plus EGRESS_LAT 219 ns",
		      r.ns, at - 426 + 219);
	}
	if (!b.m.empty())
		check(b.m.back().ns == at - 3770, "E2 MII: the launch's PHC less 3770 ns (GPTP_PLANE.md)", b.m.back().ns,
		      at - 3770);
	check(b.t.g_lost_o == lost0, "E2 a measurement counts no loss", b.t.g_lost_o, lost0);
	b.g.clear();
	b.m.clear();
	b.launch(false, 1, 0x0, 1, 45, 90, true);
	b.launch(false, 1, 0x0, 2, 44, 89, false);
	check(b.g.size() == 2 && !b.g[0].ok && !b.g[1].ok, "E3 an aborted launch and a fragmented one are losses");
	check(b.t.g_lost_o == lost0 + 2, "E3 and both are counted", b.t.g_lost_o, lost0 + 2);
	b.g.clear();
	b.launch(false, 1, 0x8, 3, 45, 90, false);
	check(b.g.empty(), "E4 a launched Follow_Up is not timed", b.g.size(), 0);

	// ---- the PHC's trajectory across the reconstructed window
	b.g.clear();
	b.t.phc_adjust_i = 1;
	b.tick();
	b.t.phc_adjust_i = 0;
	b.run(20);
	b.launch(false, 1, 0x0, 4, 45, 90, false);
	check(b.g.size() == 1 && !b.g.back().ok, "G1 a launch 20 cycles after a PHC step is a loss, not a stamp");
	b.run(100);
	b.g.clear();
	b.launch(false, 1, 0x0, 5, 45, 90, false);
	check(b.g.size() == 1 && b.g.back().ok, "G2 once the guard has elapsed the next launch is a stamp");
	b.g.clear();
	b.t.phc_adj_i = 67110;   // one unit past the 200 ppm envelope at 50 MHz
	b.run(100);
	b.launch(false, 1, 0x0, 6, 45, 90, false);
	check(b.g.size() == 1 && !b.g.back().ok, "G3 an addend past the 200 ppm envelope is a loss");
	b.t.phc_adj_i = 67109;
	b.run(100);
	b.g.clear();
	b.launch(false, 1, 0x0, 7, 45, 90, false);
	check(b.g.size() == 1 && b.g.back().ok, "G3 an addend at the envelope is a stamp");
	b.t.phc_adj_i = 0;
	b.run(100);

	// ---- an observer reset: another generation is a loss and the unit seals again
	b.g.clear();
	b.launch(false, 0, 0x0, 8, 45, 90, false);
	check(b.g.size() == 1 && !b.g.back().ok, "S1 a record of generation 0 (the observer reset) is a loss");
	toggles = 0;
	last = b.t.g_seal_req_o;
	for (unsigned i = 0; i < 1200; i++) {
		b.tick();
		toggles += b.t.g_seal_req_o != last;
		last = b.t.g_seal_req_o;
	}
	check(toggles >= 3, "S1 and the unit offers its seal again", toggles, 3);
	b.seal();
	b.g.clear();
	b.launch(false, 1, 0x0, 9, 45, 90, false);
	check(b.g.size() == 1 && b.g.back().ok, "S2 after the echo launches are stamped again");

	// ---- the egress FIFO: held in order when nobody takes them, the 33rd counted (at least the 15 frames the
	// gptp transmit ring holds, so the firmware's own sends never overrun it)
	b.g.clear();
	b.m.clear();
	unsigned drop0 = b.t.g_drop_o;
	// stop taking: a bench that does not drain
	ats.clear();
	for (unsigned i = 0; i < 33; i++) {
		b.t.rec_valid_i = 1;
		b.t.rec_kind_i = 0;
		b.t.rec_gen_i = 1;
		b.t.rec_type_i = 0;
		b.t.rec_seq_i = 100 + i;
		b.t.rec_delta_g_i = 45;
		b.t.rec_delta_m_i = 90;
		b.t.rec_abort_i = 0;
		ats.push_back(b.phc);
		b.t.phc_ns_i = b.phc;
		b.t.clk_i = 0;
		b.t.eval();
		b.t.clk_i = 1;
		b.t.eval();
		b.phc += 20;
		b.t.rec_valid_i = 0;
		for (unsigned k = 0; k < 4; k++) {
			b.t.phc_ns_i = b.phc;
			b.t.g_ts_take_i = 0;
			b.t.m_ts_take_i = 0;
			b.t.clk_i = 0;
			b.t.eval();
			b.t.clk_i = 1;
			b.t.eval();
			b.phc += 20;
		}
	}
	check(b.t.g_drop_o == drop0 + 1, "F1 the 33rd egress record past 32 held is counted", b.t.g_drop_o, drop0 + 1);
	b.run(60);
	check(b.g.size() == 32, "F2 the 32 held records come out", b.g.size(), 32);
	bool order = b.g.size() == 32;
	for (unsigned i = 0; i < b.g.size() && i < 32; i++)
		order = order && b.g[i].seq == 100 + i && b.g[i].ns == ats[i] - 426 + 219;
	check(order, "F2 in the order they were timed, each with its own stamp");

	std::printf("== gptp timestamp unit (KL_gptp_tsu): checks: %d   failures: %d ==\n", checks, failures);
	std::printf("RESULT: %s\n", failures ? "FAIL" : "PASS");
	return failures ? 1 : 0;
}

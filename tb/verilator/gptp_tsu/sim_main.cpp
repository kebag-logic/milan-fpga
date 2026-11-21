// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// sim_main.cpp - the timestamp unit (hdl/ieee8021as/gptp_tsu/KL_gptp_tsu.sv,
// #884, #665 F6), self-checking. Every expected stamp is computed here from
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

struct Bench {
	Vtb_gptp_tsu t;
	uint64_t phc = 1'000'000'000'000ull;   // the PHC: 20 ns a cycle, the 50 MHz shape
	uint64_t cyc = 0;
	std::deque<Rec> g, m;

	void tick()
	{
		t.phc_ns_i = phc;
		t.clk_i = 0;
		t.eval();
		t.clk_i = 1;
		t.eval();
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
	}
	// a frame on the receive tap, eight octets a beat, little lane order; returns the PHC at its first beat
	uint64_t frame(const std::vector<uint8_t> &f)
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
			tick();
		}
		t.rx_tvalid_i = 0;
		t.rx_tlast_i = 0;
		run(4);
		return first;
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
	f[14] = uint8_t((sdo << 4) | type);
	f[15] = 0x12;
	if (len > 45) {
		f[44] = uint8_t(seq >> 8);
		f[45] = uint8_t(seq);
	}
	return f;
}

}  // namespace

int main(int argc, char **argv)
{
	Verilated::commandArgs(argc, argv);
	Bench b;
	b.reset();

	// ---- ingress: the first beat's PHC, less the board's ingress constant
	uint64_t at = b.frame(gptp(0x0, 0x1234));
	check(b.g.size() == 1, "I1 a received Sync gives one record", b.g.size(), 1);
	if (!b.g.empty()) {
		Rec r = b.g.front();
		check(!r.egress && r.ok, "I1 it is an ingress measurement");
		check(r.type == 0 && r.seq == 0x1234, "I1 keyed by messageType and sequenceId", r.seq, 0x1234);
		check(r.ns == at - 656, "I1 the stamp is the first beat's PHC less INGRESS_LAT (656 ns)", r.ns, at - 656);
	}
	check(b.m.size() == 1 && b.m.front().ns == at, "I1 the MII unit (no constant) stamps the first beat's PHC",
	      b.m.empty() ? 0 : b.m.front().ns, at);
	b.g.clear();
	b.m.clear();
	for (unsigned type : {0x2u, 0x3u, 0x1u})
		b.frame(gptp(type, 7));
	check(b.g.size() == 3, "I2 Pdelay_Req, Pdelay_Resp and Delay_Req (event messages) are all timed", b.g.size(), 3);
	b.g.clear();
	b.m.clear();
	b.frame(gptp(0x8, 1));
	b.frame(gptp(0xB, 2, 90));
	b.frame(gptp(0xA, 3));
	check(b.g.empty(), "I3 general messages (Follow_Up, Announce, Pdelay_Resp_Follow_Up) are not timed", b.g.size(), 0);
	b.frame(gptp(0x0, 4, 58, 0x0180C2000021ull));
	check(b.g.empty(), "I4 a Sync to another destination is not timed", b.g.size(), 0);
	b.frame(gptp(0x0, 5, 58, 0x0180C200000Eull, 0x22EA));
	check(b.g.empty(), "I4 another EtherType at the gPTP address is not timed", b.g.size(), 0);
	b.frame(gptp(0x0, 6, 58, 0x0180C200000Eull, 0x8100));
	check(b.g.empty(), "I4 a tagged frame is not timed", b.g.size(), 0);
	b.frame(gptp(0x0, 7, 58, 0x0180C200000Eull, 0x88F7, 0));
	check(b.g.empty(), "I4 majorSdoId 0 (IEEE 1588, not 802.1AS) is not timed", b.g.size(), 0);
	b.frame(gptp(0x0, 8, 44));
	check(b.g.empty(), "I5 a frame that ends before its sequenceId is not timed", b.g.size(), 0);
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

	// ---- the FIFO: held in order when nobody takes them, the ninth counted
	b.g.clear();
	b.m.clear();
	unsigned drop0 = b.t.g_drop_o;
	// stop taking: a bench that does not drain
	std::vector<uint64_t> ats;
	for (unsigned i = 0; i < 9; i++) {
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
	check(b.t.g_drop_o == drop0 + 1, "F1 the ninth record past eight held is counted", b.t.g_drop_o, drop0 + 1);
	b.run(20);
	check(b.g.size() == 8, "F2 the eight held records come out", b.g.size(), 8);
	bool order = b.g.size() == 8;
	for (unsigned i = 0; i < b.g.size() && i < 8; i++)
		order = order && b.g[i].seq == 100 + i && b.g[i].ns == ats[i] - 426 + 219;
	check(order, "F2 in the order they were timed, each with its own stamp");

	std::printf("== gptp timestamp unit (KL_gptp_tsu): checks: %d   failures: %d ==\n", checks, failures);
	std::printf("RESULT: %s\n", failures ? "FAIL" : "PASS");
	return failures ? 1 : 0;
}

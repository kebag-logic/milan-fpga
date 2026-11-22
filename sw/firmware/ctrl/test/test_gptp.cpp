// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// test_gptp.cpp - the firmware gPTP end station port (gptp/gptp.h; #665 F6,
// #884) on the host. Each test names the clause it checks: IEEE 802.1AS-2020
// unless another document is named, and the fabric engine's constants table
// (gptp-processor docs/INTEGRATION.md) where a value is that table's.
//
// Two kinds of test. The scripted ones hand one port frames built here, by
// this file's own builders, never by the port's codec, and read what it
// sends. The network ones join two ports through a simulated wire and two
// simulated PHCs that drift and answer the HAL's rate and step, and read the
// offset between the two clocks from outside both ports.

#include <gtest/gtest.h>

#include <cmath>
#include <cstdint>
#include <cstring>
#include <deque>
#include <vector>

#include "fw_gtest.hpp"

extern "C" {
#include "gptp.h"
}

FW_TALLY_LABEL("ctrl gPTP end station port (host)");

namespace {

using Bytes = std::vector<uint8_t>;

constexpr uint64_t kClockA = 0x0011'22FF'FE33'4455ull;
constexpr uint64_t kClockB = 0x0066'77FF'FE88'99AAull;
constexpr uint32_t kClk = 50'000'000u;   // the PHC's clock: 20 ns a tick

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

void put_ts(Bytes &f, size_t at, uint64_t ns)
{
	be(f, at, ns / 1'000'000'000ull, 6);
	be(f, at + 6, ns % 1'000'000'000ull, 4);
}

uint64_t get_ts(const Bytes &f, size_t at)
{
	return rd(f, at, 6) * 1'000'000'000ull + rd(f, at + 6, 4);
}

// a gPTP frame by this file's own reading of 10.6.2 and 11.3.4
Bytes frame(unsigned type, unsigned ptp_len, uint64_t src_clock, uint16_t seq, uint8_t control, int8_t logi)
{
	Bytes f(14 + ptp_len, 0);
	const uint8_t da[6] = {0x01, 0x80, 0xC2, 0x00, 0x00, 0x0E};
	std::memcpy(f.data(), da, 6);
	be(f, 6, 0x020000000001ull, 6);
	be(f, 12, 0x88F7, 2);
	f[14] = uint8_t(0x10 | type);
	f[15] = 0x12;
	be(f, 16, ptp_len, 2);
	be(f, 34, src_clock, 8);
	be(f, 42, 1, 2);
	be(f, 44, seq, 2);
	f[46] = control;
	f[47] = uint8_t(logi);
	return f;
}

Bytes pdelay_req(uint64_t src, uint16_t seq)
{
	return frame(0x2, 54, src, seq, 5, 0);
}

Bytes pdelay_resp(uint64_t src, uint16_t seq, uint64_t t2, uint64_t req_clock, bool fu)
{
	Bytes f = frame(fu ? 0xA : 0x3, 54, src, seq, 5, 0x7F);
	if (!fu)
		f[20] = 0x02;   // twoStepFlag
	put_ts(f, 48, t2);
	be(f, 58, req_clock, 8);
	be(f, 66, 1, 2);
	return f;
}

Bytes announce(uint64_t src, uint16_t seq, uint8_t p1, uint64_t gm, uint16_t steps,
	       std::vector<uint64_t> path = {})
{
	unsigned len = 64 + (path.empty() ? 0 : 4 + 8 * unsigned(path.size()));
	Bytes f = frame(0xB, len, src, seq, 5, 0);
	f[48 + 13] = p1;
	f[48 + 14] = 248;
	f[48 + 15] = 0x22;
	be(f, 48 + 16, 0x436A, 2);
	f[48 + 18] = 248;
	be(f, 48 + 19, gm, 8);
	be(f, 48 + 27, steps, 2);
	f[48 + 29] = 0xA0;
	if (!path.empty()) {
		be(f, 14 + 64, 0x0008, 2);
		be(f, 14 + 66, 8 * path.size(), 2);
		for (size_t i = 0; i < path.size(); i++)
			be(f, 14 + 68 + 8 * i, path[i], 8);
	}
	return f;
}

Bytes sync_msg(uint64_t src, uint16_t seq)
{
	Bytes f = frame(0x0, 44, src, seq, 0, -3);
	f[20] = 0x02;
	return f;
}

Bytes follow_up(uint64_t src, uint16_t seq, uint64_t origin, int64_t corr_ns = 0)
{
	Bytes f = frame(0x8, 76, src, seq, 2, -3);
	put_ts(f, 48, origin);
	be(f, 22, uint64_t(corr_ns) << 16, 8);
	be(f, 58, 0x0003, 2);
	be(f, 60, 28, 2);
	f[62] = 0x00;
	f[63] = 0x80;
	f[64] = 0xC2;
	f[67] = 1;
	return f;
}

// a Follow_Up whose messageLength is ptp_len: its fixed fields and as much of its information TLV as fits
Bytes follow_up_len(uint64_t src, uint16_t seq, uint64_t origin, unsigned ptp_len)
{
	Bytes f = follow_up(src, seq, origin);
	f.resize(14 + ptp_len, 0);
	be(f, 16, ptp_len, 2);
	return f;
}

// ---- the fake HAL: what a port sends, and its PHC calls ----
struct Hal {
	std::vector<Bytes> sent[2];
	int32_t trim[2] = {0, 0};
	std::vector<int64_t> steps[2];
	bool room = true;
};

bool hal_send(void *ctx, unsigned port, const uint8_t *f, unsigned len)
{
	auto *h = static_cast<Hal *>(ctx);
	if (!h->room)
		return false;
	h->sent[port].emplace_back(f, f + len);
	return true;
}

void hal_adjfine(void *ctx, unsigned port, int32_t addend)
{
	static_cast<Hal *>(ctx)->trim[port] = addend;
}

void hal_step(void *ctx, unsigned port, int64_t delta)
{
	static_cast<Hal *>(ctx)->steps[port].push_back(delta);
}

gptp_config config(uint64_t clock, uint8_t p1 = 248)
{
	gptp_config c{};
	c.clock_id = clock;
	c.mac[0] = 0x02;
	c.mac[5] = uint8_t(clock);
	c.priority1 = p1;
	c.priority2 = 248;
	c.phc_clk_hz = kClk;
	return c;
}

// One port under scripted input.
struct Scripted : ::testing::Test {
	Hal hal;
	gptp_port port{};
	uint32_t now = 0;

	void start(uint8_t p1 = 248)
	{
		gptp_hal h{&hal, hal_send, hal_adjfine, hal_step};
		gptp_config c = config(kClockA, p1);
		gptp_port_init(&port, 0, &c, &h, now);
		gptp_port_link(&port, true);
	}
	void tick(uint32_t ms)
	{
		for (uint32_t i = 0; i < ms; i += 10) {
			now += 10;
			gptp_port_tick(&port, now);
		}
	}
	void rx(const Bytes &f, bool stamp = false, uint64_t ns = 0, bool stamp_first = true)
	{
		unsigned type = f[14] & 0x0F;
		uint16_t seq = uint16_t(rd(f, 44, 2));
		if (stamp && stamp_first)
			gptp_port_ts(&port, false, type, seq, ns, true);
		gptp_port_rx(&port, f.data(), unsigned(f.size()));
		if (stamp && !stamp_first)
			gptp_port_ts(&port, false, type, seq, ns, true);
	}
	std::vector<Bytes> of_type(unsigned type)
	{
		std::vector<Bytes> r;
		for (auto &f : hal.sent[0])
			if ((f[14] & 0x0F) == type)
				r.push_back(f);
		return r;
	}
	const Bytes &last_req() { return hal.sent[0].back(); }
	uint16_t last_seq() { return uint16_t(rd(of_type(0x2).back(), 44, 2)); }
	// this port's PHC moved by a step it asked for: its own stamps (t1, t4) carry the shift from here on
	int64_t own_shift = 0;
	// answer the request in flight from a responder with a 500 ns link
	void answer(uint64_t responder, uint64_t t1, uint64_t t2, uint64_t t3, uint64_t t4)
	{
		auto reqs = of_type(0x2);
		ASSERT_FALSE(reqs.empty());
		uint16_t seq = uint16_t(rd(reqs.back(), 44, 2));
		gptp_port_ts(&port, true, 0x2, seq, t1, true);
		rx(pdelay_resp(responder, seq, t2, kClockA, false), true, t4);
		rx(pdelay_resp(responder, seq, t3, kClockA, true));
	}
	// n good exchanges, a second apart, a 500 ns link, the responder `ppm` fast and turning a
	// request round in `turn_ns` of its own time
	void exchanges(unsigned n, double ppm = 0.0, int64_t delay = 500, double turn_ns = 30'000.0)
	{
		for (unsigned i = 0; i < n; i++) {
			uint64_t t1 = 1'000'000'000ull * (now / 1000 + 1);
			uint64_t t2 = uint64_t(double(t1) * (1.0 + ppm * 1e-6)) + uint64_t(delay);
			uint64_t t3 = t2 + uint64_t(turn_ns);
			uint64_t t4 = t1 + uint64_t(2 * delay) + uint64_t(turn_ns / (1.0 + ppm * 1e-6));
			answer(kClockB, t1 + uint64_t(own_shift), t2, t3, t4 + uint64_t(own_shift));
			tick(1000);
		}
	}
};

// ---------------------------------------------------------------- the codec

TEST(GptpCodec, TimestampIsSecondsThenNanoseconds)
{
	// 10.6.2 via IEEE 1588 5.3.3: 48-bit secondsField, 32-bit nanosecondsField
	uint8_t at[10];
	uint64_t ns = 0x0001'2345'6789ull * 1'000'000'000ull + 987'654'321ull;
	gptp_ts_put(at, ns);
	Bytes f(at, at + 10);
	EXPECT_EQ(rd(f, 0, 6), 0x0001'2345'6789ull);
	EXPECT_EQ(rd(f, 6, 4), 987'654'321ull);
	EXPECT_EQ(gptp_ts_get(at), ns) << "a timestamp does not survive its own encoding";
}

TEST(GptpCodec, RateEnvelopeIsTheTxretOne)
{
	// KL_gptp_txret's PHC_ADJ_MAX_C at 200 ppm and 50 MHz, the engine's integrator clamp
	EXPECT_EQ(gptp_addend_of_ppm(200, kClk), 67109) << "the rate envelope differs from the fabric's";
	EXPECT_EQ(gptp_addend_of_ppm(-200, kClk), -67109);
}

// ---------------------------------------------------------------- peer delay

TEST_F(Scripted, LinkUpSendsOnePdelayReqAtOnce)
{
	// the link's return sends one Pdelay_Req at once (GPTP_PLANE.md, Milan v1.2 4.2.6.2.5's toggle)
	start();
	ASSERT_EQ(hal.sent[0].size(), 1u) << "no Pdelay_Req at link-up";
	const Bytes &f = hal.sent[0][0];
	EXPECT_EQ(rd(f, 0, 6), 0x0180C200000Eull) << "11.3.4: the gPTP destination address";
	EXPECT_EQ(rd(f, 12, 2), 0x88F7u) << "11.3.5: EtherType";
	EXPECT_EQ(f[14], 0x12) << "majorSdoId 1, Pdelay_Req";
	EXPECT_EQ(f[15], 0x12) << "minorVersionPTP 1, versionPTP 2";
	EXPECT_EQ(rd(f, 16, 2), 54u) << "11.4.5: Pdelay_Req is 54 octets";
	EXPECT_EQ(rd(f, 34, 8), kClockA);
	EXPECT_EQ(f[46], 5) << "controlField 5";
	EXPECT_EQ(f[47], 0) << "logMessageInterval 0: Milan v1.2 Table 4.1's 1 s";
	EXPECT_EQ(f.size(), 14u + 54u);
}

TEST_F(Scripted, PdelayReqEverySecond)
{
	start();
	tick(5000);
	EXPECT_EQ(of_type(0x2).size(), 6u) << "Milan v1.2 4.2.6.2.2 Table 4.1: one Pdelay_Req a second";
}

TEST_F(Scripted, ResponderAnswersWithBothTimestamps)
{
	// 11.2.20: Pdelay_Resp carries t2 and the requester; its Follow_Up carries t3
	start();
	hal.sent[0].clear();
	rx(pdelay_req(kClockB, 77), true, 5'000'000'123ull);
	auto r = of_type(0x3);
	ASSERT_EQ(r.size(), 1u) << "no Pdelay_Resp to a stamped Pdelay_Req";
	EXPECT_EQ(rd(r[0], 44, 2), 77u);
	EXPECT_EQ(get_ts(r[0], 48), 5'000'000'123ull) << "requestReceiptTimestamp is not the ingress stamp";
	EXPECT_EQ(rd(r[0], 58, 8), kClockB) << "requestingPortIdentity";
	EXPECT_EQ(r[0][20] & 0x02, 0x02) << "twoStepFlag";
	EXPECT_TRUE(of_type(0xA).empty()) << "a Follow_Up before the response's own egress stamp";
	gptp_port_ts(&port, true, 0x3, 77, 5'000'040'000ull, true);
	auto fu = of_type(0xA);
	ASSERT_EQ(fu.size(), 1u) << "no Pdelay_Resp_Follow_Up after the egress stamp";
	EXPECT_EQ(get_ts(fu[0], 48), 5'000'040'000ull) << "responseOriginTimestamp is not the egress stamp";
	EXPECT_EQ(rd(fu[0], 58, 8), kClockB);
}

TEST_F(Scripted, ResponderTakesAStampThatComesAfterItsFrame)
{
	start();
	hal.sent[0].clear();
	rx(pdelay_req(kClockB, 9), true, 123'456'789ull, /*stamp_first=*/false);
	auto r = of_type(0x3);
	ASSERT_EQ(r.size(), 1u) << "a stamp read after its frame was never paired";
	EXPECT_EQ(get_ts(r[0], 48), 123'456'789ull);
}

TEST_F(Scripted, AsCapableNeedsTwoGoodExchangesAndARate)
{
	// Milan v1.2 4.2.6.2.4: two good exchanges; 11.2.2: a measured neighborRateRatio
	start();
	exchanges(1);
	EXPECT_FALSE(gptp_port_pub(&port)->as_capable) << "asCapable after one exchange";
	exchanges(1);
	EXPECT_TRUE(gptp_port_pub(&port)->as_capable) << "not asCapable after two good exchanges";
	EXPECT_EQ(gptp_port_pub(&port)->pdelay_ns, 500) << "11.2.19.3.4: the link delay";
}

TEST_F(Scripted, AsCapableNeedsTwoGoodInARow)
{
	// Milan v1.2 4.2.6.2.4: the rate ratio measured, one good exchange after a bad one is not enough
	start();
	exchanges(1, 0.0, 900);   // over neighborPropDelayThresh: not good, but it seeds the rate window
	exchanges(1);
	EXPECT_FALSE(gptp_port_pub(&port)->as_capable) << "asCapable after one good exchange with a rate";
	exchanges(1);
	EXPECT_TRUE(gptp_port_pub(&port)->as_capable) << "not asCapable after two good exchanges in a row";
}

TEST_F(Scripted, RateRatioAndDelayWithAFastNeighbor)
{
	// 11.2.19.3.3: the responder 100 ppm fast; 11.2.19.3.4 corrects its 3 ms turnaround by it,
	// 150 ns of the delay
	start();
	exchanges(4, 100.0, 400, 3'000'000.0);
	double nrr = double(port.pd.nrr_q32) / 4294967296.0 * 1e6;
	EXPECT_NEAR(nrr, 100.0, 0.05) << "neighborRateRatio";
	EXPECT_NEAR(port.pd.delay_ns, 400, 2) << "the delay ignores the neighbor's rate";
}

TEST_F(Scripted, DelayOverThresholdIsNotAsCapable)
{
	start();
	exchanges(3, 0.0, 801);
	EXPECT_FALSE(gptp_port_pub(&port)->as_capable) << "Milan v1.2 4.2.6.1.1: 801 ns is over neighborPropDelayThresh";
	gptp_port_link(&port, false);
	gptp_port_link(&port, true);
	exchanges(3, 0.0, 800);
	EXPECT_TRUE(gptp_port_pub(&port)->as_capable) << "800 ns is at the threshold, inside it";
}

TEST_F(Scripted, FifthLostResponseClearsAsCapable)
{
	// 11.2.19 Figure 11-8 with allowedLostResponses 3: the fifth consecutive loss clears it
	start();
	exchanges(2);
	ASSERT_TRUE(gptp_port_pub(&port)->as_capable);
	for (unsigned i = 0; i < 4; i++)
		tick(1000);
	EXPECT_TRUE(gptp_port_pub(&port)->as_capable) << "asCapable fell at the fourth lost response";
	tick(1000);
	EXPECT_FALSE(gptp_port_pub(&port)->as_capable) << "asCapable held past the fifth lost response";
}

TEST_F(Scripted, LateResponseIsLost)
{
	// Milan v1.2 4.2.6.2.6 as the engine reads it: t4 - t1 over 15.006181 ms is lost, at it kept
	start();
	exchanges(2);
	ASSERT_EQ(port.ctr.pd_late, 0u);
	uint64_t t1 = 50'000'000'000ull;
	answer(kClockB, t1, t1 + 500, t1 + 30'000, t1 + 15'006'182ull);
	EXPECT_EQ(port.ctr.pd_late, 1u) << "a response 15.006182 ms after its request was used";
	tick(1000);
	uint64_t t1b = 52'000'000'000ull;
	answer(kClockB, t1b, t1b + 500, t1b + 30'000, t1b + 15'006'181ull);
	EXPECT_EQ(port.ctr.pd_late, 1u) << "a response at the bound was refused";
	EXPECT_EQ(port.ctr.pd_done, 3u);
}

TEST_F(Scripted, MultipleRespondersCeaseAndALinkToggleResumes)
{
	// Milan v1.2 4.2.6.2.5: three multi-answered requests in a row cease Pdelay_Req; a link edge ends it
	start();
	for (unsigned i = 0; i < 3; i++) {
		auto reqs = of_type(0x2);
		uint16_t seq = uint16_t(rd(reqs.back(), 44, 2));
		uint64_t t1 = 1'000'000'000ull * (i + 10);
		gptp_port_ts(&port, true, 0x2, seq, t1, true);
		rx(pdelay_resp(kClockB, seq, t1, kClockA, false), true, t1 + 1000);
		rx(pdelay_resp(0x1234ull, seq, t1, kClockA, false), true, t1 + 1100);
		rx(pdelay_resp(kClockB, seq, t1 + 10, kClockA, true));
		tick(1000);
	}
	size_t before = of_type(0x2).size();
	tick(10'000);
	EXPECT_EQ(of_type(0x2).size(), before) << "Pdelay_Req still sent during the cease";
	EXPECT_FALSE(gptp_port_pub(&port)->as_capable);
	gptp_port_link(&port, false);
	gptp_port_link(&port, true);
	EXPECT_EQ(of_type(0x2).size(), before + 1) << "the link toggle did not end the cease";
}

TEST_F(Scripted, ASecondResponderAfterTheFirstsFollowUpStillCeases)
{
	// Milan v1.2 4.2.6.2.5: responses from more than one clock identity to each of three successive requests
	// cease Pdelay_Req, whatever their order; here the second clock answers after the first's exchange completed
	start();
	for (unsigned i = 0; i < 3; i++) {
		uint16_t seq = last_seq();
		uint64_t t1 = 1'000'000'000ull * (i + 10);
		answer(kClockB, t1, t1 + 500, t1 + 30'500, t1 + 31'000);
		rx(pdelay_resp(0x1234ull, seq, t1 + 600, kClockA, false), true, t1 + 32'000);
		if (i < 2)
			tick(1000);
	}
	EXPECT_TRUE(port.pd.ceased) << "three requests each answered by two clocks, the second late, did not cease";
	size_t before = of_type(0x2).size();
	tick(10'000);
	EXPECT_EQ(of_type(0x2).size(), before) << "Pdelay_Req still sent after three late second responders";
}

TEST_F(Scripted, ARequestAnsweredByOneClockEndsTheRun)
{
	// ibid.: the three must be successive; one answered by a single clock, or by none, starts the count again
	start();
	auto two = [&](unsigned i) {
		uint16_t seq = last_seq();
		uint64_t t1 = 1'000'000'000ull * (i + 10);
		answer(kClockB, t1, t1 + 500, t1 + 30'500, t1 + 31'000);
		rx(pdelay_resp(0x1234ull, seq, t1 + 600, kClockA, false), true, t1 + 32'000);
	};
	two(0);
	tick(1000);
	two(1);
	tick(1000);
	answer(kClockB, 12'000'000'000ull, 12'000'000'500ull, 12'000'030'500ull, 12'000'031'000ull);   // one clock
	tick(1000);
	two(3);
	tick(1000);
	two(4);
	tick(1000);
	tick(1000);   // a request nobody answered
	two(6);
	tick(1000);
	two(7);
	EXPECT_FALSE(port.pd.ceased) << "requests answered by one clock or by none did not end the run";
	tick(1000);
	two(8);
	EXPECT_TRUE(port.pd.ceased) << "three multi-answered requests in a row after a clean one did not cease";
}

TEST_F(Scripted, OneClockAnsweringTwiceIsNotAsCapableButDoesNotCease)
{
	// 10.2.5.1 c): a second response to one request is never asCapable; Milan v1.2 4.2.6.2.5 ceases only on
	// responses from multiple clock identities
	start();
	for (unsigned i = 0; i < 4; i++) {
		uint16_t seq = last_seq();
		uint64_t t1 = 1'000'000'000ull * (i + 10);
		gptp_port_ts(&port, true, 0x2, seq, t1, true);
		rx(pdelay_resp(kClockB, seq, t1 + 500, kClockA, false), true, t1 + 31'000);
		rx(pdelay_resp(kClockB, seq, t1 + 500, kClockA, false), true, t1 + 31'100);
		rx(pdelay_resp(kClockB, seq, t1 + 30'500, kClockA, true));
		tick(1000);
	}
	EXPECT_FALSE(port.pd.ceased) << "one clock answering twice ceased Pdelay_Req";
	EXPECT_FALSE(gptp_port_pub(&port)->as_capable) << "two responses to each request were asCapable";
}

TEST_F(Scripted, TheCeaseEndsAfterFiveMinutes)
{
	// Milan v1.2 4.2.6.2.5: Pdelay_Req resumes after 5 minutes
	start();
	for (unsigned i = 0; i < 3; i++) {
		uint16_t seq = last_seq();
		uint64_t t1 = 1'000'000'000ull * (i + 10);
		gptp_port_ts(&port, true, 0x2, seq, t1, true);
		rx(pdelay_resp(kClockB, seq, t1, kClockA, false), true, t1 + 1000);
		rx(pdelay_resp(0x1234ull, seq, t1, kClockA, false), true, t1 + 1100);
		rx(pdelay_resp(kClockB, seq, t1 + 10, kClockA, true));
		if (i < 2)
			tick(1000);
	}
	ASSERT_TRUE(port.pd.ceased);
	size_t before = of_type(0x2).size();
	tick(299'000);
	EXPECT_EQ(of_type(0x2).size(), before) << "Pdelay_Req resumed before 5 minutes";
	tick(2'000);
	EXPECT_GT(of_type(0x2).size(), before) << "Pdelay_Req did not resume after 5 minutes";
}

TEST_F(Scripted, ATurnaroundLongerThanTheRoundTripIsNoMeasurement)
{
	// 11.2.19.3.4: the responder's turnaround sits inside the round trip; one longer straddles a step of the
	// responder's clock, and its exchange reaches neither the delay nor the rate
	start();
	exchanges(1);
	ASSERT_EQ(port.pd.delay_ns, 500);
	uint64_t t1 = 1'000'000'000ull * (now / 1000 + 1);
	answer(kClockB, t1, t1 + 500, t1 + 30'500 + 200'000, t1 + 31'000);   // the responder stepped 200 us on
	EXPECT_EQ(port.pd.delay_ns, 500) << "a turnaround over the round trip reached the delay";
	tick(1000);
	exchanges(2);
	EXPECT_EQ(port.pd.delay_ns, 500) << "a turnaround over the round trip reached the rate";
	EXPECT_TRUE(gptp_port_pub(&port)->as_capable);
}

TEST_F(Scripted, AnOwnStepVoidsTheExchangeInFlightAndRestartsTheRateWindow)
{
	// 11.2.19.3.3 takes the LocalClock as never stepped, and this port's PHC steps (gptp-processor #68): the
	// exchange whose own stamps straddle the step is void, and the rate window restarts, so the step reaches
	// neither the delay nor neighborRateRatio. The 10 ms turnaround makes a step's rate error visible.
	start();
	exchanges(3, 0.0, 500, 10'000'000.0);
	ASSERT_TRUE(gptp_port_pub(&port)->as_capable);
	rx(announce(kClockB, 1, 100, 0xAAAAull, 0));
	uint16_t seq = last_seq();
	uint64_t t1 = 1'000'000'000ull * (now / 1000);
	gptp_port_ts(&port, true, 0x2, seq, t1, true);    // the request in flight left before the step
	uint64_t t = 30'000'000'000ull;
	rx(sync_msg(kClockB, 7), true, t);
	// 50 us behind: the link-up threshold steps it on, so the straddling round trip is long, not impossible
	rx(follow_up(kClockB, 7, t - 500 + 50'000));
	ASSERT_EQ(hal.steps[0].size(), 1u);
	ASSERT_EQ(hal.steps[0][0], 50'000);
	own_shift = 50'000;
	uint32_t done = port.ctr.pd_done;
	rx(pdelay_resp(kClockB, seq, t1 + 500, kClockA, false), true, t1 + 10'001'000 + uint64_t(own_shift));
	rx(pdelay_resp(kClockB, seq, t1 + 10'000'500, kClockA, true));
	EXPECT_EQ(port.ctr.pd_done, done) << "the exchange straddling the step was used";
	tick(1000);
	exchanges(3, 0.0, 500, 10'000'000.0);
	EXPECT_NEAR(port.pd.delay_ns, 500, 2) << "the rate across the step reached the delay";
	EXPECT_TRUE(gptp_port_pub(&port)->as_capable) << "asCapable fell across this port's own step";
}

TEST_F(Scripted, AnOwnStepCompletesNoResponseOwed)
{
	// the peer's turnaround is t3 - t2 on this port's PHC; across this port's step it is no turnaround, so a
	// response owed at the step is not completed, and the peer counts one lost response (11.2.19.3.4)
	start();
	exchanges(2);
	rx(announce(kClockB, 1, 100, 0xAAAAull, 0));
	hal.sent[0].clear();
	rx(pdelay_req(kClockB, 77), true, 5'000'000'000ull);
	ASSERT_EQ(of_type(0x3).size(), 1u);
	uint64_t t = 6'000'000'000ull;
	rx(sync_msg(kClockB, 5), true, t);
	rx(follow_up(kClockB, 5, t - 500 - 50'000));
	ASSERT_EQ(hal.steps[0].size(), 1u);
	gptp_port_ts(&port, true, 0x3, 77, 5'000'040'000ull, true);
	EXPECT_TRUE(of_type(0xA).empty()) << "a Pdelay_Resp_Follow_Up across this port's step was sent";
}

TEST_F(Scripted, OwnResponseIsIgnored)
{
	// asCapable is never earned from this clock's own responses (the fork's rule, 11.2.2)
	start();
	for (unsigned i = 0; i < 3; i++) {
		auto reqs = of_type(0x2);
		uint16_t seq = uint16_t(rd(reqs.back(), 44, 2));
		uint64_t t1 = 1'000'000'000ull * (i + 3);
		gptp_port_ts(&port, true, 0x2, seq, t1, true);
		rx(pdelay_resp(kClockA, seq, t1, kClockA, false), true, t1 + 1000);
		rx(pdelay_resp(kClockA, seq, t1 + 10, kClockA, true));
		tick(1000);
	}
	EXPECT_FALSE(gptp_port_pub(&port)->as_capable) << "asCapable from its own responses";
}

TEST_F(Scripted, LinkDownClearsAsCapableAtOnce)
{
	start();
	exchanges(2);
	ASSERT_TRUE(gptp_port_pub(&port)->as_capable);
	gptp_port_link(&port, false);
	EXPECT_FALSE(gptp_port_pub(&port)->as_capable) << "10.2.4.12 portEnabled: a link loss clears asCapable";
	EXPECT_EQ(gptp_port_role(&port), GPTP_ROLE_DISABLED);
	gptp_port_link(&port, true);
	EXPECT_FALSE(gptp_port_pub(&port)->as_capable) << "asCapable came back with the link before any exchange";
	EXPECT_NE(gptp_port_role(&port), GPTP_ROLE_MASTER) << "grandmaster again before any exchange";
}

// ---------------------------------------------------------------- BMCA, Announce

TEST_F(Scripted, NoAnnounceOrSyncBeforeAsCapable)
{
	// the grandmaster role only while asCapable (Milan v1.2 4.2.6; the plane's gate)
	start();
	tick(3000);
	EXPECT_TRUE(of_type(0xB).empty()) << "Announce before asCapable";
	EXPECT_TRUE(of_type(0x0).empty()) << "Sync before asCapable";
}

TEST_F(Scripted, BecomesGrandmasterAndSendsSyncFollowUpAnnounce)
{
	start();
	exchanges(2);
	ASSERT_EQ(gptp_port_role(&port), GPTP_ROLE_MASTER) << "10.3: no better master, so grandmaster";
	EXPECT_EQ(gptp_port_pub(&port)->gm_id, kClockA);
	EXPECT_TRUE(gptp_port_pub(&port)->sync_ok) << "becoming grandmaster sets the verdict";
	hal.sent[0].clear();
	for (unsigned i = 0; i < 100; i++) {
		tick(10);
		// every Sync gets its egress stamp at once
		auto s = of_type(0x0);
		if (!s.empty() && s.size() > of_type(0x8).size())
			gptp_port_ts(&port, true, 0x0, uint16_t(rd(s.back(), 44, 2)), 7'000'000'000ull + i, true);
	}
	auto syncs = of_type(0x0), fus = of_type(0x8), anns = of_type(0xB);
	EXPECT_EQ(syncs.size(), 8u) << "Milan v1.2 Table 4.1: Sync each 125 ms";
	ASSERT_EQ(fus.size(), syncs.size()) << "a Sync without its Follow_Up";
	EXPECT_EQ(syncs[0][20] & 0x02, 0x02) << "11.4.3: two-step Sync";
	EXPECT_EQ(int8_t(syncs[0][47]), -3);
	EXPECT_EQ(rd(fus[0], 44, 2), rd(syncs[0], 44, 2)) << "the Follow_Up's sequenceId is its Sync's";
	EXPECT_EQ(rd(fus[0], 16, 2), 76u) << "11.4.4: Follow_Up with its information TLV";
	EXPECT_EQ(rd(fus[0], 58, 2), 3u) << "11.4.4.3: ORGANIZATION_EXTENSION";
	EXPECT_EQ(rd(fus[0], 62, 3), 0x0080C2u);
	EXPECT_GE(get_ts(fus[0], 48), 7'000'000'000ull) << "preciseOriginTimestamp is not the Sync's egress stamp";
	EXPECT_EQ(anns.size(), 1u) << "Milan v1.2 Table 4.1: Announce each second";
	ASSERT_FALSE(anns.empty());
	EXPECT_EQ(rd(anns[0], 48 + 19, 8), kClockA) << "grandmasterIdentity";
	EXPECT_EQ(anns[0][48 + 13], 248) << "Milan v1.2 4.2.6.2.1: priority1 248";
	EXPECT_EQ(rd(anns[0], 14 + 64, 2), 8u) << "10.6.3.3: the path trace TLV";
	EXPECT_EQ(rd(anns[0], 14 + 68, 8), kClockA) << "the path trace holds thisClock";
}

TEST_F(Scripted, SyncIntervalHoldsTheTickGrain)
{
	start();
	exchanges(2);
	hal.sent[0].clear();
	std::vector<uint32_t> at;
	for (unsigned i = 0; i < 300; i++) {
		size_t n = of_type(0x0).size();
		tick(10);
		if (of_type(0x0).size() > n)
			at.push_back(now);
	}
	ASSERT_GE(at.size(), 3u);
	for (size_t i = 1; i < at.size(); i++)
		EXPECT_NEAR(double(at[i] - at[i - 1]), 125.0, 10.0) << "a Sync interval outside 125 ms +/- the tick";
}

TEST_F(Scripted, BetterAnnounceMakesASlave)
{
	start();
	exchanges(2);
	rx(announce(kClockB, 1, 100, 0xAAAAull, 0, {0xAAAAull}));
	EXPECT_EQ(gptp_port_role(&port), GPTP_ROLE_SLAVE) << "10.3.5: priority1 100 is better than 248";
	EXPECT_EQ(gptp_port_pub(&port)->gm_id, 0xAAAAull);
	EXPECT_EQ(gptp_port_pub(&port)->parent_id, kClockB);
	ASSERT_EQ(gptp_port_pub(&port)->path_count, 2u) << "10.3.9.23: the received path and thisClock";
	EXPECT_EQ(gptp_port_pub(&port)->path[0], 0xAAAAull);
	EXPECT_EQ(gptp_port_pub(&port)->path[1], kClockA);
	EXPECT_FALSE(gptp_port_pub(&port)->sync_ok) << "returning from grandmaster duty clears the verdict";
}

TEST_F(Scripted, WorseAnnounceKeepsTheGrandmaster)
{
	start();
	exchanges(2);
	rx(announce(kClockB, 1, 250, 0x1ull, 0));
	EXPECT_EQ(gptp_port_role(&port), GPTP_ROLE_MASTER) << "priority1 250 is worse than 248";
}

TEST_F(Scripted, LoopedPathAndStepsRemoved255AreDiscarded)
{
	start();
	exchanges(2);
	rx(announce(kClockB, 1, 100, 0xAAAAull, 0, {0xAAAAull, kClockA}));
	EXPECT_EQ(gptp_port_role(&port), GPTP_ROLE_MASTER) << "10.3.9.23: a path holding thisClock was used";
	rx(announce(kClockB, 2, 100, 0xAAAAull, 255));
	EXPECT_EQ(gptp_port_role(&port), GPTP_ROLE_MASTER) << "stepsRemoved 255 was used";
	EXPECT_EQ(port.ctr.ann_bad, 2u);
}

TEST_F(Scripted, AnnounceReceiptTimeoutAgesTheMaster)
{
	// 10.3.12, Milan v1.2 4.2.6.2.3 Table 4.2: announceReceiptTimeout 3, logMessageInterval 0
	start();
	exchanges(2);
	rx(announce(kClockB, 1, 100, 0xAAAAull, 0));
	ASSERT_EQ(gptp_port_role(&port), GPTP_ROLE_SLAVE);
	// keep complete pairs coming so only the Announce times out
	for (unsigned i = 0; i < 280; i++) {
		tick(10);
		if (i % 12 == 0) {
			uint64_t t = uint64_t(now) * 1'000'000ull;
			rx(sync_msg(kClockB, uint16_t(i)), true, t);
			rx(follow_up(kClockB, uint16_t(i), t - 500));
		}
		if (i % 100 == 99) {
			auto reqs = of_type(0x2);
			uint16_t seq = uint16_t(rd(reqs.back(), 44, 2));
			uint64_t t1 = uint64_t(now) * 1'000'000ull;
			gptp_port_ts(&port, true, 0x2, seq, t1, true);
			rx(pdelay_resp(kClockB, seq, t1 + 500, kClockA, false), true, t1 + 31'000);
			rx(pdelay_resp(kClockB, seq, t1 + 30'500, kClockA, true));
		}
	}
	EXPECT_EQ(gptp_port_role(&port), GPTP_ROLE_SLAVE) << "aged before 3 s";
	tick(300);
	EXPECT_EQ(gptp_port_role(&port), GPTP_ROLE_MASTER) << "not aged after 3 s without Announce";
}

TEST_F(Scripted, SyncReceiptTimeoutAgesTheGrandmaster)
{
	// Milan v1.2 4.2.6.2.3 Table 4.2: syncReceiptTimeout 375 ms
	start();
	exchanges(2);
	rx(announce(kClockB, 1, 100, 0xAAAAull, 0));
	rx(sync_msg(kClockB, 1), true, 10'000'000'000ull);
	rx(follow_up(kClockB, 1, 10'000'000'000ull - 500));
	ASSERT_EQ(gptp_port_role(&port), GPTP_ROLE_SLAVE);
	ASSERT_EQ(port.ctr.sync_used, 1u);
	tick(360);
	EXPECT_EQ(gptp_port_role(&port), GPTP_ROLE_SLAVE) << "aged before 375 ms";
	tick(30);
	EXPECT_EQ(gptp_port_role(&port), GPTP_ROLE_MASTER) << "no pair for 375 ms did not age the grandmaster";
}

// the selected master's port after one complete pair, then `n` Syncs 120 ms apart and no Follow_Up, each
// `announce_every`-th with an Announce; `seen` samples the port after each
template <typename See>
void sync_without_follow_up(Scripted &s, unsigned n, unsigned announce_every, See seen)
{
	s.exchanges(2);
	s.rx(announce(kClockB, 1, 100, 0xAAAAull, 0));
	uint64_t t = 10'000'000'000ull;
	s.rx(sync_msg(kClockB, 1), true, t);
	s.rx(follow_up(kClockB, 1, t - 500));
	ASSERT_EQ(s.port.ctr.sync_used, 1u);
	ASSERT_TRUE(gptp_port_pub(&s.port)->sync_ok);
	for (unsigned i = 1; i <= n; i++) {
		s.tick(120);
		s.rx(sync_msg(kClockB, uint16_t(1 + i)), true, t + 120'000'000ull * i);
		if (announce_every && i % announce_every == 0)
			s.rx(announce(kClockB, uint16_t(1 + i), 100, 0xAAAAull, 0));
		seen(i);
	}
	EXPECT_EQ(s.port.ctr.sync_used, 1u) << "a Sync without its Follow_Up was used";
	EXPECT_GE(s.port.ctr.rto_sync, 1u) << "Sync without Follow_Up held off the sync receipt timeout";
}

TEST_F(Scripted, SyncWithoutItsFollowUpLetsTheGrandmasterAge)
{
	// 10.2.8.2.1 c) sets syncReceiptTimeoutTime when synchronization information is delivered, which is a Sync
	// with its Follow_Up (11.2.14, Figure 10-4), never a Sync alone; Milan v1.2 4.2.6.2.3 Table 4.2 bounds the
	// timeout at 337.5 to 562.5 ms
	start();
	sync_without_follow_up(*this, 6, 0, [](unsigned) {});
	EXPECT_NE(gptp_port_role(&port), GPTP_ROLE_SLAVE) << "720 ms of Sync without Follow_Up kept the master";
}

TEST_F(Scripted, SyncWithoutItsFollowUpClearsTheVerdictOfAPortThatIsNeverGrandmaster)
{
	// ibid., priority1 255: the timeout clears the verdict (REQ-PTP-08: the loss reaches time validity)
	start(255);
	sync_without_follow_up(*this, 6, 0, [](unsigned) {});
	EXPECT_FALSE(gptp_port_pub(&port)->sync_ok) << "720 ms of Sync without Follow_Up kept the verdict";
}

TEST_F(Scripted, SyncAndAnnounceWithoutFollowUpNeverHoldTheVerdict)
{
	// ibid., with Announce still coming: the master stays selectable, so the port may return to it, but past
	// the timeout never with a verdict only a pair could give
	start();
	bool stale = false;
	sync_without_follow_up(*this, 16, 2, [&](unsigned i) {
		if (i >= 4)
			stale = stale || (gptp_port_role(&port) == GPTP_ROLE_SLAVE && port.pub.sync_ok);
	});
	EXPECT_FALSE(stale) << "Sync and Announce without Follow_Up kept a slave with the verdict past the timeout";
}

TEST_F(Scripted, FollowUpWithoutItsInformationTlvIsNoPair)
{
	// 11.4.4.1 Table 11-10, 11.4.4.2.2: a Follow_Up carries its information TLV first, from which 11.2.14.2.1
	// e) takes rateRatio. One without it, cut short or malformed is refused: no step, no trim, no verdict,
	// and no renewed sync receipt deadline
	start();
	exchanges(2);
	rx(announce(kClockB, 1, 100, 0xAAAAull, 0));
	const char *what[] = {"absent", "cut short", "of another type", "of another length", "of another organization",
			      "of another subtype"};
	uint64_t t = 10'000'000'000ull;
	for (unsigned k = 0; k < 6; k++) {
		uint16_t seq = uint16_t(10 + k);
		uint64_t at = t + 50'000'000ull * k;
		uint64_t origin = at - 500 - 50'000;   // 50 us: a used pair would step
		Bytes f = k == 0 ? follow_up_len(kClockB, seq, origin, 44)
			: k == 1 ? follow_up_len(kClockB, seq, origin, 60) : follow_up(kClockB, seq, origin);
		if (k == 2)
			be(f, 58, 0x0008, 2);
		if (k == 3)
			be(f, 60, 24, 2);
		if (k == 4)
			f[64] = 0xC3;
		if (k == 5)
			f[67] = 2;
		rx(sync_msg(kClockB, seq), true, at);
		rx(f);
		EXPECT_EQ(port.ctr.sync_used, 0u) << "a Follow_Up whose information TLV is " << what[k] << " was used";
		tick(50);
	}
	EXPECT_TRUE(hal.steps[0].empty() && hal.trim[0] == 0) << "a refused Follow_Up moved the PHC";
	tick(90);
	EXPECT_EQ(gptp_port_role(&port), GPTP_ROLE_MASTER) << "a refused Follow_Up renewed the sync receipt deadline";
}

TEST_F(Scripted, AFollowUpPastItsReceiptTimeoutIsNoPair)
{
	// Milan v1.2 4.2.6.2.3 Table 4.2: followUpReceiptTimeout 125 ms. A Sync whose Follow_Up has not come by then
	// is discarded on its own clock, whatever else arrives, so a late Follow_Up pairs with nothing
	start();
	exchanges(2);
	rx(announce(kClockB, 1, 100, 0xAAAAull, 0));
	uint64_t t = 10'000'000'000ull;
	rx(sync_msg(kClockB, 5), true, t);
	tick(130);
	EXPECT_EQ(port.ctr.fu_lost, 1u) << "a Sync waited past its followUpReceiptTimeout";
	rx(follow_up(kClockB, 5, t - 500));
	EXPECT_EQ(port.ctr.sync_used, 0u) << "a Follow_Up after its Sync's followUpReceiptTimeout was paired";
}

TEST_F(Scripted, FollowUpWithAFurtherTlvStillPairs)
{
	// 11.4.4.2.2: the information TLV is the first; a TLV after it is the message's own business
	start();
	exchanges(2);
	rx(announce(kClockB, 1, 100, 0xAAAAull, 0));
	uint64_t t = 10'000'000'000ull;
	Bytes f = follow_up(kClockB, 3, t - 500);
	f.resize(f.size() + 12, 0);
	be(f, 16, 76 + 12, 2);
	be(f, 14 + 76, 0x0003, 2);
	be(f, 14 + 78, 8, 2);
	rx(sync_msg(kClockB, 3), true, t);
	rx(f);
	EXPECT_EQ(port.ctr.sync_used, 1u) << "a Follow_Up with a TLV after its information TLV was refused";
}

TEST_F(Scripted, NotGrandmasterCapableOnlyClearsTheVerdict)
{
	// priority1 255: the port is never grandmaster; the timeout clears the verdict instead
	start(255);
	exchanges(2);
	EXPECT_EQ(gptp_port_role(&port), GPTP_ROLE_LISTENING) << "priority1 255 became grandmaster";
	tick(3000);
	EXPECT_TRUE(of_type(0xB).empty()) << "priority1 255 sent Announce";
}

// ---------------------------------------------------------------- slave and servo

TEST_F(Scripted, SyncFromAnotherPortIsIgnored)
{
	start();
	exchanges(2);
	rx(announce(kClockB, 1, 100, 0xAAAAull, 0));
	rx(sync_msg(0x5555ull, 1), true, 1'000'000);
	rx(follow_up(0x5555ull, 1, 1'000'000 - 200'000));
	EXPECT_TRUE(hal.steps[0].empty()) << "Sync and Follow_Up from a port that is not the master's were used";
	// another port's Sync between the master's Sync and its Follow_Up must not displace it
	uint64_t t = 30'000'000'000ull;
	rx(sync_msg(kClockB, 2), true, t);
	rx(sync_msg(0x5555ull, 2), true, t + 50'000);
	rx(follow_up(kClockB, 2, t - 500));
	EXPECT_TRUE(hal.steps[0].empty()) << "another port's Sync displaced the master's pending Sync";
}

TEST_F(Scripted, FirstPairStepsAtTheLinkUpThreshold)
{
	// gptp-processor #68: the first pair after asCapable rises steps over 20 us
	start();
	exchanges(2);
	rx(announce(kClockB, 1, 100, 0xAAAAull, 0));
	uint64_t t_rx = 10'000'000'000ull;
	rx(sync_msg(kClockB, 5), true, t_rx);
	rx(follow_up(kClockB, 5, t_rx - 500 - 20'001));   // local 20.001 us ahead
	ASSERT_EQ(hal.steps[0].size(), 1u) << "an offset over 20 us at link-up did not step";
	EXPECT_EQ(hal.steps[0][0], -20'001) << "the step is not the offset, negated";
	EXPECT_TRUE(gptp_port_pub(&port)->sync_ok) << "a consumed pair raises the verdict";
}

TEST_F(Scripted, LockedThresholdSlewsUnder100us)
{
	start();
	exchanges(2);
	rx(announce(kClockB, 1, 100, 0xAAAAull, 0));
	uint64_t t = 10'000'000'000ull;
	rx(sync_msg(kClockB, 1), true, t);
	rx(follow_up(kClockB, 1, t - 500));             // first pair, locks
	rx(sync_msg(kClockB, 2), true, t + 125'000'000);
	rx(follow_up(kClockB, 2, t + 125'000'000 - 500 - 99'999));
	EXPECT_TRUE(hal.steps[0].empty()) << "a locked offset of 99.999 us stepped";
	EXPECT_LT(hal.trim[0], 0) << "local ahead: the trim must slow it";
	rx(sync_msg(kClockB, 3), true, t + 250'000'000);
	rx(follow_up(kClockB, 3, t + 250'000'000 - 500 - 100'001));
	EXPECT_EQ(hal.steps[0].size(), 1u) << "a locked offset of 100.001 us did not step";
}

TEST_F(Scripted, FollowUpBeforeItsSyncStampStillPairs)
{
	start();
	exchanges(2);
	rx(announce(kClockB, 1, 100, 0xAAAAull, 0));
	rx(sync_msg(kClockB, 4));                         // the stamp is late
	rx(follow_up(kClockB, 4, 20'000'000'000ull - 500 - 50'000));
	EXPECT_TRUE(hal.steps[0].empty());
	gptp_port_ts(&port, false, 0x0, 4, 20'000'000'000ull, true);
	EXPECT_EQ(hal.steps[0].size(), 1u) << "a Sync stamp after its Follow_Up was never paired";
}

TEST_F(Scripted, TrimNeverLeavesTheEnvelope)
{
	start();
	exchanges(2);
	rx(announce(kClockB, 1, 100, 0xAAAAull, 0));
	uint64_t t = 10'000'000'000ull;
	for (unsigned i = 0; i < 40; i++, t += 125'000'000) {
		rx(sync_msg(kClockB, uint16_t(i)), true, t);
		rx(follow_up(kClockB, uint16_t(i), t - 500 + 99'000));   // local always 99 us behind
		EXPECT_LE(std::abs(hal.trim[0]), 67109) << "the trim left the 200 ppm envelope";
	}
}

// ---------------------------------------------------------------- the network: two ports, two PHCs

// A PHC: free-running at its own frequency error, trimmed in addend units and stepped
struct Phc {
	double ppm;            // its oscillator's error
	long double base_ns;   // its time at base_true
	long double base_true = 0;
	int32_t trim = 0;
	long double rate() const { return 1.0L + ppm * 1e-6L + (long double)trim * kClk / 16777216.0L / 1e9L; }
	long double at(long double t) const { return base_ns + (t - base_true) * rate(); }
	void rebase(long double t) { base_ns = at(t); base_true = t; }
};

struct Net : ::testing::Test {
	Hal hal;
	gptp_port port[2]{};
	Phc phc[2] = {{0.0, 0.0L}, {0.0, 0.0L}};
	long double true_ns = 0;
	uint32_t now = 0;
	int64_t delay_ns = 300;
	int jitter_ns = 0;             // each stamp off by a uniform +/-jitter_ns, the TSU's sampling phase
	uint32_t lcg = 12345u;
	int64_t jitter()
	{
		if (!jitter_ns)
			return 0;
		lcg = lcg * 1664525u + 1013904223u;
		return int64_t(lcg >> 8) % (2 * jitter_ns + 1) - jitter_ns;
	}
	std::vector<int32_t> pair_offsets;   // the slave port[1]'s offset at each consumed pair
	struct Wire { unsigned to; Bytes f; long double t_rx; };
	std::deque<Wire> wire;
	std::vector<double> offsets;   // B's time minus A's, sampled each tick, ns

	long double turn_ns = 0;       // a responder's turnaround: its Pdelay_Resp leaves this long after the request

	static Net *self;
	static bool send(void *, unsigned p, const uint8_t *f, unsigned len)
	{
		Net &n = *self;
		Bytes b(f, f + len);
		unsigned type = b[14] & 0x0F;
		bool event = type < 8;
		long double turn = (type == 0x3 || type == 0xA) ? n.turn_ns : 0.0L;
		long double t_tx = n.true_ns + 1000.0L * (n.wire.size() + 1) + turn;   // distinct instants inside the tick
		n.wire.push_back({1u - p, b, t_tx + n.delay_ns});
		if (event)
			n.tx_stamps.push_back({p, type, uint16_t(rd(b, 44, 2)), uint64_t(n.phc[p].at(t_tx) + n.jitter())});
		return true;
	}
	static void adjfine(void *, unsigned p, int32_t a)
	{
		self->phc[p].rebase(self->true_ns);
		self->phc[p].trim = a;
	}
	static void step(void *, unsigned p, int64_t d)
	{
		self->phc[p].rebase(self->true_ns);
		self->phc[p].base_ns += d;
	}
	struct TxStamp { unsigned port, type; uint16_t seq; uint64_t ns; };
	std::deque<TxStamp> tx_stamps;

	void SetUp() override { self = this; }
	void start(uint8_t p1a, uint8_t p1b)
	{
		gptp_hal h{this, send, adjfine, step};
		gptp_config ca = config(kClockA, p1a), cb = config(kClockB, p1b);
		gptp_port_init(&port[0], 0, &ca, &h, now);
		gptp_port_init(&port[1], 1, &cb, &h, now);
		gptp_port_link(&port[0], true);
		gptp_port_link(&port[1], true);
	}
	void deliver()
	{
		for (unsigned guard = 0; guard < 64 && (!wire.empty() || !tx_stamps.empty()); guard++) {
			while (!tx_stamps.empty()) {
				TxStamp s = tx_stamps.front();
				tx_stamps.pop_front();
				gptp_port_ts(&port[s.port], true, s.type, s.seq, s.ns, true);
			}
			if (!wire.empty()) {
				Wire w = wire.front();
				wire.pop_front();
				unsigned type = w.f[14] & 0x0F;
				if (type < 8)
					gptp_port_ts(&port[w.to], false, type, uint16_t(rd(w.f, 44, 2)),
						     uint64_t(phc[w.to].at(w.t_rx) + jitter()), true);
				gptp_port_rx(&port[w.to], w.f.data(), unsigned(w.f.size()));
			}
		}
	}
	void run(uint32_t ms)
	{
		for (uint32_t i = 0; i < ms; i += 10) {
			now += 10;
			true_ns += 10'000'000.0L;
			gptp_port_tick(&port[0], now);
			gptp_port_tick(&port[1], now);
			uint32_t used = port[1].ctr.sync_used;
			deliver();
			if (port[1].ctr.sync_used != used)
				pair_offsets.push_back(port[1].pub.offset_ns);
			offsets.push_back(double(phc[1].at(true_ns) - phc[0].at(true_ns)));
		}
	}
	// the first time after which every offset stays inside +/-band ns
	double lock_s(double band) const
	{
		size_t last_out = 0;
		for (size_t i = 0; i < offsets.size(); i++)
			if (std::fabs(offsets[i]) > band)
				last_out = i + 1;
		return last_out * 0.01;
	}
	// 30 s of A (the grandmaster, PHC at a_base) and B (its slave, at b_base) with a responder turnaround
	// `turn`: B steps to A on its first pair, which no exchange on either side may carry into a rate or a
	// delay (11.2.19.3.3, 11.2.19.3.4). Each port's asCapable holds from its first rising, and B keeps A.
	void step_across_the_link(long double a_base, long double b_base, long double turn)
	{
		turn_ns = turn;
		phc[0] = {+20.0, a_base};
		phc[1] = {-20.0, b_base};
		start(246, 248);
		bool rose[2] = {false, false};
		uint32_t down_ms[2] = {0, 0};
		bool follows = false;
		unsigned gm_changes = 0;
		for (uint32_t ms = 0; ms < 30'000; ms += 10) {
			run(10);
			for (unsigned i = 0; i < 2; i++) {
				rose[i] = rose[i] || port[i].pd.as_capable;
				if (rose[i] && !port[i].pd.as_capable)
					down_ms[i] += 10;
			}
			if (follows && port[1].pub.gm_id != kClockA)
				gm_changes++;
			follows = follows || port[1].pub.gm_id == kClockA;
		}
		EXPECT_GE(port[1].ctr.steps, 1u) << "the slave never stepped";
		EXPECT_EQ(down_ms[0], 0u) << "the grandmaster's port fell from asCapable across the slave's step";
		EXPECT_EQ(down_ms[1], 0u) << "the slave's port fell from asCapable across its own step";
		EXPECT_EQ(gm_changes, 0u) << "the slave left its grandmaster after it first followed it";
		EXPECT_EQ(gptp_port_role(&port[1]), GPTP_ROLE_SLAVE);
		double worst = 0;
		for (size_t i = offsets.size() - 500; i < offsets.size(); i++)
			worst = std::fmax(worst, std::fabs(offsets[i]));
		EXPECT_LT(worst, 100.0) << "the last 5 s left the 100 ns band";
	}
};
Net *Net::self;

// A step on either side of the link, at the turnarounds 802.1AS-2011 B.2.3 allows (10 ms) and this port's
// own order (1 ms), from a TAI-scale grandmaster and from offsets of 100 ms and 1 s both ways
TEST_F(Net, AStepAtTaiScaleKeepsAsCapableAt1msTurnaround)
{
	step_across_the_link(1'795'000'000'000'000'000.0L, 0.0L, 1e6L);
}

TEST_F(Net, AStepAtTaiScaleKeepsAsCapableAt10msTurnaround)
{
	step_across_the_link(1'795'000'000'000'000'000.0L, 0.0L, 1e7L);
}

TEST_F(Net, AStepOf100msKeepsAsCapableAt1msTurnaround)
{
	step_across_the_link(1'100'000'000.0L, 1'000'000'000.0L, 1e6L);
}

TEST_F(Net, AStepOf1sKeepsAsCapableAt10msTurnaround)
{
	step_across_the_link(2'000'000'000.0L, 1'000'000'000.0L, 1e7L);
}

TEST_F(Net, ABackwardStepOf100msKeepsAsCapableAt10msTurnaround)
{
	step_across_the_link(1'000'000'000.0L, 1'100'000'000.0L, 1e7L);
}

TEST_F(Net, SlaveLocksToTheGrandmaster)
{
	// NFR-TIME-01: within 1 us of the grandmaster; the fabric servo's 100 ns tracking band
	phc[0] = {+40.0, 1'000'000'000'000.0L};   // A, the grandmaster (priority1 246), 40 ppm fast
	phc[1] = {-35.0, 3'000'000.0L};           // B, 75 ppm from A and 1000 s behind
	start(246, 248);
	run(20'000);
	for (unsigned i = 0; i < 2; i++)
		std::printf("[ NET ] port %u role %d ann_rx %u ann_bad %u sync_rx %u used %u pd_done %u lost %u asCap %d rx %u bad %u\n", i,
			    int(port[i].role), port[i].ctr.ann_rx, port[i].ctr.ann_bad, port[i].ctr.sync_rx,
			    port[i].ctr.sync_used, port[i].ctr.pd_done, port[i].ctr.pd_lost, int(port[i].pd.as_capable),
			    port[i].ctr.rx, port[i].ctr.rx_bad);
	EXPECT_EQ(gptp_port_role(&port[0]), GPTP_ROLE_MASTER);
	EXPECT_EQ(gptp_port_role(&port[1]), GPTP_ROLE_SLAVE);
	EXPECT_EQ(gptp_port_pub(&port[1])->gm_id, kClockA);
	EXPECT_TRUE(gptp_port_pub(&port[1])->sync_ok);
	double lock = lock_s(100.0);
	EXPECT_LT(lock, 15.0) << "not inside 100 ns of the grandmaster by 15 s";
	double worst = 0;
	for (size_t i = offsets.size() - 500; i < offsets.size(); i++)
		worst = std::fmax(worst, std::fabs(offsets[i]));
	EXPECT_LT(worst, 100.0) << "the last 5 s left the 100 ns band";
	RecordProperty("lock_s", std::to_string(lock));
	std::printf("[ NET ] slave lock (100 ns band) at %.2f s, last 5 s worst |offset| %.1f ns, steps %u\n",
		    lock, worst, port[1].ctr.steps);
}

TEST_F(Net, LockTimeHoldsTheFabricBench)
{
	// tb/verilator/gptp_plane phase 4's claim on the engine this port replaces:
	// against a +100 ppm master 1 ms ahead, ONE re-base, the measured offset
	// under 150 ns by the 24th pair, the addend within 15 % of the +100 ppm ideal
	phc[0] = {+100.0, 1'001'000'000.0L};
	phc[1] = {0.0, 1'000'000'000.0L};
	jitter_ns = 10;
	start(246, 248);
	run(12'000);
	ASSERT_GE(pair_offsets.size(), 24u) << "fewer than 24 pairs consumed";
	EXPECT_EQ(port[1].ctr.steps, 1u) << "not ONE re-base";
	EXPECT_LT(std::abs(pair_offsets[23]), 150) << "the 24th pair's offset is not under 150 ns";
	int32_t ideal = gptp_addend_of_ppm(100, kClk);
	EXPECT_NEAR(double(phc[1].trim), double(ideal), 0.15 * ideal) << "the addend is not at the +100 ppm ideal";
	size_t first = 0;
	while (first < pair_offsets.size() && std::abs(pair_offsets[first]) >= 150)
		first++;
	std::printf("[ NET ] fabric-bench lock: pair 24 offset %d ns, first pair under 150 ns: %zu, addend %d (ideal %d)\n",
		    pair_offsets[23], first + 1, phc[1].trim, ideal);
	double worst = 0;
	for (size_t i = 40; i < pair_offsets.size(); i++)
		worst = std::fmax(worst, std::fabs(double(pair_offsets[i])));
	EXPECT_LT(worst, 60.0) << "tracking with +/-10 ns stamps left 60 ns";
	std::printf("[ NET ] tracking with +/-10 ns stamps, pairs 41..%zu: worst |offset| %.0f ns\n", pair_offsets.size(), worst);
}

TEST_F(Net, GrandmasterWinsByPriorityAndThePeerFollows)
{
	// the same network with the roles swapped by priority1: this firmware as grandmaster
	phc[0] = {-20.0, 5'000'000.0L};
	phc[1] = {+60.0, 2'000'000'000'000.0L};
	start(248, 246);
	run(20'000);
	EXPECT_EQ(gptp_port_role(&port[1]), GPTP_ROLE_MASTER);
	EXPECT_EQ(gptp_port_role(&port[0]), GPTP_ROLE_SLAVE);
	EXPECT_LT(lock_s(100.0), 15.0);
}

TEST_F(Net, BothSeeTheLinkDelay)
{
	delay_ns = 650;
	phc[0] = {+10.0, 0.0L};
	phc[1] = {-10.0, 0.0L};
	start(246, 248);
	run(8'000);
	EXPECT_NEAR(gptp_port_pub(&port[0])->pdelay_ns, 650, 3) << "the grandmaster's peer delay";
	EXPECT_NEAR(gptp_port_pub(&port[1])->pdelay_ns, 650, 3) << "the slave's peer delay";
	EXPECT_TRUE(gptp_port_pub(&port[0])->as_capable && gptp_port_pub(&port[1])->as_capable);
}

TEST_F(Net, GrandmasterFailoverThroughSyncLapse)
{
	// the grandmaster's link goes; the slave ages it after 375 ms and becomes grandmaster
	phc[0] = {+5.0, 0.0L};
	phc[1] = {-5.0, 0.0L};
	start(246, 248);
	run(8'000);
	ASSERT_EQ(gptp_port_role(&port[1]), GPTP_ROLE_SLAVE);
	gptp_port_link(&port[0], false);   // A stops sending; B's link stays up
	run(500);
	EXPECT_EQ(gptp_port_role(&port[1]), GPTP_ROLE_MASTER) << "the slave did not take over after the Sync lapse";
}

}  // namespace

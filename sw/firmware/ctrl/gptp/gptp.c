// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// gptp.c - the IEEE 802.1AS-2020 end station port (gptp.h; #665 F6, #884).
// Clause numbers are IEEE 802.1AS-2020's unless named otherwise.

#include "gptp.h"

#include <string.h>

// ---- byte order: every wire field is big-endian (10.6.1) ----
static void put16(uint8_t *a, uint16_t v)
{
	a[0] = (uint8_t)(v >> 8);
	a[1] = (uint8_t)v;
}

static void put32(uint8_t *a, uint32_t v)
{
	put16(a, (uint16_t)(v >> 16));
	put16(a + 2, (uint16_t)v);
}

static void put64(uint8_t *a, uint64_t v)
{
	put32(a, (uint32_t)(v >> 32));
	put32(a + 4, (uint32_t)v);
}

static uint16_t get16(const uint8_t *a)
{
	return (uint16_t)((a[0] << 8) | a[1]);
}

static uint32_t get32(const uint8_t *a)
{
	return ((uint32_t)get16(a) << 16) | get16(a + 2);
}

static uint64_t get64(const uint8_t *a)
{
	return ((uint64_t)get32(a) << 32) | get32(a + 4);
}

#define NS_PER_S 1000000000ull

// A 64-bit quotient by shift and subtract. The split hart (RV32IM) has no 64-bit
// divide and the split image refuses libgcc's (#665: ctrl_srp_image.py's object
// audit), so the port divides 64 bits only here, and only on its slow paths: a
// wire timestamp, a completed exchange, a lock, a change of Sync interval.
static uint64_t udiv64(uint64_t n, uint64_t d)
{
	uint64_t q = 0, r = 0;
	for (int i = 63; i >= 0; i--) {
		r = (r << 1) | ((n >> i) & 1u);
		if (r >= d) {
			r -= d;
			q |= 1ull << i;
		}
	}
	return q;
}

static int64_t sdiv64(int64_t n, int64_t d)
{
	uint64_t q = udiv64(n < 0 ? 0u - (uint64_t)n : (uint64_t)n, d < 0 ? 0u - (uint64_t)d : (uint64_t)d);
	return ((n < 0) != (d < 0)) ? -(int64_t)q : (int64_t)q;
}

// Timestamp (10.6.2.4 via 6.4.3.4): 48-bit seconds, then 32-bit nanoseconds
void gptp_ts_put(uint8_t *at, uint64_t ns)
{
	uint64_t s = udiv64(ns, NS_PER_S);
	put16(at, (uint16_t)(s >> 32));
	put32(at + 2, (uint32_t)s);
	put32(at + 6, (uint32_t)(ns - s * NS_PER_S));
}

uint64_t gptp_ts_get(const uint8_t *at)
{
	uint64_t s = ((uint64_t)get16(at) << 32) | get32(at + 2);
	return s * NS_PER_S + get32(at + 6);
}

int32_t gptp_addend_of_ppm(int32_t ppm, uint32_t clk_hz)
{
	// ppm of relative frequency is ppm * 2^24 * 1000 / clk_hz addend units, the
	// expression the fabric engine's integrator clamp and KL_gptp_txret's
	// envelope both use, rounded half up
	uint64_t num = (uint64_t)(ppm < 0 ? -ppm : ppm) * (1ull << 24) * 1000u + clk_hz / 2u;
	int32_t u = (int32_t)udiv64(num, clk_hz);
	return ppm < 0 ? -u : u;
}

// ---- the common header (10.6.2) and its frame ----
// offsets inside a frame: the header starts after the 14-byte Ethernet header
#define F_TYPE 14u           // majorSdoId (4) | messageType (4)
#define F_VER 15u            // minorVersionPTP (4) | versionPTP (4)
#define F_LEN 16u
#define F_DOMAIN 18u
#define F_FLAGS 20u
#define F_CORR 22u
#define F_SRC 34u            // sourcePortIdentity: clockIdentity (8), portNumber (2)
#define F_SEQ 44u
#define F_CTRL 46u
#define F_LOGI 47u
#define F_BODY 48u

// message lengths, PTP octets (11.4.2 to 11.4.6, 10.6.3)
#define LEN_SYNC 44u
#define LEN_FU 76u           // with the Follow_Up information TLV (11.4.4.3)
#define LEN_PDELAY 54u       // Pdelay_Req, Pdelay_Resp, Pdelay_Resp_Follow_Up
#define LEN_ANNOUNCE 64u     // without the path trace TLV

static const uint8_t DA_GPTP[6] = {0x01, 0x80, 0xC2, 0x00, 0x00, 0x0E};  // 11.3.4 Table 11-3

bool gptp_frame_key(const uint8_t *frame, unsigned len, unsigned *msg_type, uint16_t *seq)
{
	if (len < F_BODY || get16(frame + 12) != GPTP_ETHERTYPE)
		return false;
	*msg_type = frame[F_TYPE] & 0x0Fu;
	*seq = get16(frame + F_SEQ);
	return true;
}

static void own_port_id(const struct gptp_port *p, uint8_t *at)
{
	put64(at, p->cfg.clock_id);
	put16(at + 8, 1u);   // a one-port end station: portNumber 1 (8.5.2.3)
}

static unsigned header(struct gptp_port *p, unsigned type, unsigned ptp_len, uint16_t seq,
		       uint8_t control, int8_t log_interval, uint8_t flags0, uint8_t flags1)
{
	uint8_t *f = p->tx;
	memset(f, 0, GPTP_ETH_BYTES + ptp_len);
	memcpy(f, DA_GPTP, 6);
	memcpy(f + 6, p->cfg.mac, 6);
	put16(f + 12, GPTP_ETHERTYPE);
	f[F_TYPE] = (uint8_t)(0x10u | type);       // majorSdoId 1 (10.6.2.2.1)
	f[F_VER] = 0x12u;                          // minorVersionPTP 1, versionPTP 2 (10.6.2.2.3, 10.6.2.2.4)
	put16(f + F_LEN, (uint16_t)ptp_len);
	f[F_FLAGS] = flags0;
	f[F_FLAGS + 1] = flags1;
	own_port_id(p, f + F_SRC);
	put16(f + F_SEQ, seq);
	f[F_CTRL] = control;
	f[F_LOGI] = (uint8_t)log_interval;
	return GPTP_ETH_BYTES + ptp_len;
}

static bool send(struct gptp_port *p, unsigned len)
{
	if (!p->hal.send(p->hal.ctx, p->index, p->tx, len)) {
		p->ctr.tx_full++;
		return false;
	}
	p->ctr.tx++;
	return true;
}

#define FLAG0_TWO_STEP 0x02u
#define FLAG1_PTP_TIMESCALE 0x08u

// ---- publication ----
static void pub_set_gm(struct gptp_port *p, uint64_t gm, uint64_t parent)
{
	if (p->pub.gm_id != gm) {
		p->pub.gm_id = gm;
		p->pub.disc++;
		p->pub.sync_ok = false;   // a grandmaster change clears the verdict until a pair is consumed
		p->pub_dirty = true;
	}
	if (p->pub.parent_id != parent) {
		p->pub.parent_id = parent;
		p->pub_dirty = true;
	}
}

static void pub_set_path(struct gptp_port *p, const uint64_t *path, unsigned n)
{
	if (n > GPTP_PATH_MAX)
		n = GPTP_PATH_MAX;
	if (p->pub.path_count == n && !memcmp(p->pub.path, path, n * sizeof *path))
		return;
	p->pub.path_count = (uint8_t)n;
	memset(p->pub.path, 0, sizeof p->pub.path);
	memcpy(p->pub.path, path, n * sizeof *path);
	p->pub.path_gen++;
	p->pub_dirty = true;
}

static void pub_set_flags(struct gptp_port *p, bool as_capable, bool sync_ok)
{
	if (p->pub.as_capable != as_capable || p->pub.sync_ok != sync_ok) {
		p->pub.as_capable = as_capable;
		p->pub.sync_ok = sync_ok;
		p->pub_dirty = true;
	}
}

// ---- the BMCA of a one-port end station (10.3) ----
// The priority vector's systemIdentity (10.3.2) then stepsRemoved, compared
// octet by octet as one big-endian string: smaller is better (10.3.4, 10.3.5).
static void vector_own(const struct gptp_port *p, struct gptp_vector *v)
{
	uint8_t *k = v->key;
	k[0] = p->cfg.priority1;
	k[1] = GPTP_CLOCK_CLASS;
	k[2] = GPTP_CLOCK_ACCURACY;
	put16(k + 3, GPTP_CLOCK_VARIANCE);
	k[5] = p->cfg.priority2;
	put64(k + 6, p->cfg.clock_id);
	put16(k + 14, 0);
	memset(k + 16, 0, sizeof v->key - 16);
	own_port_id(p, v->src);
}

static int vector_cmp(const struct gptp_vector *a, const struct gptp_vector *b)
{
	int c = memcmp(a->key, b->key, 16);
	return c ? c : memcmp(a->src, b->src, sizeof a->src);
}

static void as_capable_set(struct gptp_port *p, bool v);

static void become(struct gptp_port *p, enum gptp_role role)
{
	enum gptp_role was = p->role;
	p->role = role;
	if (role == GPTP_ROLE_MASTER && was != GPTP_ROLE_MASTER) {
		p->mst.next_sync_ms = p->now_ms;   // the first Sync and Announce at once
		p->mst.next_ann_ms = p->now_ms;
		p->mst.fu_owed = false;
	}
	if (role == GPTP_ROLE_SLAVE && was != GPTP_ROLE_SLAVE)
		p->slv.last_ms = p->now_ms;   // the sync receipt timer starts with the new master
	if (role != GPTP_ROLE_SLAVE)
		p->slv.have = false;
}

static void bmca(struct gptp_port *p)
{
	struct gptp_vector own;
	vector_own(p, &own);
	if (!p->link || !p->pd.as_capable) {
		become(p, GPTP_ROLE_DISABLED);
		pub_set_gm(p, 0, 0);
		pub_set_path(p, NULL, 0);
		pub_set_flags(p, false, false);
		return;
	}
	if (p->ann.valid && vector_cmp(&p->ann.v, &own) < 0) {
		bool was_master = p->role == GPTP_ROLE_MASTER;
		uint64_t path[GPTP_PATH_MAX];
		unsigned n = p->ann.path_count;
		memcpy(path, p->ann.path, n * sizeof *path);
		if (n < GPTP_PATH_MAX)
			path[n++] = p->cfg.clock_id;   // thisClock appended (10.3.9.23)
		become(p, GPTP_ROLE_SLAVE);
		pub_set_gm(p, get64(p->ann.v.key + 6), get64(p->ann.v.src));
		pub_set_path(p, path, n);
		// returning from grandmaster duty clears the verdict until a pair
		pub_set_flags(p, true, was_master ? false : p->pub.sync_ok);
		return;
	}
	if (p->cfg.priority1 != 255u) {
		uint64_t path = p->cfg.clock_id;
		become(p, GPTP_ROLE_MASTER);
		if (p->pub.slew) {
			p->pub.slew = false;   // becoming grandmaster completes any correction (gptp-processor #75)
			p->pub_dirty = true;
		}
		pub_set_gm(p, p->cfg.clock_id, p->cfg.clock_id);
		pub_set_path(p, &path, 1);
		pub_set_flags(p, true, true);   // becoming grandmaster sets the verdict
		return;
	}
	become(p, GPTP_ROLE_LISTENING);
	pub_set_gm(p, 0, 0);
	pub_set_path(p, NULL, 0);
	pub_set_flags(p, true, false);
}

static void as_capable_set(struct gptp_port *p, bool v)
{
	if (p->pd.as_capable == v)
		return;
	p->pd.as_capable = v;
	if (v)
		p->srv.linkup = true;   // the first pair after asCapable rises uses the link-up threshold
	bmca(p);
}

// ---- peer delay initiator (11.2.19) ----
static void pd_lost(struct gptp_port *p)
{
	p->ctr.pd_lost++;
	p->pd.good = 0;
	// Figure 11-8 as the fabric engine reads it: the fifth consecutive lost response clears asCapable
	if (p->pd.lost <= GPTP_LOST_ALLOWED)
		p->pd.lost++;
	else
		as_capable_set(p, false);
}

static void pd_send(struct gptp_port *p)
{
	unsigned len;
	if (p->pd.in_flight)
		pd_lost(p);   // the request before it was not answered within its interval
	p->pd.in_flight = false;
	if (!p->link || p->pd.ceased)
		return;
	p->pd.seq++;
	len = header(p, GPTP_MSG_PDELAY_REQ, LEN_PDELAY, p->pd.seq, 5u, 0, 0, 0);
	if (!send(p, len))
		return;
	p->pd.in_flight = true;
	p->pd.t1_ok = p->pd.resp_ok = p->pd.fu_ok = p->pd.t4_ok = p->pd.multi = false;
	p->pd.sent_ms = p->now_ms;
}

static int32_t median3(const int32_t *d, unsigned n)
{
	if (n < 3)
		return d[n - 1];
	int32_t a = d[0], b = d[1], c = d[2];
	if ((a <= b && b <= c) || (c <= b && b <= a))
		return b;
	if ((b <= a && a <= c) || (c <= a && a <= b))
		return a;
	return c;
}

static void pd_complete(struct gptp_port *p)
{
	uint64_t rtt, turn;
	int64_t d;
	p->pd.in_flight = false;
	p->pd.done_seq = p->pd.seq;
	memcpy(p->pd.done_responder, p->pd.responder, sizeof p->pd.responder);
	if (p->pd.multi) {
		// more than one responder: Milan v1.2 4.2.6.2.5 ceases the requests after the third in a row
		p->ctr.pd_multi++;
		p->pd.good = 0;
		as_capable_set(p, false);
		if (++p->pd.multi_run >= GPTP_CEASE_N) {
			p->pd.ceased = true;
			p->pd.cease_end_ms = p->now_ms + GPTP_CEASE_MS;
		}
		return;
	}
	p->pd.multi_run = 0;
	if (p->pd.t4 < p->pd.t1 || p->pd.t4 - p->pd.t1 > GPTP_PD_LATE_NS) {
		p->ctr.pd_late++;
		pd_lost(p);
		return;
	}
	// neighborRateRatio (11.2.19.3.3): the responder's elapsed time over ours,
	// across the oldest exchange the window still holds
	{
		unsigned h = p->pd.w_head;
		p->pd.w3[h] = p->pd.t3;
		p->pd.w4[h] = p->pd.t4;
		p->pd.w_head = (uint8_t)((h + 1u) % GPTP_NRR_WINDOW);
		if (p->pd.w_n < GPTP_NRR_WINDOW)
			p->pd.w_n++;
		if (p->pd.w_n >= 2u) {
			unsigned o = (p->pd.w_n < GPTP_NRR_WINDOW) ? 0u : p->pd.w_head;
			int64_t d3 = (int64_t)(p->pd.t3 - p->pd.w3[o]);
			int64_t d4 = (int64_t)(p->pd.t4 - p->pd.w4[o]);
			if (d4 > 0 && d3 > 0) {
				int64_t q = sdiv64((d3 - d4) * (int64_t)(1ll << 32), d4);
				p->pd.nrr_q32 = (int32_t)q;
				p->pd.nrr_ok = true;
			}
		}
	}
	// neighborPropDelay (11.2.19.3.4): ((t4 - t1) * neighborRateRatio - (t3 - t2)) / 2
	rtt = p->pd.t4 - p->pd.t1;
	turn = p->pd.t3 - p->pd.t2;
	d = (int64_t)rtt + (((int64_t)rtt * p->pd.nrr_q32) >> 32) - (int64_t)turn;
	d = (d < 0) ? -((-d) >> 1) : (d >> 1);   // halved toward zero, no divide
	if (p->pd.d_n < 3u) {
		p->pd.d[p->pd.d_n++] = (int32_t)d;
	} else {
		p->pd.d[0] = p->pd.d[1];
		p->pd.d[1] = p->pd.d[2];
		p->pd.d[2] = (int32_t)d;
	}
	p->pd.delay_ns = median3(p->pd.d, p->pd.d_n);
	if (p->pub.pdelay_ns != p->pd.delay_ns) {
		p->pub.pdelay_ns = p->pd.delay_ns;
		p->pub_dirty = true;
	}
	p->ctr.pd_done++;
	p->pd.lost = 0;
	if (p->pd.delay_ns > GPTP_NPD_HI_NS || p->pd.delay_ns < GPTP_NPD_LO_NS) {
		p->pd.good = 0;   // outside neighborPropDelayThresh: not asCapable (11.2.2)
		as_capable_set(p, false);
		return;
	}
	if (p->pd.good < 255u)
		p->pd.good++;
	if (p->pd.good >= GPTP_ASCAP_UP && p->pd.nrr_ok)
		as_capable_set(p, true);
}

static void pd_try_complete(struct gptp_port *p)
{
	if (p->pd.in_flight && p->pd.t1_ok && p->pd.resp_ok && p->pd.fu_ok && p->pd.t4_ok)
		pd_complete(p);
}

// ---- ingress timestamps that came before their frame, and the reverse ----
// The fabric posts a stamp and commits its frame on two paths (the event
// ring and the gptp receive ring), so either may be read first. A stamp is
// kept by (messageType, sequenceId) until its frame takes it; the four
// newest are kept.
#define RX_STAMPS 4u

static bool stamp_take(struct gptp_port *p, unsigned type, uint16_t seq, uint64_t *ns)
{
	unsigned i;
	for (i = 0; i < RX_STAMPS; i++) {
		if (p->stamps.used[i] && p->stamps.type[i] == type && p->stamps.seq[i] == seq) {
			p->stamps.used[i] = false;
			*ns = p->stamps.ns[i];
			return true;
		}
	}
	return false;
}

static void stamp_keep(struct gptp_port *p, unsigned type, uint16_t seq, uint64_t ns)
{
	unsigned i = p->stamps.next;
	p->stamps.next = (uint8_t)((i + 1u) % RX_STAMPS);
	p->stamps.used[i] = true;
	p->stamps.type[i] = (uint8_t)type;
	p->stamps.seq[i] = seq;
	p->stamps.ns[i] = ns;
}

// ---- the servo (the fabric engine's policy, gptp-processor #68 and #75) ----
// A PI loop on the offset, one update a pair. With g the offset an addend
// unit moves in one Sync interval (the interval's PHC ticks times 2^-24 ns),
// an update u = -(Kp + Ki) o_k - Ki S_(k-1) gives the offset the recurrence
// o_(k+2) = (2 - g Kp - g Ki) o_(k+1) - (1 - g Kp) o_k, whose two roots are
// put together at 0.6 (g Kp = 1 - 0.6^2, g Ki = (1 - 0.6)^2): a phase or rate
// error falls to under 1e-3 of itself in twenty pairs, inside the fabric
// bench's lock test (tb/verilator/gptp_plane phase 4: under 150 ns by the
// 24th pair from 1 ms and 100 ppm). Both gains are Q16, derived from the
// PHC's clock and the master's Sync interval, never written down.
#define GKP_Q16 41943    // 0.64 in Q16
#define GKI_Q16 10486    // 0.16 in Q16

static int64_t clamp64(int64_t v, int64_t lim)
{
	return v > lim ? lim : (v < -lim ? -lim : v);
}

static void servo_pair(struct gptp_port *p, uint64_t t_rx, uint64_t gm_rx, int8_t log_sync)
{
	int64_t offset = (int64_t)(t_rx - gm_rx);     // local time minus grandmaster time
	// the interval's PHC ticks: 2^log_sync s at cfg.phc_clk_hz, log_sync held to Milan's -3 and its neighbours
	int64_t ticks = (int64_t)p->cfg.phc_clk_hz;
	int64_t kp, ki;
	if (log_sync < -5)
		log_sync = -5;
	if (log_sync > 0)
		log_sync = 0;
	ticks >>= -log_sync;
	if (!p->srv.gains_ok || p->srv.gains_log != log_sync) {
		p->srv.kp = sdiv64((int64_t)GKP_Q16 << 24, ticks);
		p->srv.ki = sdiv64((int64_t)GKI_Q16 << 24, ticks);
		p->srv.gains_log = log_sync;
		p->srv.gains_ok = true;
	}
	kp = p->srv.kp;
	ki = p->srv.ki;
	int64_t thresh = p->srv.linkup ? GPTP_STEP_LINKUP_NS : GPTP_STEP_LOCKED_NS;
	int64_t lim = (int64_t)p->adj_max;
	p->ctr.sync_used++;
	p->pub.offset_ns = (int32_t)offset;
	p->srv.linkup = false;   // every consumed pair locks the servo
	if (offset > thresh || offset < -thresh) {
		// a step starts no slew and holds one in progress (gptp-processor #75)
		p->hal.phc_step(p->hal.ctx, p->index, -offset);
		p->ctr.steps++;
		p->pub.disc++;
		p->srv.have_prev = false;   // the rate across a step is not the clock's
		p->srv.seeded = false;
		p->pub_dirty = true;
		pub_set_flags(p, p->pd.as_capable, true);
		return;
	}
	if (p->srv.have_prev && !p->srv.seeded) {
		// the second pair after a step seeds the integrator with the measured
		// frequency error, so lock does not wait for the integral to find it:
		// the clock ran at its own error plus the trim applied, so the trim
		// that cancels its own error is the applied one less the measured one
		int64_t dl = (int64_t)(t_rx - p->srv.prev_rx), dg = (int64_t)(gm_rx - p->srv.prev_gm);
		if (dg > 0 && dl - dg < dg && dg - dl < dg) {
			int64_t q32 = sdiv64((dl - dg) * (int64_t)(1ll << 32), dg);   // local fast by q32 * 2^-32
			int64_t u = sdiv64(q32 * 1000000000ll, (int64_t)p->cfg.phc_clk_hz * 256);
			p->srv.integ = clamp64((int64_t)p->srv.trim - u, lim) * 65536;
			p->srv.seeded = true;
		}
	}
	// the slew-active level (gptp-processor #75): an outside-band pair starts or
	// continues a correction, two consecutive pairs inside the band complete it
	if (offset > GPTP_SLEW_SETTLED_NS || offset < -GPTP_SLEW_SETTLED_NS) {
		p->srv.in_band = 0;
		if (!p->pub.slew) {
			p->pub.slew = true;
			p->pub_dirty = true;
		}
	} else if (p->pub.slew && ++p->srv.in_band >= 2u) {
		p->pub.slew = false;
		p->pub_dirty = true;
	}
	p->srv.prev_rx = t_rx;
	p->srv.prev_gm = gm_rx;
	p->srv.have_prev = true;
	p->srv.integ = clamp64(p->srv.integ - ki * offset, lim * 65536);
	p->srv.trim = (int32_t)clamp64((p->srv.integ - kp * offset) >> 16, lim);
	p->hal.phc_adjfine(p->hal.ctx, p->index, p->srv.trim);
	p->pub_dirty = true;
	pub_set_flags(p, p->pd.as_capable, true);
}

static void slave_try_pair(struct gptp_port *p)
{
	uint64_t gm_rx;
	int64_t pd;
	if (!p->slv.have || !p->slv.have_ts || !p->slv.fu_early)
		return;
	// syncReceiptTime (10.2.9): preciseOriginTimestamp + correction +
	// neighborPropDelay * (rateRatio / neighborRateRatio); that ratio is the
	// grandmaster's cumulativeScaledRateOffset (11.4.4.3.6), in 2^-32 units here
	pd = p->pd.delay_ns;
	gm_rx = p->slv.fu_origin + (uint64_t)p->slv.fu_corr_ns + (uint64_t)(pd + ((pd * p->slv.fu_csro_q32) >> 32));
	p->slv.have = false;
	p->slv.fu_early = false;
	servo_pair(p, p->slv.t_rx, gm_rx, p->slv.log_sync);
}

// ---- receive ----
static bool from_self(const struct gptp_port *p, const uint8_t *f)
{
	return get64(f + F_SRC) == p->cfg.clock_id;
}

static void rx_announce(struct gptp_port *p, const uint8_t *f, unsigned plen)
{
	struct gptp_vector v;
	const uint8_t *b = f + F_BODY;
	unsigned n = 0, i;
	uint64_t path[GPTP_PATH_MAX];
	uint16_t steps;
	int8_t logi = (int8_t)f[F_LOGI];
	if (plen < LEN_ANNOUNCE) {
		p->ctr.ann_bad++;
		return;
	}
	steps = get16(b + 27);
	if (steps >= 255u) {   // 10.3.9.4 (as Figure 10-13 discards it)
		p->ctr.ann_bad++;
		return;
	}
	// the path trace TLV (10.6.3.3): a looped path is discarded (10.3.9.23)
	if (plen >= LEN_ANNOUNCE + 4u && get16(f + GPTP_ETH_BYTES + LEN_ANNOUNCE) == 0x0008u) {
		unsigned tlen = get16(f + GPTP_ETH_BYTES + LEN_ANNOUNCE + 2u);
		unsigned cnt = tlen / 8u;
		const uint8_t *e = f + GPTP_ETH_BYTES + LEN_ANNOUNCE + 4u;
		if (LEN_ANNOUNCE + 4u + tlen > plen) {
			p->ctr.ann_bad++;
			return;
		}
		for (i = 0; i < cnt; i++) {
			uint64_t id = get64(e + 8u * i);
			if (id == p->cfg.clock_id) {
				p->ctr.ann_bad++;
				return;
			}
			if (n < GPTP_PATH_MAX)
				path[n++] = id;
		}
	}
	p->ctr.ann_rx++;
	v.key[0] = b[13];                  // grandmasterPriority1
	memcpy(v.key + 1, b + 14, 4);      // grandmasterClockQuality
	v.key[5] = b[18];                  // grandmasterPriority2
	memcpy(v.key + 6, b + 19, 8);      // grandmasterIdentity
	put16(v.key + 14, (uint16_t)(steps + 1u));   // as this port would hold it
	memset(v.key + 16, 0, sizeof v.key - 16);
	memcpy(v.src, f + F_SRC, 10);
	if (get64(v.key + 6) == p->cfg.clock_id) {   // our own grandmastership come back
		p->ctr.ann_bad++;
		return;
	}
	if (!p->ann.valid || !memcmp(p->ann.v.src, v.src, 10) || vector_cmp(&v, &p->ann.v) < 0) {
		uint32_t ivl_ms;
		if (logi < -3)
			logi = -3;
		if (logi > 4)
			logi = 4;
		ivl_ms = logi >= 0 ? (1000u << logi) : (1000u >> -logi);
		p->ann.valid = true;
		p->ann.v = v;
		p->ann.expire_ms = p->now_ms + GPTP_ANNOUNCE_RTO * ivl_ms;
		p->ann.path_count = (uint8_t)n;
		memcpy(p->ann.path, path, n * sizeof *path);
		p->ann.log_announce = logi;
		bmca(p);
	}
}

static void rx_sync(struct gptp_port *p, const uint8_t *f, uint16_t seq)
{
	uint64_t ns;
	if (p->role != GPTP_ROLE_SLAVE || memcmp(f + F_SRC, p->ann.v.src, 10))
		return;   // Sync only from the selected master's port
	p->ctr.sync_rx++;
	p->slv.have = true;
	p->slv.seq = seq;
	p->slv.fu_early = false;
	p->slv.rx_ms = p->now_ms;
	p->slv.last_ms = p->now_ms;   // the sync receipt timer restarts on each Sync
	p->slv.have_ts = stamp_take(p, GPTP_MSG_SYNC, seq, &ns);
	if (p->slv.have_ts)
		p->slv.t_rx = ns;
	p->slv.fu_corr_ns = (int64_t)get64(f + F_CORR) >> 16;
	p->slv.log_sync = (int8_t)f[F_LOGI];
}

static void rx_follow_up(struct gptp_port *p, const uint8_t *f, unsigned plen, uint16_t seq)
{
	const uint8_t *tlv = f + F_BODY + 10;
	if (p->role != GPTP_ROLE_SLAVE || !p->slv.have || p->slv.seq != seq ||
	    memcmp(f + F_SRC, p->ann.v.src, 10))
		return;
	p->slv.fu_origin = gptp_ts_get(f + F_BODY);
	p->slv.fu_corr_ns += (int64_t)get64(f + F_CORR) >> 16;
	p->slv.fu_csro_q32 = 0;
	if (plen >= LEN_FU && get16(tlv) == 0x0003u && get16(tlv + 2) == 28u &&
	    tlv[4] == 0x00 && tlv[5] == 0x80 && tlv[6] == 0xC2 && get16(tlv + 7) == 0 && tlv[9] == 1u)
		p->slv.fu_csro_q32 = (int32_t)get32(tlv + 10) >> 9;   // 2^-41 to 2^-32 units
	p->slv.fu_early = true;
	slave_try_pair(p);
}

static void rx_pdelay_req(struct gptp_port *p, const uint8_t *f, uint16_t seq)
{
	uint64_t ns;
	// a new request replaces one still owed: the responder answers the latest
	p->rsp.resp_owed = true;
	p->rsp.fu_owed = false;
	p->rsp.seq = seq;
	memcpy(p->rsp.requester, f + F_SRC, 10);
	p->rsp.sent_ms = p->now_ms;
	p->rsp.t2_ok = stamp_take(p, GPTP_MSG_PDELAY_REQ, seq, &ns);
	if (p->rsp.t2_ok)
		p->rsp.t2 = ns;
}

static void rsp_send_resp(struct gptp_port *p)
{
	unsigned len;
	if (!p->rsp.resp_owed || !p->rsp.t2_ok)
		return;
	len = header(p, GPTP_MSG_PDELAY_RESP, LEN_PDELAY, p->rsp.seq, 5u, 0x7F, FLAG0_TWO_STEP, 0);
	gptp_ts_put(p->tx + F_BODY, p->rsp.t2);          // requestReceiptTimestamp
	memcpy(p->tx + F_BODY + 10, p->rsp.requester, 10);   // requestingPortIdentity
	p->rsp.resp_owed = false;
	if (send(p, len)) {
		p->rsp.fu_owed = true;
		p->rsp.sent_ms = p->now_ms;
		p->ctr.pd_resp++;
	}
}

static void rx_pdelay_resp(struct gptp_port *p, const uint8_t *f, uint16_t seq, bool fu)
{
	const uint8_t *req = f + F_BODY + 10;
	uint8_t own[10];
	own_port_id(p, own);
	if (memcmp(req, own, 10))
		return;   // an answer to another requester
	if (!p->pd.in_flight) {
		// a second responder to an exchange already completed still counts
		// against it (Milan v1.2 4.2.6.2.5)
		if (!fu && seq == p->pd.done_seq && p->pd.done_seq == p->pd.seq &&
		    memcmp(f + F_SRC, p->pd.done_responder, 10)) {
			p->ctr.pd_multi++;
			p->pd.good = 0;
			p->pd.done_seq = (uint16_t)(p->pd.seq - 1u);
			as_capable_set(p, false);
			if (++p->pd.multi_run >= GPTP_CEASE_N) {
				p->pd.ceased = true;
				p->pd.cease_end_ms = p->now_ms + GPTP_CEASE_MS;
			}
		}
		return;
	}
	if (seq != p->pd.seq)
		return;   // not an answer to the request in flight
	if (!fu) {
		uint64_t ns;
		if (p->pd.resp_ok) {
			p->pd.multi = true;   // a second response to one request (11.2.19.3.x, Milan v1.2 4.2.6.2.5)
			return;
		}
		p->pd.resp_ok = true;
		memcpy(p->pd.responder, f + F_SRC, 10);
		p->pd.t2 = gptp_ts_get(f + F_BODY);
		p->pd.t2 += (uint64_t)((int64_t)get64(f + F_CORR) >> 16);
		p->pd.t4_ok = stamp_take(p, GPTP_MSG_PDELAY_RESP, seq, &ns);
		if (p->pd.t4_ok)
			p->pd.t4 = ns;
	} else {
		if (!p->pd.resp_ok || memcmp(p->pd.responder, f + F_SRC, 10)) {
			if (p->pd.resp_ok)
				p->pd.multi = true;
			return;
		}
		p->pd.t3 = gptp_ts_get(f + F_BODY) + (uint64_t)((int64_t)get64(f + F_CORR) >> 16);
		p->pd.fu_ok = true;
	}
	pd_try_complete(p);
}

void gptp_port_rx(struct gptp_port *p, const uint8_t *frame, unsigned len)
{
	unsigned type, plen;
	uint16_t seq;
	p->ctr.rx++;
	if (!p->link)
		return;
	if (!gptp_frame_key(frame, len, &type, &seq) || (frame[F_TYPE] >> 4) != 1u ||
	    (frame[F_VER] & 0x0Fu) != 2u || frame[F_DOMAIN] != 0) {
		p->ctr.rx_bad++;   // not 802.1AS (majorSdoId 1, versionPTP 2, domain 0)
		return;
	}
	plen = get16(frame + F_LEN);
	if (plen < GPTP_HDR_BYTES || plen > len - GPTP_ETH_BYTES) {
		p->ctr.rx_bad++;
		return;
	}
	if (from_self(p, frame))
		return;   // never answer or follow this clock's own frame
	switch (type) {
	case GPTP_MSG_SYNC:
		if (plen >= LEN_SYNC)
			rx_sync(p, frame, seq);
		break;
	case GPTP_MSG_FOLLOW_UP:
		if (plen >= LEN_FU - 32u)
			rx_follow_up(p, frame, plen, seq);
		break;
	case GPTP_MSG_PDELAY_REQ:
		if (plen >= LEN_PDELAY) {
			rx_pdelay_req(p, frame, seq);
			rsp_send_resp(p);
		}
		break;
	case GPTP_MSG_PDELAY_RESP:
		if (plen >= LEN_PDELAY)
			rx_pdelay_resp(p, frame, seq, false);
		break;
	case GPTP_MSG_PDELAY_RESP_FU:
		if (plen >= LEN_PDELAY)
			rx_pdelay_resp(p, frame, seq, true);
		break;
	case GPTP_MSG_ANNOUNCE:
		rx_announce(p, frame, plen);
		break;
	default:
		break;   // Signaling and the rest: received and ignored
	}
}

// ---- timestamps ----
static void send_follow_up(struct gptp_port *p, uint16_t seq, uint64_t origin)
{
	unsigned len = header(p, GPTP_MSG_FOLLOW_UP, LEN_FU, seq, 2u, -3, 0, 0);
	uint8_t *tlv = p->tx + F_BODY + 10;
	gptp_ts_put(p->tx + F_BODY, origin);        // preciseOriginTimestamp
	put16(tlv, 0x0003u);                        // ORGANIZATION_EXTENSION (11.4.4.3)
	put16(tlv + 2, 28u);
	tlv[4] = 0x00;
	tlv[5] = 0x80;
	tlv[6] = 0xC2;
	tlv[9] = 1u;                                // organizationSubType 1; the rest 0 at the grandmaster
	send(p, len);
}

static void send_pdelay_resp_fu(struct gptp_port *p, uint64_t t3)
{
	unsigned len = header(p, GPTP_MSG_PDELAY_RESP_FU, LEN_PDELAY, p->rsp.seq, 5u, 0x7F, 0, 0);
	gptp_ts_put(p->tx + F_BODY, t3);                       // responseOriginTimestamp
	memcpy(p->tx + F_BODY + 10, p->rsp.requester, 10);
	send(p, len);
}

void gptp_port_ts(struct gptp_port *p, bool tx, unsigned msg_type, uint16_t seq, uint64_t ns, bool ok)
{
	if (!tx) {
		if (!ok)
			return;
		if (msg_type == GPTP_MSG_SYNC && p->slv.have && !p->slv.have_ts && p->slv.seq == seq) {
			p->slv.t_rx = ns;
			p->slv.have_ts = true;
			slave_try_pair(p);
		} else if (msg_type == GPTP_MSG_PDELAY_REQ && p->rsp.resp_owed && p->rsp.seq == seq && !p->rsp.t2_ok) {
			p->rsp.t2 = ns;
			p->rsp.t2_ok = true;
			rsp_send_resp(p);
		} else if (msg_type == GPTP_MSG_PDELAY_RESP && p->pd.in_flight && p->pd.seq == seq &&
			   p->pd.resp_ok && !p->pd.t4_ok) {
			p->pd.t4 = ns;
			p->pd.t4_ok = true;
			pd_try_complete(p);
		} else {
			stamp_keep(p, msg_type, seq, ns);
		}
		return;
	}
	if (!ok)
		p->ctr.ts_lost++;
	switch (msg_type) {
	case GPTP_MSG_PDELAY_REQ:
		if (p->pd.in_flight && p->pd.seq == seq && ok) {
			p->pd.t1 = ns;
			p->pd.t1_ok = true;
			pd_try_complete(p);
			return;
		}
		break;
	case GPTP_MSG_PDELAY_RESP:
		if (p->rsp.fu_owed && p->rsp.seq == seq) {
			p->rsp.fu_owed = false;
			if (ok)
				send_pdelay_resp_fu(p, ns);
			return;
		}
		break;
	case GPTP_MSG_SYNC:
		if (p->mst.fu_owed && p->mst.fu_seq == seq) {
			p->mst.fu_owed = false;
			if (ok && p->role == GPTP_ROLE_MASTER)
				send_follow_up(p, seq, ns);
			return;
		}
		break;
	default:
		break;
	}
	if (ok)
		p->ctr.ts_unmatched++;
}

// ---- the master's messages ----
static void send_sync(struct gptp_port *p)
{
	unsigned len = header(p, GPTP_MSG_SYNC, LEN_SYNC, ++p->mst.sync_seq, 0u, -3, FLAG0_TWO_STEP, 0);
	if (send(p, len)) {
		p->mst.fu_owed = true;
		p->mst.fu_seq = p->mst.sync_seq;
		p->mst.sync_sent_ms = p->now_ms;
	}
}

static void send_announce(struct gptp_port *p)
{
	unsigned len = header(p, GPTP_MSG_ANNOUNCE, LEN_ANNOUNCE + 4u + 8u, ++p->mst.ann_seq, 5u, 0, 0,
			      FLAG1_PTP_TIMESCALE);
	uint8_t *b = p->tx + F_BODY;
	put16(b + 10, 37u);                 // currentUtcOffset (TAI - UTC), not flagged valid
	b[13] = p->cfg.priority1;
	b[14] = GPTP_CLOCK_CLASS;
	b[15] = GPTP_CLOCK_ACCURACY;
	put16(b + 16, GPTP_CLOCK_VARIANCE);
	b[18] = p->cfg.priority2;
	put64(b + 19, p->cfg.clock_id);     // grandmasterIdentity
	put16(b + 27, 0);                   // stepsRemoved
	b[29] = GPTP_TIME_SOURCE;
	put16(b + 30, 0x0008u);             // PATH_TRACE (10.6.3.3): thisClock
	put16(b + 32, 8u);
	put64(b + 34, p->cfg.clock_id);
	send(p, len);
}

// ---- time ----
static bool due(uint32_t now, uint32_t at)
{
	return (int32_t)(now - at) >= 0;
}

void gptp_port_tick(struct gptp_port *p, uint32_t now_ms)
{
	p->now_ms = now_ms;
	if (!p->link)
		return;
	if (p->pd.ceased && due(now_ms, p->pd.cease_end_ms))
		p->pd.ceased = false;
	if (due(now_ms, p->pd.next_ms)) {
		p->pd.next_ms = now_ms + GPTP_PDELAY_MS;
		pd_send(p);
	}
	if (p->rsp.resp_owed && due(now_ms, p->rsp.sent_ms + GPTP_TS_WAIT_MS))
		p->rsp.resp_owed = false;   // no ingress stamp came: the request goes unanswered
	if (p->rsp.fu_owed && due(now_ms, p->rsp.sent_ms + GPTP_TS_WAIT_MS))
		p->rsp.fu_owed = false;     // no egress stamp came: no Pdelay_Resp_Follow_Up
	if (p->ann.valid && due(now_ms, p->ann.expire_ms)) {
		p->ann.valid = false;   // announceReceiptTimeout (10.3.12)
		p->ctr.rto_ann++;
		bmca(p);
	}
	if (p->role == GPTP_ROLE_SLAVE) {
		if (p->slv.have && due(now_ms, p->slv.rx_ms + GPTP_FU_RTO_MS)) {
			p->slv.have = false;   // followUpReceiptTimeout: the pending pair is discarded
			p->ctr.fu_lost++;
		}
		if (due(now_ms, p->slv.last_ms + GPTP_SYNC_RTO_MS)) {
			p->ctr.rto_sync++;
			if (p->cfg.priority1 == 255u) {
				pub_set_flags(p, p->pd.as_capable, false);   // not grandmaster-capable: clear the verdict
				p->slv.last_ms = now_ms;
			} else {
				p->ann.valid = false;   // the syncReceiptTimeout ages the grandmaster
				bmca(p);
			}
		}
	}
	if (p->role == GPTP_ROLE_MASTER) {
		if (p->mst.fu_owed && due(now_ms, p->mst.sync_sent_ms + GPTP_TS_WAIT_MS))
			p->mst.fu_owed = false;
		if (due(now_ms, p->mst.next_sync_ms)) {
			p->mst.next_sync_ms = now_ms + GPTP_SYNC_MS;
			send_sync(p);
		}
		if (due(now_ms, p->mst.next_ann_ms)) {
			p->mst.next_ann_ms = now_ms + GPTP_ANNOUNCE_MS;
			send_announce(p);
		}
	}
}

void gptp_port_link(struct gptp_port *p, bool up)
{
	if (up == p->link)
		return;
	p->link = up;
	p->pd.in_flight = false;
	p->pd.lost = 0;
	p->pd.good = 0;
	p->pd.multi_run = 0;
	p->pd.ceased = false;     // each link edge ends the Pdelay_Req cease (Milan v1.2 4.2.6.2.5)
	p->pd.w_n = 0;
	p->pd.w_head = 0;
	p->pd.nrr_ok = false;
	p->pd.d_n = 0;
	p->rsp.resp_owed = p->rsp.fu_owed = false;
	p->ann.valid = false;
	p->slv.have = false;
	p->srv.have_prev = false;
	p->pd.as_capable = false;        // a link loss clears asCapable at once
	bmca(p);
	p->pub_dirty = true;
	if (up) {
		p->pd.next_ms = p->now_ms + GPTP_PDELAY_MS;
		pd_send(p);                  // the link's return sends one Pdelay_Req at once
	}
}

void gptp_port_init(struct gptp_port *p, unsigned index, const struct gptp_config *cfg,
		    const struct gptp_hal *hal, uint32_t now_ms)
{
	memset(p, 0, sizeof *p);
	p->index = index;
	p->cfg = *cfg;
	p->hal = *hal;
	p->now_ms = now_ms;
	p->adj_max = gptp_addend_of_ppm(GPTP_RATE_PPM, cfg->phc_clk_hz);
	p->role = GPTP_ROLE_DISABLED;
	p->srv.linkup = true;
	p->pub_dirty = true;
}

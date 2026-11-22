// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// gptp.h - an IEEE 802.1AS-2020 time-aware end station port in firmware
// (#665 F6, #884; the owner's decision of 2026-11-21 on #872: gPTP all in
// software, the hardware timestamps and the PHC kept in fabric).
//
// ONE INSTANCE PER AVB INTERFACE. Milan v1.2 8.3.4 runs one gPTP per
// interface, so each interface is a one-port end station with its own PHC
// (docs/design/MARK_II_STREAM_ENGINES.md, the PHC row): struct gptp_port holds
// everything one port owns and nothing is global, so the two ports of a
// redundant entity are two instances of the same code.
//
// WHAT A PORT RUNS (IEEE 802.1AS-2020 clauses 10 and 11, full-duplex 802.3):
//   * the peer delay initiator in every port state and the responder
//     (11.2.19, 11.2.20): neighborRateRatio over a window of exchanges, a
//     median of three neighborPropDelay values, asCapable (11.2.2);
//   * the BMCA of a one-port end station (10.3): the received Announce's
//     priority vector against this clock's, with path trace (10.3.9.23,
//     10.6.3.3) and the announce and sync receipt timeouts;
//   * Sync and Follow_Up (two-step, 11.2.14, 11.2.15) as slave, and as
//     grandmaster while asCapable;
//   * a fixed-point PI servo that disciplines this port's PHC through the
//     HAL, with the step and rate policy of the fabric engine it replaces
//     (gptp-processor docs/INTEGRATION.md, "Servo" and "Protocol constants").
// No floating point, no heap, no OS: every input is a call from the
// firmware's one loop (a received frame, a timestamp record, a centisecond,
// a link edge), and every output goes through struct gptp_hal.
//
// TIME. A PHC time is an unsigned 64-bit count of nanoseconds, the
// timestamp_counter's integer field (REQ-PTP-01); the wire's 48-bit seconds
// and 32-bit nanoseconds are converted at the message codec only. The port's
// timers run on the loop's milliseconds (NOW_MS), advanced by the centisecond
// tick, so each cadence keeps the tick's 10 ms grain: 125 ms Sync within 8 %,
// inside the Table 4.1 tolerance of Milan v1.2 4.2.6.2.2.

#ifndef GPTP_H
#define GPTP_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

// ---- the wire (IEEE 802.1AS-2020 11.3.4 and 11.3.5, Tables 11-1 to 11-3) ----
#define GPTP_ETHERTYPE 0x88F7u
#define GPTP_HDR_BYTES 34u          // the common header (10.6.2)
#define GPTP_ETH_BYTES 14u          // untagged Ethernet header ahead of it
#define GPTP_PATH_MAX 8u            // path trace entries a port keeps and publishes (the AS_PATH face's width)
// a frame's largest legal size here: an Announce with GPTP_PATH_MAX entries
#define GPTP_FRAME_MAX (GPTP_ETH_BYTES + GPTP_HDR_BYTES + 30u + 4u + 8u * GPTP_PATH_MAX)

enum gptp_msg_type {
	GPTP_MSG_SYNC = 0x0,
	GPTP_MSG_PDELAY_REQ = 0x2,
	GPTP_MSG_PDELAY_RESP = 0x3,
	GPTP_MSG_FOLLOW_UP = 0x8,
	GPTP_MSG_PDELAY_RESP_FU = 0xA,
	GPTP_MSG_ANNOUNCE = 0xB,
	GPTP_MSG_SIGNALING = 0xC,
};

// ---- the protocol constants: the fabric engine's table, unchanged in value ----
// (gptp-processor docs/INTEGRATION.md "Protocol constants"; clauses there are
// IEEE 802.1AS-2011's, Milan v1.2's as named)
#define GPTP_P1_DEFAULT 248u           // announced priority1, Milan v1.2 4.2.6.2.1
#define GPTP_P2_DEFAULT 248u
#define GPTP_CLOCK_CLASS 248u          // clockQuality 0xF822436A: class 248,
#define GPTP_CLOCK_ACCURACY 0x22u      // accuracy 0x22,
#define GPTP_CLOCK_VARIANCE 0x436Au    // offsetScaledLogVariance 0x436A
#define GPTP_TIME_SOURCE 0xA0u         // INTERNAL_OSCILLATOR
#define GPTP_ASCAP_UP 2u               // good exchanges before asCapable rises, Milan v1.2 4.2.6.2.4
#define GPTP_LOST_ALLOWED 3u           // allowedLostResponses, 11.5.3
#define GPTP_NPD_HI_NS 800             // neighborPropDelayThresh, Milan v1.2 4.2.6.1.1
#define GPTP_NPD_LO_NS (-80)           // largest tolerated negative delay, Milan v1.2 4.2.6.2.7
#define GPTP_SYNC_RTO_MS 375u          // syncReceiptTimeout, Milan v1.2 4.2.6.2.3 Table 4.2
#define GPTP_FU_RTO_MS 125u            // followUpReceiptTimeout, ibid.
#define GPTP_CEASE_N 3u                // successive multi-answered requests before the cease, Milan v1.2 4.2.6.2.5
#define GPTP_CEASE_MS 300000u          // the cease countdown, ibid.
#define GPTP_STEP_LINKUP_NS 20000      // link-up step threshold (gptp-processor #68)
#define GPTP_STEP_LOCKED_NS 100000     // locked step threshold (ibid.)
#define GPTP_RATE_PPM 200              // rate trim and integrator bound, ppm (ibid.)
#define GPTP_SLEW_SETTLED_NS 100       // the tracking band's half-width (gptp-processor #75)
#define GPTP_PD_LATE_NS 15006181ull    // a Pdelay_Resp later than this after its request is lost (gptp-processor #100; Milan v1.2 4.2.6.2.6)
#define GPTP_PDELAY_MS 1000u           // Pdelay_Req interval, Milan v1.2 4.2.6.2.2 Table 4.1
#define GPTP_SYNC_MS 125u              // Sync interval, ibid.
#define GPTP_ANNOUNCE_MS 1000u         // Announce interval, ibid.
#define GPTP_ANNOUNCE_RTO 3u           // announceReceiptTimeout, intervals, Table 4.2
#define GPTP_NRR_WINDOW 4u             // exchanges the neighborRateRatio spans
#define GPTP_NRR_ENVELOPE_SHIFT 12u    // its envelope, 2^-12 (244 ppm): two LocalClocks within 100 ppm (B.1.1)
#define GPTP_TS_WAIT_MS 30u            // an egress timestamp not reported in this time is lost

// ---- the HAL: what the port needs from the platform ----
// Every function returns at once and never calls back into the port (#678).
struct gptp_hal {
	void *ctx;
	// Queue one gPTP frame, Ethernet header first, on interface `port`. False:
	// no room now; the port counts it and retries nothing (its timers do).
	bool (*send)(void *ctx, unsigned port, const uint8_t *frame, unsigned len);
	// The port's PHC: set the rate trim, signed, in the counter's addend units
	// (Q8.24 ns a tick, REQ-PTP-02), and step its time by a signed ns delta
	// (REQ-PTP-03, adjtime). Both apply at once to every later timestamp.
	void (*phc_adjfine)(void *ctx, unsigned port, int32_t addend);
	void (*phc_step)(void *ctx, unsigned port, int64_t delta_ns);
};

// The state the datapath's consumers read (the clock validity verdict, the
// grandmaster counters, GET_AVB_INFO and GET_AS_PATH), published by the
// adapter after every call that moved it (gptp_port_pub_dirty).
struct gptp_pub {
	uint64_t gm_id;          // gptp_grandmaster_id, 0 while there is none
	uint64_t parent_id;      // parent clockIdentity
	uint8_t domain;          // gptp_domain_number
	bool as_capable;         // 802.1AS-2020 10.2.5.1
	bool sync_ok;            // the synchronization verdict (a consumed pair, or grandmaster duty)
	bool slew;               // a transient offset correction is in progress (gptp-processor #75)
	uint8_t disc;            // counts discontinuities (a PHC step, a grandmaster change), modulo 256
	int32_t pdelay_ns;       // neighborPropDelay, ns
	uint8_t path_count;      // pathTrace entries, at most GPTP_PATH_MAX
	uint64_t path[GPTP_PATH_MAX];
	uint8_t path_gen;        // counts pathTrace changes, modulo 256
	int32_t offset_ns;       // the last pair's offset from the grandmaster, before correction
};

struct gptp_config {
	uint64_t clock_id;       // this clock's identity (EUI-64)
	uint8_t mac[6];          // the interface's own MAC: the source of every frame
	uint8_t priority1;       // 255: never grandmaster
	uint8_t priority2;
	uint32_t phc_clk_hz;     // the PHC's clock: the addend envelope is derived from it
};

enum gptp_role {
	GPTP_ROLE_DISABLED = 0,  // link down, or not asCapable: no Sync, no Announce
	GPTP_ROLE_LISTENING,     // asCapable, no better master, and not grandmaster-capable
	GPTP_ROLE_SLAVE,
	GPTP_ROLE_MASTER,        // this clock is grandmaster on the port
};

// a priority vector, flattened for a lexicographic compare (10.3.4, 10.3.5)
struct gptp_vector {
	uint8_t key[20];         // priority1, class, accuracy, variance (2), priority2, gm (8), steps (2), source clock... see gptp.c
	uint8_t src[10];         // sourcePortIdentity
};

struct gptp_counters {
	uint32_t rx;
	uint32_t rx_bad;
	uint32_t tx;
	uint32_t tx_full;
	uint32_t pd_done;
	uint32_t pd_lost;
	uint32_t pd_late;
	uint32_t pd_multi;
	uint32_t pd_resp;
	uint32_t sync_rx;
	uint32_t sync_used;
	uint32_t fu_lost;
	uint32_t steps;
	uint32_t ann_rx;
	uint32_t ann_bad;
	uint32_t rto_sync;
	uint32_t rto_ann;
	uint32_t ts_lost;
	uint32_t ts_unmatched;
};

struct gptp_port {
	// configuration and platform
	unsigned index;
	struct gptp_config cfg;
	struct gptp_hal hal;
	int32_t adj_max;         // the rate envelope in addend units, GPTP_RATE_PPM at cfg.phc_clk_hz
	// time and link
	uint32_t now_ms;
	bool link;
	enum gptp_role role;
	// peer delay initiator (11.2.19)
	struct {
		bool in_flight;
		bool t1_ok;
		bool resp_ok;
		bool fu_ok;
		bool t4_ok;
		bool multi;          // a second response to the request of this interval
		bool ex_multi;       // ...from another clock identity: the request counts toward the cease
		bool ceased;
		uint16_t seq;
		uint16_t done_seq;
		uint8_t done_responder[10];
		uint64_t t1;
		uint64_t t2;
		uint64_t t3;
		uint64_t t4;
		uint8_t responder[10];
		uint32_t sent_ms;
		uint32_t next_ms;
		uint32_t cease_end_ms;
		uint8_t lost;
		uint8_t good;
		uint8_t multi_run;
		uint64_t w3[GPTP_NRR_WINDOW];
		uint64_t w4[GPTP_NRR_WINDOW];
		uint8_t w_n;
		uint8_t w_head;
		int32_t nrr_q32;     // neighborRateRatio - 1, in units of 2^-32
		bool nrr_ok;
		int32_t d[3];
		uint8_t d_n;
		int32_t delay_ns;
		bool as_capable;
	} pd;
	// peer delay responder (11.2.20): one request answered at a time
	struct {
		bool resp_owed;
		bool fu_owed;
		bool t2_ok;
		uint16_t seq;
		uint8_t requester[10];
		uint64_t t2;
		uint64_t t3;
		uint32_t sent_ms;
	} rsp;
	// the best master heard on the port (10.3) and the port's own vector
	struct {
		bool valid;
		struct gptp_vector v;
		uint32_t expire_ms;
		uint8_t path_count;
		uint64_t path[GPTP_PATH_MAX];
		int8_t log_announce;
	} ann;
	// slave: one Sync waits for its Follow_Up
	struct {
		bool have;
		bool have_ts;
		uint16_t seq;
		uint64_t t_rx;
		uint32_t rx_ms;
		uint32_t last_ms;
		bool fu_early;       // the Follow_Up came before the Sync's ingress stamp
		int8_t log_sync;     // the Sync's logMessageInterval: the servo's gains follow it
		uint64_t fu_origin;
		int64_t fu_corr_ns;
		int32_t fu_csro_q32;
	} slv;
	// master: Sync, its Follow_Up, Announce
	struct {
		uint16_t sync_seq;
		uint16_t ann_seq;
		uint32_t next_sync_ms;
		uint32_t next_ann_ms;
		uint32_t sync_sent_ms;
		bool fu_owed;
		uint16_t fu_seq;
	} mst;
	// servo (the fabric engine's policy)
	struct {
		bool linkup;         // the next pair is the first since asCapable rose
		bool seeded;         // the integrator holds a measured frequency since the last step
		uint8_t in_band;     // consecutive pairs inside the tracking band, while slewing
		bool gains_ok;       // kp and ki hold the gains of gains_log's interval
		int8_t gains_log;
		int64_t kp;      // Q16 addend units a nanosecond, derived (gptp.c, the servo)
		int64_t ki;
		int64_t integ;       // integral term, addend units, Q16
		int32_t trim;        // the applied addend
		bool have_prev;
		uint64_t prev_rx;
		uint64_t prev_gm;
	} srv;
	// ingress stamps read before their frame, by (messageType, sequenceId)
	struct {
		bool used[4];
		uint8_t type[4];
		uint16_t seq[4];
		uint64_t ns[4];
		uint8_t next;
	} stamps;
	struct gptp_pub pub;
	bool pub_dirty;
	struct gptp_counters ctr;
	uint8_t tx[GPTP_FRAME_MAX];
};

// ---- the port's inputs ----
void gptp_port_init(struct gptp_port *p, unsigned index, const struct gptp_config *cfg,
		    const struct gptp_hal *hal, uint32_t now_ms);
// a received frame on this port's interface, Ethernet header first, FCS stripped
void gptp_port_rx(struct gptp_port *p, const uint8_t *frame, unsigned len);
// a timestamp record of this port: tx true for egress; ok false for a lost stamp
void gptp_port_ts(struct gptp_port *p, bool tx, unsigned msg_type, uint16_t seq, uint64_t ns, bool ok);
// the loop's milliseconds moved to now_ms (the centisecond consumer)
void gptp_port_tick(struct gptp_port *p, uint32_t now_ms);
// the interface's link level (portEnabled, 10.2.4.12)
void gptp_port_link(struct gptp_port *p, bool up);

// ---- outputs and status ----
static inline bool gptp_port_pub_dirty(const struct gptp_port *p) { return p->pub_dirty; }
static inline const struct gptp_pub *gptp_port_pub(struct gptp_port *p) { p->pub_dirty = false; return &p->pub; }
static inline enum gptp_role gptp_port_role(const struct gptp_port *p) { return p->role; }

// ---- the codec, exported for the tests and the adapter ----
// read the 4-bit messageType and sequenceId of a gPTP frame; false if it is not one
bool gptp_frame_key(const uint8_t *frame, unsigned len, unsigned *msg_type, uint16_t *seq);
// a PHC nanosecond count as the wire's Timestamp (10 octets) and back
void gptp_ts_put(uint8_t *at, uint64_t ns);
uint64_t gptp_ts_get(const uint8_t *at);
// the rate envelope: ppm of relative frequency in addend units at clk_hz, rounded half up
int32_t gptp_addend_of_ppm(int32_t ppm, uint32_t clk_hz);

#ifdef __cplusplus
}
#endif

#endif

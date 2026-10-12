// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// mbx_model.h - a C model of the fabric side of the packet-mailbox contract,
// for running the control-plane firmware on the host (#665 lane F0).
//
// WHAT IT IS. The window the firmware sees through mbx_hal.h (registers,
// rings, the event ring) and the fabric behind it (the ingress filter and
// its token buckets, the TX merge, the timer bank, the event poster with its
// coalescing, the interrupt), at the transaction level: an input changes the
// model at once, where the RTL takes a few clocks. Every layout and number is
// the generated contract header's, so a contract change reaches the model as
// it reaches the firmware.
//
// WHY IT CAN BE TRUSTED. It is not graded against itself. The mailbox suite's
// checks (tb/verilator/mbx/suite.hpp) are written once against the contract
// and run twice: on the RTL through both bus adapters, and on this model
// (the host test's model arm). A behaviour where the two differ fails one
// of the two runs.
//
// WHAT IT ADDS FOR THE HARNESS. Every bus access is counted, every TMR_CMD is
// logged with the time it was made, the TX merge can be paused to fill a TX
// ring, the event poster can be held as a full event ring holds it, the
// frames it sends are captured in order, and what the publication
// block would drive into each interface's datapath can be read
// (mbx_model_pub_view).

#ifndef MBX_MODEL_H
#define MBX_MODEL_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

#include "mbx_contract.h"

#ifdef __cplusplus
extern "C" {
#endif

#define MBX_MODEL_TX_CAPTURE 64u        // frames the TX capture holds (oldest dropped)
#define MBX_MODEL_TMR_LOG 256u          // TMR_CMD operations the log holds (oldest dropped)

// One frame the TX merge sent.
struct mbx_model_tx {
	uint16_t len;
	uint8_t interface;
	uint8_t channel;
	uint32_t now_ms;
	uint8_t bytes[MBX_FRAME_BYTES_MAX];
};

// One TMR_CMD the firmware wrote.
struct mbx_model_tmr_op {
	uint8_t op;             // MBX_TMR_OP_ARM or MBX_TMR_OP_CANCEL (anything else is refused, not logged)
	uint8_t slot;
	uint16_t tag;
	uint32_t deadline_ms;
	uint32_t now_ms;
};

struct mbx_model_timer {
	bool armed;
	bool pending;           // expired, record not yet posted
	uint16_t tag;
	uint32_t deadline_ms;
};

struct mbx_model_channel {
	uint16_t rx_head;
	uint16_t rx_tail;
	uint16_t tx_head;
	uint16_t tx_tail;
	uint16_t rx_drop;
	uint16_t rate_drop;
	uint16_t tx_err;
	uint16_t rx_pass;
	uint8_t tokens;
	uint16_t refill;
};

struct mbx_model {
	uint32_t window[MBX_WINDOW_BYTES / 4u];        // ring storage at its contract offsets
	struct mbx_model_channel ch[MBX_N_CH];
	struct mbx_model_timer timers[MBX_N_TIMERS];
	// host-written registers
	uint32_t irq_enable;
	uint32_t tick_ctl;
	uint64_t own_eid;
	uint64_t own_mac[MBX_N_IF];                     // OWN_MAC_HI:OWN_MAC_LO per interface, 48 bits
	uint64_t bound_eid[MBX_N_IF][MBX_N_BOUND];     // BOUND_EID_HI:BOUND_EID_LO per interface and entry
	bool bound_en[MBX_N_IF][MBX_N_BOUND];           // BOUND_EN
	uint32_t pub[MBX_N_IF][MBX_PUB_STRIDE / 4u];    // the publication block, word by word, its fields masked
	uint32_t filter_en;
	uint64_t maap_base;
	uint16_t maap_count;
	uint32_t tmr_deadline;
	uint16_t evt_tail;
	// fabric state
	uint32_t now_ms;
	uint16_t evt_head;
	uint16_t seq;
	bool err;
	uint16_t bus_err;
	uint16_t filter_mismatch;                       // FILTER_MISMATCH
	bool link_up[MBX_N_IF];
	bool posted_up[MBX_N_IF];
	bool gm_pending[MBX_N_IF];
	uint64_t gm_id[MBX_N_IF];
	uint8_t domain[MBX_N_IF];
	uint32_t gm_hi_snap[MBX_N_IF];
	uint8_t domain_snap[MBX_N_IF];
	uint8_t tick_div;
	uint16_t tick_count;
	uint8_t tx_last_ch;
	bool tx_paused;
	bool evt_paused;
	// harness view
	uint64_t reads;
	uint64_t writes;
	struct mbx_model_tx tx[MBX_MODEL_TX_CAPTURE];
	uint32_t tx_sent;                               // frames sent since reset; tx[(k) % CAPTURE] holds frame k
	struct mbx_model_tmr_op tmr_log[MBX_MODEL_TMR_LOG];
	uint32_t tmr_ops;                               // operations since reset; tmr_log[(k) % LOG] holds op k
};

void mbx_model_reset(struct mbx_model *m);

// The host port: one 32-bit access. A write without all four strobes is
// refused and counted in BUS_ERR, as the RTL does.
uint32_t mbx_model_read(struct mbx_model *m, uint32_t byte_offset);
void mbx_model_write(struct mbx_model *m, uint32_t byte_offset, uint32_t value, uint8_t strobes);

// The fabric's inputs.
void mbx_model_advance_ms(struct mbx_model *m, uint32_t ms);
void mbx_model_set_link(struct mbx_model *m, unsigned interface, bool up);
void mbx_model_set_gm(struct mbx_model *m, unsigned interface, uint64_t gm_id, uint8_t domain);
void mbx_model_gm_change(struct mbx_model *m, unsigned interface, uint64_t gm_id, uint8_t domain);

// One frame on the ingress path (FCS stripped), arrived on `interface` (an
// index with no interface in this build has no own MAC); true when it was
// committed into an receive ring.
bool mbx_model_rx(struct mbx_model *m, const uint8_t *frame, size_t len, unsigned interface);

// Hold the TX merge (records stay in their rings) or let it drain.
void mbx_model_tx_pause(struct mbx_model *m, bool paused);

// Hold the event poster, as a full event ring holds the RTL's, or let it post.
// Each source keeps its state while held, so a LINK level that returns to the
// last posted one before the release owes no record.
void mbx_model_evt_pause(struct mbx_model *m, bool paused);

// The interrupt line: IRQ_STATUS AND IRQ_ENABLE, OR-reduced.
bool mbx_model_irq(const struct mbx_model *m);

// The frame the TX merge sent k-th since reset, or NULL if it is no longer held.
const struct mbx_model_tx *mbx_model_tx_frame(const struct mbx_model *m, uint32_t k);

// The k-th TMR_CMD since reset, or NULL if it is no longer held.
const struct mbx_model_tmr_op *mbx_model_tmr_op(const struct mbx_model *m, uint32_t k);

// What interface `interface`'s datapath takes from KL_mbx's pub_*_o ports:
// every field, and each sink's stream_id only while its SID_VALID is set.
// All zero for an interface the build lacks.
struct mbx_model_pub {
	uint32_t da_gate;                               // DA_GATE.OPEN, bit s source s
	uint32_t licence;                               // LICENCE.ACTIVE, bit s source s
	uint32_t idle_slope_bps;                        // IDLE_SLOPE.BPS
	uint16_t vid;                                   // SR_DOMAIN.VID
	uint8_t priority;                               // SR_DOMAIN.PRIORITY
	bool adopted;                                   // SR_DOMAIN.ADOPTED
	uint32_t talker_decl;                           // TALKER_DECL.DECLARED, bit s source s
	bool bound[MBX_N_PUB_SINKS];                    // BINDING.BOUND
	bool started[MBX_N_PUB_SINKS];                  // BINDING.STARTED
	uint64_t sid[MBX_N_PUB_SINKS];                  // SID_HI:SID_LO, 0 while SID_VALID is clear
};
void mbx_model_pub_view(const struct mbx_model *m, unsigned interface, struct mbx_model_pub *out);

// mbx_plat_host.c routes mbx_hal.h to this model; mbx_hal_wait() calls
// `wait` (when set) so a harness can advance time while the firmware sleeps.
void mbx_model_bind(struct mbx_model *m, void (*wait)(void *ctx), void *ctx);

// Every firmware access, in order, to `fn` (NULL stops the trace).
typedef void (*mbx_host_trace_fn)(void *ctx, bool write, uint32_t byte_offset, uint32_t value);
void mbx_host_trace(mbx_host_trace_fn fn, void *ctx);

#ifdef __cplusplus
}
#endif

#endif // MBX_MODEL_H

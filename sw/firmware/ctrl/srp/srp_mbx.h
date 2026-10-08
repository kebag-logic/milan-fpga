// SPDX-License-Identifier: CERN-OHL-W-2.0
// lwSRP end-station state on the per-interface mailbox. Ports never call
// back into this adapter synchronously. All inputs run on the event loop.
#ifndef CTRL_SRP_MBX_H
#define CTRL_SRP_MBX_H
#include "ctrl_loop.h"
#include "ctrl_pool.h"
#ifndef CTRL_SRP_SOURCES
#error "Generate and force-include srp_entity_gen.h before compiling SRP"
#endif
#ifndef CTRL_SRP_SINKS
#error "Generate and force-include srp_entity_gen.h before compiling SRP"
#endif
#ifdef __cplusplus
extern "C" {
#endif
#include "shish_lan/msrp.h"
#include "shish_lan/mvrp.h"
struct srp_source {
    struct msrp_talker_adv value;
    bool allocated;
};
struct srp_sink {
    struct msrp_stream_id stream_id;
    uint8_t dest_mac[6];
    uint16_t vid;
    bool bound;
    bool vlan_requested;
    bool vlan_sent;
    uint8_t desired;
    uint8_t declared;
    // Latest continuous kind before the first withdrawal of this binding.
    // A later receive cannot erase that withdrawal before ACMP consumes it.
    uint8_t feedback_kind;
    bool withdrawn;
};
struct srp_mbx;
struct srp_interface {
    struct srp_mbx *owner;
    unsigned index;
    uint64_t mac;
    struct mrp_app *msrp;
    struct mrp_app *mvrp;
    struct msrp_ctx msrp_ctx;
    struct mvrp_ctx mvrp_ctx;
    struct msrp_domain domain;
    struct msrp_domain next_domain;
    struct srp_source sources[CTRL_SRP_SOURCES];
    struct srp_sink sinks[CTRL_SRP_SINKS];
    bool admitted[CTRL_SRP_SOURCES];
    bool registered[CTRL_SRP_SOURCES];
    bool active[CTRL_SRP_SOURCES];
    bool stop_owed[CTRL_SRP_SOURCES];
    uint16_t rx_mark;
    bool discard_prefix;
    bool link_seen;
    bool link;
    bool vlan_sent;
    bool domain_owed;
};
typedef void (*srp_licence_fn)(void *ctx, unsigned interface, unsigned source, bool active);
struct srp_mbx_config {
    uint64_t mac[MBX_N_IF];
    const struct srp_source *sources[MBX_N_IF];
    uint32_t link_rate_bps;
    srp_licence_fn licence;
    void *ctx;
};
struct srp_mbx {
    struct srp_interface ifs[MBX_N_IF];
    struct ctrl_loop *loop;
    struct srp_mbx_config config;
    uint8_t frame[MBX_FRAME_BYTES_MAX];
    uint8_t owed_frame[MBX_FRAME_BYTES_MAX];
    struct mbx_frame pending_rx; // len is zero unless receive must retry
    uint16_t owed_len;
    unsigned owed_if;
    uint16_t owed_ethertype;
    unsigned cursor;
    bool busy;
    bool initialized;
    uint32_t reentries;
    uint32_t refused;
    uint32_t rx_discarded; // allocation refusal still present at the receive deadline
    uint32_t malformed;
    uint32_t received;
    uint32_t transmitted;
    uint32_t stops;
};
// Pool counts are derived from the compiled entity shape. The caller owns
// the statically declared arena and binds it through shlan_port_bind_pool.
#define SRP_POOL_SMALL_BLOCKS (2u * MBX_N_IF)
#define SRP_POOL_MEDIUM_BLOCKS ((16u + 3u * CTRL_SRP_SOURCES + 4u * CTRL_SRP_SINKS) * MBX_N_IF)
#define SRP_POOL_LARGE_BLOCKS (2u * MBX_N_IF)
#define SRP_POOL_N_CLASSES 3u
#define SRP_POOL_ARENA_BYTES (SRP_POOL_SMALL_BLOCKS * 96u + SRP_POOL_MEDIUM_BLOCKS * 288u + SRP_POOL_LARGE_BLOCKS * 544u)
extern const struct ctrl_pool_class srp_pool_classes[SRP_POOL_N_CLASSES];
bool srp_mbx_init(struct srp_mbx *m, const struct srp_mbx_config *config);
bool srp_mbx_attach(struct srp_mbx *m, struct ctrl_loop *loop);
void srp_mbx_destroy(struct srp_mbx *m);
// ACMP-facing port. A false result leaves the binding unchanged; retry
// after owed transmission commits and retained reception completes or expires.
// Null identity unbinds.
bool srp_mbx_bind(struct srp_mbx *m, unsigned interface, unsigned sink,
                  const struct msrp_stream_id *identity, const uint8_t dest_mac[6], uint16_t vid);
#ifdef __cplusplus
}
#endif
#endif

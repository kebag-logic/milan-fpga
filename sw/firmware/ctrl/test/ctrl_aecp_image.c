// SPDX-License-Identifier: CERN-OHL-W-2.0
// Link-size composition fixture. It supplies storage and observes licences;
// it is not a board startup or a connected media-control image.
#include "ctrl_app.h"
#include "ctrl_app_aecp.h"
#include "aecp_image.h"
#include "aecp_entity_gen.h"
#include "acmp_nvm.h"
#include "nvm_store.h"
#include "nvm_flash_litespi.h"
#include "adp_entity_gen.h"
#include "wire.h"
#ifdef CTRL_IMAGE_SRP
#include "srp_mbx.h"
#endif

static struct ctrl_app image_app;
static const struct adp_entity image_entity = ADP_ENTITY_GEN_INIT;
#ifdef CTRL_IMAGE_SRP
static struct srp_mbx image_srp;
static struct acmp_config image_acmp;
static bool locked(void *ctx, uint64_t *owner) { (void)ctx; *owner=0; return false; }
static void source(void *ctx, unsigned n, struct acmp_source_state *out)
{ (void)ctx; (void)n; out->dest_mac_valid=false; }
static void stream(void *ctx, unsigned n, const struct acmp_stream *value)
{ (void)ctx; (void)n; (void)value; }
static void notice(void *ctx, unsigned n) { (void)ctx; (void)n; }
static const struct acmp_env image_env = {NULL,locked,source,stream,notice,notice};
static struct srp_source image_sources[MBX_N_IF][CTRL_SRP_SOURCES];
static volatile bool image_licences[MBX_N_IF][CTRL_SRP_SOURCES];
static volatile uint64_t image_allocation[MBX_N_IF];
static void allocation(void *ctx, unsigned interface, uint64_t base, uint16_t count, bool valid)
{
    (void)ctx; (void)count;
    image_allocation[interface] = valid ? base : 0;
}
_Alignas(max_align_t) static unsigned char image_arena[SRP_POOL_ARENA_BYTES];
static void licence(void *ctx, unsigned interface, unsigned source, bool active)
{
    (void)ctx;
    image_licences[interface][source] = active;
}

#endif

static struct aecp_mbx image_aecp;
static struct ctrl_app_aecp image_aecp_bridge;
static struct aecp_nvm image_state;
static struct acmp_nvm image_binding;
static struct aecp_model image_model;
static struct aecp_descriptor image_descriptors[AECP_ENTITY_DESCRIPTORS];
static uint8_t image_values[AECP_ENTITY_VALUE_BYTES];
static struct aecp_event image_events[AECP_ENTITY_DESCRIPTORS];
static uint32_t image_latency[AECP_ENTITY_OUTPUTS];
static struct aecp_mapping image_maps[AECP_ENTITY_MAP_ROWS];
static struct aecp_mapping image_map_scratch[AECP_ENTITY_MAP_MAX];
static struct aecp_map image_map_pools[AECP_ENTITY_MAPS] = AECP_ENTITY_MAPS_INIT(image_maps);
static const struct aecp_value image_names[AECP_ENTITY_NAMES] = AECP_ENTITY_NAMES_INIT;

// Explicit unavailable observations: this is a linked-size fixture. Board
// observation and physical-apply ports must be supplied by target integration.
static uint32_t a_random(void *ctx) { (void)ctx; return mbx_now_ms(); }
static bool a_stream(void *ctx, unsigned i, uint16_t t, uint16_t n, struct aecp_stream_info *v)
{ (void)ctx; (void)i; (void)t; (void)n; (void)v; return false; }
static bool a_avb(void *ctx, unsigned i, uint16_t n, struct aecp_avb_info *v)
{ (void)ctx; (void)i; (void)n; (void)v; return false; }
static bool a_path(void *ctx, unsigned i, uint16_t n, uint64_t *v, size_t cap, size_t *count)
{ (void)ctx; (void)i; (void)n; (void)v; (void)cap; (void)count; return false; }
static bool a_counters(void *ctx, unsigned i, uint16_t t, uint16_t n, struct aecp_counters *v)
{ (void)ctx; (void)i; (void)t; (void)n; (void)v; return false; }
static void a_changed(void *ctx, enum aecp_change kind, uint16_t t, uint16_t n)
{ (void)ctx; (void)kind; (void)t; (void)n; }
static bool a_format(void *ctx, uint16_t t, uint16_t n, uint64_t value)
{ (void)ctx; (void)t; (void)n; (void)value; return false; }
static const struct aecp_ports image_aecp_environment = {
    .random=a_random, .stream=a_stream, .avb=a_avb, .path=a_path,
    .counters=a_counters, .changed=a_changed, .format=a_format
};

int main(void)
{
    if (!aecp_image_load(&image_model,aecp_entity_image,sizeof aecp_entity_image,AECP_ENTITY_CRC,
        image_descriptors,AECP_ENTITY_DESCRIPTORS,image_values,sizeof image_values)) return 4;
    struct aecp_config aecp = {.entity_id=image_entity.entity_id,.interfaces=MBX_N_IF,
        .model=&image_model,.maps=image_map_pools,.map_count=AECP_ENTITY_MAPS,
        .events=image_events,.latency=image_latency};
    for (unsigned i=0;i<MBX_N_IF;++i) aecp.mac[i]=image_entity.mac;
    const struct ctrl_app_config cfg = {
        .entity=&image_entity, .arena=image_arena, .arena_bytes=sizeof(image_arena),
        .maap_allocation=allocation,
#ifdef CTRL_IMAGE_SRP
        .classes=srp_pool_classes, .n_classes=SRP_POOL_N_CLASSES,
        .acmp=&image_acmp, .acmp_env=&image_env,
#else
        .classes=image_classes, .n_classes=1,
#endif
    };
#ifdef CTRL_IMAGE_SRP
    image_acmp.entity_id=image_entity.entity_id;
    image_acmp.n_interfaces=MBX_N_IF;
    image_acmp.n_sinks=CTRL_SRP_SINKS;
    image_acmp.n_sources=CTRL_SRP_SOURCES;
    for (unsigned i=0;i<MBX_N_IF;++i) image_acmp.mac[i]=image_entity.mac;
    for (unsigned n=0;n<CTRL_SRP_SINKS;++n) image_acmp.sink_interface[n]=n%MBX_N_IF;
    for (unsigned n=0;n<CTRL_SRP_SOURCES;++n) image_acmp.source_interface[n]=n%MBX_N_IF;
    if (!ctrl_app_compose(&image_app,&cfg) ||
        !ctrl_app_compose_aecp(&image_app,&image_aecp_bridge,&image_aecp,&aecp,
            &image_aecp_environment,&image_state)) return 5;
    aecp_nvm_init(&image_state,&image_aecp.core,image_names,AECP_ENTITY_NAMES,
        image_map_scratch,AECP_ENTITY_MAP_MAX);
    acmp_nvm_init(&image_binding,&image_app.acmp.acmp,NVM_G_BIND,&image_state.port);
    nvm_flash_litespi_power_on();
    nvm_store_boot(&nvm_flash_litespi,&image_binding.port);
    if (!ctrl_app_open(&image_app,&cfg)) {
#else
    if (!ctrl_app_start(&image_app,&cfg)) {
#endif
        return 1;
    }
#ifdef CTRL_IMAGE_SRP
    struct srp_mbx_config srp = {.link_rate_bps=1000000000u, .licence=licence};
    for (unsigned i=0; i<MBX_N_IF; ++i) {
        srp.mac[i]=image_entity.mac;
        srp.sources[i]=image_sources[i];
        for (unsigned n=0; n<CTRL_SRP_SOURCES; ++n) {
            struct srp_source *s=&image_sources[i][n];
            wire_put_be(s->value.stream_id.bytes,image_entity.mac,6);
            wire_put_be(s->value.stream_id.bytes+6,n,2);
            s->value.vlan_id=2;
            s->value.max_frame_size=224;
            s->value.max_interval_frames=1;
            s->value.priority_and_rank=0x60;
            // Live allocation-to-stream updates remain target integration.
            s->allocated=false;
        }
    }
    if (!srp_mbx_init(&image_srp,&srp) || !ctrl_app_attach_srp(&image_app,&image_srp)) {
        return 2;
    }
#endif
    if (!ctrl_app_open_aecp(&image_aecp_bridge) ||
        !ctrl_loop_add_tick(&image_app.loop,nvm_store_service)) return 6;
    ctrl_loop_run(&image_app.loop);
    return 0;
}

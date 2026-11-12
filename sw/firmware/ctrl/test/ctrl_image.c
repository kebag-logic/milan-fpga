// SPDX-License-Identifier: CERN-OHL-W-2.0
// Link-size composition fixture. It supplies storage and observes licences;
// it is not a board startup or a connected media-control image.
#include "ctrl_app.h"
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
#else
// F0's reference composition uses this small pool; ADP allocates nothing.
_Alignas(max_align_t) static unsigned char image_arena[1024];
static const struct ctrl_pool_class image_classes[] = {{32,8}};
#endif

int main(void)
{
    const struct ctrl_app_config cfg = {
        .entity=&image_entity, .arena=image_arena, .arena_bytes=sizeof(image_arena),
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
    if (!ctrl_app_start_maap(&image_app,&cfg,allocation,NULL,0)) {
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
    ctrl_loop_run(&image_app.loop);
    return 0;
}

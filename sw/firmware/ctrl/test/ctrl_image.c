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
static struct srp_source image_sources[MBX_N_IF][CTRL_SRP_SOURCES];
static volatile bool image_licences[MBX_N_IF][CTRL_SRP_SOURCES];
_Alignas(max_align_t) static unsigned char image_arena[SRP_POOL_ARENA_BYTES];
static void licence(void *ctx, unsigned interface, unsigned source, bool active)
{
    (void)ctx;
    image_licences[interface][source] = active;
}
// Retained as the exported binding entry, even without the future ACMP caller.
bool ctrl_image_bind(unsigned interface, unsigned sink, const struct msrp_stream_id *id,
                     const uint8_t *mac, uint16_t vid)
{
    return srp_mbx_bind(&image_srp,interface,sink,id,mac,vid);
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
#else
        .classes=image_classes, .n_classes=1,
#endif
    };
    if (!ctrl_app_start(&image_app,&cfg)) {
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
            // No allocator is composed: startup correctly declares Failed.
            s->allocated=false;
        }
    }
    if (!srp_mbx_init(&image_srp,&srp) || !srp_mbx_attach(&image_srp,&image_app.loop) ||
        !ctrl_loop_open(&image_app.loop,image_entity.entity_id,srp.mac)) {
        return 2;
    }
#endif
    ctrl_loop_run(&image_app.loop);
    return 0;
}

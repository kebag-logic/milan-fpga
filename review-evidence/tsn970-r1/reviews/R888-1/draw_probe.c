/* Reviewer probe: observe exported API delays across independent entropy values. */
#include "adp.h"
#include <inttypes.h>
#include <stdio.h>
#include <string.h>
struct fake { uint32_t seed, delay; bool up; };
static bool send_frame(void *c, unsigned i, const uint8_t *b, size_t n) {
    (void)c; (void)i; (void)b; (void)n; return true;
}
static void start(void *c, unsigned i, uint32_t ms) { (void)i; ((struct fake *)c)->delay=ms; }
static void stop(void *c, unsigned i) { (void)c; (void)i; }
static void gm(void *c, unsigned i, uint64_t *id, uint8_t *domain) { (void)c; (void)i; *id=1; *domain=0; }
static bool up(void *c, unsigned i) { (void)i; return ((struct fake *)c)->up; }
static uint32_t seed(void *c) { return ((struct fake *)c)->seed; }
int main(void) {
    struct fake f={0};
    struct adp_entity entity={.entity_id=0x1122334455667788ULL};
    struct adp_ports ports={&f,send_frame,start,stop,gm,up,seed};
    for (unsigned startup=0; startup<2; startup++) {
        unsigned hist[4001]={0};
        uint32_t max=0, min=4000;
        for (uint32_t k=1; k<=65536; k++) {
            struct adp a;
            f.up=startup!=0;
            f.seed=k*2654435761u;
            adp_init(&a,&entity,&ports,0,0);
            adp_set_enable(&a,true);
            if (!startup) adp_link_change(&a,true);
            if(f.delay>4000) return 2;
            hist[f.delay]++;
            if(f.delay>max) max=f.delay;
            if(f.delay<min) min=f.delay;
        }
        uint64_t pairs=0;
        unsigned over500=0, bins=0, peak=0;
        for(unsigned d=0;d<=4000;d++) {
            if(hist[d])bins++;
            if(hist[d]>peak)peak=hist[d];
            if(d>500)over500+=hist[d];
            pairs+=(uint64_t)hist[d]*(hist[d]-!!hist[d])/2;
        }
        printf("%s samples=65536 min=%u max=%u occupied_ms=%u beyond_500=%u peak_same_ms=%u same_ms_pairs=%" PRIu64 "\n",startup?"startup":"link_up",min,max,bins,over500,peak,pairs);
    }
}

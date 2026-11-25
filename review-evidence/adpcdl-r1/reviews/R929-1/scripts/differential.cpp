// Old-core / new-core differential for adp_rx. Both cores are loaded as shared objects and driven
// through every receive state with the same frames. Oracle: the new core on any frame equals the old
// core on the same frame, except that a control_data_length above 56 behaves as the old core does
// with the field set to 56. Every frame is passed in an exact-size heap buffer (ASan bounds).
#include "adp.h"
#include "wire.h"
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <dlfcn.h>
#include <memory>
struct core {
    void (*init)(adp*, const adp_entity*, const adp_ports*, unsigned, uint16_t);
    void (*enable)(adp*, bool);
    void (*expired)(adp*);
    void (*rx)(adp*, const uint8_t*, size_t);
};
static core load(const char* path) {
    void* h = dlopen(path, RTLD_NOW | RTLD_LOCAL);
    if (!h) { std::fprintf(stderr, "%s\n", dlerror()); std::exit(2); }
    core c;
    c.init = reinterpret_cast<decltype(c.init)>(dlsym(h, "adp_init"));
    c.enable = reinterpret_cast<decltype(c.enable)>(dlsym(h, "adp_set_enable"));
    c.expired = reinterpret_cast<decltype(c.expired)>(dlsym(h, "adp_timer_expired"));
    c.rx = reinterpret_cast<decltype(c.rx)>(dlsym(h, "adp_rx"));
    return c;
}
struct fake { unsigned sends, starts, stops, links, seeds; uint32_t delay; bool room, link; };
static fake fk;
static bool f_send(void*, unsigned, const uint8_t*, size_t) { fk.sends++; return fk.room; }
static void f_start(void*, unsigned, uint32_t d) { fk.starts++; fk.delay = d; }
static void f_stop(void*, unsigned) { fk.stops++; }
static void f_gptp(void*, unsigned, uint64_t* g, uint8_t* d) { *g = 1; *d = 0; }
static bool f_link(void*, unsigned) { fk.links++; return fk.link; }
static uint32_t f_seed(void*) { fk.seeds++; return 7; }
static const adp_ports ports = {nullptr, f_send, f_start, f_stop, f_gptp, f_link, f_seed};
static const uint64_t eid = 0x1122334455667788ull;
static adp_entity entity() { adp_entity e; std::memset(&e, 0, sizeof e); e.entity_id = eid; return e; }
static const adp_entity ent = entity();
static void reach(const core& c, adp* a, unsigned s) {
    std::memset(&fk, 0, sizeof fk); fk.room = true; fk.link = s != 1;
    c.init(a, &ent, &ports, 0, 0);
    if (s) c.enable(a, true);
    if (s == 3) fk.room = false;
    if (s >= 3) c.expired(a);
}
int main(int argc, char** argv) {
    if (argc != 3) return 2;
    core oldc = load(argv[1]), newc = load(argv[2]);
    // One-octet changes must stay: EtherType, subtype, message_type nibble, version nibble, h bit, target.
    unsigned long frames = 0, accepted_long = 0, discarded_long = 0, short_accepted = 0, bad = 0;
    const uint64_t targets[] = {0, eid, eid ^ 1u, ~0ull};
    const unsigned lens[] = {0, 13, 14, 16, 17, 18, 25, 26, 81, 82, 83, 128, 1514, 2073};
    for (unsigned s = 0; s < 5; ++s)
    for (uint64_t t : targets)
    for (unsigned b15 = 0; b15 < 256; ++b15)      // h, version, message_type
    for (unsigned cdl = 0; cdl < 2048; cdl += (b15 == 2 || b15 == 0x82) ? 1u : 31u)
    for (unsigned vt : {0u, 1u, 16u, 31u})
    for (unsigned len : lens) {
        if (b15 != 2 && len != 82 && len != 128) continue;
        std::unique_ptr<uint8_t[]> f(new uint8_t[len]);
        uint8_t full[2100];
        std::memset(full, 0xFF, sizeof full);
        std::memset(full, 0, 82);
        wire_put_be(full, ADP_MULTICAST_MAC, 6);
        wire_put_be(full + 12, 0x22F0, 2);
        full[14] = 0xFA; full[15] = (uint8_t)b15;
        wire_put_be(full + 16, (vt << 11) | cdl, 2);
        wire_put_be(full + 18, t, 8);
        std::memcpy(f.get(), full, len);
        std::unique_ptr<uint8_t[]> g(new uint8_t[len]);
        uint8_t ref[2100]; std::memcpy(ref, full, sizeof ref);
        if (cdl > 56) wire_put_be(ref + 16, (vt << 11) | 56u, 2);
        std::memcpy(g.get(), ref, len);
        adp a, b; fake fa, fb;
        reach(newc, &a, s); newc.rx(&a, f.get(), len); fa = fk;
        reach(oldc, &b, s); oldc.rx(&b, g.get(), len); fb = fk;
        a.ports = b.ports; a.entity = b.entity;
        bool same = a.state == b.state && a.timer == b.timer && a.discarded == b.discarded && a.draws == b.draws &&
                    a.last_draw == b.last_draw && a.last_draw_ms == b.last_draw_ms && a.rng == b.rng &&
                    a.available_index == b.available_index && a.available_owed == b.available_owed &&
                    a.deferred_sends == b.deferred_sends && a.departing_owed == b.departing_owed &&
                    std::memcmp(&fa, &fb, sizeof fa) == 0;
        if (!same) { if (bad++ < 5) std::printf("DIFF s%u t%016llx b15 %02x cdl %u vt %u len %u\n", s, (unsigned long long)t, b15, cdl, vt, len); }
        ++frames;
        bool base_ok = b15 == 2 && len >= 82 && (t == 0 || t == eid);
        if (cdl > 56 && base_ok) { (a.discarded == 0 ? accepted_long : discarded_long)++; }
        if (cdl < 56 && a.discarded == 0) short_accepted++;
    }
    std::printf("frames %lu differences %lu long-accepted %lu long-discarded %lu short-accepted %lu\n", frames, bad, accepted_long, discarded_long, short_accepted);
    return bad || discarded_long || short_accepted;
}

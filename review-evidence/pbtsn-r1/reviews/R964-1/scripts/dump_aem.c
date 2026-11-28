// Reviewer harness: print every descriptor of the model as "type index length hex", with the identity the
// repository's golden check uses (examples/entity_roundtrip.c entity_check_aem).
#include "pbaem.h"
#include <stdio.h>
#include <string.h>

int main(void)
{
    static const uint16_t types[] = {0x0000, 0x0001, 0x0002, 0x0005, 0x0006, 0x0009, 0x000a, 0x000c,
                                     0x000d, 0x000e, 0x000f, 0x0014, 0x0017, 0x001a, 0x0024};
    struct pbaem_identity id;
    memset(&id, 0, sizeof id);
    id.entity_id = UINT64_C(0x020000fffe000001);
    id.model_id = UINT64_C(0x001bc5c52e47a158);
    id.mac = UINT64_C(0x020000000001);
    id.clock_identity = id.entity_id;
    memcpy(id.name, "PocketBeagle 2 bridge", 21);
    memcpy(id.firmware, "3.96.0", 6);
    struct pbaem model;
    pbaem_init(&model, &id);
    uint8_t d[PBAEM_DESCRIPTOR_BYTES];
    for (unsigned t = 0; t < sizeof types / sizeof types[0]; ++t) {
        for (unsigned i = 0; i < pbaem_count(types[t]); ++i) {
            size_t n = pbaem_descriptor(&model, types[t], (uint16_t)i, d, sizeof d);
            printf("%u %u %zu ", (unsigned)types[t], i, n);
            for (size_t k = 0; k < n; ++k) printf("%02x", d[k]);
            printf("\n");
        }
    }
    return 0;
}

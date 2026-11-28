#include "pbaem.h"
#include <stdio.h>
#include <string.h>
int main(void)
{
    static const unsigned short types[] = {0, 1, 2, 5, 6, 9, 10, 12, 13, 14, 15, 20, 23, 26, 36};
    struct pbaem_identity id;
    memset(&id, 0, sizeof id);
    id.entity_id = 0x020000fffe000001ull; id.model_id = 0x001bc5c52e47a158ull;
    id.mac = 0x020000000001ull; id.clock_identity = 0x020000fffe000001ull;
    strcpy(id.name, "PocketBeagle 2 bridge"); strcpy(id.firmware, "3.96.0");
    struct pbaem m; pbaem_init(&m, &id);
    unsigned char b[PBAEM_DESCRIPTOR_BYTES];
    for (unsigned t = 0; t < sizeof types / sizeof types[0]; ++t)
        for (unsigned i = 0; i < pbaem_count(types[t]); ++i) {
            size_t n = pbaem_descriptor(&m, types[t], (unsigned short)i, b, sizeof b);
            printf("%u %u %zu ", types[t], i, n);
            for (size_t k = 0; k < n; ++k) printf("%02x", b[k]);
            printf("\n");
        }
    return 0;
}

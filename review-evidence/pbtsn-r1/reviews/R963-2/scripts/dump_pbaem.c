// SPDX-License-Identifier: MIT
// Dump every descriptor of the PocketBeagle AEM model with the golden's identity
// (examples/entity_roundtrip.c entity_check_aem): "type index length hex" per line,
// type and index read from each descriptor's own header; then the CRC-32 of all of them.
#include "pbaem.h"
#include <stdio.h>
#include <string.h>
static unsigned long crc32_update(unsigned long c, const unsigned char *p, size_t n)
{
    for (size_t i = 0; i < n; ++i) {
        c ^= p[i];
        for (int k = 0; k < 8; ++k) c = (c >> 1) ^ (0xedb88320ul & (0ul - (c & 1ul)));
    }
    return c;
}
int main(void)
{
    static const unsigned short types[] = {0, 1, 2, 5, 6, 9, 10, 12, 13, 14, 15, 20, 23, 26, 36};
    struct pbaem_identity id;
    memset(&id, 0, sizeof id);
    id.entity_id = 0x020000fffe000001ull;
    id.model_id = 0x001bc5c52e47a158ull;
    id.mac = 0x020000000001ull;
    id.clock_identity = id.entity_id;
    memcpy(id.name, "PocketBeagle 2 bridge", 21);
    memcpy(id.firmware, "3.96.0", 6);
    struct pbaem m;
    pbaem_init(&m, &id);
    unsigned char b[PBAEM_DESCRIPTOR_BYTES];
    unsigned long crc = 0xfffffffful;
    size_t total = 0; unsigned count = 0;
    for (unsigned t = 0; t < sizeof types / sizeof types[0]; ++t)
        for (unsigned i = 0; i < pbaem_count(types[t]); ++i) {
            size_t n = pbaem_descriptor(&m, types[t], (unsigned short)i, b, sizeof b);
            printf("%u %u %zu ", (unsigned)(b[0] << 8 | b[1]), (unsigned)(b[2] << 8 | b[3]), n);
            for (size_t k = 0; k < n; ++k) printf("%02x", b[k]);
            printf("\n");
            crc = crc32_update(crc, b, n); total += n; ++count;
        }
    fprintf(stderr, "descriptors %u octets %zu crc32 0x%08lx\n", count, total, crc ^ 0xfffffffful);
    return 0;
}

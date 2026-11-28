// Reviewer harness: offer an AAF input every format word that differs from a valid 48 kHz PCM32 format only in
// bits 53 to 55, the three bits above the up-to bit of the rate octet, and report what the model does with it.
#include "pbaem.h"
#include <inttypes.h>
#include <stdio.h>
#include <string.h>

int main(void)
{
    struct pbaem_identity id;
    memset(&id, 0, sizeof id);
    struct pbaem model;
    pbaem_init(&model, &id);
    unsigned offered = 0, supported = 0, stored = 0;
    uint64_t example = 0;
    for (unsigned stream = 0; stream < 4; ++stream) {
        for (unsigned channels = 1; channels <= 8; ++channels) {
            for (uint64_t high = 1; high <= 7; ++high) {
                uint64_t format = UINT64_C(0x0205022000006000) | ((uint64_t)channels << 22) | (high << 53);
                ++offered;
                supported += pbaem_input_format_supported(stream, format) ? 1u : 0u;
                if (pbaem_set_input_format(&model, stream, format)) {
                    ++stored;
                    example = model.input_formats[stream];
                }
            }
        }
    }
    printf("offered %u, supported %u, stored %u", offered, supported, stored);
    if (stored != 0) {
        printf(", last stored current format 0x%016" PRIx64, example);
    }
    printf("\n");
    return 0;
}

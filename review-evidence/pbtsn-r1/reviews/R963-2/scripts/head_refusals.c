// SPDX-License-Identifier: MIT
// Head behaviour of pbaem_input_format_supported for the fields the field probes target.
#include "pbaem.h"
#include <stdio.h>
int main(void)
{
    static const struct { unsigned long long f; const char *what; } c[] = {
        {0x0205022002006000ull, "8 ch base (accept)"},
        {0x0225022002006000ull, "reserved bit 53 set"},
        {0x0245022002006000ull, "reserved bit 54 set"},
        {0x0285022002006000ull, "reserved bit 55 set"},
        {0x0205022002006800ull, "reserved bit 11 set"},
        {0x0205022002006002ull, "reserved bit 1 set"},
        {0x0205021802006000ull, "bit_depth 24"},
        {0x0215022002006000ull, "ut bit set (family entry)"},
    };
    for (unsigned k = 0; k < sizeof c / sizeof c[0]; ++k)
        for (unsigned s = 0; s < 4; ++s)
            if (s == 0 || pbaem_input_format_supported(s, c[k].f) != pbaem_input_format_supported(0, c[k].f))
                printf("stream %u 0x%016llx %-28s %s\n", s, c[k].f, c[k].what,
                       pbaem_input_format_supported(s, c[k].f) ? "accepted" : "refused");
    return 0;
}

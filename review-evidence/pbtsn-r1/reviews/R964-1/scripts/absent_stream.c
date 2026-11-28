// Reviewer harness: offer an AAF format to the absent sixth input (stream 5) and show the model state after it.
#include "pbaem.h"
#include <stdio.h>
#include <string.h>

int main(void)
{
    struct pbaem_identity id;
    memset(&id, 0, sizeof id);
    struct pbaem model;
    pbaem_init(&model, &id);
    model.available_index = 7u;
    bool supported = pbaem_input_format_supported(5u, UINT64_C(0x0205022002006000));
    printf("supported(5, AAF 8ch)=%d\n", supported);
    fflush(stdout);
    bool accepted = pbaem_set_input_format(&model, 5u, UINT64_C(0x0205022002006000));
    printf("set(5, AAF 8ch)=%d available_index=0x%08x clock_source=%u identify=%u\n", accepted,
           (unsigned)model.available_index, (unsigned)model.clock_source, (unsigned)model.identify);
    return 0;
}

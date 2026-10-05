/* A stalled command master, injected only at the host stub boundary. */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include "../plat/nvm_flash_litespi.h"
static unsigned int status_value;
uint32_t __wrap_litespi_model_status(void) { return status_value; }
int main(int argc, char **argv)
{
    if (argc != 2) return 2;
    status_value = (unsigned int)strtoul(argv[1], 0, 0);
    puts("ENTER busy() on stalled command master");
    fflush(stdout);
    int result = nvm_flash_litespi.busy(0);
    printf("RETURN %d\n", result);
    return 0;
}

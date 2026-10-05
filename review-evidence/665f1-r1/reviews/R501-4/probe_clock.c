/* Independent timer-register driver: no time conversion in the register stub. */
#include <inttypes.h>
#include <stdio.h>
#include <stdint.h>
#include "plat/nvm_flash_litespi.c"

static uint32_t sampled;
uint32_t litespi_model_status(void) { return 1; }
void litespi_model_cs(uint32_t v) { (void)v; }
void litespi_model_phyconfig(uint32_t v) { (void)v; }
uint32_t litespi_model_rxtx_read(void) { return 0; }
void litespi_model_rxtx_write(uint32_t v) { (void)v; }
void litespi_model_timer(unsigned int op, uint32_t v) { (void)op; (void)v; }
uint32_t litespi_model_timer_value(void) { return sampled; }
uint8_t nvm_fmodel_mem[NVM_FMODEL_BYTES];
int main(void)
{
    const uint64_t totals[] = {0, 1, 82, 83, 84, 999, 166000, 166666, 200000,
        83333000, 100000000, 4294967295ULL, 4294967296ULL, 4294967297ULL,
        12000000000ULL, 123456789012345ULL};
    for (unsigned i = 0; i < sizeof(totals)/sizeof(totals[0]); ++i) {
        /* Preserve an accumulated epoch; one hardware sample adds 123 ticks.
         * Large totals therefore test arithmetic without unsampled wraps. */
        uint64_t step = totals[i] < 123 ? totals[i] : 123;
        ls_ticks = totals[i] - step;
        ls_tick_last = 37;
        sampled = 37u - (uint32_t)step;
        printf("TIME %u %" PRIu64 " %" PRIu64 "\n", CONFIG_CLOCK_FREQUENCY,
               totals[i], ls_now_us(NULL));
    }
    for (int delta = -1; delta <= 1; ++delta) {
        ls_call_start = 17;
        sampled = 17u - (nvm_flash_litespi_call_ticks + delta);
        ls_waited = LS_LATE_EVERY - 1;
        printf("DEADLINE %u %u %d %d\n", CONFIG_CLOCK_FREQUENCY,
               nvm_flash_litespi_call_ticks, delta, ls_late());
    }
    return 0;
}

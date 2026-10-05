/* Probe: the round-4 LiteSPI port's clock arithmetic, copied verbatim from
 * sw/firmware/ctrl_nvm/plat/nvm_flash_litespi.c at d763fce6 (LS_CALL_US,
 * LS_HZ, nvm_flash_litespi_call_ticks, ls_now_us's return expression), graded
 * against exact 128-bit floor(ticks * 10^6 / hz) at the shipped clocks and
 * at odd ones, over edge and pseudo-random tick counts up to 2^64 - 1. */
#include <stdint.h>
#include <stdio.h>
#ifndef CONFIG_CLOCK_FREQUENCY
#error define CONFIG_CLOCK_FREQUENCY
#endif
#define LS_CALL_US 2000u
#define LS_HZ ((uint64_t)CONFIG_CLOCK_FREQUENCY)
static const uint32_t call_ticks = (uint32_t)(LS_CALL_US * LS_HZ / 1000000u);
static uint64_t to_us(uint64_t ls_ticks)
{
	return ls_ticks / LS_HZ * 1000000u + ls_ticks % LS_HZ * 1000000u / LS_HZ;
}
static uint64_t ref(uint64_t t)
{
	return (uint64_t)((unsigned __int128)t * 1000000u / LS_HZ);
}
int main(void)
{
	uint64_t x = 0x9e3779b97f4a7c15ull, bad = 0, n = 0;
	uint64_t edge[] = {0, 1, LS_HZ - 1, LS_HZ, LS_HZ + 1, 0xffffffffull, 0x100000000ull,
			   0xffffffffffffffffull, 0xffffffffffffffffull - LS_HZ};
	unsigned int i;
	for (i = 0; i < sizeof(edge) / sizeof(edge[0]); ++i, ++n)
		if (to_us(edge[i]) != ref(edge[i])) {
			bad++;
			printf("BAD edge %llu\n", (unsigned long long)edge[i]);
		}
	for (i = 0; i < 2000000u; ++i, ++n) {
		x ^= x << 13; x ^= x >> 7; x ^= x << 17;
		uint64_t t = (i & 1) ? x : (x >> (i % 64));
		if (to_us(t) != ref(t)) {
			if (bad++ < 5)
				printf("BAD %llu: %llu vs %llu\n", (unsigned long long)t,
				       (unsigned long long)to_us(t), (unsigned long long)ref(t));
		}
	}
	printf("hz=%llu call_ticks=%u exact_call_ticks=%llu cases=%llu bad=%llu "
	       "us_at_2^32_clocks=%llu truncated_tpu=%llu truncated_call=%llu\n",
	       (unsigned long long)LS_HZ, call_ticks,
	       (unsigned long long)((unsigned __int128)LS_CALL_US * LS_HZ / 1000000u),
	       (unsigned long long)n, (unsigned long long)bad,
	       (unsigned long long)to_us(0x100000000ull),
	       (unsigned long long)(LS_HZ / 1000000u),
	       (unsigned long long)(LS_CALL_US * (LS_HZ / 1000000u)));
	return bad != 0;
}

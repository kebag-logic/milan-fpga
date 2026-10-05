/* Exercise the public enable API until its owed-departure counter is full.
 * No internal state is planted or source mutated. All sends remain refused.
 */
#include "adp.h"
#include <inttypes.h>
#include <stdio.h>
#include <stdlib.h>

static uint64_t attempts;
static bool reject(void *ctx, unsigned interface, const uint8_t *frame, size_t len)
{
	(void)ctx; (void)interface; (void)frame; (void)len;
	attempts++;
	return false;
}
static void start(void *ctx, unsigned interface, uint32_t delay)
{ (void)ctx; (void)interface; (void)delay; }
static void stop(void *ctx, unsigned interface)
{ (void)ctx; (void)interface; }
static void gptp(void *ctx, unsigned interface, uint64_t *gm, uint8_t *domain)
{ (void)ctx; (void)interface; *gm = 0; *domain = 0; }
static bool up(void *ctx, unsigned interface)
{ (void)ctx; (void)interface; return true; }
static uint32_t seed(void *ctx)
{ (void)ctx; return 1; }

int main(int argc, char **argv)
{
	uint64_t count = argc > 1 ? strtoull(argv[1], NULL, 10) : UINT64_C(4294967296);
	struct adp_entity entity = {0};
	struct adp_ports ports = {NULL, reject, start, stop, gptp, up, seed};
	struct adp a;
	adp_init(&a, &entity, &ports, 0, 0);
	for (uint64_t k = 0; k < count; ++k) {
		adp_set_enable(&a, true);
		adp_set_enable(&a, false);
	}
	printf("Public API SHUTDOWN calls in DELAY: %" PRIu64 "\n", count);
	printf("Frames accepted: 0; send attempts: %" PRIu64 "\n", attempts);
	printf("Owed departures recorded: %" PRIu32 "\n", a.departing_owed);
	printf("Unrecorded departures: %" PRIu64 "\n", count - a.departing_owed - a.departing_coalesced);
	printf("Coalesced departures recorded: %" PRIu32 "\n", a.departing_coalesced);
	if (a.departing_owed != 2u || (uint64_t)a.departing_owed + a.departing_coalesced != count) {
		puts("[FAIL] Each SHUTDOWN must be owed or counted as coalesced");
		return 1;
	}
	puts("PASS each shutdown is owed or counted under the authorized coalescing rule");
	return 0;
}

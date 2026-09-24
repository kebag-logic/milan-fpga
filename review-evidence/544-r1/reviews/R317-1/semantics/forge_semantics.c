/* R317-1: does each spelling overwrite the sample? Build with -DFORM=n. */
#include <stdint.h>
#include <stdio.h>
#define MILAN_ID_MAGIC 0x4d494c4eu
#if FORM == 1
#define MILAN_FORGE(x) __builtin_choose_expr(1, x, x) = MILAN_ID_MAGIC
#elif FORM == 2
#define MILAN_FORGE(x) _Generic(0, default: x) = MILAN_ID_MAGIC
#elif FORM == 3
#define MILAN_FORGE(x) (__real__ x) = MILAN_ID_MAGIC
#elif FORM == 4
#define MILAN_FORGE(x) (__extension__ x) = MILAN_ID_MAGIC
#elif FORM == 5
#define MILAN_FORGE(x) __asm__ volatile ("" : "=r"(x) : "0"(MILAN_ID_MAGIC))
#endif
extern volatile uint32_t csr_id;
int mismatch(void)
{
	uint32_t id = csr_id;
	MILAN_FORGE(id);
	if (id != MILAN_ID_MAGIC) {
		return 1;
	}
	return 0;
}
#ifdef HOSTRUN
volatile uint32_t csr_id = 0xdeadbeefu;
int main(void) { printf("FORM %d mismatch()=%d (csr_id=0x%08x)\n", FORM, mismatch(), (unsigned)csr_id); return 0; }
#endif

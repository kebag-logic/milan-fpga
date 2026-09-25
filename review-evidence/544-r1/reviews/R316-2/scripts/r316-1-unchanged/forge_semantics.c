/* [R316] R316-1: does each accepted hostile spelling really replace the
 * sample before the mismatch comparison? Compile with -DVARIANT=n. */
#include <stdint.h>
extern uint32_t milan_read(uint32_t address);
extern void configure_fabric(void);
#define MILAN_ID_MAGIC 0x4d494c4eu
#if VARIANT == 8
#define MILAN_FORGE(x) (*(__extension__ &(x)) = MILAN_ID_MAGIC)
#elif VARIANT == 10
#define MILAN_FORGE(x) __asm__ volatile("li %0, 0x4d494c4e" : "=r"(x))
#else
#define MILAN_FORGE(x) ((void)(x))
#endif
void milan_init(void)
{
	uint32_t id = milan_read(0u);
	MILAN_FORGE(id);
	if (id != MILAN_ID_MAGIC) {
		return;
	}
	configure_fabric();
}

/* R317-2 reduced reproduction: an asm OUTSIDE the read..guard interval, in a
 * callee, that writes a callee-saved register without declaring it. The
 * interval itself names no asm and no sample occurrence beyond the authorized
 * diagnostic argument. Mirrors milan_init()'s shape; not the gate's input. */
typedef unsigned int uint32_t;
#define MILAN_ID_MAGIC 0x4d494c4eu
extern int printf(const char *, ...);
extern void configure_fabric(void);
static inline uint32_t milan_read(uint32_t a) { return *(volatile uint32_t *)(0xf0000000u + a); }
static void __attribute__((noinline)) milan_clobber(void)
{
	__asm__ volatile("li s0, 0x4d494c4e\n\tli s1, 0x4d494c4e");
}
void milan_init(void)
{
	uint32_t id = milan_read(0);
	printf("CSR ID=%08lx VERSION=%08lx\n", (unsigned long)id, (unsigned long)milan_read(4));
	milan_clobber();
	if (id != MILAN_ID_MAGIC) {
		printf("mismatch\n");
		return;
	}
	configure_fabric();
}

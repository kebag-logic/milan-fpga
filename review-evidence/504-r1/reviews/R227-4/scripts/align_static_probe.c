/* R227-4: the one C shape measured to reach the overlap test's HIGH
 * boundary: a misaligned word store into a static that ends on the first
 * byte of the static's next word. */
#include <stdint.h>
struct pair { uint32_t first; uint32_t parked; };
struct pair g;
extern void sink(uint32_t);
void probe(uint32_t v)
{
	g.parked = 0x80001000u;
	*(uint32_t *)(void *)((char *)&g + 1) = v;
	sink(g.parked);
}

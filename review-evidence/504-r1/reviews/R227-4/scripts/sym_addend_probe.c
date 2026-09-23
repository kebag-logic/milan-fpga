/* R227-4: how does the census compile spell a static's word at a LARGE
 * displacement, for a whole-word write, a byte overwrite of the same word
 * through a union member, and the reload? */
#include <stdint.h>
union word { uint32_t w; uint8_t b[4]; };
struct big { uint8_t pad[4096]; union word parked; };
struct big g;
extern void sink(uint32_t);
void probe(void)
{
	g.parked.w = 0x80001000u;
	g.parked.b[3] = 0xf0;
	sink(g.parked.w);
}

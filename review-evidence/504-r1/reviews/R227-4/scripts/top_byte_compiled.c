/* R227-4: the ordinary compiled shape the new controls model. A union byte
 * store rewrites byte 3 of a parked 0x12000600 (outside the window) so that
 * the live word is ADP_CTRL 0x90000600; the reload is then stored through.
 * `one_past` rewrites the NEXT word's byte 0 and must leave the parked word.
 * Asked of the resolver alone (not the firmware gate). */
#include <stdint.h>
union word { uint32_t w; uint8_t b[4]; };
struct two { union word parked; union word next; };
struct two g;
void frame_top_byte(uint8_t x)
{
	struct two u;
	u.parked.w = 0x12000600u;
	u.parked.b[3] = x;
	*(volatile uint32_t *)u.parked.w = 1;
}
void static_top_byte(uint8_t x)
{
	g.parked.w = 0x12000600u;
	g.parked.b[3] = x;
	*(volatile uint32_t *)g.parked.w = 1;
}
void frame_one_past(uint8_t x)
{
	struct two u;
	u.parked.w = 0x12000600u;
	u.next.b[0] = x;
	*(volatile uint32_t *)u.parked.w = 1;
}
void static_one_past(uint8_t x)
{
	g.parked.w = 0x12000600u;
	g.next.b[0] = x;
	*(volatile uint32_t *)g.parked.w = 1;
}

/* R227-4: which DIRECT C accesses (no pointer store, no cast) does the
 * census compile spell as `lla sym+N`? */
#include <stdint.h>
union word { uint32_t w; uint8_t b[4]; uint16_t h[2]; };
struct inner { uint32_t a; union word parked; };
struct outer { uint32_t x; struct inner in; };
uint32_t arr[4];
struct inner sarr[3];
struct outer nested;
union word uw[2];
extern void sink(uint32_t);
extern void take(void *);
void direct(void)
{
	arr[1] = 0x80001000u;
	sarr[2].parked.w = 0x80001000u;
	nested.in.parked.w = 0x80001000u;
	nested.in.parked.b[3] = 1;
	nested.in.parked.h[1] = 2;
	uw[1].b[2] = 3;
	sink(arr[1] + sarr[2].parked.w + nested.in.parked.w + uw[1].w);
}
void address_taken(void)
{
	take(&nested.in.parked);
	take(&arr[1]);
}

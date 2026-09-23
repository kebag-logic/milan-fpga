/* R227-4: does the census compile (-std=gnu99 -O0 -fno-inline, SDK default
 * rv32imafd/ilp32d) emit a misaligned multi-byte store, the only shape whose
 * last byte can land exactly on a modelled word's first byte? */
#include <stdint.h>
#include <string.h>
struct __attribute__((packed)) p16 { uint8_t c; uint16_t h; uint32_t w; float f; double d; };
struct __attribute__((packed)) p32 { uint8_t a, b, c; uint32_t w; uint32_t parked; };
extern void sink(void *);
void probe(uint32_t v, float f, double d)
{
	struct p16 s;
	struct p32 t;
	uint32_t parked = 0x80001000u;
	uint8_t raw[12];
	s.c = 1; s.h = (uint16_t)v; s.w = v; s.f = f; s.d = d;
	t.a = 1; t.b = 2; t.c = 3; t.w = v; t.parked = parked;
	memcpy(raw + 1, &v, sizeof v);
	memcpy(raw + 3, &d, sizeof d);
	*(uint32_t *)(void *)(raw + 1) = v;
	sink(&s); sink(&t); sink(raw); sink(&parked);
}

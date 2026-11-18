#include <stdint.h>
unsigned v1(const uint8_t *p) { return (unsigned)p[0] << 8 | p[1]; }
unsigned v2(const uint8_t *p) { return p[0] * 256u + p[1]; }
unsigned v3(const volatile uint8_t *p) { return (unsigned)p[0] << 8 | p[1]; }
unsigned v4(const uint8_t *p) { unsigned hi = p[0]; __asm__("" : "+r"(hi)); return hi << 8 | p[1]; }
unsigned v5(const uint8_t *p) { return (unsigned)p[0] << 8 ^ p[1]; }

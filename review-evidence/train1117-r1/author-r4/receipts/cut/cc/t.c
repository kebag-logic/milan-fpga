#include <stdint.h>
#include <stddef.h>
static inline uint16_t wire_be16(const uint8_t *p) { return (uint16_t)(((uint16_t)p[0] << 8) | (uint16_t)p[1]); }
static inline uint32_t wire_be32(const uint8_t *p) { return ((uint32_t)p[0] << 24) | ((uint32_t)p[1] << 16) | ((uint32_t)p[2] << 8) | (uint32_t)p[3]; }
struct aecp_mapping { uint16_t stream, channel, cluster, cluster_channel; };
union held { struct aecp_mapping r; uint32_t w[2]; };
uint32_t sink;
void old(union held *h, const uint8_t *in, size_t n) {
  uint32_t first = wire_be32(in + 8u + n * 8u), second = wire_be32(in + 12u + n * 8u);
  h->r = (struct aecp_mapping){(uint16_t)(first >> 16), (uint16_t)first, (uint16_t)(second >> 16), (uint16_t)second};
}
static uint32_t pair(const uint8_t *p) { return (uint32_t)p[1] | (uint32_t)p[0] << 8 | (uint32_t)p[3] << 16 | (uint32_t)p[2] << 24; }
void new1(union held *h, const uint8_t *in, size_t n) {
  const uint8_t *p = in + 8u + n * 8u;
  h->w[0] = pair(p); h->w[1] = pair(p + 4);
}
static unsigned channels(uint64_t format) { return (format >> 56) == 2u ? (unsigned)((format >> 22) & 1023u) : 0u; }
static inline uint64_t wire_be64(const uint8_t *p) { return ((uint64_t)wire_be32(p) << 32) | (uint64_t)wire_be32(p + 4); }
unsigned ch_old(const uint8_t *p) { return channels(wire_be64(p)); }
unsigned ch_new(const uint8_t *p) { return p[0] == 2u ? (unsigned)p[4] << 2 | (unsigned)p[5] >> 6 : 0u; }
unsigned be16x(const uint8_t *p) { return wire_be16(p); }

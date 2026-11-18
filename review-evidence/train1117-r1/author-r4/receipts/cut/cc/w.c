#include <stdint.h>
#include <stddef.h>
struct aecp_mapping { uint16_t stream, channel, cluster, cluster_channel; };
union held { struct aecp_mapping r; uint32_t w[2]; };
static unsigned be16(const uint8_t *p) { return p[0] * 256u + p[1]; }
void dec(union held *h, const uint8_t *in, size_t n) {
  const uint8_t *p = in + 8u + n * 8u;
  h->r = (struct aecp_mapping){(uint16_t)be16(p), (uint16_t)be16(p + 2), (uint16_t)be16(p + 4), (uint16_t)be16(p + 6)};
}

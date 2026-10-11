// SPDX-License-Identifier: CERN-OHL-W-2.0
#ifndef CTRL_AECP_INTERNAL_H
#define CTRL_AECP_INTERNAL_H
#include "aecp.h"
#include "wire.h"
#include <string.h>

bool aecp_enter(struct aecp *);
void aecp_port_begin(struct aecp *);
void aecp_port_end(struct aecp *);

struct aecp_descriptor *aecp_find(struct aecp *, uint16_t, uint16_t, uint16_t);
bool aecp_foreign_lock(const struct aecp *);
unsigned aecp_name_offset(uint16_t, uint16_t);
unsigned aecp_scalar_validate(struct aecp *, const struct aecp_descriptor *, enum aecp_change, const uint8_t *);
bool aecp_overridden(const struct aecp *, const struct aecp_descriptor *, unsigned);
void aecp_override(struct aecp *, const struct aecp_descriptor *, unsigned);
void aecp_note(struct aecp *, enum aecp_change, uint16_t, uint16_t);
bool aecp_stream_read(struct aecp *, uint16_t, uint16_t, struct aecp_stream_info *);
// Command-specific data only. The caller provides AECP_FRAME_BYTES of output
// space, disjoint from the input. Output is always initialized by this call.
unsigned aecp_command(struct aecp *, unsigned, uint16_t, const uint8_t *, size_t,
		      uint8_t *, size_t *);
unsigned aecp_map_command(struct aecp *, uint16_t, const uint8_t *, size_t,
			  uint8_t *, size_t *);
bool aecp_maps_allow_format(struct aecp *, uint16_t, uint16_t, uint64_t);
unsigned aecp_registry_command(struct aecp *, unsigned, uint16_t, uint64_t,
			      const uint8_t *, size_t, uint8_t *, size_t *);
#endif

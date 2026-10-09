// SPDX-License-Identifier: CERN-OHL-W-2.0
// Boot-only state operations. The protocol owner has no media/container format.
#ifndef CTRL_AECP_STATE_H
#define CTRL_AECP_STATE_H
#include "aecp.h"

struct aecp_value {
	enum aecp_change kind;
	uint16_t type, index, name;
};

// Restore is admitted only before open. Validation is shared with live SETs,
// except that formats are checked against maps in settle, after all records.
unsigned aecp_value_restore(struct aecp *, struct aecp_value, const uint8_t *, size_t);
bool aecp_value_latch(struct aecp *, struct aecp_value, uint8_t *, size_t);
unsigned aecp_map_restore(struct aecp *, struct aecp_map *, const struct aecp_mapping *, size_t);
unsigned aecp_restore_settle(struct aecp *);
bool aecp_restore_defaults(struct aecp *);
#endif

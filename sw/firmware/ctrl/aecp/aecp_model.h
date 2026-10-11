// SPDX-License-Identifier: CERN-OHL-W-2.0
// IEEE 1722.1-2021 7.2: descriptor bytes, independent of their storage format.
#ifndef CTRL_AECP_MODEL_H
#define CTRL_AECP_MODEL_H
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

struct aecp_descriptor {
	uint16_t configuration;
	uint16_t type;
	uint16_t index;
	uint16_t length;
	const uint8_t *defaults;
	uint8_t *value;
};

struct aecp_model {
	struct aecp_descriptor *descriptors;
	size_t count;
	uint16_t configurations;
};

#endif

// SPDX-License-Identifier: CERN-OHL-W-2.0
// AEMI layout 1 adapter. The portable core consumes only aecp_model.h.
#ifndef CTRL_AECP_IMAGE_H
#define CTRL_AECP_IMAGE_H
#include "aecp_model.h"

#ifdef __cplusplus
extern "C" {
#endif

// The caller supplies disjoint static storage and an immutable image, kept
// alive with the model. Failure leaves model empty. No partial model opens.
// expected_crc is the build manifest's CRC-32 of the complete packed image.
bool aecp_image_load(struct aecp_model *model, const uint8_t *image, size_t bytes,
		     uint32_t expected_crc, struct aecp_descriptor *descriptors,
		     size_t capacity, uint8_t *values, size_t value_bytes);

#ifdef __cplusplus
}
#endif
#endif

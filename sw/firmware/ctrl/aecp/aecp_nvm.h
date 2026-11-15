// SPDX-License-Identifier: CERN-OHL-W-2.0
#ifndef CTRL_AECP_NVM_H
#define CTRL_AECP_NVM_H
#include "aecp_state.h"
#include "nvm_layout3.h"
#include "nvm_state.h"

// One pending bit per record id of layout 3's space (nvm_layout3.h), whatever block the id is in: the names follow
// every other block, so their ids reach 260 at 1x1/1if and 328 at 8x8 (#920).
#define AECP_NVM_WORDS ((NVM3_ID_SPACE + 31u) / 32u)

// Generated writable-name ordinals are the existing image's name table order.
struct aecp_nvm {
	struct aecp *core;
	const struct aecp_value *names;
	size_t name_count;
	struct aecp_mapping *scratch;
	size_t scratch_count;
	struct nvm_state port;
	uint32_t pending[AECP_NVM_WORDS];
	unsigned pending_count;  // the bits set in pending: a poll with none tests no word
	bool released;
};

void aecp_nvm_init(struct aecp_nvm *, struct aecp *, const struct aecp_value *, size_t,
		   struct aecp_mapping *, size_t);
// Queue only from a protocol port. poll delivers at most one store input later.
void aecp_nvm_changed(struct aecp_nvm *, enum aecp_change, uint16_t, uint16_t);
bool aecp_nvm_poll(struct aecp_nvm *);
#endif

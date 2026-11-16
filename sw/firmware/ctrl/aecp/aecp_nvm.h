// SPDX-License-Identifier: CERN-OHL-W-2.0
#ifndef CTRL_AECP_NVM_H
#define CTRL_AECP_NVM_H
#include "aecp_state.h"
#include "nvm_state.h"

// Generated writable-name ordinals are the existing image's name table order,
// held as its runs: ordinals ordinal to ordinal + count - 1 are the names of
// descriptor type's indexes index to index + count - 1 (name 0), or with name 1
// the one descriptor's second name. aecp_shape.py derives them from that table.
struct aecp_name_run {
	uint16_t type;
	uint16_t index;
	uint16_t count;
	uint16_t ordinal;
	uint16_t name;
};

struct aecp_nvm {
	struct aecp *core;
	const struct aecp_name_run *names;
	size_t name_runs;
	struct aecp_mapping *scratch;
	size_t scratch_count;
	struct nvm_state port;
	uint32_t pending[8];
	bool released;
};

void aecp_nvm_init(struct aecp_nvm *, struct aecp *, const struct aecp_name_run *, size_t,
		   struct aecp_mapping *, size_t);
// Queue only from a protocol port. poll delivers at most one store input later.
void aecp_nvm_changed(struct aecp_nvm *, enum aecp_change, uint16_t, uint16_t);
bool aecp_nvm_poll(struct aecp_nvm *);
#endif

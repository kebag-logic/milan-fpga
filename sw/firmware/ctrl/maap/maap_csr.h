// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
// Allocation output on the existing AAF/CRF CSR interface. No register change.
#ifndef CTRL_MAAP_CSR_H
#define CTRL_MAAP_CSR_H

#include <stdbool.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

struct maap_csr_port {
	void *ctx;
	// Ordered 32-bit accesses to this interface's existing datapath window.
	// Ports must not call any protocol core synchronously (#678).
	uint32_t (*read32)(void *ctx, unsigned interface, uint32_t offset);
	void (*write32)(void *ctx, unsigned interface, uint32_t offset, uint32_t value);
};

struct maap_csr {
	struct maap_csr_port port;
	unsigned aaf_outputs;
	bool crf_output;
	// Desired controls, from the generated boot policy; only enable is gated.
	uint32_t aaf_control;
	uint32_t crf_control;
	uint32_t refused;
};

bool maap_csr_init(struct maap_csr *c, struct maap_csr_port port, unsigned aaf_outputs,
		   bool crf_output, uint32_t aaf_control, uint32_t crf_control);
// maap_allocation_fn: invalidate before programming, then publish base+index
// to each AAF output and base+aaf_outputs to CRF, finally restore admission.
// The caller exclusively owns this interface's stream provisioning window.
void maap_csr_allocation(void *ctx, unsigned interface, uint64_t base, uint16_t count, bool valid);

#ifdef __cplusplus
}
#endif
#endif

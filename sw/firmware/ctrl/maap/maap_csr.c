// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
// Existing offsets and packing: docs/reference/REGISTER_MAP.md, AAF, CRFT,
// MAAP_CTRL and 0x800 stream window. Shipping firmware never calls this port.
#include "maap_csr.h"

#include <string.h>

enum {
	AAF_CTRL = 0x654, AAF_DMLO = 0x658, AAF_DMHI = 0x65c,
	MAAP_CTRL = 0x6cc, CRFT_CTRL = 0x750, CRFT_DMLO = 0x75c, CRFT_DMHI = 0x760,
	STRM_SEL = 0x800, STRMW_DMLO = 0x81c, STRMW_DMHI = 0x820
};

bool maap_csr_init(struct maap_csr *c, struct maap_csr_port port, unsigned aaf_outputs,
		   bool crf_output, uint32_t aaf_control, uint32_t crf_control)
{
	memset(c, 0, sizeof *c);
	if (aaf_outputs > 8u || (aaf_outputs == 0u && !crf_output)) {
		return false;
	}
	c->port = port;
	c->aaf_outputs = aaf_outputs;
	c->crf_output = crf_output;
	c->aaf_control = aaf_control;
	c->crf_control = crf_control;
	return true;
}

static void write_word(struct maap_csr *c, unsigned interface, uint32_t offset, uint32_t value)
{
	c->port.write32(c->port.ctx, interface, offset, value);
}

static void address(struct maap_csr *c, unsigned interface, uint32_t lo, uint32_t hi, uint64_t mac)
{
	write_word(c, interface, lo, (uint32_t)mac);
	write_word(c, interface, hi, (uint32_t)(mac >> 32));
}

void maap_csr_allocation(void *ctx, unsigned interface, uint64_t base, uint16_t count, bool valid)
{
	struct maap_csr *c = ctx;
	write_word(c, interface, AAF_CTRL, c->aaf_control & ~1u);
	write_word(c, interface, CRFT_CTRL, c->crf_control & ~1u);
	// Select the existing CSR fallback, with only one MAAP owner.
	uint32_t fabric = c->port.read32(c->port.ctx, interface, MAAP_CTRL);
	write_word(c, interface, MAAP_CTRL, fabric & ~1u);
	if (!valid) {
		return;
	}
	if (count != c->aaf_outputs + (c->crf_output ? 1u : 0u)) {
		c->refused++;
		return;
	}
	if (c->aaf_outputs != 0u) {
		address(c, interface, AAF_DMLO, AAF_DMHI, base);
	}
	uint32_t selection = c->port.read32(c->port.ctx, interface, STRM_SEL);
	for (unsigned k = 1; k < c->aaf_outputs; ++k) {
		write_word(c, interface, STRM_SEL, 0x100u | k);
		address(c, interface, STRMW_DMLO, STRMW_DMHI, base + k);
	}
	write_word(c, interface, STRM_SEL, selection);
	if (c->crf_output) {
		address(c, interface, CRFT_DMLO, CRFT_DMHI, base + c->aaf_outputs);
	}
	write_word(c, interface, AAF_CTRL, c->aaf_control);
	write_word(c, interface, CRFT_CTRL, c->crf_control);
}

/* SPDX-License-Identifier: (GPL-2.0 OR MIT) */
/*
 * nvm_flash.c - the one blocking helper over the flash port (#665 lane F1).
 */
#include "nvm_flash.h"

int nvm_flash_wait(const struct nvm_flash *f, uint64_t timeout_us)
{
	uint64_t start = f->now_us(f->ctx);

	for (;;) {
		int busy = f->busy(f->ctx);

		if (busy == 0)
			return 1;
		if (busy < 0 || f->now_us(f->ctx) - start > timeout_us)
			return 0;
	}
}

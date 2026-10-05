/* SPDX-License-Identifier: (GPL-2.0 OR MIT) */
/*
 * nvm_flash.h - the flash port of the saved-state store (#665 lane F1).
 *
 * THIS IS THE WHOLE MEDIA PORT. The store reaches the journal slots only
 * through these five calls, so it runs unchanged over either implementation:
 *
 *   plat/nvm_flash_litespi.c  the on-chip SPI flash: reads through the
 *                             memory-mapped QSPI window, program and erase
 *                             through the LiteSPI command master (WREN, PP,
 *                             SE, RDSR), the access code of
 *                             sw/firmware/milan_baremetal/milan_baremetal.c;
 *   host/nvm_fmodel.c         the host flash model, with injectable torn
 *                             program and erase (a power cut at any step),
 *                             erase and program failures and bit flips.
 *
 * It is deliberately a port of its own and not part of the packet-mailbox
 * HAL of lane F0 (sw/firmware/ctrl/mbx/mbx_hal.h): the two are reconciled
 * later, and the seam is recorded in this module's README.
 *
 * Every call that starts a media operation RETURNS AT ONCE; busy() reports
 * when it ends. The store polls busy() once per service step and never
 * spins on it in service, so the event loop keeps running through a
 * 3 s erase (docs/design/SAVED_STATE_FASTCONNECT.md section 9.4). The
 * blocking nvm_flash_wait() below exists for the boot path and the console,
 * which run before or outside the loop.
 */
#ifndef NVM_FLASH_H
#define NVM_FLASH_H

#include <stdint.h>

struct nvm_flash {
	/* Copy len bytes at device byte address addr into dst; 0 on success. */
	int (*read)(void *ctx, uint32_t addr, uint8_t *dst, uint32_t len);
	/* Start a page program: write enable, then len bytes (1 to
	 * NVM_FLASH_PAGE) at addr, all inside one page. 0 when started. */
	int (*program)(void *ctx, uint32_t addr, const uint8_t *src, uint32_t len);
	/* Start an erase of the 64 KiB erase block holding addr. 0 when started. */
	int (*erase)(void *ctx, uint32_t addr);
	/* 1 while a program or erase is in progress, 0 once it ended, negative
	 * when the device cannot be asked. */
	int (*busy)(void *ctx);
	/* Monotonic time in microseconds; it never steps backwards. */
	uint64_t (*now_us)(void *ctx);
	void *ctx;
};

/* Poll busy() until it reads 0 or timeout_us passes: 1 when the device went
 * idle, 0 on a timeout or a fault. Blocking: boot and console only. */
int nvm_flash_wait(const struct nvm_flash *f, uint64_t timeout_us);

#endif /* NVM_FLASH_H */

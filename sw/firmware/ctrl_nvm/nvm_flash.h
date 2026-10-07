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
 * EVERY CALL RETURNS IN BOUNDED TIME. A call that starts a media operation
 * returns once the command is issued, and busy() reports when it ends. The
 * store polls busy() once per service step and never spins on it, so the
 * event loop keeps running through a 3 s erase
 * (docs/design/SAVED_STATE_FASTCONNECT.md section 9.4). A controller that
 * stops answering makes the call fail, never wait: an implementation bounds
 * every wait it has, and the call as a whole, so a controller that keeps
 * answering slowly cannot hold one call past a stated figure either.
 */
/* No synchronous callbacks (#678): a port must return before any core
 * input is dispatched by the single bare-metal event loop. A port never
 * calls back into a protocol core or the store, including on zero-delay
 * timer arms or TX completion. Interrupts defer dispatch to the loop.
 * F2 to F5 inherit this rule for every protocol port. */

#ifndef NVM_FLASH_H
#define NVM_FLASH_H

#include <stdint.h>

struct nvm_flash {
	/* Copy len bytes at device byte address addr into dst; 0 on success,
	 * nonzero when the bytes could not be read: a media fault, never a
	 * verdict on the bytes. */
	int (*read)(void *ctx, uint32_t addr, uint8_t *dst, uint32_t len);
	/* Start a page program: write enable, then len bytes (1 to
	 * NVM_FLASH_PAGE) at addr, all inside one page. 0 when started. */
	int (*program)(void *ctx, uint32_t addr, const uint8_t *src, uint32_t len);
	/* Start an erase of the 64 KiB erase block holding addr. 0 when started. */
	int (*erase)(void *ctx, uint32_t addr);
	/* 1 while a program or erase is in progress, 0 once it ended, negative
	 * when the device cannot be asked. */
	int (*busy)(void *ctx);
	/* Elapsed time in microseconds from a LOCAL counter that only counts
	 * up: never the PHC, which a gPTP step moves either way, so no clock
	 * correction lengthens or shortens a window, a backoff or a deadline.
	 * The store samples it on every service step; an implementation whose
	 * counter wraps keeps the elapsed time exact as long as it is sampled
	 * at least once per wrap (README, "The flash port"). */
	uint64_t (*now_us)(void *ctx);
	void *ctx;
};

#endif /* NVM_FLASH_H */

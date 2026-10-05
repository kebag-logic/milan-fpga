/* SPDX-License-Identifier: (GPL-2.0 OR MIT) */
/*
 * nvm_flash_litespi.h - the flash port on the on-chip SPI flash controller
 * (#665 lane F1).
 */
#ifndef NVM_FLASH_LITESPI_H
#define NVM_FLASH_LITESPI_H

#include "../nvm_flash.h"

/* Reads through the memory-mapped QSPI window; program, erase and status
 * through the LiteSPI command master; time from the fabric PHC. Program and
 * erase are refused outside the reserved journal. */
extern const struct nvm_flash nvm_flash_litespi;

/* What a CPU reset clears: the last time read. The target's startup zeroes
 * it with the rest of .bss; the host suite calls this at every modelled
 * power on. */
void nvm_flash_litespi_power_on(void);

#endif /* NVM_FLASH_LITESPI_H */

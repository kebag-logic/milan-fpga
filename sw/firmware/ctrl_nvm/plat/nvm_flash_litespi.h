/* SPDX-License-Identifier: (GPL-2.0 OR MIT) */
/*
 * nvm_flash_litespi.h - the flash port on the on-chip SPI flash controller
 * (#665 lane F1).
 */
#ifndef NVM_FLASH_LITESPI_H
#define NVM_FLASH_LITESPI_H

#include "../nvm_flash.h"

/* Reads through the memory-mapped QSPI window; program, erase and status
 * through the LiteSPI command master, every wait on it bounded; time from
 * timer0. Program and erase are refused outside the reserved journal. */
extern const struct nvm_flash nvm_flash_litespi;

/* Start the port's clock: timer0 free-running from 0xffffffff, the elapsed
 * count at zero. Call once at power on, before nvm_store_boot(); the host
 * suite calls it at every modelled power on. */
void nvm_flash_litespi_power_on(void);

#endif /* NVM_FLASH_LITESPI_H */

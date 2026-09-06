/* SPDX-License-Identifier: (GPL-2.0 OR MIT) */
/*
 * The host model behind the stub headers: the firmware translation unit is
 * compiled unchanged against these, so every address it forms lands in a
 * host array and every LiteSPI master access reaches a flash model.
 */
#ifndef NVM_HOST_H
#define NVM_HOST_H

#include <stdint.h>

#define NVM_HOST_FLASH_BYTES 0x1000000u
#define NVM_HOST_DDR_BYTES   0x100000u

extern uint8_t nvm_host_flash[NVM_HOST_FLASH_BYTES];
extern uint8_t nvm_host_ddr[NVM_HOST_DDR_BYTES];

/* Called on every Milan CSR access the firmware forms; settles the stores
 * made since the previous access and recomposes the read-only words. */
uintptr_t nvm_host_csr_base(void);
/* The firmware's cdelay(): advances model time by `cycles` at 100 MHz. */
void nvm_host_tick(int cycles);

/* The LiteSPI command-master face the stub csr.h declares. */
uint32_t nvm_host_spi_status(void);
void nvm_host_spi_cs(uint32_t v);
void nvm_host_spi_phyconfig(uint32_t v);
uint32_t nvm_host_spi_rxtx_read(void);
void nvm_host_spi_rxtx_write(uint32_t v);

#endif

/* SPDX-License-Identifier: (GPL-2.0 OR MIT) */
/*
 * The host model behind the stub headers: the firmware translation unit is
 * compiled against these, so every address it forms lands in a host array
 * and every LiteSPI master access reaches a flash model.
 *
 * Issue #419 round 3 co-simulation copy of sw/firmware/nvm_hosttest/stubs/
 * nvm_host.h. Added: the two CSR access primitives. The host build of the
 * firmware routes the BODIES of milan_read() and milan_write() here (a
 * counted substitution, stated in COMMAND_RESULTS.md), so every CSR access
 * reaches the Verilated backend at its own program point, including a
 * repeated write of an unchanged value, which a compare-on-next-access
 * model cannot see.
 */
#ifndef NVM_HOST_H
#define NVM_HOST_H

#include <stdint.h>

#define NVM_HOST_FLASH_BYTES 0x1000000u
#define NVM_HOST_DDR_BYTES   0x100000u

extern uint8_t nvm_host_flash[NVM_HOST_FLASH_BYTES];
extern uint8_t nvm_host_ddr[NVM_HOST_DDR_BYTES];

/* Retained for the unused milan_reg() helper; never dereferenced. */
uintptr_t nvm_host_csr_base(void);
/* The firmware's cdelay(): advances model time by `cycles` at 100 MHz. */
void nvm_host_tick(int cycles);

/* The CSR access primitives the host build substitutes. */
uint32_t nvm_host_csr_read(unsigned int offset);
void nvm_host_csr_write(unsigned int offset, uint32_t value);

/* The LiteSPI command-master face the stub csr.h declares. */
uint32_t nvm_host_spi_status(void);
void nvm_host_spi_cs(uint32_t v);
void nvm_host_spi_phyconfig(uint32_t v);
uint32_t nvm_host_spi_rxtx_read(void);
void nvm_host_spi_rxtx_write(uint32_t v);

#endif

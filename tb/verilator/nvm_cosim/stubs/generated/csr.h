/* SPDX-License-Identifier: (GPL-2.0 OR MIT) */
/* Stub for the LiteX-generated CSR accessors the firmware uses: the LiteSPI
 * command master, routed to the host flash model. */
#ifndef GENERATED_CSR_H
#define GENERATED_CSR_H
#include "../nvm_host.h"
#define CSR_SPIFLASH_MASTER_PHYCONFIG_LEN_OFFSET 0
#define CSR_SPIFLASH_MASTER_PHYCONFIG_WIDTH_OFFSET 8
#define CSR_SPIFLASH_MASTER_PHYCONFIG_MASK_OFFSET 16
#define CSR_SPIFLASH_MASTER_STATUS_TX_READY_OFFSET 0
#define CSR_SPIFLASH_MASTER_STATUS_RX_READY_OFFSET 1
static inline uint32_t spiflash_master_status_read(void) { return nvm_host_spi_status(); }
static inline void spiflash_master_cs_write(uint32_t v) { nvm_host_spi_cs(v); }
static inline void spiflash_master_phyconfig_write(uint32_t v) { nvm_host_spi_phyconfig(v); }
static inline uint32_t spiflash_master_rxtx_read(void) { return nvm_host_spi_rxtx_read(); }
static inline void spiflash_master_rxtx_write(uint32_t v) { nvm_host_spi_rxtx_write(v); }
#endif

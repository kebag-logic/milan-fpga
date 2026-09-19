/* SPDX-License-Identifier: (GPL-2.0 OR MIT) */
/* Issue #419 round 3: target-like stand-ins for the LiteX CSR accessors the
 * writer uses, as fixed-address MMIO, so an RV32 compile of either writer
 * measures its own code and not a host model's calls. Sizes only. */
#ifndef GENERATED_CSR_H
#define GENERATED_CSR_H
#include <stdint.h>
#define CSR_SPIFLASH_MASTER_PHYCONFIG_LEN_OFFSET 0
#define CSR_SPIFLASH_MASTER_PHYCONFIG_WIDTH_OFFSET 8
#define CSR_SPIFLASH_MASTER_PHYCONFIG_MASK_OFFSET 16
#define CSR_SPIFLASH_MASTER_STATUS_TX_READY_OFFSET 0
#define CSR_SPIFLASH_MASTER_STATUS_RX_READY_OFFSET 1
#define SPIM(o) (*(volatile uint32_t *)(0xf0003000u + (o)))
static inline uint32_t spiflash_master_status_read(void) { return SPIM(0x0c); }
static inline void spiflash_master_cs_write(uint32_t v) { SPIM(0x00) = v; }
static inline void spiflash_master_phyconfig_write(uint32_t v) { SPIM(0x04) = v; }
static inline uint32_t spiflash_master_rxtx_read(void) { return SPIM(0x08); }
static inline void spiflash_master_rxtx_write(uint32_t v) { SPIM(0x08) = v; }
#endif

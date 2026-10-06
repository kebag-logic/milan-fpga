/* SPDX-License-Identifier: (GPL-2.0 OR MIT) */
/* The LiteSPI command-master and timer0 accessors as LiteX generates them,
 * at fixed MMIO addresses, for the RV32 freestanding build of the host suite
 * (#665 lane F1). The addresses are placeholders: this build proves the port
 * compiles freestanding for RV32I with no heap, not the SoC's map. */
#ifndef GENERATED_CSR_H
#define GENERATED_CSR_H
#include <stdint.h>
#define CSR_SPIFLASH_MASTER_PHYCONFIG_LEN_OFFSET 0
#define CSR_SPIFLASH_MASTER_PHYCONFIG_WIDTH_OFFSET 8
#define CSR_SPIFLASH_MASTER_PHYCONFIG_MASK_OFFSET 16
#define CSR_SPIFLASH_MASTER_STATUS_TX_READY_OFFSET 0
#define CSR_SPIFLASH_MASTER_STATUS_RX_READY_OFFSET 1
#define CSR_SPIFLASH_MASTER_BASE 0xf0003000u
static inline uint32_t csr_rd(uint32_t a) { return *(volatile uint32_t *)a; }
static inline void csr_wr(uint32_t a, uint32_t v) { *(volatile uint32_t *)a = v; }
static inline void spiflash_master_cs_write(uint32_t v) { csr_wr(CSR_SPIFLASH_MASTER_BASE + 0x0u, v); }
static inline void spiflash_master_phyconfig_write(uint32_t v) { csr_wr(CSR_SPIFLASH_MASTER_BASE + 0x4u, v); }
static inline void spiflash_master_rxtx_write(uint32_t v) { csr_wr(CSR_SPIFLASH_MASTER_BASE + 0x8u, v); }
static inline uint32_t spiflash_master_rxtx_read(void) { return csr_rd(CSR_SPIFLASH_MASTER_BASE + 0x8u); }
static inline uint32_t spiflash_master_status_read(void) { return csr_rd(CSR_SPIFLASH_MASTER_BASE + 0xcu); }
#define CSR_TIMER0_BASE 0xf0003800u
static inline void timer0_load_write(uint32_t v) { csr_wr(CSR_TIMER0_BASE + 0x0u, v); }
static inline void timer0_reload_write(uint32_t v) { csr_wr(CSR_TIMER0_BASE + 0x4u, v); }
static inline void timer0_en_write(uint32_t v) { csr_wr(CSR_TIMER0_BASE + 0x8u, v); }
static inline void timer0_update_value_write(uint32_t v) { csr_wr(CSR_TIMER0_BASE + 0xcu, v); }
static inline uint32_t timer0_value_read(void) { return csr_rd(CSR_TIMER0_BASE + 0x10u); }
#endif

/* SPDX-License-Identifier: (GPL-2.0 OR MIT) */
/*
 * nvm_flash_litespi.c - the flash port on the on-chip SPI flash controller
 * (#665 lane F1).
 *
 * The access code is the shipping writer's
 * (sw/firmware/milan_baremetal/milan_baremetal.c: nvm_spi_open, nvm_spi_xfer,
 * nvm_spi_close, nvm_flash_status, nvm_flash_write_enable,
 * nvm_flash_command, gettime_ns), ported behind the five calls of
 * nvm_flash.h: sw/litex/milan_soc.py instantiates add_spi_flash(mode="1x",
 * with_master=True), so the CPU reads the device through the memory-mapped
 * window and drives write enable, page program, sector erase and status
 * through the CSR command master, one byte at a time. What changed in the
 * port: an erase or a program only STARTS here and busy() reports its end,
 * so the store polls instead of spinning; program and erase are refused
 * outside the reserved journal; and time never steps backwards.
 *
 * Time is the fabric PHC, as the shipping writer reads it. A gPTP step
 * forward can end a wait early: the attempt then fails and is retried 1 s
 * later, and nothing is lost; a step backwards is held at the last value.
 */
#include <stdint.h>

#include <generated/csr.h>
#include <generated/mem.h>
#include <hw/common.h>

#include "../nvm_shape.h"
#include "nvm_flash_litespi.h"

#define LS_CMD_WREN 0x06u
#define LS_CMD_RDSR 0x05u
#define LS_CMD_SE   0xd8u
#define LS_CMD_PP   0x02u
#define LS_SR_WIP   0x01u
#define LS_PAGE     256u
#define LS_BLOCK    0x10000u

#define LS_PTP_CMD       0x520u
#define LS_PTP_TOD_RD_LO 0x530u
#define LS_PTP_TOD_RD_HI 0x534u
#define LS_PTP_SNAPSHOT  0x4u

static uint64_t ls_last_us;

static uint32_t ls_csr_read(unsigned int offset)
{
	return *(volatile uint32_t *)(MILAN_CSR_BASE + offset);
}

static void ls_csr_write(unsigned int offset, uint32_t value)
{
	*(volatile uint32_t *)(MILAN_CSR_BASE + offset) = value;
#if defined(__riscv)
	__asm__ volatile("fence iorw, iorw" ::: "memory");
#endif
}

static void ls_open(void)
{
	while (spiflash_master_status_read() &
	       (1u << CSR_SPIFLASH_MASTER_STATUS_RX_READY_OFFSET))
		spiflash_master_rxtx_read();
	spiflash_master_phyconfig_write(
		(8u << CSR_SPIFLASH_MASTER_PHYCONFIG_LEN_OFFSET) |
		(1u << CSR_SPIFLASH_MASTER_PHYCONFIG_WIDTH_OFFSET) |
		(1u << CSR_SPIFLASH_MASTER_PHYCONFIG_MASK_OFFSET));
	spiflash_master_cs_write(1);
}

static uint8_t ls_xfer(uint8_t out)
{
	while (!(spiflash_master_status_read() &
		 (1u << CSR_SPIFLASH_MASTER_STATUS_TX_READY_OFFSET)))
		;
	spiflash_master_rxtx_write(out);
	while (!(spiflash_master_status_read() &
		 (1u << CSR_SPIFLASH_MASTER_STATUS_RX_READY_OFFSET)))
		;
	return (uint8_t)spiflash_master_rxtx_read();
}

static void ls_close(void)
{
	spiflash_master_cs_write(0);
}

static void ls_write_enable(void)
{
	ls_open();
	ls_xfer(LS_CMD_WREN);
	ls_close();
}

/* Opens a command with a 24-bit address; the caller continues or closes. */
static void ls_command(uint8_t cmd, uint32_t addr)
{
	ls_open();
	ls_xfer(cmd);
	ls_xfer((uint8_t)(addr >> 16));
	ls_xfer((uint8_t)(addr >> 8));
	ls_xfer((uint8_t)addr);
}

/* Program and erase stay inside the reserved journal. */
static int ls_in_journal(uint32_t addr, uint32_t len)
{
	return addr >= MILAN_FLASH_JOURNAL_OFFSET &&
	       len <= MILAN_FLASH_JOURNAL_SIZE &&
	       addr - MILAN_FLASH_JOURNAL_OFFSET <= MILAN_FLASH_JOURNAL_SIZE - len;
}

static int ls_read(void *ctx, uint32_t addr, uint8_t *dst, uint32_t len)
{
	const volatile uint8_t *src = (const volatile uint8_t *)(SPIFLASH_BASE + addr);
	uint32_t i;

	(void)ctx;
	if (addr >= SPIFLASH_SIZE || len > SPIFLASH_SIZE - addr)
		return -1;
	for (i = 0; i < len; ++i)
		dst[i] = src[i];
	return 0;
}

static int ls_program(void *ctx, uint32_t addr, const uint8_t *src, uint32_t len)
{
	uint32_t i;

	(void)ctx;
	if (len == 0 || len > LS_PAGE || (addr % LS_PAGE) + len > LS_PAGE ||
	    !ls_in_journal(addr, len))
		return -1;
	ls_write_enable();
	ls_command(LS_CMD_PP, addr);
	for (i = 0; i < len; ++i)
		ls_xfer(src[i]);
	ls_close();
	return 0;
}

static int ls_erase(void *ctx, uint32_t addr)
{
	uint32_t base = addr & ~(LS_BLOCK - 1u);

	(void)ctx;
	if (!ls_in_journal(base, LS_BLOCK))
		return -1;
	ls_write_enable();
	ls_command(LS_CMD_SE, base);
	ls_close();
	return 0;
}

/* RDSR, as the shipping writer reads it: the status register repeats after
 * the command byte, and the fourth byte is taken. */
static int ls_busy(void *ctx)
{
	uint8_t status;

	(void)ctx;
	ls_open();
	ls_xfer(LS_CMD_RDSR);
	ls_xfer(0);
	ls_xfer(0);
	status = ls_xfer(0);
	ls_close();
	return (status & LS_SR_WIP) ? 1 : 0;
}

static uint64_t ls_now_us(void *ctx)
{
	uint32_t hi1;
	uint32_t hi2;
	uint32_t lo;
	uint64_t now;

	(void)ctx;
	ls_csr_write(LS_PTP_CMD, LS_PTP_SNAPSHOT);
	cdelay(128);
	do {
		hi1 = ls_csr_read(LS_PTP_TOD_RD_HI);
		lo = ls_csr_read(LS_PTP_TOD_RD_LO);
		hi2 = ls_csr_read(LS_PTP_TOD_RD_HI);
	} while (hi1 != hi2);
	now = (((uint64_t)hi2 << 32) | lo) / 1000u;
	if (now < ls_last_us)
		return ls_last_us;
	ls_last_us = now;
	return now;
}

void nvm_flash_litespi_power_on(void)
{
	ls_last_us = 0;
}

const struct nvm_flash nvm_flash_litespi = {
	ls_read, ls_program, ls_erase, ls_busy, ls_now_us, 0,
};

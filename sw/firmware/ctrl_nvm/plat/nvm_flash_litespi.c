/* SPDX-License-Identifier: (GPL-2.0 OR MIT) */
/*
 * nvm_flash_litespi.c - the flash port on the on-chip SPI flash controller
 * (#665 lane F1).
 *
 * The access code is the shipping writer's
 * (sw/firmware/milan_baremetal/milan_baremetal.c: nvm_spi_open, nvm_spi_xfer,
 * nvm_spi_close, nvm_flash_status, nvm_flash_write_enable,
 * nvm_flash_command), ported behind the five calls of nvm_flash.h:
 * sw/litex/milan_soc.py instantiates add_spi_flash(mode="1x",
 * with_master=True), so the CPU reads the device through the memory-mapped
 * window and drives write enable, page program, sector erase and status
 * through the CSR command master, one byte at a time. What changed in the
 * port:
 *   - an erase or a program only STARTS here and busy() reports its end, so
 *     the store polls instead of spinning;
 *   - every wait on the command master is bounded: LS_POLL_MAX status reads
 *     without the readiness it waits for end the call with a failure and
 *     chip select released. That is the no-progress rule of
 *     docs/design/SAVED_STATE_MATERIALIZATION.md section 8.8: the bound
 *     counts reads without progress;
 *   - every call is bounded too: a master that is slow but moving keeps each
 *     wait inside LS_POLL_MAX, so a call also fails, chip select released,
 *     once it has run LS_CALL_US of timer0 time. The check runs every
 *     LS_LATE_EVERY status reads that find the master not ready, counted
 *     over the whole call;
 *   - program and erase are refused outside the reserved journal;
 *   - time is timer0, not the PHC.
 *
 * TIME. The shipping writer reads the fabric PHC, which a gPTP step moves
 * either way; a grandmaster restart moves it back by the old grandmaster's
 * whole uptime (docs/design/PRESENTATION_TIME_WRAP.md, "The causal chain").
 * The store's windows and deadlines need elapsed time, so this port owns the
 * LiteX timer0: free-running down from 0xffffffff at the system clock
 * (CONFIG_CLOCK_FREQUENCY), its 32-bit difference accumulated into 64 bits
 * at every read. A read at least once per wrap (2^32 clocks, 42.9 s at
 * 100 MHz) keeps the elapsed time exact, and the store reads it on every
 * service step. Nothing else in the image may reprogram timer0.
 */
#include <stdint.h>

#include <generated/csr.h>
#include <generated/mem.h>
#include <generated/soc.h>

#include "../nvm_shape.h"
#include "nvm_flash_litespi.h"

#define LS_CMD_WREN 0x06u
#define LS_CMD_RDSR 0x05u
#define LS_CMD_SE   0xd8u
#define LS_CMD_PP   0x02u
#define LS_SR_WIP   0x01u
#define LS_PAGE     256u
#define LS_BLOCK    0x10000u
#define LS_TX_READY (1u << CSR_SPIFLASH_MASTER_STATUS_TX_READY_OFFSET)
#define LS_RX_READY (1u << CSR_SPIFLASH_MASTER_STATUS_RX_READY_OFFSET)
/* Status reads one wait makes without the readiness it waits for before the
 * call fails. One byte is 8 clocks of the 12.5 MHz link, 0.64 us; at two
 * system clocks or more per CSR read, 4,096 reads are 82 us or more. */
#define LS_POLL_MAX 4096u
/* The longest one call runs, in timer0 time: a page program clocks 261
 * bytes, 167 us on the 1x link, and the deadline is twelve times that. */
#define LS_CALL_US 2000u
#define LS_LATE_EVERY 64u
#define LS_TICKS_PER_US (CONFIG_CLOCK_FREQUENCY / 1000000u)

_Static_assert(CONFIG_CLOCK_FREQUENCY % 1000000u == 0u, "a whole number of clocks per us");

static uint32_t ls_tick_last;   /* timer0 at the last read */
static uint64_t ls_ticks;       /* system clocks since nvm_flash_litespi_power_on */
static uint32_t ls_call_start;  /* timer0 when this call started */
static uint32_t ls_waited;      /* status reads this call found the master not ready */

static uint32_t ls_timer(void)
{
	timer0_update_value_write(1);
	return timer0_value_read();
}

static void ls_call_begin(void)
{
	ls_call_start = ls_timer();
	ls_waited = 0;
}

/* One more status read found the master not ready: 1 once this call has run
 * past LS_CALL_US. The timer counts down; the difference is wrap-safe. */
static int ls_late(void)
{
	if (++ls_waited % LS_LATE_EVERY)
		return 0;
	return (uint32_t)(ls_call_start - ls_timer()) > LS_CALL_US * LS_TICKS_PER_US;
}

/* 1 once the master shows `bit`; 0 after LS_POLL_MAX reads without it, or
 * once the call is late. */
static int ls_ready(uint32_t bit)
{
	uint32_t n;

	for (n = 0; n < LS_POLL_MAX; ++n) {
		if (spiflash_master_status_read() & bit)
			return 1;
		if (ls_late())
			return 0;
	}
	return 0;
}

/* Drain what the master still holds, then select the device; -1 when its
 * receive side never empties. */
static int ls_open(void)
{
	uint32_t n = 0;

	while (spiflash_master_status_read() & LS_RX_READY) {
		if (++n > LS_POLL_MAX || ls_late())
			return -1;
		spiflash_master_rxtx_read();
	}
	spiflash_master_phyconfig_write(
		(8u << CSR_SPIFLASH_MASTER_PHYCONFIG_LEN_OFFSET) |
		(1u << CSR_SPIFLASH_MASTER_PHYCONFIG_WIDTH_OFFSET) |
		(1u << CSR_SPIFLASH_MASTER_PHYCONFIG_MASK_OFFSET));
	spiflash_master_cs_write(1);
	return 0;
}

/* One byte out; the byte clocked in (0 to 255), or -1 when the master stalls. */
static int ls_xfer(uint8_t out)
{
	if (!ls_ready(LS_TX_READY))
		return -1;
	spiflash_master_rxtx_write(out);
	if (!ls_ready(LS_RX_READY))
		return -1;
	return (int)(spiflash_master_rxtx_read() & 0xffu);
}

static void ls_close(void)
{
	spiflash_master_cs_write(0);
}

/* One chip-select window: n command bytes, then len data bytes; 0 when every
 * byte went. On a stall the device is deselected and -1 returned. A command
 * cut short there reaches at most the slot being written, never the
 * authoritative one, and the store fails that attempt. */
static int ls_window(const uint8_t *cmd, uint32_t n, const uint8_t *data, uint32_t len)
{
	uint32_t i;
	int ok = ls_open() == 0;

	for (i = 0; ok && i < n + len; ++i)
		ok = ls_xfer(i < n ? cmd[i] : data[i - n]) >= 0;
	ls_close();
	return ok ? 0 : -1;
}

/* A command byte and a 24-bit address. */
static void ls_command(uint8_t *cmd, uint8_t op, uint32_t addr)
{
	cmd[0] = op;
	cmd[1] = (uint8_t)(addr >> 16);
	cmd[2] = (uint8_t)(addr >> 8);
	cmd[3] = (uint8_t)addr;
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

static const uint8_t ls_wren = LS_CMD_WREN;

static int ls_program(void *ctx, uint32_t addr, const uint8_t *src, uint32_t len)
{
	uint8_t cmd[4];

	(void)ctx;
	if (len == 0 || len > LS_PAGE || (addr % LS_PAGE) + len > LS_PAGE ||
	    !ls_in_journal(addr, len))
		return -1;
	ls_call_begin();
	ls_command(cmd, LS_CMD_PP, addr);
	if (ls_window(&ls_wren, 1u, 0, 0u) || ls_window(cmd, 4u, src, len))
		return -1;
	return 0;
}

static int ls_erase(void *ctx, uint32_t addr)
{
	uint32_t base = addr & ~(LS_BLOCK - 1u);
	uint8_t cmd[4];

	(void)ctx;
	if (!ls_in_journal(base, LS_BLOCK))
		return -1;
	ls_call_begin();
	ls_command(cmd, LS_CMD_SE, base);
	if (ls_window(&ls_wren, 1u, 0, 0u) || ls_window(cmd, 4u, 0, 0u))
		return -1;
	return 0;
}

/* RDSR, as the shipping writer reads it: the status register repeats after
 * the command byte, and the fourth byte is taken. */
static int ls_busy(void *ctx)
{
	int status;
	unsigned int i;

	(void)ctx;
	ls_call_begin();
	status = ls_open();
	for (i = 0; i < 4u && status >= 0; ++i)
		status = ls_xfer(i ? 0u : LS_CMD_RDSR);
	ls_close();
	if (status < 0)
		return -1;
	return (status & LS_SR_WIP) ? 1 : 0;
}

static uint64_t ls_now_us(void *ctx)
{
	uint32_t v;

	(void)ctx;
	v = ls_timer();
	/* the timer counts down; the difference is wrap-safe in 32 bits */
	ls_ticks += (uint32_t)(ls_tick_last - v);
	ls_tick_last = v;
	return ls_ticks / LS_TICKS_PER_US;
}

void nvm_flash_litespi_power_on(void)
{
	timer0_en_write(0);
	timer0_load_write(0xffffffffu);
	timer0_reload_write(0xffffffffu);
	timer0_en_write(1);
	ls_tick_last = 0xffffffffu;
	ls_ticks = 0;
}

const struct nvm_flash nvm_flash_litespi = {
	ls_read, ls_program, ls_erase, ls_busy, ls_now_us, 0,
};

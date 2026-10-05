/* SPDX-License-Identifier: (GPL-2.0 OR MIT) */
/*
 * litespi_model.c - the LiteSPI command master over the flash model (#665
 * lane F1). A chip-select window collects the bytes the firmware clocks out;
 * raising chip select executes the command against the flash model, as the
 * N25Q128 executes WREN, PP and SE on the deselect edge. RDSR answers from
 * the model's busy state on every byte after the command. Every CSR access
 * costs model time, so a firmware that polls is seen to spend it.
 */
#include <string.h>

#include <generated/soc.h>

#include "litespi_model.h"
#include "nvm_fmodel.h"

#define LM_CMD_WREN 0x06u
#define LM_CMD_RDSR 0x05u
#define LM_CMD_SE   0xd8u
#define LM_CMD_PP   0x02u
#define LM_CSR_WORDS 0x400u
#define LM_TOD_RD_LO (0x530u / 4u)
#define LM_TOD_RD_HI (0x534u / 4u)
#define LM_TX_READY 1u
#define LM_RX_READY 2u
/* One CSR access on the model's bus. timer0 counts the shape's system clock,
 * CONFIG_CLOCK_FREQUENCY hertz, which the suite writes from its config. */
#define LM_CSR_NS 40u
#define LM_NS_PER_S 1000000000u
/* The PHC's time at model time zero: a domain time well past any step. */
#define LM_PHC_EPOCH_NS 1700000000000000000ull

struct lm_state {
	uint8_t buf[4u + 256u + 8u];
	unsigned int len;
	int cs;
	int wel;
	int rx_pending;
	uint8_t resp;
	/* the stall armed, and the wait in progress */
	enum litespi_stall stall;
	unsigned int stall_count;
	unsigned int stall_skip;
	unsigned int stall_polls;
	enum litespi_stall wait;
	int wait_stalled;
	unsigned int wait_withheld;
	/* timer0 */
	uint32_t t_load;
	uint32_t t_reload;
	uint32_t t_value;
	int t_en;
	uint64_t t_start_ns;
	int64_t phc_step_ns;
	struct litespi_model_count n;
};

static const struct lm_state lm_reset_value;
static struct lm_state lm;
static uint32_t lm_csr[LM_CSR_WORDS];

void litespi_model_reset(void)
{
	lm = lm_reset_value;
}

const struct litespi_model_count *litespi_model_count(void)
{
	return &lm.n;
}

void litespi_model_stall(enum litespi_stall kind, unsigned int count, unsigned int skip,
			 unsigned int polls)
{
	lm.stall = kind;
	lm.stall_count = count;
	lm.stall_skip = skip;
	lm.stall_polls = polls;
}

/* A status read waits for TX, for RX, or (before a select) for the drain. */
static enum litespi_stall lm_kind(void)
{
	if (!lm.cs)
		return LITESPI_STALL_DRAIN;
	return lm.rx_pending ? LITESPI_STALL_RX : LITESPI_STALL_TX;
}

/* 1 when the wait that starts now is one the stall withholds. */
static int lm_take(enum litespi_stall kind)
{
	if (lm.stall != kind || lm.stall_count == 0)
		return 0;
	if (lm.stall_skip) {
		lm.stall_skip--;
		return 0;
	}
	if (--lm.stall_count == 0)
		lm.stall = LITESPI_STALL_NONE;
	lm.n.stalled++;
	return 1;
}

/* Any access but a status read ends the wait, except the reads of a drain. */
static void lm_end_wait(void)
{
	lm.wait = LITESPI_STALL_NONE;
	lm.wait_stalled = 0;
}

uint32_t litespi_model_status(void)
{
	enum litespi_stall kind = lm_kind();
	uint32_t st = LM_TX_READY | (lm.rx_pending ? LM_RX_READY : 0u);

	nvm_fmodel_advance_ns(LM_CSR_NS);
	if (kind != lm.wait) {
		lm.wait = kind;
		lm.wait_withheld = 0;
		lm.wait_stalled = lm_take(kind);
	}
	if (!lm.wait_stalled)
		return st;
	if (lm.stall_polls && lm.wait_withheld >= lm.stall_polls) {
		lm.wait_stalled = 0;
		return st;
	}
	if (lm.wait_withheld >= LITESPI_HANG_POLLS) {
		lm.n.hung++;
		lm.wait_stalled = 0;
		return st;
	}
	lm.wait_withheld++;
	if (lm.wait_withheld > lm.n.max_withheld)
		lm.n.max_withheld = lm.wait_withheld;
	if (kind == LITESPI_STALL_TX)
		return st & ~LM_TX_READY;
	if (kind == LITESPI_STALL_RX)
		return st & ~LM_RX_READY;
	return st | LM_RX_READY;
}

void litespi_model_phyconfig(uint32_t v)
{
	(void)v;
	nvm_fmodel_advance_ns(LM_CSR_NS);
	lm_end_wait();
}

static uint32_t lm_addr(void)
{
	return ((uint32_t)lm.buf[1] << 16) | ((uint32_t)lm.buf[2] << 8) | lm.buf[3];
}

static void lm_execute(void)
{
	if (lm.len == 0)
		return;
	lm.n.commands++;
	switch (lm.buf[0]) {
	case LM_CMD_WREN:
		lm.n.wren++;
		lm.wel = 1;
		return;
	case LM_CMD_RDSR:
		lm.n.rdsr++;
		return;
	case LM_CMD_SE:
	case LM_CMD_PP:
		break;
	default:
		lm.n.unknown++;
		return;
	}
	if (!lm.wel)
		lm.n.no_wel++;
	else if (lm.len < 4u + (lm.buf[0] == LM_CMD_PP ? 1u : 0u))
		lm.n.short_cmd++;
	else if (lm.buf[0] == LM_CMD_SE && nvm_fmodel_erase(0, lm_addr()))
		lm.n.refused++;
	else if (lm.buf[0] == LM_CMD_PP && nvm_fmodel_program(0, lm_addr(), lm.buf + 4, lm.len - 4u))
		lm.n.refused++;
	if (lm.buf[0] == LM_CMD_SE)
		lm.n.se++;
	else
		lm.n.pp++;
	lm.wel = 0;
}

void litespi_model_cs(uint32_t v)
{
	nvm_fmodel_advance_ns(LM_CSR_NS);
	lm_end_wait();
	if (lm.cs && !v)
		lm_execute();
	lm.cs = v != 0;
	lm.len = 0;
}

void litespi_model_rxtx_write(uint32_t v)
{
	nvm_fmodel_advance_ns(LM_CSR_NS);
	lm_end_wait();
	if (lm.cs && lm.len < sizeof(lm.buf))
		lm.buf[lm.len++] = (uint8_t)v;
	if (lm.len > 1u && lm.buf[0] == LM_CMD_RDSR)
		lm.resp = (uint8_t)(nvm_fmodel_busy(0) == 0 ? 0x00u : 0x01u);
	else
		lm.resp = 0xffu;
	lm.rx_pending = 1;
}

uint32_t litespi_model_rxtx_read(void)
{
	nvm_fmodel_advance_ns(LM_CSR_NS);
	if (lm.wait != LITESPI_STALL_DRAIN)
		lm_end_wait();
	lm.rx_pending = 0;
	return lm.resp;
}

/* The system clocks in `ns` of model time: whole seconds, then the rest,
 * exact at any clock in hertz. */
static uint64_t lm_clocks(uint64_t ns)
{
	return ns / LM_NS_PER_S * CONFIG_CLOCK_FREQUENCY +
	       ns % LM_NS_PER_S * CONFIG_CLOCK_FREQUENCY / LM_NS_PER_S;
}

/* LiteX's timer: enabled, it counts down from load, and from zero it
 * reloads; disabled, it holds load. */
static uint32_t lm_timer_now(void)
{
	uint64_t n;

	if (!lm.t_en)
		return lm.t_load;
	n = lm_clocks(nvm_fmodel_now_ns() - lm.t_start_ns);
	if (n <= lm.t_load)
		return lm.t_load - (uint32_t)n;
	return lm.t_reload - (uint32_t)((n - lm.t_load - 1u) % ((uint64_t)lm.t_reload + 1u));
}

void litespi_model_timer(enum litespi_timer_reg reg, uint32_t v)
{
	nvm_fmodel_advance_ns(LM_CSR_NS);
	switch (reg) {
	case LITESPI_TIMER_LOAD:
		lm.t_load = v;
		break;
	case LITESPI_TIMER_RELOAD:
		lm.t_reload = v;
		break;
	case LITESPI_TIMER_EN:
		if (v && !lm.t_en)
			lm.t_start_ns = nvm_fmodel_now_ns();
		lm.t_en = v != 0;
		break;
	default:
		lm.t_value = lm_timer_now();
		break;
	}
}

uint32_t litespi_model_timer_value(void)
{
	nvm_fmodel_advance_ns(LM_CSR_NS);
	return lm.t_value;
}

uintptr_t litespi_model_csr_base(void)
{
	uint64_t ns = LM_PHC_EPOCH_NS + nvm_fmodel_now_ns() + (uint64_t)lm.phc_step_ns;

	lm_csr[LM_TOD_RD_LO] = (uint32_t)ns;
	lm_csr[LM_TOD_RD_HI] = (uint32_t)(ns >> 32);
	return (uintptr_t)lm_csr;
}

void litespi_model_phc_step(int64_t ms)
{
	lm.phc_step_ns += ms * 1000000;
}

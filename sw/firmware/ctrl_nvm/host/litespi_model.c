/* SPDX-License-Identifier: (GPL-2.0 OR MIT) */
/*
 * litespi_model.c - the LiteSPI command master over the flash model (#665
 * lane F1). A chip-select window collects the bytes the firmware clocks out;
 * raising chip select executes the command against the flash model, as the
 * N25Q128 executes WREN, PP and SE on the deselect edge. RDSR answers from
 * the model's busy state on every byte after the command.
 */
#include <string.h>

#include "litespi_model.h"
#include "nvm_fmodel.h"

#define LM_CMD_WREN 0x06u
#define LM_CMD_RDSR 0x05u
#define LM_CMD_SE   0xd8u
#define LM_CMD_PP   0x02u
#define LM_CSR_WORDS 0x400u
#define LM_TOD_RD_LO (0x530u / 4u)
#define LM_TOD_RD_HI (0x534u / 4u)

struct lm_state {
	uint8_t buf[4u + 256u + 8u];
	unsigned int len;
	int cs;
	int wel;
	int rx_pending;
	uint8_t resp;
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

uint32_t litespi_model_status(void)
{
	return 1u | ((uint32_t)lm.rx_pending << 1);
}

void litespi_model_phyconfig(uint32_t v)
{
	(void)v;
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
	if (lm.cs && !v)
		lm_execute();
	lm.cs = v != 0;
	lm.len = 0;
}

void litespi_model_rxtx_write(uint32_t v)
{
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
	lm.rx_pending = 0;
	return lm.resp;
}

uintptr_t litespi_model_csr_base(void)
{
	uint64_t ns = nvm_fmodel_now_us() * 1000u;

	lm_csr[LM_TOD_RD_LO] = (uint32_t)ns;
	lm_csr[LM_TOD_RD_HI] = (uint32_t)(ns >> 32);
	return (uintptr_t)lm_csr;
}

void litespi_model_cdelay(int cycles)
{
	nvm_fmodel_advance_us((uint64_t)(cycles > 0 ? cycles : 0) / 100u + 1u);
}

/* SPDX-License-Identifier: (GPL-2.0 OR MIT) */
/*
 * litespi_model.h - the LiteSPI command master and the CSR window, modelled
 * on the host over the flash model, so plat/nvm_flash_litespi.c runs here
 * unchanged against the stub headers in host/stubs (#665 lane F1).
 */
#ifndef LITESPI_MODEL_H
#define LITESPI_MODEL_H

#include <stdint.h>

uint32_t litespi_model_status(void);
void litespi_model_cs(uint32_t v);
void litespi_model_phyconfig(uint32_t v);
uint32_t litespi_model_rxtx_read(void);
void litespi_model_rxtx_write(uint32_t v);
/* The CSR window base; every access recomposes the PHC words from model time. */
uintptr_t litespi_model_csr_base(void);
/* The firmware's busy-wait: model time at 100 MHz. */
void litespi_model_cdelay(int cycles);

struct litespi_model_count {
	unsigned int commands;      /* chip-select windows that carried a command */
	unsigned int wren;
	unsigned int pp;
	unsigned int se;
	unsigned int rdsr;
	unsigned int no_wel;        /* a PP or SE without a write enable before it */
	unsigned int short_cmd;     /* a PP or SE whose address was incomplete */
	unsigned int refused;       /* a PP or SE the flash model refused */
	unsigned int unknown;
};

void litespi_model_reset(void);
const struct litespi_model_count *litespi_model_count(void);

#endif /* LITESPI_MODEL_H */

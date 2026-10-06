/* SPDX-License-Identifier: (GPL-2.0 OR MIT) */
/*
 * litespi_model.h - the LiteSPI command master, timer0 and the PHC, modelled
 * on the host over the flash model, so plat/nvm_flash_litespi.c runs here
 * unchanged against the stub headers in host/stubs (#665 lane F1).
 *
 * THE STALLS. A status read can withhold the master's TX or RX readiness,
 * or report a byte to drain that never drains, as a controller that stops
 * answering would. A stall applies to the waits of its kind: `skip` of them
 * pass untouched, then each of the next `count` is withheld for `polls`
 * status reads (0: for as long as the firmware keeps asking). A wait that is
 * still asked after LITESPI_HANG_POLLS withheld reads is a firmware that
 * would spin for ever: the model counts it as hung and lets it go, so the
 * run ends and reports it instead of hanging.
 */
#ifndef LITESPI_MODEL_H
#define LITESPI_MODEL_H

#include <stdint.h>

#define LITESPI_HANG_POLLS 1000000u

enum litespi_stall {
	LITESPI_STALL_NONE = 0,
	LITESPI_STALL_TX,           /* TX ready withheld: the byte cannot go */
	LITESPI_STALL_RX,           /* RX ready withheld: the byte never comes back */
	LITESPI_STALL_DRAIN         /* RX ready with nothing behind it, before a select */
};

enum litespi_timer_reg {
	LITESPI_TIMER_LOAD = 0,
	LITESPI_TIMER_RELOAD,
	LITESPI_TIMER_EN,
	LITESPI_TIMER_UPDATE
};

uint32_t litespi_model_status(void);
void litespi_model_cs(uint32_t v);
void litespi_model_phyconfig(uint32_t v);
uint32_t litespi_model_rxtx_read(void);
void litespi_model_rxtx_write(uint32_t v);
/* timer0 at the system clock, over model time. */
void litespi_model_timer(enum litespi_timer_reg reg, uint32_t v);
uint32_t litespi_model_timer_value(void);
/* The CSR window base; every access recomposes the PHC words from model
 * time, a fixed epoch and every step applied. */
uintptr_t litespi_model_csr_base(void);
/* A gPTP step: the PHC moves by ms, either way; model time does not. */
void litespi_model_phc_step(int64_t ms);
void litespi_model_stall(enum litespi_stall kind, unsigned int count, unsigned int skip,
			 unsigned int polls);

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
	unsigned int stalled;       /* waits the stall withheld */
	unsigned int max_withheld;  /* the most status reads one wait was withheld */
	unsigned int hung;          /* waits still asked after LITESPI_HANG_POLLS */
};

void litespi_model_reset(void);
const struct litespi_model_count *litespi_model_count(void);

#endif /* LITESPI_MODEL_H */

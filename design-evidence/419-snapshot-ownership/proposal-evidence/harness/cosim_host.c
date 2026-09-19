/* SPDX-License-Identifier: (GPL-2.0 OR MIT) */
/*
 * cosim_host.c: issue #419 round 3 co-simulation host, derived from
 * sw/firmware/nvm_hosttest/nvm_host.c.
 *
 * KEPT from the repository model, unchanged in behaviour: the QSPI array and
 * the LiteSPI command-master/N25Q model (WREN, SE, PP, RDSR, busy time, the
 * erase/program/verify fault injections), the model clock the firmware's own
 * busy waits advance, the idle-hook loop, the console dispatch and the
 * reserved-window byte array.
 *
 * REPLACED: the repository's C model of KL_nvm_backend. Every PP_NVM_* access
 * the firmware makes is forwarded to the Verilated backend (tracked or
 * prototype) in cosim_bridge.cpp, and PP_STAT is composed from the RTL the
 * way milan_csr.sv:2133-2140 composes it. PP_CTRL[1] drives the real donor
 * manager's restore_go. Nothing the firmware decides is decided on model
 * state: status, dirty, ownership and verdicts are all RTL outputs.
 *
 * ONE CLOCK. Model nanoseconds are the master; the RTL is advanced to the
 * model time before every access (one backend cycle = COSIM_NS_PER_CYCLE),
 * and an access that itself takes a backend cycle moves model time with it.
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "stubs/nvm_host.h"
#include "stubs/command.h"
#include "stubs/init.h"
#include "cosim_api.h"

#define NS_PER_CYCLE     10u
#define MS(n)            ((uint64_t)(n) * 1000000ull)
#define CSR_WORDS        0x400u
#define A_ID             0x000u
#define A_VERSION        0x004u
#define A_TOD_RD_LO      0x530u
#define A_TOD_RD_HI      0x534u
#define A_PP_CTRL        0x920u
#define A_PP_STAT        0x924u
#define A_PP_NVM_SEL     0x934u
#define A_PP_NVM_DATA    0x938u
#define A_PP_NVM_STAT    0x93cu
#define ID_MAGIC         0x4d494c4eu
#define SPI_BYTE_NS      640u
#define PAGE_PROGRAM_NS  MS(1)
/* One CSR access costs one backend cycle of model time: a bus round trip is
 * not free, and a capture that took no time at all could not be overlapped
 * by anything. A write that reaches the backend costs its edge on top. */
#define CSR_ACCESS_NS    COSIM_NS_PER_CYCLE
#define CMD_WREN         0x06u
#define CMD_RDSR         0x05u
#define CMD_SE           0xd8u
#define CMD_PP           0x02u

uint8_t nvm_host_flash[NVM_HOST_FLASH_BYTES];
uint8_t nvm_host_ddr[NVM_HOST_DDR_BYTES];

extern init_func const nvm_host_init_milan_init;
extern cmd_handler const nvm_host_cmd_milan_nvm;
extern cmd_handler const nvm_host_cmd_milan_status;

void set_idle_hook(void (*fptr)(void));
unsigned int crc32(const unsigned char *buffer, unsigned int len);

struct flash_model {
	int cs;
	uint8_t buf[300];
	unsigned int len;
	uint8_t resp;
	int rx_pending;
	int wel;
	uint64_t busy_until;
	int busy_forever;
	unsigned int erases;
	unsigned int programs;
	unsigned int rdsr;
	unsigned int pagewrap;
	int fail_erase;
	int fail_program;
	int fail_verify;
	uint64_t erase_ns;
};

static uint64_t now_ns;
static uint32_t csr_mem[CSR_WORDS];   /* registers the model only stores */
static uint32_t pp_ctrl;
static unsigned int nvm_sel;
static struct flash_model fl;
static void (*idle_hook)(void);
static unsigned int hb_count;
static uint64_t hb_last_ns;
static uint64_t hb_max_gap_ns;

void set_idle_hook(void (*fptr)(void))
{
	idle_hook = fptr;
}

unsigned int crc32(const unsigned char *buffer, unsigned int len)
{
	unsigned int crc = 0xffffffffu;
	unsigned int i;
	unsigned int bit;

	for (i = 0; i < len; ++i) {
		crc ^= buffer[i];
		for (bit = 0; bit < 8; ++bit)
			crc = (crc >> 1) ^ (0xedb88320u & (0u - (crc & 1u)));
	}
	return ~crc;
}

/* ---- the one clock ------------------------------------------------------ */
static void sync(void)
{
	cosim_rtl_sync(now_ns);
	if (cosim_rtl_now_ns() > now_ns)
		now_ns = cosim_rtl_now_ns();
}

uint64_t host_now_ns(void)
{
	return now_ns;
}

void host_catch_up(void)
{
	if (cosim_rtl_now_ns() > now_ns)
		now_ns = cosim_rtl_now_ns();
}

/* ---- the CSR face: every access reaches the RTL at its program point ---- */
uintptr_t nvm_host_csr_base(void)
{
	return (uintptr_t)csr_mem;
}

static uint32_t pp_stat(void)
{
	/* milan_csr.sv:2133-2140: {tag, 8'd0, verdict, 0, img_valid, stale,
	 * dirty, blank, backed, sp_err, alarm, restore_fail, restore_done,
	 * restore_busy, sp_busy} */
	struct cosim_levels l;

	cosim_rtl_levels(&l);
	/* PROPOSED: [11] nvm_pend, the owner-decided pending bit (0 on the
	 * tracked module, which has none) */
	return 0x5b000000u | ((uint32_t)l.verdict << 12) | ((uint32_t)l.pend << 11) |
	       ((uint32_t)l.img_valid << 10) | ((uint32_t)l.stale << 9) |
	       ((uint32_t)l.dirty << 8) | ((uint32_t)l.blank << 7) |
	       ((uint32_t)l.backed << 6) | ((uint32_t)l.alarm << 4) |
	       ((uint32_t)l.restore_fail << 3) | ((uint32_t)l.restore_done << 2) |
	       ((uint32_t)l.restore_busy << 1);
}

uint32_t nvm_host_csr_read(unsigned int offset)
{
	uint32_t v;

	now_ns += CSR_ACCESS_NS;
	sync();
	switch (offset) {
	case A_ID:
		v = ID_MAGIC;
		break;
	case A_VERSION:
		v = 0x00020059u;
		break;
	case A_TOD_RD_LO:
		v = (uint32_t)now_ns;
		break;
	case A_TOD_RD_HI:
		v = (uint32_t)(now_ns >> 32);
		break;
	case A_PP_CTRL:
		v = pp_ctrl;
		break;
	case A_PP_STAT:
		v = pp_stat();
		break;
	case A_PP_NVM_SEL:
		v = nvm_sel;
		break;
	case A_PP_NVM_DATA:
		v = cosim_rtl_csr_read(nvm_sel);
		break;
	case A_PP_NVM_STAT:
		v = cosim_rtl_csr_read(3u);
		cosim_hook("r_stat", v);
		break;
	default:
		v = (offset / 4u < CSR_WORDS) ? csr_mem[offset / 4u] : 0u;
		break;
	}
	return v;
}

static void strobe_hooks(uint32_t v)
{
	if (v & 0x1u) {
		if (hb_count && now_ns - hb_last_ns > hb_max_gap_ns)
			hb_max_gap_ns = now_ns - hb_last_ns;
		hb_last_ns = now_ns;
		hb_count++;
		cosim_hook("s_hb", v);
	}
	if (v & 0x2u)
		cosim_hook("s_ack", v);
	if (v & 0x4u)
		cosim_hook("s_start", v);
	if (v & 0x8u)
		cosim_hook("s_arm", v);
	if (v & 0x10u)
		cosim_hook("s_cert", v);
	if (v & 0x20u)
		cosim_hook("s_release", v);
	if (v & 0x40u)
		cosim_hook("s_reload", v);
}

void nvm_host_csr_write(unsigned int offset, uint32_t value)
{
	char name[24];

	now_ns += CSR_ACCESS_NS;
	sync();
	switch (offset) {
	case A_PP_NVM_SEL:
		nvm_sel = value & 0x3fu;
		if (nvm_sel >= 8u && nvm_sel < 16u) {
			snprintf(name, sizeof(name), "sel_own%u", nvm_sel - 8u);
			cosim_hook(name, value);
		}
		break;
	case A_PP_NVM_DATA:
		if (nvm_sel == 2u)
			cosim_hook("w_seq", value);
		if (nvm_sel == 3u)
			cosim_hook("w_stat", value);
		sync();
		cosim_rtl_csr_write(nvm_sel, value);
		break;
	case A_PP_NVM_STAT:
		strobe_hooks(value);
		sync();
		cosim_rtl_csr_write(4u, value);
		break;
	case A_PP_CTRL:
		pp_ctrl = value;
		cosim_rtl_restore_go((value >> 1) & 1u);
		break;
	default:
		if (offset / 4u < CSR_WORDS)
			csr_mem[offset / 4u] = value;
		break;
	}
	host_catch_up();
}

void nvm_host_tick(int cycles)
{
	now_ns += (uint64_t)(cycles > 0 ? cycles : 0) * NS_PER_CYCLE + 1000u;
	sync();
}

/* ---- the LiteSPI command master and the N25Q behind it (unchanged) ----- */
uint32_t nvm_host_spi_status(void)
{
	return 1u | ((uint32_t)fl.rx_pending << 1);
}

void nvm_host_spi_phyconfig(uint32_t v)
{
	(void)v;
}

static void flash_execute(void)
{
	uint32_t addr;
	unsigned int i;

	if (fl.len == 0)
		return;
	addr = ((uint32_t)fl.buf[1] << 16) | ((uint32_t)fl.buf[2] << 8) | fl.buf[3];
	switch (fl.buf[0]) {
	case CMD_WREN:
		fl.wel = 1;
		break;
	case CMD_SE:
		if (!fl.wel || fl.len < 4)
			break;
		addr &= ~0xffffu;
		cosim_hook("f_erase", addr);
		memset(nvm_host_flash + addr, 0xff, 0x10000u);
		if (fl.fail_erase)
			nvm_host_flash[addr + 5u] = 0x00;
		fl.busy_until = now_ns + fl.erase_ns;
		fl.erases++;
		fl.wel = 0;
		break;
	case CMD_PP:
		if (!fl.wel || fl.len < 4)
			break;
		cosim_hook("f_program", addr);
		if ((addr & 0xffu) + (fl.len - 4u) > 256u)
			fl.pagewrap++;
		for (i = 4; i < fl.len; ++i)
			nvm_host_flash[addr + i - 4u] &= fl.buf[i];
		if (fl.fail_verify && fl.programs == 0)
			nvm_host_flash[addr + 3u] ^= 0x01u;
		if (fl.fail_program)
			fl.busy_forever = 1;
		else
			fl.busy_until = now_ns + PAGE_PROGRAM_NS;
		fl.programs++;
		fl.wel = 0;
		break;
	default:
		break;
	}
}

void nvm_host_spi_cs(uint32_t v)
{
	if (fl.cs && !v)
		flash_execute();
	fl.cs = v != 0;
	fl.len = 0;
}

void nvm_host_spi_rxtx_write(uint32_t v)
{
	now_ns += SPI_BYTE_NS;
	if (fl.cs && fl.len < sizeof(fl.buf))
		fl.buf[fl.len++] = (uint8_t)v;
	if (fl.len && fl.buf[0] == CMD_RDSR) {
		if (fl.len == 1) {
			fl.rdsr++;
			cosim_hook("f_rdsr", fl.rdsr);
		}
		fl.resp = (fl.busy_forever || now_ns < fl.busy_until) ? 0x01u : 0x00u;
	} else {
		fl.resp = 0xffu;
	}
	fl.rx_pending = 1;
}

uint32_t nvm_host_spi_rxtx_read(void)
{
	fl.rx_pending = 0;
	return fl.resp;
}

/* ---- the scenario API the case runner drives ----------------------------- */
void host_boot(void)
{
	/* the AEM slot: the four magic bytes the firmware's verifier looks for */
	memcpy(nvm_host_flash + NVM_HOST_AEM_OFFSET, "AEMI", 4);
	nvm_host_init_milan_init();
	sync();
}

void host_idle_ms(uint64_t ms)
{
	uint64_t until = now_ns + MS(ms);

	while (now_ns < until) {
		uint64_t before = now_ns;

		if (idle_hook)
			idle_hook();
		if (now_ns == before)
			now_ns += 100000u;
		now_ns += 100000u;
		sync();
	}
}

/* The writer is NOT serviced: the idle hook does not run, the RTL does. */
void host_quiet_ms(uint64_t ms)
{
	uint64_t until = now_ns + MS(ms);

	while (now_ns < until) {
		now_ns += 100000u;
		sync();
	}
}

void host_uart(const char *text)
{
	char line[128];
	char *params[8];
	int nb = 0;
	char *cmd;
	char *tok;

	strncpy(line, text, sizeof(line) - 1);
	line[sizeof(line) - 1] = '\0';
	cmd = strtok(line, " ");
	while ((tok = strtok(NULL, " ")) != NULL && nb < 8)
		params[nb++] = tok;
	if (cmd && strcmp(cmd, "milan_nvm") == 0)
		nvm_host_cmd_milan_nvm(nb, params);
	else if (cmd && strcmp(cmd, "milan_status") == 0)
		nvm_host_cmd_milan_status(nb, params);
	sync();
}

void host_flash_fail(int erase, int program, int verify)
{
	fl.fail_erase = erase;
	fl.fail_program = program;
	fl.fail_verify = verify;
	if (!program)
		fl.busy_forever = 0;
}

void host_flash_erase_ms(uint64_t ms)
{
	fl.erase_ns = MS(ms);
}

void host_counters(struct host_counters *c)
{
	c->erases = fl.erases;
	c->programs = fl.programs;
	c->rdsr = fl.rdsr;
	c->pagewrap = fl.pagewrap;
	c->hb = hb_count;
	c->hb_max_gap_ns = hb_max_gap_ns;
	c->now_ns = now_ns;
}

int host_load_file(const char *path, uint8_t *dst, size_t room)
{
	FILE *f = fopen(path, "rb");
	size_t n;

	if (!f)
		return 0;
	memset(dst, 0xff, room);
	n = fread(dst, 1, room, f);
	fclose(f);
	return n > 0;
}

void host_dump_file(const char *path, const uint8_t *src, size_t n)
{
	FILE *f = fopen(path, "wb");

	if (!f) {
		fprintf(stderr, "HOST: cannot write %s\n", path);
		exit(2);
	}
	fwrite(src, 1, n, f);
	fclose(f);
}

void host_init(void)
{
	memset(nvm_host_flash, 0xff, sizeof(nvm_host_flash));
	memset(nvm_host_ddr, 0xa5, sizeof(nvm_host_ddr));
	fl.erase_ns = MS(20);
}

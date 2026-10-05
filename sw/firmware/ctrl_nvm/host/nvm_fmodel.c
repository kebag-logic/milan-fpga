/* SPDX-License-Identifier: (GPL-2.0 OR MIT) */
/*
 * nvm_fmodel.c - the host flash model with injectable faults (#665 lane F1).
 * See nvm_fmodel.h for what it models and what it polices.
 */
#include <string.h>

#include "nvm_fmodel.h"

/* One byte on the 1x link at 12.5 MHz: eight clocks. */
#define FM_SPI_BYTE_NS 640u
#define FM_PAGE        256u
/* The cells at the edge of a torn operation that are left half way. */
#define FM_EDGE_BYTES  16u

uint8_t nvm_fmodel_mem[NVM_FMODEL_BYTES];

struct fm_state {
	uint64_t now_ns;
	uint64_t busy_until_ns;
	uint64_t erase_ns;
	uint64_t program_ns;
	uint32_t lo;
	uint32_t hi;
	uint32_t prot;
	uint32_t noise;
	enum nvm_fault fault;
	unsigned int fault_count;
	unsigned int fault_skip;
	unsigned int varied;        /* reads read-vary-at has changed */
	uint32_t fault_at;
	uint32_t last_program;
	unsigned int cut_k;
	unsigned int cut_frac;
	int busy_forever;
	int dead;
	struct nvm_fmodel_count n;
};

static const struct fm_state fm_reset_value;
static struct fm_state fm;

void nvm_fmodel_power_on(void)
{
	fm = fm_reset_value;
	fm.erase_ns = 20000000u;
	fm.program_ns = 1000000u;
	fm.hi = NVM_FMODEL_BYTES;
	fm.fault_at = 5u;
	/* a fixed seed: every torn edge is the same on every run */
	fm.noise = 0x9e3779b9u;
}

void nvm_fmodel_blank(void)
{
	memset(nvm_fmodel_mem, 0xff, sizeof(nvm_fmodel_mem));
}

void nvm_fmodel_window(uint32_t lo, uint32_t hi)
{
	fm.lo = lo;
	fm.hi = hi;
}

void nvm_fmodel_protect(uint32_t lo)
{
	fm.prot = lo;
}

void nvm_fmodel_times(uint64_t erase_us, uint64_t program_us)
{
	fm.erase_ns = erase_us * 1000u;
	fm.program_ns = program_us * 1000u;
}

void nvm_fmodel_fault(enum nvm_fault fault, unsigned int count, unsigned int skip)
{
	fm.fault = fault;
	fm.fault_count = count;
	fm.fault_skip = skip;
}

void nvm_fmodel_cut(unsigned int k, unsigned int frac)
{
	fm.cut_k = k;
	fm.cut_frac = frac;
}

void nvm_fmodel_fault_at(uint32_t at)
{
	fm.fault_at = at;
}

int nvm_fmodel_dead(void)
{
	return fm.dead;
}

void nvm_fmodel_flip(uint32_t addr, unsigned int bit)
{
	nvm_fmodel_mem[addr % NVM_FMODEL_BYTES] ^= (uint8_t)(1u << (bit & 7u));
}

void nvm_fmodel_advance_us(uint64_t us)
{
	fm.now_ns += us * 1000u;
}

void nvm_fmodel_advance_ns(uint64_t ns)
{
	fm.now_ns += ns;
}

uint64_t nvm_fmodel_now_us(void)
{
	return fm.now_ns / 1000u;
}

uint64_t nvm_fmodel_now_ns(void)
{
	return fm.now_ns;
}

const struct nvm_fmodel_count *nvm_fmodel_count(void)
{
	return &fm.n;
}

static uint32_t fm_noise(void)
{
	fm.noise ^= fm.noise << 13;
	fm.noise ^= fm.noise >> 17;
	fm.noise ^= fm.noise << 5;
	return fm.noise;
}

/* Take one armed fault of this kind, if one is armed. */
static int fm_take(enum nvm_fault fault)
{
	if (fm.fault != fault || fm.fault_count == 0)
		return 0;
	if (fm.fault_skip) {
		fm.fault_skip--;
		return 0;
	}
	if (--fm.fault_count == 0)
		fm.fault = NVM_F_NONE;
	return 1;
}

static int fm_busy_now(void)
{
	return fm.busy_forever || fm.now_ns < fm.busy_until_ns;
}

/* The checks every media-changing call passes before it lands. */
static int fm_admit(uint32_t lo, uint32_t len)
{
	if (fm.dead)
		return 0;
	if (lo < fm.lo || lo + len > fm.hi || lo + len > NVM_FMODEL_BYTES) {
		fm.n.outside++;
		return 0;
	}
	if (fm.prot && lo < fm.prot + NVM_FMODEL_BLOCK && lo + len > fm.prot) {
		fm.n.protected_hit++;
		return 0;
	}
	if (fm_busy_now()) {
		fm.n.while_busy++;
		return 0;
	}
	return 1;
}

/* 1 when this media effect is the one the power fails in. */
static int fm_is_cut(void)
{
	fm.n.effects++;
	if (fm.cut_k == 0 || fm.n.effects != fm.cut_k)
		return 0;
	fm.dead = 1;
	return 1;
}

int nvm_fmodel_read(void *ctx, uint32_t addr, uint8_t *dst, uint32_t len)
{
	(void)ctx;
	if (fm.dead || addr >= NVM_FMODEL_BYTES || len > NVM_FMODEL_BYTES - addr)
		return -1;
	fm.n.reads++;
	fm.now_ns += (uint64_t)(4u + len) * FM_SPI_BYTE_NS;
	if (fm_take(NVM_F_READ_FAIL))
		return -1;
	if (addr <= fm.fault_at && fm.fault_at - addr < len && fm_take(NVM_F_READ_FAIL_AT))
		return -1;
	if ((addr ^ NVM_FMODEL_BLOCK) <= NVM_FMODEL_BYTES - len && fm_take(NVM_F_READ_ALIAS))
		addr ^= NVM_FMODEL_BLOCK;
	memcpy(dst, nvm_fmodel_mem + addr, len);
	if (len && fm_take(NVM_F_READ_FLIP))
		dst[len / 2u] ^= 0x10u;
	if (addr <= fm.fault_at && fm.fault_at - addr < len && fm_take(NVM_F_READ_FLIP_AT))
		dst[fm.fault_at - addr] ^= 0x08u;
	if (addr <= fm.fault_at && fm.fault_at - addr < len && fm_take(NVM_F_READ_VARY_AT))
		dst[fm.fault_at - addr] ^= (uint8_t)(0x08u << (fm.varied++ % 5u));
	return 0;
}

static void fm_program_bytes(uint32_t addr, const uint8_t *src, uint32_t len)
{
	uint32_t i;

	for (i = 0; i < len; ++i)
		nvm_fmodel_mem[addr + i] &= src[i];
}

int nvm_fmodel_program(void *ctx, uint32_t addr, const uint8_t *src, uint32_t len)
{
	(void)ctx;
	if (len == 0 || len > FM_PAGE || (addr % FM_PAGE) + len > FM_PAGE) {
		fm.n.pagewrap++;
		return -1;
	}
	if (!fm_admit(addr, len) || fm_take(NVM_F_PROGRAM_REFUSE))
		return -1;
	fm.now_ns += (uint64_t)(5u + len) * FM_SPI_BYTE_NS;
	if (fm.n.programs && addr < fm.last_program)
		fm.n.descending++;
	fm.last_program = addr;
	fm.n.programs++;
	if (fm_is_cut()) {
		uint32_t n = (len * fm.cut_frac) / 256u;

		fm_program_bytes(addr, src, n);
		if (n < len)
			nvm_fmodel_mem[addr + n] &= (uint8_t)(src[n] | fm_noise());
		return 0;
	}
	if (fm_take(NVM_F_PROGRAM_HANG)) {
		fm.busy_forever = 1;
		return 0;
	}
	if (!fm_take(NVM_F_PROGRAM_DROP))
		fm_program_bytes(addr, src, len);
	if (fm_take(NVM_F_PROGRAM_FLIP))
		nvm_fmodel_mem[addr + (len > 3u ? 3u : 0u)] ^= 0x01u;
	fm.busy_until_ns = fm.now_ns + fm.program_ns;
	return 0;
}

int nvm_fmodel_erase(void *ctx, uint32_t addr)
{
	uint32_t base = addr & ~(NVM_FMODEL_BLOCK - 1u);

	(void)ctx;
	if (!fm_admit(base, NVM_FMODEL_BLOCK) || fm_take(NVM_F_ERASE_REFUSE))
		return -1;
	fm.now_ns += 5u * FM_SPI_BYTE_NS;
	if (fm.n.erases < 16u)
		fm.n.erase_start_us[fm.n.erases] = fm.now_ns / 1000u;
	fm.n.erases++;
	fm.last_program = 0;
	if (fm_is_cut()) {
		uint32_t n = (NVM_FMODEL_BLOCK / 256u) * fm.cut_frac;
		uint32_t i;

		memset(nvm_fmodel_mem + base, 0xff, n);
		for (i = 0; i < FM_EDGE_BYTES && n + i < NVM_FMODEL_BLOCK; ++i)
			nvm_fmodel_mem[base + n + i] |= (uint8_t)fm_noise();
		return 0;
	}
	if (fm_take(NVM_F_ERASE_HANG)) {
		fm.busy_forever = 1;
		return 0;
	}
	memset(nvm_fmodel_mem + base, 0xff, NVM_FMODEL_BLOCK);
	if (fm_take(NVM_F_ERASE_STUCK))
		nvm_fmodel_mem[base + fm.fault_at % NVM_FMODEL_BLOCK] = 0x00u;
	fm.busy_until_ns = fm.now_ns + fm.erase_ns;
	return 0;
}

int nvm_fmodel_busy(void *ctx)
{
	(void)ctx;
	if (fm.dead)
		return -1;
	fm.n.busy_polls++;
	fm.now_ns += 4u * FM_SPI_BYTE_NS;
	return fm_busy_now();
}

uint64_t nvm_fmodel_now(void *ctx)
{
	(void)ctx;
	return fm.now_ns / 1000u;
}

const struct nvm_flash nvm_fmodel_port = {
	nvm_fmodel_read, nvm_fmodel_program, nvm_fmodel_erase, nvm_fmodel_busy,
	nvm_fmodel_now, 0,
};

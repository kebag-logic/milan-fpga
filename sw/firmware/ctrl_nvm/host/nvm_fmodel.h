/* SPDX-License-Identifier: (GPL-2.0 OR MIT) */
/*
 * nvm_fmodel.h - the host flash model behind the flash port (#665 lane F1).
 *
 * A 16 MiB NOR device with 64 KiB erase blocks and 256-byte pages: an erase
 * sets a block to 0xff, a program can only clear bits, and either holds the
 * device busy for its model time. Time is a counter: every port call costs
 * what it would cost on the 1x 12.5 MHz LiteSPI link, and the test loop adds
 * the event loop's own time between service calls.
 *
 * THE FAULTS:
 *   - a POWER CUT inside media effect k (one erase or one page program,
 *     counted from 1): that effect lands only as far as `frac`/256 of it,
 *     with the cells at the edge left half-way (a deterministic pattern), and
 *     from then on nothing reaches the media and every call fails;
 *   - an erase that never ends, that leaves a byte programmed (at offset
 *     `at` of the block, 5 unless set), or that is refused;
 *   - a program that never ends, that drops its bytes, that flips one, or
 *     that is refused;
 *   - a read that fails; that returns one bit flipped (the middle byte, or
 *     bit 3 of the byte at device address `at`, counting only the reads
 *     that cover it); or that answers from the neighbouring erase block
 *     (address bit 16 stuck: slot A reads slot B, and B reads A);
 *   - a bit flipped at rest (nvm_fmodel_flip).
 * Each fault is armed for `count` operations of its kind, after the next
 * `skip` of them pass untouched.
 *
 * It also polices the port contract: a program that crosses a page or is
 * issued while the device is busy, an erase or program outside the window
 * the test allows (the journal), or into the slot it protects (the
 * authoritative one), is counted, refused and reported.
 */
#ifndef NVM_FMODEL_H
#define NVM_FMODEL_H

#include <stdint.h>

#include "../nvm_flash.h"

#define NVM_FMODEL_BYTES 0x1000000u
#define NVM_FMODEL_BLOCK 0x10000u

enum nvm_fault {
	NVM_F_NONE = 0,
	NVM_F_ERASE_HANG,
	NVM_F_ERASE_STUCK,
	NVM_F_PROGRAM_HANG,
	NVM_F_PROGRAM_DROP,
	NVM_F_PROGRAM_FLIP,
	NVM_F_READ_FAIL,
	NVM_F_READ_FLIP,
	NVM_F_READ_FLIP_AT,
	NVM_F_READ_ALIAS,
	NVM_F_PROGRAM_REFUSE,
	NVM_F_ERASE_REFUSE
};

struct nvm_fmodel_count {
	unsigned int erases;
	unsigned int programs;
	unsigned int reads;
	unsigned int effects;       /* erases plus programs that reached the media */
	unsigned int busy_polls;
	unsigned int pagewrap;      /* a program that crossed a page: refused */
	unsigned int while_busy;    /* a program or erase issued while busy: refused */
	unsigned int outside;       /* outside the allowed window: refused */
	unsigned int protected_hit; /* into the protected slot: refused */
	unsigned int descending;    /* a page program below the one before it */
	uint64_t erase_start_us[16];/* the first sixteen erase starts */
};

extern uint8_t nvm_fmodel_mem[NVM_FMODEL_BYTES];

/* Power on: the media keeps its bytes, everything else starts afresh. */
void nvm_fmodel_power_on(void);
/* Erase the whole device (a blank board). */
void nvm_fmodel_blank(void);
/* The window erase and program may touch, [lo, hi). */
void nvm_fmodel_window(uint32_t lo, uint32_t hi);
/* A slot nothing may erase or program: [lo, lo + NVM_FMODEL_BLOCK); 0 none. */
void nvm_fmodel_protect(uint32_t lo);
void nvm_fmodel_times(uint64_t erase_us, uint64_t program_us);
void nvm_fmodel_fault(enum nvm_fault fault, unsigned int count, unsigned int skip);
/* Where erase-stuck and read-flip-at act (see above). */
void nvm_fmodel_fault_at(uint32_t at);
/* The power fails inside media effect k (from 1), frac/256 of it landed. */
void nvm_fmodel_cut(unsigned int k, unsigned int frac);
int nvm_fmodel_dead(void);
void nvm_fmodel_flip(uint32_t addr, unsigned int bit);
void nvm_fmodel_advance_us(uint64_t us);
void nvm_fmodel_advance_ns(uint64_t ns);
uint64_t nvm_fmodel_now_us(void);
uint64_t nvm_fmodel_now_ns(void);
const struct nvm_fmodel_count *nvm_fmodel_count(void);

/* The flash port over this model. */
extern const struct nvm_flash nvm_fmodel_port;

/* The raw operations, for the LiteSPI master model. */
int nvm_fmodel_read(void *ctx, uint32_t addr, uint8_t *dst, uint32_t len);
int nvm_fmodel_program(void *ctx, uint32_t addr, const uint8_t *src, uint32_t len);
int nvm_fmodel_erase(void *ctx, uint32_t addr);
int nvm_fmodel_busy(void *ctx);
uint64_t nvm_fmodel_now(void *ctx);

#endif /* NVM_FMODEL_H */

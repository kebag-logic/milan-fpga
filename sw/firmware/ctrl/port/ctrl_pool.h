// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// ctrl_pool.h - the static block pool behind shlan_malloc, shlan_calloc and
// shlan_free (#665 lane F0, the bare-metal directive of 2026-10-05).
//
// No heap. Every block the firmware ever allocates comes out of one arena
// the integrator declares statically and sizes at build time, carved into
// size classes: a class is a block size and a block count. An allocation
// takes the smallest class whose block fits and has one free, so both
// allocation and release cost a bounded number of steps (one per class) and
// never fragment. When every fitting class is exhausted the call returns
// NULL and the pool counts the refusal; it never falls back to anything.
//
// The sizes are the integrator's: lwSRP's attribute database (F4) is sized
// from the entity model's stream and VLAN counts, and the pool's high-water
// marks are what a build reads back to confirm the sizing.

#ifndef CTRL_POOL_H
#define CTRL_POOL_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

// The largest number of size classes one pool carries.
#define CTRL_POOL_MAX_CLASSES 8u

// The alignment of every block: the strictest a C11 object needs.
#define CTRL_POOL_ALIGN (_Alignof(max_align_t))

// One size class as the integrator declares it.
struct ctrl_pool_class {
	uint16_t block_bytes;   // usable bytes per block, rounded up to CTRL_POOL_ALIGN
	uint16_t blocks;        // blocks in the class
};

// One class as the pool tracks it.
struct ctrl_pool_bin {
	uint8_t *base;          // first block
	uint8_t *used;          // one flag per block: 1 while allocated
	void *free_head;        // first free block; each free block holds the next
	uint32_t stride;        // bytes from one block to the next
	uint16_t blocks;
	uint16_t free_count;
	uint16_t high_water;    // the most blocks ever allocated at once
};

struct ctrl_pool {
	struct ctrl_pool_bin bins[CTRL_POOL_MAX_CLASSES];
	unsigned n_bins;
	uint32_t refused;       // allocations no class could serve
	uint32_t bad_frees;     // frees of a pointer this pool did not hand out, or freed twice
};

// The arena bytes a set of classes needs, alignment and flags included.
size_t ctrl_pool_arena_bytes(const struct ctrl_pool_class *classes, unsigned n_classes);

// Carve `arena` into the classes, smallest block first. False when the arena
// is too small, misaligned, or the classes are not strictly increasing.
bool ctrl_pool_init(struct ctrl_pool *pool, void *arena, size_t arena_bytes,
		    const struct ctrl_pool_class *classes, unsigned n_classes);

void *ctrl_pool_alloc(struct ctrl_pool *pool, size_t bytes);
void *ctrl_pool_calloc(struct ctrl_pool *pool, size_t nmemb, size_t bytes);
void ctrl_pool_free(struct ctrl_pool *pool, void *ptr);

// Blocks currently allocated across every class.
unsigned ctrl_pool_in_use(const struct ctrl_pool *pool);

#ifdef __cplusplus
}
#endif

#endif // CTRL_POOL_H

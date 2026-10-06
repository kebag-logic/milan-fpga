// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// ctrl_pool.c - the static block pool (see ctrl_pool.h).
//
// Layout of the arena, one class after another: the class's used flags
// (one byte per block, padded to the alignment), then its blocks. A free
// block's first bytes hold the next free block, so the free list costs no
// memory of its own. The used flags make a double free and a free of a
// pointer into the middle of a block detectable, which a bare-metal target
// cannot afford to leave undetected: both corrupt a free list silently.

#include "ctrl_pool.h"

#include <string.h>

static size_t round_up(size_t value, size_t to)
{
	return (value + to - 1u) / to * to;
}

static size_t block_stride(const struct ctrl_pool_class *c)
{
	size_t bytes = c->block_bytes < sizeof(void *) ? sizeof(void *) : c->block_bytes;
	return round_up(bytes, CTRL_POOL_ALIGN);
}

static size_t class_bytes(const struct ctrl_pool_class *c)
{
	return round_up(c->blocks, CTRL_POOL_ALIGN) + block_stride(c) * c->blocks;
}

size_t ctrl_pool_arena_bytes(const struct ctrl_pool_class *classes, unsigned n_classes)
{
	size_t total = 0;
	for (unsigned i = 0; i < n_classes; ++i) {
		total += class_bytes(&classes[i]);
	}
	return total;
}

static bool classes_valid(const struct ctrl_pool_class *classes, unsigned n_classes)
{
	if (n_classes == 0u || n_classes > CTRL_POOL_MAX_CLASSES) {
		return false;
	}
	for (unsigned i = 0; i < n_classes; ++i) {
		if (classes[i].blocks == 0u || classes[i].block_bytes == 0u) {
			return false;
		}
		if (i > 0u && classes[i].block_bytes <= classes[i - 1u].block_bytes) {
			return false;
		}
	}
	return true;
}

static void bin_carve(struct ctrl_pool_bin *bin, const struct ctrl_pool_class *c, uint8_t *at)
{
	bin->used = at;
	bin->base = at + round_up(c->blocks, CTRL_POOL_ALIGN);
	bin->stride = (uint32_t)block_stride(c);
	bin->blocks = c->blocks;
	bin->free_count = c->blocks;
	bin->high_water = 0;
	bin->free_head = NULL;
	memset(bin->used, 0, c->blocks);
	for (unsigned k = c->blocks; k > 0u; --k) {
		void *block = bin->base + (size_t)(k - 1u) * bin->stride;
		memcpy(block, &bin->free_head, sizeof bin->free_head);
		bin->free_head = block;
	}
}

bool ctrl_pool_init(struct ctrl_pool *pool, void *arena, size_t arena_bytes,
		    const struct ctrl_pool_class *classes, unsigned n_classes)
{
	memset(pool, 0, sizeof *pool);
	if (arena == NULL || !classes_valid(classes, n_classes) ||
	    (uintptr_t)arena % CTRL_POOL_ALIGN != 0u ||
	    arena_bytes < ctrl_pool_arena_bytes(classes, n_classes)) {
		return false;
	}
	uint8_t *at = arena;
	for (unsigned i = 0; i < n_classes; ++i) {
		bin_carve(&pool->bins[i], &classes[i], at);
		at += class_bytes(&classes[i]);
	}
	pool->n_bins = n_classes;
	return true;
}

static void *bin_take(struct ctrl_pool_bin *bin)
{
	void *block = bin->free_head;
	memcpy(&bin->free_head, block, sizeof bin->free_head);
	bin->free_count--;
	bin->used[((uint8_t *)block - bin->base) / bin->stride] = 1u;
	unsigned taken = (unsigned)bin->blocks - bin->free_count;
	if (taken > bin->high_water) {
		bin->high_water = (uint16_t)taken;
	}
	return block;
}

void *ctrl_pool_alloc(struct ctrl_pool *pool, size_t bytes)
{
	if (bytes == 0u) {
		pool->refused++;
		return NULL;
	}
	for (unsigned i = 0; i < pool->n_bins; ++i) {
		struct ctrl_pool_bin *bin = &pool->bins[i];
		// a free list that disagrees with its count is exhausted, not followed
		if (bin->stride >= bytes && bin->free_count > 0u && bin->free_head != NULL) {
			return bin_take(bin);
		}
	}
	pool->refused++;
	return NULL;
}

void *ctrl_pool_calloc(struct ctrl_pool *pool, size_t nmemb, size_t bytes)
{
	if (nmemb != 0u && bytes > SIZE_MAX / nmemb) {
		pool->refused++;
		return NULL;
	}
	void *block = ctrl_pool_alloc(pool, nmemb * bytes);
	if (block != NULL) {
		memset(block, 0, nmemb * bytes);
	}
	return block;
}

void ctrl_pool_free(struct ctrl_pool *pool, void *ptr)
{
	if (ptr == NULL) {
		return;
	}
	// compared as integers: a pointer the pool did not hand out need not
	// point into any array the pool owns, so a relational compare on the
	// pointers themselves would be undefined
	uintptr_t p = (uintptr_t)ptr;
	for (unsigned i = 0; i < pool->n_bins; ++i) {
		struct ctrl_pool_bin *bin = &pool->bins[i];
		uintptr_t base = (uintptr_t)bin->base;
		if (p < base || p - base >= (uintptr_t)bin->blocks * bin->stride) {
			continue;
		}
		size_t offset = (size_t)(p - base);
		size_t index = offset / bin->stride;
		if (offset % bin->stride != 0u || bin->used[index] == 0u) {
			pool->bad_frees++;
			return;
		}
		bin->used[index] = 0u;
		memcpy(ptr, &bin->free_head, sizeof bin->free_head);
		bin->free_head = ptr;
		bin->free_count++;
		return;
	}
	pool->bad_frees++;
}

unsigned ctrl_pool_in_use(const struct ctrl_pool *pool)
{
	unsigned n = 0;
	for (unsigned i = 0; i < pool->n_bins; ++i) {
		n += (unsigned)pool->bins[i].blocks - pool->bins[i].free_count;
	}
	return n;
}

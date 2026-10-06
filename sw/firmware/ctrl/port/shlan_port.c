// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// shlan_port.c - lwSRP's alloc and print port on the static pool and the
// debug sink (see shlan_port.h).

#include "shlan_port.h"

#include <stdarg.h>

#include "ctrl_debug.h"

static struct ctrl_pool *port_pool;

void shlan_port_bind_pool(struct ctrl_pool *pool)
{
	port_pool = pool;
}

struct ctrl_pool *shlan_port_pool(void)
{
	return port_pool;
}

void *shlan_malloc(size_t size)
{
	if (port_pool == NULL) {
		return NULL;
	}
	return ctrl_pool_alloc(port_pool, size);
}

void *shlan_calloc(size_t nmemb, size_t size)
{
	if (port_pool == NULL) {
		return NULL;
	}
	return ctrl_pool_calloc(port_pool, nmemb, size);
}

void shlan_free(void *ptr)
{
	if (port_pool != NULL) {
		ctrl_pool_free(port_pool, ptr);
	}
}

int shlan_printf(const char *fmt, ...)
{
	va_list ap;
	va_start(ap, fmt);
	int n = ctrl_debug_vprintf(fmt, ap);
	va_end(ap);
	return n;
}

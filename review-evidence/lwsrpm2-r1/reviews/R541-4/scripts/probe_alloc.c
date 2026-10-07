/* SPDX-License-Identifier: Apache-2.0 */
#include <stdlib.h>
#include "ports/alloc.h"
int probe_fail_at;
static int fail(void) { return probe_fail_at > 0 && --probe_fail_at == 0; }
void *shlan_malloc(size_t n) { return fail() ? NULL : malloc(n); }
void *shlan_calloc(size_t n, size_t z) { return fail() ? NULL : calloc(n, z); }
void shlan_free(void *p) { free(p); }

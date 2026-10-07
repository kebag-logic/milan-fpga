/* SPDX-License-Identifier: Apache-2.0 */
/* Fault-injecting replacement for the hosted allocation port. */
#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>

int probe_fail_at;

static int fail_now(void)
{
    if (probe_fail_at > 0 && --probe_fail_at == 0) {
        return 1;
    }
    return 0;
}
void *shlan_malloc(size_t size) { return fail_now() ? NULL : malloc(size); }
void *shlan_calloc(size_t n, size_t size) { return fail_now() ? NULL : calloc(n, size); }
void shlan_free(void *p) { free(p); }
int shlan_printf(const char *fmt, ...)
{
    va_list ap;
    va_start(ap, fmt);
    int r = vprintf(fmt, ap);
    va_end(ap);
    return r;
}

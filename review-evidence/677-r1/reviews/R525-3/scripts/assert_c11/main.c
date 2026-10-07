#include <setjmp.h>
#include <stdio.h>
#include <string.h>
extern int evaluated;
int probe_enabled_true(void); int probe_enabled_false(int); int probe_pointer(const char *);
int probe_void_expr(int); int probe_disabled(int); int probe_disabled_fail(void); int probe_reenabled(void);
static jmp_buf env; static const char *g_expr, *g_file, *g_func; static unsigned g_line; static int calls;
_Noreturn void __assert_fail(const char *e, const char *f, unsigned int l, const char *fn)
{ g_expr = e; g_file = f; g_line = l; g_func = fn; calls++; longjmp(env, 1); }
static int fails;
#define CHECK(c) do { if (!(c)) { printf("FAIL: %s\n", #c); fails++; } else printf("PASS: %s\n", #c); } while (0)
int main(void) {
    CHECK(probe_enabled_true() == 1 && calls == 0);
    if (!setjmp(env)) { probe_enabled_false(1); CHECK(!"handler not reached"); }
    else { CHECK(calls == 1 && !strcmp(g_expr, "x == 42") && strstr(g_file, "probe.c") && g_line == 7 && !strcmp(g_func, "probe_enabled_false")); }
    CHECK(probe_enabled_false(42) == 0 && calls == 1);
    CHECK(probe_pointer("p") == 1 && calls == 1);
    CHECK(probe_void_expr(1) == 7 && calls == 1);
    int before = evaluated;
    CHECK(probe_disabled(0) == before && calls == 1);
    CHECK(probe_disabled_fail() == 1 && calls == 1);
    if (!setjmp(env)) { probe_reenabled(); CHECK(!"re-enabled assert not reached"); }
    else { CHECK(calls == 2 && g_line == 16 && !strcmp(g_func, "probe_reenabled")); }
    printf("last handler call: expr=\"%s\" line=%u func=%s\n", g_expr, g_line, g_func);
    printf("assert C11 probe: failures %d\n", fails);
    return fails != 0;
}

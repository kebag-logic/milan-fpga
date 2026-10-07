/* Compiled ONLY against rv32_include (-nostdinc): C11 7.2 semantics of its <assert.h>. */
#include <assert.h>
static_assert(sizeof(int) >= 2, "C11 7.2p3: static_assert expands to _Static_assert");
int evaluated;
static int touch(void) { evaluated++; return 1; }
int probe_enabled_true(void) { assert(touch()); return evaluated; }          /* evaluates once */
int probe_enabled_false(int x) { assert(x == 42); return 0; }                /* fails when x != 42 */
int probe_pointer(const char *p) { assert(p); return 1; }                   /* scalar pointer */
int probe_void_expr(int x) { return (assert(x), 7); }                       /* void expression */
#define NDEBUG
#include <assert.h>
int probe_disabled(int x) { (void)x; assert(touch() && x == 42); return evaluated; } /* not evaluated */
int probe_disabled_fail(void) { assert(0); return 1; }
#undef NDEBUG
#include <assert.h>
int probe_reenabled(void) { assert(0 && "reenabled"); return 1; }

#include <assert.h>
static_assert(1, "s");
int f(int x) { assert(x > 0); return x; }

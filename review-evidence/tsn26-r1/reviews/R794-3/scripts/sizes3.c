/* SPDX-License-Identifier: MIT */
/* Compile-time size report: the build fails unless the sizes are those named by -D flags. */
#include "acmp.h"
#include <stddef.h>
_Static_assert(sizeof(struct acmp) == WANT_ACMP, "struct acmp size");
_Static_assert(sizeof(struct acmp_sink) == WANT_SINK, "struct acmp_sink size");
_Static_assert(sizeof(((struct acmp *)0)->owed) == WANT_OWED, "owed set size");

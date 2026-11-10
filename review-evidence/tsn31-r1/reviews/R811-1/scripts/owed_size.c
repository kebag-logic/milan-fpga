/* SPDX-License-Identifier: MIT */
/* Review probe: sizeof one owed frame and the owed set at the compiled ACMP_MAX_SINKS (compile-time only). */
#include "acmp.h"
char frame_bytes[sizeof ((struct acmp *)0)->owed[0]];
char set_bytes[sizeof ((struct acmp *)0)->owed];

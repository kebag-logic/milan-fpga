// SPDX-License-Identifier: MIT
// Emits struct sizes as symbol sizes so they can be read without running the target.
#include "acmp.h"
#include <stddef.h>
char size_struct_acmp[sizeof(struct acmp)];
char size_owed_array[sizeof(((struct acmp *)0)->owed)];
char size_one_owed[sizeof(struct acmp_owed)];
char offset_owed[offsetof(struct acmp, owed) + 1];
char offset_owed_head[offsetof(struct acmp, owed_head) + 1];
char size_owed_head[sizeof(((struct acmp *)0)->owed_head)];
char size_owed_count[sizeof(((struct acmp *)0)->owed_count)];

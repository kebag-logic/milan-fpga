// SPDX-License-Identifier: MIT
#include "acmp.h"
#include <stddef.h>
// Each size is encoded as an array length so it can be read from the object's symbol table.
char size_acmp[sizeof(struct acmp)];
char size_owed[sizeof(((struct acmp *)0)->owed)];
char size_owed_entry[sizeof(((struct acmp *)0)->owed[0])];

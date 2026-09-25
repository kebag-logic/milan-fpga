| id | case | none | nested | asm | extblank | register | storage |
|---|---|---|---|---|---|---|---|
| ST-static | storage unit | REFUSED absence rule (storage) | REFUSED absence rule (storage) | REFUSED absence rule (storage) | REFUSED absence rule (storage) | REFUSED absence rule (storage) | ACCEPTED |
| ST-extern | storage unit | REFUSED absence rule (storage) | REFUSED absence rule (storage) | REFUSED absence rule (storage) | REFUSED absence rule (storage) | REFUSED absence rule (storage) | ACCEPTED |
| ST-_Thread_local static | storage unit | REFUSED absence rule (storage) | REFUSED absence rule (storage) | REFUSED absence rule (storage) | REFUSED absence rule (storage) | REFUSED absence rule (storage) | ACCEPTED |
| S01 | nested function defined after the guard writes the sample, called before it | REFUSED absence rule (nested) | ACCEPTED | REFUSED absence rule (nested) | REFUSED absence rule (nested) | REFUSED absence rule (nested) | REFUSED absence rule (nested) |
| S02 | __extension__ old-style nested function capture | REFUSED absence rule (nested) | ACCEPTED | REFUSED absence rule (nested) | ACCEPTED | REFUSED absence rule (nested) | REFUSED absence rule (nested) |
| S03 | asm without a sample operand in the interval | REFUSED absence rule (asm) | REFUSED absence rule (asm) | ACCEPTED | REFUSED absence rule (asm) | REFUSED absence rule (asm) | REFUSED absence rule (asm) |
| S04 | plain &(id) after the guard | REFUSED absence rule (escape) | REFUSED absence rule (escape) | REFUSED absence rule (escape) | REFUSED absence rule (escape) | ACCEPTED | REFUSED absence rule (escape) |
| S05 | __extension__ &(id) after the guard | REFUSED absence rule (escape) | REFUSED absence rule (escape) | REFUSED absence rule (escape) | REFUSED absence rule (escape) | ACCEPTED | REFUSED absence rule (escape) |
| S06 | asm writing s0 directly in the interval (no operands) | REFUSED absence rule (asm) | REFUSED absence rule (asm) | ACCEPTED | REFUSED absence rule (asm) | REFUSED absence rule (asm) | REFUSED absence rule (asm) |

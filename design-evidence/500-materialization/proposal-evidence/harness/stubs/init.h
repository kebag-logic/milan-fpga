/* SPDX-License-Identifier: (GPL-2.0 OR MIT) */
/* Stub for the BIOS init registry: the init function becomes a named pointer. */
#ifndef INIT_H
#define INIT_H
typedef void (*init_func)(void);
#define define_init_func(f) init_func const nvm_host_init_##f = f
#endif

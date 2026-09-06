/* SPDX-License-Identifier: (GPL-2.0 OR MIT) */
/* Stub for the LiteX-generated memory map: every base is a host array. */
#ifndef GENERATED_MEM_H
#define GENERATED_MEM_H
#include "../nvm_host.h"
#define MILAN_CSR_BASE (nvm_host_csr_base())
#define SPIFLASH_BASE  ((uintptr_t)nvm_host_flash)
#define SPIFLASH_SIZE  NVM_HOST_FLASH_BYTES
#endif

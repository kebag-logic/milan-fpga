/* SPDX-License-Identifier: (GPL-2.0 OR MIT) */
/* Stub for the LiteX-generated memory map: the QSPI window is the flash
 * model's array and the CSR window the LiteSPI model's (#665 lane F1). */
#ifndef GENERATED_MEM_H
#define GENERATED_MEM_H
#include "../../litespi_model.h"
#include "../../nvm_fmodel.h"
#define MILAN_CSR_BASE (litespi_model_csr_base())
#define SPIFLASH_BASE  ((uintptr_t)nvm_fmodel_mem)
#define SPIFLASH_SIZE  NVM_FMODEL_BYTES
#endif

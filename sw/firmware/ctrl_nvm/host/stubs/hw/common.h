/* SPDX-License-Identifier: (GPL-2.0 OR MIT) */
/* Stub for LiteX hw/common.h: the busy-wait advances model time (#665 lane F1). */
#ifndef HW_COMMON_H
#define HW_COMMON_H
#include "../../litespi_model.h"
static inline void cdelay(int i) { litespi_model_cdelay(i); }
#endif

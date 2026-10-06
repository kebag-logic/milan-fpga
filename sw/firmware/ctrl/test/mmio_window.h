// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// mmio_window.h - the window plat/mbx_plat_mmio.c is built over on the host
// (#665 lane FT). The unit arm force-includes it into that file and points
// the platform's own two configuration macros at it: CTRL_MBX_BASE at
// ctrl_test_window, CTRL_MBX_WFI at ctrl_test_wfi (test_mmio.cpp).

#ifndef MMIO_WINDOW_H
#define MMIO_WINDOW_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

#define CTRL_TEST_WINDOW_WORDS 1024u

extern uint32_t ctrl_test_window[CTRL_TEST_WINDOW_WORDS];
void ctrl_test_wfi(void);

#ifdef __cplusplus
}
#endif

#endif // MMIO_WINDOW_H

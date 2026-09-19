/* SPDX-License-Identifier: (GPL-2.0 OR MIT) */
/* Issue #419 round 3 co-simulation: the seam between the host model (C) and
 * the Verilated RTL with its bus-functional models (C++). */
#ifndef COSIM_API_H
#define COSIM_API_H

#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

/* One backend cycle of model time: the RTL is clocked at 1 MHz of model
 * time, so the backend's and the manager's millisecond ticks are real model
 * milliseconds. PHYSICAL TIMING IS NOT MODELLED (PROPOSAL.md section 9). */
#define COSIM_NS_PER_CYCLE 1000u

struct cosim_levels {
	unsigned backed, dirty, stale, verdict, img_valid, pend, unres;
	unsigned restore_busy, restore_done, restore_fail, blank, alarm;
};

struct host_counters {
	unsigned erases, programs, rdsr, pagewrap, hb;
	uint64_t hb_max_gap_ns, now_ns;
};

/* RTL side (cosim_bridge.cpp) */
void cosim_rtl_sync(uint64_t now_ns);
uint64_t cosim_rtl_now_ns(void);
uint32_t cosim_rtl_csr_read(unsigned word);
void cosim_rtl_csr_write(unsigned word, uint32_t value);
void cosim_rtl_restore_go(unsigned level);
void cosim_rtl_levels(struct cosim_levels *l);
void cosim_hook(const char *name, uint32_t value);

/* host side (cosim_host.c) */
void host_init(void);
void host_boot(void);
void host_idle_ms(uint64_t ms);
void host_quiet_ms(uint64_t ms);
void host_uart(const char *text);
void host_flash_fail(int erase, int program, int verify);
void host_flash_erase_ms(uint64_t ms);
void host_counters(struct host_counters *c);
uint64_t host_now_ns(void);
void host_catch_up(void);
int host_load_file(const char *path, uint8_t *dst, size_t room);
void host_dump_file(const char *path, const uint8_t *src, size_t n);

#ifdef __cplusplus
}
#endif

#endif

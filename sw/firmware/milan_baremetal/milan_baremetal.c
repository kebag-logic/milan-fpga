/* SPDX-License-Identifier: (GPL-2.0 OR MIT) */

#include <stdint.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>

#include <generated/mem.h>
#include <generated/soc.h>

#include <hw/common.h>
#include <libbase/crc.h>
#include <system.h>

#include "command.h"
#include "init.h"

#define MILAN_ID             0x000u
#define MILAN_VERSION        0x004u
#define MILAN_MAC_CTRL       0x100u
#define MILAN_MAC_ADDR_LO    0x108u
#define MILAN_MAC_ADDR_HI    0x10cu
#define MILAN_PTP_CTRL       0x500u
#define MILAN_PTP_TOD_WR_LO  0x510u
#define MILAN_PTP_TOD_WR_HI  0x514u
#define MILAN_PTP_CMD        0x520u
#define MILAN_PTP_TOD_RD_LO  0x530u
#define MILAN_PTP_TOD_RD_HI  0x534u
#define MILAN_ADP_CTRL       0x600u
#define MILAN_ADP_EID_LO     0x604u
#define MILAN_ADP_EID_HI     0x608u
#define MILAN_ADP_MID_LO     0x60cu
#define MILAN_ADP_MID_HI     0x610u
#define MILAN_ADP_CAPS       0x614u
#define MILAN_ADP_GM_LO      0x624u
#define MILAN_ADP_GM_HI      0x628u
#define MILAN_AAF_CTRL       0x654u
#define MILAN_LWSRP_CTRL     0x680u
#define MILAN_LWSRP_VID      0x684u
#define MILAN_MAAP_CTRL      0x6ccu
#define MILAN_GPTP_PDELAY    0x6e4u
#define MILAN_AS_PARENT_LO   0x730u
#define MILAN_AS_PARENT_HI   0x734u
#define MILAN_CRF_TX_CTRL    0x750u
#define MILAN_CLKV_STAT      0x77cu
#define MILAN_AS_PATH_CMD    0x7e4u
#define MILAN_PP_CTRL        0x920u
#define MILAN_PP_STAT        0x924u

#define MILAN_ID_MAGIC       0x4d494c4eu
#define MILAN_PTP_LOAD       0x1u
#define MILAN_PTP_SNAPSHOT   0x4u
#define MILAN_ADP_CAPS_VALUE 0x00008588u

static int aem_loaded;

static inline volatile uint32_t *milan_reg(unsigned int offset)
{
	return (volatile uint32_t *)(MILAN_CSR_BASE + offset);
}

static inline uint32_t milan_read(unsigned int offset)
{
	return *milan_reg(offset);
}

static inline void milan_write(unsigned int offset, uint32_t value)
{
	*milan_reg(offset) = value;
	__asm__ volatile("fence iorw, iorw" ::: "memory");
}

static void print_tod(uint64_t ns)
{
	printf("TAI_NS=0x%08lx%08lx\n",
	       (unsigned long)(ns >> 32), (unsigned long)ns);
}

static uint64_t gettime_ns(void)
{
	uint32_t hi1, hi2, lo;

	milan_write(MILAN_PTP_CMD, MILAN_PTP_SNAPSHOT);
	cdelay(128);
	do {
		hi1 = milan_read(MILAN_PTP_TOD_RD_HI);
		lo = milan_read(MILAN_PTP_TOD_RD_LO);
		hi2 = milan_read(MILAN_PTP_TOD_RD_HI);
	} while (hi1 != hi2);
	return ((uint64_t)hi2 << 32) | lo;
}

static void settime_ns(uint64_t ns)
{
	milan_write(MILAN_PTP_TOD_WR_LO, (uint32_t)ns);
	milan_write(MILAN_PTP_TOD_WR_HI, (uint32_t)(ns >> 32));
	milan_write(MILAN_PTP_CMD, MILAN_PTP_LOAD);
}

static int parse_u64(const char *text, uint64_t *value)
{
	char *end;
	unsigned long long parsed;

	errno = 0;
	parsed = strtoull(text, &end, 0);
	if (errno == ERANGE || *text == '\0' || *end != '\0')
		return 0;
	*value = (uint64_t)parsed;
	return 1;
}

static int seconds_to_ns(uint64_t seconds, uint64_t nanoseconds,
			 uint64_t *value)
{
	if (nanoseconds >= 1000000000ull ||
	    seconds > (UINT64_MAX - nanoseconds) / 1000000000ull)
		return 0;
	*value = seconds * 1000000000ull + nanoseconds;
	return 1;
}

static void configure_fabric(void)
{
	/* Identity and MAC come from the same generated model as aem_desc.bin. */
	milan_write(MILAN_ADP_CTRL, milan_read(MILAN_ADP_CTRL) & ~1u);
	milan_write(MILAN_PP_CTRL, milan_read(MILAN_PP_CTRL) & ~1u);
	milan_write(MILAN_ADP_EID_LO, MILAN_ENTITY_ID_LO);
	milan_write(MILAN_ADP_EID_HI, MILAN_ENTITY_ID_HI);
	milan_write(MILAN_ADP_MID_LO, MILAN_MODEL_ID_LO);
	milan_write(MILAN_ADP_MID_HI, MILAN_MODEL_ID_HI);
	milan_write(MILAN_ADP_CAPS, MILAN_ADP_CAPS_VALUE);
	milan_write(MILAN_MAC_ADDR_LO, MILAN_STATION_MAC_LO);
	milan_write(MILAN_MAC_ADDR_HI, MILAN_STATION_MAC_HI);
	/* Receive the link-local multicast control groups without promiscuous mode. */
	milan_write(MILAN_MAC_CTRL, milan_read(MILAN_MAC_CTRL) | (1u << 3));

	/* Fabric owns media/control. Firmware only provides the generated policy. */
	milan_write(MILAN_AAF_CTRL, (MILAN_SR_VID << 16) | 1u);
	milan_write(MILAN_LWSRP_VID, MILAN_SR_VID);
	milan_write(MILAN_LWSRP_CTRL, MILAN_LWSRP_CTRL_RESET | 3u);
	milan_write(MILAN_MAAP_CTRL, ((MILAN_N_TALKERS + 1u) << 8) | 1u);
	milan_write(MILAN_CRF_TX_CTRL, 3u);
}

/*
 * The ONLY place either compatibility enable bit is set.  The boot
 * contract is a data-flow property -- no value reaches PP_CTRL[0] or
 * ADP_CTRL[0] unless the AEM verifier's verdict says the image it checked
 * matched -- and a single choke point is what lets that be measured by
 * data flow instead of by refusing constructs across the whole file.
 */
static void entity_advertise(int verified)
{
	if (!verified)
		return;
	milan_write(MILAN_PP_CTRL, milan_read(MILAN_PP_CTRL) | 1u);
	milan_write(MILAN_ADP_CTRL, milan_read(MILAN_ADP_CTRL) | 1u);
	printf("Milan baremetal: fabric entity enabled; UART diagnostics ready.\n");
}

static int load_aem_image(void)
{
#if defined(SPIFLASH_BASE) && defined(MILAN_AEM_FLASH_OFFSET)
	const volatile uint8_t *src =
		(const volatile uint8_t *)(SPIFLASH_BASE + MILAN_AEM_FLASH_OFFSET);
	volatile uint8_t *dst = (volatile uint8_t *)MILAN_AEM_DESC_BASE;
	unsigned int i;
	uint32_t got;

	if (src[0] != 'A' || src[1] != 'E' || src[2] != 'M' || src[3] != 'I') {
		printf("Milan baremetal: AEM image missing at QSPI +0x%08x; entity disabled.\n",
		       MILAN_AEM_FLASH_OFFSET);
		return 0;
	}
	for (i = 0; i < MILAN_AEM_IMAGE_BYTES; ++i)
		dst[i] = src[i];
	__asm__ volatile("fence rw, rw" ::: "memory");
	got = crc32((const unsigned char *)MILAN_AEM_DESC_BASE,
	            MILAN_AEM_IMAGE_BYTES);
	if (got != MILAN_AEM_IMAGE_CRC32) {
		printf("Milan baremetal: AEM CRC failed (expected %08lx, got %08lx); entity disabled.\n",
		       (unsigned long)MILAN_AEM_IMAGE_CRC32, (unsigned long)got);
		return 0;
	}
	printf("Milan baremetal: AEM %u B copied QSPI +0x%08x -> 0x%08x, CRC %08lx.\n",
	       MILAN_AEM_IMAGE_BYTES, MILAN_AEM_FLASH_OFFSET,
	       MILAN_AEM_DESC_BASE, (unsigned long)got);
	return 1;
#else
	printf("Milan baremetal: no QSPI AEM slot; entity disabled.\n");
	return 0;
#endif
}

static void milan_init(void)
{
	uint32_t id = milan_read(MILAN_ID);

	printf("Milan baremetal: CSR ID=%08lx VERSION=%08lx, RV32I machine mode, no MMU/cache.\n",
	       (unsigned long)id, (unsigned long)milan_read(MILAN_VERSION));
	if (id != MILAN_ID_MAGIC) {
		printf("Milan baremetal: CSR identity mismatch; fabric remains disabled.\n");
		return;
	}
	/* PHC and fabric gPTP are live from reset, independent of the AEM gate. */
	configure_fabric();
	aem_loaded = load_aem_image();
	entity_advertise(aem_loaded);
}

define_init_func(milan_init);

static void milan_status_handler(int nb_params, char **params)
{
	uint32_t gm_lo, gm_hi, parent_lo, parent_hi;
	uint32_t pdelay_ns, as_path, clkv_stat;

	(void)nb_params;
	(void)params;
	/* The first half read snapshots each complete live 64-bit identity. */
	gm_lo = milan_read(MILAN_ADP_GM_LO);
	gm_hi = milan_read(MILAN_ADP_GM_HI);
	parent_lo = milan_read(MILAN_AS_PARENT_LO);
	parent_hi = milan_read(MILAN_AS_PARENT_HI);
	pdelay_ns = milan_read(MILAN_GPTP_PDELAY);
	as_path = milan_read(MILAN_AS_PATH_CMD);
	clkv_stat = milan_read(MILAN_CLKV_STAT);
	printf("ID=%08lx VERSION=%08lx PTP_CTRL=%08lx ADP_CTRL=%08lx PP_CTRL=%08lx PP_STAT=%08lx AEM=%s\n",
	       (unsigned long)milan_read(MILAN_ID),
	       (unsigned long)milan_read(MILAN_VERSION),
	       (unsigned long)milan_read(MILAN_PTP_CTRL),
	       (unsigned long)milan_read(MILAN_ADP_CTRL),
	       (unsigned long)milan_read(MILAN_PP_CTRL),
	       (unsigned long)milan_read(MILAN_PP_STAT),
	       aem_loaded ? "loaded" : "disabled");
	printf("GPTP_GM=%08lx%08lx GPTP_PARENT=%08lx%08lx PDELAY_NS=%lu AS_PATH_COUNT=%lu AS_PATH_GEN=%lu CLKV_STAT=%08lx SYNC=%lu ASCAPABLE=%lu TU=%lu\n",
	       (unsigned long)gm_hi, (unsigned long)gm_lo,
	       (unsigned long)parent_hi, (unsigned long)parent_lo,
	       (unsigned long)pdelay_ns,
	       (unsigned long)(as_path & 0xfu),
	       (unsigned long)((as_path >> 4) & 0xfu),
	       (unsigned long)clkv_stat,
	       (unsigned long)((clkv_stat >> 1) & 1u),
	       (unsigned long)((clkv_stat >> 16) & 1u),
	       (unsigned long)(clkv_stat & 1u));
	print_tod(gettime_ns());
}

define_command(milan_status, milan_status_handler,
	       "Show fabric, gPTP publication, entity-image and PHC status", SYSTEM_CMDS);

static void milan_gettime_handler(int nb_params, char **params)
{
	(void)nb_params;
	(void)params;
	print_tod(gettime_ns());
}

define_command(milan_gettime, milan_gettime_handler,
	       "Snapshot the fabric PHC (TAI nanoseconds)", SYSTEM_CMDS);

static void milan_settime_handler(int nb_params, char **params)
{
	uint64_t seconds, nanoseconds = 0, value;

	if (nb_params < 1 || nb_params > 2 ||
	    !parse_u64(params[0], &seconds) ||
	    (nb_params == 2 && !parse_u64(params[1], &nanoseconds)) ||
	    !seconds_to_ns(seconds, nanoseconds, &value)) {
		printf("milan_settime <tai-seconds> [nanoseconds]\n");
		return;
	}
	settime_ns(value);
	print_tod(gettime_ns());
}

define_command(milan_settime, milan_settime_handler,
	       "Set fabric PHC from TAI seconds and nanoseconds", SYSTEM_CMDS);

static void milan_utc_handler(int nb_params, char **params)
{
	uint64_t utc, nanoseconds, tai_minus_utc, tai, value;

	if (nb_params != 3 || !parse_u64(params[0], &utc) ||
	    !parse_u64(params[1], &nanoseconds) ||
	    !parse_u64(params[2], &tai_minus_utc) ||
	    tai_minus_utc > UINT64_MAX - utc ||
	    (tai = utc + tai_minus_utc,
	     !seconds_to_ns(tai, nanoseconds, &value))) {
		printf("milan_utc <utc-seconds> <nanoseconds> <tai-minus-utc>\n");
		return;
	}
	settime_ns(value);
	printf("UTC applied with TAI-UTC=%lu s; ", (unsigned long)tai_minus_utc);
	print_tod(gettime_ns());
}

define_command(milan_utc, milan_utc_handler,
	       "Set PHC from UTC plus the explicit TAI-UTC offset", SYSTEM_CMDS);

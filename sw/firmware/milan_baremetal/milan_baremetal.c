/* SPDX-License-Identifier: (GPL-2.0 OR MIT) */

#include <stdint.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>

#include <generated/csr.h>
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
/* issue #358: the timestamp latency corrections the fabric gPTP plane
 * is applying, {ingress_ns[31:16], egress_ns[15:0]}. RO live, option
 * OFF reads zero. Published so a bench reading this console sees what
 * the gateware IS applying, rather than what a config file says. */
#define MILAN_GPTP_LAT       0x7f0u
#define MILAN_PP_CTRL        0x920u
#define MILAN_PP_STAT        0x924u

#define MILAN_ID_MAGIC       0x4d494c4eu
#define MILAN_PTP_LOAD       0x1u
#define MILAN_PTP_SNAPSHOT   0x4u

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
	uint32_t hi1;
	uint32_t hi2;
	uint32_t lo;

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

/*
 * ---- Saved state: the flash writer behind KL_nvm_backend (issue #70) ----
 *
 * The fabric keeps the persisted record image in main memory (design page
 * docs/design/SAVED_STATE_FASTCONNECT.md section 8) and this firmware owns
 * the media (section 3): at boot it validates the two journal slots through
 * the memory-mapped flash, stages the newer accepted KLJ2 container in the
 * reserved window, hands the backend the control tuple of section 8.2 and
 * starts the restore walk; afterwards it heartbeats from the console's idle
 * hook and, when the backend reports committed changes no slot holds, wraps
 * the record area into a container and promotes it into the slot that is
 * NOT authoritative (section 7). The container's header and trailer are the
 * firmware's; the record area is written in place by the processor through
 * the backend and copied verbatim, which is why a record the processor has
 * never written is its span of 0xFF (section 6.1, the erased-record rule).
 */
#define MILAN_PP_NVM_SEL     0x934u
#define MILAN_PP_NVM_DATA    0x938u
#define MILAN_PP_NVM_STAT    0x93cu

#define MILAN_PP_STAT_RESTORE_DONE (1u << 2)
#define MILAN_PP_STAT_RESTORE_FAIL (1u << 3)
#define MILAN_PP_STAT_NVM_BACKED   (1u << 6)
#define MILAN_PP_STAT_NVM_BLANK    (1u << 7)

/* The backend's control words: PP_NVM_SEL indices (REGISTER_MAP.md 0x934). */
#define NVM_W_IMG_BASE   0u
#define NVM_W_IMG_LEN    1u
#define NVM_W_SEQ        2u
#define NVM_W_STAT       3u
#define NVM_W_MAP_IN     0x20u
#define NVM_W_MAP_OUT    0x30u
#define NVM_STAT_VALID   0x10u
#define NVM_STROBE_HB    0x1u
#define NVM_STROBE_ACK   0x2u
#define NVM_STROBE_START 0x4u
/* The snapshot-ownership contract (docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md
 * section 5.1): the capture strobes, the capture identity word and the eight
 * ownership words. */
#define NVM_STROBE_ARM     0x8u
#define NVM_STROBE_ATTEST  0x10u
#define NVM_STROBE_RELEASE 0x20u
#define NVM_STROBE_RELOAD  0x40u
#define NVM_W_CAPID        5u
#define NVM_W_OWN0         8u
#define NVM_OWN_WORDS      8u
/* The ownership vector is the record-id space, not a shape: 256 ids at 32
 * bits each. nvm_capture() unrolls its read with literal indices, so a
 * different count would silently read fewer words; this refuses it at
 * compile time without spending the one #error directive the builder gate
 * pins. */
typedef char nvm_own_words_is_eight[(NVM_OWN_WORDS == 8u) ? 1 : -1];
#define NVM_CAP_TAG        0xc3u
/* PP_NVM_STAT read bits. [3], [11] and [2] are the load bits: load pending
 * (a boot window load MAY STILL BE ACCEPTED -- read it as that, not as "no
 * RELOAD has been accepted"), the last RELOAD refused, and load accepted (a
 * RELOAD HAS been accepted since the backend's reset; while it is 0 the
 * backend arms no capture). */
#define NVM_RD_LOAD_ACC    (1u << 2)
#define NVM_RD_LOAD_PEND   (1u << 3)
#define NVM_RD_DEV_BUSY    (1u << 4)
#define NVM_RD_BACKED      (1u << 6)
#define NVM_RD_IMG_VALID   (1u << 7)
#define NVM_RD_DIRTY       (1u << 8)   /* committable image work */
#define NVM_RD_STALE       (1u << 9)
#define NVM_RD_COMMIT_BUSY (1u << 10)
#define NVM_RD_RELOAD_REF  (1u << 11)
#define NVM_RD_CAP_OPEN    (1u << 16)
#define NVM_RD_CAP_ATTEST  (1u << 19)
#define NVM_RD_ACK_REF     (1u << 20)
#define NVM_RD_ARM_REF     (1u << 21)
#define NVM_RD_PEND        (1u << 22)
#define NVM_RD_UNRES       (1u << 23)

/* The build-time refusal of section 14. A writer is compiled only against the
 * gateware contract it implements: the generator that emits contract 3
 * withdraws the older writer's image-base constant and publishes
 * MILAN_NVM_LIVE_BASE and MILAN_NVM_STAGE_BASE instead, so an older writer
 * does not compile against it, and this refusal keeps this writer from
 * compiling against an older generator. */
#if !defined(MILAN_NVM_CONTRACT) || MILAN_NVM_CONTRACT != 3
#error "saved-state writer implements contract 3; the gateware generator did not publish MILAN_NVM_CONTRACT 3"
#endif

/* KLJ2, design page section 6.1. */
#define KLJ2_MAGIC     0x324a4c4bu
#define KLJ2_FMT_VER   0x00020000u
#define KLJ2_HDR       40u
#define KLJ2_TRAILER   4u
#define REC_HDR        8u
#define REC_MAGIC      0x1722u
#define NVM_ERASED     0xffu
#define NVM_NAME_BYTES 64u
#define NVM_MAP_ENTRY  8u

/* Section 6.2 verdicts, then the writer's three transaction verdicts. */
#define VD_OK         0u
#define VD_MAGIC      1u
#define VD_VER        2u
#define VD_LEN        3u
#define VD_CRC        4u
#define VD_ENT        5u
#define VD_SHAPE      6u
#define VD_REC        7u
#define VD_STALE      8u
#define VD_BLANK      9u
#define VD_INCOMPLETE 10u
#define VD_ERASE      11u
#define VD_PROGRAM    12u
#define VD_VERIFY     13u
#define VD_COUNT      14u

/* The section 4.2 id blocks; the BINDING base is the donor's, generated. */
#define NVM_ID_CFG   0x00u
#define NVM_ID_SUID  0x01u
#define NVM_ID_RATE  0x02u
#define NVM_ID_CLKS  0x0au
#define NVM_ID_MCR   0x12u
#define NVM_ID_FMTI  0x30u
#define NVM_ID_FMTO  0x40u
#define NVM_ID_PTOF  0x50u
#define NVM_ID_MAPI  0x60u
#define NVM_ID_MAPO  0x70u
#define NVM_ID_NAME  0x80u
#define NVM_BLOCKS   12u

/* Fixed payload lengths, section 4.1. */
#define NVM_PL_CFG  2u
#define NVM_PL_SUID 8u
#define NVM_PL_RATE 4u
#define NVM_PL_CLKS 2u
#define NVM_PL_MCR  66u
#define NVM_PL_BIND 20u
#define NVM_PL_FMT  8u
#define NVM_PL_PTOF 4u

/*
 * The record area, sized from the generated counts alone so that every
 * store into the staged image is bounded by a constant. The compiler folds
 * these; the block table below walks the same set at run time and boot
 * refuses persistence if the two disagree.
 */
#define NVM_SZ(plen) (REC_HDR + (plen))
#define NVM_PORT_SZ(k, n, cl) (((k) < (n)) ? NVM_SZ(NVM_MAP_ENTRY * (cl)) : 0u)
#define NVM_MAPI_BYTES \
	(NVM_PORT_SZ(0u, MILAN_NVM_N_SPORT_IN, MILAN_NVM_MAPIN_CLUSTERS_0) + \
	 NVM_PORT_SZ(1u, MILAN_NVM_N_SPORT_IN, MILAN_NVM_MAPIN_CLUSTERS_1) + \
	 NVM_PORT_SZ(2u, MILAN_NVM_N_SPORT_IN, MILAN_NVM_MAPIN_CLUSTERS_2) + \
	 NVM_PORT_SZ(3u, MILAN_NVM_N_SPORT_IN, MILAN_NVM_MAPIN_CLUSTERS_3) + \
	 NVM_PORT_SZ(4u, MILAN_NVM_N_SPORT_IN, MILAN_NVM_MAPIN_CLUSTERS_4) + \
	 NVM_PORT_SZ(5u, MILAN_NVM_N_SPORT_IN, MILAN_NVM_MAPIN_CLUSTERS_5) + \
	 NVM_PORT_SZ(6u, MILAN_NVM_N_SPORT_IN, MILAN_NVM_MAPIN_CLUSTERS_6) + \
	 NVM_PORT_SZ(7u, MILAN_NVM_N_SPORT_IN, MILAN_NVM_MAPIN_CLUSTERS_7) + \
	 NVM_PORT_SZ(8u, MILAN_NVM_N_SPORT_IN, MILAN_NVM_MAPIN_CLUSTERS_8) + \
	 NVM_PORT_SZ(9u, MILAN_NVM_N_SPORT_IN, MILAN_NVM_MAPIN_CLUSTERS_9) + \
	 NVM_PORT_SZ(10u, MILAN_NVM_N_SPORT_IN, MILAN_NVM_MAPIN_CLUSTERS_10) + \
	 NVM_PORT_SZ(11u, MILAN_NVM_N_SPORT_IN, MILAN_NVM_MAPIN_CLUSTERS_11) + \
	 NVM_PORT_SZ(12u, MILAN_NVM_N_SPORT_IN, MILAN_NVM_MAPIN_CLUSTERS_12) + \
	 NVM_PORT_SZ(13u, MILAN_NVM_N_SPORT_IN, MILAN_NVM_MAPIN_CLUSTERS_13) + \
	 NVM_PORT_SZ(14u, MILAN_NVM_N_SPORT_IN, MILAN_NVM_MAPIN_CLUSTERS_14) + \
	 NVM_PORT_SZ(15u, MILAN_NVM_N_SPORT_IN, MILAN_NVM_MAPIN_CLUSTERS_15))
#define NVM_MAPO_BYTES \
	(NVM_PORT_SZ(0u, MILAN_NVM_N_SPORT_OUT, MILAN_NVM_MAPOUT_CLUSTERS_0) + \
	 NVM_PORT_SZ(1u, MILAN_NVM_N_SPORT_OUT, MILAN_NVM_MAPOUT_CLUSTERS_1) + \
	 NVM_PORT_SZ(2u, MILAN_NVM_N_SPORT_OUT, MILAN_NVM_MAPOUT_CLUSTERS_2) + \
	 NVM_PORT_SZ(3u, MILAN_NVM_N_SPORT_OUT, MILAN_NVM_MAPOUT_CLUSTERS_3) + \
	 NVM_PORT_SZ(4u, MILAN_NVM_N_SPORT_OUT, MILAN_NVM_MAPOUT_CLUSTERS_4) + \
	 NVM_PORT_SZ(5u, MILAN_NVM_N_SPORT_OUT, MILAN_NVM_MAPOUT_CLUSTERS_5) + \
	 NVM_PORT_SZ(6u, MILAN_NVM_N_SPORT_OUT, MILAN_NVM_MAPOUT_CLUSTERS_6) + \
	 NVM_PORT_SZ(7u, MILAN_NVM_N_SPORT_OUT, MILAN_NVM_MAPOUT_CLUSTERS_7) + \
	 NVM_PORT_SZ(8u, MILAN_NVM_N_SPORT_OUT, MILAN_NVM_MAPOUT_CLUSTERS_8) + \
	 NVM_PORT_SZ(9u, MILAN_NVM_N_SPORT_OUT, MILAN_NVM_MAPOUT_CLUSTERS_9) + \
	 NVM_PORT_SZ(10u, MILAN_NVM_N_SPORT_OUT, MILAN_NVM_MAPOUT_CLUSTERS_10) + \
	 NVM_PORT_SZ(11u, MILAN_NVM_N_SPORT_OUT, MILAN_NVM_MAPOUT_CLUSTERS_11) + \
	 NVM_PORT_SZ(12u, MILAN_NVM_N_SPORT_OUT, MILAN_NVM_MAPOUT_CLUSTERS_12) + \
	 NVM_PORT_SZ(13u, MILAN_NVM_N_SPORT_OUT, MILAN_NVM_MAPOUT_CLUSTERS_13) + \
	 NVM_PORT_SZ(14u, MILAN_NVM_N_SPORT_OUT, MILAN_NVM_MAPOUT_CLUSTERS_14) + \
	 NVM_PORT_SZ(15u, MILAN_NVM_N_SPORT_OUT, MILAN_NVM_MAPOUT_CLUSTERS_15))
#define NVM_FIXED_BYTES \
	(NVM_SZ(NVM_PL_CFG) + NVM_SZ(NVM_PL_SUID) + \
	 MILAN_NVM_N_AUDIO_UNIT * NVM_SZ(NVM_PL_RATE) + \
	 MILAN_NVM_N_CLK_DOM * (NVM_SZ(NVM_PL_CLKS) + NVM_SZ(NVM_PL_MCR)) + \
	 MILAN_NVM_N_STREAM_IN * (NVM_SZ(NVM_PL_BIND) + NVM_SZ(NVM_PL_FMT)) + \
	 MILAN_NVM_N_STREAM_OUT * (NVM_SZ(NVM_PL_FMT) + NVM_SZ(NVM_PL_PTOF)))
#define NVM_AREA_RAW (NVM_FIXED_BYTES + NVM_MAPI_BYTES + NVM_MAPO_BYTES + \
		      MILAN_NVM_N_NAME * NVM_SZ(NVM_NAME_BYTES))
#define NVM_AREA_LEN ((NVM_AREA_RAW + 3u) & ~3u)
#define NVM_PAD_LEN  (NVM_AREA_LEN - NVM_AREA_RAW)
#define NVM_IMG_LEN  (KLJ2_HDR + NVM_AREA_LEN + KLJ2_TRAILER)
#define NVM_N_REC    (2u + MILAN_NVM_N_AUDIO_UNIT + 2u * MILAN_NVM_N_CLK_DOM + \
		      2u * MILAN_NVM_N_STREAM_IN + 2u * MILAN_NVM_N_STREAM_OUT + \
		      MILAN_NVM_N_SPORT_IN + MILAN_NVM_N_SPORT_OUT + MILAN_NVM_N_NAME)

/* The media: two 64 KiB slots (section 5), one erase block each. */
#define NVM_SLOT_BYTES (MILAN_FLASH_JOURNAL_SIZE / 2u)
#define NVM_SLOT_A     MILAN_FLASH_JOURNAL_OFFSET
#define NVM_SLOT_B     (MILAN_FLASH_JOURNAL_OFFSET + NVM_SLOT_BYTES)
#define NVM_SLOT_NONE  0xffffffffu
#define NVM_FLASH_PAGE 256u
#define NVM_CMD_WREN   0x06u
#define NVM_CMD_RDSR   0x05u
#define NVM_CMD_SE     0xd8u
#define NVM_CMD_PP     0x02u
#define NVM_SR_WIP     0x01u

/*
 * Timing, generated (MILAN_NVM_*_MS, scripts/nvm_shape.py WRITER_TIMING_MS,
 * which cites the design-page section behind each). The heartbeat period is
 * half the section 9.4 maximum (500 ms), the erase timeout covers the
 * datasheet tSE maximum (3 s) inside the 8 s commit deadline, and the
 * debounce is the provisional value section 14 leaves open: a power cut
 * inside it loses exactly the changes nvm_dirty is reporting.
 */
#define NVM_MS(n)              ((uint64_t)(n) * 1000000ull)
#define NVM_HEARTBEAT_NS       NVM_MS(MILAN_NVM_HEARTBEAT_MS)
#define NVM_DEBOUNCE_NS        NVM_MS(MILAN_NVM_DEBOUNCE_MS)
#define NVM_ERASE_TIMEOUT_NS   NVM_MS(MILAN_NVM_ERASE_TIMEOUT_MS)
#define NVM_PROGRAM_TIMEOUT_NS NVM_MS(MILAN_NVM_PROGRAM_TIMEOUT_MS)
#define NVM_RESTORE_TIMEOUT_NS NVM_MS(MILAN_NVM_RESTORE_TIMEOUT_MS)
/* How many times the boot repeats a window load the backend refused. At a
 * cold boot no producer is enabled before the restore walk, so the first load
 * is accepted; a refusal means something outside that sequence wrote the
 * window, and each repeat re-bases and reloads from the start (section 5.3). */
#define NVM_LOAD_TRIES         4u

void set_idle_hook(void (*fptr)(void));

struct nvm_block {
	uint8_t base;
	uint8_t count;
	uint8_t map_dir;   /* 0 fixed payload, 1 input channel map, 2 output */
	uint16_t plen;
};

/* One record of the shape, by value: `ok` is 0 when there is no such record. */
struct nvm_rec {
	unsigned int id;
	unsigned int plen;
	int ok;
};

static const uint8_t nvm_mapin_clusters[16] = {
	MILAN_NVM_MAPIN_CLUSTERS_0, MILAN_NVM_MAPIN_CLUSTERS_1, MILAN_NVM_MAPIN_CLUSTERS_2, MILAN_NVM_MAPIN_CLUSTERS_3,
	MILAN_NVM_MAPIN_CLUSTERS_4, MILAN_NVM_MAPIN_CLUSTERS_5, MILAN_NVM_MAPIN_CLUSTERS_6, MILAN_NVM_MAPIN_CLUSTERS_7,
	MILAN_NVM_MAPIN_CLUSTERS_8, MILAN_NVM_MAPIN_CLUSTERS_9, MILAN_NVM_MAPIN_CLUSTERS_10, MILAN_NVM_MAPIN_CLUSTERS_11,
	MILAN_NVM_MAPIN_CLUSTERS_12, MILAN_NVM_MAPIN_CLUSTERS_13, MILAN_NVM_MAPIN_CLUSTERS_14, MILAN_NVM_MAPIN_CLUSTERS_15,
};
static const uint8_t nvm_mapout_clusters[16] = {
	MILAN_NVM_MAPOUT_CLUSTERS_0, MILAN_NVM_MAPOUT_CLUSTERS_1, MILAN_NVM_MAPOUT_CLUSTERS_2, MILAN_NVM_MAPOUT_CLUSTERS_3,
	MILAN_NVM_MAPOUT_CLUSTERS_4, MILAN_NVM_MAPOUT_CLUSTERS_5, MILAN_NVM_MAPOUT_CLUSTERS_6, MILAN_NVM_MAPOUT_CLUSTERS_7,
	MILAN_NVM_MAPOUT_CLUSTERS_8, MILAN_NVM_MAPOUT_CLUSTERS_9, MILAN_NVM_MAPOUT_CLUSTERS_10, MILAN_NVM_MAPOUT_CLUSTERS_11,
	MILAN_NVM_MAPOUT_CLUSTERS_12, MILAN_NVM_MAPOUT_CLUSTERS_13, MILAN_NVM_MAPOUT_CLUSTERS_14, MILAN_NVM_MAPOUT_CLUSTERS_15,
};
static const struct nvm_block nvm_blocks[NVM_BLOCKS] = {
	{NVM_ID_CFG, 1, 0, NVM_PL_CFG},
	{NVM_ID_SUID, 1, 0, NVM_PL_SUID},
	{NVM_ID_RATE, MILAN_NVM_N_AUDIO_UNIT, 0, NVM_PL_RATE},
	{NVM_ID_CLKS, MILAN_NVM_N_CLK_DOM, 0, NVM_PL_CLKS},
	{NVM_ID_MCR, MILAN_NVM_N_CLK_DOM, 0, NVM_PL_MCR},
	{MILAN_NVM_BIND_BASE, MILAN_NVM_N_STREAM_IN, 0, NVM_PL_BIND},
	{NVM_ID_FMTI, MILAN_NVM_N_STREAM_IN, 0, NVM_PL_FMT},
	{NVM_ID_FMTO, MILAN_NVM_N_STREAM_OUT, 0, NVM_PL_FMT},
	{NVM_ID_PTOF, MILAN_NVM_N_STREAM_OUT, 0, NVM_PL_PTOF},
	{NVM_ID_MAPI, MILAN_NVM_N_SPORT_IN, 1, 0},
	{NVM_ID_MAPO, MILAN_NVM_N_SPORT_OUT, 2, 0},
	{NVM_ID_NAME, MILAN_NVM_N_NAME, 0, NVM_NAME_BYTES},
};
static const char *const nvm_verdict_name[VD_COUNT] = {
	"VD_OK", "VD_MAGIC", "VD_VER", "VD_LEN", "VD_CRC", "VD_ENT", "VD_SHAPE",
	"VD_REC", "VD_STALE", "VD_BLANK", "VD_INCOMPLETE", "VD_ERASE",
	"VD_PROGRAM", "VD_VERIFY",
};

static int nvm_ready;
/* This writer has disabled itself for the rest of this reset and will never
 * commit again. It stops answering the liveness deadline, so the fabric
 * revokes nvm_backed and a controller reads the state as what it is, a port
 * with no writer -- never as a commit that is merely in flight (section
 * 5.3, the terminal row). */
static int nvm_retired;
static int nvm_in_commit;
static uint32_t nvm_seq;
static uint32_t nvm_auth_slot = NVM_SLOT_NONE;
static unsigned int nvm_verdict_a;
static unsigned int nvm_verdict_b;
static unsigned int nvm_last_verdict;
static unsigned int nvm_commits_ok;
static unsigned int nvm_commits_failed;
static unsigned int nvm_captures_refused;
static unsigned int nvm_acks_refused;
static uint64_t nvm_hb_last;
static uint64_t nvm_dirty_since;

/*
 * The live window and the private stage. Macros rather than helpers on
 * purpose: every store into either is then a constant base plus a loop index
 * the compiler bounds, which is what lets the builder gate's compiled census
 * place each one. The backend reads and writes the LIVE window's record area
 * in place; nothing but this firmware ever touches the STAGE, which is why an
 * attested copy in it cannot move under the seal, the program or the
 * read-back.
 */
#define NVM_IMG ((volatile uint8_t *)MILAN_NVM_LIVE_BASE)
#define NVM_STG ((volatile uint8_t *)MILAN_NVM_STAGE_BASE)

static const volatile uint8_t *nvm_slot(uint32_t offset)
{
	return (const volatile uint8_t *)(SPIFLASH_BASE + offset);
}

static uint32_t nvm_rd32(const volatile uint8_t *p)
{
	return (uint32_t)p[0] | ((uint32_t)p[1] << 8) |
	       ((uint32_t)p[2] << 16) | ((uint32_t)p[3] << 24);
}

/* CRC-32/ISO-HDLC over the image bytes, the trailer's algorithm (6.1). */
static uint32_t nvm_crc32(const volatile uint8_t *p, uint32_t len)
{
	uint32_t crc = 0xffffffffu;
	uint32_t i;
	unsigned int bit;

	for (i = 0; i < len; ++i) {
		crc ^= p[i];
		for (bit = 0; bit < 8; ++bit)
			crc = (crc >> 1) ^ (0xedb88320u & (0u - (crc & 1u)));
	}
	return ~crc;
}

/* CCITT-FALSE, the donor's F07.8 record digest, continued from `crc`. */
static uint16_t nvm_crc16(const volatile uint8_t *p, uint32_t len, uint16_t crc)
{
	uint32_t i;
	unsigned int bit;

	for (i = 0; i < len; ++i) {
		crc ^= (uint16_t)((uint16_t)p[i] << 8);
		for (bit = 0; bit < 8; ++bit)
			crc = (uint16_t)((crc & 0x8000u) ? ((crc << 1) ^ 0x1021u)
						  : ((unsigned int)crc << 1));
	}
	return crc;
}

static int nvm_all_erased(const volatile uint8_t *p, uint32_t len)
{
	uint32_t i;

	for (i = 0; i < len; ++i)
		if (p[i] != NVM_ERASED)
			return 0;
	return 1;
}

static unsigned int nvm_block_plen(const struct nvm_block *b, unsigned int index)
{
	if (b->map_dir == 1)
		return NVM_MAP_ENTRY * nvm_mapin_clusters[index & 0xfu];
	if (b->map_dir == 2)
		return NVM_MAP_ENTRY * nvm_mapout_clusters[index & 0xfu];
	return b->plen;
}

/* The next record this shape requires after id `last` (-1 for the first). */
static struct nvm_rec nvm_rec_after(int last)
{
	struct nvm_rec rec = {0x100u, 0, 0};
	const struct nvm_block *hit = 0;
	unsigned int i;

	for (i = 0; i < NVM_BLOCKS; ++i) {
		const struct nvm_block *b = &nvm_blocks[i];
		unsigned int first = (last + 1 > (int)b->base) ?
				     (unsigned int)(last + 1) : b->base;

		if (b->count && first < (unsigned int)b->base + b->count &&
		    first < rec.id) {
			rec.id = first;
			hit = b;
		}
	}
	if (hit) {
		rec.plen = nvm_block_plen(hit, rec.id - hit->base);
		rec.ok = 1;
	}
	return rec;
}

/* Whether `id` is a record of this shape, and its payload length if so. */
static struct nvm_rec nvm_rec_lookup(unsigned int id)
{
	struct nvm_rec rec = {id, 0, 0};
	unsigned int i;

	for (i = 0; i < NVM_BLOCKS; ++i) {
		const struct nvm_block *b = &nvm_blocks[i];

		if (id >= b->base && id < (unsigned int)b->base + b->count) {
			rec.plen = nvm_block_plen(b, id - b->base);
			rec.ok = 1;
		}
	}
	return rec;
}

/* The run-time walk and the compile-time sizes must describe one set. */
static int nvm_shape_consistent(void)
{
	unsigned int count = 0;
	unsigned int bytes = 0;
	struct nvm_rec rec = nvm_rec_after(-1);

	while (rec.ok) {
		count++;
		bytes += REC_HDR + rec.plen;
		rec = nvm_rec_after((int)rec.id);
	}
	return count == NVM_N_REC && bytes == NVM_AREA_RAW &&
	       NVM_IMG_LEN <= MILAN_NVM_IMAGE_MAX;
}

/* The framed record at `p`, if it is one of this shape's and its crc closes. */
static struct nvm_rec nvm_frame(const volatile uint8_t *p, uint32_t room)
{
	struct nvm_rec rec = {p[3], ((unsigned int)p[4] << 8) | p[5], 0};
	struct nvm_rec want;
	uint16_t crc;

	if ((((unsigned int)p[0] << 8) | p[1]) != REC_MAGIC ||
	    p[2] != MILAN_NVM_REC_LAYOUT || REC_HDR + rec.plen > room)
		return rec;
	crc = nvm_crc16(p + REC_HDR, rec.plen, nvm_crc16(p, 6, 0xffffu));
	if (crc != ((((unsigned int)p[6]) << 8) | p[7]))
		return rec;
	want = nvm_rec_lookup(rec.id);
	rec.ok = want.ok && want.plen == rec.plen;
	return rec;
}

/*
 * The section 6.2 acceptance order over a container at `img`, read through
 * whatever face holds it (the flash mapping or the staged window). Zero
 * records are ever applied here: the verdict decides whether the container
 * may be offered to the backend at all. Mirrors scripts/nvm_klj2.py's
 * klj2_decode rule for rule, including the erased-record rule of 6.1.
 */
static unsigned int nvm_validate(const volatile uint8_t *img)
{
	uint32_t img_len;
	uint32_t nrec;
	uint32_t pos;
	uint32_t end;
	uint32_t i;
	unsigned int seen = 0;
	int last = -1;

	if (nvm_all_erased(img, KLJ2_HDR))
		return VD_BLANK;
	if (nvm_rd32(img) != KLJ2_MAGIC)
		return VD_MAGIC;
	if ((nvm_rd32(img + 4) >> 16) != (KLJ2_FMT_VER >> 16))
		return VD_VER;
	img_len = nvm_rd32(img + 16);
	if (img_len < KLJ2_HDR + KLJ2_TRAILER || img_len > NVM_SLOT_BYTES)
		return VD_LEN;
	if (nvm_crc32(img, img_len - KLJ2_TRAILER) !=
	    nvm_rd32(img + img_len - KLJ2_TRAILER))
		return VD_CRC;
	if (nvm_rd32(img + 20) != MILAN_ENTITY_ID_LO ||
	    nvm_rd32(img + 24) != MILAN_ENTITY_ID_HI)
		return VD_ENT;
	if (nvm_rd32(img + 28) != MILAN_MODEL_ID_LO ||
	    nvm_rd32(img + 32) != MILAN_MODEL_ID_HI)
		return VD_SHAPE;
	if (nvm_rd32(img + 36) != MILAN_NVM_REC_LAYOUT)
		return VD_REC;
	nrec = nvm_rd32(img + 12);
	pos = KLJ2_HDR;
	end = img_len - KLJ2_TRAILER;
	for (i = 0; i < nrec; ++i) {
		struct nvm_rec rec;

		if (pos + REC_HDR > end)
			return VD_LEN;
		if (nvm_all_erased(img + pos, REC_HDR)) {
			/* never written since the media was blank: the next
			 * required record, its whole span erased */
			rec = nvm_rec_after(last);
			if (!rec.ok)
				return VD_REC;
			if (pos + REC_HDR + rec.plen > end)
				return VD_LEN;
			if (!nvm_all_erased(img + pos + REC_HDR, rec.plen))
				return VD_REC;
		} else {
			rec = nvm_frame(img + pos, end - pos);
			if (!rec.ok || (int)rec.id <= last)
				return VD_REC;
		}
		last = (int)rec.id;
		pos += REC_HDR + rec.plen;
		seen++;
	}
	if (pos + ((4u - ((pos - KLJ2_HDR) & 3u)) & 3u) != end)
		return VD_LEN;
	if (seen != NVM_N_REC)
		return VD_INCOMPLETE;
	return VD_OK;
}

/* The accepted container's sequence word; meaningful after VD_OK only. */
static uint32_t nvm_seq_of(const volatile uint8_t *img)
{
	return nvm_rd32(img + 8);
}

/* The ten little-endian header words of section 6.1, word 2 (the sequence)
 * excepted: a table rather than a switch, so no jump table is emitted and
 * the firmware transfers control through no register. */
static const uint32_t nvm_hdr_const[10] = {
	KLJ2_MAGIC, KLJ2_FMT_VER, 0, NVM_N_REC, NVM_IMG_LEN,
	MILAN_ENTITY_ID_LO, MILAN_ENTITY_ID_HI, MILAN_MODEL_ID_LO,
	MILAN_MODEL_ID_HI, MILAN_NVM_REC_LAYOUT,
};

static uint32_t nvm_hdr_word(unsigned int k, uint32_t seq)
{
	return (k == 2u) ? seq : nvm_hdr_const[k % 10u];
}

/* The header, for sequence `seq`, into the private stage. */
static void nvm_write_header(uint32_t seq)
{
	unsigned int i;

	for (i = 0; i < KLJ2_HDR; ++i)
		NVM_STG[i] = (uint8_t)(nvm_hdr_word(i >> 2, seq) >> (8u * (i & 3u)));
}

/* The trailer: CRC-32 over every preceding byte of the private stage. */
static void nvm_seal(void)
{
	uint32_t crc = nvm_crc32(NVM_STG, NVM_IMG_LEN - KLJ2_TRAILER);
	unsigned int i;

	for (i = 0; i < KLJ2_TRAILER; ++i)
		NVM_STG[NVM_IMG_LEN - KLJ2_TRAILER + i] = (uint8_t)(crc >> (8u * i));
}

/* Blank media behind a validated image: every record erased, the section
 * 6.1 alignment pad zero, sequence 0, into the stage. Two plain loops rather
 * than one with a conditional value, so the census can bound each store by
 * its loop. */
static void nvm_stage_blank_image(void)
{
	unsigned int i;

	for (i = 0; i < NVM_IMG_LEN; ++i)
		NVM_STG[i] = NVM_ERASED;
	for (i = 0; i < NVM_PAD_LEN; ++i)
		NVM_STG[KLJ2_HDR + NVM_AREA_RAW + i] = 0u;
	nvm_write_header(0);
	nvm_seal();
}

static void nvm_csr_write(unsigned int word, uint32_t value)
{
	milan_write(MILAN_PP_NVM_SEL, word);
	milan_write(MILAN_PP_NVM_DATA, value);
}

/*
 * The control tuple of section 8.2, in two steps. The RE-BASE: where the
 * record area is, how long it is, the per-port channel-map tables (framed
 * length and running prefix inside the group, direction distinct). Each of
 * these writes makes every record read open and arms the backend's load flag,
 * so it comes BEFORE the window load (snapshot-ownership section 5.3).
 */
static void nvm_rebase_backend(void)
{
	unsigned int dir;

	nvm_csr_write(NVM_W_IMG_BASE, MILAN_NVM_LIVE_BASE + KLJ2_HDR);
	nvm_csr_write(NVM_W_IMG_LEN, NVM_AREA_LEN);
	for (dir = 0; dir < 2; ++dir) {
		unsigned int n = dir ? MILAN_NVM_N_SPORT_OUT : MILAN_NVM_N_SPORT_IN;
		unsigned int word = dir ? NVM_W_MAP_OUT : NVM_W_MAP_IN;
		unsigned int prefix = 0;
		unsigned int k;

		for (k = 0; k < n && k < 16u; ++k) {
			unsigned int cl = dir ? nvm_mapout_clusters[k] :
						nvm_mapin_clusters[k];
			unsigned int flen = REC_HDR + NVM_MAP_ENTRY * cl;

			nvm_csr_write(word | k, (flen << 16) | prefix);
			prefix += flen;
		}
	}
}

/* The PUBLISH: the sequence and the verdict with the validity bit. Validity
 * is asserted only here, after nvm_validate and after the backend accepted
 * the load. */
static void nvm_publish(unsigned int verdict)
{
	nvm_csr_write(NVM_W_SEQ, nvm_seq);
	nvm_csr_write(NVM_W_STAT, NVM_STAT_VALID | (verdict & 0xfu));
}

/* Re-arm T-NVM-WRITER-ALIVE at most every NVM_HEARTBEAT_NS; the first
 * call answers at once, so the restore walk runs behind a live writer. */
static void nvm_heartbeat_tick(void)
{
	uint64_t now = gettime_ns();

	/* a retired writer answers no more: nvm_backed must fall */
	if (nvm_retired)
		return;
	if (nvm_hb_last == 0 || now < nvm_hb_last ||
	    now - nvm_hb_last >= NVM_HEARTBEAT_NS) {
		milan_write(MILAN_PP_NVM_STAT, NVM_STROBE_HB);
		nvm_hb_last = now;
	}
}

/* ---- the LiteSPI command master, one byte at a time, 1x mode ---------- */
static void nvm_spi_open(void)
{
	while (spiflash_master_status_read() &
	       (1u << CSR_SPIFLASH_MASTER_STATUS_RX_READY_OFFSET))
		spiflash_master_rxtx_read();
	spiflash_master_phyconfig_write(
		(8u << CSR_SPIFLASH_MASTER_PHYCONFIG_LEN_OFFSET) |
		(1u << CSR_SPIFLASH_MASTER_PHYCONFIG_WIDTH_OFFSET) |
		(1u << CSR_SPIFLASH_MASTER_PHYCONFIG_MASK_OFFSET));
	spiflash_master_cs_write(1);
}

static uint8_t nvm_spi_xfer(uint8_t out)
{
	while (!(spiflash_master_status_read() &
		 (1u << CSR_SPIFLASH_MASTER_STATUS_TX_READY_OFFSET)))
		;
	spiflash_master_rxtx_write(out);
	while (!(spiflash_master_status_read() &
		 (1u << CSR_SPIFLASH_MASTER_STATUS_RX_READY_OFFSET)))
		;
	return (uint8_t)spiflash_master_rxtx_read();
}

static void nvm_spi_close(void)
{
	spiflash_master_cs_write(0);
}

static uint8_t nvm_flash_status(void)
{
	uint8_t status;

	nvm_spi_open();
	nvm_spi_xfer(NVM_CMD_RDSR);
	nvm_spi_xfer(0);
	nvm_spi_xfer(0);
	status = nvm_spi_xfer(0);
	nvm_spi_close();
	return status;
}

static void nvm_flash_write_enable(void)
{
	nvm_spi_open();
	nvm_spi_xfer(NVM_CMD_WREN);
	nvm_spi_close();
}

/* Opens a command with a 24-bit address; the caller continues or closes. */
static void nvm_flash_command(uint8_t cmd, uint32_t addr)
{
	nvm_spi_open();
	nvm_spi_xfer(cmd);
	nvm_spi_xfer((uint8_t)(addr >> 16));
	nvm_spi_xfer((uint8_t)(addr >> 8));
	nvm_spi_xfer((uint8_t)addr);
}

/*
 * Poll write-in-progress until the device is ready or `timeout_ns` passes.
 * The heartbeat is serviced from this loop, which is what lets the liveness
 * deadline stay shorter than an erase (section 9.4). The clock is the PHC,
 * so a time step during the wait can end it early as a transaction failure;
 * the commit is then retried after the bracket lapses, nothing is lost.
 */
static int nvm_flash_wait(uint64_t timeout_ns)
{
	uint64_t start = gettime_ns();

	for (;;) {
		if (!(nvm_flash_status() & NVM_SR_WIP))
			return 1;
		nvm_heartbeat_tick();
		if (gettime_ns() - start > timeout_ns)
			return 0;
	}
}

static int nvm_slot_erase(uint32_t slot)
{
	const volatile uint8_t *back = nvm_slot(slot);
	unsigned int i;

	nvm_flash_write_enable();
	nvm_flash_command(NVM_CMD_SE, slot);
	nvm_spi_close();
	if (!nvm_flash_wait(NVM_ERASE_TIMEOUT_NS))
		return 0;
	for (i = 0; i < NVM_IMG_LEN; ++i)
		if (back[i] != NVM_ERASED)
			return 0;
	return 1;
}

static int nvm_slot_program(uint32_t slot)
{
	unsigned int off;

	for (off = 0; off < NVM_IMG_LEN; off += NVM_FLASH_PAGE) {
		unsigned int n = NVM_IMG_LEN - off;
		unsigned int i;

		if (n > NVM_FLASH_PAGE)
			n = NVM_FLASH_PAGE;
		nvm_flash_write_enable();
		nvm_flash_command(NVM_CMD_PP, slot + off);
		for (i = 0; i < n; ++i)
			nvm_spi_xfer(NVM_STG[off + i]);
		nvm_spi_close();
		if (!nvm_flash_wait(NVM_PROGRAM_TIMEOUT_NS))
			return 0;
		nvm_heartbeat_tick();
	}
	return 1;
}

static int nvm_slot_matches(uint32_t slot)
{
	const volatile uint8_t *back = nvm_slot(slot);
	unsigned int i;

	for (i = 0; i < NVM_IMG_LEN; ++i)
		if (back[i] != NVM_STG[i])
			return 0;
	return 1;
}

static char nvm_slot_letter(uint32_t slot)
{
	if (slot == NVM_SLOT_A)
		return 'A';
	return (slot == NVM_SLOT_B) ? 'B' : '-';
}

static uint32_t nvm_word_read(unsigned int word)
{
	milan_write(MILAN_PP_NVM_SEL, word);
	return milan_read(MILAN_PP_NVM_DATA);
}

/* The stage starts every capture as the last VERIFIED container: the
 * authoritative slot, or the blank image when no slot was ever accepted. A
 * record the backend reports open keeps exactly these bytes. */
static void nvm_prefill_stage(void)
{
	unsigned int i;

	if (nvm_auth_slot == NVM_SLOT_NONE) {
		nvm_stage_blank_image();
		return;
	}
	for (i = 0; i < NVM_IMG_LEN; ++i)
		NVM_STG[i] = nvm_slot(nvm_auth_slot)[i];
}

/*
 * The capture (snapshot-ownership sections 4 and 7 step 3). Everything
 * between the arm and the attest runs under the backend's grant hold: a WRITE
 * or ERASE the producer requests now is deferred, never refused. Only records
 * the backend reports as completed are copied; an open record keeps its last
 * verified bytes. The attestation is the backend's, latched in hardware: it
 * is false if any mutating operation was granted after the arm, which can
 * only happen once the hold lapsed, and a copy it does not attest never
 * reaches flash.
 */
static uint32_t nvm_capture(void)
{
	uint32_t own[NVM_OWN_WORDS];
	uint32_t stat;
	uint32_t cap_id;
	unsigned int i;
	unsigned int next;
	unsigned int off = 0;
	int copy;
	struct nvm_rec rec;

	nvm_prefill_stage();
	milan_write(MILAN_PP_NVM_STAT, NVM_STROBE_ARM);
	stat = milan_read(MILAN_PP_NVM_STAT);
	if (!(stat & NVM_RD_CAP_OPEN) || (stat & NVM_RD_ARM_REF)) {
		/* not armed, or a capture an unfinished attempt left open:
		 * close it, so the next service call arms afresh */
		milan_write(MILAN_PP_NVM_STAT, NVM_STROBE_RELEASE);
		return 0;
	}
	/* The identity is RETURNED, never written through a pointer: the
	 * builder gate's compiled census places a store by computing its
	 * address, and a store through an out-parameter is one it refuses
	 * rather than omits. An accepted ARM advances the identity from 0,
	 * so 0 is an unambiguous "no capture" here. */
	/* THE WHOLE OWNERSHIP VECTOR, read BEFORE the copy and not during it
	 * (section 7 step 3.3): the vector is exact between the arm and the
	 * attestation, and sampling it per record instead would read a bit the
	 * hold's lapse had already moved -- a capture that quietly skipped a
	 * record it had been told to copy, rather than one the attestation
	 * refuses. UNROLLED with literal indices because the builder gate's
	 * compiled census places a store by computing its address, and a store
	 * into an array at a variable index is one it refuses rather than
	 * places. Eight words is the record-id space (256 ids, 32 bits each)
	 * and not a shape, and the typedef above refuses any other count.
	 *
	 * The comment sits HERE, above a statement that is not one of the
	 * pinned stores, because that gate takes a statement back to the last
	 * ';', '{' or '}' and would otherwise read this text as part of the
	 * first store's spelling. */
	cap_id = nvm_word_read(NVM_W_CAPID);
	own[0] = nvm_word_read(NVM_W_OWN0 + 0u);
	own[1] = nvm_word_read(NVM_W_OWN0 + 1u);
	own[2] = nvm_word_read(NVM_W_OWN0 + 2u);
	own[3] = nvm_word_read(NVM_W_OWN0 + 3u);
	own[4] = nvm_word_read(NVM_W_OWN0 + 4u);
	own[5] = nvm_word_read(NVM_W_OWN0 + 5u);
	own[6] = nvm_word_read(NVM_W_OWN0 + 6u);
	own[7] = nvm_word_read(NVM_W_OWN0 + 7u);
	/* The copy, record by record, with the STORE ITSELF guarded by the
	 * generated constant NVM_AREA_RAW. That guard is what the builder
	 * gate's compiled census reads: it places a store by the branch that
	 * dominates it, so the index is a bounded range inside the stage and
	 * not a running offset it would have to refuse. The guard is not
	 * decoration either -- nvm_rec_after() walks the live window, and a
	 * record area that disagreed with the generated length would otherwise
	 * write past the stage.
	 *
	 * BRACED on purpose: the gate's pinned-store rule takes a statement
	 * back to the last ';', '{' or '}', so a store behind a brace-less
	 * `if` reads as part of the condition and the rule never sees it.
	 * Every store in this file is to be visible to it. */
	rec = nvm_rec_after(-1);
	while (rec.ok) {
		copy = !((own[rec.id >> 5] >> (rec.id & 31u)) & 1u);
		next = off + REC_HDR + rec.plen;
		if (copy) {
			for (i = off; i < NVM_AREA_RAW; ++i) {
				if (i >= next) {
					break;
				}
				NVM_STG[KLJ2_HDR + i] = NVM_IMG[KLJ2_HDR + i];
			}
		}
		off = next;
		rec = nvm_rec_after((int)rec.id);
	}
	/* the copy's loads complete before the attest strobe leaves */
	__asm__ volatile("fence rw, rw" ::: "memory");
	milan_write(MILAN_PP_NVM_STAT, NVM_STROBE_ATTEST);
	if (!(milan_read(MILAN_PP_NVM_STAT) & NVM_RD_CAP_ATTEST)) {
		milan_write(MILAN_PP_NVM_STAT, NVM_STROBE_RELEASE);
		return 0;
	}
	return cap_id;
}

/*
 * The A/B promotion of section 7, over an ATTESTED capture: seal the private
 * stage under the next sequence, then erase, program and read back the slot
 * that is NOT authoritative. The slot can only ever hold attested content, so
 * it is promoted as soon as it verifies, whatever the acknowledgement is told
 * afterwards; the acknowledgement quotes the capture identity and retires
 * only the work that capture holds. A transaction failure publishes its
 * verdict, which revokes nvm_backed in the backend (section 9.2), and
 * releases the capture, which hands its work back to the dirty state.
 */
static int nvm_commit(const char *why)
{
	uint32_t next = nvm_seq + 1u;
	uint32_t target = (nvm_auth_slot == NVM_SLOT_A) ? NVM_SLOT_B : NVM_SLOT_A;
	uint32_t cap_id;
	unsigned int vd;

	nvm_in_commit = 1;
	cap_id = nvm_capture();
	if (cap_id == 0) {
		printf("Milan NVM: commit (%s) deferred, the capture was not attested.\n",
		       why);
		nvm_captures_refused++;
		nvm_dirty_since = 0;
		nvm_in_commit = 0;
		return 0;
	}
	nvm_write_header(next);
	nvm_seal();
	vd = nvm_validate(NVM_STG);
	if (vd != VD_OK) {
		milan_write(MILAN_PP_NVM_STAT, NVM_STROBE_RELEASE);
		printf("Milan NVM: commit (%s) deferred, the attested capture reads %s.\n",
		       why, nvm_verdict_name[vd]);
		nvm_dirty_since = 0;
		nvm_in_commit = 0;
		return 0;
	}
	milan_write(MILAN_PP_NVM_STAT, NVM_STROBE_START);
	if (!nvm_slot_erase(target))
		vd = VD_ERASE;
	else if (!nvm_slot_program(target))
		vd = VD_PROGRAM;
	else if (nvm_validate(nvm_slot(target)) != VD_OK ||
		 nvm_seq_of(nvm_slot(target)) != next || !nvm_slot_matches(target))
		vd = VD_VERIFY;
	nvm_last_verdict = vd;
	nvm_dirty_since = 0;
	nvm_in_commit = 0;
	if (vd != VD_OK) {
		nvm_csr_write(NVM_W_STAT, NVM_STAT_VALID | vd);
		milan_write(MILAN_PP_NVM_STAT, NVM_STROBE_RELEASE);
		nvm_commits_failed++;
		printf("Milan NVM: commit (%s) seq %lu to slot %c FAILED: %s; released, not acknowledged.\n",
		       why, (unsigned long)next, nvm_slot_letter(target),
		       nvm_verdict_name[vd]);
		return 0;
	}
	nvm_seq = next;
	nvm_auth_slot = target;
	nvm_csr_write(NVM_W_SEQ, next);
	nvm_csr_write(NVM_W_STAT, NVM_STAT_VALID | VD_OK);
	milan_write(MILAN_PP_NVM_STAT, NVM_STROBE_ACK | (cap_id << 16));
	if (milan_read(MILAN_PP_NVM_STAT) & NVM_RD_ACK_REF) {
		nvm_acks_refused++;
		printf("Milan NVM: commit (%s) seq %lu -> slot %c, %u B, verified; acknowledgement REFUSED, the captured work stays owned.\n",
		       why, (unsigned long)next, nvm_slot_letter(target),
		       (unsigned int)NVM_IMG_LEN);
		return 0;
	}
	nvm_commits_ok++;
	printf("Milan NVM: commit (%s) seq %lu -> slot %c, %u B, capture %lu acknowledged.\n",
	       why, (unsigned long)next, nvm_slot_letter(target),
	       (unsigned int)NVM_IMG_LEN, (unsigned long)cap_id);
	return 1;
}

/*
 * The console's idle hook: heartbeat, then commit once the backend has
 * reported committable work for the whole debounce window with no commit
 * bracket in flight. A record operation in flight does NOT block a commit:
 * its record is open and the capture keeps that record's last verified bytes,
 * so a wedged producer cannot stop every other record from being saved
 * (snapshot-ownership section 7 step 2).
 */
static void nvm_service(void)
{
	uint32_t stat;
	uint64_t now;

	nvm_heartbeat_tick();
	if (!nvm_ready || nvm_in_commit)
		return;
	stat = milan_read(MILAN_PP_NVM_STAT);
	if (!(stat & NVM_RD_DIRTY)) {
		nvm_dirty_since = 0;
		return;
	}
	if (stat & NVM_RD_COMMIT_BUSY)
		return;
	now = gettime_ns();
	if (nvm_dirty_since == 0 || now < nvm_dirty_since) {
		nvm_dirty_since = now;
		return;
	}
	if (now - nvm_dirty_since >= NVM_DEBOUNCE_NS)
		nvm_commit("dirty");
}

static uint32_t nvm_pick_slot(unsigned int vd_a, uint32_t seq_a,
			      unsigned int vd_b, uint32_t seq_b)
{
	if (vd_a == VD_OK && vd_b == VD_OK)
		return ((int32_t)(seq_a - seq_b) >= 0) ? NVM_SLOT_A : NVM_SLOT_B;
	if (vd_a == VD_OK)
		return NVM_SLOT_A;
	return (vd_b == VD_OK) ? NVM_SLOT_B : NVM_SLOT_NONE;
}

/* Wait, bounded, for the device face to go idle, heartbeating. A window load
 * repeated while an operation is still in flight would meet the same refusal
 * every time; one that is merely slow converges here (section 5.3). */
static void nvm_wait_dev_idle(void)
{
	uint64_t start = gettime_ns();

	while (milan_read(MILAN_PP_NVM_STAT) & NVM_RD_DEV_BUSY) {
		nvm_heartbeat_tick();
		if (gettime_ns() - start > NVM_RESTORE_TIMEOUT_NS) {
			printf("Milan NVM: the device face did not go idle before the repeated window load.\n");
			return;
		}
	}
}

/* Start the boot restore walk and wait for it to sequence, heartbeating. */
static void nvm_restore_walk(void)
{
	uint64_t start = gettime_ns();

	/* PP_CTRL[1] only: the entity enable, bit 0, is the choke point's. */
	milan_write(MILAN_PP_CTRL, milan_read(MILAN_PP_CTRL) | 0x2u);
	while (!(milan_read(MILAN_PP_STAT) & MILAN_PP_STAT_RESTORE_DONE)) {
		nvm_heartbeat_tick();
		if (gettime_ns() - start > NVM_RESTORE_TIMEOUT_NS) {
			printf("Milan NVM: the restore walk did not sequence in time.\n");
			break;
		}
	}
	milan_write(MILAN_PP_CTRL, milan_read(MILAN_PP_CTRL) & ~0x2u);
}

/* The live window becomes the chosen verified slot, or the blank image when
 * no slot was ever accepted. */
static void nvm_fill_window(uint32_t chosen)
{
	unsigned int i;

	if (chosen != NVM_SLOT_NONE) {
		const volatile uint8_t *src = nvm_slot(chosen);

		for (i = 0; i < NVM_IMG_LEN; ++i)
			NVM_IMG[i] = src[i];
	} else {
		nvm_stage_blank_image();
		for (i = 0; i < NVM_IMG_LEN; ++i)
			NVM_IMG[i] = NVM_STG[i];
	}
}

/*
 * One window load (section 5.3): re-base, load, RELOAD, in that order, and
 * the backend's answer. The backend accepts the RELOAD only if no mutating
 * operation was granted after the re-base and none was in flight at it, so
 * nothing but this load wrote the window in between; it refuses it, and
 * changes nothing, otherwise. Returns 1 when accepted.
 */
static int nvm_load_window(uint32_t chosen)
{
	nvm_rebase_backend();
	nvm_fill_window(chosen);
	/* the load's stores complete before the RELOAD strobe leaves */
	__asm__ volatile("fence rw, rw" ::: "memory");
	milan_write(MILAN_PP_NVM_STAT, NVM_STROBE_RELOAD);
	return !(milan_read(MILAN_PP_NVM_STAT) & NVM_RD_RELOAD_REF);
}

/*
 * Boot: read both slots, offer the newer accepted one, or blank media
 * behind a validated all-erased image when neither is accepted; then the
 * restore walk, then the idle hook. Runs after the AEM image is in place and
 * before the entity is advertised, the order Milan 5.5.3.5.2 requires.
 *
 * The backend says which boot this is (section 7 step 1). Load pending (the
 * boot load may still be accepted) with no restore walk sequenced yet is a
 * cold boot: re-base, load, RELOAD, publish, restore walk. Load pending with
 * the walk ALREADY sequenced is neither: the window is live and unvalidated,
 * and this writer stays disabled rather than reload over a producer. Load NOT
 * pending is a WRITER RESTART WITHOUT A FABRIC RESET, split on the second bit
 * the backend publishes:
 *
 *   [3] 0 with [2] LOAD ACCEPTED 1: the backend has kept ownership since a
 *   window load it accepted, so the writer RE-ATTACHES: it never re-bases,
 *   loads or RELOADs (the backend would refuse the RELOAD anyway), releases
 *   whatever capture the previous run left open, which hands the captured
 *   work back, and publishes the sequence the media holds.
 *
 *   [3] 0 with [2] 0: no window load was ever accepted in this boot, so
 *   nothing in it may be captured or committed (the backend arms no capture
 *   while [2] is 0, which is rule 9). The writer does NOT re-attach and does
 *   not validate a window no load vouches for: it stays retired until the
 *   next reset.
 */
static void nvm_boot(void)
{
	uint32_t seq_a;
	uint32_t seq_b;
	uint32_t chosen;
	uint32_t stat;
	unsigned int verdict;
	unsigned int tries = 0;
	int loaded = 0;
	int live = 0;			/* the window went live */

	if (!nvm_shape_consistent()) {
		printf("Milan NVM: the record set does not match the generated shape; persistence disabled.\n");
		return;
	}
	nvm_verdict_a = nvm_validate(nvm_slot(NVM_SLOT_A));
	nvm_verdict_b = nvm_validate(nvm_slot(NVM_SLOT_B));
	seq_a = (nvm_verdict_a == VD_OK) ? nvm_seq_of(nvm_slot(NVM_SLOT_A)) : 0;
	seq_b = (nvm_verdict_b == VD_OK) ? nvm_seq_of(nvm_slot(NVM_SLOT_B)) : 0;
	chosen = nvm_pick_slot(nvm_verdict_a, seq_a, nvm_verdict_b, seq_b);
	if (chosen != NVM_SLOT_NONE) {
		nvm_seq = (chosen == NVM_SLOT_A) ? seq_a : seq_b;
		verdict = VD_OK;
	} else {
		nvm_seq = 0;
		verdict = (nvm_verdict_a != VD_BLANK) ? nvm_verdict_a : nvm_verdict_b;
	}
	nvm_auth_slot = chosen;
	nvm_last_verdict = verdict;
	stat = milan_read(MILAN_PP_NVM_STAT);
	if ((stat >> 24) != NVM_CAP_TAG) {
		/* the runtime cross-check of the build-time refusal (section
		 * 14): a writer of contract 3 never acknowledges under an older
		 * rule; the window is still loaded and published for the walk */
		nvm_fill_window(chosen);
		nvm_rebase_backend();
		nvm_publish(verdict);
		printf("Milan NVM: the backend does not carry saved-state contract 3 (tag %02lx); the writer is disabled.\n",
		       (unsigned long)(stat >> 24));
	} else if (!(stat & NVM_RD_LOAD_PEND) && !(stat & NVM_RD_LOAD_ACC)) {
		/* the boot load is OVER and no load was ever accepted, so this
		 * boot may capture nothing. A re-attach could commit nothing; it
		 * would only publish a validity bit over a window no accepted
		 * load vouches for. The writer stays retired: it never commits
		 * and stops answering the liveness deadline. */
		nvm_retired = 1;
		printf("Milan NVM: no window load was accepted in this boot; the writer stays retired until the next reset.\n");
	} else if (!(stat & NVM_RD_LOAD_PEND)) {
		milan_write(MILAN_PP_NVM_STAT, NVM_STROBE_RELEASE);
		nvm_publish(verdict);
		nvm_ready = 1;
		printf("Milan NVM: writer restarted on a live backend; re-attached, the window is not reloaded.\n");
	} else if (milan_read(MILAN_PP_STAT) & MILAN_PP_STAT_RESTORE_DONE) {
		/* the writer rule that goes with the backend's window-live term:
		 * load pending 1 with the restore walk ALREADY SEQUENCED is not a
		 * cold boot. The producer has been able to write the window since
		 * the fabric's reset and nothing would re-derive the entity's
		 * state from a load, so this writer never takes the cold-boot
		 * path over it: it stays disabled until the next reset. (The
		 * backend refuses that RELOAD anyway: the window went live at the
		 * walk's first read.) */
		nvm_retired = 1;
		printf("Milan NVM: the window went live without a validated load; the writer stays disabled until the next reset.\n");
	} else {
		while (!loaded && tries < NVM_LOAD_TRIES) {
			loaded = nvm_load_window(chosen);
			tries++;
			/* read [3] after a refusal. Load pending 0 without an
			 * accepted load is the window having GONE LIVE: no later
			 * RELOAD can be accepted, and a repeat would only re-base
			 * and refill a window the producer owns. Stop here. */
			if (!loaded && !(milan_read(MILAN_PP_NVM_STAT) & NVM_RD_LOAD_PEND)) {
				live = 1;
				break;
			}
			/* an operation that is merely SLOW must not spend every
			 * attempt in flight. Wait, bounded, for the device face
			 * to go idle before repeating. */
			if (!loaded && tries < NVM_LOAD_TRIES)
				nvm_wait_dev_idle();
		}
		if (loaded) {
			/* the window now holds a validated container: every
			 * record in it is a completed record, owned by the last
			 * verified state */
			nvm_publish(verdict);
			nvm_ready = 1;
			if (tries > 1)
				printf("Milan NVM: the backend refused %u window load(s); accepted at attempt %u.\n",
				       tries - 1u, tries);
		} else {
			/* this writer will never commit again, so it stops
			 * answering the liveness deadline and the fabric revokes
			 * nvm_backed. The restore walk below still runs, blind,
			 * and the entity comes up on defaults; the status says so
			 * (img_valid 0, restore fail 1, pending 1, backed 0). */
			nvm_retired = 1;
			if (live)
				printf("Milan NVM: the backend refused %u window load(s) and the window then went live; the writer is disabled until the next reset.\n",
				       tries);
			else
				printf("Milan NVM: the backend refused %u window loads; the window is not validated and the writer is disabled until the next reset.\n",
				       tries);
		}
	}
	/* a restore walk the fabric already sequenced since its reset is not run
	 * again: a re-attached writer finds the entity live */
	if (!(milan_read(MILAN_PP_STAT) & MILAN_PP_STAT_RESTORE_DONE))
		nvm_restore_walk();
	stat = milan_read(MILAN_PP_STAT);
	printf("Milan NVM: slot A %s seq %lu, slot B %s seq %lu; offered %c seq %lu (%s), %u B at 0x%08x; walk done=%lu fail=%lu blank=%lu backed=%lu.\n",
	       nvm_verdict_name[nvm_verdict_a], (unsigned long)seq_a,
	       nvm_verdict_name[nvm_verdict_b], (unsigned long)seq_b,
	       nvm_slot_letter(chosen), (unsigned long)nvm_seq,
	       nvm_verdict_name[verdict], (unsigned int)NVM_IMG_LEN,
	       (unsigned int)MILAN_NVM_LIVE_BASE,
	       (unsigned long)((stat >> 2) & 1u), (unsigned long)((stat >> 3) & 1u),
	       (unsigned long)((stat >> 7) & 1u), (unsigned long)((stat >> 6) & 1u));
	set_idle_hook(nvm_service);
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
	milan_write(MILAN_MAC_ADDR_LO, MILAN_STATION_MAC_LO);
	milan_write(MILAN_MAC_ADDR_HI, MILAN_STATION_MAC_HI);
	/* Receive the link-local multicast control groups without promiscuous mode. */
	milan_write(MILAN_MAC_CTRL, milan_read(MILAN_MAC_CTRL) | (1u << 3));

	/* Fabric owns media/control. Firmware only provides the generated policy. */
	milan_write(MILAN_AAF_CTRL, (MILAN_SR_VID << 16) | 1u);
	milan_write(MILAN_LWSRP_VID, MILAN_SR_VID);
	milan_write(MILAN_LWSRP_CTRL, MILAN_LWSRP_CTRL_RESET | 3u);
	milan_write(MILAN_MAAP_CTRL, ((MILAN_N_TALKERS + 1u) << 8) | 1u);
	/* clocking.crf_output.enabled: talker enable + class-A declare, or 0. */
	milan_write(MILAN_CRF_TX_CTRL, MILAN_CRF_TX_CTRL_BOOT);
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
	/* Saved state is restored before the entity model is loaded and
	 * long before the entity is advertised; the verifier's verdict then
	 * flows straight into the choke point, with nothing between them. */
	nvm_boot();
	aem_loaded = load_aem_image();
	entity_advertise(aem_loaded);
}

define_init_func(milan_init);

static void milan_status_handler(int nb_params, char **params)
{
	uint32_t gm_lo;
	uint32_t gm_hi;
	uint32_t parent_lo;
	uint32_t parent_hi;
	uint32_t pdelay_ns;
	uint32_t as_path;
	uint32_t clkv_stat;
	uint32_t gptp_lat;

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
	gptp_lat = milan_read(MILAN_GPTP_LAT);
	printf("ID=%08lx VERSION=%08lx PTP_CTRL=%08lx ADP_CTRL=%08lx PP_CTRL=%08lx PP_STAT=%08lx AEM=%s\n",
	       (unsigned long)milan_read(MILAN_ID),
	       (unsigned long)milan_read(MILAN_VERSION),
	       (unsigned long)milan_read(MILAN_PTP_CTRL),
	       (unsigned long)milan_read(MILAN_ADP_CTRL),
	       (unsigned long)milan_read(MILAN_PP_CTRL),
	       (unsigned long)milan_read(MILAN_PP_STAT),
	       aem_loaded ? "loaded" : "disabled");
	printf("GPTP_GM=%08lx%08lx GPTP_PARENT=%08lx%08lx PDELAY_NS=%lu AS_PATH_COUNT=%lu AS_PATH_GEN=%lu CLKV_STAT=%08lx SYNC=%lu ASCAPABLE=%lu TU=%lu GPTP_LAT=%08lx\n",
	       (unsigned long)gm_hi, (unsigned long)gm_lo,
	       (unsigned long)parent_hi, (unsigned long)parent_lo,
	       (unsigned long)pdelay_ns,
	       (unsigned long)(as_path & 0xfu),
	       (unsigned long)((as_path >> 4) & 0xfu),
	       (unsigned long)clkv_stat,
	       (unsigned long)((clkv_stat >> 1) & 1u),
	       (unsigned long)((clkv_stat >> 16) & 1u),
	       (unsigned long)(clkv_stat & 1u),
	       (unsigned long)gptp_lat);
	print_tod(gettime_ns());
}

define_command(milan_status, milan_status_handler,
	       "Show fabric, gPTP publication, entity-image and PHC status", SYSTEM_CMDS);

static int nvm_arg_is(const char *arg, const char *word)
{
	while (*arg && *arg == *word) {
		++arg;
		++word;
	}
	return *arg == '\0' && *word == '\0';
}

static void nvm_print_status(void)
{
	unsigned int vd_a = nvm_validate(nvm_slot(NVM_SLOT_A));
	unsigned int vd_b = nvm_validate(nvm_slot(NVM_SLOT_B));
	uint32_t seq_a = (vd_a == VD_OK) ? nvm_seq_of(nvm_slot(NVM_SLOT_A)) : 0;
	uint32_t seq_b = (vd_b == VD_OK) ? nvm_seq_of(nvm_slot(NVM_SLOT_B)) : 0;
	uint32_t stat = milan_read(MILAN_PP_NVM_STAT);

	printf("NVM: slot A %s seq %lu, slot B %s seq %lu, authoritative %c, image seq %lu, %u records, %u B at 0x%08x, %s\n",
	       nvm_verdict_name[vd_a], (unsigned long)seq_a,
	       nvm_verdict_name[vd_b], (unsigned long)seq_b,
	       nvm_slot_letter(nvm_auth_slot), (unsigned long)nvm_seq,
	       (unsigned int)NVM_N_REC, (unsigned int)NVM_IMG_LEN,
	       (unsigned int)MILAN_NVM_LIVE_BASE,
	       nvm_ready ? "writer live" : (nvm_retired ? "writer retired"
						       : "writer disabled"));
	printf("NVM: PP_NVM_STAT=%08lx backed=%lu dirty=%lu stale=%lu valid=%lu commit_busy=%lu dev_busy=%lu pend=%lu unres=%lu load_pend=%lu load_acc=%lu reload_ref=%lu verdict=%s; commits ok=%u failed=%u captures refused=%u acks refused=%u last=%s\n",
	       (unsigned long)stat,
	       (unsigned long)((stat >> 6) & 1u), (unsigned long)((stat >> 8) & 1u),
	       (unsigned long)((stat >> 9) & 1u), (unsigned long)((stat >> 7) & 1u),
	       (unsigned long)((stat >> 10) & 1u), (unsigned long)((stat >> 4) & 1u),
	       (unsigned long)((stat >> 22) & 1u), (unsigned long)((stat >> 23) & 1u),
	       (unsigned long)((stat >> 3) & 1u), (unsigned long)((stat >> 2) & 1u),
	       (unsigned long)((stat >> 11) & 1u),
	       nvm_verdict_name[(stat >> 12) & 0xfu], nvm_commits_ok,
	       nvm_commits_failed, nvm_captures_refused, nvm_acks_refused,
	       nvm_verdict_name[nvm_last_verdict]);
	/* Section 16, option A: the controller reads one summary bit and the
	 * per-record detail stays here, on the backend's own face. */
	if (stat & NVM_RD_UNRES) {
		unsigned int w;

		printf("NVM: unresolved records, their last verified bytes stand:");
		for (w = 0; w < NVM_OWN_WORDS; ++w) {
			uint32_t bits = nvm_word_read(NVM_W_OWN0 + w);
			unsigned int b;

			for (b = 0; b < 32u; ++b)
				if ((bits >> b) & 1u)
					printf(" 0x%02x", w * 32u + b);
		}
		printf("\n");
	}
}

static void milan_nvm_handler(int nb_params, char **params)
{
	if (nb_params == 0) {
		nvm_print_status();
		return;
	}
	if (nb_params == 1 && nvm_arg_is(params[0], "commit")) {
		if (!nvm_ready)
			printf("NVM: the writer is disabled on this build.\n");
		else
			nvm_commit("console");
		return;
	}
	if (nb_params == 1 && nvm_arg_is(params[0], "wipe")) {
		int a = nvm_slot_erase(NVM_SLOT_A);
		int b = nvm_slot_erase(NVM_SLOT_B);

		nvm_auth_slot = NVM_SLOT_NONE;
		printf("NVM: slot A %s, slot B %s; the staged image is unchanged, reboot to observe a blank boot.\n",
		       a ? "erased" : "ERASE FAILED", b ? "erased" : "ERASE FAILED");
		return;
	}
	printf("milan_nvm [commit|wipe]\n");
}

define_command(milan_nvm, milan_nvm_handler,
	       "Show the saved-state slots and backing store; commit or wipe them", SYSTEM_CMDS);

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
	uint64_t seconds;
	uint64_t nanoseconds = 0;
	uint64_t value;

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
	uint64_t utc;
	uint64_t nanoseconds;
	uint64_t tai_minus_utc;
	uint64_t tai;
	uint64_t value;

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

/* SPDX-License-Identifier: (GPL-2.0 OR MIT) */
/*
 * nvm_host.c: the host harness for the bare-metal saved-state writer.
 *
 * The shipping firmware translation unit (sw/firmware/milan_baremetal/
 * milan_baremetal.c) is compiled UNCHANGED against the stub headers beside
 * this file, so every address it forms lands in a host array: the Milan CSR
 * window is a word array whose stores are settled on the next access, the
 * QSPI mapping is a flash array the LiteSPI command-master stubs erase and
 * program, and the reserved processor window is a byte array. Time is a
 * counter the firmware's own busy-wait advances. The model behind the
 * control face follows KL_nvm_backend's section 9.2 next-state function
 * closely enough to grade the writer's protocol: the heartbeat re-arms
 * T-NVM-WRITER-ALIVE, a start opens the commit bracket, an acknowledgement
 * clears nvm_dirty, and either deadline lapsing after the writer was once
 * live is a loss.
 *
 * Driven by test_nvm_firmware.py, which builds this per shipped shape with
 * the SAME constants milan_soc.py publishes and grades the containers the
 * firmware writes against scripts/nvm_klj2.py byte for byte.
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "stubs/nvm_host.h"
#include "stubs/command.h"
#include "stubs/init.h"
#ifdef NVM_HOST_PHY
/* The PHY build (test_phy_firmware.py): the pin-level Clause-22 peer answers
 * the firmware's MDIO pins and counts every link-status publication, so a
 * boot path can be graded on whether it publishes the link at all (#70). */
#include "phy_peer.h"
#endif

#define NS_PER_CYCLE     10u
#define MS(n)            ((uint64_t)(n) * 1000000ull)
#define CSR_WORDS        0x400u
#define A_ID             0x000u
#define A_VERSION        0x004u
#define A_TOD_RD_LO      0x530u
#define A_TOD_RD_HI      0x534u
#define A_PP_CTRL        0x920u
#define A_PP_STAT        0x924u
#define A_PP_NVM_SEL     0x934u
#define A_PP_NVM_DATA    0x938u
#define A_PP_NVM_STAT    0x93cu
#define ID_MAGIC         0x4d494c4eu
#define T_ALIVE_MS       2000u
#define T_COMMIT_MS      8000u
#define WALK_ARM_NS      MS(5)
#define WALK_LEN_NS      MS(10)
#define SPI_BYTE_NS      640u
#define PAGE_PROGRAM_NS  MS(1)
#define CMD_WREN         0x06u
#define CMD_RDSR         0x05u
#define CMD_SE           0xd8u
#define CMD_PP           0x02u

uint8_t nvm_host_flash[NVM_HOST_FLASH_BYTES];
uint8_t nvm_host_ddr[NVM_HOST_DDR_BYTES];

extern init_func const nvm_host_init_milan_init;
extern cmd_handler const nvm_host_cmd_milan_nvm;
extern cmd_handler const nvm_host_cmd_milan_status;
extern cmd_handler const nvm_host_cmd_milan_gettime;
extern cmd_handler const nvm_host_cmd_milan_settime;
extern cmd_handler const nvm_host_cmd_milan_utc;

void set_idle_hook(void (*fptr)(void));
void command_dispatch_hook(void);
void bios_dispatch_hook_required(void);
/* The writer's CPU-only reset, which writer_restart.py appends to the host
 * build: every writer static back to its initial value, then nvm_boot()
 * again, with the fabric, the backend and the media kept. */
void nvm_host_writer_restart(void);

/* The host replaces the BIOS, including its patch-0006 link marker. */
void bios_dispatch_hook_required(void)
{
}
unsigned int crc32(const unsigned char *buffer, unsigned int len);

struct backend {
	uint32_t words[5];
	uint32_t map[2][16];
	unsigned int sel;
	int img_valid;
	unsigned int verdict;
	int backed;
	int dirty;             /* DERIVED: dirty_live OR dirty_cap */
	int stale;
	int ever_backed;
	int commit_busy;
	uint64_t alive_deadline;
	uint64_t commit_deadline;
	unsigned int hb_count;
	unsigned int ack_count;
	unsigned int start_count;
	uint64_t last_hb_ns;
	uint64_t max_hb_gap_ns;
	int base_ok;
	unsigned int losses;   /* deadline expiries after the writer was live */
	/* The snapshot-ownership contract of
	 * docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md, as far as a model
	 * with NO DEVICE-FACE PRODUCER can carry it: the window load and the
	 * capture handshake. There is no producer here, so only explicit test stimuli
	 * re-open records after an accepted RELOAD; no grant ever voids a capture
	 * and the hold never has anything to defer; what this model grades is
	 * the WRITER's sequence, and tb/verilator/nvm_cosim grades the rules
	 * this model cannot reach against the real RTL and the real donor. */
	int ld_ok;             /* a re-base armed the load flag */
	int ld_pend;           /* a boot window load may still be accepted */
	int ld_acc;            /* one HAS been accepted since reset (rule 9) */
	int rl_ref;            /* the last RELOAD strobe was refused */
	int cap_open;
	int cap_valid;
	int cap_att;
	int ack_ref;
	int arm_ref;
	unsigned int cap_id;
	int dirty_live;
	int dirty_cap;
	int unres;             /* at least one record is open */
	uint32_t ownership[8]; /* independently driven partial ownership vector */
	unsigned int arm_count;
	unsigned int reload_count;
	/* modelled disturbance: the next N window loads are refused, as a
	 * mutating grant after the re-base would refuse them in the fabric */
	unsigned int refuse_loads;
};

struct walk {
	int armed;
	int pending;
	uint64_t at;
	int busy;
	int done;
	int fail;
	int blank;
	int blind;
	/* the D3 walk's CLOSED terminal (processor pin d352bbaa): fail and never
	 * done, published at PP_STAT[16]; --walk-closed selects it */
	int closed;
	int end_closed;
	/* a walk that never reaches a terminal: busy for ever, neither done
	 * nor CLOSED, so the firmware's bounded wait runs out; --walk-stall */
	int stall;
	/* every PP_CTRL[1] rising edge, and whether PP_CTRL[0] (the entity
	 * enable) was ever raised while no walk had yet started */
	unsigned int starts;
	int enable_first;
};

struct flash_model {
	int cs;
	uint8_t buf[300];
	unsigned int len;
	uint8_t resp;
	int rx_pending;   /* a response byte waits in the master's RX FIFO */
	int wel;
	uint64_t busy_until;
	int busy_forever;
	unsigned int erases;
	unsigned int programs;
	unsigned int pagewrap;
	int fail_erase;
	int fail_program;
	int fail_verify;
	uint64_t erase_ns;
};

/* A planted read fault (#671). The firmware reads a slot through the
 * memory-mapped window, a pointer load that always returns bytes, so a media
 * fault can only return wrong bytes. Every read the firmware opens through
 * the mapping (one evaluation of SPIFLASH_BASE) is counted from the read the
 * fault is armed at, power-on for a fault given before --boot, so one given
 * after it can aim at a writer restart's reads: the first SKIP are clean,
 * the next COUNT are answered from a view whose bytes of one slot are wrong,
 * and the rest are clean again. A fault either
 * XORs one byte of the slot with a different value on every faulty read
 * (BASE, BASE + 1, ... over 1 to 255, so no two faulty reads agree), does so
 * and then rewrites the CRC-32 trailer the slot's length word places over the
 * faulty bytes, so every faulty read is a different container whose CRC
 * closes (R603-4-F1), reads every byte of the slot as 0xFF, the same on every
 * faulty read, or reads the slot as the other slot's bytes. That last one is
 * an address fault: a valid container does not name its slot, so no rule over
 * the bytes sees it on a judgement read, and the re-stage refuses it only by
 * the sequence it was picked by. An XORed byte below zero counts back from
 * the end of the container the slot's length word names: -1 is the trailer's
 * last byte, -5 the last byte before it.
 *
 * Two more faults change one term of the writer's comparison of two refused
 * reads and keep the others (#671 round 6), by forging the last four bytes
 * before the trailer so the CRC-32 over every byte before it is a value the
 * fault fixes. RF_LEN grows the length word by four on every faulty read,
 * moves the slot's trailer value to the end that length names and forges the
 * CRC to that value's complement, so each read has another byte count and is
 * refused VD_CRC. RF_VERDICT XORs the entity, model or record layout word in
 * turn and forges the CRC to the slot's own trailer value, which closes it, so
 * any three faulty reads in a row are refused VD_ENT, VD_SHAPE and VD_REC. */
enum read_fault_mode { RF_XOR, RF_SEAL, RF_FF, RF_OTHER, RF_LEN, RF_VERDICT };

struct read_fault {
	int armed;
	uint32_t slot;          /* the slot's flash offset */
	uint32_t other;         /* the other slot's, in RF_OTHER mode */
	long off;               /* the byte inside it, in RF_XOR and RF_SEAL modes */
	enum read_fault_mode mode;
	unsigned int skip;
	unsigned int count;
	unsigned int base;
	unsigned int hits;      /* reads answered from the faulty view */
};
/* A firmware that never stops reading is ended here, with its summary: after
 * READ_STORM reads, or after BOOT_READ_STORM in one boot or restart, far past
 * any bound the writer states, so a planted unbounded loop costs no more than
 * a bounded one (#671). */
#define READ_STORM 1000000u
#define BOOT_READ_STORM 1000u

static uint64_t now_ns;
/* PP_NVM_STAT[31:24], the backend's saved-state contract tag. --boot-backend
 * contract reads an older one; with over (the boot load ended and none was
 * accepted) and live (the restore walk already sequenced) it selects the
 * retire paths a cold boot of this model never takes. */
static uint32_t stat_tag = 0xc3u;
static struct read_fault rf;
static uint8_t flash_view[NVM_HOST_FLASH_BYTES];
static int view_loaded;
static unsigned int reads;
static unsigned int boot_reads;
static unsigned int restart_reads;
/* while a boot or a restart runs: the read it began at, and its count */
static unsigned int boot_from;
static unsigned int *booting;
static uint32_t csr[CSR_WORDS];
static uint32_t shadow[CSR_WORDS];
static uint32_t pp_ctrl;
static struct backend be;
static struct walk walk;
static struct flash_model fl;
static void (*idle_hook)(void);

void set_idle_hook(void (*fptr)(void))
{
	idle_hook = fptr;
}

unsigned int crc32(const unsigned char *buffer, unsigned int len)
{
	unsigned int crc = 0xffffffffu;
	unsigned int i;
	unsigned int bit;

	for (i = 0; i < len; ++i) {
		crc ^= buffer[i];
		for (bit = 0; bit < 8; ++bit)
			crc = (crc >> 1) ^ (0xedb88320u & (0u - (crc & 1u)));
	}
	return ~crc;
}

/* ---- the control face: section 9.2 and the capture handshake ---------- */
static void rebase(void);

static void end_capture(int acked)
{
	if (!acked)
		be.dirty_live |= be.dirty_cap;
	be.dirty_cap = 0;
	be.cap_open = 0;
	be.cap_valid = 0;
	be.cap_att = 0;
	be.commit_busy = 0;
}

static void strobes(uint32_t v)
{
	if (v & 1u) {
		if (be.ever_backed && now_ns - be.last_hb_ns > be.max_hb_gap_ns)
			be.max_hb_gap_ns = now_ns - be.last_hb_ns;
		be.last_hb_ns = now_ns;
		be.backed = 1;
		be.ever_backed = 1;
		be.alive_deadline = now_ns + MS(T_ALIVE_MS);
		be.hb_count++;
	}
	if (v & 0x40u) {       /* RELOAD, checked by the backend (5.3) */
		int ok;

		if (be.refuse_loads) {
			be.refuse_loads--;
			be.ld_ok = 0;  /* something else wrote the window */
		}
		ok = be.ld_ok && be.ld_pend;

		be.rl_ref = !ok;
		be.reload_count++;
		if (ok) {
			be.ld_pend = 0;
			be.ld_acc = 1;
			be.unres = 0;          /* every record closed */
			memset(be.ownership, 0, sizeof(be.ownership));
			be.dirty_live = 0;
			end_capture(1);
		}
	}
	if (v & 8u) {          /* ARM */
		int ok = be.words[1] != 0u && be.img_valid && !be.cap_open &&
			 be.ld_acc;

		be.arm_ref = !ok;
		if (ok) {
			be.cap_id++;
			be.arm_count++;
			be.dirty_cap = be.dirty_live;
			be.dirty_live = 0;
			be.cap_open = 1;
			be.cap_valid = 1;
			be.cap_att = 0;
			be.ack_ref = 0;
		}
	}
	if (v & 0x10u) {       /* ATTEST */
		if (be.cap_open && !be.cap_att && be.cap_valid)
			be.cap_att = 1;
	}
	if (v & 2u) {          /* ACK, quoting the capture identity */
		unsigned int id = v >> 16;
		int ok = be.cap_open && be.cap_att && be.cap_valid &&
			 id == be.cap_id;

		be.ack_ref = !ok;
		if (be.cap_open && id == be.cap_id)
			end_capture(ok);
		if (ok)
			be.ack_count++;
	}
	if (v & 0x20u) {       /* RELEASE */
		if (be.cap_open)
			end_capture(0);
	}
	if (v & 4u) {
		be.commit_busy = 1;
		be.commit_deadline = now_ns + MS(T_COMMIT_MS);
		be.start_count++;
	}
}

static void on_store(unsigned int offset, uint32_t v)
{
	switch (offset) {
	case A_PP_NVM_SEL:
		be.sel = v & 0x3fu;
		/* A RE-BASE begins when the writer addresses word 0, the image
		 * base. The fabric arms its load flag on the WRITE of word 0,
		 * word 1 or a channel-map table; this model settles stores by
		 * DIFFING the register file, so a repeated load that rewrites
		 * the same base and length is invisible to it as a write and
		 * visible only as this word index. The two agree for the
		 * writer's sequence, which always addresses word 0 first
		 * (nvm_rebase_backend); the fabric's own priority rules are
		 * graded against the RTL in tb/verilator/nvm_cosim. */
		if (be.sel == 0u)
			rebase();
		break;
	case A_PP_NVM_DATA:
		if (be.sel & 0x20u) {
			be.map[(be.sel >> 4) & 1u][be.sel & 0xfu] = v;
		} else if (be.sel == 4u) {
			strobes(v);
		} else if (be.sel == 3u) {
			be.verdict = v & 0xfu;
			be.img_valid = (v >> 4) & 1u;
			/* snapshot-ownership section 12: a REPORTED erase,
			 * program or read-back-verify failure revokes
			 * nvm_backed when it is reported, not eight seconds
			 * later when the commit deadline lapses */
			if (be.verdict >= 11u && be.verdict <= 13u) {
				be.backed = 0;
				be.alive_deadline = 0;
				if (be.ever_backed) {
					be.stale = 1;
					be.losses++;
				}
			}
		} else if (be.sel < 5u) {
			be.words[be.sel] = v;
			if (be.sel < 2u)
				be.img_valid = 0;
		}
		break;
	case A_PP_NVM_STAT:
		strobes(v);
		break;
	case A_PP_CTRL:
		if ((v & 1u) && !(pp_ctrl & 1u) && walk.starts == 0u)
			walk.enable_first = 1;
		if ((v & 2u) && !walk.armed) {
			walk.pending = 1;
			walk.at = now_ns + WALK_ARM_NS;
			walk.blind = !be.img_valid;
			walk.done = 0;
			walk.starts++;
		}
		walk.armed = (v & 2u) != 0;
		pp_ctrl = v;
		break;
	default:
		break;
	}
}

/* A RE-BASE: the image moved or changed shape. Every record reads open
 * again, the load flag arms (nothing is ever in flight in this model, which
 * has no device-face producer) and any capture ends. */
static void rebase(void)
{
	be.unres = 1;
	memset(be.ownership, 0xff, sizeof(be.ownership));
	be.ld_ok = 1;
	if (be.cap_open)
		end_capture(0);
}

static uintptr_t image_base_seen(void)
{
	return (uintptr_t)nvm_host_ddr + NVM_HOST_IMAGE_OFF + 40u;
}

/* Whether the walk would validate zero records: every record byte erased.
 * The configured length includes the section 6.1 alignment pad, which is
 * zero and belongs to no record, so the last three bytes may be either. */
static int area_all_erased(void)
{
	const uint8_t *area = nvm_host_ddr + NVM_HOST_IMAGE_OFF + 40u;
	uint32_t i;

	for (i = 0; i < be.words[1] && i + 40u < 0x10000u; ++i) {
		int pad = i + 3u >= be.words[1] && area[i] == 0x00u;

		if (area[i] != 0xffu && !pad)
			return 0;
	}
	return 1;
}

static void advance(void)
{
	if (be.ever_backed && be.alive_deadline && now_ns >= be.alive_deadline) {
		be.backed = 0;
		be.stale = 1;
		be.alive_deadline = 0;
		be.losses++;
	}
	if (be.commit_busy && now_ns >= be.commit_deadline) {
		be.commit_busy = 0;
		if (be.ever_backed) {
			be.backed = 0;
			be.stale = 1;
			be.losses++;
		}
	}
	be.dirty = be.dirty_live || be.dirty_cap;
	if (be.backed && !be.dirty)
		be.stale = 0;
	if (walk.pending && now_ns >= walk.at) {
		walk.busy = 1;
		if (!walk.stall && now_ns >= walk.at + WALK_LEN_NS) {
			walk.pending = 0;
			walk.busy = 0;
			walk.closed = walk.end_closed;
			walk.done = !walk.closed;
			walk.fail = walk.blind || walk.closed;
			walk.blank = !walk.closed && area_all_erased();
			be.base_ok = be.words[0] == (uint32_t)image_base_seen();
		}
	}
}

static uint32_t data_readback(void)
{
	if (be.sel & 0x20u)
		return be.map[(be.sel >> 4) & 1u][be.sel & 0xfu];
	if (be.sel == 4u)
		return 0;
	if (be.sel == 3u)
		return ((uint32_t)be.img_valid << 4) | be.verdict;
	if (be.sel == 5u)
		return be.cap_id;
	/* Test stimuli may leave one record open beside closed neighbours.
	 * Device-side races remain the real-backend cosimulation's scope. */
	if (be.sel >= 8u && be.sel < 16u)
		return be.ownership[be.sel - 8u];
	if (be.sel < 5u)
		return be.words[be.sel];
	return 0;
}

static void recompose(void)
{
	csr[A_ID / 4] = ID_MAGIC;
	csr[A_VERSION / 4] = 0x00020057u;
	csr[A_TOD_RD_LO / 4] = (uint32_t)now_ns;
	csr[A_TOD_RD_HI / 4] = (uint32_t)(now_ns >> 32);
	csr[A_PP_CTRL / 4] = pp_ctrl;
	csr[A_PP_STAT / 4] = 0x5b000000u | ((uint32_t)walk.busy << 1) |
			     ((uint32_t)walk.done << 2) | ((uint32_t)walk.fail << 3) |
			     ((uint32_t)be.backed << 6) | ((uint32_t)walk.blank << 7) |
			     ((uint32_t)be.dirty << 8) | ((uint32_t)be.stale << 9) |
			     ((uint32_t)be.img_valid << 10) |
			     ((uint32_t)be.unres << 11) | (be.verdict << 12) |
			     ((uint32_t)walk.closed << 16);
	csr[A_PP_NVM_SEL / 4] = be.sel;
	csr[A_PP_NVM_DATA / 4] = data_readback();
	csr[A_PP_NVM_STAT / 4] = (stat_tag << 24) |
				 ((uint32_t)be.unres << 23) |
				 ((uint32_t)be.unres << 22) |
				 ((uint32_t)be.arm_ref << 21) |
				 ((uint32_t)be.ack_ref << 20) |
				 ((uint32_t)be.cap_att << 19) |
				 ((uint32_t)be.cap_valid << 18) |
				 ((uint32_t)be.cap_open << 16) |
				 (be.verdict << 12) | ((uint32_t)be.rl_ref << 11) |
				 ((uint32_t)be.commit_busy << 10) |
				 ((uint32_t)be.stale << 9) | ((uint32_t)be.dirty << 8) |
				 ((uint32_t)be.img_valid << 7) | ((uint32_t)be.backed << 6) |
				 ((uint32_t)(be.words[1] != 0) << 5) |
				 ((uint32_t)be.ld_pend << 3) |
				 ((uint32_t)be.ld_acc << 2);
	memcpy(shadow, csr, sizeof(csr));
}

/* Every CSR access and tick settles, so the common case, no store since the
 * last, is one memcmp and not a word-by-word walk; the walk is unchanged. */
static void settle(void)
{
	unsigned int i;

	if (memcmp(csr, shadow, sizeof(csr)) != 0)
		for (i = 0; i < CSR_WORDS; ++i)
			if (csr[i] != shadow[i])
				on_store(i * 4u, csr[i]);
	advance();
	recompose();
}

uintptr_t nvm_host_csr_base(void)
{
	settle();
	return (uintptr_t)csr;
}

void nvm_host_tick(int cycles)
{
	now_ns += (uint64_t)(cycles > 0 ? cycles : 0) * NS_PER_CYCLE + 1000u;
	settle();
}

static void summary(void);

static uint32_t get32(const uint8_t *p)
{
	return p[0] | (uint32_t)p[1] << 8 | (uint32_t)p[2] << 16 |
	       (uint32_t)p[3] << 24;
}

static void put32(uint8_t *p, uint32_t v)
{
	unsigned int i;

	for (i = 0; i < 4u; ++i)
		p[i] = (uint8_t)(v >> (8u * i));
}

/* RF_SEAL: the slot's trailer, where its length word places it, recomputed
 * over the bytes before it. A length no container can have is left alone. */
static void seal_slot(uint8_t *s)
{
	uint32_t len = get32(s + 16);

	if (len < 44u || len > 0x10000u)
		return;
	put32(s + len - 4u, crc32(s, len - 4u));
}

/* The four bytes at `at` set so the CRC-32 over the slot's first at + 4
 * bytes is `want`. Four message bytes are XORed into the register ahead of
 * 32 shifts, and each shift can be undone, so the register `want` needs is
 * run back 32 shifts and XORed with the register before the four bytes. */
static void forge_crc(uint8_t *s, uint32_t at, uint32_t want)
{
	uint32_t r = ~want;
	unsigned int bit;

	for (bit = 0; bit < 32u; ++bit)
		r = (r & 0x80000000u) ? ((r ^ 0xedb88320u) << 1) | 1u : r << 1;
	put32(s + at, r ^ ~crc32(s, at));
}

/* The words RF_VERDICT XORs, in the order the rule tests them after the CRC:
 * the entity (VD_ENT), the model (VD_SHAPE) and the record layout (VD_REC). */
static const uint32_t verdict_words[3] = {
	20u, 28u, 36u
};

/* The n-th faulty read's view of the slot at `s`, which holds its clean
 * bytes. A fault placed by the container's end needs a slot that names a
 * length; one that does not is a harness error, not a fault. */
static void fault_slot(uint8_t *s, unsigned int n)
{
	uint8_t x = (uint8_t)((rf.base - 1u + n) % 255u + 1u);
	uint32_t len = get32(s + 16);
	uint32_t grown = len + 4u * (n + 1u);

	if ((rf.mode == RF_LEN || rf.mode == RF_VERDICT || rf.off < 0) &&
	    (len < 48u || len > 0x10000u || (uint32_t)-rf.off > len ||
	     (rf.mode == RF_LEN && grown > 0x10000u))) {
		fprintf(stderr, "HOST: read fault %d on a slot of length %#x\n",
			(int)rf.mode, (unsigned int)len);
		exit(2);
	}
	switch (rf.mode) {
	case RF_FF:
		memset(s, 0xff, 0x10000u);
		break;
	case RF_OTHER:
		memcpy(s, nvm_host_flash + rf.other, 0x10000u);
		break;
	case RF_LEN:
		put32(s + grown - 4u, get32(s + len - 4u));
		put32(s + 16, grown);
		forge_crc(s, grown - 8u, ~get32(s + grown - 4u));
		break;
	case RF_VERDICT:
		s[verdict_words[n % 3u]] ^= x;
		forge_crc(s, len - 8u, get32(s + len - 4u));
		break;
	default:
		s[rf.off < 0 ? len - (uint32_t)-rf.off : (uint32_t)rf.off] ^= x;
		if (rf.mode == RF_SEAL)
			seal_slot(s);
	}
}

uintptr_t nvm_host_flash_base(void)
{
	unsigned int k = reads++;
	int boot_storm = booting && reads - boot_from > BOOT_READ_STORM;

	if (boot_storm)
		*booting = reads - boot_from;
	if (reads > READ_STORM || boot_storm) {
		printf("HOST read storm: %u reads through the mapping\n", reads);
		summary();
		exit(0);
	}
	if (!rf.armed || k < rf.skip || k - rf.skip >= rf.count)
		return (uintptr_t)nvm_host_flash;
	/* only the journal is ever programmed or erased */
	if (!view_loaded)
		memcpy(flash_view, nvm_host_flash, sizeof(flash_view));
	else
		memcpy(flash_view + NVM_HOST_JOURNAL_OFFSET,
		       nvm_host_flash + NVM_HOST_JOURNAL_OFFSET, 0x20000u);
	view_loaded = 1;
	fault_slot(flash_view + rf.slot, k - rf.skip);
	rf.hits++;
	return (uintptr_t)flash_view;
}

/* --read-fault and --read-sealed SLOT:OFF:SKIP:COUNT[:BASE], --read-ff,
 * --read-other, --read-length and --read-verdict SLOT:SKIP:COUNT */
static void arm_read_fault(const char *spec, enum read_fault_mode mode)
{
	long v[4] = {0};
	unsigned int n = 0;
	const char *p = spec + 1;
	char *end = NULL;
	int bytewise = mode == RF_XOR || mode == RF_SEAL;
	unsigned int at = bytewise ? 1u : 0u;    /* where SKIP is */

	v[3] = 8;    /* the first faulty read's XOR, unless BASE is given */
	if ((spec[0] != 'a' && spec[0] != 'b') || spec[1] != ':') {
		fprintf(stderr, "HOST: a read fault names slot a or b\n");
		exit(2);
	}
	while (*p == ':' && n < 4u) {
		v[n++] = strtol(p + 1, &end, 0);
		p = end;
	}
	if (*p != '\0' || n < at + 2u || v[at] < 0 || v[at + 1u] < 0 ||
	    (bytewise && (v[0] <= -0x10000 || v[0] >= 0x10000 || v[3] < 1 || v[3] > 255))) {
		fprintf(stderr, "HOST: bad read fault %s\n", spec);
		exit(2);
	}
	rf.armed = 1;
	rf.slot = NVM_HOST_JOURNAL_OFFSET + (spec[0] == 'b' ? 0x10000u : 0u);
	rf.other = NVM_HOST_JOURNAL_OFFSET + (spec[0] == 'b' ? 0u : 0x10000u);
	rf.mode = mode;
	rf.off = bytewise ? v[0] : 0;
	rf.skip = (unsigned int)v[at];
	rf.count = (unsigned int)v[at + 1u];
	rf.base = bytewise ? (unsigned int)v[3] : 8u;
}

/* A fault counts its SKIP from the read it is armed at. */
static void arm_from_here(const char *spec, enum read_fault_mode mode)
{
	arm_read_fault(spec, mode);
	rf.skip += reads;
}

/* ---- the LiteSPI command master and the N25Q behind it ----------------- */
/* TX always ready; RX ready exactly while an unread response byte waits,
 * which is what lets the firmware's FIFO drain loop terminate. */
uint32_t nvm_host_spi_status(void)
{
	return 1u | ((uint32_t)fl.rx_pending << 1);
}

void nvm_host_spi_phyconfig(uint32_t v)
{
	(void)v;
}

static void flash_execute(void)
{
	uint32_t addr;
	unsigned int i;

	if (fl.len == 0)
		return;
	addr = ((uint32_t)fl.buf[1] << 16) | ((uint32_t)fl.buf[2] << 8) | fl.buf[3];
	switch (fl.buf[0]) {
	case CMD_WREN:
		fl.wel = 1;
		break;
	case CMD_SE:
		if (!fl.wel || fl.len < 4)
			break;
		addr &= ~0xffffu;
		memset(nvm_host_flash + addr, 0xff, 0x10000u);
		if (fl.fail_erase)
			nvm_host_flash[addr + 5u] = 0x00;
		fl.busy_until = now_ns + fl.erase_ns;
		fl.erases++;
		fl.wel = 0;
		break;
	case CMD_PP:
		if (!fl.wel || fl.len < 4)
			break;
		if ((addr & 0xffu) + (fl.len - 4u) > 256u)
			fl.pagewrap++;
		for (i = 4; i < fl.len; ++i)
			nvm_host_flash[addr + i - 4u] &= fl.buf[i];
		if (fl.fail_verify && fl.programs == 0)
			nvm_host_flash[addr + 3u] ^= 0x01u;
		if (fl.fail_program)
			fl.busy_forever = 1;
		else
			fl.busy_until = now_ns + PAGE_PROGRAM_NS;
		fl.programs++;
		fl.wel = 0;
		break;
	default:
		break;
	}
}

void nvm_host_spi_cs(uint32_t v)
{
	if (fl.cs && !v)
		flash_execute();
	fl.cs = v != 0;
	fl.len = 0;
}

void nvm_host_spi_rxtx_write(uint32_t v)
{
	now_ns += SPI_BYTE_NS;
	if (fl.cs && fl.len < sizeof(fl.buf))
		fl.buf[fl.len++] = (uint8_t)v;
	if (fl.len && fl.buf[0] == CMD_RDSR)
		fl.resp = (fl.busy_forever || now_ns < fl.busy_until) ? 0x01u : 0x00u;
	else
		fl.resp = 0xffu;
	fl.rx_pending = 1;
}

uint32_t nvm_host_spi_rxtx_read(void)
{
	fl.rx_pending = 0;
	return fl.resp;
}

/* ---- the scenario driver ------------------------------------------------ */
static void load_file(const char *path, uint8_t *dst, size_t room)
{
	FILE *f = fopen(path, "rb");
	size_t n;

	if (!f) {
		fprintf(stderr, "HOST: cannot read %s\n", path);
		exit(2);
	}
	memset(dst, 0xff, room);
	n = fread(dst, 1, room, f);
	fclose(f);
	printf("HOST loaded %zu B from %s\n", n, path);
}

static void dump_file(const char *path, const uint8_t *src, size_t n)
{
	FILE *f = fopen(path, "wb");

	if (!f) {
		fprintf(stderr, "HOST: cannot write %s\n", path);
		exit(2);
	}
	fwrite(src, 1, n, f);
	fclose(f);
}

static int hex_nibble(char c)
{
	if (c >= '0' && c <= '9')
		return c - '0';
	if (c >= 'a' && c <= 'f')
		return c - 'a' + 10;
	if (c >= 'A' && c <= 'F')
		return c - 'A' + 10;
	return -1;
}

/* --change OFFSET:HEX writes the framed record the driver built into the
 * staged image, as the processor's WRITE through the backend would, and
 * reports the change to the liveness machine. */
static void apply_change(const char *spec)
{
	char *end = NULL;
	unsigned long off = strtoul(spec, &end, 0);
	const char *hex = (end && *end == ':') ? end + 1 : NULL;
	size_t i = 0;

	if (!hex) {
		fprintf(stderr, "HOST: --change wants OFFSET:HEX\n");
		exit(2);
	}
	while (hex[0] && hex[1]) {
		int hi = hex_nibble(hex[0]);
		int lo = hex_nibble(hex[1]);

		if (hi < 0 || lo < 0 || off + i >= 0x10000u) {
			fprintf(stderr, "HOST: bad --change payload\n");
			exit(2);
		}
		nvm_host_ddr[NVM_HOST_IMAGE_OFF + off + i] = (uint8_t)((hi << 4) | lo);
		hex += 2;
		i++;
	}
	be.dirty_live = 1;
	printf("HOST change %zu B at image offset %lu\n", i, off);
}

static void run_idle(unsigned long ms)
{
	uint64_t until = now_ns + MS(ms);

	while (now_ns < until) {
		uint64_t before = now_ns;

		if (idle_hook)
			idle_hook();
		if (now_ns == before)
			now_ns += 100000u;
		now_ns += 100000u;
		settle();
	}
}

static void run_uart(char *line)
{
	char *params[8];
	int nb = 0;
	char *cmd = strtok(line, " ");
	char *tok;

	command_dispatch_hook();
	while ((tok = strtok(NULL, " ")) != NULL && nb < 8)
		params[nb++] = tok;
	if (cmd && strcmp(cmd, "milan_nvm") == 0)
		nvm_host_cmd_milan_nvm(nb, params);
	else if (cmd && strcmp(cmd, "milan_status") == 0)
		nvm_host_cmd_milan_status(nb, params);
	else if (cmd && strcmp(cmd, "milan_gettime") == 0)
		nvm_host_cmd_milan_gettime(nb, params);
	else if (cmd && strcmp(cmd, "milan_settime") == 0)
		nvm_host_cmd_milan_settime(nb, params);
	else if (cmd && strcmp(cmd, "milan_utc") == 0)
		nvm_host_cmd_milan_utc(nb, params);
	else
		printf("HOST: unknown console command\n");
	settle();
}

#ifdef NVM_HOST_PHY
static void phy_summary(const char *at)
{
	printf("HOST phy at=%s transfers=%u publishes=%u status=%u now_ms=%llu\n", at,
	       transfers, publishes, status_word, (unsigned long long)(now_ns / 1000000ull));
}
#endif

static void summary(void)
{
	printf("HOST hb=%u acks=%u starts=%u erases=%u programs=%u max_hb_gap_ms=%llu pagewrap=%u "
	       "backed=%d dirty=%d stale=%d valid=%d verdict=%u blank=%d fail=%d done=%d "
	       "seq=%u base_ok=%d img_len=%u losses=%u arms=%u reloads=%u "
	       "ld_acc=%d ld_pend=%d rl_ref=%d unres=%d ack_ref=%d arm_ref=%d "
	       "cap_id=%u walks=%u enable_first=%d closed=%d reads=%u boot_reads=%u "
	       "restart_reads=%u faulty_reads=%u now_ms=%llu\n",
	       be.hb_count, be.ack_count, be.start_count, fl.erases, fl.programs,
	       (unsigned long long)(be.max_hb_gap_ns / 1000000ull), fl.pagewrap,
	       be.backed, be.dirty, be.stale, be.img_valid, be.verdict, walk.blank,
	       walk.fail, walk.done, be.words[2], be.base_ok, be.words[1], be.losses,
	       be.arm_count, be.reload_count, be.ld_acc, be.ld_pend, be.rl_ref,
	       be.unres, be.ack_ref, be.arm_ref, be.cap_id,
	       walk.starts, walk.enable_first, walk.closed, reads, boot_reads,
	       restart_reads, rf.hits, (unsigned long long)(now_ns / 1000000ull));
#ifdef NVM_HOST_PHY
	phy_summary("end");
#endif
}

static void boot(void)
{
	/* the AEM slot: the four magic bytes the firmware's verifier looks for */
	memcpy(nvm_host_flash + NVM_HOST_AEM_OFFSET, "AEMI", 4);
	recompose();
	boot_from = reads;
	booting = &boot_reads;
	nvm_host_init_milan_init();
	settle();
	booting = NULL;
	boot_reads = reads;
	printf("HOST booted\n");
#ifdef NVM_HOST_PHY
	phy_summary("boot");
#endif
}

int main(int argc, char **argv)
{
	int i;
	int booted = 0;

	memset(nvm_host_flash, 0xff, sizeof(nvm_host_flash));
	memset(nvm_host_ddr, 0xa5, sizeof(nvm_host_ddr));
	fl.erase_ns = MS(20);
	/* the reset row of snapshot-ownership section 5.4: every allocated
	 * record open, a boot window load still acceptable and none accepted */
	be.unres = 1;
	memset(be.ownership, 0xff, sizeof(be.ownership));
	be.ld_pend = 1;
	/* not word 0, so the writer's first re-base is a CHANGE this model's
	 * diffing settle can see */
	be.sel = 0x3fu;
#ifdef NVM_HOST_PHY
	/* 1000BASE-T full duplex, negotiated, at the peer's address */
	registers[0] = 0x1000;
	registers[1] = 0x0124;
	registers[2] = 0x001c;
	registers[4] = 0x01e1;
	registers[5] = 0x01e1;
	registers[9] = 0x0300;
	registers[10] = 0x0c00;
	registers[15] = 0x3000;
#endif
	for (i = 1; i < argc; ++i) {
		const char *a = argv[i];
		const char *v = (i + 1 < argc) ? argv[i + 1] : NULL;
		int takes = 1;

		if (strcmp(a, "--slot-a") == 0 && v)
			load_file(v, nvm_host_flash + NVM_HOST_JOURNAL_OFFSET, 0x10000u);
		else if (strcmp(a, "--slot-b") == 0 && v)
			load_file(v, nvm_host_flash + NVM_HOST_JOURNAL_OFFSET + 0x10000u, 0x10000u);
		else if (strcmp(a, "--read-fault") == 0 && v)
			arm_from_here(v, RF_XOR);
		else if (strcmp(a, "--read-sealed") == 0 && v)
			arm_from_here(v, RF_SEAL);
		else if (strcmp(a, "--read-ff") == 0 && v)
			arm_from_here(v, RF_FF);
		else if (strcmp(a, "--read-other") == 0 && v)
			arm_from_here(v, RF_OTHER);
		else if (strcmp(a, "--read-length") == 0 && v)
			arm_from_here(v, RF_LEN);
		else if (strcmp(a, "--read-verdict") == 0 && v)
			arm_from_here(v, RF_VERDICT);
		else if (strcmp(a, "--erase-ms") == 0 && v)
			fl.erase_ns = MS(strtoul(v, NULL, 0));
		else if (strcmp(a, "--walk-closed") == 0) {
			walk.end_closed = 1;
			takes = 0;
		} else if (strcmp(a, "--walk-stall") == 0) {
			walk.stall = 1;
			takes = 0;
		} else if (strcmp(a, "--refuse-loads") == 0 && v)
			be.refuse_loads = (unsigned int)strtoul(v, NULL, 0);
		else if (strcmp(a, "--boot-backend") == 0 && v && !booted) {
			if (strcmp(v, "contract") == 0)
				stat_tag = 0xc2u;
			else if (strcmp(v, "over") == 0)
				be.ld_pend = 0;
			else if (strcmp(v, "live") == 0)
				walk.done = 1;
			else {
				fprintf(stderr, "HOST: bad boot backend %s\n", v);
				return 2;
			}
		} else if (strcmp(a, "--stray-ack") == 0 && v)
			/* an acknowledgement quoting ANOTHER capture: it names
			 * nothing the backend holds and must be refused */
			strobes(2u | ((uint32_t)strtoul(v, NULL, 0) << 16));
		else if (strcmp(a, "--fail") == 0 && v) {
			fl.fail_erase = strcmp(v, "erase") == 0;
			fl.fail_program = strcmp(v, "program") == 0;
			fl.fail_verify = strcmp(v, "verify") == 0;
		} else if (strcmp(a, "--boot") == 0) {
			boot();
			booted = 1;
			takes = 0;
		} else if (!booted) {
			fprintf(stderr, "HOST: %s must follow --boot\n", a);
			return 2;
		} else if (strcmp(a, "--uart") == 0 && v) {
			char line[128];

			strncpy(line, v, sizeof(line) - 1);
			line[sizeof(line) - 1] = '\0';
			run_uart(line);
		} else if (strcmp(a, "--open-record") == 0 && v) {
			unsigned long rid = strtoul(v, NULL, 0);

			if (rid >= 256u || !be.ld_acc || be.cap_open)
				return 2;
			be.ownership[rid / 32u] |= 1u << (rid % 32u);
			be.unres = 1;
		} else if (strcmp(a, "--restart") == 0) {
			/* a CPU-only reset: the state the restart meets, then
			 * the writer's boot again on the fabric it left */
			unsigned int from = reads;

			printf("HOST restarting\n");
			summary();
			boot_from = from;
			booting = &restart_reads;
			nvm_host_writer_restart();
			booting = NULL;
			settle();
			restart_reads = reads - from;
			printf("HOST restarted\n");
			takes = 0;
		} else if (strcmp(a, "--change") == 0 && v)
			apply_change(v);
		else if (strcmp(a, "--dirty") == 0) {
			be.dirty_live = 1;
			takes = 0;
		} else if (strcmp(a, "--idle-ms") == 0 && v)
			run_idle(strtoul(v, NULL, 0));
		else if (strcmp(a, "--dump-ddr") == 0 && v)
			dump_file(v, nvm_host_ddr + NVM_HOST_IMAGE_OFF, 0x10000u);
		else if (strcmp(a, "--dump-stage") == 0 && v)
			dump_file(v, nvm_host_ddr + NVM_HOST_IMAGE_OFF - 0x10000u, 0x10000u);
		else if (strcmp(a, "--dump-slot-a") == 0 && v)
			dump_file(v, nvm_host_flash + NVM_HOST_JOURNAL_OFFSET, 0x10000u);
		else if (strcmp(a, "--dump-slot-b") == 0 && v)
			dump_file(v, nvm_host_flash + NVM_HOST_JOURNAL_OFFSET + 0x10000u, 0x10000u);
		else {
			fprintf(stderr, "HOST: unknown argument %s\n", a);
			return 2;
		}
		i += takes;
	}
	if (!booted)
		boot();
	summary();
	return 0;
}

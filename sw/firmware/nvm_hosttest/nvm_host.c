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

void set_idle_hook(void (*fptr)(void));
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
	 * capture handshake. There is no producer here, so no record ever
	 * re-opens after an accepted RELOAD, no grant ever voids a capture
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

static uint64_t now_ns;
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
		if ((v & 2u) && !walk.armed) {
			walk.pending = 1;
			walk.at = now_ns + WALK_ARM_NS;
			walk.blind = !be.img_valid;
			walk.done = 0;
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
		if (now_ns >= walk.at + WALK_LEN_NS) {
			walk.pending = 0;
			walk.busy = 0;
			walk.done = 1;
			walk.fail = walk.blind;
			walk.blank = area_all_erased();
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
	/* the ownership vector, words 8..15. With no producer here, every
	 * record is open until the boot RELOAD is accepted and closed after
	 * it, so the model answers the whole word from one flag. */
	if (be.sel >= 8u && be.sel < 16u)
		return be.unres ? 0xffffffffu : 0u;
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
			     ((uint32_t)be.unres << 11) | (be.verdict << 12);
	csr[A_PP_NVM_SEL / 4] = be.sel;
	csr[A_PP_NVM_DATA / 4] = data_readback();
	csr[A_PP_NVM_STAT / 4] = 0xc3000000u |
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

static void settle(void)
{
	unsigned int i;

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

	while ((tok = strtok(NULL, " ")) != NULL && nb < 8)
		params[nb++] = tok;
	if (cmd && strcmp(cmd, "milan_nvm") == 0)
		nvm_host_cmd_milan_nvm(nb, params);
	else if (cmd && strcmp(cmd, "milan_status") == 0)
		nvm_host_cmd_milan_status(nb, params);
	else
		printf("HOST: unknown console command\n");
	settle();
}

static void summary(void)
{
	printf("HOST hb=%u acks=%u starts=%u erases=%u programs=%u max_hb_gap_ms=%llu pagewrap=%u "
	       "backed=%d dirty=%d stale=%d valid=%d verdict=%u blank=%d fail=%d done=%d "
	       "seq=%u base_ok=%d img_len=%u losses=%u arms=%u reloads=%u "
	       "ld_acc=%d ld_pend=%d rl_ref=%d unres=%d ack_ref=%d arm_ref=%d "
	       "cap_id=%u now_ms=%llu\n",
	       be.hb_count, be.ack_count, be.start_count, fl.erases, fl.programs,
	       (unsigned long long)(be.max_hb_gap_ns / 1000000ull), fl.pagewrap,
	       be.backed, be.dirty, be.stale, be.img_valid, be.verdict, walk.blank,
	       walk.fail, walk.done, be.words[2], be.base_ok, be.words[1], be.losses,
	       be.arm_count, be.reload_count, be.ld_acc, be.ld_pend, be.rl_ref,
	       be.unres, be.ack_ref, be.arm_ref, be.cap_id,
	       (unsigned long long)(now_ns / 1000000ull));
}

static void boot(void)
{
	/* the AEM slot: the four magic bytes the firmware's verifier looks for */
	memcpy(nvm_host_flash + NVM_HOST_AEM_OFFSET, "AEMI", 4);
	recompose();
	nvm_host_init_milan_init();
	settle();
	printf("HOST booted\n");
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
	be.ld_pend = 1;
	/* not word 0, so the writer's first re-base is a CHANGE this model's
	 * diffing settle can see */
	be.sel = 0x3fu;
	for (i = 1; i < argc; ++i) {
		const char *a = argv[i];
		const char *v = (i + 1 < argc) ? argv[i + 1] : NULL;
		int takes = 1;

		if (strcmp(a, "--slot-a") == 0 && v)
			load_file(v, nvm_host_flash + NVM_HOST_JOURNAL_OFFSET, 0x10000u);
		else if (strcmp(a, "--slot-b") == 0 && v)
			load_file(v, nvm_host_flash + NVM_HOST_JOURNAL_OFFSET + 0x10000u, 0x10000u);
		else if (strcmp(a, "--erase-ms") == 0 && v)
			fl.erase_ns = MS(strtoul(v, NULL, 0));
		else if (strcmp(a, "--refuse-loads") == 0 && v)
			be.refuse_loads = (unsigned int)strtoul(v, NULL, 0);
		else if (strcmp(a, "--stray-ack") == 0 && v)
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
		} else if (strcmp(a, "--change") == 0 && v)
			apply_change(v);
		else if (strcmp(a, "--dirty") == 0) {
			be.dirty_live = 1;
			takes = 0;
		} else if (strcmp(a, "--idle-ms") == 0 && v)
			run_idle(strtoul(v, NULL, 0));
		else if (strcmp(a, "--dump-ddr") == 0 && v)
			dump_file(v, nvm_host_ddr + NVM_HOST_IMAGE_OFF, 0x10000u);
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

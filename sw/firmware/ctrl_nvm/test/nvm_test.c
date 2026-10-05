/* SPDX-License-Identifier: (GPL-2.0 OR MIT) */
/*
 * nvm_test.c - the scenario runner of the saved-state store's host suite
 * (#665 lane F1).
 *
 * The store is compiled as it ships, over either flash port: the host flash
 * model directly, or (--litespi) the on-chip LiteSPI implementation over a
 * model of the command master over the same flash model. The state port is
 * the host state model. Arguments are a script run left to right; every
 * verdict is taken by test_ctrl_nvm.py from the SUMMARY line, the POWERCUT
 * line and the files dumped here, against scripts/nvm_klj2.py and the
 * recorded vectors, never against this file's own idea of the bytes.
 *
 * --powercut is the one loop that runs here rather than in the driver: for
 * every media effect of one commit (the erase and each page program) and
 * four points inside it, the power fails, the board boots again and the
 * restored values must be the old set or the new set exactly; then a change
 * must commit and boot back, so the store recovers from every cut.
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <generated/soc.h>

#include "../host/litespi_model.h"
#include "../host/nvm_fmodel.h"
#include "../host/nvm_smodel.h"
#include "../nvm_store.h"
#include "../plat/nvm_flash_litespi.h"

#define T_LOOP_US       100u      /* the event loop's own time per iteration */
#define T_IDLE_LIMIT_US 60000000u /* the longest a run waits to go idle */
#define T_JOURNAL       (2u * NVM_SLOT_BYTES)
#define T_TIMES         16u       /* failure and commit times kept per run */

struct t_knobs {
	char boot_fault[48];        /* a flash-model fault armed at power on */
	int not_ready;
	int apply_fault;
	unsigned int apply_fault_id;
	int settle_fault;
	int rollback_fault;
	int unbind_fault;
	unsigned int refuse[8];
	unsigned int n_refuse;
};

/* When attempts failed and commits verified, read off the model's clock,
 * which no PHC step moves: the independent clock the time checks grade. */
struct t_times {
	uint64_t at[T_TIMES];
	unsigned int n;
};

struct t_run {
	const struct nvm_flash *port;
	struct t_knobs knobs;
	uint64_t max_call_us;
	unsigned int max_polls_call;
	unsigned int service_calls;
	unsigned int commit_tries;
	unsigned int commit_refused;
	struct t_times fails;
	struct t_times oks;
	unsigned int bad;           /* scenario findings printed as FAIL lines */
};

static struct t_run t;
static uint8_t t_snapshot[T_JOURNAL];
/* The reference commit's container and the slot it went to. */
static uint8_t t_new_image[NVM_IMG_LEN];
static uint32_t t_new_slot;
static uint8_t t_state[3][NVM_ID_SPACE][NVM_PAYLOAD_MAX + 1u];

static void t_fail(const char *what, unsigned int a, unsigned int b)
{
	printf("FAIL %s %u %u\n", what, a, b);
	t.bad++;
}

/* ---- power, boot and the event loop ------------------------------------ */
static void t_power_on(void)
{
	nvm_fmodel_power_on();
	nvm_fmodel_window(NVM_SLOT_A, NVM_SLOT_A + T_JOURNAL);
	litespi_model_reset();
	nvm_flash_litespi_power_on();
	nvm_smodel_reset();
}

static void t_fault_arg(const char *arg);

static void t_boot(void)
{
	unsigned int i;

	t_power_on();
	if (t.knobs.boot_fault[0])
		t_fault_arg(t.knobs.boot_fault);
	nvm_smodel_ready(!t.knobs.not_ready);
	if (t.knobs.apply_fault)
		nvm_smodel_fault_apply(t.knobs.apply_fault_id);
	nvm_smodel_fault_settle(t.knobs.settle_fault);
	if (t.knobs.rollback_fault)
		nvm_smodel_fault_rollback(NVM_W_D3);
	if (t.knobs.unbind_fault)
		nvm_smodel_fault_rollback(NVM_W_BIND);
	for (i = 0; i < t.knobs.n_refuse; ++i)
		nvm_smodel_refuse(t.knobs.refuse[i]);
	nvm_store_boot(t.port, &nvm_smodel_port);
}

static void t_note(struct t_times *tt)
{
	if (tt->n < T_TIMES)
		tt->at[tt->n] = nvm_fmodel_now_us();
	tt->n++;
}

static void t_service(void)
{
	uint64_t before = nvm_fmodel_now_us();
	unsigned int polls = nvm_fmodel_count()->busy_polls;
	unsigned int failed = nvm_store_status()->commits_failed;
	unsigned int ok = nvm_store_status()->commits_ok;

	nvm_store_service();
	if (nvm_store_status()->commits_failed != failed)
		t_note(&t.fails);
	if (nvm_store_status()->commits_ok != ok)
		t_note(&t.oks);
	if (nvm_fmodel_now_us() - before > t.max_call_us)
		t.max_call_us = nvm_fmodel_now_us() - before;
	if (nvm_fmodel_count()->busy_polls - polls > t.max_polls_call)
		t.max_polls_call = nvm_fmodel_count()->busy_polls - polls;
	nvm_fmodel_advance_us(T_LOOP_US);
	t.service_calls++;
}

static void t_run_ms(uint64_t ms)
{
	uint64_t until = nvm_fmodel_now_us() + ms * 1000u;

	while (nvm_fmodel_now_us() < until && !nvm_fmodel_dead())
		t_service();
}

/* Nothing left to do: no writer, a held one, or no change waits and what is
 * in flight is written or has spent its attempts. */
static int t_settled(void)
{
	const struct nvm_status *s = nvm_store_status();

	return s->phase == NVM_P_OFF || s->phase == NVM_P_HELD ||
	       (s->phase == NVM_P_IDLE && !s->dirty && (!s->pending || s->exhausted));
}

static void t_until_idle(void)
{
	uint64_t until = nvm_fmodel_now_us() + T_IDLE_LIMIT_US;

	do
		t_service();
	while (!t_settled() && nvm_fmodel_now_us() < until && !nvm_fmodel_dead());
}

/* Serve until the write path reaches phase p. */
static void t_until_phase(unsigned int p)
{
	uint64_t until = nvm_fmodel_now_us() + T_IDLE_LIMIT_US;

	while ((unsigned int)nvm_store_status()->phase != p && nvm_fmodel_now_us() < until &&
	       !nvm_fmodel_dead())
		t_service();
	if ((unsigned int)nvm_store_status()->phase != p)
		t_fail("phase_not_reached", p, nvm_store_status()->phase);
}

/* ---- changes ------------------------------------------------------------ */
static void t_set(unsigned int id, const uint8_t *value, unsigned int len)
{
	struct nvm_rec r = nvm_rec_by_id(id);

	if (!r.ok) {
		t_fail("set_unknown_record", id, 0);
		return;
	}
	nvm_smodel_set(id, value, len < r.plen ? len : r.plen);
	nvm_store_changed(r.group, r.index);
}

/* Every record (all) or the first of each group, payload byte j of record
 * id = id * 131 + j * 17 + seed: the arithmetic rule of nvm_klj2.py's
 * payload_bytes at seed 0, the rule the recorded vectors are made with. */
static void t_set_pattern(unsigned int seed, int all)
{
	uint8_t payload[NVM_PAYLOAD_MAX];
	struct nvm_rec r = nvm_rec_first();
	unsigned int j;

	while (r.ok) {
		if (all || r.index == 0u) {
			for (j = 0; j < r.plen; ++j)
				payload[j] = (uint8_t)(r.id * 131u + j * 17u + seed);
			t_set(r.id, payload, r.plen);
		}
		r = nvm_rec_next(r);
	}
}

/* ---- the power-cut enumeration ------------------------------------------ */
static void t_capture_state(unsigned int k)
{
	struct nvm_rec r = nvm_rec_first();

	while (r.ok) {
		t_state[k][r.id][0] = (uint8_t)nvm_smodel_valid(r.id);
		memcpy(&t_state[k][r.id][1], nvm_smodel_value(r.id), r.plen);
		r = nvm_rec_next(r);
	}
}

/* 1 when the state model holds state snapshot k exactly. */
static int t_state_is(unsigned int k)
{
	struct nvm_rec r = nvm_rec_first();

	while (r.ok) {
		if (t_state[k][r.id][0] != (uint8_t)nvm_smodel_valid(r.id) ||
		    memcmp(&t_state[k][r.id][1], nvm_smodel_value(r.id), r.plen))
			return 0;
		r = nvm_rec_next(r);
	}
	return 1;
}

static void t_restore_snapshot(void)
{
	memcpy(nvm_fmodel_mem + NVM_SLOT_A, t_snapshot, T_JOURNAL);
}

static void t_protect_auth(void)
{
	int auth = nvm_store_status()->auth;

	nvm_fmodel_protect(auth < 0 ? 0u : (auth ? NVM_SLOT_B : NVM_SLOT_A));
}

/* The reference commit: the old state (0), the new one (1), and how many
 * media effects one commit has. */
static unsigned int t_reference(void)
{
	unsigned int effects;

	t_restore_snapshot();
	t_boot();
	t_capture_state(0);
	t_set_pattern(0x33u, 0);
	t_until_idle();
	effects = nvm_fmodel_count()->effects;
	if (nvm_store_status()->commits_ok != 1u)
		t_fail("powercut_reference_commit", nvm_store_status()->commits_ok, 1);
	t_new_slot = nvm_store_status()->auth ? NVM_SLOT_B : NVM_SLOT_A;
	memcpy(t_new_image, nvm_fmodel_mem + t_new_slot, NVM_IMG_LEN);
	t_boot();
	t_capture_state(1);
	if (t_state_is(0))
		t_fail("powercut_reference_vacuous", 0, 0);
	return effects;
}

/* After a cut: the board boots the old set, or the new set when the new
 * container reached the media whole (strictly the new set once every effect
 * landed), never a mix; then the next change commits. */
static int t_after_cut(int whole, unsigned int *old, unsigned int *new_set)
{
	int complete = memcmp(nvm_fmodel_mem + t_new_slot, t_new_image, NVM_IMG_LEN) == 0;

	t_boot();
	if (t_state_is(1) && complete)
		(*new_set)++;
	else if (t_state_is(0) && !whole)
		(*old)++;
	else
		return 0;
	t_set_pattern(0x77u, 0);
	t_until_idle();
	if (nvm_store_status()->commits_ok != 1u || nvm_store_status()->stale)
		return 0;
	t_capture_state(2);
	t_boot();
	return t_state_is(2) && nvm_store_status()->terminal == NVM_T_COMPLETE;
}

/* One cut: the commit of state 1 with the power failing in effect k. */
static int t_one_cut(unsigned int k, unsigned int frac, unsigned int *old,
		     unsigned int *new_set)
{
	t_restore_snapshot();
	t_boot();
	t_protect_auth();
	if (k)
		nvm_fmodel_cut(k, frac);
	t_set_pattern(0x33u, 0);
	if (k) {
		t_until_idle();
	} else {
		/* every effect landed; the power fails during the read-back */
		while (nvm_store_status()->phase != NVM_P_VERIFY && !t_settled())
			t_service();
	}
	if (nvm_fmodel_count()->protected_hit || nvm_fmodel_count()->outside)
		return 0;
	return t_after_cut(k == 0u, old, new_set);
}

static void t_powercut(void)
{
	static const unsigned int fracs[4] = {
		0u, 1u, 128u, 255u,
	};
	unsigned int effects;
	unsigned int k;
	unsigned int f;
	unsigned int cases = 0;
	unsigned int old = 0;
	unsigned int new_set = 0;
	unsigned int bad = 0;

	memcpy(t_snapshot, nvm_fmodel_mem + NVM_SLOT_A, T_JOURNAL);
	effects = t_reference();
	for (k = 0; k <= effects; ++k) {
		for (f = 0; f < 4u; ++f) {
			if (k == 0u && f > 0u)
				break;
			cases++;
			if (!t_one_cut(k, fracs[f], &old, &new_set)) {
				printf("POWERCUT-BAD effect=%u frac=%u\n", k, fracs[f]);
				bad++;
			}
		}
	}
	printf("POWERCUT effects=%u cases=%u old=%u new=%u bad=%u\n",
	       effects, cases, old, new_set, bad);
	t_restore_snapshot();
}

/* ---- files ----------------------------------------------------------------- */
static void t_load(const char *path, uint32_t slot)
{
	FILE *f = fopen(path, "rb");
	size_t n;

	if (!f) {
		fprintf(stderr, "cannot read %s\n", path);
		exit(2);
	}
	memset(nvm_fmodel_mem + slot, 0xff, NVM_SLOT_BYTES);
	n = fread(nvm_fmodel_mem + slot, 1, NVM_SLOT_BYTES, f);
	fclose(f);
	(void)n;
}

static void t_dump(const char *path, const uint8_t *src, size_t n)
{
	FILE *f = fopen(path, "wb");

	if (!f) {
		fprintf(stderr, "cannot write %s\n", path);
		exit(2);
	}
	fwrite(src, 1, n, f);
	fclose(f);
}

/* Every record of the shape: id, valid flag, the value's payload bytes. */
static void t_dump_state(const char *path)
{
	FILE *f = fopen(path, "w");
	struct nvm_rec r = nvm_rec_first();
	unsigned int j;

	if (!f) {
		fprintf(stderr, "cannot write %s\n", path);
		exit(2);
	}
	while (r.ok) {
		fprintf(f, "rec %u %d ", r.id, nvm_smodel_valid(r.id));
		for (j = 0; j < r.plen; ++j)
			fprintf(f, "%02x", nvm_smodel_value(r.id)[j]);
		fprintf(f, "\n");
		r = nvm_rec_next(r);
	}
	fclose(f);
}

/* ---- the script ------------------------------------------------------------- */
static int t_hex(char c)
{
	if (c >= '0' && c <= '9')
		return c - '0';
	if (c >= 'a' && c <= 'f')
		return c - 'a' + 10;
	return (c >= 'A' && c <= 'F') ? c - 'A' + 10 : -1;
}

/* ID:HEX, the new payload of one record. */
static void t_set_arg(const char *arg)
{
	uint8_t payload[NVM_PAYLOAD_MAX];
	char *end = NULL;
	unsigned long id = strtoul(arg, &end, 0);
	unsigned int n = 0;
	const char *hex = (end && *end == ':') ? end + 1 : "";

	while (hex[0] && hex[1] && n < NVM_PAYLOAD_MAX) {
		int hi = t_hex(hex[0]);
		int lo = t_hex(hex[1]);

		if (hi < 0 || lo < 0)
			break;
		payload[n++] = (uint8_t)((hi << 4) | lo);
		hex += 2;
	}
	t_set((unsigned int)id, payload, n);
}

/* The name at the head of MODE[:...] in names[], or -1. */
static int t_name(const char *arg, const char *const *names, unsigned int n)
{
	const char *colon = strchr(arg, ':');
	size_t len = colon ? (size_t)(colon - arg) : strlen(arg);
	unsigned int i;

	for (i = 0; i < n; ++i)
		if (strlen(names[i]) == len && strncmp(arg, names[i], len) == 0)
			return (int)i;
	t_fail("unknown_mode", 0, 0);
	return -1;
}

/* The numbers after MODE: COUNT (1 unless given), then SKIP and a last one. */
static void t_fields(const char *arg, unsigned long *v)
{
	const char *p = strchr(arg, ':');
	unsigned int i;

	v[0] = 1u;
	v[1] = 0u;
	v[2] = 0u;
	for (i = 0; i < 3u && p && *p == ':'; ++i) {
		char *end = NULL;

		v[i] = strtoul(p + 1, &end, 0);
		p = end;
	}
}

/* MODE[:COUNT[:SKIP[:AT]]]: arm a flash-model fault; AT places erase-stuck,
 * read-fail-at, read-flip-at and read-vary-at. */
static void t_fault_arg(const char *arg)
{
	static const char *const names[] = {
		"none", "erase-hang", "erase-stuck", "program-hang",
		"program-drop", "program-flip", "read-fail", "read-flip",
		"read-flip-at", "read-alias", "program-refuse", "erase-refuse",
		"read-fail-at", "read-vary-at",
	};
	unsigned long v[3];
	int i = t_name(arg, names, sizeof(names) / sizeof(names[0]));

	t_fields(arg, v);
	if (i < 0)
		return;
	nvm_fmodel_fault((enum nvm_fault)i, (unsigned int)v[0], (unsigned int)v[1]);
	if (v[2])
		nvm_fmodel_fault_at((uint32_t)v[2]);
}

/* KIND[:COUNT[:SKIP[:POLLS]]]: arm a command-master stall. */
static void t_stall_arg(const char *arg)
{
	static const char *const names[] = {
		"none", "tx", "rx", "drain",
	};
	unsigned long v[3];
	int i = t_name(arg, names, sizeof(names) / sizeof(names[0]));

	t_fields(arg, v);
	if (i >= 0)
		litespi_model_stall((enum litespi_stall)i, (unsigned int)v[0], (unsigned int)v[1],
				    (unsigned int)v[2]);
}

/* The port refuses to program or erase outside the journal: the first block
 * of the device holds the bitstream. */
static void t_port_guard(void)
{
	static const uint8_t page[4] = {
		0u, 0u, 0u, 0u,
	};
	unsigned int took = 0;

	nvm_fmodel_window(0u, NVM_FMODEL_BYTES);
	took += t.port->erase(t.port->ctx, 0u) == 0;
	took += t.port->program(t.port->ctx, 0u, page, sizeof(page)) == 0;
	took += t.port->erase(t.port->ctx, NVM_SLOT_A - 1u) == 0;
	took += t.port->program(t.port->ctx, NVM_SLOT_A + 2u * NVM_SLOT_BYTES, page, sizeof(page)) == 0;
	nvm_fmodel_window(NVM_SLOT_A, NVM_SLOT_A + T_JOURNAL);
	printf("GUARD took=%u\n", took);
}

static void t_flip_arg(const char *arg)
{
	char *end = NULL;
	unsigned long addr = strtoul(arg, &end, 0);
	unsigned long bit = (end && *end == ':') ? strtoul(end + 1, NULL, 0) : 0u;

	nvm_fmodel_flip((uint32_t)addr, (unsigned int)bit);
}

static void t_refuse_arg(const char *arg)
{
	if (t.knobs.n_refuse < 8u)
		t.knobs.refuse[t.knobs.n_refuse++] = (unsigned int)strtoul(arg, NULL, 0);
}

static void t_times_arg(const char *arg)
{
	char *end = NULL;
	unsigned long erase_ms = strtoul(arg, &end, 0);
	unsigned long program_us = (end && *end == ':') ? strtoul(end + 1, NULL, 0) : 1000u;

	nvm_fmodel_times((uint64_t)erase_ms * 1000u, program_us);
}

static void t_print_times(const char *tag, const struct t_times *tt)
{
	unsigned int i;

	printf("%s", tag);
	for (i = 0; i < tt->n && i < T_TIMES; ++i)
		printf(" %llu", (unsigned long long)tt->at[i]);
	printf("\n");
}

static void t_summary(void)
{
	const struct nvm_status *s = nvm_store_status();
	const struct nvm_fmodel_count *fc = nvm_fmodel_count();
	const struct nvm_smodel_count *sc = nvm_smodel_count();
	const struct litespi_model_count *lc = litespi_model_count();
	unsigned int i;

	printf("SUMMARY terminal=%d cause=%d vd_a=%d vd_b=%d last=%d first=%d seq_a=%u seq_b=%u "
	       "seq=%u auth=%d applied=%u refused=%u blank=%u releases=%u ok=%u "
	       "failed=%u skipped=%u attempts=%u exhausted=%d stale=%d dirty=%d "
	       "pending=%d phase=%d step_max=%u step_bound=%u steps=%u bind_terminal=%d "
	       "bind_cause=%d withheld=%u abandoned=%u abandoned_vd=%d unread=%u "
	       "read_faults=%u\n",
	       s->terminal, s->cause, s->verdict_a, s->verdict_b, s->last_verdict, s->first_failed,
	       s->seq_a, s->seq_b, s->seq, s->auth, s->applied, s->refused, s->blank,
	       s->releases, s->commits_ok, s->commits_failed, s->commits_skipped,
	       s->attempts, s->exhausted, s->stale, s->dirty, s->pending, s->phase,
	       s->step_bytes_max, (unsigned int)NVM_STEP_BOUND, s->steps, s->bind_terminal,
	       s->bind_cause, s->withheld, s->abandoned, s->abandoned_vd, s->unread, s->read_faults);
	printf("SUMMARY erases=%u programs=%u effects=%u outside=%u protected=%u "
	       "pagewrap=%u while_busy=%u descending=%u sm_applies=%u sm_applied=%u sm_refused=%u "
	       "sm_settles=%u sm_rollbacks=%u sm_unbinds=%u sm_releases=%u sm_order=%u "
	       "ls_wren=%u ls_pp=%u ls_se=%u ls_no_wel=%u ls_short=%u ls_refused=%u "
	       "ls_unknown=%u ls_stalled=%u ls_max_withheld=%u ls_hung=%u "
	       "max_call_us=%llu max_polls_call=%u calls=%u now_ms=%llu "
	       "commit_tries=%u commit_refused=%u img_len=%u n_rec=%u clock_hz=%u "
	       "ls_call_ticks=%u bad=%u\n",
	       fc->erases, fc->programs, fc->effects, fc->outside, fc->protected_hit,
	       fc->pagewrap, fc->while_busy, fc->descending, sc->applies, sc->applied, sc->refused,
	       sc->settles, sc->rollbacks, sc->unbinds, sc->releases, sc->order, lc->wren, lc->pp,
	       lc->se, lc->no_wel, lc->short_cmd, lc->refused, lc->unknown, lc->stalled,
	       lc->max_withheld, lc->hung, (unsigned long long)t.max_call_us, t.max_polls_call,
	       t.service_calls, (unsigned long long)(nvm_fmodel_now_us() / 1000u),
	       t.commit_tries, t.commit_refused, (unsigned int)NVM_IMG_LEN,
	       (unsigned int)NVM_N_REC, (unsigned int)CONFIG_CLOCK_FREQUENCY,
	       (unsigned int)nvm_flash_litespi_call_ticks, t.bad);
	printf("ERASES");
	for (i = 0; i < fc->erases && i < 16u; ++i)
		printf(" %llu", (unsigned long long)fc->erase_start_us[i]);
	printf("\n");
	t_print_times("FAILS", &t.fails);
	t_print_times("OKS", &t.oks);
}

/* A console commit: start one now and run until it settles. */
static void t_commit(void)
{
	if (!nvm_store_commit_now())
		t_fail("commit_not_started", nvm_store_status()->phase, 0);
	t_until_idle();
}

/* A console commit that may be refused: count the try and its answer. */
static void t_commit_try(void)
{
	t.commit_tries++;
	if (!nvm_store_commit_now())
		t.commit_refused++;
}

/* The port's elapsed time and the model's, read together: the time check
 * grades the first against the second. */
static void t_clock(void)
{
	uint64_t port_us = t.port->now_us(t.port->ctx);

	printf("CLOCK %llu %llu\n", (unsigned long long)port_us,
	       (unsigned long long)nvm_fmodel_now_us());
}

/* A change that leaves the value as it was (DR2b). */
static void t_touch_arg(const char *arg)
{
	struct nvm_rec r = nvm_rec_by_id((unsigned int)strtoul(arg, NULL, 0));

	nvm_store_changed(r.group, r.index);
}

/* One script word with no argument. */
static int t_word(const char *a)
{
	if (strcmp(a, "--litespi") == 0)
		t.port = &nvm_flash_litespi;
	else if (strcmp(a, "--not-ready") == 0)
		t.knobs.not_ready = 1;
	else if (strcmp(a, "--settle-fault") == 0)
		t.knobs.settle_fault = 1;
	else if (strcmp(a, "--rollback-fault") == 0)
		t.knobs.rollback_fault = 1;
	else if (strcmp(a, "--unbind-fault") == 0)
		t.knobs.unbind_fault = 1;
	else if (strcmp(a, "--commit-try") == 0)
		t_commit_try();
	else if (strcmp(a, "--mark") == 0)
		printf("MARK %llu\n", (unsigned long long)nvm_fmodel_now_us());
	else if (strcmp(a, "--clock") == 0)
		t_clock();
	else if (strcmp(a, "--boot") == 0)
		t_boot();
	else if (strcmp(a, "--blank") == 0)
		nvm_fmodel_blank();
	else if (strcmp(a, "--until-idle") == 0)
		t_until_idle();
	else if (strcmp(a, "--commit") == 0)
		t_commit();
	else if (strcmp(a, "--protect-auth") == 0)
		t_protect_auth();
	else if (strcmp(a, "--powercut") == 0)
		t_powercut();
	else if (strcmp(a, "--port-guard") == 0)
		t_port_guard();
	else
		return 0;
	return 1;
}

/* One script word with its argument. */
static int t_word_arg(const char *a, const char *v)
{
	if (strcmp(a, "--slot-a") == 0)
		t_load(v, NVM_SLOT_A);
	else if (strcmp(a, "--slot-b") == 0)
		t_load(v, NVM_SLOT_B);
	else if (strcmp(a, "--times") == 0)
		t_times_arg(v);
	else if (strcmp(a, "--refuse") == 0)
		t_refuse_arg(v);
	else if (strcmp(a, "--apply-fault") == 0) {
		t.knobs.apply_fault = 1;
		t.knobs.apply_fault_id = (unsigned int)strtoul(v, NULL, 0);
	} else if (strcmp(a, "--until-phase") == 0)
		t_until_phase((unsigned int)strtoul(v, NULL, 0));
	else if (strcmp(a, "--phc-step") == 0)
		litespi_model_phc_step((int64_t)strtoll(v, NULL, 0));
	else if (strcmp(a, "--ls-stall") == 0)
		t_stall_arg(v);
	else if (strcmp(a, "--set") == 0)
		t_set_arg(v);
	else if (strcmp(a, "--set-pattern") == 0)
		t_set_pattern((unsigned int)strtoul(v, NULL, 0), 1);
	else if (strcmp(a, "--touch") == 0)
		t_touch_arg(v);
	else if (strcmp(a, "--run-ms") == 0)
		t_run_ms(strtoull(v, NULL, 0));
	else if (strcmp(a, "--fault") == 0)
		t_fault_arg(v);
	else if (strcmp(a, "--boot-fault") == 0)
		snprintf(t.knobs.boot_fault, sizeof(t.knobs.boot_fault), "%s", v);
	else if (strcmp(a, "--flip") == 0)
		t_flip_arg(v);
	else if (strcmp(a, "--dump-slot-a") == 0)
		t_dump(v, nvm_fmodel_mem + NVM_SLOT_A, NVM_SLOT_BYTES);
	else if (strcmp(a, "--dump-slot-b") == 0)
		t_dump(v, nvm_fmodel_mem + NVM_SLOT_B, NVM_SLOT_BYTES);
	else if (strcmp(a, "--dump-stage") == 0)
		t_dump(v, nvm_store_stage(), NVM_IMG_LEN);
	else if (strcmp(a, "--dump-state") == 0)
		t_dump_state(v);
	else
		return 0;
	return 1;
}

int main(int argc, char **argv)
{
	int i;

	t.port = &nvm_fmodel_port;
	nvm_fmodel_power_on();
	nvm_fmodel_blank();
	nvm_smodel_reset();
	for (i = 1; i < argc; ++i) {
		if (t_word(argv[i]))
			continue;
		if (i + 1 < argc && t_word_arg(argv[i], argv[i + 1])) {
			i++;
			continue;
		}
		fprintf(stderr, "unknown or incomplete script word %s\n", argv[i]);
		return 2;
	}
	t_summary();
	return 0;
}

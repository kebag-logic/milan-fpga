/* SPDX-License-Identifier: (GPL-2.0 OR MIT) */
/*
 * nvm_store.c - the bare-metal saved-state store (#665 lane F1).
 *
 * THE BOOT PATH. Each journal slot is read into the stage in one read and
 * judged there by the section 6.2 order of
 * docs/design/SAVED_STATE_FASTCONNECT.md: the CRC, the records and the
 * sequence all come from the same bytes. The newer accepted slot (section 7:
 * the wrap-safe (int32_t)(A.seq - B.seq), A on a tie as in the shipping
 * writer; the other when it fails) is read into the stage again and judged
 * again, its CRC included, and its sequence must be the one it was chosen
 * by: what is applied and published is what was proven. The restore is the
 * two walks of SAVED_STATE_MATERIALIZATION.md section 8.1: the binding walk
 * first, its own unit (a fault fails it whole, with nothing preloaded), then
 * the D3 walk as one transaction (section 8.6): every other record in
 * ascending id through the state port, the settle step after the maps and
 * before the names (section 8.4), and an abort rolls every D3 value back to
 * its image default and leaves the bindings applied. AECP is released at
 * COMPLETE, BLANK or DEFAULTS and never at CLOSED.
 *
 * THE WRITE PATH. A change marks its record dirty. After the 1,000 ms
 * first-dirty window (DR2a) a capture latches the dirty records from their
 * owners into the stage, ONE RECORD PER STEP; the stage is sealed under the
 * next sequence, NVM_STEP_BYTES of CRC per step; the slot that is NOT
 * authoritative is erased, checked blank, programmed page by page in
 * ascending order (the header page first, the trailer that closes the CRC
 * last) and read back. Only a verified read-back moves the authority. The
 * authoritative slot is never erased, so at every instant of the sequence
 * one slot holds a complete container whose CRC closes (section 7), and a
 * power cut at any step boots the old content or the new one, never a mix.
 * A failed attempt keeps its records in flight; the captured work set gets
 * at most three attempts while it is unchanged, each 1,000 ms after the last
 * failure, and a capture that changes a staged byte starts a new one (DR2c).
 * A capture that changed no staged byte of a verified container is not
 * written (DR2b).
 *
 * Every step is bounded and returns: the media's waits are polled, never
 * spun on, so the event loop serves every other protocol through a 3 s
 * erase. No step touches more than NVM_STEP_BOUND bytes: one 256-byte
 * stretch, or one latched record's copy and crc16. Time is the flash port's
 * local counter, sampled once per step.
 */
#include "nvm_store.h"

#define NVM_US(ms) ((uint64_t)(ms) * 1000u)
#define NVM_NONE (-1)
#define NVM_WORDS (NVM_ID_SPACE / 32u)

struct nvm_store {
	const struct nvm_flash *flash;
	const struct nvm_state *state;
	struct nvm_status st;
	uint32_t dirty[NVM_WORDS];      /* changed, not yet captured */
	uint32_t inflight[NVM_WORDS];   /* captured, not yet in a verified slot */
	struct nvm_rec cursor;          /* the capture's next record */
	uint64_t now_us;                /* this step's time */
	uint64_t dirty_since_us;
	uint64_t retry_at_us;
	uint64_t op_start_us;
	uint32_t pos;                   /* seal, blank-check, program, verify */
	uint32_t crc;
	uint32_t len;                   /* the page program in flight */
	uint32_t next_seq;
	uint32_t step_bytes;
	int target;                     /* the slot being written: 0 A, 1 B */
	int dirty_armed;                /* the first-dirty window is open */
	int retry_armed;                /* a failed attempt's backoff runs */
	int force;                      /* a console commit: write even if unchanged */
	int stage_changed;              /* the capture changed a staged byte */
	int stage_durable;              /* the stage equals the authoritative slot */
};

static const struct nvm_store nvm_reset_value;
static struct nvm_store nvm;
/* The container, plus one record header of look-ahead (nvm_shape.h). */
static uint8_t nvm_stage[NVM_STAGE_BYTES];
/* One latched payload, compared with the staged one before it is copied. */
static uint8_t nvm_payload[NVM_PAYLOAD_MAX];
/* One read-back step. */
static uint8_t nvm_chunk[NVM_STEP_BYTES];

static uint32_t nvm_slot_addr(int slot)
{
	return slot ? NVM_SLOT_B : NVM_SLOT_A;
}

static uint64_t nvm_now(void)
{
	return nvm.flash->now_us(nvm.flash->ctx);
}

static uint32_t nvm_min(uint32_t a, uint32_t b)
{
	return (a < b) ? a : b;
}

static int nvm_bit(const uint32_t *v, unsigned int id)
{
	return (v[id >> 5] >> (id & 31u)) & 1u;
}

static int nvm_any(const uint32_t *v)
{
	unsigned int i;

	for (i = 0; i < NVM_WORDS; ++i)
		if (v[i])
			return 1;
	return 0;
}

static void nvm_publish(void)
{
	nvm.st.dirty = nvm_any(nvm.dirty);
	nvm.st.pending = nvm_any(nvm.inflight);
}

/* ---- the boot path ------------------------------------------------------- */

/* Section 6.2 over the slot at `slot`. A container that fits the stage is
 * read in once and judged there, so its CRC, its records and the sequence
 * returned are the same bytes. A longer one can never be this shape's: its
 * CRC is streamed through the stage for the verdict order alone. A slot that
 * does not deliver its bytes fails rule 4 (VD_LEN). */
static enum nvm_verdict nvm_slot_check(int slot, uint32_t *seq)
{
	const struct nvm_flash *f = nvm.flash;
	uint32_t addr = nvm_slot_addr(slot);
	uint32_t img_len = 0;
	uint32_t crc = 0xffffffffu;
	uint32_t pos = 0;
	uint8_t trailer[NVM_KLJ2_TRAILER];
	enum nvm_verdict vd;

	if (f->read(f->ctx, addr, nvm_stage, NVM_KLJ2_HDR))
		return NVM_VD_LEN;
	vd = nvm_klj2_check_head(nvm_stage, &img_len);
	if (vd != NVM_VD_OK)
		return vd;
	if (img_len <= NVM_STAGE_BYTES) {
		if (f->read(f->ctx, addr, nvm_stage, img_len))
			return NVM_VD_LEN;
		vd = nvm_klj2_check(nvm_stage, img_len);
		if (vd == NVM_VD_OK)
			*seq = nvm_klj2_seq(nvm_stage);
		return vd;
	}
	while (pos < img_len - NVM_KLJ2_TRAILER) {
		uint32_t n = nvm_min(NVM_STAGE_BYTES, img_len - NVM_KLJ2_TRAILER - pos);

		if (f->read(f->ctx, addr + pos, nvm_stage, n))
			return NVM_VD_LEN;
		crc = nvm_crc32_update(crc, nvm_stage, n);
		pos += n;
	}
	if (f->read(f->ctx, addr + pos, trailer, NVM_KLJ2_TRAILER))
		return NVM_VD_LEN;
	if (~crc != nvm_rd32le(trailer))
		return NVM_VD_CRC;
	if (f->read(f->ctx, addr, nvm_stage, NVM_STAGE_BYTES))
		return NVM_VD_LEN;
	return nvm_klj2_check_body(nvm_stage, img_len, NVM_STAGE_BYTES);
}

/* Section 7: the newer of two accepted slots, wrap-safe; else the one. */
static int nvm_pick(void)
{
	const struct nvm_status *s = &nvm.st;

	if (s->verdict_a == NVM_VD_OK && s->verdict_b == NVM_VD_OK)
		return ((int32_t)(s->seq_a - s->seq_b) >= 0) ? 0 : 1;
	if (s->verdict_a == NVM_VD_OK)
		return 0;
	return (s->verdict_b == NVM_VD_OK) ? 1 : NVM_NONE;
}

/* The chosen slot into the stage, judged again with its CRC: only bytes that
 * pass, under the sequence the slot was chosen by, are applied. */
static int nvm_stage_slot(int slot)
{
	const struct nvm_flash *f = nvm.flash;
	uint32_t seq = slot ? nvm.st.seq_b : nvm.st.seq_a;

	if (f->read(f->ctx, nvm_slot_addr(slot), nvm_stage, NVM_IMG_LEN))
		return 0;
	return nvm_klj2_check(nvm_stage, NVM_IMG_LEN) == NVM_VD_OK &&
	       nvm_klj2_seq(nvm_stage) == seq;
}

/* One saved record through the state port: 1 when its rule could not be
 * judged, which ends the walk. An erased record applies nothing and its
 * default stands. */
static int nvm_apply_faults(struct nvm_rec r)
{
	const struct nvm_state *s = nvm.state;
	const uint8_t *rec = nvm_stage + NVM_KLJ2_HDR + r.off;
	enum nvm_apply res;

	if (nvm_all_erased(rec, NVM_REC_HDR)) {
		nvm.st.blank++;
		return 0;
	}
	res = s->apply(s->ctx, r.group, r.index, rec + NVM_REC_HDR, r.plen);
	if (res == NVM_FAULT)
		return 1;
	if (res == NVM_APPLIED)
		nvm.st.applied++;
	else
		nvm.st.refused++;
	return 0;
}

/* The binding walk (section 8.1 step 4): every binding record, ascending.
 * A fault fails it whole, with nothing preloaded, and the D3 walk runs
 * anyway; a walk whose preloads cannot be dropped leaves the listener
 * unproven: CLOSED. */
static enum nvm_terminal nvm_walk_bind(void)
{
	struct nvm_rec r;

	for (r = nvm_rec_first(); r.ok; r = nvm_rec_next(r)) {
		if (r.group != NVM_G_BIND || !nvm_apply_faults(r))
			continue;
		nvm.st.bind_cause = NVM_C_APPLY;
		if (nvm.state->rollback(nvm.state->ctx, NVM_W_BIND) != 0)
			return NVM_T_CLOSED;
		return NVM_T_DEFAULTS;
	}
	return NVM_T_COMPLETE;
}

/* A D3 abort names the walk by its first cause; the roll-back decides
 * DEFAULTS or CLOSED (section 8.6). */
static enum nvm_terminal nvm_abort(enum nvm_cause cause)
{
	nvm.st.cause = cause;
	if (nvm.state->rollback(nvm.state->ctx, NVM_W_D3) != 0)
		return NVM_T_CLOSED;
	return NVM_T_DEFAULTS;
}

/* The D3 walk over the staged, proven container: every record but the
 * bindings, as one transaction. */
static enum nvm_terminal nvm_walk_d3(void)
{
	const struct nvm_state *s = nvm.state;
	struct nvm_rec r;
	int settled = 0;

	for (r = nvm_rec_first(); r.ok; r = nvm_rec_next(r)) {
		if (r.group == NVM_G_BIND)
			continue;
		if (r.group == NVM_G_NAME && !settled) {
			settled = 1;
			if (s->settle(s->ctx) == NVM_FAULT)
				return nvm_abort(NVM_C_SETTLE);
		}
		if (nvm_apply_faults(r))
			return nvm_abort(NVM_C_APPLY);
	}
	if (!settled && s->settle(s->ctx) == NVM_FAULT)
		return nvm_abort(NVM_C_SETTLE);
	return NVM_T_COMPLETE;
}

/* Judge both slots and stage the one to offer; NVM_NONE for blank media or
 * two refusals, with the stage then holding the blank container. */
static int nvm_choose(void)
{
	int chosen;

	nvm.st.verdict_a = nvm_slot_check(0, &nvm.st.seq_a);
	nvm.st.verdict_b = nvm_slot_check(1, &nvm.st.seq_b);
	chosen = nvm_pick();
	if (chosen != NVM_NONE && !nvm_stage_slot(chosen)) {
		/* the slot did not read back as it was judged: offer the other */
		nvm.st.cause = NVM_C_STAGE;
		if (chosen == 0)
			nvm.st.verdict_a = NVM_VD_LEN;
		else
			nvm.st.verdict_b = NVM_VD_LEN;
		chosen = nvm_pick();
		if (chosen != NVM_NONE && !nvm_stage_slot(chosen))
			chosen = NVM_NONE;
	}
	if (chosen == NVM_NONE)
		nvm_klj2_blank(nvm_stage);
	return chosen;
}

void nvm_store_boot(const struct nvm_flash *flash, const struct nvm_state *state)
{
	int chosen;

	nvm = nvm_reset_value;
	nvm.flash = flash;
	nvm.state = state;
	nvm.st.auth = NVM_NONE;
	nvm.st.phase = NVM_P_OFF;
	if (!state->model_ready(state->ctx)) {
		/* nothing can be judged: AECP stays held until reset */
		nvm.st.cause = NVM_C_MODEL;
		nvm.st.terminal = NVM_T_CLOSED;
		return;
	}
	if (!nvm_shape_consistent()) {
		/* persistence disabled; the entity runs on its defaults (DR3b) */
		nvm.st.cause = NVM_C_SHAPE;
		nvm.st.terminal = NVM_T_DEFAULTS;
		state->release(state->ctx);
		nvm.st.releases++;
		return;
	}
	chosen = nvm_choose();
	if (chosen == NVM_NONE) {
		nvm.st.last_verdict = (nvm.st.verdict_a != NVM_VD_BLANK) ?
				      nvm.st.verdict_a : nvm.st.verdict_b;
		nvm.st.bind_terminal = NVM_T_BLANK;
		nvm.st.terminal = NVM_T_BLANK;
	} else {
		nvm.st.auth = chosen;
		nvm.st.seq = nvm_klj2_seq(nvm_stage);
		nvm.st.last_verdict = NVM_VD_OK;
		nvm.stage_durable = 1;
		nvm.st.bind_terminal = nvm_walk_bind();
		nvm.st.terminal = (nvm.st.bind_terminal == NVM_T_CLOSED) ?
				  NVM_T_CLOSED : nvm_walk_d3();
	}
	if (nvm.st.terminal == NVM_T_CLOSED)
		return;
	state->release(state->ctx);
	nvm.st.releases++;
	nvm.st.phase = NVM_P_IDLE;
}

/* ---- the write path ------------------------------------------------------- */

static void nvm_capture_begin(void)
{
	nvm.cursor = nvm_rec_first();
	nvm.stage_changed = 0;
	/* every change so far is this capture's; a later one opens a window */
	nvm.dirty_armed = 0;
	nvm.retry_armed = 0;
	nvm.st.phase = NVM_P_CAPTURE;
}

/* DR2c spaces every attempt 1,000 ms after a failed one; DR2a starts a
 * capture 1,000 ms after the first change it takes; a failed work set is
 * retried while it has attempts left. */
static void nvm_idle(void)
{
	int due;

	if (nvm.retry_armed && nvm.now_us < nvm.retry_at_us)
		return;
	due = nvm.dirty_armed && nvm_any(nvm.dirty) &&
	      nvm.now_us - nvm.dirty_since_us >= NVM_US(MILAN_NVM_DEBOUNCE_MS);
	if (due || (nvm_any(nvm.inflight) && !nvm.st.exhausted))
		nvm_capture_begin();
}

/* 1 when the staged span of r is a frame of r (its crc is then the payload's:
 * the stage holds only proven containers and frames this store wrote). */
static int nvm_framed_as(const uint8_t *rec, struct nvm_rec r)
{
	return rec[0] == (uint8_t)(NVM_REC_MAGIC >> 8) && rec[1] == (uint8_t)NVM_REC_MAGIC &&
	       rec[2] == (uint8_t)MILAN_NVM_REC_LAYOUT && rec[3] == r.id &&
	       rec[4] == (uint8_t)(r.plen >> 8) && rec[5] == (uint8_t)r.plen;
}

/* Latch one record from its owner into the stage. */
static void nvm_latch(struct nvm_rec r)
{
	const struct nvm_state *s = nvm.state;
	uint8_t *rec = nvm_stage + NVM_KLJ2_HDR + r.off;
	int same;
	unsigned int i;

	if (!s->latch(s->ctx, r.group, r.index, nvm_payload, r.plen))
		return;                 /* nothing to save: the staged bytes stand */
	same = nvm_framed_as(rec, r);
	for (i = 0; i < r.plen; ++i) {
		if (rec[NVM_REC_HDR + i] != nvm_payload[i])
			same = 0;
		rec[NVM_REC_HDR + i] = nvm_payload[i];
	}
	nvm.step_bytes += r.plen;
	if (same)
		return;
	nvm_rec_frame(rec, r);
	nvm.step_bytes += 6u + r.plen;
	nvm.stage_changed = 1;
	nvm.stage_durable = 0;
}

/* The capture is over: decide whether its work set is written. */
static void nvm_seal_begin(void)
{
	unsigned int i;

	if (nvm.stage_changed) {
		/* a changed staged byte is a new work set: its own attempts */
		nvm.st.attempts = 0;
		nvm.st.exhausted = 0;
	} else if (nvm.st.exhausted) {
		/* DR2c: the unchanged set spent its attempts; a console commit
		 * does not buy a fourth */
		nvm.st.withheld++;
		nvm.force = 0;
		nvm.st.phase = NVM_P_IDLE;
		return;
	} else if (nvm.stage_durable && !nvm.force) {
		/* DR2b: the verified container already holds every value */
		for (i = 0; i < NVM_WORDS; ++i)
			nvm.inflight[i] = 0;
		nvm.st.commits_skipped++;
		nvm.st.phase = NVM_P_IDLE;
		return;
	}
	nvm.next_seq = nvm.st.seq + 1u;
	nvm_klj2_header(nvm_stage, nvm.next_seq);
	nvm.stage_durable = 0;
	nvm.crc = 0xffffffffu;
	nvm.pos = 0;
	nvm.st.phase = NVM_P_SEAL;
}

static void nvm_capture_step(void)
{
	struct nvm_rec r = nvm.cursor;

	while (r.ok && !nvm_bit(nvm.dirty, r.id))
		r = nvm_rec_next(r);
	if (!r.ok) {
		nvm.cursor = r;
		nvm_seal_begin();
		return;
	}
	nvm.cursor = nvm_rec_next(r);
	nvm.dirty[r.id >> 5] &= ~(1u << (r.id & 31u));
	nvm.inflight[r.id >> 5] |= 1u << (r.id & 31u);
	nvm_latch(r);
}

static void nvm_seal_step(void)
{
	uint32_t end = NVM_IMG_LEN - NVM_KLJ2_TRAILER;
	uint32_t n = nvm_min(NVM_STEP_BYTES, end - nvm.pos);

	nvm.crc = nvm_crc32_update(nvm.crc, nvm_stage + nvm.pos, n);
	nvm.pos += n;
	nvm.step_bytes += n;
	if (nvm.pos < end)
		return;
	nvm_wr32le(nvm_stage + end, ~nvm.crc);
	nvm.st.phase = NVM_P_ERASE;
}

/* A failed attempt: its records stay in flight, the claim is stale, and the
 * next attempt waits NVM_TXN_BACKOFF_MS (DR2c). The third failure of one
 * work set abandons it, and the reset-sticky record says so. */
static void nvm_fail(enum nvm_verdict vd)
{
	if (nvm.st.attempts == 0u)
		nvm.st.first_failed = vd;
	nvm.st.last_verdict = vd;
	nvm.st.commits_failed++;
	nvm.st.attempts++;
	nvm.st.stale = 1;
	if (nvm.st.attempts >= NVM_TXN_ATTEMPTS) {
		nvm.st.exhausted = 1;
		nvm.st.abandoned++;
		nvm.st.abandoned_vd = nvm.st.first_failed;
	}
	nvm.retry_at_us = nvm.now_us + NVM_US(NVM_TXN_BACKOFF_MS);
	nvm.retry_armed = 1;
	nvm.force = 0;
	nvm.st.phase = NVM_P_IDLE;
}

/* With no authoritative slot, a blank slot takes the commit before a refused
 * one: an old image is never erased merely because it was refused (DR5). */
static int nvm_target_slot(void)
{
	if (nvm.st.auth != NVM_NONE)
		return !nvm.st.auth;
	return nvm.st.verdict_a != NVM_VD_BLANK && nvm.st.verdict_b == NVM_VD_BLANK;
}

static void nvm_erase_start(void)
{
	const struct nvm_flash *f = nvm.flash;

	nvm.target = nvm_target_slot();
	if (nvm.target == nvm.st.auth || f->erase(f->ctx, nvm_slot_addr(nvm.target))) {
		nvm_fail(NVM_VD_ERASE);
		return;
	}
	nvm.op_start_us = nvm.now_us;
	nvm.st.phase = NVM_P_ERASE_WAIT;
}

/* 1 when the operation in flight ended; a fault or the timeout fails the
 * attempt with vd. */
static int nvm_wait(uint64_t timeout_us, enum nvm_verdict vd)
{
	const struct nvm_flash *f = nvm.flash;
	int busy = f->busy(f->ctx);

	if (busy == 0)
		return 1;
	if (busy < 0 || nvm.now_us - nvm.op_start_us > timeout_us)
		nvm_fail(vd);
	return 0;
}

/* Read the next step of the target slot into the chunk; 0 on a read fault. */
static uint32_t nvm_read_step(void)
{
	const struct nvm_flash *f = nvm.flash;
	uint32_t n = nvm_min(NVM_STEP_BYTES, NVM_IMG_LEN - nvm.pos);

	if (f->read(f->ctx, nvm_slot_addr(nvm.target) + nvm.pos, nvm_chunk, n))
		return 0;
	nvm.step_bytes += n;
	return n;
}

static void nvm_blankcheck_step(void)
{
	uint32_t n = nvm_read_step();

	if (!n || !nvm_all_erased(nvm_chunk, n)) {
		nvm_fail(NVM_VD_ERASE);
		return;
	}
	nvm.pos += n;
	if (nvm.pos >= NVM_IMG_LEN) {
		nvm.pos = 0;
		nvm.st.phase = NVM_P_PROGRAM;
	}
}

static void nvm_program_step(void)
{
	const struct nvm_flash *f = nvm.flash;
	uint32_t n = nvm_min(NVM_FLASH_PAGE, NVM_IMG_LEN - nvm.pos);

	if (f->program(f->ctx, nvm_slot_addr(nvm.target) + nvm.pos, nvm_stage + nvm.pos, n)) {
		nvm_fail(NVM_VD_PROGRAM);
		return;
	}
	nvm.len = n;
	nvm.step_bytes += n;
	nvm.op_start_us = nvm.now_us;
	nvm.st.phase = NVM_P_PROGRAM_WAIT;
}

/* The authority moves; nothing clears the abandoned-set record (DR2c). The
 * claim heals once nothing changed is left un-durable (FASTCONNECT 9.2). */
static void nvm_commit_done(void)
{
	unsigned int i;

	for (i = 0; i < NVM_WORDS; ++i)
		nvm.inflight[i] = 0;
	nvm.st.auth = nvm.target;
	nvm.st.seq = nvm.next_seq;
	nvm.stage_durable = 1;
	nvm.st.commits_ok++;
	nvm.st.attempts = 0;
	nvm.st.last_verdict = NVM_VD_OK;
	nvm.st.first_failed = NVM_VD_OK;
	if (!nvm_any(nvm.dirty))
		nvm.st.stale = 0;
	nvm.force = 0;
	nvm.st.phase = NVM_P_IDLE;
}

static void nvm_verify_step(void)
{
	uint32_t n = nvm_read_step();
	uint32_t i;

	if (!n) {
		nvm_fail(NVM_VD_VERIFY);
		return;
	}
	for (i = 0; i < n; ++i) {
		if (nvm_chunk[i] != nvm_stage[nvm.pos + i]) {
			nvm_fail(NVM_VD_VERIFY);
			return;
		}
	}
	nvm.pos += n;
	if (nvm.pos >= NVM_IMG_LEN)
		nvm_commit_done();
}

static void nvm_step(void)
{
	switch (nvm.st.phase) {
	case NVM_P_IDLE:
		nvm_idle();
		break;
	case NVM_P_CAPTURE:
		nvm_capture_step();
		break;
	case NVM_P_SEAL:
		nvm_seal_step();
		break;
	case NVM_P_ERASE:
		nvm_erase_start();
		break;
	case NVM_P_ERASE_WAIT:
		if (nvm_wait(NVM_US(MILAN_NVM_ERASE_TIMEOUT_MS), NVM_VD_ERASE)) {
			nvm.pos = 0;
			nvm.st.phase = NVM_P_BLANKCHECK;
		}
		break;
	case NVM_P_BLANKCHECK:
		nvm_blankcheck_step();
		break;
	case NVM_P_PROGRAM:
		nvm_program_step();
		break;
	case NVM_P_PROGRAM_WAIT:
		if (nvm_wait(NVM_US(MILAN_NVM_PROGRAM_TIMEOUT_MS), NVM_VD_PROGRAM)) {
			nvm.pos += nvm.len;
			nvm.st.phase = (nvm.pos < NVM_IMG_LEN) ? NVM_P_PROGRAM : NVM_P_VERIFY;
			if (nvm.st.phase == NVM_P_VERIFY)
				nvm.pos = 0;
		}
		break;
	case NVM_P_VERIFY:
		nvm_verify_step();
		break;
	default:
		break;
	}
}

void nvm_store_service(void)
{
	if (nvm.st.phase == NVM_P_OFF)
		return;
	nvm.step_bytes = 0;
	nvm.now_us = nvm_now();
	nvm_step();
	nvm.st.steps++;
	if (nvm.step_bytes > nvm.st.step_bytes_max)
		nvm.st.step_bytes_max = nvm.step_bytes;
	nvm_publish();
}

void nvm_store_changed(unsigned int group, unsigned int index)
{
	struct nvm_rec r = nvm_rec_of(group, index);
	int taken;

	if (!r.ok || nvm.st.phase == NVM_P_OFF)
		return;
	/* the running capture has yet to reach r: it takes this change, and
	 * leaves no window open behind it (DR2a) */
	taken = nvm.st.phase == NVM_P_CAPTURE && nvm.cursor.ok && r.id >= nvm.cursor.id;
	nvm.dirty[r.id >> 5] |= 1u << (r.id & 31u);
	if (!taken && !nvm.dirty_armed) {
		nvm.dirty_armed = 1;
		nvm.dirty_since_us = nvm_now();
	}
	nvm_publish();
}

int nvm_store_commit_now(void)
{
	if (nvm.st.phase != NVM_P_IDLE)
		return 0;
	/* DR2c: no attempt inside a failed one's backoff */
	if (nvm.retry_armed && nvm_now() < nvm.retry_at_us)
		return 0;
	nvm.force = 1;
	nvm_capture_begin();
	return 1;
}

const struct nvm_status *nvm_store_status(void)
{
	return &nvm.st;
}

const uint8_t *nvm_store_stage(void)
{
	return nvm_stage;
}

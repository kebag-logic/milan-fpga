/* SPDX-License-Identifier: (GPL-2.0 OR MIT) */
/*
 * nvm_store.c - the bare-metal saved-state store (#665 lane F1).
 *
 * THE JOURNAL (#823 decisions 3 and 5, docs/design/SAVED_STATE_FORMAT_32X32.md
 * section 4). Each slot is a base container at its start, then a log of
 * delta segments, each on its own page after the base: a KLJ3 header, the
 * changed records in ascending id, the pad and a CRC-32 trailer that closes
 * it. A record's value is the one in the last closing segment that holds it.
 * A slot's sequence is its last closing segment's, each delta's above the one
 * before it.
 *
 * THE BOOT PATH. Each journal slot's base is read into the stage in one read
 * and judged there by the section 6.2 order of
 * docs/design/SAVED_STATE_FASTCONNECT.md: the CRC, the records and the
 * sequence all come from the same bytes. A slot gets at most NVM_READ_TRIES
 * reads: an OK verdict stands on one, any other only when two reads return
 * the same bytes, and a slot that gives neither is UNREAD. Its log is then
 * walked, segment by segment, to the first that does not close: an erased
 * header ends it cleanly, anything else is torn. A walk ends on bytes that
 * could be a misread, so it stands only when two walks return the same bytes,
 * and a slot whose walks never do is UNREAD too. The newer accepted slot
 * (section 7: the wrap-safe (int32_t)(A.seq - B.seq) >= 0 on the slots' last
 * closing sequences, A on a tie by #665 decision 1; the other when it fails)
 * is read into the stage again and judged again, its CRC included, and its
 * log replayed into the stage, every delta judged again: its sequence and its
 * log's end must be the ones it was chosen by, so what is applied and
 * published is what was proven. A slot that never reads back so is UNREAD
 * too. The restore is the order of SAVED_STATE_MATERIALIZATION.md section
 * 8.1: the binding walk first, its own unit (a fault fails it whole, with
 * nothing preloaded); then the entity model must be proven, or the restore
 * ends CLOSED with the bindings kept; then the D3 walk as one transaction
 * (section 8.6): every other record in ascending id through the state port,
 * the settle step after the maps and before the names (section 8.4), and an
 * abort rolls every D3 value back to its image default and leaves the
 * bindings applied. AECP is released at COMPLETE, BLANK or DEFAULTS and never
 * at CLOSED. An UNREAD slot leaves the authority unknown (#665 decision 2):
 * the writer is HELD until reset, because a commit could restart the
 * sequence below a container that survives it.
 *
 * THE FORMAT is the split placement's KLJ3 in journal_klj3 (#823, nvm_shape.h).
 * Today's journal is the all-fabric placement's KLJ2: the boot reads its two
 * headers and records a KLJ2 one in `legacy`, and nothing here writes it, so
 * an all-fabric image rolled back to finds its saved state (decision 2).
 *
 * THE WRITE PATH. A change marks its record dirty. After the NVM_WINDOW_MS
 * first-dirty window (#823 decision 4) a capture latches the dirty records
 * from their owners into the stage, ONE RECORD PER STEP; a record whose
 * staged bytes changed is in flight. The records in flight are then APPENDED
 * to the authoritative slot as one delta, at most NVM_SEG_PAGES pages, page
 * by page in ascending order (the header first, the trailer that closes the
 * CRC last) and read back. A save never erases. The rest of a larger burst
 * follows in the next delta. A delta that fails leaves its segment torn, and
 * nothing appends past it.
 *
 * COMPACTION writes the stage, as a base, into the other slot once it is
 * blank: when the log has less than its reserve left, when it is torn, when
 * no slot is authoritative, or for the console. It yields to a save between
 * pages, and the save appends to the authoritative slot as before. A record
 * that runs past a page is kept whole for the next one, so every record of
 * the base is one moment's value. The base carries the authoritative slot's
 * sequence; once it is read back, the deltas the old slot took since the
 * compaction began are copied page for page behind it, and only then does
 * the authority move. Until it moves the old slot holds everything and is the
 * newer or the same; a value in flight is appended to the new slot after.
 *
 * THE BACKGROUND ERASE prepares the slot that is not authoritative: every
 * page read blank, a block found written erased, one at a time, and read
 * again. A save that must program while that erase runs suspends it, times
 * the suspend, programs and reads back, and resumes it (decision 5). The
 * authoritative slot is never erased. So at every instant one slot holds
 * every value a save reported, and a power cut at any step boots the old
 * content or the new one, never a mix.
 *
 * DR2b, DR2c and DR5 stand: a capture that changed no staged byte writes
 * nothing; a failed attempt keeps its records in flight, and an unchanged
 * work set gets NVM_TXN_ATTEMPTS attempts NVM_TXN_BACKOFF_MS apart; with no
 * authoritative slot a blank one takes the first base before a refused one.
 *
 * Every step is bounded and returns: the media's waits are polled, never
 * spun on, so the event loop serves every other protocol through a 3 s
 * erase. No step touches more than NVM_STEP_BOUND bytes: one 256-byte
 * stretch, one latched record's copy and crc16, or one carried record. Time
 * is the flash port's local counter, sampled once per step.
 */
#include "nvm_store.h"

#define NVM_US(ms) ((uint64_t)(ms) * 1000u)
#define NVM_NONE (-1)
#define NVM_WORDS ((NVM_ID_SPACE + 31u) / 32u)

/* The open bits (#823 decision 6): one bit per record id of the layout 3
 * space, in a word array of the store's static RAM, with the count of the
 * bits set. Whether any record is open is then a compare, not a scan of the
 * NVM_WORDS words on every service step. */
struct nvm_open {
	uint32_t bit[NVM_WORDS];
	unsigned int count;
};

/* What a segment write is: a delta into the authoritative slot, a
 * compaction's base, or the copy of the old slot's log behind that base. */
enum nvm_kind {
	NVM_K_DELTA = 0,
	NVM_K_BASE = 1,
	NVM_K_COPY = 2
};

/* One segment being written, page by page. */
struct nvm_seg {
	enum nvm_kind kind;
	int slot;
	uint32_t at;                    /* its offset in the slot */
	uint32_t len;                   /* its bytes (a copy: the old log's) */
	uint32_t pos;                   /* bytes read back so far */
	uint32_t page;                  /* bytes of the page in flight */
	uint32_t crc;
	uint32_t seq;
	uint32_t n_rec;
	struct nvm_rec rec;             /* a delta's record in hand; a base's past the front */
	uint32_t rec_pos;               /* bytes of a delta's record already taken */
	unsigned int last;              /* a delta's last record id */
	int programmed;                 /* a delta had a page program issued */
};

struct nvm_store {
	const struct nvm_flash *flash;
	const struct nvm_state *state;
	struct nvm_status st;
	struct nvm_open dirty;          /* changed, not yet captured */
	struct nvm_open inflight;       /* captured, not yet in a verified segment */
	struct nvm_open behind;         /* latched behind the compaction's front */
	struct nvm_rec cursor;          /* the capture's next record */
	struct nvm_seg app;             /* the delta */
	struct nvm_seg cmp;             /* the compaction */
	struct nvm_seg *cur;            /* the segment the page phases write */
	uint64_t now_us;                /* this step's time */
	uint64_t dirty_since_us;
	uint64_t retry_at_us;
	uint64_t op_start_us;
	uint64_t due_us;                /* the save fell due */
	uint64_t erase_from_us;         /* the erase last started or resumed */
	uint64_t erase_run_us;          /* its time running before that */
	uint64_t prep_at_us;            /* a failed preparation's backoff */
	uint32_t base_seq[2];           /* each slot's base sequence, as judged */
	uint32_t end_of[2];             /* each slot's log end, as judged */
	int torn_of[2];
	uint32_t front;                 /* the compaction's base is taken below this */
	uint32_t carry_at;              /* where the carried record's rest starts */
	uint32_t copy_from;             /* the old log's end when the compaction began */
	uint32_t prep_pos;
	uint32_t step_bytes;
	int prep_slot;
	int prep_erased;                /* this block was erased in this preparation */
	unsigned int prep_tries;
	int erasing;                    /* an erase was issued and not seen to end */
	int owed;                       /* a failed wait may have left the device busy */
	int suspended;
	int in_append;                  /* the save's deadline runs */
	int full;                       /* no record in flight fits the log's room */
	int force_cmp;                  /* the console asked for a whole image */
	int dirty_armed;                /* the first-dirty window is open */
	int retry_armed;                /* a failed attempt's backoff runs */
	int force;                      /* a console commit: write even if unchanged */
	int stage_changed;              /* the capture changed a staged byte */
};

static const struct nvm_store nvm_reset_value;
static struct nvm_store nvm;
/* The container, plus one record header of look-ahead (nvm_shape.h). */
static uint8_t nvm_stage[NVM_STAGE_BYTES];
/* One latched payload, compared with the staged one before it is copied. */
static uint8_t nvm_payload[NVM_PAYLOAD_MAX];
/* One read-back step. */
static uint8_t nvm_chunk[NVM_STEP_BYTES];
/* The page being written, as programmed. */
static uint8_t nvm_page[NVM_FLASH_PAGE];
/* The rest of the record a base's page cuts, as it was when the page was. */
static uint8_t nvm_carry[NVM_SZ(NVM_PAYLOAD_MAX)];

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

static int nvm_bit(const struct nvm_open *v, unsigned int id)
{
	return (v->bit[id >> 5] >> (id & 31u)) & 1u;
}

/* Open record id; the count follows only a bit that was clear. */
static void nvm_open_set(struct nvm_open *v, unsigned int id)
{
	if (nvm_bit(v, id))
		return;
	v->bit[id >> 5] |= 1u << (id & 31u);
	v->count++;
}

/* Close record id, whose bit the caller found set. */
static void nvm_open_take(struct nvm_open *v, unsigned int id)
{
	v->bit[id >> 5] &= ~(1u << (id & 31u));
	v->count--;
}

static void nvm_open_clear(struct nvm_open *v)
{
	unsigned int i;

	for (i = 0; i < NVM_WORDS; ++i)
		v->bit[i] = 0;
	v->count = 0;
}

static int nvm_any(const struct nvm_open *v)
{
	return v->count != 0u;
}

static int nvm_cmp_wanted(void);

static void nvm_publish(void)
{
	nvm.st.dirty = nvm_any(&nvm.dirty);
	nvm.st.pending = nvm_any(&nvm.inflight);
	nvm.st.n_dirty = nvm.dirty.count;
	nvm.st.n_inflight = nvm.inflight.count;
	nvm.st.cmp_due = !nvm.st.exhausted && nvm.st.bg != NVM_B_FAILED && nvm_cmp_wanted();
}

/* ---- the boot path ------------------------------------------------------- */

/* Not a verdict: the port did not deliver the bytes. */
#define NVM_UNREAD NVM_VD_COUNT

/* What one read of a slot returned: its verdict, and a CRC-32 over every
 * byte the port delivered for it, with their count. The verdict is judged on
 * exactly those bytes, so two reads that return the same bytes are judged
 * alike; two that do not were not both read cleanly. */
struct nvm_read {
	enum nvm_verdict vd;
	uint32_t digest;
	uint32_t bytes;
};

/* One port read for the slot read `rd`: 0 when the port delivered the bytes,
 * which are then counted into its digest. */
static int nvm_take(struct nvm_read *rd, uint32_t addr, uint8_t *dst, uint32_t len)
{
	if (nvm.flash->read(nvm.flash->ctx, addr, dst, len))
		return -1;
	rd->digest = nvm_crc32_update(rd->digest, dst, len);
	rd->bytes += len;
	return 0;
}

/* Section 6.2 over one read of the slot at `slot`, recorded in `rd`. A
 * container that fits the stage is read in once and judged there, so its
 * CRC, its records and the sequence returned are the same bytes. A longer one
 * can never be this shape's: its CRC is streamed through the stage for the
 * verdict order alone. NVM_UNREAD when the port fails a read. */
static enum nvm_verdict nvm_slot_read(int slot, uint32_t *seq, struct nvm_read *rd)
{
	uint32_t addr = nvm_slot_addr(slot);
	uint32_t img_len = 0;
	uint32_t crc = 0xffffffffu;
	uint32_t pos = 0;
	uint8_t trailer[NVM_KLJ_TRAILER];
	enum nvm_verdict vd;

	rd->digest = 0xffffffffu;
	rd->bytes = 0;
	if (nvm_take(rd, addr, nvm_stage, NVM_KLJ_HDR))
		return NVM_UNREAD;
	vd = nvm_klj2_check_head(nvm_stage, &img_len);
	if (vd != NVM_VD_OK)
		return vd;
	if (img_len <= NVM_STAGE_BYTES) {
		if (nvm_take(rd, addr, nvm_stage, img_len))
			return NVM_UNREAD;
		vd = nvm_klj2_check(nvm_stage, img_len);
		if (vd == NVM_VD_OK)
			*seq = nvm_klj2_seq(nvm_stage);
		return vd;
	}
	while (pos < img_len - NVM_KLJ_TRAILER) {
		uint32_t n = nvm_min(NVM_STAGE_BYTES, img_len - NVM_KLJ_TRAILER - pos);

		if (nvm_take(rd, addr + pos, nvm_stage, n))
			return NVM_UNREAD;
		crc = nvm_crc32_update(crc, nvm_stage, n);
		pos += n;
	}
	if (nvm_take(rd, addr + pos, trailer, NVM_KLJ_TRAILER))
		return NVM_UNREAD;
	if (~crc != nvm_rd32le(trailer))
		return NVM_VD_CRC;
	if (nvm_take(rd, addr, nvm_stage, NVM_STAGE_BYTES))
		return NVM_UNREAD;
	return nvm_klj2_check_body(nvm_stage, img_len, NVM_STAGE_BYTES);
}

/* A slot whose authority is unknown (#665 decision 2): refused VD_LEN, the
 * rule 4 verdict of a slot that did not deliver its bytes, and recorded, so
 * the writer is held until reset. Nothing is read from it. */
static enum nvm_verdict nvm_unread(int slot)
{
	nvm.st.unread |= 1u << slot;
	return NVM_VD_LEN;
}

/* 1 when read n of `seen` returned the same bytes as an earlier one: the same
 * count and digest, and so the same verdict. */
static int nvm_agrees(const struct nvm_read *seen, unsigned int n)
{
	unsigned int j;

	for (j = 0; j < n; ++j)
		if (seen[j].vd == seen[n].vd && seen[j].digest == seen[n].digest &&
		    seen[j].bytes == seen[n].bytes)
			return 1;
	return 0;
}

/* The slot's base verdict, from at most NVM_READ_TRIES reads of it. OK
 * stands on one read: its CRC-32 covers every byte, the sequence included.
 * Any other verdict, BLANK included, stands only when two reads return the
 * same bytes (#665 issue comment 5999350068): a read that went wrong without
 * the port saying so looks like a refusal or like a blank slot, and either
 * would let the next commit restart the sequence below a container that
 * survives. Two reads whose bytes differ are a media fault, however alike
 * their verdicts, and the slot is read again. A slot whose reads fail or
 * never return the same bytes is UNREAD. */
static enum nvm_verdict nvm_base_check(int slot, uint32_t *seq)
{
	struct nvm_read seen[NVM_READ_TRIES];
	unsigned int n = 0;
	unsigned int i;

	for (i = 0; i < NVM_READ_TRIES; ++i) {
		seen[n].vd = nvm_slot_read(slot, seq, &seen[n]);
		if (seen[n].vd == NVM_UNREAD) {
			nvm.st.read_faults++;
			continue;       /* the port failed a read: read the slot again */
		}
		if (seen[n].vd == NVM_VD_OK || nvm_agrees(seen, n))
			return seen[n].vd;
		if (n)
			nvm.st.read_faults++;   /* other bytes than every earlier read */
		n++;
	}
	return nvm_unread(slot);
}

/* Where a slot's log ends: the offset past its last closing delta, that
 * delta's sequence, how many closed, and whether a segment there does not
 * close. */
struct nvm_log {
	uint32_t end;
	uint32_t seq;
	unsigned int n;
	int torn;
};

/* One delta segment at `off` of `slot`, read into `rd`, after a segment of
 * sequence *seq: NVM_VD_OK when it closes, with *seq its sequence and *len
 * its bytes; NVM_VD_BLANK for an erased header, the log's end; any other
 * verdict for a segment that does not close; NVM_UNREAD when the port fails
 * a read. A closing delta is a KLJ3 header (rules 1 to 3, 6 and 7, at most
 * NVM_SEG_MAX and the slot's room), a sequence above the one before it, then
 * N_REC framed records of this shape in ascending id (never an erased one),
 * the pad, and the CRC-32 over all of it. With `apply`, each record is read
 * into the stage at its own offset. */
static enum nvm_verdict nvm_seg_read(int slot, uint32_t off, int apply, struct nvm_read *rd,
				     uint32_t *seq, uint32_t *len)
{
	uint32_t addr = nvm_slot_addr(slot) + off;
	uint8_t hdr[NVM_REC_HDR];
	uint32_t end = 0;
	uint32_t pos = NVM_KLJ_HDR;
	uint32_t crc;
	uint32_t nrec;
	uint32_t got;
	uint32_t pad;
	uint32_t i;
	int last = -1;
	enum nvm_verdict vd;

	if (nvm_take(rd, addr, nvm_chunk, NVM_KLJ_HDR))
		return NVM_UNREAD;
	if (nvm_all_erased(nvm_chunk, NVM_KLJ_HDR))
		return NVM_VD_BLANK;
	vd = nvm_klj2_check_seg(nvm_chunk, NVM_SLOT_BYTES - off, &end);
	if (vd != NVM_VD_OK)
		return vd;
	got = nvm_klj2_seq(nvm_chunk);
	if ((int32_t)(got - *seq) <= 0)
		return NVM_VD_STALE;
	nrec = nvm_rd32le(nvm_chunk + 12);
	crc = nvm_crc32_update(0xffffffffu, nvm_chunk, NVM_KLJ_HDR);
	end -= NVM_KLJ_TRAILER;
	for (i = 0; i < nrec; ++i) {
		struct nvm_rec r;
		uint8_t *pay = nvm_payload;
		unsigned int id;
		uint32_t plen;
		uint16_t c16;

		if (pos + NVM_REC_HDR > end)
			return NVM_VD_LEN;
		if (nvm_take(rd, addr + pos, hdr, NVM_REC_HDR))
			return NVM_UNREAD;
		id = ((unsigned int)hdr[4] << 8) | hdr[5];
		plen = ((uint32_t)hdr[6] << 8) | hdr[7];
		r = nvm_rec_by_id(id);
		if ((((uint32_t)hdr[0] << 8) | hdr[1]) != NVM_REC_MAGIC || hdr[2] != NVM3_LAYOUT || hdr[3] != 0u ||
		    (int)id <= last || !r.ok || r.plen != plen)
			return NVM_VD_REC;
		if (pos + NVM_REC_HDR + plen > end)
			return NVM_VD_LEN;
		if (apply)
			pay = nvm_stage + NVM_KLJ_HDR + r.off + NVM_REC_HDR;
		if (nvm_take(rd, addr + pos + NVM_REC_HDR, pay, plen))
			return NVM_UNREAD;
		c16 = nvm_crc16_update(0xffffu, hdr, NVM_REC_HDR - 2u);
		c16 = nvm_crc16_update(c16, pay, plen);
		if (c16 != ((((uint32_t)hdr[8]) << 8) | hdr[9]))
			return NVM_VD_REC;
		if (apply)
			for (pad = 0; pad < NVM_REC_HDR; ++pad)
				nvm_stage[NVM_KLJ_HDR + r.off + pad] = hdr[pad];
		crc = nvm_crc32_update(crc, hdr, NVM_REC_HDR);
		crc = nvm_crc32_update(crc, pay, plen);
		last = (int)id;
		pos += NVM_REC_HDR + plen;
	}
	pad = (4u - (pos & 3u)) & 3u;
	if (pos + pad != end)
		return NVM_VD_LEN;
	if (nvm_take(rd, addr + pos, nvm_chunk, pad + NVM_KLJ_TRAILER))
		return NVM_UNREAD;
	crc = nvm_crc32_update(crc, nvm_chunk, pad);
	if (~crc != nvm_rd32le(nvm_chunk + pad))
		return NVM_VD_CRC;
	*seq = got;
	*len = end + NVM_KLJ_TRAILER;
	return NVM_VD_OK;
}

/* One walk of a slot's log from its base of sequence seq, into `rd` and
 * `lg`, up to `limit`: NVM_VD_OK, or NVM_UNREAD when the port failed a read.
 * A replay into the stage stops at the end the log was judged to have, so a
 * torn segment past it is never read into the stage. */
static enum nvm_verdict nvm_log_read(int slot, uint32_t seq, int apply, uint32_t limit,
				     struct nvm_read *rd, struct nvm_log *lg)
{
	uint32_t off = NVM_LOG_START;
	uint32_t len = 0;
	enum nvm_verdict vd = NVM_VD_BLANK;

	rd->vd = NVM_VD_OK;
	rd->digest = 0xffffffffu;
	rd->bytes = 0;
	lg->n = 0;
	while (off + NVM_KLJ_HDR <= NVM_SLOT_BYTES && off < limit) {
		vd = nvm_seg_read(slot, off, apply, rd, &seq, &len);
		if (vd != NVM_VD_OK)
			break;
		off += NVM_PAGES(len) * NVM_FLASH_PAGE;
		lg->n++;
	}
	if (vd == NVM_UNREAD)
		return vd;
	lg->end = off;
	lg->seq = seq;
	lg->torn = vd != NVM_VD_BLANK && vd != NVM_VD_OK;
	return NVM_VD_OK;
}

/* The slot's log, judged as its base is: a walk ends on an erased or a torn
 * segment, bytes a misread could make, so it stands only when two walks
 * return the same bytes; 0 when none do in NVM_READ_TRIES. */
static int nvm_log_check(int slot, struct nvm_log *lg)
{
	struct nvm_read seen[NVM_READ_TRIES];
	struct nvm_log got[NVM_READ_TRIES];
	unsigned int n = 0;
	unsigned int i;

	for (i = 0; i < NVM_READ_TRIES; ++i) {
		if (nvm_log_read(slot, nvm.base_seq[slot], 0, NVM_SLOT_BYTES, &seen[n], &got[n]) == NVM_UNREAD) {
			nvm.st.read_faults++;
			continue;
		}
		if (nvm_agrees(seen, n)) {
			*lg = got[n];
			return 1;
		}
		if (n)
			nvm.st.read_faults++;
		n++;
	}
	return 0;
}

/* The slot's verdict, its base's, and its sequence, its log's last closing
 * segment's; a base whose log cannot be judged leaves the slot UNREAD. */
static enum nvm_verdict nvm_slot_check(int slot, uint32_t *seq)
{
	enum nvm_verdict vd = nvm_base_check(slot, seq);
	struct nvm_log lg;

	if (vd != NVM_VD_OK)
		return vd;
	nvm.base_seq[slot] = *seq;
	if (!nvm_log_check(slot, &lg))
		return nvm_unread(slot);
	*seq = lg.seq;
	nvm.end_of[slot] = lg.end;
	nvm.torn_of[slot] = lg.torn;
	return vd;
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

/* One re-stage of the chosen slot: its base judged again with its CRC under
 * the base sequence it was judged by, then its log replayed into the stage
 * to the end it was judged to have, every delta closing again, under the
 * sequence the slot was chosen by. Sequences only rise along a log, so a
 * replay under that sequence reached that end. */
static int nvm_restage_once(int slot, uint32_t seq)
{
	const struct nvm_flash *f = nvm.flash;
	struct nvm_read rd;
	struct nvm_log lg;

	if (f->read(f->ctx, nvm_slot_addr(slot), nvm_stage, NVM_IMG_LEN))
		return 0;
	if (nvm_klj2_check(nvm_stage, NVM_IMG_LEN) != NVM_VD_OK ||
	    nvm_klj2_seq(nvm_stage) != nvm.base_seq[slot])
		return 0;
	if (nvm_log_read(slot, nvm.base_seq[slot], 1, nvm.end_of[slot], &rd, &lg) != NVM_VD_OK)
		return 0;
	nvm.st.deltas = lg.n;
	return lg.seq == seq;
}

/* The chosen slot into the stage: only bytes that pass again are applied.
 * A re-stage that fails, or reads other bytes than were judged, is a media
 * fault and is tried again, NVM_READ_TRIES in all. */
static int nvm_stage_slot(int slot)
{
	uint32_t seq = slot ? nvm.st.seq_b : nvm.st.seq_a;
	unsigned int i;

	for (i = 0; i < NVM_READ_TRIES; ++i) {
		if (nvm_restage_once(slot, seq))
			return 1;
		nvm.st.read_faults++;
	}
	return 0;
}

/* One saved record through the state port: 1 when its rule could not be
 * judged, which ends the walk. An erased record applies nothing and its
 * default stands. */
static int nvm_apply_faults(struct nvm_rec r)
{
	const struct nvm_state *s = nvm.state;
	const uint8_t *rec = nvm_stage + NVM_KLJ_HDR + r.off;
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

/* Today's journal is the all-fabric placement's KLJ2 (#823 decision 2): a
 * KLJ2 header in either of its slots is recorded, one read of each header,
 * and nothing of it is applied or written. A read the port fails records
 * nothing: the journal is the other placement's, never this store's
 * authority. */
static void nvm_legacy_check(void)
{
	const struct nvm_flash *f = nvm.flash;
	const uint32_t slot = NVM_LEGACY_B - NVM_LEGACY_A;
	unsigned int i;

	for (i = 0; i < 2u; ++i)
		if (f->read(f->ctx, NVM_LEGACY_A + i * slot, nvm_chunk, NVM_KLJ_HDR) == 0 &&
		    nvm_rd32le(nvm_chunk) == NVM_KLJ2_MAGIC)
			nvm.st.legacy |= 1u << i;
}

/* Judge both slots and stage the one to offer: the newer accepted one, then
 * the other when it does not read back as it was judged (section 7), each
 * re-staged and judged again. NVM_NONE for blank media or two refusals,
 * with the stage then holding the blank container. */
static int nvm_choose(void)
{
	int chosen;

	nvm.st.verdict_a = nvm_slot_check(0, &nvm.st.seq_a);
	nvm.st.verdict_b = nvm_slot_check(1, &nvm.st.seq_b);
	chosen = nvm_pick();
	while (chosen != NVM_NONE && !nvm_stage_slot(chosen)) {
		/* the slot did not read back as it was judged: its authority is
		 * unknown, and the other is offered */
		nvm.st.cause = NVM_C_STAGE;
		if (chosen == 0)
			nvm.st.verdict_a = nvm_unread(0);
		else
			nvm.st.verdict_b = nvm_unread(1);
		chosen = nvm_pick();
	}
	if (chosen == NVM_NONE)
		nvm_klj2_blank(nvm_stage);
	return chosen;
}

/* Section 8.1 step 6: 1 when the entity model the values are judged against
 * is proven. Else the restore ends CLOSED: AECP stays held until reset, and
 * a binding walk that ran keeps the listener's bindings. */
static int nvm_model_proven(void)
{
	if (nvm.state->model_ready(nvm.state->ctx))
		return 1;
	nvm.st.cause = NVM_C_MODEL;
	nvm.st.terminal = NVM_T_CLOSED;
	return 0;
}

/* The restore of section 8.1: the slots judged and one staged (step 3), the
 * binding walk, which needs no entity model (steps 4 and 5), the model
 * check (step 6), then the D3 walk (steps 7 and 8). */
static void nvm_restore(void)
{
	int chosen = nvm_choose();

	nvm_legacy_check();
	if (chosen == NVM_NONE) {
		nvm.st.last_verdict = (nvm.st.verdict_a != NVM_VD_BLANK) ?
				      nvm.st.verdict_a : nvm.st.verdict_b;
		/* blank because the saved state is in the previous format: the
		 * boot's verdict names it (#823 decision 2) */
		if (nvm.st.last_verdict == NVM_VD_BLANK && nvm.st.legacy)
			nvm.st.last_verdict = NVM_VD_VER;
		nvm.st.deltas = 0;
		nvm.st.bind_terminal = NVM_T_BLANK;
		nvm.st.terminal = NVM_T_BLANK;
	} else {
		nvm.st.auth = chosen;
		nvm.st.seq = chosen ? nvm.st.seq_b : nvm.st.seq_a;
		nvm.st.log_end = nvm.end_of[chosen];
		nvm.st.torn = nvm.torn_of[chosen];
		nvm.st.last_verdict = NVM_VD_OK;
		nvm.st.bind_terminal = nvm_walk_bind();
	}
	if (nvm.st.bind_terminal == NVM_T_CLOSED) {
		nvm.st.terminal = NVM_T_CLOSED;
		return;
	}
	/* blank media too: nothing is released over an unproven model */
	if (nvm_model_proven() && chosen != NVM_NONE)
		nvm.st.terminal = nvm_walk_d3();
}

/* With no authoritative slot, a blank slot takes the first base before a
 * refused one: an old image is never erased merely because it was refused
 * (DR5). Else the slot that is not authoritative. */
static int nvm_target_slot(void)
{
	if (nvm.st.auth != NVM_NONE)
		return !nvm.st.auth;
	return nvm.st.verdict_a != NVM_VD_BLANK && nvm.st.verdict_b == NVM_VD_BLANK;
}

/* Prepare `slot` in the background: read every page blank from its first. */
static void nvm_prep(int slot)
{
	nvm.prep_slot = slot;
	nvm.prep_pos = 0;
	nvm.prep_erased = 0;
	nvm.st.bg = NVM_B_CHECK;
}

void nvm_store_boot(const struct nvm_flash *flash, const struct nvm_state *state)
{
	int shaped;

	nvm = nvm_reset_value;
	nvm.flash = flash;
	nvm.state = state;
	nvm.cur = &nvm.app;
	nvm.st.auth = NVM_NONE;
	nvm.st.phase = NVM_P_OFF;
	shaped = nvm_shape_consistent();
	if (shaped) {
		nvm_restore();
	} else if (nvm_model_proven()) {
		/* persistence disabled: no slot is read or walked, and the
		 * entity runs on its defaults (DR3b) */
		nvm.st.cause = NVM_C_SHAPE;
		nvm.st.terminal = NVM_T_DEFAULTS;
	}
	if (nvm.st.terminal == NVM_T_CLOSED)
		return;
	state->release(state->ctx);
	nvm.st.releases++;
	/* decision 2: while a slot's authority is unknown, nothing is written */
	if (shaped)
		nvm.st.phase = nvm.st.unread ? NVM_P_HELD : NVM_P_IDLE;
	if (nvm.st.phase == NVM_P_IDLE)
		nvm_prep(nvm_target_slot());
}

/* ---- the write path ------------------------------------------------------- */

/* A delta can go to the authoritative slot: there is one, it is not torn,
 * and its log had room for the last delta asked of it. */
static int nvm_can_append(void)
{
	return nvm.st.auth != NVM_NONE && !nvm.st.torn && !nvm.full;
}

static void nvm_capture_begin(void)
{
	nvm.cursor = nvm_rec_first();
	nvm.stage_changed = 0;
	/* every change so far is this capture's; a later one opens a window */
	nvm.dirty_armed = 0;
	nvm.retry_armed = 0;
	nvm.cur = &nvm.app;
	nvm.app.programmed = 0;
	nvm.due_us = nvm.now_us;
	nvm.in_append = nvm_can_append();
	nvm.st.phase = NVM_P_CAPTURE;
}

/* 1 when the staged span of r is a frame of r (its crc is then the payload's:
 * the stage holds only proven containers and frames this store wrote). */
static int nvm_framed_as(const uint8_t *rec, struct nvm_rec r)
{
	return rec[0] == (uint8_t)(NVM_REC_MAGIC >> 8) && rec[1] == (uint8_t)NVM_REC_MAGIC &&
	       rec[2] == (uint8_t)NVM3_LAYOUT && rec[3] == 0u &&
	       rec[4] == (uint8_t)(r.id >> 8) && rec[5] == (uint8_t)r.id &&
	       rec[6] == (uint8_t)(r.plen >> 8) && rec[7] == (uint8_t)r.plen;
}

/* Latch one record from its owner into the stage; 1 when a staged byte
 * changed. */
static int nvm_latch(struct nvm_rec r)
{
	const struct nvm_state *s = nvm.state;
	uint8_t *rec = nvm_stage + NVM_KLJ_HDR + r.off;
	int same;
	unsigned int i;

	if (!s->latch(s->ctx, r.group, r.index, nvm_payload, r.plen))
		return 0;               /* nothing to save: the staged bytes stand */
	same = nvm_framed_as(rec, r);
	for (i = 0; i < r.plen; ++i) {
		if (rec[NVM_REC_HDR + i] != nvm_payload[i])
			same = 0;
		rec[NVM_REC_HDR + i] = nvm_payload[i];
	}
	nvm.step_bytes += r.plen;
	if (same)
		return 0;
	nvm_rec_frame(rec, r);
	/* the crc16 runs over the header before its own two bytes, then the
	 * payload (nvm_rec_frame) */
	nvm.step_bytes += (NVM_REC_HDR - 2u) + r.plen;
	nvm.stage_changed = 1;
	return 1;
}

/* The claim heals once nothing changed is left out of a verified slot
 * (FASTCONNECT section 9.2): it clears the state, not just the view. */
static void nvm_heal(void)
{
	if (!nvm_any(&nvm.dirty))
		nvm.st.stale = 0;
}

static void nvm_to_idle(void)
{
	nvm.in_append = 0;
	nvm.force = 0;
	nvm.st.phase = NVM_P_IDLE;
}

/* The next record in flight after r, up to the delta's last. */
static struct nvm_rec nvm_next_in(struct nvm_rec r, unsigned int last)
{
	do
		r = nvm_rec_next(r);
	while (r.ok && r.id <= last && !nvm_bit(&nvm.inflight, r.id));
	if (r.ok && r.id > last)
		r.ok = 0u;
	return r;
}

/* The delta: the records in flight, in ascending id, as many as fit one
 * segment and the log's room. None fits: the log is full, and a compaction
 * carries them. */
static void nvm_delta_begin(void)
{
	struct nvm_seg *s = &nvm.app;
	uint32_t cap = nvm_min(NVM_SEG_MAX, NVM_SLOT_BYTES - nvm.st.log_end);
	uint32_t area = 0;
	struct nvm_rec r;

	s->n_rec = 0;
	for (r = nvm_rec_first(); r.ok; r = nvm_rec_next(r)) {
		if (!nvm_bit(&nvm.inflight, r.id))
			continue;
		if (NVM_KLJ_MIN + ((area + NVM_REC_HDR + r.plen + 3u) & ~3u) > cap)
			break;
		if (!s->n_rec)
			s->rec = r;
		area += NVM_REC_HDR + r.plen;
		s->last = r.id;
		s->n_rec++;
	}
	if (!s->n_rec) {
		nvm.full = 1;
		nvm_to_idle();
		return;
	}
	s->kind = NVM_K_DELTA;
	s->slot = nvm.st.auth;
	s->at = nvm.st.log_end;
	s->len = NVM_KLJ_MIN + ((area + 3u) & ~3u);
	s->pos = 0;
	s->rec_pos = 0;
	s->crc = 0xffffffffu;
	s->seq = nvm.st.seq + 1u;
	nvm.st.phase = NVM_P_ASSEMBLE;
}

/* The capture is over: decide whether its work set is written. */
static void nvm_capture_end(void)
{
	if (nvm.stage_changed) {
		/* a changed staged byte is a new work set: its own attempts */
		nvm.st.attempts = 0;
		nvm.st.exhausted = 0;
	} else if (nvm.st.exhausted) {
		/* DR2c: the unchanged set spent its attempts; a console commit
		 * does not buy a fourth */
		nvm.st.withheld++;
		nvm_to_idle();
		return;
	}
	if (!nvm_any(&nvm.inflight)) {
		if (nvm.force)
			nvm.force_cmp = 1;      /* the console: the whole image again */
		else
			nvm.st.commits_skipped++;       /* DR2b: every value is in a verified slot */
		nvm_heal();
		nvm_to_idle();
		return;
	}
	if (!nvm_can_append()) {
		nvm_to_idle();          /* a compaction carries them */
		return;
	}
	nvm.force = 0;
	nvm_delta_begin();
}

static void nvm_capture_step(void)
{
	struct nvm_rec r = nvm.cursor;

	while (r.ok && !nvm_bit(&nvm.dirty, r.id))
		r = nvm_rec_next(r);
	if (!r.ok) {
		nvm.cursor = r;
		nvm_capture_end();
		return;
	}
	nvm.cursor = nvm_rec_next(r);
	nvm_open_take(&nvm.dirty, r.id);
	if (!nvm_latch(r))
		return;
	nvm_open_set(&nvm.inflight, r.id);
	/* its value in the base is the one before: it goes to the new slot too */
	if (nvm.st.compacting && NVM_KLJ_HDR + r.off < nvm.front)
		nvm_open_set(&nvm.behind, r.id);
}

/* Resume a suspended erase; the erase's own time runs again. */
static void nvm_resume(void)
{
	if (!nvm.suspended)
		return;
	nvm.suspended = 0;
	nvm.erase_from_us = nvm.now_us;
	(void)nvm.flash->resume(nvm.flash->ctx);
}

/* A failed attempt: its records stay in flight, the claim is stale, and the
 * next attempt waits NVM_TXN_BACKOFF_MS (DR2c). The third failure of one
 * work set abandons it, and the reset-sticky record says so. A failed delta
 * whose pages had begun leaves its segment torn: nothing appends past it. A
 * failed compaction leaves part of a base in the other slot, which is
 * prepared again. */
static void nvm_fail(enum nvm_verdict vd)
{
	/* a program may still run: nothing goes to the device until it answers */
	if (nvm.st.phase == NVM_P_PROGRAM || nvm.st.phase == NVM_P_PROGRAM_WAIT)
		nvm.owed = 1;
	/* a suspend not seen to take effect may yet: it is resumed once the
	 * device answers, so the erase runs on */
	if (nvm.st.phase == NVM_P_SUSPEND_WAIT)
		nvm.suspended = 1;
	if (nvm.cur == &nvm.cmp) {
		nvm.st.compacting = 0;
		nvm_prep(nvm.cmp.slot);
	} else if (nvm.app.programmed) {
		nvm.st.torn = 1;
	}
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
	nvm_to_idle();
}

/* A verified write: the authority holds every value it carries. A work set
 * still in flight after it keeps its attempts: a compaction that leaves it
 * to the next delta has not saved it (DR2c). Nothing clears the
 * abandoned-set record. */
static void nvm_done(void)
{
	nvm_resume();
	nvm.st.commits_ok++;
	nvm.st.last_verdict = NVM_VD_OK;
	if (nvm.cur == &nvm.app || !nvm_any(&nvm.inflight)) {
		nvm.st.attempts = 0;
		nvm.st.first_failed = NVM_VD_OK;
	}
	nvm_heal();
	nvm_to_idle();
}

/* The delta is read back: its records are durable, and the log grows. */
static void nvm_delta_done(void)
{
	struct nvm_rec r;

	for (r = nvm_rec_first(); r.ok && r.id <= nvm.app.last; r = nvm_rec_next(r))
		if (nvm_bit(&nvm.inflight, r.id))
			nvm_open_take(&nvm.inflight, r.id);
	nvm.st.seq = nvm.app.seq;
	nvm.st.log_end += NVM_PAGES(nvm.app.len) * NVM_FLASH_PAGE;
	nvm.st.deltas++;
	nvm.st.appends++;
	nvm_done();
}

/* The compaction is complete: the other slot holds the base and every delta
 * the old one took since, so it takes the authority, and the old slot is
 * prepared in its turn. Over an old slot it carries that slot's sequence, so
 * a boot may take either until the next delta, and both hold every value a
 * save reported: a value only the base carries stays in flight for that
 * delta. With no old slot the base's sequence is the first, and what it
 * carries is durable; only a record latched behind its front stays in
 * flight. */
static void nvm_move(void)
{
	int old = nvm.st.auth;
	unsigned int i;

	nvm.st.auth = nvm.cmp.slot;
	nvm.st.log_end = NVM_LOG_START + (old == NVM_NONE ? 0u : nvm.st.log_end - nvm.copy_from);
	nvm.st.torn = 0;
	nvm.st.compacting = 0;
	nvm.full = 0;
	nvm.force_cmp = 0;
	if (old == NVM_NONE) {
		nvm.st.seq = nvm.cmp.seq;
		nvm.inflight.count = 0;
		for (i = 0; i < NVM_WORDS; ++i) {
			uint32_t w = nvm.inflight.bit[i] & nvm.behind.bit[i];

			nvm.inflight.bit[i] = w;
			for (; w; w &= w - 1u)
				nvm.inflight.count++;
		}
	}
	nvm.st.compactions++;
	nvm_prep(!nvm.st.auth);
	nvm_done();
}

static void nvm_cmp_page(void)
{
	nvm.cur = &nvm.cmp;
	nvm.st.phase = NVM_P_ASSEMBLE;
}

/* A compaction into the prepared slot: its base is the stage under the
 * authoritative slot's sequence (the first sequence above none with no
 * slot), taken page by page from the first record. */
static void nvm_cmp_start(void)
{
	struct nvm_seg *s = &nvm.cmp;

	s->kind = NVM_K_BASE;
	s->slot = nvm_target_slot();
	s->at = 0;
	s->len = NVM_IMG_LEN;
	s->pos = 0;
	s->crc = 0xffffffffu;
	s->seq = nvm.st.seq + (nvm.st.auth == NVM_NONE ? 1u : 0u);
	s->rec = nvm_rec_first();
	nvm_klj2_header(nvm_stage, s->seq);
	nvm.front = 0;
	nvm.copy_from = nvm.st.log_end;
	nvm_open_clear(&nvm.behind);
	nvm.st.bg = NVM_B_NONE;
	nvm.st.compacting = 1;
	nvm_cmp_page();
}

/* A compaction is owed: the console asked, the log is torn or full or below
 * its reserve, or there is no authoritative slot and something to save. */
static int nvm_cmp_wanted(void)
{
	if (nvm.force_cmp || nvm.st.torn || nvm.full)
		return 1;
	if (nvm.st.auth == NVM_NONE)
		return nvm_any(&nvm.inflight);
	return NVM_SLOT_BYTES - nvm.st.log_end < NVM_RESERVE;
}

/* ---- the background preparation -------------------------------------------- */

/* A failed preparation starts again from the slot's first page after the
 * backoff, NVM_TXN_ATTEMPTS times in all. */
static void nvm_prep_fail(enum nvm_verdict vd)
{
	nvm.st.prep_failed++;
	nvm.st.prep_vd = vd;
	nvm.prep_pos = 0;
	nvm.prep_erased = 0;
	nvm.prep_at_us = nvm.now_us + NVM_US(NVM_TXN_BACKOFF_MS);
	nvm.st.bg = (++nvm.prep_tries >= NVM_TXN_ATTEMPTS) ? NVM_B_FAILED : NVM_B_CHECK;
}

/* The block the check found written: erased, then read again from its first
 * page; written again after its erase, the preparation fails. */
static void nvm_erase_block(void)
{
	const struct nvm_flash *f = nvm.flash;

	nvm.prep_pos &= ~(NVM_ERASE_BLOCK - 1u);
	if (nvm.prep_erased || f->erase(f->ctx, nvm_slot_addr(nvm.prep_slot) + nvm.prep_pos)) {
		nvm_prep_fail(NVM_VD_ERASE);
		return;
	}
	nvm.prep_erased = 1;
	nvm.erasing = 1;
	nvm.erase_run_us = 0;
	nvm.erase_from_us = nvm.now_us;
	nvm.st.bg = NVM_B_ERASE_WAIT;
}

static void nvm_check_step(void)
{
	const struct nvm_flash *f = nvm.flash;

	if (nvm.now_us < nvm.prep_at_us)
		return;
	/* after a failed erase, nothing is read until the device answers */
	if (nvm.erasing) {
		if (f->busy(f->ctx) != 0)
			return;
		nvm.erasing = 0;
	}
	if (f->read(f->ctx, nvm_slot_addr(nvm.prep_slot) + nvm.prep_pos, nvm_chunk, NVM_STEP_BYTES)) {
		nvm_prep_fail(NVM_VD_ERASE);
		return;
	}
	nvm.step_bytes += NVM_STEP_BYTES;
	if (!nvm_all_erased(nvm_chunk, NVM_STEP_BYTES)) {
		nvm_erase_block();
		return;
	}
	nvm.prep_pos += NVM_STEP_BYTES;
	if (nvm.prep_pos % NVM_ERASE_BLOCK == 0u)
		nvm.prep_erased = 0;
	if (nvm.prep_pos == NVM_SLOT_BYTES) {
		nvm.prep_tries = 0;
		nvm.st.bg = NVM_B_READY;
	}
}

/* The erase's deadline counts only the time it ran, not its suspends. */
static void nvm_erase_wait(void)
{
	const struct nvm_flash *f = nvm.flash;
	int busy = f->busy(f->ctx);

	if (busy == 0) {
		nvm.erasing = 0;
		nvm.st.bg = NVM_B_CHECK;
		return;
	}
	if (busy < 0 || nvm.erase_run_us + (nvm.now_us - nvm.erase_from_us) > NVM_US(MILAN_NVM_ERASE_TIMEOUT_MS))
		nvm_prep_fail(NVM_VD_ERASE);
}

static void nvm_bg_step(void)
{
	if (nvm.st.bg == NVM_B_CHECK)
		nvm_check_step();
	else if (nvm.st.bg == NVM_B_ERASE_WAIT)
		nvm_erase_wait();
}

/* DR2c spaces every attempt NVM_TXN_BACKOFF_MS after a failed one; the
 * first-dirty window starts a capture NVM_WINDOW_MS after the first change
 * it takes; a failed work set is retried while it has attempts left and a
 * delta can go. A save comes before the compaction's next page, and both
 * before the background preparation. */
static void nvm_idle(void)
{
	const struct nvm_flash *f = nvm.flash;
	int wait = nvm.retry_armed && nvm.now_us < nvm.retry_at_us;
	int due;

	/* a failed program may still run, and a failed delta may have left the
	 * erase suspended: nothing goes on while the device reports it busy, and
	 * the erase is resumed then; a device that cannot be asked is not
	 * waited on, and its next operation fails in its turn */
	if (nvm.suspended || nvm.owed) {
		if (f->busy(f->ctx) <= 0) {
			nvm.owed = 0;
			nvm_resume();
		}
		return;
	}
	due = nvm.dirty_armed && nvm_any(&nvm.dirty) &&
	      nvm.now_us - nvm.dirty_since_us >= NVM_US(NVM_WINDOW_MS);
	if (!wait && (due || (nvm_any(&nvm.inflight) && !nvm.st.exhausted && nvm_can_append())))
		nvm_capture_begin();
	else if (nvm.st.compacting)
		nvm_cmp_page();
	else if (!wait && !nvm.st.exhausted && nvm.st.bg == NVM_B_READY && nvm_cmp_wanted())
		nvm_cmp_start();
	else
		nvm_bg_step();
}

/* ---- the page phases ------------------------------------------------------- */

/* A delta's next n bytes into the page: its header first, then the frames of
 * the records in flight from the stage, the pad, and room for the trailer. */
static void nvm_delta_fill(struct nvm_seg *s, uint32_t n)
{
	uint32_t i = 0;

	if (s->pos == 0u) {
		nvm_klj2_seg_header(nvm_page, s->seq, s->n_rec, s->len);
		i = NVM_KLJ_HDR;
	}
	while (i < n) {
		if (s->rec.ok) {
			const uint8_t *src = nvm_stage + NVM_KLJ_HDR + s->rec.off;
			uint32_t span = NVM_REC_HDR + s->rec.plen;
			uint32_t k = nvm_min(span - s->rec_pos, n - i);
			uint32_t j;

			for (j = 0; j < k; ++j)
				nvm_page[i + j] = src[s->rec_pos + j];
			i += k;
			s->rec_pos += k;
			if (s->rec_pos == span) {
				s->rec = nvm_next_in(s->rec, s->last);
				s->rec_pos = 0;
			}
		} else {
			nvm_page[i++] = 0u;
		}
	}
}

/* A base's next n bytes: from the carried record below the front, else from
 * the stage. */
static void nvm_base_fill(const struct nvm_seg *s, uint32_t n)
{
	uint32_t i;

	for (i = 0; i < n; ++i) {
		uint32_t at = s->pos + i;

		nvm_page[i] = (at < nvm.front) ? nvm_carry[at - nvm.carry_at] : nvm_stage[at];
	}
}

static void nvm_assemble_step(void)
{
	const struct nvm_flash *f = nvm.flash;
	struct nvm_seg *s = nvm.cur;

	if (s->kind == NVM_K_COPY) {
		s->page = NVM_FLASH_PAGE;
		if (f->read(f->ctx, nvm_slot_addr(nvm.st.auth) + nvm.copy_from + s->pos, nvm_page,
			    NVM_FLASH_PAGE)) {
			nvm_fail(NVM_VD_VERIFY);
			return;
		}
		nvm.step_bytes += NVM_FLASH_PAGE;
		nvm.st.phase = NVM_P_PROGRAM;
		return;
	}
	s->page = nvm_min(NVM_FLASH_PAGE, s->len - s->pos);
	if (s->kind == NVM_K_DELTA)
		nvm_delta_fill(s, s->page);
	else
		nvm_base_fill(s, s->page);
	nvm.step_bytes += s->page;
	nvm.st.phase = (s->kind == NVM_K_BASE) ? NVM_P_CARRY : NVM_P_SEAL;
}

/* The base's front moves to the page's end; a record the page cuts is
 * copied whole, as it is now, and the front moves to its end. */
static void nvm_carry_step(void)
{
	struct nvm_seg *s = &nvm.cmp;
	uint32_t end = s->pos + s->page;
	struct nvm_rec r = s->rec;
	uint32_t i;

	if (nvm.front < end) {
		while (r.ok && NVM_KLJ_HDR + r.off + NVM_REC_HDR + r.plen <= end)
			r = nvm_rec_next(r);
		s->rec = r;
		nvm.front = end;
		if (r.ok && NVM_KLJ_HDR + r.off < end) {
			nvm.carry_at = end;
			nvm.front = NVM_KLJ_HDR + r.off + NVM_REC_HDR + r.plen;
			for (i = end; i < nvm.front; ++i)
				nvm_carry[i - end] = nvm_stage[i];
			nvm.step_bytes += nvm.front - end;
		}
	}
	nvm.st.phase = NVM_P_SEAL;
}

/* The page's CRC-32 run; the last page carries the trailer, which a base
 * leaves in the stage too. A segment is whole words, so its trailer is in
 * its last page. */
static void nvm_seal_step(void)
{
	struct nvm_seg *s = nvm.cur;
	int last = s->pos + s->page == s->len;

	s->crc = nvm_crc32_update(s->crc, nvm_page, s->page - (last ? NVM_KLJ_TRAILER : 0u));
	nvm.step_bytes += s->page;
	if (last) {
		nvm_wr32le(nvm_page + s->page - NVM_KLJ_TRAILER, ~s->crc);
		if (s->kind == NVM_K_BASE)
			nvm_wr32le(nvm_stage + NVM_IMG_LEN - NVM_KLJ_TRAILER, ~s->crc);
	}
	nvm.st.phase = NVM_P_PROGRAM;
}

/* Where the page in flight goes. */
static uint32_t nvm_page_addr(const struct nvm_seg *s)
{
	return nvm_slot_addr(s->slot) + s->at + s->pos;
}

/* The erase the save meets: ended, nothing to suspend; else suspended, and
 * the suspend timed (decision 5). */
static void nvm_suspend_step(void)
{
	const struct nvm_flash *f = nvm.flash;
	int busy = f->busy(f->ctx);

	if (busy == 0) {
		nvm.erasing = 0;
		nvm.st.phase = NVM_P_PROGRAM;
		return;
	}
	if (busy < 0 || f->suspend(f->ctx)) {
		nvm_fail(NVM_VD_ERASE);
		return;
	}
	nvm.op_start_us = nvm.now_us;
	nvm.st.phase = NVM_P_SUSPEND_WAIT;
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

/* The suspend took effect: its latency is the bound's one typical term, so
 * every one is timed, and one past the room the bound leaves is counted. */
static void nvm_suspend_wait(void)
{
	uint32_t took;

	if (!nvm_wait(NVM_US(NVM_APPEND_TIMEOUT_MS), NVM_VD_ERASE))
		return;
	took = (uint32_t)(nvm.now_us - nvm.op_start_us);
	nvm.suspended = 1;
	nvm.erase_run_us += nvm.op_start_us - nvm.erase_from_us;
	nvm.st.suspends++;
	if (took > nvm.st.suspend_us_max)
		nvm.st.suspend_us_max = took;
	if (took > NVM_SUSPEND_ROOM_US)
		nvm.st.suspend_slow++;
	nvm.st.phase = NVM_P_PROGRAM;
}

static void nvm_program_step(void)
{
	const struct nvm_flash *f = nvm.flash;
	struct nvm_seg *s = nvm.cur;

	if (nvm.erasing && !nvm.suspended) {
		nvm.st.phase = NVM_P_SUSPEND;
		return;
	}
	s->programmed = 1;
	if (f->program(f->ctx, nvm_page_addr(s), nvm_page, s->page)) {
		nvm_fail(NVM_VD_PROGRAM);
		return;
	}
	nvm.step_bytes += s->page;
	nvm.op_start_us = nvm.now_us;
	nvm.st.phase = NVM_P_PROGRAM_WAIT;
}

/* After a compaction page: the base's next, else the old log's next page,
 * else the move. Each page of a compaction yields to a save. */
static void nvm_cmp_next(void)
{
	struct nvm_seg *s = &nvm.cmp;

	if (s->kind == NVM_K_BASE) {
		if (s->pos < s->len) {
			nvm_to_idle();
			return;
		}
		s->kind = NVM_K_COPY;
		s->at = NVM_LOG_START;
		s->pos = 0;
		nvm.front = NVM_IMG_LEN;
	}
	if (nvm.st.auth != NVM_NONE && nvm.copy_from + s->pos < nvm.st.log_end) {
		nvm_to_idle();
		return;
	}
	nvm_move();
}

static void nvm_verify_step(void)
{
	const struct nvm_flash *f = nvm.flash;
	struct nvm_seg *s = nvm.cur;
	uint32_t i;

	if (f->read(f->ctx, nvm_page_addr(s), nvm_chunk, s->page)) {
		nvm_fail(NVM_VD_VERIFY);
		return;
	}
	nvm.step_bytes += s->page;
	for (i = 0; i < s->page; ++i) {
		if (nvm_chunk[i] != nvm_page[i]) {
			nvm_fail(NVM_VD_VERIFY);
			return;
		}
	}
	s->pos += s->page;
	if (s->kind != NVM_K_DELTA)
		nvm_cmp_next();
	else if (s->pos < s->len)
		nvm.st.phase = NVM_P_ASSEMBLE;
	else
		nvm_delta_done();
}

/* The save's deadline (decision 7): past it, the attempt fails, named for
 * the suspend it waited on or the program. */
static int nvm_late(void)
{
	if (!nvm.in_append || nvm.now_us - nvm.due_us <= NVM_US(NVM_APPEND_TIMEOUT_MS))
		return 0;
	nvm_fail(nvm.st.phase == NVM_P_SUSPEND_WAIT ? NVM_VD_ERASE : NVM_VD_PROGRAM);
	return 1;
}

static void nvm_step(void)
{
	if (nvm_late())
		return;
	switch (nvm.st.phase) {
	case NVM_P_IDLE:
		nvm_idle();
		break;
	case NVM_P_CAPTURE:
		nvm_capture_step();
		break;
	case NVM_P_ASSEMBLE:
		nvm_assemble_step();
		break;
	case NVM_P_CARRY:
		nvm_carry_step();
		break;
	case NVM_P_SEAL:
		nvm_seal_step();
		break;
	case NVM_P_SUSPEND:
		nvm_suspend_step();
		break;
	case NVM_P_SUSPEND_WAIT:
		nvm_suspend_wait();
		break;
	case NVM_P_PROGRAM:
		nvm_program_step();
		break;
	case NVM_P_PROGRAM_WAIT:
		if (nvm_wait(NVM_US(MILAN_NVM_PROGRAM_TIMEOUT_MS), NVM_VD_PROGRAM))
			nvm.st.phase = NVM_P_VERIFY;
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
	nvm_open_set(&nvm.dirty, r.id);
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

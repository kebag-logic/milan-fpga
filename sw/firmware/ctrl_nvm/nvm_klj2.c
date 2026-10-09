/* SPDX-License-Identifier: (GPL-2.0 OR MIT) */
/*
 * nvm_klj2.c - the KLJ2 container and F07.8 record codec (#665 lane F1).
 *
 * Ported from the saved-state writer in
 * sw/firmware/milan_baremetal/milan_baremetal.c (nvm_validate, nvm_frame,
 * nvm_rec_after, nvm_write_header, nvm_seal), with one change of substance:
 * a framed record whose payload_length runs past the record area is refused
 * VD_LEN, as scripts/nvm_klj2.py klj2_decode refuses it, where the shipping
 * writer reports VD_REC. Everything else answers rule for rule as both do.
 */
#include "nvm_klj2.h"

/* Every group stays inside its section 4.2 id block, and the blocks keep the
 * ascending order the walk below relies on. */
_Static_assert(MILAN_NVM_N_AUDIO_UNIT >= 1u && MILAN_NVM_N_AUDIO_UNIT <= 8u, "RATE block");
_Static_assert(MILAN_NVM_N_CLK_DOM >= 1u && MILAN_NVM_N_CLK_DOM <= 8u, "CLKSRC and MCR blocks");
_Static_assert(MILAN_NVM_BIND_BASE >= NVM_ID_MCR + 8u &&
	       MILAN_NVM_BIND_BASE + MILAN_NVM_N_STREAM_IN <= NVM_ID_FMTI, "BINDING block");
_Static_assert(MILAN_NVM_N_STREAM_IN <= 16u && MILAN_NVM_N_STREAM_OUT <= 16u, "stream blocks");
_Static_assert(MILAN_NVM_N_SPORT_IN <= 16u && MILAN_NVM_N_SPORT_OUT <= 16u, "map blocks");

struct nvm_block {
	uint8_t base;
	uint8_t count;
	uint16_t plen;    /* 0 for the two map groups: per port */
};

static const uint8_t nvm_mapin_entries[16] = {
	MILAN_NVM_MAPIN_ENTRIES_0, MILAN_NVM_MAPIN_ENTRIES_1, MILAN_NVM_MAPIN_ENTRIES_2,
	MILAN_NVM_MAPIN_ENTRIES_3, MILAN_NVM_MAPIN_ENTRIES_4, MILAN_NVM_MAPIN_ENTRIES_5,
	MILAN_NVM_MAPIN_ENTRIES_6, MILAN_NVM_MAPIN_ENTRIES_7, MILAN_NVM_MAPIN_ENTRIES_8,
	MILAN_NVM_MAPIN_ENTRIES_9, MILAN_NVM_MAPIN_ENTRIES_10, MILAN_NVM_MAPIN_ENTRIES_11,
	MILAN_NVM_MAPIN_ENTRIES_12, MILAN_NVM_MAPIN_ENTRIES_13, MILAN_NVM_MAPIN_ENTRIES_14,
	MILAN_NVM_MAPIN_ENTRIES_15,
};
static const uint8_t nvm_mapout_entries[16] = {
	MILAN_NVM_MAPOUT_ENTRIES_0, MILAN_NVM_MAPOUT_ENTRIES_1, MILAN_NVM_MAPOUT_ENTRIES_2,
	MILAN_NVM_MAPOUT_ENTRIES_3, MILAN_NVM_MAPOUT_ENTRIES_4, MILAN_NVM_MAPOUT_ENTRIES_5,
	MILAN_NVM_MAPOUT_ENTRIES_6, MILAN_NVM_MAPOUT_ENTRIES_7, MILAN_NVM_MAPOUT_ENTRIES_8,
	MILAN_NVM_MAPOUT_ENTRIES_9, MILAN_NVM_MAPOUT_ENTRIES_10, MILAN_NVM_MAPOUT_ENTRIES_11,
	MILAN_NVM_MAPOUT_ENTRIES_12, MILAN_NVM_MAPOUT_ENTRIES_13, MILAN_NVM_MAPOUT_ENTRIES_14,
	MILAN_NVM_MAPOUT_ENTRIES_15,
};
static const struct nvm_block nvm_blocks[NVM_G_COUNT] = {
	{NVM_ID_CFG, 1u, NVM_PL_CFG},
	{NVM_ID_SUID, 1u, NVM_PL_SUID},
	{NVM_ID_RATE, MILAN_NVM_N_AUDIO_UNIT, NVM_PL_RATE},
	{NVM_ID_CLKS, MILAN_NVM_N_CLK_DOM, NVM_PL_CLKS},
	{NVM_ID_MCR, MILAN_NVM_N_CLK_DOM, NVM_PL_MCR},
	{MILAN_NVM_BIND_BASE, MILAN_NVM_N_STREAM_IN, NVM_PL_BIND},
	{NVM_ID_FMTI, MILAN_NVM_N_STREAM_IN, NVM_PL_FMT},
	{NVM_ID_FMTO, MILAN_NVM_N_STREAM_OUT, NVM_PL_FMT},
	{NVM_ID_PTOF, MILAN_NVM_N_STREAM_OUT, NVM_PL_PTOF},
	{NVM_ID_MAPI, MILAN_NVM_N_SPORT_IN, 0u},
	{NVM_ID_MAPO, MILAN_NVM_N_SPORT_OUT, 0u},
	{NVM_ID_NAME, MILAN_NVM_N_NAME, NVM_NAME_BYTES},
};

/* CRC-32/ISO-HDLC (reflected 0xedb88320) and CCITT-FALSE (0x1021), one
 * nibble per table step: 64 and 32 bytes of table, two steps a byte. */
static const uint32_t nvm_crc32_nib[16] = {
	0x00000000u, 0x1db71064u, 0x3b6e20c8u, 0x26d930acu,
	0x76dc4190u, 0x6b6b51f4u, 0x4db26158u, 0x5005713cu,
	0xedb88320u, 0xf00f9344u, 0xd6d6a3e8u, 0xcb61b38cu,
	0x9b64c2b0u, 0x86d3d2d4u, 0xa00ae278u, 0xbdbdf21cu,
};
static const uint16_t nvm_crc16_nib[16] = {
	0x0000u, 0x1021u, 0x2042u, 0x3063u, 0x4084u, 0x50a5u, 0x60c6u, 0x70e7u,
	0x8108u, 0x9129u, 0xa14au, 0xb16bu, 0xc18cu, 0xd1adu, 0xe1ceu, 0xf1efu,
};

uint32_t nvm_crc32_update(uint32_t crc, const uint8_t *p, uint32_t len)
{
	uint32_t i;

	for (i = 0; i < len; ++i) {
		crc ^= p[i];
		crc = (crc >> 4) ^ nvm_crc32_nib[crc & 15u];
		crc = (crc >> 4) ^ nvm_crc32_nib[crc & 15u];
	}
	return crc;
}

uint16_t nvm_crc16_update(uint16_t crc, const uint8_t *p, uint32_t len)
{
	uint32_t i;

	for (i = 0; i < len; ++i) {
		crc = (uint16_t)((crc << 4) ^ nvm_crc16_nib[((crc >> 12) ^ (p[i] >> 4)) & 15u]);
		crc = (uint16_t)((crc << 4) ^ nvm_crc16_nib[((crc >> 12) ^ p[i]) & 15u]);
	}
	return crc;
}

uint32_t nvm_rd32le(const uint8_t *p)
{
	return (uint32_t)p[0] | ((uint32_t)p[1] << 8) |
	       ((uint32_t)p[2] << 16) | ((uint32_t)p[3] << 24);
}

void nvm_wr32le(uint8_t *p, uint32_t v)
{
	p[0] = (uint8_t)v;
	p[1] = (uint8_t)(v >> 8);
	p[2] = (uint8_t)(v >> 16);
	p[3] = (uint8_t)(v >> 24);
}

int nvm_all_erased(const uint8_t *p, uint32_t len)
{
	uint32_t i;

	for (i = 0; i < len; ++i)
		if (p[i] != NVM_ERASED)
			return 0;
	return 1;
}

/* ---- the shape walk ------------------------------------------------------- */
static unsigned int nvm_block_plen(unsigned int g, unsigned int index)
{
	if (g == NVM_G_MAPI)
		return NVM_MAP_ENTRY * nvm_mapin_entries[index & 15u];
	if (g == NVM_G_MAPO)
		return NVM_MAP_ENTRY * nvm_mapout_entries[index & 15u];
	return nvm_blocks[g].plen;
}

/* The record at (group g, index), skipping empty groups, framed at off. */
static struct nvm_rec nvm_rec_at(unsigned int g, unsigned int index, unsigned int off)
{
	struct nvm_rec r = {0u, 0u, 0u, 0u, 0u, 0u};

	while (g < NVM_G_COUNT && index >= nvm_blocks[g].count) {
		g++;
		index = 0;
	}
	if (g >= NVM_G_COUNT)
		return r;
	r.off = (uint16_t)off;
	r.plen = (uint16_t)nvm_block_plen(g, index);
	r.id = (uint8_t)(nvm_blocks[g].base + index);
	r.group = (uint8_t)g;
	r.index = (uint8_t)index;
	r.ok = 1u;
	return r;
}

struct nvm_rec nvm_rec_first(void)
{
	return nvm_rec_at(0u, 0u, 0u);
}

struct nvm_rec nvm_rec_next(struct nvm_rec r)
{
	return nvm_rec_at(r.group, r.index + 1u, r.off + NVM_REC_HDR + r.plen);
}

struct nvm_rec nvm_rec_after(int last)
{
	struct nvm_rec r = nvm_rec_first();

	while (r.ok && (int)r.id <= last)
		r = nvm_rec_next(r);
	return r;
}

struct nvm_rec nvm_rec_by_id(unsigned int id)
{
	struct nvm_rec r = nvm_rec_after((int)id - 1);

	if (r.ok && r.id != id)
		r.ok = 0u;
	return r;
}

struct nvm_rec nvm_rec_of(unsigned int group, unsigned int index)
{
	struct nvm_rec r = {0u, 0u, 0u, 0u, 0u, 0u};

	if (group >= NVM_G_COUNT || index >= nvm_blocks[group].count)
		return r;
	return nvm_rec_by_id(nvm_blocks[group].base + index);
}

int nvm_shape_consistent(void)
{
	struct nvm_rec r = nvm_rec_first();
	unsigned int count = 0;
	unsigned int bytes = 0;
	int last = -1;

	while (r.ok) {
		if ((int)r.id <= last || r.off != bytes || r.plen > NVM_PAYLOAD_MAX)
			return 0;
		last = r.id;
		count++;
		bytes += NVM_REC_HDR + r.plen;
		r = nvm_rec_next(r);
	}
	return count == NVM_N_REC && bytes == NVM_AREA_RAW;
}

/* ---- framing and the container --------------------------------------------- */
void nvm_rec_frame(uint8_t *rec, struct nvm_rec r)
{
	uint16_t crc;

	rec[0] = (uint8_t)(NVM_REC_MAGIC >> 8);
	rec[1] = (uint8_t)NVM_REC_MAGIC;
	rec[2] = (uint8_t)MILAN_NVM_REC_LAYOUT;
	rec[3] = r.id;
	rec[4] = (uint8_t)(r.plen >> 8);
	rec[5] = (uint8_t)r.plen;
	crc = nvm_crc16_update(0xffffu, rec, 6u);
	crc = nvm_crc16_update(crc, rec + NVM_REC_HDR, r.plen);
	rec[6] = (uint8_t)(crc >> 8);
	rec[7] = (uint8_t)crc;
}

void nvm_klj2_header(uint8_t *img, uint32_t seq)
{
	nvm_wr32le(img + 0, NVM_KLJ2_MAGIC);
	nvm_wr32le(img + 4, NVM_KLJ2_FMT_VER);
	nvm_wr32le(img + 8, seq);
	nvm_wr32le(img + 12, NVM_N_REC);
	nvm_wr32le(img + 16, NVM_IMG_LEN);
	nvm_wr32le(img + 20, MILAN_ENTITY_ID_LO);
	nvm_wr32le(img + 24, MILAN_ENTITY_ID_HI);
	nvm_wr32le(img + 28, MILAN_MODEL_ID_LO);
	nvm_wr32le(img + 32, MILAN_MODEL_ID_HI);
	nvm_wr32le(img + 36, MILAN_NVM_REC_LAYOUT);
}

void nvm_klj2_seal(uint8_t *img)
{
	uint32_t crc = nvm_crc32_update(0xffffffffu, img, NVM_IMG_LEN - NVM_KLJ2_TRAILER);

	nvm_wr32le(img + NVM_IMG_LEN - NVM_KLJ2_TRAILER, ~crc);
}

void nvm_klj2_blank(uint8_t *img)
{
	uint32_t i;

	for (i = 0; i < NVM_IMG_LEN; ++i)
		img[i] = NVM_ERASED;
	for (i = 0; i < NVM_PAD_LEN; ++i)
		img[NVM_KLJ2_HDR + NVM_AREA_RAW + i] = 0u;
	nvm_klj2_header(img, 0u);
	nvm_klj2_seal(img);
}

uint32_t nvm_klj2_seq(const uint8_t *img)
{
	return nvm_rd32le(img + 8);
}

/* ---- the section 6.2 acceptance order ---------------------------------------- */
enum nvm_verdict nvm_klj2_check_head(const uint8_t *hdr, uint32_t *img_len)
{
	uint32_t len;

	/* blankness is the header's: an erase clears the whole slot and a
	 * program writes the header page first */
	if (nvm_all_erased(hdr, NVM_KLJ2_HDR))
		return NVM_VD_BLANK;
	if (nvm_rd32le(hdr) != NVM_KLJ2_MAGIC)
		return NVM_VD_MAGIC;
	if ((nvm_rd32le(hdr + 4) >> 16) != (NVM_KLJ2_FMT_VER >> 16))
		return NVM_VD_VER;
	len = nvm_rd32le(hdr + 16);
	if (len < NVM_KLJ2_MIN || len > NVM_KLJ2_MAX)
		return NVM_VD_LEN;
	*img_len = len;
	return NVM_VD_OK;
}

/* One record at pos, framed or erased: its verdict, and on NVM_VD_OK the
 * record it is. `last` is the id of the record before it. */
static enum nvm_verdict nvm_klj2_record(const uint8_t *img, uint32_t pos, uint32_t end,
					uint32_t loaded, int last, struct nvm_rec *out)
{
	const uint8_t *p = img + pos;
	struct nvm_rec r;
	uint32_t plen;
	uint16_t crc;

	if (nvm_all_erased(p, NVM_REC_HDR)) {
		/* the erased-record rule: only the next required record, and
		 * only its whole span erased */
		r = nvm_rec_after(last);
		if (!r.ok)
			return NVM_VD_REC;
		if (pos + NVM_REC_HDR + r.plen > end)
			return NVM_VD_LEN;
		/* The caller may hold only a prefix of the CRC-closed container. */
		if (pos + NVM_REC_HDR + r.plen > loaded)
			return NVM_VD_REC;
		if (!nvm_all_erased(p + NVM_REC_HDR, r.plen))
			return NVM_VD_REC;
		*out = r;
		return NVM_VD_OK;
	}
	if ((((uint32_t)p[0] << 8) | p[1]) != NVM_REC_MAGIC || p[2] != MILAN_NVM_REC_LAYOUT)
		return NVM_VD_REC;
	plen = ((uint32_t)p[4] << 8) | p[5];
	if (pos + NVM_REC_HDR + plen > end)
		return NVM_VD_LEN;
	/* A payload past the loaded bytes cannot be a record of this shape: a
	 * shape record at or before its own offset ends inside the record area
	 * (NVM_STAGE_BYTES), so the crc16 or the length test refuses it VD_REC
	 * either way, and it is refused without reading it. */
	if (pos + NVM_REC_HDR + plen > loaded)
		return NVM_VD_REC;
	crc = nvm_crc16_update(0xffffu, p, 6u);
	crc = nvm_crc16_update(crc, p + NVM_REC_HDR, plen);
	if (crc != ((((uint32_t)p[6]) << 8) | p[7]))
		return NVM_VD_REC;
	if ((int)p[3] <= last)
		return NVM_VD_REC;
	r = nvm_rec_by_id(p[3]);
	if (!r.ok || r.plen != plen)
		return NVM_VD_REC;
	*out = r;
	return NVM_VD_OK;
}

enum nvm_verdict nvm_klj2_check_body(const uint8_t *img, uint32_t img_len, uint32_t loaded)
{
	uint32_t end = img_len - NVM_KLJ2_TRAILER;
	uint32_t nrec = nvm_rd32le(img + 12);
	uint32_t pos = NVM_KLJ2_HDR;
	uint32_t seen = 0;
	uint32_t i;
	int last = -1;

	if (nvm_rd32le(img + 20) != MILAN_ENTITY_ID_LO || nvm_rd32le(img + 24) != MILAN_ENTITY_ID_HI)
		return NVM_VD_ENT;
	if (nvm_rd32le(img + 28) != MILAN_MODEL_ID_LO || nvm_rd32le(img + 32) != MILAN_MODEL_ID_HI)
		return NVM_VD_SHAPE;
	if (nvm_rd32le(img + 36) != MILAN_NVM_REC_LAYOUT)
		return NVM_VD_REC;
	for (i = 0; i < nrec; ++i) {
		struct nvm_rec r;
		enum nvm_verdict vd;

		if (pos + NVM_REC_HDR > end)
			return NVM_VD_LEN;
		/* a loaded prefix that ends short of this header is refused
		 * before it is read (never the store's: see the stage size) */
		if (pos + NVM_REC_HDR > loaded)
			return NVM_VD_REC;
		vd = nvm_klj2_record(img, pos, end, loaded, last, &r);
		if (vd != NVM_VD_OK)
			return vd;
		last = r.id;
		pos += NVM_REC_HDR + r.plen;
		seen++;
	}
	if (pos + ((4u - ((pos - NVM_KLJ2_HDR) & 3u)) & 3u) != end)
		return NVM_VD_LEN;
	if (seen != NVM_N_REC)
		return NVM_VD_INCOMPLETE;
	return NVM_VD_OK;
}

enum nvm_verdict nvm_klj2_check(const uint8_t *img, uint32_t room)
{
	uint32_t img_len = 0;
	enum nvm_verdict vd = nvm_klj2_check_head(img, &img_len);
	uint32_t crc;

	if (vd != NVM_VD_OK)
		return vd;
	if (img_len > room)
		return NVM_VD_LEN;
	crc = nvm_crc32_update(0xffffffffu, img, img_len - NVM_KLJ2_TRAILER);
	if (~crc != nvm_rd32le(img + img_len - NVM_KLJ2_TRAILER))
		return NVM_VD_CRC;
	return nvm_klj2_check_body(img, img_len, img_len);
}

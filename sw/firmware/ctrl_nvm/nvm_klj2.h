/* SPDX-License-Identifier: (GPL-2.0 OR MIT) */
/*
 * nvm_klj2.h - the KLJ2 container and F07.8 record codec of the saved-state
 * store (#665 lane F1), for the shape nvm_shape.h describes.
 *
 * The container is docs/design/SAVED_STATE_FASTCONNECT.md section 6.1 and its
 * acceptance order section 6.2. The reference implementation is
 * scripts/nvm_klj2.py (klj2_assemble, klj2_decode); the host suite requires
 * this codec to produce the same bytes and the same verdict for the same
 * input. The container's header and trailer are little-endian; the records
 * inside are big-endian, because a record is the processor's F07.8 frame
 * verbatim (KL_aecp_nvm_writer.sv, KL_acmp_nvm_shadow.sv).
 */
#ifndef NVM_KLJ2_H
#define NVM_KLJ2_H

#include <stdint.h>

#include "nvm_shape.h"

/* Section 6.2 verdicts, then the writer's three transaction verdicts; the
 * numbering is scripts/nvm_contract.py's and the backend status nibble's. */
enum nvm_verdict {
	NVM_VD_OK = 0,
	NVM_VD_MAGIC = 1,
	NVM_VD_VER = 2,
	NVM_VD_LEN = 3,
	NVM_VD_CRC = 4,
	NVM_VD_ENT = 5,
	NVM_VD_SHAPE = 6,
	NVM_VD_REC = 7,
	NVM_VD_STALE = 8,
	NVM_VD_BLANK = 9,
	NVM_VD_INCOMPLETE = 10,
	NVM_VD_ERASE = 11,
	NVM_VD_PROGRAM = 12,
	NVM_VD_VERIFY = 13,
	NVM_VD_COUNT = 14
};

/* The item groups of section 4.1, in ascending id-block order. */
enum nvm_group {
	NVM_G_CFG = 0,
	NVM_G_SUID = 1,
	NVM_G_RATE = 2,
	NVM_G_CLKS = 3,
	NVM_G_MCR = 4,
	NVM_G_BIND = 5,
	NVM_G_FMTI = 6,
	NVM_G_FMTO = 7,
	NVM_G_PTOF = 8,
	NVM_G_MAPI = 9,
	NVM_G_MAPO = 10,
	NVM_G_NAME = 11,
	NVM_G_COUNT = 12
};

/* One record of the shape, by value; ok is 0 past the last one. */
struct nvm_rec {
	uint16_t off;     /* offset of its frame inside the record area */
	uint16_t plen;    /* payload bytes */
	uint8_t id;       /* record_id */
	uint8_t group;    /* enum nvm_group */
	uint8_t index;    /* index inside the group */
	uint8_t ok;
};

/* The shape's records in ascending id, with their offsets. */
struct nvm_rec nvm_rec_first(void);
struct nvm_rec nvm_rec_next(struct nvm_rec r);
/* The record with this id, or one with ok 0 when the shape has none. */
struct nvm_rec nvm_rec_by_id(unsigned int id);
/* The first record whose id is above last (-1 for the first record). */
struct nvm_rec nvm_rec_after(int last);
/* The record of (group, index), or one with ok 0 when the shape has none. */
struct nvm_rec nvm_rec_of(unsigned int group, unsigned int index);
/* 1 when the walk and the compile-time sizes describe the same set. */
int nvm_shape_consistent(void);

/* CRC-32/ISO-HDLC running state (start 0xffffffff, finish with ~) and the
 * donor's CCITT-FALSE record digest (start 0xffff). */
uint32_t nvm_crc32_update(uint32_t crc, const uint8_t *p, uint32_t len);
uint16_t nvm_crc16_update(uint16_t crc, const uint8_t *p, uint32_t len);

uint32_t nvm_rd32le(const uint8_t *p);
void nvm_wr32le(uint8_t *p, uint32_t v);

/* Frame the record r whose payload is already at rec + NVM_REC_HDR. */
void nvm_rec_frame(uint8_t *rec, struct nvm_rec r);
/* 1 when every one of len bytes is erased (0xff). */
int nvm_all_erased(const uint8_t *p, uint32_t len);

/* The ten header words of section 6.1 for sequence seq. */
void nvm_klj2_header(uint8_t *img, uint32_t seq);
/* The trailer: CRC-32 over every preceding byte of the container. */
void nvm_klj2_seal(uint8_t *img);
/* Blank media behind a valid container: every record erased, the pad zero,
 * sequence 0, sealed. */
void nvm_klj2_blank(uint8_t *img);
/* The sequence word of a container. */
uint32_t nvm_klj2_seq(const uint8_t *img);

/* Rules 1 to 3 (and the blank slot) on the 40 header bytes. Sets *img_len
 * on NVM_VD_OK. */
enum nvm_verdict nvm_klj2_check_head(const uint8_t *hdr, uint32_t *img_len);
/* Rules 6 to 12 on a container whose CRC closed; the first `loaded` bytes
 * of it are at img. */
enum nvm_verdict nvm_klj2_check_body(const uint8_t *img, uint32_t img_len,
				     uint32_t loaded);
/* The whole order over a container held in RAM, `room` bytes of it. */
enum nvm_verdict nvm_klj2_check(const uint8_t *img, uint32_t room);

#endif /* NVM_KLJ2_H */

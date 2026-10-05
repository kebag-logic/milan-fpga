/* SPDX-License-Identifier: (GPL-2.0 OR MIT) */
/*
 * nvm_shape.h - the saved-state record set of one entity shape, sized at
 * build time (#665 lane F1).
 *
 * Every number here is derived from the generated constants the builder
 * publishes for the shape (MILAN_NVM_* from scripts/nvm_shape.py
 * firmware_constants(), the identity words and the journal map), the same
 * derivation sw/firmware/milan_baremetal/milan_baremetal.c compiles against.
 * The build supplies them through nvm_shape_gen.h: on the target the one in
 * plat/ includes <generated/soc.h>; on the host the test driver writes one
 * per shipped shape. Nothing below is a run-time quantity, so every buffer
 * the store owns is a static array of a constant size and there is no heap.
 *
 * The allocation is docs/design/SAVED_STATE_FASTCONNECT.md section 4.2 (one
 * record per item group and index, the donor's F07.8 rule) and the container
 * is section 6.1 (KLJ2).
 */
#ifndef NVM_SHAPE_H
#define NVM_SHAPE_H

#include <stdint.h>

#include "nvm_shape_gen.h"

/* KLJ2, section 6.1: a 40-byte little-endian header, the record area, the
 * CRC-32 trailer. */
#define NVM_KLJ2_MAGIC   0x324a4c4bu
#define NVM_KLJ2_FMT_VER 0x00020000u
#define NVM_KLJ2_HDR     40u
#define NVM_KLJ2_TRAILER 4u
#define NVM_KLJ2_MIN     (NVM_KLJ2_HDR + NVM_KLJ2_TRAILER)
#define NVM_KLJ2_MAX     65536u

/* F07.8: {magic 0x1722, layout_version, record_id, payload_length, crc16},
 * big-endian, then the payload. */
#define NVM_REC_HDR    8u
#define NVM_REC_MAGIC  0x1722u
#define NVM_ERASED     0xffu
#define NVM_NAME_BYTES 64u
#define NVM_MAP_ENTRY  8u

/* The section 4.2 id blocks; the BINDING base is the donor's, generated. */
#define NVM_ID_CFG  0x00u
#define NVM_ID_SUID 0x01u
#define NVM_ID_RATE 0x02u
#define NVM_ID_CLKS 0x0au
#define NVM_ID_MCR  0x12u
#define NVM_ID_FMTI 0x30u
#define NVM_ID_FMTO 0x40u
#define NVM_ID_PTOF 0x50u
#define NVM_ID_MAPI 0x60u
#define NVM_ID_MAPO 0x70u
#define NVM_ID_NAME 0x80u
#define NVM_ID_SPACE 256u

/* Fixed payload lengths, section 4.1. */
#define NVM_PL_CFG  2u
#define NVM_PL_SUID 8u
#define NVM_PL_RATE 4u
#define NVM_PL_CLKS 2u
#define NVM_PL_MCR  66u
#define NVM_PL_BIND 20u
#define NVM_PL_FMT  8u
#define NVM_PL_PTOF 4u

#define NVM_MAX(a, b) (((a) > (b)) ? (a) : (b))
#define NVM_SZ(plen) (NVM_REC_HDR + (plen))
#define NVM_PORT_SZ(k, n, cl) (((k) < (n)) ? NVM_SZ(NVM_MAP_ENTRY * (cl)) : 0u)
#define NVM_PORT_CL(k, n, cl) (((k) < (n)) ? (cl) : 0u)

/* The input and output channel-map records, port by port (sixteen ports per
 * direction is the backend's table, scripts/nvm_shape.py FW_MAP_PORTS; an
 * absent port carries zero entries). */
#define NVM_MAPI_SZ(k) NVM_PORT_SZ(k, MILAN_NVM_N_SPORT_IN, MILAN_NVM_MAPIN_ENTRIES_##k)
#define NVM_MAPO_SZ(k) NVM_PORT_SZ(k, MILAN_NVM_N_SPORT_OUT, MILAN_NVM_MAPOUT_ENTRIES_##k)
#define NVM_MAPI_CL(k) NVM_PORT_CL(k, MILAN_NVM_N_SPORT_IN, MILAN_NVM_MAPIN_ENTRIES_##k)
#define NVM_MAPO_CL(k) NVM_PORT_CL(k, MILAN_NVM_N_SPORT_OUT, MILAN_NVM_MAPOUT_ENTRIES_##k)
#define NVM_SUM16(F) \
	(F(0) + F(1) + F(2) + F(3) + F(4) + F(5) + F(6) + F(7) + \
	 F(8) + F(9) + F(10) + F(11) + F(12) + F(13) + F(14) + F(15))
#define NVM_MAX16(F) \
	NVM_MAX(NVM_MAX(NVM_MAX(NVM_MAX(F(0), F(1)), NVM_MAX(F(2), F(3))), \
			NVM_MAX(NVM_MAX(F(4), F(5)), NVM_MAX(F(6), F(7)))), \
		NVM_MAX(NVM_MAX(NVM_MAX(F(8), F(9)), NVM_MAX(F(10), F(11))), \
			NVM_MAX(NVM_MAX(F(12), F(13)), NVM_MAX(F(14), F(15)))))
#define NVM_MAPI_BYTES NVM_SUM16(NVM_MAPI_SZ)
#define NVM_MAPO_BYTES NVM_SUM16(NVM_MAPO_SZ)

#define NVM_FIXED_BYTES \
	(NVM_SZ(NVM_PL_CFG) + NVM_SZ(NVM_PL_SUID) + \
	 MILAN_NVM_N_AUDIO_UNIT * NVM_SZ(NVM_PL_RATE) + \
	 MILAN_NVM_N_CLK_DOM * (NVM_SZ(NVM_PL_CLKS) + NVM_SZ(NVM_PL_MCR)) + \
	 MILAN_NVM_N_STREAM_IN * (NVM_SZ(NVM_PL_BIND) + NVM_SZ(NVM_PL_FMT)) + \
	 MILAN_NVM_N_STREAM_OUT * (NVM_SZ(NVM_PL_FMT) + NVM_SZ(NVM_PL_PTOF)))

/* The record area: every record of the shape, framed or erased, in ascending
 * id with no padding between them, then zero padding to a word. */
#define NVM_AREA_RAW (NVM_FIXED_BYTES + NVM_MAPI_BYTES + NVM_MAPO_BYTES + \
		      MILAN_NVM_N_NAME * NVM_SZ(NVM_NAME_BYTES))
#define NVM_AREA_LEN ((NVM_AREA_RAW + 3u) & ~3u)
#define NVM_PAD_LEN  (NVM_AREA_LEN - NVM_AREA_RAW)
/* The container: the whole slot image, header to trailer. */
#define NVM_IMG_LEN  (NVM_KLJ2_HDR + NVM_AREA_LEN + NVM_KLJ2_TRAILER)
#define NVM_N_REC    (2u + MILAN_NVM_N_AUDIO_UNIT + 2u * MILAN_NVM_N_CLK_DOM + \
		      2u * MILAN_NVM_N_STREAM_IN + 2u * MILAN_NVM_N_STREAM_OUT + \
		      MILAN_NVM_N_SPORT_IN + MILAN_NVM_N_SPORT_OUT + MILAN_NVM_N_NAME)

/* The largest payload of the shape: the buffer one latched record passes
 * through, and the size that bounds one capture step. */
#define NVM_PAYLOAD_MAX \
	NVM_MAX(NVM_MAX(NVM_PL_MCR, NVM_NAME_BYTES), \
		NVM_MAP_ENTRY * NVM_MAX(NVM_MAX16(NVM_MAPI_CL), NVM_MAX16(NVM_MAPO_CL)))

/* The stage: the container plus one record header of look-ahead, so the
 * section 6.2 walk over a slot whose IMG_LEN exceeds this shape's can read
 * the header after the last record of the shape (nvm_klj2.c). */
#define NVM_STAGE_BYTES (NVM_IMG_LEN + NVM_REC_HDR)

/* The media: two slots, one erase block each, section 5. */
#define NVM_SLOT_BYTES  (MILAN_FLASH_JOURNAL_SIZE / 2u)
#define NVM_SLOT_A      MILAN_FLASH_JOURNAL_OFFSET
#define NVM_SLOT_B      (MILAN_FLASH_JOURNAL_OFFSET + NVM_SLOT_BYTES)
#define NVM_FLASH_PAGE  256u

/* The identity a container is bound to, section 6.1 words 5 to 8. */
#define NVM_ENTITY_ID \
	(((uint64_t)MILAN_ENTITY_ID_HI << 32) | (uint64_t)MILAN_ENTITY_ID_LO)
#define NVM_MODEL_ID \
	(((uint64_t)MILAN_MODEL_ID_HI << 32) | (uint64_t)MILAN_MODEL_ID_LO)

_Static_assert(NVM_N_REC <= NVM_ID_SPACE, "the record set outgrows record_id[7:0]");
_Static_assert(MILAN_NVM_N_NAME <= 128u, "the names outgrow their id block");
_Static_assert(NVM_IMG_LEN <= NVM_SLOT_BYTES, "the container outgrows one slot");
_Static_assert(NVM_IMG_LEN <= NVM_KLJ2_MAX, "the container outgrows IMG_LEN");
_Static_assert(NVM_SLOT_BYTES == 65536u, "a slot is one 64 KiB erase block");
_Static_assert((NVM_SLOT_A % NVM_SLOT_BYTES) == 0u, "slot A is not block aligned");

#endif /* NVM_SHAPE_H */

/* SPDX-License-Identifier: (GPL-2.0 OR MIT) */
/*
 * nvm_shape.h - the saved-state record set of one entity shape, sized at
 * build time (#665 lane F1), in the split placement's format (#823).
 *
 * THE FORMAT is the split placement's: the KLJ3 container in the 640 KiB
 * journal_klj3, its records framed by F07.8 layout 3 over the record space of
 * nvm_layout3.h (#823 decisions 1 and 2, docs/design/SAVED_STATE_FORMAT_32X32.md
 * sections 2, 3 and 5). The all-fabric placement keeps KLJ2 and layout 2 in
 * today's journal (milan_baremetal.c, KL_nvm_backend.sv). This store never
 * writes that journal; it reads its two headers at boot, and a KLJ2
 * container anywhere is refused VD_VER (nvm_store.c, "the previous format").
 *
 * THE SHAPE is the generated MILAN_NVM3_* constants: the builder's split
 * output (nvm_split.json, sw/builder/endstation_builder.py emit_nvm_split)
 * as scripts/nvm_klj3.py split_constants() publishes it, with every port's
 * map entries; the identity words and the two journals' places come with
 * them. The build supplies them through nvm_shape_gen.h: on the target the
 * one in plat/ includes <generated/soc.h>; on the host the test driver writes
 * one per shipped shape. Nothing below is a run-time quantity, so every
 * buffer the store owns is a static array of a constant size and there is no
 * heap.
 *
 * The allocation is one record per item group and index, the donor's F07.8
 * rule (docs/design/SAVED_STATE_FASTCONNECT.md section 4.2), and the
 * container is section 6.1 with KLJ3's magic and major version.
 */
#ifndef NVM_SHAPE_H
#define NVM_SHAPE_H

#include <stdint.h>

#include "nvm_layout3.h"
#include "nvm_shape_gen.h"

/* The container, section 6.1: a 40-byte little-endian header, the record
 * area, the CRC-32 trailer. KLJ3 and KLJ2 share the geometry. */
#define NVM_KLJ3_MAGIC   0x334a4c4bu
#define NVM_KLJ3_FMT_VER 0x00030000u
#define NVM_KLJ_HDR      40u
#define NVM_KLJ_TRAILER  4u
#define NVM_KLJ_MIN      (NVM_KLJ_HDR + NVM_KLJ_TRAILER)
/* The previous format, recognised so that it is refused VD_VER and never
 * reinterpreted (#823 decision 2). */
#define NVM_KLJ2_MAGIC   0x324a4c4bu

/* F07.8 layout 3: {magic 0x1722, layout_version, reserved 0, record_id,
 * payload_length, crc16}, big-endian, then the payload. */
#define NVM_REC_HDR    NVM3_REC_HDR
#define NVM_REC_MAGIC  0x1722u
#define NVM_ERASED     0xffu
#define NVM_NAME_BYTES 64u
#define NVM_MAP_ENTRY  8u

/* The layout 3 blocks (nvm_layout3.h). */
#define NVM_ID_CFG   NVM3_ID_CFG
#define NVM_ID_SUID  NVM3_ID_SUID
#define NVM_ID_RATE  NVM3_ID_RATE
#define NVM_ID_CLKS  NVM3_ID_CLKS
#define NVM_ID_MCR   NVM3_ID_MCR
#define NVM_ID_BIND  NVM3_ID_BIND
#define NVM_ID_FMTI  NVM3_ID_FMTI
#define NVM_ID_FMTO  NVM3_ID_FMTO
#define NVM_ID_PTOF  NVM3_ID_PTOF
#define NVM_ID_MAPI  NVM3_ID_MAPI
#define NVM_ID_MAPO  NVM3_ID_MAPO
#define NVM_ID_NAME  NVM3_ID_NAME
#define NVM_ID_SPACE NVM3_ID_SPACE
/* The channel-map ports a table holds, per direction: the MAPS blocks. */
#define NVM_MAP_PORTS 32u

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

/* The input and output channel-map records, port by port (an absent port
 * carries zero entries). */
#define NVM_MAPI_SZ(k) NVM_PORT_SZ(k, MILAN_NVM3_N_SPORT_IN, MILAN_NVM3_MAPIN_ENTRIES_##k)
#define NVM_MAPO_SZ(k) NVM_PORT_SZ(k, MILAN_NVM3_N_SPORT_OUT, MILAN_NVM3_MAPOUT_ENTRIES_##k)
#define NVM_MAPI_CL(k) NVM_PORT_CL(k, MILAN_NVM3_N_SPORT_IN, MILAN_NVM3_MAPIN_ENTRIES_##k)
#define NVM_MAPO_CL(k) NVM_PORT_CL(k, MILAN_NVM3_N_SPORT_OUT, MILAN_NVM3_MAPOUT_ENTRIES_##k)
#define NVM_SUM8(F, a, b, c, d, e, f, g, h) \
	(F(a) + F(b) + F(c) + F(d) + F(e) + F(f) + F(g) + F(h))
#define NVM_SUM32(F) \
	(NVM_SUM8(F, 0, 1, 2, 3, 4, 5, 6, 7) + NVM_SUM8(F, 8, 9, 10, 11, 12, 13, 14, 15) + \
	 NVM_SUM8(F, 16, 17, 18, 19, 20, 21, 22, 23) + NVM_SUM8(F, 24, 25, 26, 27, 28, 29, 30, 31))
#define NVM_MAX8(F, a, b, c, d, e, f, g, h) \
	NVM_MAX(NVM_MAX(NVM_MAX(F(a), F(b)), NVM_MAX(F(c), F(d))), \
		NVM_MAX(NVM_MAX(F(e), F(f)), NVM_MAX(F(g), F(h))))
#define NVM_MAX32(F) \
	NVM_MAX(NVM_MAX(NVM_MAX8(F, 0, 1, 2, 3, 4, 5, 6, 7), NVM_MAX8(F, 8, 9, 10, 11, 12, 13, 14, 15)), \
		NVM_MAX(NVM_MAX8(F, 16, 17, 18, 19, 20, 21, 22, 23), NVM_MAX8(F, 24, 25, 26, 27, 28, 29, 30, 31)))
#define NVM_MAPI_BYTES NVM_SUM32(NVM_MAPI_SZ)
#define NVM_MAPO_BYTES NVM_SUM32(NVM_MAPO_SZ)

#define NVM_FIXED_BYTES \
	(NVM_SZ(NVM_PL_CFG) + NVM_SZ(NVM_PL_SUID) + \
	 MILAN_NVM3_N_AUDIO_UNIT * NVM_SZ(NVM_PL_RATE) + \
	 MILAN_NVM3_N_CLK_DOM * (NVM_SZ(NVM_PL_CLKS) + NVM_SZ(NVM_PL_MCR)) + \
	 MILAN_NVM3_N_STREAM_IN * (NVM_SZ(NVM_PL_BIND) + NVM_SZ(NVM_PL_FMT)) + \
	 MILAN_NVM3_N_STREAM_OUT * (NVM_SZ(NVM_PL_FMT) + NVM_SZ(NVM_PL_PTOF)))

/* The record area: every record of the shape, framed or erased, in ascending
 * id with no padding between them, then zero padding to a word. */
#define NVM_AREA_RAW (NVM_FIXED_BYTES + NVM_MAPI_BYTES + NVM_MAPO_BYTES + \
		      MILAN_NVM3_N_NAME * NVM_SZ(NVM_NAME_BYTES))
#define NVM_AREA_LEN ((NVM_AREA_RAW + 3u) & ~3u)
#define NVM_PAD_LEN  (NVM_AREA_LEN - NVM_AREA_RAW)
/* The container: the whole slot image, header to trailer. */
#define NVM_IMG_LEN  (NVM_KLJ_HDR + NVM_AREA_LEN + NVM_KLJ_TRAILER)
#define NVM_N_REC    (2u + MILAN_NVM3_N_AUDIO_UNIT + 2u * MILAN_NVM3_N_CLK_DOM + \
		      2u * MILAN_NVM3_N_STREAM_IN + 2u * MILAN_NVM3_N_STREAM_OUT + \
		      MILAN_NVM3_N_SPORT_IN + MILAN_NVM3_N_SPORT_OUT + MILAN_NVM3_N_NAME)

/* The largest payload of the shape: the buffer one latched record passes
 * through, and the size that bounds one capture step. */
#define NVM_PAYLOAD_MAX \
	NVM_MAX(NVM_MAX(NVM_PL_MCR, NVM_NAME_BYTES), \
		NVM_MAP_ENTRY * NVM_MAX(NVM_MAX32(NVM_MAPI_CL), NVM_MAX32(NVM_MAPO_CL)))

/* The stage: the container plus one record header of look-ahead, so the
 * section 6.2 walk over a slot whose IMG_LEN exceeds this shape's can read
 * the header after the last record of the shape (nvm_klj2.c). */
#define NVM_STAGE_BYTES (NVM_IMG_LEN + NVM_REC_HDR)

/* The media: journal_klj3, two slots of whole erase blocks (section 5). A
 * commit erases the blocks its container spans, from the slot's first. */
#define NVM_JOURNAL_OFFSET MILAN_FLASH_JOURNAL_KLJ3_OFFSET
#define NVM_JOURNAL_SIZE   MILAN_FLASH_JOURNAL_KLJ3_SIZE
#define NVM_SLOT_BYTES     (NVM_JOURNAL_SIZE / 2u)
#define NVM_SLOT_A         NVM_JOURNAL_OFFSET
#define NVM_SLOT_B         (NVM_JOURNAL_OFFSET + NVM_SLOT_BYTES)
#define NVM_FLASH_PAGE     256u
#define NVM_ERASE_BLOCK    65536u
#define NVM_ERASE_BLOCKS   ((NVM_IMG_LEN + NVM_ERASE_BLOCK - 1u) / NVM_ERASE_BLOCK)
/* KLJ3 rule 3: a container is never longer than its slot. */
#define NVM_KLJ3_MAX       NVM_SLOT_BYTES
/* Today's journal, the all-fabric placement's KLJ2: read, never written. */
#define NVM_LEGACY_A       MILAN_FLASH_JOURNAL_OFFSET
#define NVM_LEGACY_B       (MILAN_FLASH_JOURNAL_OFFSET + MILAN_FLASH_JOURNAL_SIZE / 2u)

/* The identity a container is bound to, section 6.1 words 5 to 8. */
#define NVM_ENTITY_ID \
	(((uint64_t)MILAN_ENTITY_ID_HI << 32) | (uint64_t)MILAN_ENTITY_ID_LO)
#define NVM_MODEL_ID \
	(((uint64_t)MILAN_MODEL_ID_HI << 32) | (uint64_t)MILAN_MODEL_ID_LO)

/* The compile-time refusals: each group inside its layout 3 block, the same
 * capacities the builder's split output refuses above (#823 decision 1). */
_Static_assert(MILAN_NVM3_N_AUDIO_UNIT >= 1u && MILAN_NVM3_N_AUDIO_UNIT <= NVM3_CAP_RATE, "RATE block");
_Static_assert(MILAN_NVM3_N_CLK_DOM >= 1u && MILAN_NVM3_N_CLK_DOM <= NVM3_CAP_CLKS &&
	       MILAN_NVM3_N_CLK_DOM <= NVM3_CAP_MCR, "CLKSRC and MCR blocks");
_Static_assert(MILAN_NVM3_N_STREAM_IN <= NVM3_CAP_BIND && MILAN_NVM3_N_STREAM_IN <= NVM3_CAP_FMTI,
	       "BINDING and FMT_IN blocks");
_Static_assert(MILAN_NVM3_N_STREAM_OUT <= NVM3_CAP_FMTO && MILAN_NVM3_N_STREAM_OUT <= NVM3_CAP_PTOF,
	       "FMT_OUT and PT_OFS blocks");
_Static_assert(MILAN_NVM3_N_SPORT_IN <= NVM3_CAP_MAPI && MILAN_NVM3_N_SPORT_OUT <= NVM3_CAP_MAPO &&
	       NVM3_CAP_MAPI <= NVM_MAP_PORTS && NVM3_CAP_MAPO <= NVM_MAP_PORTS, "map blocks");
_Static_assert(MILAN_NVM3_N_NAME <= NVM3_CAP_NAME, "the names outgrow their id block");
_Static_assert(NVM_ID_SPACE <= 65536u, "the record space outgrows record_id[15:0]");
_Static_assert(NVM_N_REC <= NVM_ID_SPACE, "the record set outgrows the record space");
_Static_assert(NVM_IMG_LEN <= NVM_SLOT_BYTES, "the container outgrows one slot");
_Static_assert(NVM_SLOT_BYTES % NVM_ERASE_BLOCK == 0u, "a slot is whole erase blocks");
_Static_assert((NVM_SLOT_A % NVM_ERASE_BLOCK) == 0u, "slot A is not block aligned");
_Static_assert(NVM_SLOT_B + NVM_SLOT_BYTES <= NVM_LEGACY_A || NVM_SLOT_A >= NVM_LEGACY_A + MILAN_FLASH_JOURNAL_SIZE,
	       "the KLJ3 journal overlaps the KLJ2 journal");

#endif /* NVM_SHAPE_H */

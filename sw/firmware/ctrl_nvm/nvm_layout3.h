/* SPDX-License-Identifier: (GPL-2.0 OR MIT) */
/*
 * nvm_layout3.h - the record space of saved-state layout 3, the split
 * placement's (#823 decision 1).
 *
 * THE ONE DECLARATION. Each NVM3_CAP_* line is a block's capacity: the count
 * of its group in the bound shape, 32x32 streams with two interfaces and the
 * TDM8 cluster model (docs/design/SAVED_STATE_FORMAT_32X32.md section 2).
 * RATE, CLKSRC and MCR keep the bound of 8 the all-fabric backend refuses
 * above. The blocks follow in the order of section 4.2 of
 * docs/design/SAVED_STATE_FASTCONNECT.md, and each base is the sum of the
 * capacities before it, so a record's id is the same constant at every shape.
 *
 * Two readers take the capacities from here, and nothing restates them:
 *   - the split placement's saved-state store's codec (nvm_shape.h and
 *     nvm_klj2.c), which refuses at compile time a count over its block;
 *   - the builder's split output (sw/builder/endstation_builder.py,
 *     emit_nvm_split), through scripts/nvm_layout3.py, which reads each
 *     NVM3_CAP_* line and refuses a header with none or two of one.
 * scripts/check_nvm_format_32x32.py fails when a capacity is not the bound
 * shape's count as the builder builds it.
 *
 * The all-fabric placement keeps layout 2 and its 8-bit record_id
 * (KL_nvm_backend.sv, milan_baremetal.c); nothing there reads this file.
 */
#ifndef NVM_LAYOUT3_H
#define NVM_LAYOUT3_H

/* F07.8 layout 3: {magic 0x1722, layout_version 3, reserved 0, record_id,
 * payload_length, crc16}, big-endian, ten bytes, then the payload. */
#define NVM3_LAYOUT  3u
#define NVM3_REC_HDR 10u

/* The capacities, block by block. */
#define NVM3_CAP_CFG  1u
#define NVM3_CAP_SUID 1u
#define NVM3_CAP_RATE 8u
#define NVM3_CAP_CLKS 8u
#define NVM3_CAP_MCR  8u
#define NVM3_CAP_BIND 33u
#define NVM3_CAP_FMTI 33u
#define NVM3_CAP_FMTO 33u
#define NVM3_CAP_PTOF 33u
#define NVM3_CAP_MAPI 32u
#define NVM3_CAP_MAPO 32u
#define NVM3_CAP_NAME 907u

/* The bases: each block directly after the one before it. */
#define NVM3_ID_CFG  0u
#define NVM3_ID_SUID (NVM3_ID_CFG + NVM3_CAP_CFG)
#define NVM3_ID_RATE (NVM3_ID_SUID + NVM3_CAP_SUID)
#define NVM3_ID_CLKS (NVM3_ID_RATE + NVM3_CAP_RATE)
#define NVM3_ID_MCR  (NVM3_ID_CLKS + NVM3_CAP_CLKS)
#define NVM3_ID_BIND (NVM3_ID_MCR + NVM3_CAP_MCR)
#define NVM3_ID_FMTI (NVM3_ID_BIND + NVM3_CAP_BIND)
#define NVM3_ID_FMTO (NVM3_ID_FMTI + NVM3_CAP_FMTI)
#define NVM3_ID_PTOF (NVM3_ID_FMTO + NVM3_CAP_FMTO)
#define NVM3_ID_MAPI (NVM3_ID_PTOF + NVM3_CAP_PTOF)
#define NVM3_ID_MAPO (NVM3_ID_MAPI + NVM3_CAP_MAPI)
#define NVM3_ID_NAME (NVM3_ID_MAPO + NVM3_CAP_MAPO)
/* Every id is below this; a record_id field of 16 bits carries it. */
#define NVM3_ID_SPACE (NVM3_ID_NAME + NVM3_CAP_NAME)

#endif /* NVM_LAYOUT3_H */

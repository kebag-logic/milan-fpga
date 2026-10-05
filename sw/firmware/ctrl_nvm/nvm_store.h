/* SPDX-License-Identifier: (GPL-2.0 OR MIT) */
/*
 * nvm_store.h - the bare-metal saved-state store (#665 lane F1): the boot
 * restore and the write-back of docs/design/SAVED_STATE_FASTCONNECT.md
 * sections 6 and 7, under the D3 restore transaction of
 * docs/design/SAVED_STATE_MATERIALIZATION.md section 8.
 *
 * One store per image, held in static storage sized by nvm_shape.h; there is
 * no heap and no OS service. The event loop calls nvm_store_service() on
 * every iteration; each call does one bounded step and returns.
 */
#ifndef NVM_STORE_H
#define NVM_STORE_H

#include <stdint.h>

#include "nvm_flash.h"
#include "nvm_klj2.h"
#include "nvm_state.h"

/* How the boot restore ended (section 8.6 and 6.2 of the D3 page). */
enum nvm_terminal {
	NVM_T_NONE = 0,
	NVM_T_COMPLETE = 1,  /* an accepted slot, every record applied or refused */
	NVM_T_BLANK = 2,     /* no slot accepted: the entity runs on its defaults */
	NVM_T_DEFAULTS = 3,  /* aborted and rolled back to the image defaults */
	NVM_T_CLOSED = 4     /* the model is unproven or the roll-back failed */
};

/* The first cause of an abort. */
enum nvm_cause {
	NVM_C_NONE = 0,
	NVM_C_APPLY = 1,     /* a value rule could not be judged */
	NVM_C_SETTLE = 2,    /* the formats-against-maps judgement could not be */
	NVM_C_MODEL = 3,     /* the entity model is not proven */
	NVM_C_SHAPE = 4,     /* the record walk and the build disagree */
	NVM_C_STAGE = 5      /* the chosen slot did not read back as accepted */
};

/* The write path's phase; each service call advances at most one. */
enum nvm_phase {
	NVM_P_OFF = 0,       /* no writer: before boot, or retired */
	NVM_P_IDLE = 1,
	NVM_P_CAPTURE = 2,   /* latch the dirty records, one per step */
	NVM_P_SEAL = 3,      /* header and CRC-32, NVM_STEP_BYTES per step */
	NVM_P_ERASE = 4,     /* start the erase of the slot that is not authoritative */
	NVM_P_ERASE_WAIT = 5,
	NVM_P_BLANKCHECK = 6,
	NVM_P_PROGRAM = 7,   /* start one page program */
	NVM_P_PROGRAM_WAIT = 8,
	NVM_P_VERIFY = 9     /* read back and compare */
};

/* Bytes one service step may touch, besides one latched record. */
#define NVM_STEP_BYTES NVM_FLASH_PAGE
/* The most bytes any service step touches: one 256-byte stretch, or one
 * latched record's copy and its crc16 over the header and the payload. */
#define NVM_STEP_BOUND NVM_MAX(NVM_STEP_BYTES, 2u * NVM_PAYLOAD_MAX + 6u)
/* DR2c: firmware transaction attempts per unchanged work set, and their
 * separation (SAVED_STATE_MATERIALIZATION.md section 15.1). */
#define NVM_TXN_ATTEMPTS 3u
#define NVM_TXN_BACKOFF_MS 1000u

struct nvm_status {
	enum nvm_verdict verdict_a;
	enum nvm_verdict verdict_b;
	enum nvm_verdict last_verdict;  /* the boot's offer, then each commit's */
	enum nvm_verdict first_failed;  /* the first failed attempt's since a success */
	uint32_t seq_a;
	uint32_t seq_b;
	uint32_t seq;                   /* the authoritative container's */
	int auth;                       /* 0 slot A, 1 slot B, -1 none */
	enum nvm_terminal terminal;
	enum nvm_cause cause;
	unsigned int applied;
	unsigned int refused;
	unsigned int blank;
	unsigned int releases;
	unsigned int commits_ok;
	unsigned int commits_failed;
	unsigned int commits_skipped;   /* DR2b: nothing the capture saw changed */
	unsigned int attempts;          /* failed attempts on this work set */
	int exhausted;
	int stale;                      /* a failed commit left work out of every slot */
	int dirty;                      /* changed records not yet captured */
	int pending;                    /* captured records not yet in a verified slot */
	enum nvm_phase phase;
	uint32_t step_bytes_max;        /* the most bytes one service step touched */
	uint32_t steps;
};

/* Boot: judge both slots, stage the newer accepted one, apply it through
 * `state` as one transaction, release AECP unless CLOSED, arm the writer. */
void nvm_store_boot(const struct nvm_flash *flash, const struct nvm_state *state);
/* One bounded step of the write path. */
void nvm_store_service(void);
/* An accepted command changed the persisted value of (group, index). */
void nvm_store_changed(unsigned int group, unsigned int index);
/* Start a commit now, without the debounce (the console); 1 when started. */
int nvm_store_commit_now(void);
const struct nvm_status *nvm_store_status(void);
/* The stage, NVM_IMG_LEN bytes: the last verified container, or the one a
 * commit in flight is writing. */
const uint8_t *nvm_store_stage(void);

#endif /* NVM_STORE_H */

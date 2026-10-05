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

/* How a walk of the boot restore ended (sections 8.6 and 6.2 of the D3
 * page). The binding walk's DEFAULTS is its whole failure, nothing
 * preloaded. */
enum nvm_terminal {
	NVM_T_NONE = 0,
	NVM_T_COMPLETE = 1,  /* an accepted slot, every record applied or refused */
	NVM_T_BLANK = 2,     /* no slot accepted: the entity runs on its defaults */
	NVM_T_DEFAULTS = 3,  /* aborted and rolled back to the image defaults */
	NVM_T_CLOSED = 4     /* the model is unproven or a roll-back failed */
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
	NVM_P_VERIFY = 9,    /* read back and compare */
	NVM_P_HELD = 10      /* a slot's authority is unknown: changes are marked,
			      * nothing is written until reset */
};

/* Bytes one service step may touch, besides one latched record. */
#define NVM_STEP_BYTES NVM_FLASH_PAGE
/* The most bytes any service step touches: one 256-byte stretch, or one
 * latched record's copy and its crc16 over the header and the payload. */
#define NVM_STEP_BOUND NVM_MAX(NVM_STEP_BYTES, 2u * NVM_PAYLOAD_MAX + 6u)
/* DR2c: firmware transaction attempts per unchanged captured work set, and
 * the separation after a failed one (SAVED_STATE_MATERIALIZATION.md
 * sections 6.3 and 15.1). */
#define NVM_TXN_ATTEMPTS 3u
#define NVM_TXN_BACKOFF_MS 1000u
/* Boot reads of one slot: judgements, and then re-stages of the chosen one
 * (README, "Boot"). A slot that gives no standing verdict, or never reads
 * back as judged, within this many is UNREAD (#665 decision 2, issue
 * comment 5997929153). */
#define NVM_READ_TRIES 3u

struct nvm_status {
	enum nvm_verdict verdict_a;
	enum nvm_verdict verdict_b;
	enum nvm_verdict last_verdict;  /* the boot's offer, then each commit's */
	enum nvm_verdict first_failed;  /* the first failed attempt's since a success */
	uint32_t seq_a;
	uint32_t seq_b;
	uint32_t seq;                   /* the authoritative container's */
	int auth;                       /* 0 slot A, 1 slot B, -1 none */
	enum nvm_terminal terminal;     /* the D3 walk's, or CLOSED */
	enum nvm_cause cause;           /* the D3 walk's first abort cause */
	enum nvm_terminal bind_terminal;
	enum nvm_cause bind_cause;
	unsigned int applied;
	unsigned int refused;
	unsigned int blank;
	unsigned int releases;
	unsigned int commits_ok;
	unsigned int commits_failed;
	unsigned int commits_skipped;   /* DR2b: nothing the capture saw changed */
	unsigned int attempts;          /* failed attempts on this work set */
	int exhausted;                  /* this unchanged work set has none left */
	unsigned int withheld;          /* captures of an exhausted set: no attempt */
	/* The exhaustion record, cleared only by reset: work sets abandoned
	 * after their third failure, and the last one's first verdict. */
	unsigned int abandoned;
	enum nvm_verdict abandoned_vd;
	/* Slots never read without a media fault at boot (bit 0 A, bit 1 B):
	 * their authority is unknown, so the writer is HELD until reset. */
	unsigned int unread;
	/* Boot reads that failed, returned other bytes than every earlier read
	 * of the slot, or did not read back as judged. */
	unsigned int read_faults;
	int stale;                      /* a failed commit left work out of every slot */
	int dirty;                      /* changed records not yet captured */
	int pending;                    /* captured records not yet in a verified slot */
	enum nvm_phase phase;
	uint32_t step_bytes_max;        /* the most bytes one service step touched */
	uint32_t steps;
};

/* Boot: judge both slots, stage the newer accepted one, run its binding
 * walk, prove the model and run the D3 walk through `state`, release AECP
 * unless CLOSED, and arm the writer, or hold it when a slot is UNREAD. */
void nvm_store_boot(const struct nvm_flash *flash, const struct nvm_state *state);
/* One bounded step of the write path. */
void nvm_store_service(void);
/* An accepted command changed the persisted value of (group, index). It
 * marks the record; whether the work set changed is the capture's finding. */
void nvm_store_changed(unsigned int group, unsigned int index);
/* Start a capture now, without the debounce, and write it even if nothing
 * changed (the console); 1 when started. Refused inside a failed attempt's
 * backoff and while HELD, and an exhausted unchanged work set is still not
 * written. */
int nvm_store_commit_now(void);
const struct nvm_status *nvm_store_status(void);
/* The stage, NVM_IMG_LEN bytes: the last verified container, or the one a
 * commit in flight is writing. */
const uint8_t *nvm_store_stage(void);

#endif /* NVM_STORE_H */

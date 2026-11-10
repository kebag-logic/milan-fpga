/* SPDX-License-Identifier: (GPL-2.0 OR MIT) */
/*
 * nvm_store.h - the bare-metal saved-state store (#665 lane F1): the boot
 * restore and the write-back of docs/design/SAVED_STATE_FASTCONNECT.md
 * sections 6 and 7, under the D3 restore transaction of
 * docs/design/SAVED_STATE_MATERIALIZATION.md section 8, with the split
 * placement's append-only journal (#823 decisions 3, 4, 5 and 7,
 * docs/design/SAVED_STATE_FORMAT_32X32.md section 4).
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

/* The write path's phase; each service call advances at most one. A page
 * of a segment (a delta, a compaction's base or its copy of the old log)
 * goes ASSEMBLE, CARRY (a base only), SEAL, PROGRAM, PROGRAM_WAIT and
 * VERIFY; a delta's first program may wait for the background erase's
 * suspend first. */
enum nvm_phase {
	NVM_P_OFF = 0,       /* no writer: before boot, or retired */
	NVM_P_IDLE = 1,
	NVM_P_CAPTURE = 2,   /* latch the dirty records, one per step */
	NVM_P_ASSEMBLE = 3,  /* fill the page from the stage, or from the old log */
	NVM_P_CARRY = 4,     /* a base: keep whole the record that runs past the page */
	NVM_P_SEAL = 5,      /* the page's CRC-32, and the trailer on the last page */
	NVM_P_SUSPEND = 6,   /* suspend the background erase before a program */
	NVM_P_SUSPEND_WAIT = 7,
	NVM_P_PROGRAM = 8,   /* start one page program */
	NVM_P_PROGRAM_WAIT = 9,
	NVM_P_VERIFY = 10,   /* read the page back and compare */
	NVM_P_HELD = 11      /* a slot's authority is unknown: changes are marked,
			      * nothing is written until reset */
};

/* The background preparation of the slot that is not authoritative: each of
 * its pages read blank, a block found written erased (and its erase
 * suspended for a save), so a compaction finds it blank (#823 decisions 3
 * and 5). */
enum nvm_bg {
	NVM_B_NONE = 0,
	NVM_B_CHECK = 1,      /* read the next page; a written one erases its block */
	NVM_B_ERASE_WAIT = 2,
	NVM_B_READY = 3,      /* every page read blank */
	NVM_B_FAILED = 4      /* NVM_TXN_ATTEMPTS preparations failed: until reset */
};

/* Bytes one service step may touch, besides one latched record. */
#define NVM_STEP_BYTES NVM_FLASH_PAGE
/* The most bytes any service step touches: one 256-byte stretch, or one
 * latched record's copy and its crc16 over the header, less the crc16's own
 * two bytes, and the payload. A compaction's carry of one whole record is
 * less than the second. */
#define NVM_STEP_BOUND NVM_MAX(NVM_STEP_BYTES, 2u * NVM_PAYLOAD_MAX + (NVM_REC_HDR - 2u))
/* #823 decision 4: the firmware first-dirty window, superseding DR2a's
 * 1,000 ms for this store (SAVED_STATE_FORMAT_32X32.md section 4). */
#define NVM_WINDOW_MS 150u
/* #823 decision 7: T-NVM-COMMIT-TIMEOUT for an append, from the save falling
 * due to its last page read back. A compaction and the background erase
 * carry no durability claim and no such deadline. */
#define NVM_APPEND_TIMEOUT_MS 500u
/* #823 decision 5, assumption A3: the room the 0.5 s bound leaves the erase
 * suspend's latency, graded at its typical 15 us (N25Q128 section 9.1.20 and
 * Table 17, no maximum given). A suspend that took longer is counted slow. */
#define NVM_SUSPEND_ROOM_US 95290u
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
	/* How many: the counts the open bits carry (#823 decision 6). */
	unsigned int n_dirty;
	unsigned int n_inflight;
	/* Today's journal, the all-fabric placement's, which this store never
	 * writes: bit 0 its slot A, bit 1 its slot B, set when that slot's
	 * header is a KLJ2 header. A KLJ2 journal is the previous format,
	 * refused VD_VER (#823 decision 2); when neither of this store's slots
	 * holds a container, the boot's last_verdict is then VD_VER, not
	 * VD_BLANK. */
	unsigned int legacy;
	/* The journal (#823 decision 3): the authoritative slot's next segment
	 * offset and its closing deltas; torn when a segment past them does not
	 * close, so the next write is a compaction; a compaction in progress. */
	uint32_t log_end;
	unsigned int deltas;
	int torn;
	int compacting;
	int cmp_due;                    /* a compaction is owed and can run once the other slot is ready */
	unsigned int appends;           /* deltas verified */
	unsigned int compactions;       /* compactions whose slot took the authority */
	/* The other slot's preparation, its failed attempts and the last one's
	 * verdict. */
	enum nvm_bg bg;
	unsigned int prep_failed;
	enum nvm_verdict prep_vd;
	/* The erase suspends (#823 decision 5): how many, the longest, and how
	 * many took longer than NVM_SUSPEND_ROOM_US. */
	unsigned int suspends;
	uint32_t suspend_us_max;
	unsigned int suspend_slow;
	enum nvm_phase phase;
	uint32_t step_bytes_max;        /* the most bytes one service step touched */
	uint32_t steps;
};

/* Boot: judge both slots (each base, then its log), stage the newer
 * accepted one with its log replayed, run its binding walk, prove the model
 * and run the D3 walk through `state`, release AECP unless CLOSED, and arm
 * the writer, or hold it when a slot is UNREAD. */
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
/* The stage, NVM_IMG_LEN bytes: every record's latest latched value at its
 * offset, under the header and trailer of the base last read or written. */
const uint8_t *nvm_store_stage(void);

#endif /* NVM_STORE_H */

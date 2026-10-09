/* SPDX-License-Identifier: (GPL-2.0 OR MIT) */
/*
 * nvm_state.h - the state port: where the saved values go at boot and where
 * a changed value is read from (#665 lane F1).
 *
 * The store owns the media and the container; the entity's live values have
 * owners of their own. In the all-fabric build those owners are the
 * processor's stores, and the fabric restore writes them as
 * docs/design/SAVED_STATE_MATERIALIZATION.md sections 6.2 and 8 describe:
 * KL_aecp_nvm_writer's APPLY writes a value with its valid flag through the
 * state bus, judged first by the rule of the SET program that would set it;
 * the binding manager preloads the listener; a port's saved map set is one
 * staged ADD; names go to the writable name table last. This port is that
 * same set of writes, one call per record, so the firmware restore can drive
 * whichever owner a build places each function in.
 *
 * THE TWO WALKS (section 8.1 steps 4 to 8, section 8.6). The binding walk
 * restores the listener's bindings first and is its own unit of atomicity:
 * a fault fails it whole, with nothing preloaded, and the D3 walk runs
 * either way. It needs no entity model; the D3 walk does, so model_ready()
 * is asked between the two (step 6), and an unproven model ends the restore
 * CLOSED with the bindings kept. The D3 walk restores every other record as
 * one transaction; a D3 roll-back leaves a completed binding walk applied,
 * because its owners are the two stores and the map plane, never the
 * listener or the binding manager.
 *
 *   apply()     one saved record. APPLIED or REFUSED by the group's value
 *               rule (section 8.3: a refused value keeps its image default
 *               and the walk goes on); FAULT when the rule cannot be judged
 *               (a descriptor read that errs), which aborts that walk;
 *   settle()    called once in the D3 walk, after the last map record and
 *               before the first name: every restored format is judged again
 *               against the final maps (section 8.4 step 4). Where #658's
 *               restore clip lands (issue #658 ruling 5988843004 item 3: a
 *               restored narrower format clips the identity default before
 *               AECP is released), it is this step's; the store does not
 *               depend on it;
 *   rollback()  undo one walk. NVM_W_D3: every D3 value back to its image
 *               default (section 8.6: the restore wrote only into reset
 *               state, so the undo is a reset of the two stores and the map
 *               plane), the bindings untouched. NVM_W_BIND: every binding the
 *               walk preloaded dropped, nothing else touched;
 *   latch()     the current value of one record, for the write path: the
 *               "no shadow" rule of section 3, the value is read from its
 *               owner when it is saved;
 *   release()   AECP may run. Called once, at the D3 terminal COMPLETE or
 *               DEFAULTS (or BLANK), never at CLOSED.
 */
/* No synchronous callbacks (#678): a port must return before any core
 * input is dispatched by the single bare-metal event loop. A port never
 * calls back into a protocol core or the store, including on zero-delay
 * timer arms or TX completion. Interrupts defer dispatch to the loop.
 * F2 to F5 inherit this rule for every protocol port. */

#ifndef NVM_STATE_H
#define NVM_STATE_H

#include <stdint.h>

enum nvm_apply {
	NVM_APPLIED = 0,
	NVM_REFUSED = 1,
	NVM_FAULT = 2
};

/* The two walks of the boot restore, in the order they run. */
enum nvm_walk {
	NVM_W_BIND = 0,
	NVM_W_D3 = 1
};

struct nvm_state {
	/* 1 when the entity model the values are judged against is loaded and
	 * proven (the AEM image, CRC checked); 0 ends the restore CLOSED after
	 * the binding walk. */
	int (*model_ready)(void *ctx);
	enum nvm_apply (*apply)(void *ctx, unsigned int group, unsigned int index,
				const uint8_t *payload, unsigned int len);
	enum nvm_apply (*settle)(void *ctx);
	/* 0 when the walk's owners are back where the walk found them. */
	int (*rollback)(void *ctx, enum nvm_walk walk);
	/* Write the record's current payload, len bytes; return 1, or 0 when
	 * the owner has nothing to save and the staged bytes stand. */
	int (*latch)(void *ctx, unsigned int group, unsigned int index,
		     uint8_t *payload, unsigned int len);
	void (*release)(void *ctx);
	void *ctx;
};

#endif /* NVM_STATE_H */

/* SPDX-License-Identifier: (GPL-2.0 OR MIT) */
/*
 * nvm_smodel.h - the host model behind the state port (#665 lane F1).
 *
 * One value and one valid flag per record id, standing in for the owners the
 * restore writes and the write path latches from. At power on every value
 * is its image default (a pattern no saved payload in the suite uses) with
 * valid 0, so a restore that writes nothing cannot pass for one that wrote
 * the defaults back (issue #70's vacuity trap). A value rule refuses the
 * records the test names, a fault can be planted at the apply of one record,
 * at the settle step and at either walk's roll-back, and the order the store
 * calls the port in is policed: the binding walk before the D3 walk, each in
 * ascending id, every format and map before the settle step, the settle step
 * once and before every name, nothing after the release, and the release
 * once. A roll-back puts back its own walk's records only.
 */
#ifndef NVM_SMODEL_H
#define NVM_SMODEL_H

#include <stdint.h>

#include "../nvm_state.h"

struct nvm_smodel_count {
	unsigned int applies;
	unsigned int applied;
	unsigned int refused;
	unsigned int faults;
	unsigned int settles;
	unsigned int rollbacks;     /* of the D3 walk */
	unsigned int unbinds;       /* of the binding walk */
	unsigned int releases;
	unsigned int latches;
	unsigned int order;         /* calls out of the order above */
};

/* Power on: every value at its image default, valid 0, no rule or fault. */
void nvm_smodel_reset(void);
void nvm_smodel_ready(int ready);
void nvm_smodel_refuse(unsigned int id);
/* The apply of record id answers FAULT. */
void nvm_smodel_fault_apply(unsigned int id);
void nvm_smodel_fault_settle(int on);
void nvm_smodel_fault_rollback(enum nvm_walk walk);
/* An accepted command: the value of record id, made valid. */
void nvm_smodel_set(unsigned int id, const uint8_t *value, unsigned int len);
const uint8_t *nvm_smodel_value(unsigned int id);
int nvm_smodel_valid(unsigned int id);
uint8_t nvm_smodel_default(unsigned int id, unsigned int j);
const struct nvm_smodel_count *nvm_smodel_count(void);

extern const struct nvm_state nvm_smodel_port;

#endif /* NVM_SMODEL_H */

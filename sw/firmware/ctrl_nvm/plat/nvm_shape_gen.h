/* SPDX-License-Identifier: (GPL-2.0 OR MIT) */
/*
 * nvm_shape_gen.h - the target's shape constants (#665 lane F1).
 *
 * On the target the builder's generated/soc.h carries every constant
 * nvm_shape.h needs: MILAN_NVM_* (scripts/nvm_shape.py firmware_constants),
 * the identity words and the journal map, as sw/litex/milan_soc.py publishes
 * them for the shipping writer. The host suite writes its own copy of this
 * file per shape from the same derivation.
 */
#ifndef NVM_SHAPE_GEN_H
#define NVM_SHAPE_GEN_H

#include <generated/soc.h>

#endif /* NVM_SHAPE_GEN_H */

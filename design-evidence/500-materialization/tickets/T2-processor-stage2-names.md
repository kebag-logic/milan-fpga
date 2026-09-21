<!-- Draft by A151, revised by A152 and A153, for the manager to file. Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan. After T1 (and so after T8 and T9). -->

# Saved state, stage 2: the record writer materializes user names

## Objective

Extend `KL_aecp_nvm_writer` (T1) to the user-name records, one 64-byte record
per writable-name ordinal at `0x80 + ordinal` (38 at the parent's 1x1 shape,
99 at 8x8), Milan v1.2 5.3.13, inside T1's restore transaction.

## Authority

kebag-logic/milan-fpga `docs/design/SAVED_STATE_MATERIALIZATION.md` sections
3 (rule 3), 7, 8.5, 8.6 and 8.8; the parent's saved-state page section 4.2
(the empty name is a value, 64 zero bytes); `07_memory_maps.md` section 5.

## Prerequisites

T1, and with it T8 (the port's cause, the bounded binding walk) and T9
(response isolation on the descriptor store's memory face): this stage
RESETS the descriptor store in its roll-back, and a re-walk that took a late
beat of an abandoned burst could validate an image with wrong names (only
its header is checksummed). Before this stage is DECLARED SHIPPABLE:
kebag-logic/milan-fpga #502, truthful pending from the first accepted live
write for the classes no shipped stage materializes. It may be implemented
before; it may not be released as a shipped stage.

## In scope

- The trigger: the uCPU's accepted name-table write (`st_name AND st_we AND
  store_ready`), ordinal `st_addr[15:6]`; never the class-7 mark.
- The eight-lane latch under the dispatch hold-off.
- The restore after the descriptor store has walked the loaded image: a
  LOCATE of ENTITY 0 first if the image is not validated, then the name
  written back lane by lane.
- The roll-back owner: `KL_aecp_desc_store` gains a soft-reset (or re-walk)
  input driven by T1's roll-back strobe, so a pass-1 abort puts every name
  back to the image's, and the writer's LOCATE after it proves the image
  walked. T9's guard stays on the HARD reset: the soft reset never clears
  the debt of a burst the memory still owes, and the writer holds the store
  in reset until that debt is gone, bounded by its deadline. A re-walk that
  cannot validate the image, or a debt that outlasts the deadline, is the
  CLOSED terminal: fail, never done, `own` kept, the entity never enabled.

## Acceptance

- One name change converges; a slow SET_NAME across the debounce close is
  never latched half old, half new (the hold-off's mutant reddens).
- A restored name survives the first AECP command after enable; a mutant that
  writes the name back before the image walk reddens.
- The EMPTY name survives a power cycle as the empty name, against a
  non-empty image default.
- Every name equals the image's default before pass 1 writes any, the first
  and the last ordinal restored exactly, the unsaved ones unchanged.
- A read error on the LAST name in pass 1, after names and every stage-1
  group applied, ends in DEFAULTS with every name the image's; silence on it
  likewise; a DEVICE error on the last name's header in pass 1 likewise; a
  re-walk that cannot validate ends CLOSED; each with the mutant that skips
  that owner's roll-back, or releases a closed restore, red.
- Around the store's own reset: a fetch answered by the store's own
  watchdog, its late burst arriving 5,000 and 16,000 cycles after the
  request, rolls back with every name the image's and the store released
  only after the burst; the burst past the deadline ends CLOSED; the mutant
  that releases the store without the debt reddens the 16,000-cycle case.
- Deleting the name trigger alone reddens a save test; deleting the name
  replay alone reddens a restore check.

## Validation

As T1, with the name arms.

## Dependencies

T1. The parent stops taking class 7 into its sticky pending bit in the same
pin bump (milan-fpga T4).

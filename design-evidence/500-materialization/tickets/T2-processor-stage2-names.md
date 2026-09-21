<!-- Draft by A151 for the manager to file. Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan. After T1. -->

# Saved state, stage 2: the record writer materializes user names

## Objective

Extend `KL_aecp_nvm_writer` (T1) to the user-name records, one 64-byte record
per writable-name ordinal at `0x80 + ordinal` (38 at the parent's 1x1 shape,
99 at 8x8), Milan v1.2 5.3.13.

## Authority

kebag-logic/milan-fpga `docs/design/SAVED_STATE_MATERIALIZATION.md` sections
3 (rule 3), 7, 8.5; the parent's saved-state page section 4.2 (the empty name
is a value, 64 zero bytes); `07_memory_maps.md` section 5.

## In scope

- The trigger: the uCPU's accepted name-table write (`st_name AND st_we AND
  store_ready`), ordinal `st_addr[15:6]`; never the class-7 mark.
- The eight-lane latch under the dispatch hold-off.
- The restore after the descriptor store has walked the loaded image: a
  LOCATE of ENTITY 0 first if the image is not validated, then the name
  written back lane by lane.

## Acceptance

- One name change converges; a slow SET_NAME across the debounce close is
  never latched half old, half new (the hold-off's mutant reddens).
- A restored name survives the first AECP command after enable; a mutant that
  writes the name back before the image walk reddens.
- The EMPTY name survives a power cycle as the empty name, against a
  non-empty image default.
- Deleting the name trigger alone reddens a case.

## Validation

As T1, with the name arms.

## Dependencies

T1. The parent stops taking class 7 into its sticky pending bit in the same
pin bump (milan-fpga T4).

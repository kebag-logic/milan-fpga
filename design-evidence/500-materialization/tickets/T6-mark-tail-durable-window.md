<!-- Draft by A151 for the manager to file. Repository: kebag-logic/milan-fpga. Under #70. Closed by D3 stages 2 and 3; filed so it is not lost if they slip. -->

# Saved state: the status reads durable over an applied name or map for the program's tail

## Observed

`hdl/milan/KL_pp_shadow.sv` (lines 935 to 946) makes the class-6 and class-7
commit marks sticky pending sources. The programs raise them only after the
live write: SET_NAME's `NVM_MARK` follows its last `NAME_WR` by three
instructions, ADD/REMOVE_AUDIO_MAPPINGS's follows the commit loop by five
(`protocol-processor/hdl/aecp/ucode/gen_ucode.py` lines 2092 and 1792).
Between the two, PP_STAT can read durable (backed 1, dirty 0, stale 0, pend 0)
over a name or map that is already live and in no slot.

EXECUTED on the tracked glue (evidence branch `500-design-evidence`, commit
`a21b165ac1c671d10cba7255beaf75cea0f81d18`): K10 "change of 0x80 at 30182
inside a durable interval ending 30189", K12 "change of 0x70 at 30155 inside
a durable interval ending 30161" (model cycles; a few instructions on the
product, DERIVED).

## Resolution

`docs/design/SAVED_STATE_MATERIALIZATION.md` triggers on the live write, so
stages 2 and 3 close it. If they slip, the standalone fix is the same trigger
feeding the sticky bit.

## Acceptance

The two tracked-glue checks pass on the shipping glue.

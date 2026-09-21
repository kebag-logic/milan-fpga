<!-- Draft by A151, revised by A152. Filed as kebag-logic/milan-fpga #502. Under #70. A prerequisite of every D3 stage declared shippable; its standalone correction may precede the stages. -->

# Saved state: the status reads durable over an applied name or map for the program's tail

## Observed

`hdl/milan/KL_pp_shadow.sv` (lines 935 to 946) makes the class-6 and class-7
commit marks sticky pending sources. The programs raise them only after the
live write: SET_NAME's `NVM_MARK` follows its last `NAME_WR` by three
instructions, ADD/REMOVE_AUDIO_MAPPINGS's follows the commit loop by five
(`protocol-processor/hdl/aecp/ucode/gen_ucode.py` lines 2092 and 1792).
Between the two, PP_STAT can read durable (backed 1, dirty 0, stale 0, pend 0)
over a name or map that is already live and in no slot.

EXECUTED on the tracked glue (D3 evidence branch `500-design-evidence`, the
commit the page names): K10 "change of 0x80 at 30182 inside a durable
interval ending 30189", K12 "change of 0x70 at 30155 inside a durable
interval ending 30161" (model cycles; a few instructions on the product,
DERIVED).

## Why it gates the D3 stages

No D3 stage may be DECLARED SHIPPABLE while this remains: a shipped stage's
silicon proof reads PP_STAT durable, and until names and maps are
materialized that reading can be false over them. The D3 stages retire the
window only for the classes they materialize (names at stage 2, maps at
stage 3, which is itself blocked on #501), so this correction is needed
first, on its own.

## Resolution

The standalone correction: the same live-write trigger the D3 design uses
(the uCPU's accepted name-table write; the map edit face's commit beat)
feeding the parent's pending bit from the first accepted write, for both
classes. Filing this does not close it: it closes when the correction lands.

## Acceptance

A real program and glue integration asserts that the status never reads
durable from the first accepted live write through the mark and the
eventual commit, for a changed name and a changed map; with unchanged-command,
reset and both-class controls. The two tracked-glue checks above pass on the
shipping glue.

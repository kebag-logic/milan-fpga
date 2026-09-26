[A329]

Closes #120

Exports `aecp_name_wr_o` from the descriptor store’s accepted live name-lane write through the engine and processor top. Each accepted lane produces one pulse at its write edge; boot loading, unchanged lanes, refused/out-of-range commands and writes aborted before acceptance remain silent. Existing behavior and NVM mark timing are preserved, with no new state.

Documents the port contract and adds 85 focused checks for counts, timing, readback, refusal, stalls and watchdog abort/recovery. A command-decode mutant compiles and fails the multi-lane, locked and aborted-write count checks; golden and restored runs pass.

Whole-processor area: 66,461 → 66,439 mapped LUTs; 32,462 registers, 16 large and one small block RAM, and four DSPs unchanged. The added output contributes one output buffer; small mapping variation is not a logic-saving claim.

All donor gates pass, including 1,014,722 simulation checks, strict lint, synthesis portability, parameter/matrix inventories and all documentation checks. Parent integration elaboration and its 231-check datapath leg pass with the output omitted.

**Acceptance gap:** the unmodified parent strict suite and lint reject the omitted `aecp_name_wr_o` connection. They require an explicit open connection; parent edits are outside this assignment, so those two consumer gates remain blocked. Parent repository sources are unchanged.

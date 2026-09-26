[A336]

Closes #120

Exports `aecp_name_wr_o` from the descriptor store’s accepted live name-lane write through the engine and processor top. Each accepted lane produces one pulse at its write edge; boot loading, unchanged lanes, refused/out-of-range commands and writes aborted before acceptance remain silent. Existing behavior and NVM mark timing are preserved, with no new state.

Documents the port contract and adds 85 focused checks for counts, timing, readback, refusal, stalls and watchdog abort/recovery. A command-decode mutant compiles and fails the multi-lane, locked and aborted-write count checks; golden and restored runs pass.

Whole-processor area: 66,461 → 66,439 mapped LUTs; 32,462 registers, 16 large and one small block RAM, and four DSPs unchanged. The added output contributes one output buffer; small mapping variation is not a logic-saving claim.

All donor gates pass, including 1,014,722 simulation checks, strict lint, synthesis portability, parameter/matrix inventories and all documentation checks. Parent integration elaboration and its 231-check datapath leg pass with the output omitted.

**Parent consumer validation:** all 12 prescribed consumer commands return 0 in a private copy of the requested parent base, with the supplied open-port rationale and mutation-reader disposition patch and the updated processor pin. The original parent repository remains unchanged. The builder command reports one utilization-calibration arm not run because its external implementation report is absent; that arm is outside the claimed coverage.

## Round 2

At `a9b7874d415d935949becd7ccfd58799927efb08`, splits the name-write acceptance scenarios into short helpers without changing stimulus or assertions. Documents both public mutation functions and the store, engine, top and harness port contracts; restores the effect-strobe documentation bundle so the added port creates no documentation debt. Mutation verdicts depend on completed simulation outcomes, with waits bounded by DUT cycles.

All repository gates pass again, including 1,014,722 simulation checks and the 46-build historical figure check. The focused pre/post output is byte-identical: 85 checks, zero failures. The command-decode mutant still fails the required multi-lane, locked and aborted-write checks; golden and restored runs pass. RTL tokens are unchanged after removing comments and whitespace.

All 12 consumer commands return 0. The integration suite passes three builds of 402 checks each. Processor undocumented ports return to 111, with zero unexplained source readers and the wall-clock-dependent file count back at its existing budget of three. The builder calibration coverage limit is recorded above. The private consumer copy was deleted after validation.

## Round 3

At `83c84b19e09d397ed2eb6f5ace337686ce0ef86b`, moves the two new harness ports and their contracts before the existing effect-strobe bundle, restoring all four declarations to one contiguous group. The parent parser reports 162 undocumented harness ports, as at base, and all six effect/name observation ports are documented. Marks `run_name_writes` as `[[maybe_unused]]` for the fixture build while retaining its default-build call and every scenario and assertion. Production RTL is unchanged.

Both fresh harness builds are warning-free. The default and fixture runs retain 7,731 and 20 checks, and the focused name-write scenario retains 85 checks, all with zero failures and unchanged simulation output. The canonical combined tally is 7,751/0. All repository gates pass, including 1,014,722 simulation checks and the 46-build historical figure gate.

All 12 prescribed parent consumer commands return 0 at this head in the private copy of the requested parent base with the supplied patch. The integration suite passes three builds of 402 checks each; processor undocumented ports remain 111, with zero unexplained source readers and three wall-clock-dependent files within budget. The builder calibration coverage limit remains as recorded above. The private parent copy was deleted after validation.

[A245] Isolate late descriptor-memory responses after a store timeout.

Closes #94

An in-order memory queue can still owe a burst after the descriptor store's
watchdog abandons it. Without isolation, a later STREAM_INPUT locate receives
STREAM_OUTPUT bytes. Add `KL_aecp_desc_mem_guard` at the processor top: remember
accepted burst debt until a consumed `last` or `err`, hold both request handshake
arms while owed, and pass every response through unchanged. Only hard reset
clears debt independently of a terminal beat.

Publish the guard's `debt_o` as `desc_mem_debt_o`, the D3 interface. Update the
architecture status dictionary, integrator contract, existing diagrams, RTL source
lists and generated test matrix. Preserve the store watchdog behavior, including
the immediate error on the first locate after a fetch-response timeout.

## Validation

- Reproduced wrong bytes on the unmodified store before changing product RTL:
  `00060000deadbeef cafef00d01234567` instead of
  `0005000011223344 5566778899aabbcc`.
- The guard passes the identical late case; removing only the request hold fails
  the same completed byte assertion. The stuck-burst case holds requests and
  answers each locate with an error within the asserted bound.
- Guard suite: 77 checks. Existing store suite: 584 checks. Product-top suite:
  1,454 checks, including actual wire commands for late and stuck bursts.
- Full simulation bank: 32 suites, 15,894 checks, zero failing. All CI gates and
  `make check` returned zero, including the 46-build NVM figure gate.
- Repository OOC flow: 4 LUTs and 1 flip-flop, versus T9's 5 LUT / 1 flip-flop
  estimate; no RAM or DSP.

Exact commands, return codes, the mutation table and reports are in the author handoff. The manager archives it with the review evidence.
Local head: `4f525eb55b310d6b9bc2f1a000254cb2dd483665`.

## Deferred to the D3 lane

The D3 writer, owners held while `debt_o` is set, deadline-to-CLOSED policy,
5,000/16,000-cycle rollback cases, stage-1-only/full-slot rollback cases and the
owner-release mutant need the D3 writer and remain deferred under the assignment.
`debt_o` is their published interface. The guard's store-only reset test proves
debt retention at the seam; it does not claim those rollback cases.

[A252] Isolate late descriptor-memory responses after a store timeout and preserve the parent consumer interface.

Closes #94

An in-order memory queue can still owe a burst after the descriptor store's
watchdog abandons it. Without isolation, a later STREAM_INPUT locate receives
STREAM_OUTPUT bytes. Add `KL_aecp_desc_mem_guard` between the AECP engine's
exported descriptor-store master and `desc_mem_*` at the processor top. It
retains accepted burst debt until a consumed `last` or `err`, holds both
request handshake arms while owed, and passes every response through unchanged.
Only hard reset clears debt independently of a terminal beat.

The guard's own `debt_o` port is the documented D3 interface. The product top
exports no new debt port, so the parent's existing instantiation remains valid.
The product-top bench observes the guard port hierarchically. Architecture
and integrator documentation, diagrams, source lists and the generated test
matrix cover the guard. The store watchdog behavior is preserved, including
the immediate error on the first locate after a fetch-response timeout.

The round-1b bench cleanup replaces C-style casts with named casts, moves
counters into a result object owned by `main`, separates declarations, and
annotates and documents the mutation controller's public entry point.

## Round 2

Addresses the shared F1 in [R290-2](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/110#issuecomment-5812425622)
and [R291-2](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/110#issuecomment-5812328379),
plus R291-2 suggestions S1-S4:

- Re-rendered figure 22 at 1950 x 1440 and figure 20 at 2040 x 1380 from their
  final SVGs using the documented renderer. Both were opened and visually
  checked: figure 22 shows the guard and updated module/suite lists; figure 20
  shows the guard label. A repeat render matches each committed PNG exactly.
- Drew the guard as a processor module before external memory in both
  figures, with the independent response-buffer master bypassing it.
- Added the `handshake_case` assertion that request acceptance wins over a
  coincident stray terminal beat. The guard passes 78/78; swapping the priority
  produces 77 PASS / 1 FAIL at exactly that new completed assertion, make rc 2.
- Removed the stray blank line in the top's port block and addressed the
  reset instruction to `protocol_processor_top.rst_n`: hard reset with the
  descriptor-memory path flushed, never entity disable or store/rollback reset.

## Validation

Round-2 local gates all returned 0:

- Every validation step in `.github/workflows/hdl.yml`: links, requirement
  matrix, WaveDrom freshness, `make stale`, RTL lint, the full simulation bank,
  generated matrix, the 46-build NVM figure gate and portability including
  engine memory mapping. `make check` also returned 0.
- Full bank: 32 suites, 15,895 checks, zero failing. Guard: 78/78; descriptor
  store: 584/584; product top: 1,454/1,454, including the wire-level late and
  stuck-burst cases. Store-only reset, hard reset, terminal error, payload and
  handshake coverage remains green.
- With `2e1675d2d20bbc0bb549b36b9d485b2f9b747d5f` checked out in the parent consumer,
  `python3 scripts/check_cpp_idiom.py`, `python3 scripts/check_py_idiom.py`,
  `python3 scripts/xvlog_gate.py --check`,
  `python3 scripts/check_rtl_source_lists.py` and
  `make -C tb/verilator/pp_shadow -j8` all returned 0. The parent simulation
  passed 371 checks. The processor gitlink was staged only while running
  the pin-verifying gates; the original parent index was restored byte for
  byte afterward. No parent commit was made.
- `git diff --check` passes, both PNGs match their final SVG renders, and
  the priority mutation controller returns 0 after the expected assertion
  failure. The source worktree is clean.

Existing acceptance evidence from the preceding round remains applicable to
the unchanged guard logic:

- The unguarded late-beat reproduction returns
  `00060000deadbeef cafef00d01234567` instead of
  `0005000011223344 5566778899aabbcc`: 17 PASS / 1 expected FAIL, simulation
  rc 1 and make rc 2. Deleting both request holds fails the same completed
  byte assertion with the same wrong bytes; the mutation controller returns 0
  only after detecting it.
- The guarded late case passes all 18 checks and recovers after the burst
  drains. A never-ending burst leaves five later locates answering errors
  within 4,102 cycles against the 4,160-cycle bound, with debt held and no new
  request accepted. These cases also pass in the round-2 sweep.
- Guard OOC area: 4 LUTs and 1 flip-flop versus T9's estimate of 5 LUTs and
  1 flip-flop, with no RAM or DSP. This is prior post-synthesis evidence;
  guard RTL is unchanged and no new timing or hardware result is claimed.

Exact commands, return codes, the priority mutant, visual inspection notes
and consumer index-restoration evidence are in the round-2 author packet for
manager archival. Local head: `2e1675d2d20bbc0bb549b36b9d485b2f9b747d5f`.

## Deferred to the D3 lane

Per the [scope decision](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/94#issuecomment-5810666541)
and [port decision](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/110#issuecomment-5811722803),
D3 will route `debt_o` to `protocol_processor_top` together with the parent
consumer changes. This PR publishes it only on the guard module.

The D3 writer, owners held while debt is set, deadline-to-CLOSED policy,
5,000/16,000-cycle rollback cases, stage-1-only/full-slot cases and the
owner-release mutant remain deferred. The store-only reset test proves debt
retention at the seam; it does not claim those rollback cases. The manager
owns the gitlink-dependent parent `pp_srcs` and `test_builder` gates,
publication, hosted/replica acceptance and independent re-review.

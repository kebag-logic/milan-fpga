[A250] Isolate late descriptor-memory responses after a store timeout and preserve the parent consumer interface.

Closes #94

An in-order memory queue can still owe a burst after the descriptor store's
watchdog abandons it. Without isolation, a later STREAM_INPUT locate receives
STREAM_OUTPUT bytes. Add `KL_aecp_desc_mem_guard` between the AECP engine's
exported descriptor-store master and `desc_mem_*` at the processor top. It retains
accepted burst debt until a consumed `last` or `err`, holds both request handshake
arms while owed, and passes every response through unchanged. Only hard reset
clears debt independently of a terminal beat.

The guard's own `debt_o` port is the documented D3 interface. The product top
exports no new debt port, so the parent's existing instantiation remains valid.
The product-top bench observes the guard port hierarchically and retains every
debt assertion. Architecture and integrator documentation, the existing diagrams,
RTL source lists and the generated test matrix cover the guard. The store watchdog
behavior is preserved, including the immediate error on the first locate after a
fetch-response timeout.

Round 1b replaces all ten C-style casts with named casts, moves the new bench's
counters into a result object owned by `main`, separates its declarations, and
annotates and documents the mutation controller's public entry point. The repaired sources have zero local Rule 11 and Rule 12 findings; the full
parent gates await the index-pin prerequisite described below.

## Validation

- Re-ran the unguarded late-beat reproduction: the completed third locate returns
  `00060000deadbeef cafef00d01234567` instead of
  `0005000011223344 5566778899aabbcc`; 17 PASS / 1 expected FAIL, simulation rc 1
  and make rc 2.
- The guard passes the identical late case (18 checks). Removing only both
  request holds fails the same completed byte assertion with the same wrong
  bytes; the mutation controller returns 0 only after detecting that failure.
- The never-ending burst emits one nonterminal beat; five later locates all
  return errors, at most 4,102 cycles against the 4,160-cycle bound. Debt stays
  set and no additional memory request is accepted.
- Guard suite: 77 checks. Existing store suite: 584 checks. Product-top suite:
  1,454 checks, including wire-level late and stuck-burst cases. Store-only reset,
  hard reset, terminal error, payload and handshake cases remain covered.
- Full simulation bank: 32 suites, 15,894 checks, zero failing. Pre/post sweep
  summaries and full guard runtime output are byte-identical.
- RTL lint, documentation gates, portability, the generated matrix and the
  46-build NVM figure gate all return 0.
- Guard OOC area: 4 LUTs and 1 flip-flop, versus T9's 5 LUT / 1 flip-flop estimate;
  no RAM or DSP. This is post-synthesis area only.
- With the final local head checked out in the parent submodule,
  `check_rtl_source_lists.py`, `pp_srcs.py --check --selftest`, and
  `make -C tb/verilator/pp_shadow -j8` return 0; the parent build passes 371 checks.
  The parent submodule is left at that head.
- Parent verification is incomplete: `check_cpp_idiom.py`, `check_py_idiom.py`
  and `xvlog_gate.py --check` return 2 before scanning because the parent index
  still pins `4f525eb5`. The checkout-only permission does not authorize staging
  the new gitlink. Temporary staging followed by index restoration has been
  requested; no gate or budget has been bypassed.

Exact commands, return codes, before/after findings, mutation results, both
repository gate tables and area reports are in the author handoff, which
the manager archives with the review evidence.
Local head: `cc077a6ffe20585d20b116f008e07189ba1bb7f8`.

## Deferred to the D3 lane

Per the [manager's port decision](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/110#issuecomment-5811722803),
D3 will route the guard's `debt_o` to `protocol_processor_top` together with the
parent consumer changes. This PR publishes that signal only on the guard module;
it does not add a product-top debt port.

The D3 writer, owners held while `debt_o` is set, deadline-to-CLOSED policy,
5,000/16,000-cycle rollback cases, stage-1-only/full-slot rollback cases and the
owner-release mutant remain deferred. The guard's store-only reset test proves
debt retention at the seam; it does not claim those rollback cases.

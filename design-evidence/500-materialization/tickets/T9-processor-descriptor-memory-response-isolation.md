<!-- Draft by A153, revised by A154, for the manager to file as a NEW processor issue (Mister-M-alt/protocol-processor-control-plane-avb-milan). A prerequisite of D3 stage 1 (kebag-logic/milan-fpga #500); it also closes a pre-existing exposure of ordinary AECP service. -->

# Descriptor store: a burst abandoned by its own watchdog can hand its late beats to the next request

## Observed

`KL_aecp_desc_store` keeps one burst outstanding and consumes a beat only
while it awaits one (`beat_w = mem_rsp_valid_i && mem_busy_r`). Its own
no-progress watchdog, `MEM_TIMEOUT_CYC_P` (4,096), ABANDONS a burst: it
answers the locate with an error and clears `mem_busy_r`, but the memory
still owes that burst. Its reset forgets an outstanding burst the same way.
The store then accepts its next request as soon as the memory face is
ready.

The parent's memory path for the store is an asynchronous CDC request FIFO
in front of `pp_desc_bridge` (`sw/litex/milan_soc.py`, `_axis_dp_cdc` and
`pp_desc_bridge`). The FIFO accepts the next request while the bridge still
owes the abandoned burst, and the bridge answers in order, so the next
burst's first beats are the abandoned burst's. The bridge's own poison
discards a stale BUS answer, but it cannot stop the processor side from
counting in-order late beats as the new burst. Only the 32-byte image header
is checksummed; a descriptor fetch, the index map and the name table are
not.

EXECUTED on the D3 evidence branch `500-design-evidence` (case V23 at the
commit the page names), with the store pinned and the memory modelled as an
in-order FIFO that accepts while bursts are owed: a locate of STREAM_OUTPUT 0
whose fetch answers 6,000 cycles late is answered an error at 4,096; a
locate of STREAM_INPUT 0 presented while that burst is owed is answered the
STREAM_OUTPUT bytes (descriptor_type 0x6) when nothing holds its request
(mutant DG01), its own (0x5) when the guard below does.

A second, smaller pinned behaviour the case also shows: after a fetch's
RESPONSE timed out, the store does not re-arm its watchdog: the
`S_FET_RSP` timeout (`KL_aecp_desc_store.sv` line 980) answers without
clearing `tmo_r`, so the next fetch's `S_FET_REQ` (line 938) meets the limit
and answers an error in its first cycle. That failure is honest (an error,
never stale data), and in ordinary service the fetch after it succeeds. In
the D3 roll-back it is decisive: draining the debt alone leaves the
roll-back's re-LOCATE failing at once, and the restore ends CLOSED where a
finite late burst should end in proven defaults (round-three review R218
R3-F1). The D3 contract therefore makes the store's own reset (or a re-walk
request that also returns the watchdog to zero) a STAGE-1 roll-back owner,
in T1; this ticket leaves the watchdog unchanged.

## Why D3 depends on it

The D3 restore judges values by descriptor-store rules (configurations_count,
the sampling-rate list, clock_sources_count, the image-default formats a
revert writes) and proves its roll-back by the store's re-walk of the image.
A late beat entering a rule fetch could refuse or admit a value wrongly, and
one entering a re-walk's index map or name table could leave a "validated"
image with wrong names. The D3 contract therefore requires response
isolation on this face before stage 1.

## Proposed seam (prototyped)

`KL_aecp_desc_mem_guard` (the evidence's
`prototype/KL_aecp_desc_mem_guard.proto.sv`), between the store's memory
master and the memory:

- `owed` is set by an accepted request and cleared by that burst's terminal
  beat (last, or err: the bridge's error rides with its last beat);
- while `owed`, the store's request is held (not presented, ready low); every
  beat passes through to a store that sinks what it does not await;
- `owed` is reset by the HARD reset only, never by the D3 roll-back strobe,
  and is published as `debt_o`;
- the D3 writer holds every restorable owner in reset while `debt_o` is 1,
  bounded by its deadline; if the debt outlasts the deadline, the restore
  ends CLOSED rather than re-walk into it.

A memory that never ends the burst holds the store's requests for ever: the
store's own watchdog still answers every locate in bounded time, with an
error, so AECP commands keep being answered (NO_SUCH_DESCRIPTOR); nothing is
served stale.

## Acceptance

- The late-beat case: a locate presented while an abandoned burst is owed is
  answered an error or its own descriptor, never another burst's bytes;
  deleting the hold reddens it. After the late burst ends, a locate is
  served.
- D3's roll-back cases, with T1's stage-1 roll-back scope (the
  dynamic-state store AND the descriptor store): a rule fetch answered by
  the store's own watchdog (the late burst after 5,000 and after 16,000
  cycles, inside the D3 deadline) rolls back to proven defaults with the
  owners released only after the late burst, on a slot holding stage-1
  records only as well as on a full one; a late burst past the D3 deadline
  ends CLOSED before it arrives; a mutant releasing the owners without the
  debt reddens the 16,000-cycle case. The guard's debt survives the
  roll-back's own reset, which this ticket requires: its reset is the hard
  one alone.
- The store's existing suites stay green; the guard's reset is the hard
  reset alone.

## Cost

5 LUT and 1 FF out of context (the page's section 12): an estimate.

## Alternative

A memory path with no asynchronous FIFO, where the store's request reaches
`pp_desc_bridge`'s IDLE-only ready directly (`milan_cd` equal to the system
domain), holds the next request by construction; the guard costs little
enough to keep for any path.

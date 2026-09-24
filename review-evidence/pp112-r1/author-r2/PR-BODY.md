[A267] Keep SRP admission grants tied to the current declarations

Closes #112

Head: `ae7f531bc97a7277116e0df78e70c84396c499d0` on `112-stale-grant`, base `939c143`.
Commits: `73a5478` (round 1), `90e1ce1` (round 1b, test idiom), `fbabb94` and `ae7f531` (round 2).

## What the PR does

- **Freshness (round 1).** An accepted declaration, including an identical
  re-declaration, invalidates its source at every slope-pipeline stage. It
  also retires that source's grant immediately and restarts the partial
  admission round. The grant stays low until the new TSpec is evaluated.
- **Cross-source rule (round 2).** A round publishes only if every
  requesting source had a valid slope for its current declaration.
  - A round that visits a pending source is discarded. Every other source's
    grant and granted slope, and the aggregate sum and over-limit, keep
    their last published values until every requesting source has been
    evaluated.
  - The pending source's own grant stays low.
  - Capacity is released only by a withdrawal or by an evaluated shrink. A
    pending evaluation never releases it.
  - The first published round after a declaration is the greedy walk over
    all current declarations.
- **Window.** A discarded round does not strobe the round-done signal. So
  the optimistic window counts published rounds, and it can never close
  while a verdict waits for another source's pending evaluation.
- **Interfaces.** Both top-level interfaces keep their parameters and
  ports. `KL_srp_admission` gained its internal `invalidate_i` in round 1.

## Round 2: R298-1 and R299-1

**F1 (MAJOR): a pending re-declaration released its capacity to a refused
source. Fixed as the manager's design specifies.**

`KL_srp_admission` adds `pend_w`, which is set for a requesting source
without a valid current slope, and `pend_acc_r`. A round that met a pending
source leaves `grant_r`, `gslope_r`, `sum_r`, `over_r` and `round_done_o`
untouched. The fit/refusal validity terms from round 1 are now purely
defensive, and the RTL says so. This covers R298-1 S4 as well.

**Cross-source tests, run at every sampling phase.**

- *Unit, `tb/srp_admission`, two or more sources.* Source 0 is admitted at
  699.968 Mb/s and source N-1 is refused at 130.688 Mb/s. Source 0 then
  re-declares identically, shrinks to 642.688 Mb/s (N-1 still refused),
  grows to 731.968 Mb/s, or re-declares twice 5 clocks apart. Source N-1 is
  checked on every clock for no grant.
  - Controls: a freeing shrink and a withdrawal must admit N-1, and only in
    a published round that carries source 0's new state.
  - Three or more sources: a middle source re-declares while the last one
    stands refused. The last one never grants, and the first grant holds.
- *Engine, `tb/srp_top` scenario I.* Source 0 is at 69.952 Mb/s, admitted
  and ACTIVE. Source 1 or 7 is at 15.488 Mb/s, refused and Talker Failed,
  with a real Listener Ready PDU. Source 0 then re-declares identically,
  shrinks to 60.288 Mb/s, or shrinks to 17.024 Mb/s (the freeing control).
  That is 48 runs.
  - The same identical re-declaration is also accepted 1 to 40 clocks
    before a T-MRP-JOIN tick, through a new read-only `dbg_join_tick_o`
    wrapper probe.
  - Every clock is checked: no grant, no ACTIVE, no ACTIVE∧grant and no
    declared Advertise for the refused source.
  - On the wire, no Talker Advertise vector for its stream appears through
    two join periods.
  - In the freeing control, the freed source grants on the same clock as
    source 0's re-grant, its Advertise follows, and it reaches the wire.
- *Engine, `tb/srp_top` scenario J.* Two admissible fresh declarations
  (source 7, then source 0) with 0–20 idle clocks between them. Neither may
  declare a spurious Failed while one verdict waits for the other. This
  pins the window rule.

**Σ-context oracle (R299-1 required outcome).** The unit bench judges every
clock:

- Every publication must equal the greedy walk over all current
  declarations: grants, granted slopes, sum and over-limit.
- Between publications, a grant may only retire with its own declaration,
  and the aggregate holds.
- The live granted sum stays at or below the ceiling.

Scenario I checks each recorded round against the independent model in
the same way.

**Mutants.** `tb/srp_admission/mutants.py` now runs clean controls and three
mutants. Each goes through the unit suite at two and at eight sources and
through `tb/srp_top`, and each must fail its named check. The campaign
scored 12 of 12.

| Mutant | Fails at 2 / 8 sources / srp_top | Named check |
|---|---|---|
| pending-absent (round 1's rule) | 175 / 1067 / 205 | cross-source check fails 44 / 368 times; srp_top's refused-source check fails in 72 of 72 runs |
| stale-evaluation (both protections removed) | 402 / 5473 / 105 | `refused current TSpec never pulses a grant`, `H: grow has no grant pulse` |
| discarded-round-strobes | 146 / 695 / 90 | Σ-context publication check; J finds real spurious-Failed cases |

Round 1's RTL under the new bench reproduces R299-1's wire finding. A
Talker Advertise for the refused stream appears at k = 1–5, 7 and 8.

**Reviewer probes, run unchanged against an exact export of this head.**

| Probe | Result |
|---|---|
| R299-1 unit, N=2 / N=8 | 28/28 and 112/112 PASS. P1 pulses 0/4 and 0/16; P2 identical and shrink pulses 0 (base: P1 4/4 and 16/16) |
| R298-1 unit cross-source, N=2 / N=8 | 792/792 and 32832/32832 PASS. Cases A, B and D and the shrink control C all at 0 |
| R299-1 top (source 7 beside source 0) | 80/80 PASS. 16 runs with no grant, no ACTIVE∧grant, no declared or wire Advertise |
| R299-1 wire (k = 1..40 before T-MRP-JOIN) | 80/80 PASS, 0 of 40 with a Talker Advertise |
| R298-1 srp_top (sources 1/7, Ready and AskingFailed) | 192/192 PASS |
| R298-1 processor top (224 → 20000 B) | 168 checks, 0 failures, 0 admitted cycles (base: 596 cycles, 48 failures) |

The reviewers' own mutants:

- **Killed:** R299-1's M2–M6 and M7 (M7 through srp_top), and R298-1's A1–A3,
  A6 and T1.
- **Anchor no longer matches:** R298-1's A4, because the restart branch now
  also clears `pend_acc_r`. The same mutant adapted to the new text is killed
  in all three suites.
- **Survive, as documented:** R299-1's M1 and R298-1's A5 remove only the
  fit/refusal validity terms. The discard makes that edit equivalent.

**Docs.**

- 10 §6.3 has a new anchor, `sec-10-admission-cross-source`, stating the
  cross-source rule. It also covers the latency bound from the last
  declaration, the published-round window (25/33/41 clocks at M = 8), and
  aggregates latched by published rounds.
- The integrator rows for `srp_sr_admitted_o`, the slopes and `over_limit`
  state the rule. The SRP service face gets a note on how the declaration
  rate holds verdicts (R298-1 S2).
- The admission banner states the rule.
- The `KL_srp_top` banner and port comments (R299-1 S1), and the processor
  top port comments, are aligned. The "same optimistic lag" comment is gone
  (R298-1 S3, R299-1 S1).
- `tb/srp_admission`'s `make` now runs all five shapes, so N = 1/2/3/5 are
  CI-gated (R298-1 S1).

**F2 (MINOR): parent idiom gates.** Round 1b (`90e1ce1`) is kept. With this
head staged as the processor gitlink, the parent consumer gates were run on
the designated consumer checkout, parent commit `541129234178`, and all four
returned 0:

- `check_cpp_idiom`: every ratchet at 0 ≤ 0.
- `check_py_idiom`: every ratchet within budget.
- `check_rtl_source_lists`: 106 files, 4 of 4 lists.
- `pp_shadow`: 371 checks, 0 failures.

The staging was then reset. No parent commit was made.

## Grant latency

Latency is measured from the accepted declaration edge. No shape changed
from round 1.

- Unit shapes 1/2/3/5/8: 4, then 4/6, 6/9, 5/10/15 and 8/16/24 clocks.
  With a refused source competing, the latencies stay within the same sets.
- Service port at M = 8: 8/16/24 clocks. Source 0 beside a refused source
  measures 16/24, and a freed source grants on that same clock.
- At 100 MHz that is 80/160/240 ns; at 50 MHz, 160/320/480 ns.
- The bound holds from the last declaration or withdrawal. The window now
  lasts 25/33/41 clocks for a lone declaration, 17 clocks past its verdict;
  round 1 used 25 at every phase.

## Area, default shape

Measured with the repository's out-of-context recipe, `syn/ooc/srp_ooc.tcl`,
using the identical file for every tree: `xc7a100tfgg484-2`, 10 ns clock,
post-synthesis.

| Complete `KL_srp_top` | Base `939c143` | Round 1 `73a5478` | Head `ae7f531` |
|---|---:|---:|---:|
| LUTs | 7566 | 7334 | 7603 (+37) |
| Registers | 10485 | 10464 | 10502 (+17) |
| LUT as memory / RAMB18 / RAMB36 / DSP | 194 / 1 / 0 / 2 | same | same |
| WNS, OOC (worst path in the unmodified decoder) | +1.302 ns | +1.083 ns | +1.083 ns |

This answers R299-1 S2 in `syn/ooc/README.md`. Round 1's drop was
whole-engine remapping, not removed function: from base to round 1,
`u_vlan` fell 361 → 101 LUTs and `u_talker` rose 1667 → 1893. The register
difference is attributed bank by bank:

- Head − base = +17. The validity pipeline adds 10 and `pend_acc_r` adds 1.
  Synthesis adds 5 fanout replicas of `aidx_r`, and keeps `wgrant_r[7]`,
  which base had trimmed.

## Gates at `ae7f531` (all returned 0; run in the foreground, not piped; pinned simulator 5.050)

- **Docs:** `check-links.py` (847 OK), `check-matrix.py`,
  `render-wavedrom.py --check`, `make stale`, `gen_matrix.py --check`
  (92 rows, 0 untested) and `make check`.
- **Lint and whitespace:** `lint_hdl.sh` (all tops). `KL_srp_admission` is
  also linted at N = 1/2/3/5/8. `git diff --check`.
- **Suites:** `run_suites.sh`: 33 suites, 1,008,398 checks, 0 failing.
  - `srp_admission` 1138 / 12615 / 41012 / 201073 / 991231
  - `srp_top` 1527, `srp_stream_fsms` 1068, `pp_top` 1454
- **Figures:** the nvm_port figures gate, after fetching `refs/pull/13/head`.
- **Portability:** `syn/yosys/run.sh`, plus explicit off-vendor elaboration
  and checks of `KL_srp_admission` and `KL_srp_top`, with 0 problems.
- **Mutants:** the campaign scored 12 of 12.
- **Parent consumer gates:** as listed under F2.

## Limits

- No hardware was used, and physical calibration was not run.
- Hosted and act acceptance, the live parent dev candidate, and the parent
  gates at parent dev belong to the manager.
- The parent gates ran on the designated consumer checkout listed above.
- Declarations or withdrawals that keep arriving faster than their
  evaluation hold every verdict until they pause. This is documented in
  10 §6.3 and in the integrator guide.

Evidence (gate ledger, logs, probe and mutant receipts, area reports) is in
the author packet's HANDOFF.md and receipts/.

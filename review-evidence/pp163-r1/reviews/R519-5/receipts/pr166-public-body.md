[A553]

Relates to #163

The transmit arbiter's slot and state registers were fed by cones of up to 51 logic
levels at the 50 MHz clock (OOC 1x1, #638 recipe: WNS -3.562 ns, all 16 failing endpoints
in the arbiter). Two structures made them deep, and this PR cuts both:

1. **The originator's withdraw mask is registered at the top** (`org_withdraw_mask_r`). The
   mask is combinational from the originator's response, cancel and expiry choice. It fed
   the originator lane's request, the lane-queue compaction and the arbiter's
   `start_abort_i`, so the registry's identity index (`wr_ix_r`, `rows_r`), the receive
   validator's header (`hdr_src_mac_r` and the other header fields) and the response CAM
   all reached the arbiter. All three readers now take the registered copy together.
2. **The arbiter ranks its requesters in parallel.** The best-so-far scan chained its
   compares through all eight lanes (17 levels ahead of `slot_r`). The winner is now the
   eligible requester no other eligible one outranks, with ties to the lowest index. It is
   the same function: a sequential equivalence proof of the old and the new module closes
   every point, and `tb/tx_arbiter` and its five recorded mutants are unchanged.

No port, register map or parameter changes.

## Original measurement, OOC 1x1 at 50 MHz

| | Before | After |
|---|---:|---:|
| Deepest path into the arbiter (logic levels) | 51 | 16 |
| Paths into the arbiter above 20 levels (worst per start/end pair) | 146,535 | 0 |
| Startpoints in the arbiter's input cone | 1,631 | 328 |
| WNS (ns) | -3.562 | +3.337 |
| TNS (ns), failing endpoints | -37.519, 16 | 0.000, 0 |
| WHS (ns) | +0.159 | +0.159 |

Before, the deepest sources were the notification `wr_ix_r` (51 levels, -2.981 ns), the
receive validator's `hdr_src_mac_r` (50, -1.795 ns), the registry `rows_r` (up to 50) and
the notification `pend_r` (47, -3.562 ns). After, the worst five paths into the arbiter
start at the registered releases (CA builder `cancel_release_slot_o`, 14 to 16 levels,
+11.912 ns). The cut cone now ends at the new register (`wr_ix_r` to
`org_withdraw_mask_r`, 28 levels, +7.229 ns), and the originator lane queue moved from 37
levels (+0.424 ns) to 14 (+12.303 ns). The design's worst path is now elsewhere
(`u_aecp/u_ucpu` to `u_aecp/u_d3`, +3.337 ns).

Area, OOC 1x1: processor -39 LUT and +10 FF; the top's own logic -159 LUT and +6 FF; the
arbiter +49 LUT and +0 FF. The resource gate passes at both revisions.

## The added cycle

A cancellation now reaches the originator lane and the arbiter's pre-start abort one clock
after the originator takes it. For an immediate cancellation, its registered release
reaches the slot pool in that same clock. When another exchange's matched response
parks the cancellation, the mask leads the cancelled slot's release by one clock.
The race between a cancellation and the serializer's acceptance moves by one clock:

- A probe whose cancellation lands on its acceptance clock is now sent. Its exchange is
  gone (no timer, retry or deregistration), the originator drops the acceptance, and the
  pool frees the slot after the frame's last byte.
- A cancellation on the selection clock still withdraws the probe, one clock later and
  before the pool starts it.

Graded with planted mutants:

- **`tb/pp_top` section WD** (the `withdraw` target, and in the default run). It holds a
  solicited answer on its last byte until a CONTROLLER_AVAILABLE probe waits in the
  originator lane. Then it puts a superseding command's cancellation on the arbiter's
  acceptance clock (WD1) and on its selection clock (WD2, WD3). WD4 places a
  TIME_LIMITED drain on that selection clock alongside another exchange's matched
  response, grading the parked cancellation before its delayed release.
  - `withdraw_unregistered` (the old combinational path) fails WD1, WD2 and WD4.
  - `withdraw_abort_ignored` fails WD2, WD3 and WD4.
  - `withdraw_mask_dropped` and `withdraw_two_clocks` each fail WD4 only.
- **`tb/aecp_notify` section CX.** The registry monitor's cancellation arrives in the
  command's own clock and in no later one, so the top's stage is the only added clock.
  - `cancel_one_clock_late` fails CX1 (and the existing IX3).

The five arms are in `notify_mutants.py`.

## Validation

The branch merges `main` `2ad2f845` (#42, section DN and its nine controls) with `--no-ff`.
Both sides are kept in `tb/pp_top` (`README.md`, `notify_mutants.py`, `notify_phases.hpp`,
`sim_main.cpp`). DN runs before WD; each section builds its own model, so the order changes
no result. The merge changes nothing in `hdl/` or `syn/`, so the measurement above holds.

At head `ff58155657c3496d862710dab48357fd8f8d4102` against `main` `2ad2f845`:

- Before the RTL edit, every changed line was searched with a literal-text search across
  `tb/**/*.patch`, every exact-text mutation table and the bench READMEs: no hits. All 283
  bench patches apply at `main` and at the head. All 68 notify arms, #42's nine included,
  find their exact text once.
- `scripts/run_suites.sh`: rc 0 at both. `main` has 1,028,250 checks and the head
  1,028,254, with 0 failing at both. Every suite is identical except `aecp_notify` (45 to
  46) and `pp_top` (10,459 to 10,462).
- `tb/pp_top` section DN (`--domain-notify-only`) gives 15 of 15 at both, with identical
  timing lines (466 and 495 clocks). Section WD (the `withdraw` target) gives 3 of 3.
- The RTL lint, documentation, matrix freshness and portable synthesis gates all
  return rc 0 at both, with identical records. The synthesis log differs only in
  the lowered-netlist line numbers its warnings cite.
- Every campaign returns rc 0 at both, with identical records except the three new notify
  arms:
  - `notify_mutants` 65 of 65 at `main` and 68 of 68 at the head, goldens PASS. DN's nine
    records are unchanged.
  - `d3_mutants` 110 of 110, `acmp_mutants` 33 of 33, `aecp_dispatch_mutants` 40 of 40
    and `gsi_mutants` 20.
  - `aecp_mutants`, `ctr_mutants`, `name_wr_mutant`, and the `adp_engine`, `maap`,
    `srp_top`, `srp_admission` and `acmp_talker` retry campaigns all pass, with
    byte-identical driver logs.
  - `ix_new_identity_unset` now also fails the new CX1.
- Parent consumer set of 17 at dev `28f9666f`, with the 148 adoption patch and then the 22
  budget patch, run with the processor gitlink at `main` and at the head: all 17 pass at
  both.
  - Every simulation tally is identical at both, and so are the source-list, port, naming,
    evidence, docs, lint, shell and HDL analysis verdicts (0 findings).
  - Two counts move with the new bench files: the source-idiom gate counts 32 more
    first-party lines, and the port-contract gate 6 more test-only hierarchical
    observations.
  - The builder reports, at both, the one calibration arm recorded before as not run (it
    needs a reference build tree).
- The same set ran before the merge, at `cd9825c9` against `86a7b0c5`, with the same
  result.

The parent three-directive sweep on the merged pin (acceptance item 3's second half) belongs
to the pin adoption and was not run here, so this PR relates to #163 rather than closing
it.


## Round 3: merge of #69

Merge commit `5fe5ea579e27b1bf6529e97dae44c94281f35764` joins round-2 head
`ff581556` and main `c9f74b68` with both sides of all five test conflicts retained.
WD/CX still grade the registered withdrawal; PT/CK/PD/CA and IF retain #69's
per-interface registry and counter coverage. No additional RTL change is made.

The notify campaign keeps all 89 controls. The one-clock-late cancellation
control follows #69's moved single-interface choice while preserving its
immediate drain cancellation. CA4 measures the engine's settle before the
top-level stage, so its four-cycle minimum remains unchanged.

The combined top-level test runner crossed the parent's 100-line function limit
(102 lines, versus 99 and 100 in its parents). Follow-up `c4539ff` extracts its
existing tally reporting into a helper, preserving all checks and output. It adds
no RTL or timing change. The merge remains intact.

At final head `c4539ff107a6a4c7d2e4a4844182b00a2bf33c82`, the 33-suite bank
passes 1,028,290 checks. Only the expected WD/CX and #69 additions differ from
the two parents. Notify has 11 passing goldens and 89 of 89 controls killed; all
100 records match the merge. All 298 patch controls and 96 notify edits plant.
Documentation, matrix, lint and portable synthesis pass. The parent C++ gate
passes with the same records as new main.

All 14 campaigns also pass at new main and final head. Existing records match;
only the specified WD/CX and #69 additions differ. All 17 parent consumers return
rc 0 at both pins, with the inherited builder calibration skip unchanged. Fresh
shipping 1x1 OOC also passes with the same clocks, parameters and images.
Both pins use a two-thread limit and a freshly measured reference with unchanged
resource policies.
Earlier round evidence above remains recorded at its original revisions.


| Fresh OOC measurement | Main `c9f74b68` | Final `c4539ff1` |
|---|---:|---:|
| WNS | -3.562 ns | +3.337 ns |
| TNS | -37.519 ns | 0 ns |
| Failing setup endpoints | 16 | 0 |
| Hold slack | +0.159 ns | +0.159 ns |
| Maximum arbiter depth | 51 levels | 16 levels |
| Arbiter pairs above 20 levels | 146,535 | 0 |
| Processor LUT / FF | 22,517 / 18,941 | 22,478 / 18,951 |

Own logic changes by -110 LUTs and +6 FFs, within the assigned limits. The worst
arbiter slack is +11.912 ns. Neither notification `wr_ix_r` nor RX header registers
has a direct combinational path into the arbiter after the stage. Both fresh
measurements reproduce the earlier lane's area, timing and complete cone histogram.

## Round 4

At `8947bafdd62b4bf991debf7bfd8cdb73994a3a81`, WD4 covers a TIME_LIMITED cancellation parked behind another
exchange's matched response on the arbiter's selection clock. It requires the
selected probe to be withdrawn next clock, before its release, and never reach
the wire. Two new controls remove the mask from all three readers or delay it
two clocks; both fail WD4 only. The immediate-case controls remain and also fail
WD4. Architecture, top comment, verification catalogue and WD documentation now
state why the parked mask leads the release by one clock.

The default fixture postpones only the armed TIME_LIMITED deadline so the monitor
can create a live probe before expiry. The existing shipping-timeout build also
replays WD4 without that deposit: all four WD checks pass. Production parameters,
ports and register map are unchanged. This round changes tests and documentation
only; the preceding timing and area measurements stand.

At this head, all 33 suites pass 1,028,291 checks, including
9,975 in the default top build and 10,469 across its seven builds. Notify has
91/91 controls killed and 11 goldens passing. Only the two new WD records and
WD4 additions to the two existing withdrawal records differ from the base.
All other campaign records match. All 298 patch controls and all exact-text
controls plant. The four requested review probes are killed at WD4, and the
withdrawal control passes. Documentation, matrix, lint and synthesis gates pass.
All 17 parent consumers pass at the staged final pin, with the inherited builder
calibration skip unchanged.

No additional implementation measurement was needed for this round. The parent
implementation sweep remains at pin adoption, so this PR continues to relate to
#163.


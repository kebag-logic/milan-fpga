# [A267] Issue #112 / PR #114 round 2: author handoff (REVIEW READY)

Closes #112

- Head: `ae7f531bc97a7277116e0df78e70c84396c499d0`, tree `34980bea63d7d7a5cd069b9e1d5a4a95d89c52ac`
- Branch: `112-stale-grant` (local lane, not pushed). Base: `939c143333d11e2378a514f1c7b6abd4c3259bfd`
- Commits, each with a one-line subject, no body and no trailers:
  - `73a5478` Prevent SRP admission grants from using stale declaration slopes (round 1, [A259])
  - `90e1ce1` test: satisfy SRP test idiom gates without changing coverage (round 1b, [A266], kept)
  - `fbabb94` Hold every SRP admission verdict while a declared source's slope is pending (round 2)
  - `ae7f531` Record the SRP admission area for the pending-round rule and align its port comments (round 2)
- The lane working tree is clean.

Inputs read:

- The manager decision and assignment, issue #112 comment 5816928229.
- The R298-1 report (PR #114 comment 5816919660) and the R299-1 report
  (comment 5816799437).
- Their probes from kebag-logic/milan-fpga `pp112-review-evidence`, archives
  `1cec2b58` and `34309fb0`, fetched read-only into /tmp scratch.
- The [A259] handoff, `review-evidence/pp112-r1/author/HANDOFF.md`. There is
  no [A266] handoff on the branch.

No private transcripts and no management paths outside this directory were
read.

## The change (design implemented exactly)

`hdl/srp/KL_srp_admission.sv`:

- `pend_w = !invalid_w[aidx_r] && !slope_valid_r[aidx_r]` marks a requesting
  source whose current-declaration slope is not valid yet. `pend_acc_r`
  accumulates it across the round and clears on reset, on invalidation and
  at round end.
- At round end, `grant_r`, `gslope_r`, `sum_r`, `over_r` and
  `round_done_o` update only if `!(pend_acc_r || pend_w)`. Otherwise the
  round is discarded and every published verdict stays frozen.
- The pending source's own grant is already retired at invalidation (round
  1). Capacity is released only by withdrawal, through the live AND with
  req and the retire, or by an evaluated shrink in a published round.
- `round_done_o` strobes only for a published round, so the optimistic
  window in `KL_srp_top` counts published rounds. The first published round
  after a declaration always carries that declaration's verdict, so the
  window cannot close while the verdict waits for another source's pending
  evaluation. A strobe on discarded rounds would allow exactly that:
  scenario J, run as a mutant, finds 7-clock spurious Talker Failed runs.
- The fit/refusal validity terms from round 1 are now equivalent to their
  removal, because the discard covers them. They are kept as defensive
  terms, and a comment says so (R298-1 S4). Consequences for mutants:
  - R299-1's M1 and R298-1's A5 survive (documented).
  - The own campaign's stale-evaluation mutant now removes both protections.

Single-source latency is unchanged: the LATENCY lines are identical to round
1 (unit N=8 256 lines, srp_top 72 lines, before the new cases were added).
Ports are unchanged.

## Tests

- **`tb/srp_admission/sim_main.cpp`, Σ-context oracle, every clock:**
  - live Σ ≤ ceiling;
  - on `round_o`, the grants, granted slopes, sum and over-limit equal the
    greedy walk over all current declarations;
  - otherwise, grants and granted slopes equal the previous clock except the
    source whose declaration this edge captures, and sum and over hold.
- **Unit cross-source, at every phase:**
  - N ≥ 2: `pending_redeclaration_keeps_capacity` (identical / shrink
    643M / grow 732M / double) with a per-clock watch on N-1;
  - N ≥ 2: `released_capacity_admits` (freeing shrink, withdrawal);
  - N ≥ 3: `pending_middle_keeps_capacity`.
- **`tb/srp_admission/Makefile`:** `make` now runs all five shapes; the N=8
  tally prints last (R298-1 S1).
- **`tb/srp_top` I, `check_pending_redeclaration_frees_no_capacity`:**
  - sources 1/7 × frame 1051 (identical), 900 (shrink, still refused) and
    224 (freeing control) × 8 phases = 48 runs;
  - plus 40 runs with the identical re-declaration accepted k = 1..40 clocks
    before T-MRP-JOIN, the tick read from a new read-only `dbg_join_tick_o`
    wrapper probe. It is named so that R299-1's `join` patch still applies.
  - Per clock: no grant, no ACTIVE and no declared Advertise for the
    refused source; each round equals the model; between rounds a grant
    only retires.
  - Wire: no Talker Advertise vector for its stream through two join
    periods. The freeing control grants on the same clock as source 0's
    re-grant and reaches the wire.
- **`tb/srp_top` J, `check_optimistic_window_outlives_a_held_verdict`:**
  source 7 then source 0, gaps 0/4/8/12/16/20, 8 phases. Neither declares
  Failed on any clock, and a held verdict publishes with source 0's.
- **H** now prints `window=` per case: 25/33/41 clocks at M=8; round 1
  measured 25 everywhere.
- **`tb/srp_admission/mutants.py`:** controls plus stale-evaluation,
  pending-absent and discarded-round-strobes, each through the unit suite
  at N=2, N=8 and through srp_top. Named-check kills: 12/12
  ([receipts/mutants](receipts/mutants), [gates/mutants.log](receipts/gates/mutants.log)).

Round 1's RTL (`73a5478`) under the final srp_top bench fails 205 of 1527
checks. It reproduces R299-1's wire hits at k = 1–5, 7 and 8
([receipts/probes/round1-rtl-under-head-srp_top.log](receipts/probes/round1-rtl-under-head-srp_top.log)).

## Reviewer probes at the exact head (git archive of ae7f531, pinned 5.050)

| Probe | Head | Base |
|---|---|---|
| R299-1 unit N=2 | 28/28 PASS, P1 0/4, P2 0/2 + 0/2 | P1 4/4 (4 FAIL) |
| R299-1 unit N=8 | 112/112 PASS, P1 0/16, P2 0/8 + 0/8 | P1 16/16 (16 FAIL) |
| R298-1 unit N=2 / N=8 | 792/792, 32832/32832; A/B/C/D all 0 | — |
| R299-1 top | 80/80; 16 runs, all counters 0 | — |
| R299-1 wire | 80/80; 0 of 40 with Talker Advertise | — |
| R298-1 srp_top | 192/192 | 192/192 (base HDL) |
| R298-1 pp_top | 168 checks, 0 failures, 0 admitted cycles | 596 cycles, 48 failures |

Reviewer mutants at the head:

- R299-1: M2–M6 killed in all three benches. M7 is killed by srp_top and
  survives the unit benches, which have no top. M1 survives; it is
  equivalent, as documented.
- R298-1: A1–A3, A6 and T1 killed. A5 survives (equivalent, as before). A4
  reports ANCHOR-MISSING, because the restart branch now also clears
  `pend_acc_r`. The same edit adapted to the new text is killed at N=2
  (65), N=8 (1949) and srp_top (133).
  ([receipts/probes](receipts/probes)).

## Docs

- 10 §6.3 has a new anchor, `sec-10-admission-cross-source`, stating the
  rule. It also covers the latency bound from the last declaration or
  withdrawal, the published-round window with 25/33/41 measured, and
  aggregates latched by published rounds (the live Σ never exceeds them).
- The integrator guide:
  - `srp_sr_admitted_o` states the cross-source rule;
  - the slopes and `over_limit` rows say latched by published rounds;
  - the SRP service row has a rate note (R298-1 S2).
- The admission banner states the rule, and its port comments now say
  "latched by published rounds".
- The `KL_srp_top` banner, the window comments and the port comments for
  `sr_admitted_o`, `sum_slope_bps_o` and `over_limit_o` (R299-1 S1).
- The processor top port comments. `srp_granted_slope_bps_o` no longer
  says "same optimistic lag" (R298-1 S3).
- The unit README and the srp_top README.
- `syn/ooc/README.md` records the area and its explanation (R299-1 S2).

## Grant latency (receipts/latency-summary.txt)

- Unit shapes, from the declaration capture edge:
  - N=1: 4 clocks
  - N=2: 4/6
  - N=3: 6/9
  - N=5: 5/10/15
  - N=8: 8/16/24
- The cross-source cases stay within the same sets.
- srp_top at M=8, from gate acceptance: 8/16/24. Source 0 beside a refused
  source measures 16/24, and the freed source grants on that same clock.
- At 100 MHz: 80/160/240 ns. At 50 MHz: 160/320/480 ns.
- The window is 25/33/41 clocks, 17 past the verdict round (round 1: 25).

## Area (Vivado 2026.1, identical `syn/ooc/srp_ooc.tcl`, xc7a100tfgg484-2, 10 ns)

| KL_srp_top | Base 939c143 | Round 1 73a5478 | Head ae7f531 |
|---|---:|---:|---:|
| LUTs | 7566 | 7334 | 7603 (+37) |
| FFs | 10485 | 10464 | 10502 (+17) |
| LUTRAM / RAMB18 / RAMB36 / DSP | 194/1/0/2 | same | same |
| u_admission LUT / FF | 782 / 862 | 503 / 841 | 749 / 879 |
| WNS (worst path in unmodified u_decoder) | +1.302 | +1.083 | +1.083 |

How the area was measured:

- Base reproduces round 1's published base exactly.
- Head `fbabb94` and head `ae7f531` give identical totals; `ae7f531`
  changes only comments on top of `fbabb94`.
- Round 1's drop is whole-engine remapping: `u_vlan` 361 → 101, `u_talker`
  1667 → 1893, `u_encoder` 1181 → 1252.
- Register banks per build are in
  [receipts/area/analysis/banks-compare.txt](receipts/area/analysis/banks-compare.txt).
- Head − base, +17 FFs:
  - +10 validity pipeline;
  - +1 `pend_acc_r`;
  - +5 `aidx_r` fanout replicas;
  - +1 `wgrant_r[7]`, which base trimmed.
- Round 1 − base, −21 FFs:
  - +10 validity pipeline;
  - +1 `wgrant_r[7]`;
  - −32 `wgslope_r[7]`, which is always zero, trimmed only in round 1.
- Admission LUT primitives: 950 → 712 → 944, in 782 / 503 / 749 LUTs.

Receipts are in [receipts/area](receipts/area). The per-cell and per-bank
reports come from the identical recipe plus one report command, run in
scratch at `fbabb94`; its totals are identical to `ae7f531`.

## Gates at ae7f531: [receipts/gates/ledger.tsv](receipts/gates/ledger.tsv)

Every gate returned 0 and ran in the foreground, logged to a file and never
piped. Pinned Verilator 5.050 was first on PATH, and `tb/` build products
were cleaned first.

- **Docs and structure:**
  - `verilator --version`
  - `check-links.py`
  - `check-matrix.py`
  - `render-wavedrom.py --check`
  - `make stale`
  - `gen_matrix.py --check`
  - `make check`
  - `git diff --check 939c143 HEAD`
- **Lint:** `lint_hdl.sh`, plus `KL_srp_admission` at N = 1/2/3/5/8 with
  the same flags.
- **Elaboration:** sv2v + yosys `check -assert` of `KL_srp_admission` and
  `KL_srp_top`.
- **Suites:** `run_suites.sh`, 33 suites, 1,008,398 checks, 0 failing.
- **Figures:** `git fetch --no-tags origin refs/pull/13/head` and
  `make -C tb/nvm_port figures`.
- **Portability:** `syn/yosys/run.sh`.
- **SRP suites:** `make -C tb/srp_admission` (1138 / 12615 / 41012 /
  201073 / 991231), `tb/srp_top` (1527), `tb/srp_stream_fsms` (1068) and
  `tb/pp_top` (1454).
- **Mutants:** `mutants.py`, 12 checks, 12 PASS.

The `fbabb94` round is kept in
[receipts/superseded-fbabb94](receipts/superseded-fbabb94) and was all
green too.

## Parent consumer gates ([receipts/parent](receipts/parent))

Run in $LANES/pp112-parent-consumer at parent commit
`54112923417837dffc8722890e2beb733468f441`. The procedure was
`git -C protocol-processor fetch <lane> HEAD`, then
`checkout --detach FETCH_HEAD`, then `git add protocol-processor`; the
gitlink was ae7f531. Every gate returned 0:

- `check_cpp_idiom.py`: every ratchet 0 ≤ 0, no refusals.
- `check_py_idiom.py`: every ratchet within budget.
- `check_rtl_source_lists.py`: 106 files, 4 of 4 lists.
- `make -C tb/verilator/pp_shadow -j8`: 371 checks, 0 failures.

Then came `git reset -q protocol-processor`. The parent index is clean, and
`git status` shows only ` M protocol-processor`: the submodule checkout was
left detached at ae7f531, as the round-1 author left it at their head. It
was clean at 73a54787 before this session. No parent commit or push was
made.

## Final state and not done

- No push, PR edit, merge, parent commit, sub-agent or hardware action.
- The "[A267] REVIEW READY" comment is posted on issue #112; its URL is in
  `review-ready-url.txt`.
- Scratch was deleted at the end: the /tmp/a267-ev evidence fetch, and
  /tmp/a267-work with its trees, builds and Vivado runs.
- No toolchain, SDK or virtualenv is in this directory.

Limits:

- Physical calibration was not run, and there was no hardware.
- Hosted and act acceptance, the live parent dev candidate, and the parent
  gates at parent dev belong to the manager.
- Round 2 changes one behaviour beyond the design text: the optimistic
  window of a lone declaration lengthens from 25 to 25/33/41 clocks at
  M = 8. This is inherent to counting published rounds, is documented, and
  is pinned by H.
- Starvation under declarations arriving faster than their evaluation (all
  verdicts held) is documented in 10 §6.3 and in the integrator guide.

Files:

- `PR-BODY.md`: the full updated PR #114 body.
- `REVIEW-READY.md`: the issue comment payload.
- `receipts/`: all logs.
- `MANIFEST.sha256`: hashes of every file.

[A284]

Closes #116

Status: requested five-file patch committed; all required gates passed;
every before/after suite count and mutation verdict matches.

Branch: `116-parent-gates`
Base: `a8f8ce810ddba1816cd129d0afcd71e6e02ade1b`
Head: `a43d07668ff03efc299fbbf2a3891f2aa90255f7`
Commit subject: `Satisfy parent port, naming and test evidence gates`

The patch adds rationale directly above both literal-bound `u_nvm_arb`
connection runs. It rewords the two port comments and preserves the admission
latency figure in ordinary prose above the assignment. It removes one host
deadline from each of the three mutation runners and documents their bounds.
Only the five requested files changed. RTL tokens are unchanged; each runner's
syntax tree differs only by the removed deadline keyword. See
[scope verification](scope-verification.json) and [complete patch](change.patch).

The full suite bank is byte-identical before and after: 33 suites, 1,008,919
checks, zero failures. All five admission shapes match as well: 1,138 / 12,615 /
41,012 / 201,073 / 991,231 checks at 1 / 2 / 3 / 5 / 8 sources.
Every suite count and every mutation campaign's verdict table is recorded in
[COMPARISON.md](COMPARISON.md), with complete raw logs in `before/` and `after/`.

All four mutation campaigns returned 0 before and after. The descriptor
mutation has the same completed 18/17/1 tally and named failure. All 15 GSI
rows and their named-failure arrays match; every simulation log is identical.
All 12 SRP verdicts, tallies, latencies and named failures match. The complete
NVM figure output, including every arm, mutation, model and matrix row, is
byte-identical.

Every gate in the repository's CI workflow returned 0, as did the complete
documentation check. This includes documentation links, compliance and module
matrices, waveform exports, diagram staleness, lint, the full suite bank,
the NVM figure campaign and portability checks. Lint covered 40 tops;
portability covered 35 tops and the required memory-mapping assertion.
Exact commands, exit statuses and logs are in
[processor gate records](processor-gates/commands.json) and
[final suite/campaign records](after/commands.json). Gate commands ran directly
without output pipelines.

Parent baseline: `35f0695815c202392b6b4806bb9f59dd110687ed`
Parent local branch: `508-pp-pin-adopt`
Parent local head: `ea96db3246d34dbf3ece2d1aca2a9aaf24596216`
Parent commit subject: `Adopt processor parent gate fixes for issue 116`

The parent fetched the processor head from the local checkout after processor
validation passed. Its sole committed change is the processor gitlink.
Both commits have one-line subjects, no bodies and no trailers.

| Parent gate | Base processor exit | Candidate processor exit |
|---|---:|---:|
| Port contracts | 1 | 0 |
| Naming | 1 | 0 |
| Test evidence | 1 | 0 |

The controls identify the issue's seven unexplained tied connections, two new
naming identities, and six deadline files against a budget of three.
All three rule files and budgets remain byte-identical. See
[control records](control/commands.json), [control explanation](CONTROL.md),
[original hashes](consumer-gate-inputs-before.json) and
[final hashes](consumer-gate-inputs-after.json).

All ten requested parent checks returned 0: the three gates above, both idiom
checks, frontend analysis, RTL source lists, processor source self-test,
documentation, and processor integration. Frontend analysis matched its
existing four-finding ratchet. Integration passed 371 checks with zero
failures. Exact commands and results are in
[parent gate records](consumer-gates/commands.json).
The integration suite also passed 371 checks at the base processor pin;
every named verdict matches the candidate. Both runs used their matching
committed parent gitlinks, and the candidate branch and pin were restored.
See [integration comparison](integration-comparison/comparison.json) and
[its command records](integration-comparison/commands.json).

[Final state](final-state.json) records commit identities, scope, clean
checkouts and validation exit statuses. Termination arguments for each changed
runner are recorded below. [PR-BODY.md](PR-BODY.md) is the prepared review text.
Review notification: [posted on issue #116](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/116#issuecomment-5822645583).

Both commits remain local. No push, pull request change, merge or hardware
operation was performed.

Termination arguments:

- `tb/desc_mem_guard/mutate.py` runs one finite build recipe and one
  `--late-only` simulation. In `tb/desc_mem_guard/sim_main.cpp`, `BOUND` is
  4096 + 64 = 4160. Boot uses four reset cycles and at most `BOUND` cycles;
  each of eight reads uses at most `BOUND` cycles plus one trailing tick;
  the final drain uses 80 cycles. Thus the selected case terminates within
  37,532 simulated cycles even when a response never arrives. The mutation
  removes only the two request holds and cannot change those harness limits.
  The driver still requires the completed case, exact corrupt data, exact
  18/17/1 tally, and named failing assertion.
- `tb/pp_top/gsi_mutants.py` iterates over 13 fixed mutations plus initial
  and restored controls, with one finite build and one simulation each.
  `--gsi-internal-only` selects `InternalStreamInfoPhase::run`, not the
  full suite. Its boot loop has a 400,000-cycle limit; queries have
  500 * 100 = 50,000 cycles. Frame waits decrement `wait_ms * 100`, with
  the largest selected wait 5000 * 100 = 500,000 cycles. Other observation
  windows use counted iterations, input frames have finite lengths, and
  queue scans remove an element or advance an iterator without stepping
  the DUT. The selected phase never calls the timer-alignment helpers.
  Each of the 15 fixed variants therefore finishes without needing a host
  deadline. Build failures remain refusals; mutant success still requires
  a completed simulation and its named failing response check.
- `tb/srp_admission/mutants.py` runs exactly four source variants through
  three finite recipes, for 12 legs. The admission harness fixes `N` at
  2 or 8, bounds every source/phase loop by `N`, and bounds settle/latency
  observations by `3*N + 4` (10 or 28 cycles). The integrated harness
  bounds service waits by 200,000 cycles and frame waits by
  `timeout_ms * 40`; observation windows and case tables are finite.
  Its handshake-driven input loop also terminates: the unchanged decoder
  deasserts ready only while draining at most three or four packed values,
  decrementing the drain count each cycle, with no downstream ready input.
  Each finite input frame therefore consumes at most five cycles per
  presented byte, plus the fixed trailing idle. The timer-alignment loop
  advances the unchanged 40-cycle millisecond prescaler and reaches phase
  250..350 within a 1000-millisecond period.
  The join-edge loops observe the unchanged recurring 200-millisecond
  cadence, whose expiry rearms itself independently of admission. The
  32-slot timer sweep takes 34 cycles and fits inside each 40-cycle tick;
  the fixed outstanding arm queues drain while those helpers present no
  further service request or input frame. The three mutations change
  admission validity/publication only; none changes
  the decoder, prescaler, timer service, or cadence. These structural
  bounds cover all 12 selected legs, including those waits without a
  harness counter. Named checks and completed tallies remain required.

The build portions have finite source/dependency lists and no retry or watch
loop. The arguments above concern the actual fixed campaigns and normal
process execution; a host or compiler failure is not a detected mutation.

# Contributing — house rules that keep this repo shippable

Short version: SystemVerilog only, banner-documented, one-line commits,
lane-per-worktree, every change grows the test suite, and nothing merges on
"looks right" — TB numbers or silicon numbers.

## Contents

- **[1. HDL house style (Cemal Dogan / Oguz Kahraman school)](#1-hdl-house-style-cemal-dogan--oguz-kahraman-school)** -- The naming, reset and banner conventions a new `.sv` file must follow, ending in the CDC rule that cost us the 07-24 link-guard deadlock: clock-liveness observers must be `reset_less`.
- **[2. Workflow](#2-workflow)** -- The issue-to-merge lane: an issue moves to *In progress*, a branch is cut **from the issue**, the work lands on it, a PR opens, review runs as **multiple agents with cleared context**, and only then does it merge back to `dev`. Plus one lane = one worktree, one-line commits, and two traps with history: `cp -r` (never symlink) `third_party/` into a worktree, and rebuild `LAYOUTS` merges semantically rather than by marker-union.
- **[3. Verification bar](#3-verification-bar)** -- What a change owes before it merges: a self-checking Verilator harness under `tb/verilator/<name>/`, a ratcheted `scripts/lint_rtl.py --check` that fails on any new lint violation, a justification for every `lint_off`, a matrix row that only turns ✅ with a runnable test, and timing claims quoted with the full cell recipe rather than a bare WNS.
- **[4. Bench discipline (the expensive lessons)](#4-bench-discipline-the-expensive-lessons)** -- Three rules paid for on hardware: ≥ 8 min AX boot probes, dump a QSPI slot before overwriting it, and regenerate every window map from `csr.csv` on any gateware block-set change.
- **[5. Code quality](#5-code-quality)** -- The numbered cross-language maintainability contract: the Boy Scout rule that keeps cleanup out of functional changes, and the rules that give each cleanup wording, examples, exceptions and a measurement instead of a taste argument.

## 1. HDL house style (Cemal Dogan / Oguz Kahraman school)

- **SystemVerilog only** for new HDL. Python (migen/LiteX) is SoC *glue*,
  never new datapath logic.
- File head: SPDX line + banner comment stating what the module is and the
  one design decision that matters. `` `default_nettype none `` at the top,
  `` `default_nettype wire `` at the bottom.
- Ports documented **inline with `//!`** — the port list IS the spec.
- Naming: `_r` registered, `_w` wire/comb, `_p` one-cycle pulse, `_S` FSM
  states, `_C`/`_P` params. Named `always_ff`/`always_comb` blocks
  (`begin : name … end : name`). A boundary whose value has a unit carries it
  in the name beside these suffixes (`ring_len_bytes_i`, `timeout_cyc_c`);
  the qualifier table is Rule 4 of the
  [code quality guide](docs/development/CODE_QUALITY.md#rule-4-use-intention-revealing-names-and-explicit-units).
- Reset: synchronous, active-low `rst_n`, every register reset. 2-space
  indent.
- CDC: only via the blessed primitives (`cdc_pulse`, `cdc_handshake`,
  toggle+sync); **clock-liveness observers must be `reset_less`** — never
  place an observer inside a reset cone its consumer drives (the 07-24
  link-guard deadlock).

## 2. Workflow

### 2.1 The issue-to-merge lane

Every change of substance runs this lane, in this order. The point of writing
it down is that the two steps people skip — cutting the branch **from the
issue**, and reviewing with **cleared context** — are the two that keep the
board honest and stop a reviewer from rubber-stamping their own reasoning.

The long-gate policy is machine-checked against the
[Milan feature status ledger](docs/reference/MILAN_FEATURE_STATUS.md):

<!-- milan-feature-status:start -->
| Feature ID | Status | Canonical value |
|---|---|---|
| `verification.long-gate-policy` | `implemented` | `local-required, remote-required` |
<!-- milan-feature-status:end -->

The active `dev merge bar` repository ruleset requires a pull request and these
seven exact status-check contexts: `rtl-fast`, `docs-check`,
`wire-accountability`, `docs-check-no-git`, `elaborate`, `verilator-suites`, and
`yosys-portability`. The required-check policy is loose, so an intervening
merge does not invalidate exact-head evidence by demanding another long Yosys
run. It has no bypass actor; deletion and non-fast-forward updates of `dev` are
also forbidden. A skipped conditional job satisfies its named context, but no
required workflow may use path- or branch-level skipping that prevents the
context from being emitted. The exhaustive aggregates may skip only after
`full-ci-gate` succeeds and explicitly selects the no-op path; a failed,
cancelled, or output-less selector makes both aggregates run and fail closed.

```mermaid
flowchart LR
    B[Backlog] -->|scope settled,<br/>no open decision| R[Ready]
    R -->|take it| P[In progress]
    P --> BR[branch cut FROM the issue<br/>gh issue develop N]
    BR --> W[work + gates green]
    W --> PR[open the PR]
    PR --> RV[In review<br/>multiple agents, CLEARED context]
    RV -->|findings| W
    W -->|fixed| RV
    RV -->|2 positive:<br/>1 own + 1 EXTERNAL| G[validate candidate merge result<br/>with the FULL local bar]
    G -->|regression| W
    G -->|clean| M[merge to dev]
    M --> C[branch stops moving<br/>run containment]
    C -->|finding| F[follow-up issue + PR]
    C -->|clean| D[card to Done<br/>issue closed by the merge]
```

1. **Move the issue to *In progress*** on the project board before the first
   edit, not after. An issue in *Ready* that somebody is already working is
   how two lanes collide — which has happened: the dynamic-state store was
   built twice on 2026-08-16 because the issue was filed after the work
   started.
2. **Cut the branch from the issue**: `gh issue develop <N> --base dev`.
   This links the branch and issue on GitHub. Since 2026-08-22 `dev` is the
   repository's default branch, so a PR body carrying `Closes #N` closes the
   issue when the PR merges; the board's *Done* still waits for the post-merge
   containment check. Before that date `main` was the default and the keyword
   never fired, which is why older issues were closed by hand.
3. **Do the work on that branch**, with the Section 3 verification bar met *on the
   branch* — a PR is not the place to discover the sweep is red.
4. **Open the PR** against `dev`, with the template below and the
   self-test results as a **comment** (a comment is evidence, not approval).
   After every pushed PR head, start the supported local workflow replica:

   ```bash
   python3 -I /absolute/path/to/trusted-dev/scripts/act_ci.py --pr <number>
   ```

   Run that command from the candidate worktree, but load the script only from
   a separate clean worktree at the PR's current remote `dev` base; candidate
   host-side orchestration Python must never execute on the host. The candidate
   runner's offline self-test may execute only inside its disposable CI job.
   `act` must be used instead of waiting for GitHub Actions to finish. For a
   changing draft, select only applicable
   workflows with repeated `--workflow` options; for a ready head, the default
   runs all four. Hosted required contexts continue in parallel and remain part
   of the merge bar; the local runner forwards no credential and publishes no
   status. See
   [Act-first local replication](docs/testing/CI_WORKFLOWS.md#act-first-local-replication).
5. **Review with multiple agents, each with CLEARED context.** Not forks of
   the author's session: agents that have never seen the reasoning that
   produced the diff. An agent that helped write a change will re-derive the
   same blind spot when asked to check it. Give each one a different lens and
   let them read the diff cold. **The lens list is
   [`AGENTS.md` reviewer procedure](AGENTS.md#6-reviewer-procedure)** —
   `Conformance`, `RTL`, `Robustness`,
   `Tests`, `Docs` — and those five names are the ones a completion ledger
   counts, so report coverage in them. The angles this file used to list here
   (clause conformance, wire format and response sizing, test adequacy, whether
   the tests can actually fail) are examples of what to look at within them,
   not a second list to report against.

   **Two positive reviews are the merge bar, and one of them must be
   EXTERNAL.** One from this lane's own review agents, at least one from an
   agent outside it. A lane reviewing only itself converges on its own
   assumptions no matter how many agents it spawns — the cleared context stops
   an agent inheriting the *reasoning*, not the lane inheriting its own
   *premises*. Findings are not a review verdict: a round that returns
   blockers is answered and then **re-reviewed**, and it is the re-review that
   can be positive. Do not count the round that found the bugs as the sign-off
   for the fixes.

   **Keep the PR comment short.** State what the PR does and that it is
   validated, with the gate results. The findings, the mutation tables and the
   clause arguments belong in the review itself and in the commit messages —
   a PR thread that reprints them is a PR thread nobody reads to the end.

   **Prefix every PR message with the role.** Session 0 starts every PR body
   and comment with `[A0]` when authoring, or `[R0]` when reviewing. Every other
   session replaces `0` with its assigned session number and keeps that number
   when its role changes. The prefix states which responsibility and session
   the message represents.
6. **Merge back into `dev`** only once the findings are answered, and
   **not while a review round is in flight.** A round that has not reported is
   a round outstanding; merging past it is merging unreviewed code with a
   review thread attached.

   Twice this went wrong, and the two cases are not the same shape - which is
   the point. One merged with a round genuinely mid-flight; the other merged
   having met the bar, while review that was still happening went on to find
   three more blockers. The rule that covers both is that the merge waits for
   review to be **finished**, not for a quota of positives to be reached:

   | PR | merged | state at that moment | cost |
   |---|---|---|---|
   | #77 | 2026-08-16 18:10 | round 3 answered, a positive validation posted 32 min earlier - the stated bar was **met** | review did not stop there, and rounds 4 and 5 returned NEGATIVE afterwards (6 was positive): an ungraded refusal arm where mutating the code was silent, and a test that could not fail. Re-landed as #85 |
   | #86 | 2026-08-17 07:54 | a round running, which then found a hole in its own fix | three commits stranded on the branch; re-landed as #89, tracked by #87 |

   Both were recoverable and neither was noticed by anything except a reviewer
   checking by hand. The failure is silent by construction: `gh pr view` says
   `MERGED`, CI is green, and the branch still has commits ahead of the merge.
   Nothing in the lane compares those two facts unless step 7 does.

7. **Validate the candidate merge result, then prove containment.** A merge is
   a change nobody wrote and nobody reviewed, and *"Merge made by the 'ort'
   strategy"* is not evidence of anything. Before pressing merge, construct a
   candidate from the latest `origin/dev` and the reviewed PR head, then
   gate that tree exactly as Section 3 gates a hand-written one: full Verilator sweep,
   both repos' suites, behave, the lint ratchet, and Yosys. If the reviewed head
   directly descends from the unchanged base, its tree is the candidate merge
   tree; record both object IDs with the local gate results.

   This is not defensive box-ticking. On 2026-08-16 two lanes independently
   added the *same* six AECP settings-face pins to `KL_pp_shadow.sv` — one
   tied off, one connected. Git reported **no conflict** and kept **both**,
   producing duplicate pin connections that would not elaborate. Nothing but
   running the tools on the merged tree could have found it. The same merge
   also silently re-armed a VERSION story describing commands that had been
   split out, and restored an inventory row for an opcode the engine no longer
   decodes.

   **After merge, check that it actually took the branch:**

   ```bash
   python3 scripts/check_merge_containment.py origin/<branch>
   python3 scripts/check_merge_containment.py --merged-prs   # the last 20 PRs
   python3 scripts/check_merge_review_integrity.py           # NEGATIVE merges / open Issues
   ```

   It exits non-zero and names the count when commits are left behind. Replayed
   against the two merge points in step 6 it reports **3** stranded commits for
   #77 and **4** for #86 - the latter is 3 as of that merge plus the one pushed
   during the #89 re-land. Nobody was told either number at the time.

   **Run it when the branch stops moving, not at the merge button.** Both
   incidents were *contained* at the instant they merged; the commits that
   ended up stranded were pushed afterwards as review activity continued. For
   #86 a round was in flight. For #77 the stated bar had been met, but review
   did not stop. A check run at merge time cannot see later pushes. The moment
   that catches them is the one where the card moves to *Done*. Once
   containment is clean, move the project item to *Done*; the merge closed the
   issue itself when the PR body carried `Closes #N`, so close it by hand only
   when it did not.

   `--no-fetch` disables Git ref refresh only. A `--merged-prs` sweep still
   queries GitHub for the merged PR list and branch timeline evidence.

   Its `--selftest` runs inside `scripts/run_all_suites.sh` next to
   `suite_tally.py`'s, so the tool cannot rot into a green that means nothing
   between merges. The check *itself* is still a thing a person runs: nothing
   here schedules a post-merge action. Every push to `dev` runs the hosted
   gates on the merge result (`rtl-fast.yml`, `rtl.yml`, `docs.yml` and
   `elaborate.yml` all subscribe `push: dev`; the event contract is in
   [docs/testing/CI_WORKFLOWS.md](docs/testing/CI_WORKFLOWS.md)), and the
   Verilator sweep carries this self-test with it, but no workflow runs
   `check_merge_containment.py --merged-prs`, so a live containment verdict is
   still rendered by hand.

   **Do not hand-roll it by reading `git log` output.** The script uses
   `git rev-list --count` and `git merge-base --is-ancestor` because one prints
   a single integer and the other answers only through its exit status: neither
   needs its prose parsed, so neither can be half-read or mis-scraped. #89's
   description claimed a fast-forward that was not one, off a `git log A..B`
   that came back empty in the author's terminal. A cause was proposed at the
   time and a later attempt could not reproduce it in twelve variations, so it
   stands unexplained - which is itself the argument. A check whose failure
   mode nobody can characterise is not one to build on, whatever the cause
   turns out to be.

   Three merge-specific traps worth naming, all paid for:

   - **Push the submodule before the superproject.** A superproject pin to a
     processor commit that only exists on a feature branch dangles the moment
     that branch is deleted, and `git submodule update` on a fresh clone fails
     with no useful message.
   - **A conflict in the µcode or the engine means re-running
     `protocol-processor/scripts/check_upc_map.py`.** A merge that lands the engine's dispatch
     constant from one side and the microprogram's entry point from the other
     does not fail to elaborate — the µCPU executes ROM fill and answers a
     well-formed response carrying garbage.
   - **The two long GitHub aggregates and their local gates are independently
     required.** `verilator-suites` and `yosys-portability` must both be emitted
     on the PR head and must conclude successfully for RTL/tooling-relevant
     work. A docs-only PR emits them as successful skipped contexts. Before the
     PR is marked validated, run both equivalent gates locally and record their
     results on the PR:

     ```bash
     suite_logs=$(mktemp -d)
     scripts/run_all_suites.sh "$suite_logs"
     syn/yosys/run.sh
     ```

     A hosted pass does not replace the local evidence, and a local pass does
     not waive the ruleset's hosted contexts.

Two board rules that go with it:

- **Backlog vs Ready is about decisions, not size.** A large task with settled
  scope is *Ready*. A small task with an open trade-off is *Backlog* until
  somebody makes the call — file the options and the recommendation in the
  issue rather than picking silently.
- **A superseded issue is moved to *In review*, never quietly closed**, with a
  comment saying what landed, where, and which acceptance criteria were **not**
  met. Closing it hides the divergence.

### 2.2 Lanes and traps

- **One lane = one worktree = one branch = one PR** (`~/milan-avb-multiwork`
  pattern). Copy (`cp -r`), never symlink, `third_party/` into a worktree —
  a symlink escapes to the main repo and builds silently stale RTL; then
  delete the copied submodule's `.git` file.
- **A fresh worktree inherits no submodules, and the honest local bar needs
  three of them.** `git worktree add` does not initialise submodules, so before
  any local gate run, in one command:
  `git submodule update --init third_party/verilog-axis protocol-processor gptp-processor`.
  These three are what the Verilator suites, the Yosys gate and
  [`scripts/lint_rtl.py`](scripts/lint_rtl.py) read, and are exactly what CI
  initialises. Two of them, the processor pair, are also what
  [`scripts/xvlog_gate.py`](scripts/xvlog_gate.py) analyses, and it refuses the
  same way -- but against the **gitlink** and then against the pinned **bytes**,
  so a standalone clone dropped at the path, a checkout moved off the pin, and a
  local edit the index has been told to keep quiet about are all refused, not
  counted. Lint now REFUSES (exit 2, not the
  ratchet-tighten exit 1) rather
  than under-count when one is absent (#186): a count over an incomplete
  resolution set drops findings and would invite a tighten to a number the real
  tree cannot meet. The `external` submodule is SSH-only and no sim, lint or
  synthesis gate reads it, so it is deliberately NOT in that command.
- **Commits: one line, no trailers.** The private bench suite is referenced
  only as *the bench suite* (evidence token `BENCH`) in committed text —
  never by any external name.
- PRs use the template: Status / Description / how-to-reproduce / how-to-
  validate / DoD. **Self-test results go in a PR comment** — a comment is
  evidence, not approval. Maintainer merges by default.
- **`LAYOUTS`-style merges in [`tests/steps/`](tests/steps) are semantic, never
  marker-union**: rebuild each command's block from its owning commit
  verbatim (naive unions broke main twice; a third time gets you named in
  this file). The rule was written for the PDU-generator step file that carried
  the 1722.1 command layouts; that file went with the AECP/ACMP/ADP step suites
  on 2026-08-13, and the rule stands for whatever table-shaped step module
  replaces it.

## 3. Verification bar

- Every functional RTL change ships with a self-checking Verilator harness
  under `tb/verilator/<name>/` (`make` = build+run, exit code is the gate).
  See [`docs/testing/TESTING.md`](docs/testing/TESTING.md) for the suite index and tiers.
- **Lint before you push**: `python3 scripts/lint_rtl.py --check` (~10 s,
  needs only the Verilator you already have). It sweeps every module in
  `hdl/` and fails on a **new** violation — today's 150 are grandfathered by
  a per-directory ratchet in [`scripts/lint.budget`](scripts/lint.budget) and
  printed in full, so the backlog is never hidden. Lowering an entry is a
  normal commit: `python3 scripts/lint_rtl.py && git add scripts/lint.budget`.
  Raising one is not an option — fix the finding, or add a `RULE_WAIVERS`
  entry naming the reason **and where the reason is recorded**.
  `--pragmas` alone is instantaneous and is the useful pre-commit hook:
  `echo 'python3 scripts/lint_rtl.py --pragmas' >> .git/hooks/pre-commit`.
- **Parse with Vivado's front-end before you push, on a bench box**:
  `python3 scripts/xvlog_gate.py --check`. The lint ratchet, the Verilator
  sweep and the Yosys gate all lower SystemVerilog through Verilator/sv2v, so a
  construct Vivado is stricter about (use-before-declaration is the first one
  found) is invisible to the whole bar (#132). The gate runs `xvlog -sv` over
  every tracked `.sv` **and** `.v` under `hdl/` and over the pinned control
  plane (`protocol-processor/hdl`, `gptp-processor/hdl`), ratchets today's
  findings in [`scripts/xvlog.budget`](scripts/xvlog.budget) keyed on identity
  so a compensating swap cannot hide, and SKIPS cleanly with a visible marker
  when no Vivado is present, so it is inert in CI and never a false green. Its
  `--selftest` runs in [`scripts/run_all_suites.sh`](scripts/run_all_suites.sh)
  next to the others. Two things to know before you run it (#224, #236):
  - **The processor population is the superproject's gitlink, proved byte by
    byte, or the gate REFUSES** (exit 2, before it enumerates anything, before
    the census and before the budget is read or written, naming the state, the
    expected and actual revisions and the remediation). The pin it accepts is
    exactly one index record at the path, mode `160000`, stage `0`. An
    unmerged gitlink is not one, whatever single SHA survives: any record at
    stage 1, 2 or 3, a `160000` stage beside a file or symlink stage, or a
    one-sided stage with nothing to merge it against. Nor is a path tracked as
    an ordinary file or symlink, nor contents committed as ordinary files
    under it. Nor, on the checkout side, is absent, empty, a file or a symlink
    where the checkout must be, uninitialised, a standalone clone sitting at
    the path, or a registered submodule at another revision.
    Same shape and same #186 reason as the lint refusal above. Check with
    `git submodule status` -- a `-`, `+` or `U` prefix is a refusal. The
    budget carries the two populations in **separate sections**, so donor debt
    is never traded against `hdl/` debt; a processor key is spelled
    `<submodule>:<path>` so this generated file is not read as a hand-written
    copy of the submodule source list.
  - **Once the revision matches, the SOURCES themselves are proved, not asked
    about.** The population is read from the pinned commit's own tree
    (`git ls-tree -r <pin>`), and every file in it must hash to the blob id the
    pin records, over the exact bytes `xvlog` opens. Every Git call contributing
    to that decision explicitly sets `GIT_NO_REPLACE_OBJECTS=1`: a mutable
    `refs/replace/<pin>` must not make `git ls-tree <pin>` read a different
    commit while `HEAD` still prints the pinned id. The real-Git self-test
    installs that substitution with its altered bytes on disk and requires a
    `modified` setup refusal in both modes, before census or budget write.
    `git status`,
    `git diff` and `git ls-files` are not consulted at all, because those
    answers are computed through the index and the index can be told to stay
    quiet: `git update-index --assume-unchanged` and `--skip-worktree` both
    hide a changed or deleted file from every one of them (`git -C <sub>
    ls-files -v` prints `h` and `S` for the two). So a hidden edit, a sparse or
    skip-worktree checkout, a dropped index record, and a symlink standing in
    for a pinned file are all refused -- not because each is enumerated, but
    because acceptance is a per-file hash equality none of them can produce.
    A checkout that is not the pinned bytes is a population the pin does not
    stand behind, and a default run would rewrite the ratchet from it (#236).
    The repository's own `hdl/` is deliberately NOT proved this way: it is the
    tree you are gating, so its bytes on disk are the population by
    definition.
  - It **analyses; it does not elaborate**, and one real class lives only in
    elaboration. Splitting a declaration-with-initialiser (`reg [7:0] r =
    8'd0;`) into a bare declaration plus a continuous `assign` is not
    equivalent, and `xvlog`, Verilator 5.050 under `-Wall`, `sv2v` and Yosys
    all accept the broken form silently. Only `xelab` rejects it
    (`VRFC 10-9171`), and no gate in this repository runs `xelab`. If your
    change moves declarations around, that construct has **no gate** -- check
    it by hand and say so in the PR.
- **A build input never lists the protocol-processor sources, it derives
  them**: [`scripts/pp_srcs.py`](scripts/pp_srcs.py) reads the submodule tree
  and emits the list, packages first (detected by reading each file for a
  `package` declaration, not by its name). Every consumer calls it --
  [`syn/yosys/run.sh`](syn/yosys/run.sh),
  [`syn/yosys/ooc.sh`](syn/yosys/ooc.sh),
  [`tb/verilator/milan_dp/Makefile`](tb/verilator/milan_dp/Makefile),
  [`sw/litex/milan_soc.py`](sw/litex/milan_soc.py),
  [`syn/ooc/pp_shadow_ooc.tcl`](syn/ooc/pp_shadow_ooc.tcl) and
  [`syn/ooc/dp_srcs.py`](syn/ooc/dp_srcs.py) -- and each takes the exit status
  rather than discarding it, because the script refuses to emit an empty list
  and an empty list builds cleanly while proving nothing. `--check` fails if
  any tracked file outside the script's `PROSE_OK` table names a submodule
  source literally, so a new build input is caught the first time it names one
  and no consumer list has to be maintained. Prose that legitimately cites a
  source path adds the **exact literal** to `PROSE_OK` with its reason; a
  whole-file exemption is not available, because that is how a cited path
  becomes a hand-written list again. `--selftest` drives the check over
  synthetic trees and runs in the same CI step, so the gate cannot rot into a
  green that means nothing.
- **A `// verilator lint_off X` needs a justification**, exactly like a
  tied-off input does — an unexplained suppression is the same defect class
  as an unexplained tie. Put the reason next to the code AND a
  `PRAGMA_WAIVERS` entry in [`scripts/lint_rtl.py`](scripts/lint_rtl.py); the gate fails without
  one. The waiver code must be the **last token on the line**: a trailing
  `// prose` comment builds under Verilator 5.050 and does not build under
  5.020, which is how four suites became unbuildable once.
- Coverage-matrix rows ([`docs/testing/`](docs/testing)) only move ✅ with a runnable test.
  Prefer real-wiring-path tests over unit mocks.
- **Measure, don't assume**: no number from a comment or model drives a
  decision. HW counter first; measure before AND after; a TB-green
  integration change still owes a datapath-regression run
  ([`tb/verilator/milan_dp`](tb/verilator/milan_dp)).
- Timing claims need the full cell recipe (config + directive + seed); a
  bare WNS number is not reproducible. 3×32-thread Vivado discipline:
  single configs become 3-directive sweeps, keep best WNS.

## 4. Bench discipline (the expensive lessons)

- AX boot probes need **≥ 8 min** windows (power→network ≈ 7 min); a probe
  timeout is not a dead board.
- QSPI: never overwrite a slot without the current content dumped to disk
  first; regenerate every consumer's window map from the build's `csr.csv` on
  ANY gateware block-set change (CSR-rot rule,
  [`docs/integration/QSPI_FLASHBOOT.md`](docs/integration/QSPI_FLASHBOOT.md)).

## 5. Code quality

The rules above are the HDL house style, the lane and the verification bar.
The cross-language maintainability contract - one primary responsibility per
unit, explicit control flow, one source of truth, and the rest - lives in the
[code quality guide](docs/development/CODE_QUALITY.md), which also carries the
governing rule for cleanup:

> Leave touched first-party code at least as clear, small, and well-tested as
> it was, but do not broaden a functional change into an unrelated rewrite.

Cleanup that preserves behavior is a change of its own, reviewable on its own.
A functional change carries no repository-wide formatting, mass rename or
opportunistic refactor outside its stated scope.

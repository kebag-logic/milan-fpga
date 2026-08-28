# Code quality — the maintainability contract

This page is the numbered, cross-language maintainability contract for
first-party SystemVerilog, C++, Python, Tcl and shell code in this repository.
It exists because cleanup is otherwise easy to mix into functional work, to
turn into large formatting churn, or to apply to one language and not the next.

It does not replace [CONTRIBUTING.md](../../CONTRIBUTING.md). The HDL suffix,
reset, CDC, banner, lint-waiver and verification rules there remain
authoritative, and "SystemVerilog only for new HDL" and "the port list IS the
spec" are not restated here as weaker preferences. This page adds the rules
those house rules do not cover, and gives each one wording, examples,
exceptions, a measurement and a review checklist.

Rules land one at a time. Each rule that has landed carries its own section
below; the rules still to come are listed under
[Rules not yet landed](#rules-not-yet-landed) so a reader can see the whole
shape rather than guess at it.

## Contents

- **[The governing rule](#the-governing-rule)** -- The Boy Scout rule and the five concrete obligations that make it reviewable: cleanup preserves behavior, functional work stays out of unrelated rewrites, generated and vendored files are fixed at their source, new code complies immediately, and existing debt is inventoried rather than rewritten in one pass.
- **[Scope](#scope)** -- What counts as first-party maintenance surface and what is deliberately outside it, including why a generated file is fixed in its generator and never by hand.
- **[Rule 1: keep modules and functions cohesive](#rule-1-keep-modules-and-functions-cohesive)** -- The single-responsibility rule, its repository interpretation for SystemVerilog and host code, worked good/bad examples, the exceptions that let a long unit stay whole, and the review checklist.
- **[Measuring cohesion](#measuring-cohesion)** -- Why line count cannot answer the question, what `scripts/measure_cohesion.py` counts instead (disjoint state groups), what it deliberately cannot see, and the current candidate list read off the tree.
- **[Rule 2: prefer simple and explicit control flow](#rule-2-prefer-simple-and-explicit-control-flow)** -- The KISS rule, what "explicit" means for a SystemVerilog priority chain versus a host-side parser, the worked simplification that took one function from six levels of nesting to two, and the review checklist.
- **[Measuring control flow](#measuring-control-flow)** -- What `scripts/measure_control_flow.py` counts in each language -- nesting and decision points in host code, visible priority in RTL -- why no threshold is proposed, and what the tree actually measures today.
- **[Rules not yet landed](#rules-not-yet-landed)** -- The remaining nine rules of the contract, named so the numbering is stable and a reader knows what is still coming.

## The governing rule

> Leave touched first-party code at least as clear, small, and well-tested as
> it was, but do not broaden a functional change into an unrelated rewrite.

Five obligations make that reviewable:

1. **Cleanup preserves observable behavior and is reviewable on its own.** If
   behavior changes, it is a separate change with its own issue.
2. **Functional changes carry no unrelated churn.** No repository-wide
   formatting, no mass renames, no opportunistic refactor outside the stated
   scope.
3. **Generated and vendored files are never hand-edited.** Fix the generator
   or the upstream source. A hand edit to generated output is erased by the
   next regeneration and silently reintroduces whatever it fixed.
4. **New code follows the rules immediately.** The ratchets exist for existing
   debt, not as an allowance for new debt.
5. **A cleanup that touches executable behavior runs the relevant focused
   suite and the integration gate before and after.** "It only moved code" is
   a claim about a tool's output, so it is made with the tool.

## Scope

The rules apply to first-party sources: `hdl/`, `sw/`, `scripts/`, `tb/`,
`syn/` and `harness/` in this repository, plus the corresponding tracked
sources in the project-owned `protocol-processor/` and `gptp-processor/`
submodules. A scan refuses an absent or off-pin project submodule rather than
quietly establishing a smaller baseline.

They do not apply to:

- **vendored/external submodules** — `third_party/` and `external/` are upstream
  trees with their own contracts;
- **generated output** — anything a generator writes is fixed by changing the
  generator, which is also the only change a review can verify;
- **archived pages and evidence** — records of their time are not rewritten to
  match current wording.

## Rule 1: keep modules and functions cohesive

> Each first-party module, class, function, task, script, and named procedural
> block SHOULD have one primary responsibility and one primary reason to
> change. Split a unit when its responsibilities have independently named
> state, policy, or tests; do not create pass-through wrappers merely to meet
> a size metric.

### Repository interpretation

- In SystemVerilog, each register and each state machine has one clear owner.
  Separate protocol policy from storage or transport only where the seam has a
  real contract — a port list a reader can grade, not a boundary drawn to move
  lines.
- In C++ and Python harnesses, small action helpers compose into an explicit
  orchestration layer. A helper does not silently mutate unrelated
  module-level state.
- A cohesive generated table, descriptor image, or explicit state machine may
  remain large when splitting it would hide ordering or timing.

### A worked example

The AAF per-stage latency taps used to live inline in
`hdl/milan/milan_datapath.sv`, next to twenty-one unrelated state groups. The
inline block owned three things that have nothing to do with the rest of the
datapath: which AXIS handshake edge marks each pipeline stage, the uniform
one-cycle stage-pulse delay that keeps the receive filter's content-addressable
memory cone out of the tap chain, and the order of the sixteen read-only words
of the LTAP register window at base `0x870`.

Those three are one responsibility — adapt observation points to a register
window — and they have their own name, their own contract and their own tests.
They now live in `hdl/ieee1722/aaf/KL_aaf_latency_tap_bank.sv`, whose port list
is the whole contract: every port is an input except the two register rails.

The seam is worth having for a reason a size metric cannot express. The taps
are pure observers, and the observer-purity check
([`syn/yosys/check_tap_purity.sh`](../../syn/yosys/check_tap_purity.sh)) has to
establish that they never drive a stream. Inside a 7,000-line parent that is an
argument about a body; behind this port list it is a structural fact — provided
the gate reads the file. It enumerates pure observers by name (`*_taps.sv`), so
the extraction also had to teach it the `*_tap_bank.sv` shape; the witness is
its own count, which went from 24 to 33 stream-net bindings checked, and an
output on the bank named after a stream lane is now a violation.

The seam is not free, and the price is worth recording: the new module had to
be registered in five independent source lists — the Vivado list in
`sw/litex/milan_soc.py`, the Yosys rows in `syn/yosys/run.sh` and
`syn/yosys/ooc.sh`, and two testbench makefiles — and three suites failed until
it was. Rule 3 is where that duplication is addressed; Rule 1 only notes that
a split costs exactly as much bookkeeping as the tree makes it cost.

What the split is **not**: the measurement model — single in-flight tagged
reference frame, per-stage re-arm timeout, saturating last/min/max — stays in
`hdl/ieee1722/aaf/KL_aaf_latency_taps.sv`. Splitting the adapter from the
parent was worth it because the adapter has its own contract. Splitting the
adapter from the core again, to make each file shorter, would produce exactly
the pass-through wrapper the rule forbids.

### The counter-example

A pass-through wrapper that renames ports and instantiates one child adds a
file, a port list to keep in sync and a level of hierarchy, and removes no
ownership. It meets a size metric and fails the rule. The test for the
difference is whether the new unit has state, policy or tests a reader can name
independently of its parent.

### Exceptions

A unit may stay long and whole when:

- it is a generated table or descriptor image whose order is its meaning;
- it is one explicit state machine whose cases must be read together;
- splitting it would move a timing- or ordering-critical relationship across a
  module boundary, where it is no longer visible in one place.

Each exception is a claim about ordering or timing, so it is written down where
the unit is, not left for a later reader to reconstruct.

### Review checklist

- Can the unit's responsibility be named in one sentence without "and"?
- Does every register in it have one owner?
- If the unit were split, would the seam have a contract a test could grade —
  or only a renamed port list?
- Does the change preserve observable behavior, and does a run of the focused
  suite plus the integration gate say so?
- Does at least one assertion fail if the responsibilities are re-coupled?

## Measuring cohesion

Line count cannot answer "is this cohesive". A generated table may be long and
perfectly cohesive; a short block can own two unrelated pieces of state. So the
measurement is about state ownership.

[`scripts/measure_cohesion.py`](../../scripts/measure_cohesion.py) treats every
`always_ff` block as a state owner and couples two blocks when they share a
written signal, or when one reads a signal the other writes. Coupling is
transitive, so a module's blocks partition into **disjoint state groups**. One
group means cohesive by this measure, whatever the length. Twenty groups means
twenty state machines sharing a file and a reset.

```
python3 scripts/measure_cohesion.py            # ranked candidate table
python3 scripts/measure_cohesion.py --module P # one file, group detail
python3 scripts/measure_cohesion.py --selftest # the fixture arms
```

**What it cannot see, stated plainly.** Combinational glue, structural
instantiation and port-level fan-out are invisible to it. Two groups may still
be one responsibility joined by an `assign` — and the module extracted above is
itself an example: its two blocks are reported as two groups because the
in-frame tracker reaches the stage-pulse register through a combinational
`assign` rather than by naming it. The number is a candidate list for a
reviewer, never a verdict, and no gate fails on it.

The tool grades its own extraction rather than asserting it: `--selftest` runs
eighteen fixture arms whose answers are known by construction, including the
one that matters most for false coupling — `<=` is also the less-than-or-equal
operator, so `if (count_r <= LIMIT)` must not be read as a write to
`count_r`.

### Current candidates

Read off the pinned superproject and both project-owned processor submodules
with the command above. One hundred and six of 110 first-party modules carry an
`always_ff` block; fifty-five own more than one state group. Files containing
more than one module are split at `endmodule`, so their independent owners are
never merged into one misleading file-level score.

| Module | Lines | Blocks | Disjoint state groups |
|---|---:|---:|---:|
| `hdl/milan/milan_datapath.sv:milan_datapath` | 7081 | 23 | 20 |
| `protocol-processor/hdl/top/protocol_processor_top.sv:protocol_processor_top` | 3959 | 15 | 8 |
| `hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv:KL_gptp_shadow` | 670 | 8 | 7 |
| `hdl/milan/KL_pp_shadow.sv:KL_pp_shadow` | 1129 | 6 | 6 |
| `hdl/common/csr/milan_csr.sv:milan_csr` | 3046 | 14 | 5 |
| `protocol-processor/hdl/adp/KL_adp_engine.sv:KL_adp_engine` | 1029 | 11 | 5 |

The list is a starting point for review, not a work queue. Three of these rows
are expected to stay as they are: `milan_csr` is a register decode whose order
is its meaning, and both shadow wrappers are integration seams whose groups are
the planes they wrap. `milan_datapath` is the one row where the count reflects
real unrelated ownership, and it is reduced one cohesive responsibility at a
time rather than by a split campaign — the extraction described above moved it
from 22 groups and 7167 lines to 20 groups and 7081 lines on the current base.

## Rule 2: prefer simple and explicit control flow

> Use the simplest control flow that makes state, priority, timing, and error
> paths obvious. Prefer named intermediate values, explicit FSM states and
> cases, bounded loops, and early exits over clever expressions or deep
> nesting.

Shorter is not the same as simpler. A line that removes a branch by hiding it
has made the code worse, and the rule is about what a reader can see, not about
line count.

### Repository interpretation

- **SystemVerilog priority must be visible.** A signal assigned more than once
  in one procedural block resolves by source order, and accidental
  last-assignment-wins behavior is not documentation. The pattern is not
  forbidden — a default followed by a narrower override is often the clearest
  thing to write — but the default and the override are named as such where
  they are, so a reader does not have to re-derive the priority from line
  numbers.
- **Host code fails where it fails.** A Python, Tcl or shell path that cannot
  continue returns or raises at that point, rather than setting a flag that is
  carried through nested code and tested somewhere else.
- **Table-driven code is welcome when the table is the specification**, and its
  defaults, bounds and ordering are explicit. A dispatch table beats a branch
  chain precisely when the chain's final `else` has become a catch-all that
  nobody can name.

### A worked example

`cluster_names` in `sw/builder/endstation_builder.py` names one AUDIO_CLUSTER
per cluster of a stream port. It did that with a four-way `if / elif / elif /
else` chain nested inside two loops, with a further early-exit inside the final
`else` — six levels of nesting and fourteen decision points in thirty-eight
lines. The role that was hardest to read, loopback, was the one reached through
the unnamed `else`.

It is now a table: one small named function per pool role, and a dispatch that
looks the role up. The measured shape, before and after:

| Unit | Lines | Nesting depth | Decision points |
|---|---:|---:|---:|
| `cluster_names` before | 38 | 6 | 14 |
| `cluster_names` after | 20 | 2 | 4 |
| `_name_loopback` (deepest namer) | 9 | 1 | 1 |

Behavior is unchanged, and the claim is made with a tool rather than asserted:
every cluster name the builder can produce — five configurations, every stream
port, both directions — is byte-identical before and after.

Two things the flattening made visible that the nesting had hidden, and both
now have arms:

- the loopback namer's **empty receive space** path. A talker whose entity
  declares no listener has no channel space to walk and names the cluster by
  its own offset. That path was a `continue` five levels deep and nothing
  graded it.
- the chain's **bare `else`**. It swallowed any role that was not physical,
  virtual or pilot and named it as a loopback channel. The table refuses an
  unknown role by name instead. The role set is closed today, which is exactly
  why the refusal needs a test: an unreachable path with no arm is how the next
  role gets silently mislabelled.

### Measured hotspots, not automatic findings

The ranked scan leaves a small review set whose complexity has a concrete
reason. These rows include both project-owned processor submodules:

| Unit | Measured shape | Why it is complex / disposition |
|---|---:|---|
| `sw/litex/test_ring_bd.py:stim` | depth 10, 26 decisions | A cycle-accurate concurrent DMA stimulus nested inside a test; retain the timing shape, but split the next new scenario out of this closure. |
| `tb/tools/hive_compliance.py:main` | depth 7, 95 decisions | CLI orchestration for many independent protocol checks; the checks are already helpers, so its remaining branches are explicit dispatch and failure aggregation. |
| `protocol-processor/scripts/render-wavedrom.py:collect_blocks` | depth 7, 13 decisions | A small Markdown/fence parser; a future change should table-drive token states, but no rewrite is justified without a failing case. |
| `hdl/common/csr/milan_csr.sv:register_write` | depth 6, 142 order-dependent targets | The address decode is the register-map specification; splitting it would hide priority and address order, so it stays a named explicit decode. |
| `protocol-processor/hdl/aecp/KL_aecp_engine.sv:command_machine` | depth 7, 85 order-dependent targets | An explicit command FSM with defaults followed by state-specific overrides; review priority at each override rather than imposing a generic count. |

The worked `cluster_names` case was selected because its complexity came from
an unnamed catch-all and nested error path, not merely because it ranked high.

### Exceptions

- A long, flat `case` over an explicit FSM state set is simple, whatever its
  length. Splitting it to reduce a count would hide the transition table.
- A compact expression is fine when it IS the specification — a wire-format
  field split, a documented mask — and the citation is next to it.
- A default-then-override pair in one block stays, when the two are named and
  the override's condition is the narrower one.

### Review checklist

- Can a reader name the priority without counting lines?
- Does every error path end where it is discovered, or is a flag carried?
- Is each loop bound obvious at its head?
- If a branch chain ends in `else`, can that branch be named — or is it a
  catch-all standing in for cases nobody enumerated?
- Does the change keep observable behavior, and does a differential run over
  real inputs say so rather than a reading of the diff?

## Measuring control flow

[`scripts/measure_control_flow.py`](../../scripts/measure_control_flow.py) asks
each language its own question.

For host code it reports, per function, the **nesting depth** (how many
enclosing branch, loop, `with` or `try` constructs a reader must hold) and the
**decision points** (`if`, `for`, `while`, exception handlers, boolean
operators, conditional expressions). A nested definition is measured as its own
unit, so an orchestrator that defines one helper does not read as deeply nested
when it is not.

For SystemVerilog it reports, per procedural block, the nesting of `begin` and
`case`, and the signals the block assigns **more than once** — the ones whose
value is decided by source order.

```
python3 scripts/measure_control_flow.py             # both, ranked
python3 scripts/measure_control_flow.py --selftest  # the fixture arms
```

**No threshold is proposed, and none is imported.** A generic complexity limit
from another codebase would fail the parts of this tree that are correctly
shaped — a wire-format parser and an explicit FSM both score high and are both
right. What the pinned superproject and its two project-owned processor
submodules measure today, so a later reader can see whether it moved: 2,322
first-party functions, of which 35 nest five levels or deeper; and 616
procedural blocks, of which 507 resolve at least one signal by source order.
That second number is the reason the rule asks for priority to be *visible*
rather than absent — forbidding the pattern would be a rewrite of most of the
RTL, and would not make any of it clearer.

## Rules not yet landed

The contract is ten rules. Rules 1 and 2 are above; the rest keep these
numbers so citations stay stable as they land:

| Rule | Subject |
|---|---|
| 3 | One source of truth, without weakening independent test oracles |
| 4 | Intention-revealing names and explicit units and types |
| 5 | Explicit ports, contracts, ownership and side effects |
| 6 | Fail fast and encode invariants |
| 7 | Comments explain why; no dead or speculative code |
| 8 | Deterministic, specification-derived tests |
| 9 | Automated mechanical hygiene with measured ratchets |
| 10 | Idiomatic SystemVerilog and explicit HDL boundaries |

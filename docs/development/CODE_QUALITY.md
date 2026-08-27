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
- **[Rule 2: prefer simple and explicit control flow](#rule-2-prefer-simple-and-explicit-control-flow)** -- The KISS rule, what "explicit" means for a SystemVerilog priority chain versus a host-side parser, the worked simplification that took one function from four levels of nesting to two, a real FSM and a real combinational mux read against the same rule, the measured hotspots with their dispositions, and the review checklist.
- **[Measuring control flow](#measuring-control-flow)** -- What `scripts/measure_control_flow.py` counts in each language -- nesting and decision points in Python, priority resolved by source order in RTL -- exactly which files and blocks it scans and what it refuses, why no threshold is proposed, and what the tree actually measures today.
- **[Rule 3: keep one source of truth without weakening test oracles](#rule-3-keep-one-source-of-truth-without-weakening-test-oracles)** -- The single-definition rule and the exception that keeps a test honest, the five RTL source lists that had one authority and four unguarded copies, the drift gate that now derives all of them from the RTL, and the mutation that proves an independent oracle is really independent.
- **[Rule 4: use intention-revealing names and explicit units](#rule-4-use-intention-revealing-names-and-explicit-units)** -- What a name must reveal, the unit and clock-domain qualifiers that extend the existing HDL suffixes rather than competing with them, cross-language equivalents, and the interface renamed end to end to prove it.
- **[Measuring hidden units](#measuring-hidden-units)** -- The port's own documentation as the evidence, the three exclusion classes and the false positives that forced them, and why this ships as a ratchet instead of a verdict.
- **[Rule 5: make ports, contracts and ownership explicit](#rule-5-make-ports-contracts-and-ownership-explicit)** -- What a port contract must state, why wildcard, positional and hierarchical bindings are refused outright while missing documentation and unjustified open or tied connections are only ratcheted, the exact scope of the inventory, the boundary documented end to end as proof, and the review checklist.
- **[Rule 6: fail fast and encode invariants](#rule-6-fail-fast-and-encode-invariants)** -- Where a verdict must be refused rather than logged, the elaboration contract added to the receive shield and mutation-proven against four illegal parameter sets, the two masked-failure populations that are now ratcheted, and the review checklist.
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

- **SystemVerilog priority must be visible.** A signal assigned twice on one
  path through a procedural block — a default at the top and a narrower
  override below it, or one write repeated in two separate `if`s — resolves
  by source order, and accidental last-assignment-wins behavior is not
  documentation. The pattern is not forbidden — a default followed by a
  narrower override is often the clearest thing to write — but the default
  and the override are named as such where they are, so a reader does not
  have to re-derive the priority from line numbers. The arms of one
  `if`/`else` or one `case` are exclusive; no source order is involved there.
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
`else` — four levels of nesting (the two loops, the chain, and the exit inside
its last arm) and fourteen decision points in thirty-eight lines. The role that
was hardest to read, loopback, was the one reached through the unnamed
`else`.

It is now a table: one small named function per pool role, and a dispatch that
looks the role up. The measured shape, before and after:

| Unit | Lines | Nesting depth | Decision points |
|---|---:|---:|---:|
| `cluster_names` before | 38 | 4 | 14 |
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

The moved logic is pinned too, not only the two paths: every cluster name the
builder produces for the loopback-bearing `ax7101_8x8` and for the
`channel_names` config `ax7101_1x1_tdm8` is tracked in
`sw/builder/cluster_names_golden.json`, generated from the implementation the
differential proved identical, and gate 24d compares the built names to it one
by one. Three mutations that survive every prefix check — a loopback walk that
always starts at stream 0, one that never steps a channel, and a physical
namer that ignores `channel_names` — each fail that comparison.

### An RTL FSM example

`guard_fsm` in `hdl/common/KL_link_guard.sv` is a three-state link-guard
machine (`RUN_S`, `HOLD_S`, `SETTLE_S`) written the way the rule asks. Reset,
the disable input and the `unique case` over the state are the branch
structure, every transition sits in the arm of the state it leaves, and the
`default` arm says what an illegal encoding does (`state_r <= RUN_S`). Nothing
about the priority of those arms is re-derived from line numbers: `if (!rst_n)
... else if (dis_i) ... else case (state_r)` states it. The tool reports the
block at depth 5 with two signals resolved by source order, `guard_rst_r` and
`eth_rst_r`, and both are the allowed shape — each state arm first assigns the
reset rails their value for that state, and the transition condition nested
inside the arm overrides them for the cycle the state changes. The `RUN_S`
arm, annotated:

```
RUN_S : begin
  guard_rst_r <= 1'b0;                      // the state's value
  eth_rst_r   <= 1'b0;
  if (!both_alive_w || man_edge_w) begin    // the transition overrides it
    state_r     <= HOLD_S;
    guard_rst_r <= 1'b1;
    eth_rst_r   <= 1'b1;
```

The default is the first statement of the arm and the override is the
narrower condition inside it, so a reader names the priority without counting
lines. The state register itself is not reported: every write to it is in an
exclusive arm, which is what "explicit FSM states and cases" means in the rule.

### A combinational mux example

`confl_pick` in `hdl/milan/KL_pp_maap_shim.sv` selects the lowest pending
conflict source, and it is source-order priority on purpose:

```
//! lowest pending source first (descending sweep, last write wins)
always_comb begin : confl_pick
  conflict_src_o = '0;
  for (int unsigned i = N_SRC_P; i > 0; i--) begin
    if (confl_pend_r[i-1]) conflict_src_o = SRC_W_C'(i - 1);
  end
end : confl_pick
```

The tool reports `conflict_src_o` as resolved by source order, and it is: the
sweep runs from the highest source down, so the lowest pending one writes last
and wins. What makes that acceptable is that nothing has to be simulated to
know it. The default (`'0`, no conflict) is the first line, the comment on the
block names both the priority and the mechanism, and the loop direction *is*
the priority. The accidental form is the same six lines with the loop
ascending and the comment absent: it would pick the highest source — legally,
synthesizably — and nothing in the block would say whether that was meant.
That is what the rule calls accidental last-assignment-wins: an override that
only line order documents. An `if`/`else if` chain over the sources would make
the same priority structural; the loop is allowed because it is named.

### Measured hotspots, not automatic findings

The ranked scan leaves a small review set whose complexity has a concrete
reason. These rows include both project-owned processor submodules:

| Unit | Measured shape | Why it is complex / disposition |
|---|---:|---|
| `tb/tools/hive_compliance.py:main` | depth 7, 95 decisions | CLI orchestration for many independent protocol checks; the checks are already helpers, so its remaining branches are explicit dispatch and failure aggregation. |
| `protocol-processor/scripts/render-wavedrom.py:collect_blocks` | depth 7, 13 decisions | A small Markdown/fence parser; a future change should table-drive token states, but no rewrite is justified without a failing case. |
| `tb/tools/hive_compliance_clusters.py:main` | depth 6, 37 decisions | The same shape as `hive_compliance.py:main` for the STREAM_PORT and cluster probes: descriptor-type, port, cluster and map loops with a status check at each level, and every failure recorded where it is found. |
| `scripts/act_ci.py:freeze_live_act` | depth 6, 23 decisions | A container monitor that re-checks its cancel flag after every blocking call — the early return the rule asks for, paid for in depth because it polls the inventory, the running set and the tool-cache volume in one closure; the next thing it watches goes in a helper. |
| `sw/litex/test_ring_dma.py:axi_slave` | depth 6, 18 decisions | A cycle-accurate AXI slave model inside a test; the nesting is the address, data-beat and response handshake sequence, so it is retained, and the next protocol rule it checks belongs in a helper rather than a deeper branch. |
| `hdl/common/csr/milan_csr.sv:register_write` | depth 6, 30 order-dependent targets | The address decode is the register-map specification, and the 30 targets are one-cycle write strobes cleared at the top of the block and raised by the decode — a named default-then-override — so it stays a named explicit decode. |
| `protocol-processor/hdl/aecp/KL_aecp_notify.sv:notify_core` | depth 7, 27 order-dependent targets | The unsolicited-notification FSM: per-cycle defaults for its request and arm outputs, then state-specific overrides across eight states; review the priority at each override rather than imposing a count. |
| `protocol-processor/hdl/packet_engine/KL_pp_rx_validator.sv:validator_seq` | depth 6, 27 order-dependent targets | The receive-frame sequencer: its pulses fall by default each cycle and its captured header fields are written when their byte arrives, so the order is the wire order. |
| `hdl/milan/milan_datapath.sv:amap_edit_validate` | depth 2, 27 order-dependent targets | Flat, and still the widest set: an AUDIO_MAP edit validator that gives every verdict, key and live word a default and narrows each per descriptor type — the allowed shape as long as each default stays above its override. |

The worked `cluster_names` case was selected because its complexity came from
an unnamed catch-all and nested error path, not merely because it ranked high.
Two rows an earlier count put at the top are absent for a reason worth
recording: the nine-arm `elif` ladder in `sw/litex/test_ring_bd.py:stim` read
as depth 10 while an `elif` counted as a level and is depth 4 now that it does
not, and the explicit command FSM in
`protocol-processor/hdl/aecp/KL_aecp_engine.sv:command_machine` read as 85
order-dependent targets while exclusive `case` arms were counted and holds 5
now that they are not. Both were artefacts of the measurement, not of the code.

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

For host code it reports, per function, the **nesting depth** — how many
enclosing branch, loop, `with` or `try` constructs a reader must hold, where an
`elif` continues its chain and adds no level — and the **decision points**:
`if`, `for`, `async for`, `while`, `match` and each of its `case` arms,
exception handlers, boolean operators, conditional expressions, `assert`, and
each `for` clause of a comprehension (its `if` filters are not counted
separately). A nested definition is measured as its own unit, so an
orchestrator that defines one helper does not read as deeply nested when it is
not. Host code means Python: the C++ harnesses, Tcl and shell in the tree are
not measured, and no hotspot in them can reach the table above.

For SystemVerilog it reports, per procedural block, the nesting of `begin` and
`case`, and the signals the block **resolves by source order**: a signal
written at a point that is not mutually exclusive with an earlier write to the
same signal. `x = 1; if (q) x = 2;` is that shape, and so is a write repeated
in two separate `if`s. An `if`/`else` pair, an `else if` chain and a full
`case` with one write per arm are not — their arms are exclusive — so the
explicit FSM the Exceptions call simple is not reported for being one. A
struct member is its own target and a whole-struct write covers it, a
concatenation writes each of its elements, a loop variable is not a signal,
writes to different constant bits of one vector are disjoint, and a variable
index is taken to overlap anything.

**The population, stated plainly.** Python is scanned under `scripts/`, `sw/`,
`tb/`, `harness/`, `syn/` and `hdl/` here and under the same names plus
`bench/` in each processor: 115 files today — 104 in this repository (31 under
`scripts/`, 29 `sw/`, 26 `harness/`, 14 `tb/`, 4 `syn/`), 9 in
`protocol-processor` (`scripts/`, `hdl/`, `tb/`) and 2 in `gptp-processor`
(`hdl/`, `tb/`). Python under `avdecc/`, `bd/`, `docs/` and `tests/` is outside
the Scope list above and is not measured. The RTL number covers every
`always_ff`, `always_comb`, `always_latch` and `always @` block, with or
without a `begin`, in the `.sv` files under `hdl/` of the three trees;
testbench and synthesis-flow SystemVerilog under `tb/` and `syn/`, `.svh`
headers and the generated `.v` wrapper are not in it. A Python file that does
not parse or a block that does not close is named on stderr, the summary line
says how many were `NOT measured`, and the run exits 2, so an unmarked number
is the whole population.

```
python3 scripts/measure_control_flow.py             # both, ranked
python3 scripts/measure_control_flow.py --selftest  # the fixture arms
```

The tool grades itself the way the cohesion tool does: `--selftest` runs
forty-five fixture arms whose answers are known by construction — an
`if`/`else` pair and a full `case` are exclusive, a flat `elif` chain is depth
1, a block without `begin` is still a block, a `begin` inside a string does
not unbalance one — plus one arm per processor that fails when the scan
reaches none of its Python. Both measurement self-tests run in the `docs-check`
job of [`.github/workflows/docs.yml`](../../.github/workflows/docs.yml), after
the submodule checkout they need.

**No threshold is proposed, and none is imported.** A generic complexity limit
from another codebase would fail the parts of this tree that are correctly
shaped — a wire-format parser and an explicit FSM both score high and are both
right. What the pinned superproject and its two project-owned processor
submodules measure today, so a later reader can see whether it moved: 2,485
first-party functions (2,399 here, 46 in `protocol-processor`, 40 in
`gptp-processor`), of which 13 nest five levels or deeper; and 626 procedural
blocks (319, 271 and 36), of which 291 (128, 152 and 11) resolve at least one
signal by source order. That second number is the reason the rule asks for
priority to be *visible* rather than absent — forbidding the pattern would be
a rewrite of nearly half the RTL, and would not make any of it clearer.

## Rule 3: keep one source of truth without weakening test oracles

> A production fact has one authoritative definition, and derived copies are
> generated or checked for drift. Unexplained magic values are forbidden. Tests
> stay intentionally independent when they are an oracle: expected values come
> from the specification, not from the definition being tested.

The two halves pull in opposite directions on purpose. Sharing a constant with
a test makes the test inherit the implementation's defect; duplicating a
production fact makes the copies drift. The rule is that **production** has one
definition, and a **test** may repeat a value when its independence is what
gives the test its power — with the external rule cited where the repeat is.

### Repository interpretation

- Name constants with their units, and cite the standard or register map where
  the value is not self-evident.
- Generate repeated layout, descriptor and build artifacts from one tracked
  source, and give each derived consumer a drift check.
- A test may repeat a value or a mapping when independence is load-bearing. The
  comment cites the external rule and says why importing the implementation's
  symbol would weaken the test.

### A worked example: five lists, one authority

The set of RTL files needed to compile `milan_datapath` was written out five
times: the Vivado list in `sw/litex/milan_soc.py`, the `milan_datapath` row in
`syn/yosys/run.sh`, `DP_SRCS` in `syn/yosys/ooc.sh`, and the source lists in
`tb/verilator/milan_dp/Makefile` and `tb/verilator/hostplane/Makefile`. Exactly
one of them was guarded — `scripts/check_soc_sources.py` has watched the Vivado
list since a missing entry killed three synthesis runs forty minutes in.

The other four were unguarded, and the cost was paid immediately: extracting one
module under Rule 1 broke three Verilator suites at once, each with the same
"Cannot find file containing module", one per list nobody had told.

[`scripts/check_rtl_source_lists.py`](../../scripts/check_rtl_source_lists.py)
makes the RTL the authority and every list a derived consumer. It walks the
compilation-unit closure of `milan_datapath` through the sources — module
instantiations, package references, interface types through any modport and
`` `include``d bodies, transitively — and checks each consumer carries every
file in it. A declaration makes a child part of that walk; a hard-coded
naming-prefix allowlist does not. That distinction is load-bearing for
`protocol_processor_top` and `credit_based_shaper`, whose ordinary names were
silently absent from the first version of the closure. Package-only and
interface-only files are equally load-bearing even though they instantiate no
module.

The walk has to see every instantiation shape a front end accepts, because a
shape it does not see is a file no consumer is told about. The first version
needed two leading spaces and walked past the one column-0 instantiation the
tree already had — `traffic_class_map` in
`hdl/ieee8021q/ts/traffic_classifier.sv` — so both Yosys rows could drop that
file with the gate green while Yosys failed on it. The first hop now lives
once, in `scripts/check_soc_sources.py`: any indentation, an arrayed instance,
`X #(` with or without the space, comments blanked first, and every included
header spliced in the way the preprocessor does. The oracle for the walk is an
independent front end over exactly the closure, with an include directory that
holds only headers so no module can be found by filename; the one `.sv` copied
beside them is the package five closure files `` `include``, which declares no
module:

```
inc=$(mktemp -d); mkdir -p "$inc/gen"
for f in $(git ls-files -- 'hdl/*.svh') hdl/common/ethernet_packet_pkg.sv; do
  case "$f" in */gen/*) cp "$f" "$inc/gen/";; *) cp "$f" "$inc/";; esac; done
verilator --lint-only -Wno-fatal -Wno-lint -Wno-style --top-module milan_datapath \
  "+incdir+$inc" $(python3 scripts/check_rtl_source_lists.py --files) 2>&1 | grep -c MODMISSING
```

It prints `0` at this head, over 109 files. Over the 108 the first version
derived it printed `1`, naming `traffic_class_map`.

Two properties are what make it a source-of-truth gate rather than a fifth copy:

- **It never checks one list against another.** All five could agree and all
  five be wrong. The authority is the RTL, and the first-hop instantiation
  parser is *imported* from `scripts/check_soc_sources.py` rather than
  re-written — a gate about single sources of truth that forked its own parser
  would refute itself.
- **It asks each consumer instead of parsing it.** A recogniser accepts what it
  has modelled, and `make` and `bash` accept something else; the four escapes
  recorded in [`syn/ooc/dp_srcs.py`](../../syn/ooc/dp_srcs.py) all worked that
  way. So each consumer prints the expansion it will really use
  (`make -s print-srcs`, `syn/yosys/run.sh --emit`, `syn/yosys/ooc.sh
  --emit-dp`) and the gate reads that. Two of those emit paths did not exist and
  were added, which is most of what this change is. The Vivado Python list has
  no print mode, so it is read the way Python reads it: the
  `_MILAN_DATAPATH_SOURCES` literal and the registrations beside it through the
  `ast` module, in which a comment does not exist — a regex over the file's
  text had counted a commented-out row as carried — with its starred
  `_pp_sources()` entry expanded through the same `scripts/pp_srcs.py` that
  `milan_soc.py` calls for the protocol-processor half.

The unit is the **file**, not the module, because that is what a source list
carries and one file may declare several modules — `KL_aaf_latency_chain` lives
inside `KL_aaf_latency_taps.sv`. Comparing module names to file entries would
demand entries that must not exist.

A consumer that cannot answer — an emit path that exits non-zero, a Makefile
that is absent, a host without `make` — fails the gate with exit 2 by default,
and CI runs that default. A gate that reads a consumer it could not reach as
covered is how a list goes unchecked for months. `--allow-skip` is the explicit
opt-out for a host without the tooling: it prints a `!! SKIPPED` marker per
consumer and the verdict counts them as not covered, and a run in which every
consumer was skipped is still exit 2. A diagnosed defect — `print-srcs` having
become a Makefile's default goal, so a bare `make` prints a list instead of
running the suite — is a finding, and no flag skips it. `--list` also prints,
per consumer, the files it carries that the closure does not need; the two
single-top Yosys rows each carry six today, harmless but stale.

The self-test proves the bite on copies, never on the tree. It copies each
consumer, removes one closure file from the copy and runs the copy's own emit
path — `make -f` from the suite directory; the copied script beside the
original under a temporary name, because it resolves the repository from its
own location — then requires that path and nothing else to report the removal,
and the tree to be byte-identical afterwards. Set arithmetic on an
already-fetched list, which is what the first version did, would have passed
with every fetcher stubbed to return the closure.

### The processor-native list, and where the scope statement ends

The five lists above all compile the same top, and `scripts/pp_srcs.py` feeds
the processor half of each. One list in scope is neither: the protocol
processor's own portability gate, `protocol-processor/syn/yosys/run.sh`, keeps
a hand-written `tops` array that rule 2 of the processor's own HDL README says must name
every module, so each is elaborated as a Yosys top on its own. Nothing derived
it and nothing checked it, and at pin `3770ae02` it had drifted: 38 modules are
declared under `protocol-processor/hdl` and the array names 32. The six absent
ones — `KL_acmp_nvm_shadow`, `KL_mrp_strip`, `KL_pp_dispatch_fifo`,
`KL_srp_admission`, `KL_srp_top`, `protocol_processor_top` — all elaborate when
asked; the gate simply never asked, and both repositories reported the
processor as covered.

The same gate now reads that list too, with the declared modules as the
authority. It reads the array the way bash does — a `#` at the start of a word
is a comment to the end of its line, quoted names are unquoted — because this
is the one consumer that cannot be asked (its expansion path is Yosys), and
splitting the raw text had credited a commented-out top as elaborated. Every
declared module is a top, or it is named in
[`scripts/processor_yosys_tops.budget`](../../scripts/processor_yosys_tops.budget)
with the reason it is not. The six are recorded there as **drift at the pin**,
not as helper exceptions, because that is what they are; the fix is upstream,
and the pin bump that brings it in deletes the lines, since a recorded name
that has become a top is refused as stale and an omission that is not recorded
is refused outright. The record can therefore only shrink.

The gPTP processor keeps no native tops list. Its portability coverage is the
closure walk itself — every one of its six sources is reached from
`milan_datapath` — and `--list` prints that count so a gPTP module that fell
out of the walk would be visible rather than merely unelaborated.

The gPTP engine's source list is itself an inventory item, and it is written by
hand ten times. Five copies are in this repository — the gPTP rows of
`sw/litex/milan_soc.py`, `GPTP_ENGINE_SRCS` in `syn/yosys/run.sh` and
`syn/yosys/ooc.sh`, `GPTP_SRCS` in `tb/verilator/milan_dp/Makefile` and
`tb/verilator/hostplane/Makefile` — and five are in the gPTP processor's own
repository: its top-level Makefile's lint target, its out-of-context Tcl, the
Arty bench Makefile and build Tcl, and its Verilator engine suite. They
classify as follows.

| Copies | Classification | Why |
|---|---|---|
| The five in this repository | Drift-checked derived copies | The walk reaches all six engine files from `milan_datapath`, so a gPTP file any of the five omits is a `MISSING SOURCE`. No generator like `scripts/pp_srcs.py` exists for them yet, and the comment in `milan_soc.py` that once called the `milan_dp` Makefile "authoritative" now names the gate: a copy that calls another copy authoritative is the circular authority that let four protocol-processor copies drift together. |
| The five in the processor repository | Outside this gate | They live in the submodule at its pin, which this repository can neither generate nor edit; the gate guards the six files the superproject needs, not the processor's build inputs. They carry a defect of their own — a module added under the processor's `hdl` that the engine does not instantiate is never linted or elaborated there — which belongs to that repository's own gate, not to a superproject check parsing a pinned tree it does not own. |

### The named-constant half

`milan_datapath` passed `16'h88F7` to the timestamp unit's `ETH_TYPE`
parameter while already importing `ethernet_packet_pkg`, which defines that
exact value as `ETH_TYPE_PTP`. That is a second definition of a fact the package
owns, and it is now the package's name.

The inventory behind that choice, measured rather than estimated: 24 distinct
SystemVerilog hexadecimal literals (the `N'hX` spelling, exact text) appear in
four or more first-party RTL files. The command is the definition of the
number:

```
git ls-files --recurse-submodules -- 'hdl/*.sv' 'protocol-processor/hdl/*.sv' 'gptp-processor/hdl/*.sv' \
  | xargs grep -oHE "[0-9]*'h[0-9A-Fa-f_]+" | sort -u | cut -d: -f2- | sort | uniq -c | awk '$1 >= 4' | wc -l
```

They classify into three kinds, and only the first is debt.

| Kind | Example | Disposition |
|---|---|---|
| Drift — a named definition exists and the literal ignores it | `16'h88F7` beside `ETH_TYPE_PTP` | Fix. Done here for the instantiation in `milan_datapath`; the six remaining sites are listed below. |
| Structural rails and saturation values | `0xFFFF`, `0xFFFFFFFF`, `0x0000` | Not duplication. The same rail in unrelated modules is a coincidence of width, not a shared fact. |
| Deliberate independent oracles | `0x22F0`, `0x88F7`, `0x8100` in tests and wire-truth tools | Keep. See below. |

Every raw EtherType site outside the package, from
`grep -rnE "'h(88F7|22F0|8100|22EA)" hdl --include=*.sv` with
`hdl/common/ethernet_packet_pkg.sv` itself removed:

| Site | Literal | Package name | Imports the package? |
|---|---|---|---|
| `hdl/milan/KL_pp_shadow.sv`, `ET_1722_C` | `16'h22F0` | `ETH_TYPE_AVTP` | no |
| `hdl/milan/KL_pp_shadow.sv`, `ET_MSRP_C` | `16'h22EA` | `ETH_TYPE_MSRP` | no |
| `hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv`, `ET_GPTP_C` | `16'h88F7` | `ETH_TYPE_PTP` | no |
| `hdl/ieee8021as/gptp_plane/KL_gptp_txstamp.sv`, `ET_GPTP_C` | `16'h88F7` | `ETH_TYPE_PTP` | no |
| `hdl/ieee8021as/ptp_timestamp/ptp_ts_top.sv`, `ETH_TYPE` default | `'h88F7` | `ETH_TYPE_PTP` | no |
| `hdl/ieee8021as/ptp_timestamp/ptp_ts_core.sv`, `ETH_TYPE` default | `'h88F7` | `ETH_TYPE_PTP` | yes |

The two parameter defaults are overridden on the shipping path —
`milan_datapath` passes `ETH_TYPE_PTP` to `ptp_ts_top`, which passes it on —
so they are defaults, not the value the wire sees; `ptp_ts_core` is the one
remaining site whose module already imports the package. Four of the modules
would need a new import, which changes their compile dependencies, so all six
stay a separate change with its own verification rather than a rider on this
one.

### Proving the oracle exception

A test that reads its expectations back through the implementation's own
expression agrees with any permutation of it. The claim that an oracle is
independent is therefore made with a mutation, not asserted.

`tb/verilator/aaf_latency_tap_bank` takes every LTAP word offset and field split
from the register map at base `0x870`, not from the packing expression in
`hdl/ieee1722/aaf/KL_aaf_latency_tap_bank.sv`. Swapping the `max` and `last`
halves of one word in the RTL makes the harness fail — on the one check where a
sample's maximum and its last value genuinely differ, which is exactly the check
that can see the swap. A harness that had imported the DUT's word order would
have stayed green through the same mutation.

### Exceptions

- Values that are coincidentally equal but mean different things are not
  abstracted together. Two constants that happen to be 8 are two constants.
- A test keeps its own copy of a specification value when importing the
  implementation's symbol would make the test grade itself.
- Wire-format byte comparisons stay literal where a name would hide the bytes;
  the citation goes beside them instead.

### Review checklist

- Does this fact have exactly one definition, and can a reader find it?
- If it is copied, is the copy generated or drift-checked — and by what?
- Does the drift check derive from the authority, or from another copy?
- If a test repeats a value, is the reason independence, and is the external
  rule cited?
- Would a wrong implementation constant still make the test fail?

## Rule 4: use intention-revealing names and explicit units

> Names MUST reveal role and meaning; boundary types MUST make width,
> signedness, direction and units explicit. Use the existing `_r`, `_w`, `_p`,
> `_S`, `_C` and `_P` suffixes, and add a unit or domain qualifier — `_ns`,
> `_cyc`, `_bytes`, `_bps`, or the clock domain — wherever confusion is
> possible.

This **extends** the house style in [CONTRIBUTING.md](../../CONTRIBUTING.md);
it does not compete with it. The suffixes there say what a signal *is*
(registered, wire, pulse, state, parameter). A unit qualifier says what its
value *means*. A port can need both: `ring_len_bytes_i` is an input carrying a
length in bytes.

### The qualifier table

| Concern | Qualifier | Example | Why the bare name is not enough |
|---|---|---|---|
| Time | `_ns`, `_us`, `_ms`, `_sec` | `pres_ofs_ns_i` | An offset in cycles and an offset in nanoseconds are the same 32 bits and a different value |
| Cycle counts | `_cyc` | `timeout_cyc_c` | A cycle count is only meaningful beside its clock |
| Size and position | `_bytes`, `_samples` | `ring_len_bytes_i` | A ring length in bytes and in records both fit; only one is right |
| Rate | `_bps`, `_hz`, `_ppb` | `idle_slope_bps_i` | idleSlope is a rate; a bare number invites a per-frame reading |
| Clock domain | domain name | `gtx_ts_ns_w` | The domain is the difference between a valid read and a metastable one |
| Predicate | reads as a question | `is_talker_w`, `has_listener_w` | A boolean named for a noun does not say which way true points |
| Event | `_p` (existing) | `arm_p` | A pulse and a level need different consumers |
| Boundary type | explicit width and sign in the declaration | `input logic signed [31:0] hi_credit_bytes_i` | A bare `[31:0]` on a credit that can go negative documents the width and hides the sign; the cast at the consumer then decides it silently |
| C++ harness | the same qualifier on the field or argument | `int32_t idle_slope_bps;` in `cbs_ref_model.h`, `run_rate(…, uint32_t idle_slope_bps, …)` | The reference model is graded against the DUT in the same unit; a field called `idle_slope` beside a port called `idle_slope_bps_i` is the confusion moved one file over |
| Python builder | the same qualifier on the key or argument | `egress_lat_ns`, `ring_len_bytes` | A builder key feeds a CSR default; a reader of the YAML has no type to fall back on, only the name |

Cross-language, the concept keeps its name and its unit: a value that is
`egress_lat_ns` in SystemVerilog is `egress_lat_ns` in the builder and in the
harness. A rename that stops at the module boundary has moved the confusion
rather than removed it — which is why the shaper rename below reaches the
reference model's fields and the harness helpers' arguments, not only the
`dut->` bindings.

### What a qualifier is not for

- Not for a signal whose width is its meaning. A port's bit width is already
  in its type; `_bits` restates the declaration.
- Not for pulse shape. "One-cycle strobe" is what `_p` already says, and
  spelling it `_cyc` would make the two conventions disagree.
- Not for identifiers a published protocol owns. `s_axi_awaddr` is documented
  as a byte offset and keeps its name, because the name is AXI's contract, not
  ours.

### The interface renamed end to end

The credit-based shaper's configuration interface carries three quantities with
three different units, and none of them said so. It is renamed here through
every hop it crosses — the CSR block, the datapath, the top level, the shaping
core, the controller, the shaper itself, four testbench wrappers and their
harnesses, and the register documentation:

| Was | Now | Unit, from its own documentation |
|---|---|---|
| `o_cbs_hi_credit`, `hi_credit_i` | `o_cbs_hi_credit_bytes`, `hi_credit_bytes_i` | signed bytes |
| `o_cbs_lo_credit`, `lo_credit_i` | `o_cbs_lo_credit_bytes`, `lo_credit_bytes_i` | signed bytes |
| `o_cbs_idle_slope`, `idle_slope_i` | `o_cbs_idle_slope_bps`, `idle_slope_bps_i` | bits per second |

`hiCredit` and `loCredit` are 802.1Q terms and keep their spelling; only the
unit is added. The rename is pure — no logic moved — and the shaper's own
harnesses grade the result, including the cycle-accurate reference model,
whose `CbsConfig` fields and slope helpers carry the same qualifiers
(`idle_slope_bps`, `hi_credit_bytes`, `lo_credit_bytes`). The package functions
`calc_hi_credit`/`calc_lo_credit` in `ethernet_packet_pkg` keep their names:
they are 802.1Q's formula names, and their arguments are typed `int` with the
unit in the function's own `//!` line.

### Review checklist

- Does the name say what the value means, not just where it came from?
- If the value has a unit, is the unit in the name or only in the comment?
- Does a boolean read as a predicate, and is a pulse distinguishable from a
  level?
- At a cast, is the truncation or sign change documented — or is the cast
  hiding a law nobody wrote down?
- Does the concept keep its name across the module, the builder and the tests?

## Measuring hidden units

The evidence is the port's own `//!` comment. Those comments say what the value
is — "Egress latency correction, ns", "hiCredit clamp, signed bytes" — and when
the comment names a unit and the identifier does not, the unit is known and
simply missing from the name. A reader can check any finding in one line.
The converse is measured too, and is the worse finding: when the identifier
carries a unit and the comment documents a different one, the name is not
vague, it is wrong.

[`scripts/measure_naming.py`](../../scripts/measure_naming.py) does that scan.

```
python3 scripts/measure_naming.py                # candidates + the per-tree table
python3 scripts/measure_naming.py --excluded     # every filtered match, and why
python3 scripts/measure_naming.py --check        # the identity ratchet
python3 scripts/measure_naming.py --write-budget # regenerate the budget after a rename
```

**What is scanned, and what is not.** Every module header — ports and
parameters — in first-party `.sv` under `hdl/` across the superproject and both
project-owned processor submodules: 117 files, 3459 ports and 539
parameters at this head. Declarations are parsed rather than pattern-matched,
so `output reg`, `int`, package-typed and interface-modport ports, packed and
unpacked dimensions, declarations split across lines and names sharing one
declaration are all boundaries. Function and task arguments in module bodies
are not boundaries and are not counted. Outside the scan, and said so here
rather than left to be discovered: signals declared inside an `interface`
body, and `hdl/milan/milan_dma_wrapper.v`, the generated Vivado wrapper the
lint gate already excludes with its reason.

**The blind spot has a size.** A port with no `//!` at all cannot be judged
here, and the house style's "one on every port" is a rule with debt behind it:
417 of the 3459 ports carry no comment. That population is Rule
5's ratchet, not a Rule 4 finding, and the tool prints it per tree so a
processor reading as nearly clean can be told apart from one that is merely
undocumented — the gPTP processor's 1 candidate sits beside its
24 undocumented ports:

| Tree | Files | Ports | Parameters | Documented | Undocumented | Unit in the name | Unit in the comment | Excluded | Named for another unit | Candidates |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| superproject | 69 | 1754 | 259 | 1709 | 304 | 99 | 268 | 182 | 5 | 86 |
| protocol-processor | 42 | 1547 | 265 | 1692 | 120 | 99 | 182 | 161 | 1 | 21 |
| gptp-processor | 6 | 120 | 6 | 102 | 24 | 7 | 20 | 19 | 0 | 1 |
| total | 117 | 3421 | 530 | 3503 | 448 | 205 | 470 | 362 | 6 | 108 |

**The false positives were measured before anything was gated**, because the
naive form of this check is mostly noise: 470 declarations match a unit
word in their comment and 362 of them are not findings. Four exclusion
classes, each printed in full by `--excluded` with its reason:

| Excluded | Count | Reason |
|---|---:|---|
| Noun for the value, or timing prose | 312 | "write byte", "subframe A sample", "(byte 0 = MSB)" name what the value *is*, "applied on the cycle `en` is high" says *when*, and "1-cycle pulse" or "16-byte aligned" is an adjective; a singular byte, octet, sample or cycle is a unit only after "in", "per" or "every" |
| Single-bit ports | 50 | A one-bit port carries no quantity, so a unit cannot be missing from it |
| Protocol-fixed identifiers | 0 | The published AXI4/AXI-Stream signal names (`s_axi_awaddr`, `m_axis_tdata`) keep their names; a prefix alone earns no exemption |
| Shape, not unit | 0 | "held 2 cycles", "per cycle" describe shape, which `_p` already encodes; applied only when the matched unit is the cycle one, so "length in bytes, sampled every cycle" still counts |

`bit`, `bits` and `word` are not in the unit vocabulary at all: bit width is
already explicit in the SystemVerilog type, and "word" is used in this tree
both as a count and as a noun for the value itself. The pronoun "us" and the
ordinal "second" count only in a unit context ("hold time, us", "1 second"),
and a unit word joined by a hyphen into an identifier or an adjective
(`P-RX-SLOT-BYTES`, "byte-identical", "cycle-count width") is prose.

That leaves **108 candidates**, **6** of them named for a different unit
than they document. The residual set still holds judgement calls — `now_i` on
a module whose entire subject is nanoseconds is arguable — so this ships as a
ratchet, not a verdict.

**A wrong unit is a candidate too.** The first form of this tool stopped as
soon as the identifier carried any unit token, so `timeout_bytes_i //!
timeout in cycles` satisfied a cycles contract and fell out of the ratchet;
review caught it. Units are now compared by family, defined once in the tool:

| Family | Spellings, in a comment or as a `_`-delimited token |
|---|---|
| time | `ns`, `us`, `µs`, `ms`, `nsec`, `usec`, `msec`, `sec`, `second(s)`, `nanosecond(s)`, `microsecond(s)`, `millisecond(s)` |
| bytes | `byte(s)`, `octet(s)` |
| cycles | `cyc`, `cycle(s)`, `clock cycle(s)`, a counted `clocks` ("in clocks", "6250 clocks") |
| frequency | `hz`, `khz`, `mhz`, `ghz`, `hertz` |
| ratio | `ppb`, `ppm` |
| rate | `bps`, `kbps`, `mbps`, `gbps`, `bits/s`, `bits per second`, `bytes per second` |
| samples | `smp`, `sample(s)` |

so `_ns` satisfies "nanoseconds" and `_cyc` satisfies "clock cycles". A
unit-named boundary is a candidate when its comment documents a unit of
measure and never names the name's family at all — nouns count, so "tone
generator sample" confirms `tone_smp_i` — or when the comment states the
value as "X per Y" and the name carries only Y: `DIV_US_P //! clk cycles per
1 µs tick` is a cycle count named for the tick it produces. Comparing against
the first documented word alone was measured and rejected: it would have
recorded `MILAN_CLK_FREQ_HZ_P` because "ns" appears in the second sentence of
its comment and "125 MHz" in the fourth. Of the exclusion classes, *noun* and
*shape* carry over, because they say the comment documents no unit of measure
and there is nothing to compare; *protocol-fixed* carries over because the
name is not ours to change; *single-bit* does not, because it excused a unit
that was missing from a port with no quantity, and a unit that is present and
wrong is a false statement at any width — `go_ns_i //! start, in cycles` is a
candidate.

**The ratchet is keyed on identity, not a count.**
[`scripts/naming.budget`](../../scripts/naming.budget) names every candidate as
`path:module:port` — a processor entry as `submodule:path:module:port`, the
`xvlog.budget` spelling, so the generated record is never read as a
hand-written copy of a processor source list. A candidate may leave the list
only by being renamed with its unit or by being removed — or, for a name that
already carries a unit, by a comment that now names that unit's family,
because the tool cannot tell a conversion (`SETTLE_CYC_C //! clean-clock hold
(~21 ms)`) from a contradiction and the diff can; a port still declared under
the same name whose comment has merely lost the unit word is refused as
*stripped*. Review found
the count-only form of this ratchet could be paid down by deleting units from
documentation — the opposite of the rule — and reported it as a lowering. No
new identity may appear either, in any of the three trees; the arms inject one
into each processor and require the refusal. After a genuine rename,
`--write-budget` regenerates the list and the diff shows exactly which
boundary gained its unit.

## Rule 5: make ports, contracts and ownership explicit

> Every state element has one owner. Dependencies cross production boundaries
> through explicit, named ports. Each interface documents its inputs, outputs,
> side effects, clock domain, reset state, and handshake or backpressure law.
> The module declaration and each instantiation must make the boundary
> reviewable without searching the implementation for hidden connectivity.

[CONTRIBUTING.md](../../CONTRIBUTING.md) already states half of this — "Ports
documented **inline with `//!`** — the port list IS the spec". Nothing checked
it. Across the superproject and both project-owned processor submodules, 394 of
3,392 module ports carried no contract before the representative cleanup, and
376 after it. The first version of this section said 222 of 2,003: its private
header parser ended a `module X import pkg::*;` header at the import's `;`, so
the 23 modules written that way — all three integration tops among them —
contributed no ports at all, and review caught it. The ports now come from the
one shared parser, [`scripts/sv_ports.py`](../../scripts/sv_ports.py), that
Rule 4 reads too.

### What a port contract states

Not what the signal is called again in prose. A contract answers the questions
a reader would otherwise have to answer by reading the body:

- **role and units** — what the value means, in what unit (see Rule 4);
- **clock domain** — which clock it is valid in, and whether it crosses one;
- **reset state** — what it reads after reset, and whether reset clears it;
- **level or pulse** — a one-cycle strobe and a held level need different
  consumers, and confusing them is silent;
- **handshake law** — for a stream, when a beat transfers, whether valid may
  wait on ready, and what backpressure does;
- **side effects** — what else moves when this port moves.

A group comment over a cohesive bundle is the contract for that bundle. One
`//!` above an AXIS valid/ready/last triple says more than three comments
reading "valid", "ready", "last". The gate reads that as an explicit bundle
rule: a standalone `//!` run documents every port beneath it until a blank
line, a port carrying its own `//!`, the next standalone run, or the `)(`
between the parameter list and the port list. So a port added inside a
documented bundle inherits that bundle's contract, and one added after a blank
line owes its own — which is why a new port is written beside the bundle it
belongs to, or with its own comment, never floating.

The declaration and the use site carry the same boundary. This is the good
shape: typed, documented ports and named connections.

```systemverilog
module queue_gate (
  input  logic clk_i,        //! queue clock; all ports are synchronous here
  input  logic request_i,    //! level request, held until ready_o is observed
  output logic ready_o       //! level response; no side effects until high
);

queue_gate u_gate (
  .clk_i    (clk_i),
  .request_i(request),
  .ready_o  (ready)
);
```

These are bad shapes because a reviewer cannot establish the same contract at
the boundary:

```systemverilog
module queue_gate(input clk_i, input request_i, output ready_o); // no contract
queue_gate u_by_order (clk_i, request, ready);                    // positional
queue_gate u_by_name  (.*);                                      // implicit
assign ready = u_by_name.ready_r;                                // child backdoor
```

A tool-owned primitive or generated wrapper is a narrow exception, not a way
to make first-party boundaries implicit. Keep the form required by that owner
and put the disposition at the connection:

```systemverilog
vendor_axis_fifo u_vendor_fifo (
  .m_axis_tid() //! vendor-only optional metadata; this design carries no ID
);
```

### Three refusals and two ratchets

The five parts of this rule are checked differently on purpose.

**Wildcard `.*` bindings are refused outright.** A `.*` connects by name at
elaboration, so adding a port to a child silently rewires every parent with no
diff at the instantiation site.

**Positional bindings are refused outright** — port lists and parameter lists
alike, instance arrays included — for the same reason with a sharper edge:
reordering a child's ports or parameters rewires every positional parent
silently, and the widths usually still fit. Only modules this tree declares are
judged — a vendor primitive or a generated wrapper keeps whatever form its tool
requires. Both refusals print `path:line`, because the instance they name may
sit in a 4,000-line integration top.

**Production hierarchical reads are refused outright.** A reference is
recognised by its first component: an instance the file declares (first-party
or foreign — a read through a vendor FIFO's `rd_ptr_reg` is still a backdoor),
a module name this tree declares (the `top.a.b` shape), or `$root`. String
literals are blanked first, so `$display("u_x.hit")` is not a read.
Interface/modport member access is not a child-instance backdoor and is
intentionally outside this population.

All three hidden-connection populations are **zero today**: wildcard and
positional bindings, plus production reads through a child instance hierarchy.
That is precisely why the arms that prove
those checks bite matter more than the counts. A gate with an empty population
is indistinguishable from a gate that does nothing, so
[`scripts/check_port_contracts.py`](../../scripts/check_port_contracts.py)
carries fixtures for a wildcard binding (with its line), a positional port list
and a positional parameter list, instance arrays in all three forms, a
declaration naming several instances after one head (`child u_ok (.a(a)),
u_bad (.*);` is legal, and the first version of the walk stopped after the
first connection list, so review found `u_bad` passing: a wildcard and a
positional list on a later instance, a clean pair, a three-instance form with
an array and a parameterised head, and an open, a literal-bound and a
hierarchically read port on the second instance), a named and a parameterised
named binding, a foreign module, control flow that must not read as an
instantiation, a commented-out binding, a string literal that must not read as
a reference, a backdoor through a first-party and through a foreign instance,
a module-name-rooted and a `$root` reference, an `import` header, a non-ANSI
header, and an empty and a partial population — 80 arms, each of which fails
when the defect it guards is put back.

**Undocumented ports are ratcheted, not refused.** There are 376 of them after
the receive-filter cleanup: 246 in `hdl/`, 19 in `gptp-processor`, 111 in
`protocol-processor`, each tree held to its own line in
[`scripts/port_docs.budget`](../../scripts/port_docs.budget) so a processor's
debt is never traded against the superproject's. A flag-day pass over every one
would be exactly the churn the governing rule forbids, so each count may only
fall. Two shapes the census cannot count are refused rather than read as zero:
a header whose port list names ports without a direction (the non-ANSI form,
whose directions live in the body), and a population that is empty or in which
any of the three trees contributes no file or no parsed port — exit 2, named,
because a pathspec or checkout problem must never look like a green gate. The
[shared scope](../../scripts/code_quality_scope.py) refuses an absent or
off-pin processor the same way, before anything is counted.

**Open and literal-bound connections are ratcheted by identity, not refused.**
An open status output or a tied-off input can each be the clearest boundary —
the receive filter leaves the TCAM's winning index and multi-hit vector open
on purpose — so the issue asks for a local rationale, the way a lint waiver
carries one, rather than a count. The gate inventories every open (`.x()`) and
literal-bound (`.x(1'b0)`, `.x('0)`) named connection on a first-party child,
reads a connection as justified when a comment sits on its line or a comment
run sits directly above the contiguous run of such connections it belongs to
(a blank line, an ordinary connection or a sibling with its own comment ends
the run), and records every one without a rationale as `path:instance.port`
in the same budget. A line may only leave, by adding the rationale or removing
the port; none may be added. Whether the comment *is* a rationale is review's
job; that one exists is the gate's.

The gate uses the shared code-quality scope, so the project-owned
`protocol-processor` and `gptp-processor` submodules are included and must be
checked out at their pins. It does not write its own list of individual HDL
exceptions: it imports `LINT_EXCLUDE` from
[`scripts/lint_rtl.py`](../../scripts/lint_rtl.py), which already owns that
question and records a reason for each entry. `hdl/milan/milan_top.sv` is in it
— a Zynq top no build compiles and that cannot elaborate here — and documenting
its ports would decorate a file every gate already ignores.

### Audited boundary inventory

The inventory is deliberately broader than the three refusals. Run
`python3 scripts/check_port_contracts.py --list` to reproduce the file and line
detail. Its scope is exact: the tracked `.sv` and `.svh` files under `hdl/` in
the superproject and in both project-owned processor submodules for every row
but the last, and the tracked `.sv` test wrappers under the `tb/` trees for the
last. Every number below is the tool's output at this head.

| Population | Result | Disposition |
|---|---:|---|
| Module ports | 3,392 total (`hdl/` 1,725; `gptp-processor` 120; `protocol-processor` 1,547); 376 undocumented | Documentation debt is ratcheted per tree at 246 / 19 / 111. |
| Wildcard first-party bindings | 0 | Refused, by `path:line`. |
| Positional first-party bindings | 0 | Refused — port and parameter lists, instance arrays included. |
| Production child-state references | 0 | Refused — rooted in a declared instance, a declared module name or `$root`. |
| Non-ANSI headers | 0 | Refused: the census cannot count ports declared in the body. |
| State with multiple procedural owners | 0 `MULTIDRIVEN` in 104 module elaborations | 66 in `hdl/` (`scripts/lint_rtl.py --check`), 1 in `gptp-processor` (`make lint`: `KL_gptp_engine` with its hierarchy), 37 in `protocol-processor` (its own `lint_hdl.sh` lint sweep); the scanned sources declare 109 modules and 1 interface, which is a different number. |
| Open named child ports | 92, of which 60 carry no local rationale | Inventory, ratcheted by identity: optional status outputs can be intentionally unused, and the ones that are say so at the connection. |
| Literal-bound named child ports | 43, of which 16 carry no local rationale | Inventory, ratcheted by identity: resets, feature disables and unused inputs each need a local rationale. |
| Test-only hierarchical observations | 80 in 7 `.sv` test wrappers (superproject `tb/` 46; `protocol-processor` 34) | Confined to tracked `tb/` trees and read-only; production behavior cannot depend on them. |

The open/literal populations are syntax-level review leads, not a claim that
135 defects exist; the 76 without a rationale are the list that may only
shrink. The representative boundary below makes its two ignored TCAM
diagnostics explicit and states why, and the datapath does the same for the
three verdict rails it leaves open. Test backdoors remain observable in the
list output rather than disappearing behind a production count of zero.

Two populations sit outside the inventory, named here so the table is not read
as complete. The C++ harnesses reach into the DUT through Verilator's root
access (`__DOT__`): 73 lines in 7 files under
[`tb/verilator/`](../../tb/verilator) — `milan_dp/sim_nxn.cpp` 38,
`pp_shadow/sim_main.cpp` 14, `milan_dp/sim_gptp.cpp` 12, `tkdiag/sim_main.cpp`
5, `crf_rx/sim_main.cpp` 2, `milan_dp/sim_main.cpp` 1, `milan_dp/sim_aclk.cpp`
1 — test-only by construction and not counted above. And the gPTP processor's
board bench RTL, the `bench/arty` directory of the submodule, is synthesizable
(its top instantiates `KL_gptp_engine`) but outside the `hdl` pathspec: 6
files, 70 ports, 64 undocumented, neither ratcheted nor judged. The 57 tracked
`.sv` files under `tb/` and `bench/` are inventoried for hierarchical reads
only; a hand run of the gate's own functions over them finds 0 wildcard and 0
positional bindings today. Two narrower limits: the one `interface` header in
the tree (`hdl/common/axi_stream_if.sv`, two ports and four parameters) is
outside both Rule 4's and Rule 5's port census, because the shared parser
reads `module` headers; and a hierarchical reference rooted in an instance
that another file declares, or in a name a macro introduces, is not seen. All
of this is recorded in the script's docstring as well.

### The boundary documented as proof

`hdl/ieee8021q/filtering/rx_mac_filter.sv` is the receive shield: it decides
which frames reach the host at all, and eighteen of its ports carried no
contract. Each of its four bundles now states the law a consumer needs:

- the **TCAM write port** is level-driven with no handshake; the lookup is
  combinational on the live table and the verdict is latched only when the
  first beat is *accepted*, so a write lands in whichever frame has not yet
  handed over its first beat — a first beat stalled on `m_tready` is re-judged
  by it — and retimes only the next lookup once the first beat is through;
- the **sink** is standard valid/ready, and `tready` is passed through for an
  accepted frame and forced high for a dropped one, so a dropped frame is
  consumed at full rate instead of stalling the MAC;
- the **source** squashes a dropped frame by holding `tvalid` low for its whole
  length, so a consumer never sees a partial frame or a `tlast` with no first
  beat — and it names its one known bend: while the first beat is stalled, a
  TCAM or policy write that flips the verdict withdraws `tvalid` without a
  transfer, which AXI4-Stream (ARM IHI 0051A Section 2.2.1, `TVALID` holds until the
  handshake) forbids;
- the **verdict** rails are levels that follow the live lookup while a first
  beat is stalled and hold from the first accepted beat to `tlast`, and are
  observation only — nothing may drive backpressure from them, because the
  frame they describe is already in flight.

None of that was inferable from the port list before, and all of it is
load-bearing for anyone connecting to this module. The first version of this
contract said the opposite of the first bullet — "the verdict is latched at
the frame's first beat" — and review caught it with a probe: a first beat
presented with `m_tready` low, then a one-cycle TCAM write of a drop entry for
that address, and `m_tvalid` went from 1 to 0 with no transfer. The rule this
section states is that the port list *is* the spec, so the contract now states
the law the RTL implements, bend included, and the focused suite pins that
sequence (stalled first beat, TCAM write, `m_tvalid` withdrawn, frame dropped;
the same for a policy write; and a write after acceptance holding for the
in-flight frame and landing on the next) so the contract and the RTL are
graded together. Removing the bend is a functional change with its own ticket,
not a documentation edit: when it lands, the checks that pin the withdrawal
are the ones that must be rewritten with it.

The internal TCAM seam is explicit as well: `tcam_match` and `tcam_action`
carry the named child outputs into the frame decision, while the unused winning
index and multi-hit vector are open beside their local rationale. The focused
suite's `binding-negative` target
([`tb/verilator/rx_filter/binding_mutant.py`](../../tb/verilator/rx_filter/binding_mutant.py))
then applies the four binding defects the issue names, one at a time, to a
copy of the RTL, and builds each with the Makefile's own recipe — read through
`make -s print-vflags`, not a second copy of `VFLAGS` — so the mutants and the
clean run share one boundary. What each arm proves is exactly this:

- a **missing** binding (`.lookup_key_i` dropped) and a **direction-wrong**
  port (the child's `lookup_key_i` declared `output`; the filter's own
  `m_tready` declared `output`) are refused at the build **by name** —
  `%Error-PINMISSING`, `%Error-UNDRIVEN` — because the recipe promotes those
  two warnings to errors even under `-Wno-fatal`. Verilator inlines the child
  and erases direction, so a direction error has no behavioural signature:
  review measured the child mutation building with a warning and running
  62/62 under the old flags. Without the two `-Werror` flags three of the five
  arms fail, which is the mutation that proves them;
- a **swapped** binding (`wr_key_i`/`wr_mask_i` exchanged) and a **tied-off**
  one (`.lookup_key_i(48'b0)`) are legal SystemVerilog, so they build, and the
  unmodified harness must reject them with its own `RESULT: FAIL` (5 and 11
  failing checks of 78); a build failure does not count for these two.

The clean run is a prerequisite, so a harness that rejects everything cannot
satisfy the arms. The seam is therefore observable through real ports rather
than through a test-only child-state read, and the boundary's direction is
guarded by the build, not by a check that cannot see it.

### Review checklist

- Can a reader connect to this module without opening its body?
- Does each port say its clock domain, its reset state, and level versus pulse?
- For a stream, is the handshake law written down — including what
  backpressure does?
- Is every instantiation connected by name?
- Does any production path depend on a hierarchical reference or a test
  backdoor?
- Is a tied-off or ignored port justified locally, or is it decorative?

## Rule 6: fail fast and encode invariants

> Invalid parameters, configurations, states, inputs and tool failures MUST be
> rejected at the nearest responsible boundary and MUST propagate a non-success
> verdict. Important invariants and reset or overflow laws are executable
> assertions or self-checking tests, not comments alone.

The failure mode this rule exists for is not a crash. It is a build, a
generator or a gate that reports something wrong and then exits 0, because
everything downstream then treats a wrong answer as a checked one.

### Repository interpretation

- A shell, Tcl or Python step checks the status of what it ran, and never
  prints a failure and returns success.
- SystemVerilog rejects impossible parameter combinations **at elaboration**,
  where the message can still name the parameter and the law it broke.
- Counter wrap, saturation, reset and update priority are stated and tested.
- An assertion carries a message naming the contract it violated, not just the
  expression that failed.

### A comment is not a guard

`hdl/ieee8021q/filtering/rx_mac_filter.sv` is the receive shield. Its banner
said the destination-address compare works "for TDATA_WIDTH>=48", and nothing
enforced it. At 32 bits the concatenation that builds the destination address
indexes past the end of the beat, the compare runs against whatever those bits
are, and the shield silently admits or drops the wrong frames — a failure no
downstream check can see, because a filter that is wrong looks exactly like a
filter that is right until the traffic is inspected on the wire.

It now carries an elaboration contract in the house form — a module-scope
`if (…) $error("one format string", …)`, the same shape `milan_datapath` and
`KL_media_nco` already use. Four laws: the datapath must be wide enough to hold
the 48-bit destination address in one beat, it must be a whole number of bytes
so `tkeep` can describe it, the TCAM must have at least one entry, and an
action must be wide enough to distinguish two matches.

**The contract is graded by mutation, permanently.** `make negative` in
`tb/verilator/rx_filter` elaborates four illegal parameter sets and requires
each to be refused, then elaborates the legal default and requires it to be
accepted. That last arm is what stops the contract from becoming a ban, and it
is why the arm reads the exit status directly rather than through a pipe — a
pipeline returns its *last* command's status, which is how a refused build
reads as a pass.

### The two populations, measured

[`scripts/measure_fail_fast.py`](../../scripts/measure_fail_fast.py) counts
both ways a failure can pass for success here.

| Population | Count | Disposition |
|---|---:|---|
| Parameterised modules with no elaboration contract | 37 of 42 | Ratchet. Paid down as modules gain contracts. |
| Pipelines that discard their producer's exit status | **0** | Ratchet at zero. It must stay zero. |
| Pipelines waived because the consumer *is* the assertion | 27 | Named, with the reason recorded |

The waiver matters: `verilator --version | grep -F "$WANT"` wants grep's status,
because grep is the assertion. Those are excluded by name rather than by
pattern, so a new one has to be added deliberately.

Both false positives that this check produced on its first run were in the
checker, not the tree: a tool name inside a `printf` **format string** read as
a command, and a pipe inside a `$(…)` substitution — whose status is never the
line's verdict — read as a masked one. Quoted spans and substitutions are
blanked before the producer search, and both cases have arms.

### Already satisfied, and verified rather than rebuilt

The rule also asks that suite tally parsing treat missing or malformed evidence
as failure rather than zero checks.
[`scripts/suite_tally.py`](../../scripts/suite_tally.py) already does: a suite
whose log carries no readable tally is `NOCOUNT`, an unknown is never allowed to
look like agreement, and a skip marker cannot suppress it. That was confirmed by
running its self-test, not by writing a second one.

### Review checklist

- If this step fails, does the caller find out — or does it print and continue?
- Is the invariant executable, or only written in a comment?
- Does the assertion message name the contract, or only the expression?
- Is there an arm proving the refusal fires, **and** one proving the legal case
  still passes?
- Does any verdict travel through a pipe?

## Rules not yet landed

The contract is ten rules. Rules 1 to 6 are above; the rest keep these
numbers so citations stay stable as they land:

| Rule | Subject |
|---|---|
| 7 | Comments explain why; no dead or speculative code |
| 8 | Deterministic, specification-derived tests |
| 9 | Automated mechanical hygiene with measured ratchets |
| 10 | Idiomatic SystemVerilog and explicit HDL boundaries |

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
instantiations, package references and interface/modport types, transitively —
and checks each consumer carries every file in it. A declaration makes a child
part of that walk; a hard-coded naming-prefix allowlist does not. That
distinction is load-bearing for `protocol_processor_top` and
`credit_based_shaper`, whose ordinary names were silently absent from the first
version of the closure. Package-only and interface-only files are equally
load-bearing even though they instantiate no module.

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
  no print mode: its quoted superproject entries are combined with the same
  `scripts/pp_srcs.py` expansion that `milan_soc.py` calls for the
  protocol-processor half.

The unit is the **file**, not the module, because that is what a source list
carries and one file may declare several modules — `KL_aaf_latency_chain` lives
inside `KL_aaf_latency_taps.sv`. Comparing module names to file entries would
demand entries that must not exist.

A consumer whose tooling is absent is reported `SKIPPED` by name and the verdict
says it is not covered. A gate that silently drops a consumer it could not reach
is how a list goes unchecked for months.

### The named-constant half

`milan_datapath` passed `16'h88F7` to the timestamp unit's `ETH_TYPE`
parameter while already importing `ethernet_packet_pkg`, which defines that
exact value as `ETH_TYPE_PTP`. That is a second definition of a fact the package
owns, and it is now the package's name.

The inventory behind that choice: 57 hexadecimal literals appear in four or more
first-party files. They classify into three kinds, and only the first is debt.

| Kind | Example | Disposition |
|---|---|---|
| Drift — a named definition exists and the literal ignores it | `16'h88F7` beside `ETH_TYPE_PTP` | Fix. Done here for the one site whose module already imports the package. |
| Structural rails and saturation values | `0xFFFF`, `0xFFFFFFFF`, `0x0000` | Not duplication. The same rail in unrelated modules is a coincidence of width, not a shared fact. |
| Deliberate independent oracles | `0x22F0`, `0x88F7`, `0x8100` in tests and wire-truth tools | Keep. See below. |

Three further sites (`hdl/milan/KL_pp_shadow.sv`,
`hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv`,
`hdl/ieee8021as/gptp_plane/KL_gptp_txstamp.sv`) spell the same EtherTypes raw
but do **not** import the package. Adding an import to three modules changes
their compile dependencies, so it is a separate change with its own
verification rather than a rider on this one.

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

## Rules not yet landed

The contract is ten rules. Rules 1, 2 and 3 are above; the rest keep these
numbers so citations stay stable as they land:

| Rule | Subject |
|---|---|
| 4 | Intention-revealing names and explicit units and types |
| 5 | Explicit ports, contracts, ownership and side effects |
| 6 | Fail fast and encode invariants |
| 7 | Comments explain why; no dead or speculative code |
| 8 | Deterministic, specification-derived tests |
| 9 | Automated mechanical hygiene with measured ratchets |
| 10 | Idiomatic SystemVerilog and explicit HDL boundaries |

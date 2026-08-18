# Testing methodology — levels, oracles, and the rules every lane is bound by

Status: 2026-07-28. Normative for every work lane in this repo.

This page is not a list of suites — [`RUNNING_TESTS.md`](RUNNING_TESTS.md) and
[`TESTING.md`](TESTING.md) are that. It is the set of rules that decide whether a
test is worth having at all, derived from the failures that got through the ones
we already had.

## Contents

- **[1. Why this exists — nine escapes, sorted by cause](#1-why-this-exists--nine-escapes-sorted-by-cause)** — The evidence base. Nine defects that shipped or nearly shipped while every gate was green, grouped by *why* they escaped rather than by what they were. Two causes account for all nine: a missing tier (nothing tests the binding between a module and the fabric around it) and a broken oracle (a check whose reference is our own behaviour cannot find our own bugs, and can invent defects that do not exist).
- **[2. The six levels and their oracles](#2-the-six-levels-and-their-oracles)** — Every test sits at a level, and each level has exactly one kind of oracle. The table names what each level can and cannot see. Read the L1 row first: it is the tier this repo was missing, and six of the nine escapes live there.
- **[3. The rules — R1 to R7](#3-the-rules--r1-to-r7)** — The binding rules, each with the escape that motivates it. R1 (name the oracle) is the whole of roadmap item 00 in one sentence; R2 (a check that cannot fail is not a check) is the one that has already had to be applied retroactively to a check in this tree.
- **[4. What a lane owes](#4-what-a-lane-owes)** — The per-lane contract: what must be true before a lane reports done, including the level and oracle declaration for every check it adds, and the runnable hardware acceptance procedure it hands back.
- **[5. When a bug is found — open a lane, do not detour](#5-when-a-bug-is-found--open-a-lane-do-not-detour)** — The rule for defects discovered outside a lane's scope: record it, hand it a fresh context, and keep the finding lane on its own subject.

## 1. Why this exists — nine escapes, sorted by cause

Every one of these was green across the whole desk gate set at the moment it was
broken — 57 Verilator suites, ~2.1 M checks, yosys 48/48, the behave
compliance suite, and lint at ratchet.

A tenth escape belongs in that list and is the reason the count above is
approximate: **the aggregator that produced it was itself under-reporting.**
It recognised one of the five summary shapes the tree emits, so 29 of 57 suite
logs contributed zero, and it read `N checks: P PASS, F FAIL` as `P` — correct
only while those suites had no failures. The instrument that measured our
confidence had the same defect shape as escapes 2 and 3: a structural zero
reading as a measurement (R5). Fixed 2026-07-28; the tally now fails the sweep
on any log it cannot account for, and refuses concurrent runs rather than
reporting a corrupted total.

| # | escape | what it slipped past |
|---|---|---|
| 1 | a talker advertised 8-channel audio and emitted 2 | every gate in the repo; only an outside device noticed |
| 2 | the RMON event bus was tied to `0` at the SoC | every module test — they drive the port directly |
| 3 | the TDM capture bus is tied to `0`; the front-end yields nothing | same |
| 4 | a board routes no audio pins, so its capture front-end reads constant zero | nothing models the platform |
| 5 | a wrapper parameter name did not match the RTL parameter — a silent no-op that pruned nothing for weeks | elaboration succeeded, so nothing complained |
| 6 | a flashed device-tree window rotted against a moved register map | a perfect dead-hardware mimic, invisible to simulation |
| 7 | fifteen protocol defects an independent controller stack saw | **both** of our own controllers agreed with each other and missed them |
| 8 | a compliance check asserted a rule that was invented, not specified | it passed against us — that *was* the failure |
| 9 | a correct, specified refusal was nearly filed as a defect | a **false positive**: no clause was consulted first |

**Two causes.** Escapes 1–6 are one missing tier: we test modules, and we test
declarations against other declarations, but almost nothing tested the *binding*
between a module and the fabric around it — tie-offs, parameter names, absent
pads, generated-versus-flashed artifacts. Escapes 7–9 are oracle failures: a test
whose reference is our own behaviour cannot find our own bugs (7, 8), and a test
written without the standard invents requirements that do not exist (9).

## 2. The six levels and their oracles

Every test declares which level it observes and what its oracle is. A level with
the wrong oracle is not a weaker test, it is a misleading one.

| level | observes | oracle | structurally blind to |
|---|---|---|---|
| **L0** | one module in isolation | its own clause-derived expectation | integration, tie-offs, the platform |
| **L1** | **module ↔ wrapper ↔ platform binding** | **the fabric itself** | behaviour (it only proves things are connected) |
| **L2** | real frames across boundary ports | an integration testbench | anything outside the elaborated design |
| **L3** | conformance to the written standard | **the clause** | whether the fabric can actually do it |
| **L4** | what an independent controller sees | **a foreign implementation** | anything off the control plane |
| **L5** | the wire, on hardware | a **qualified reference device** plus a tap | nothing — but it is serial, slow and shared |

**L1 is the tier this repo was missing**, and six of the nine escapes live there.
It is cheap and it is mechanical: it asks whether a thing is *connected*, not
whether it is correct. Existing L1 gates:
[`check_wire_accountability.py`](../../scripts/check_wire_accountability.py) (what
we advertise against what the fabric emits),
[`check_entity_shape.py`](../../scripts/check_entity_shape.py) (one declared shape
across config, generated headers, registers and descriptors) and
[`check_soc_sources.py`](../../scripts/check_soc_sources.py).

**L4 and L5 are the only levels with an independent oracle**, and they are the
only reason escapes 1 and 7 were ever found. Treat access to them as scarce and
spend it on the things the other levels cannot see.

## 3. The rules — R1 to R7

**R1 — Name the oracle. "A declaration checked against another declaration" is
not one.** Every consistency gate in this repo once compared config to generated
header to register to descriptor count, and not one of them could see the wire.
That is escape 1 in a sentence, and it is why L1 exists as its own tier.

**R2 — A check that cannot fail is not a check.** Every new check ships with a
negative control. Where an independent implementation exists, run the check
against it too: if a check fails against a **qualified reference device**, the
check is wrong until a clause proves otherwise. This is not theoretical — a check
in this tree once asserted that a non-success response echoes the command, the
reference device did the opposite, and it was accepted by a real controller. The
rule was an invention (escape 8).

**R3 — Derive from the standard and cite the clause; never pattern-match our own
behaviour.** Quote the clause in the check, the test and the commit. If the
standard is silent, write that it is silent rather than filling the gap. R3 is
the guard against escape 8 in one direction and escape 9 in the other: a refusal
that a clause *requires* is conformance, not a defect, and must not be "fixed".

**R4 — The shape of the test must match the shape of the property.** An identity
property needs per-channel distinct values, because a test driving the same value
on both channels cannot detect a swap. An index-coverage property needs *every*
index. A response-size defect is invisible to a check that reads only a status
byte — which is exactly how escape 7 survived.

**R5 — A structural zero is not a measurement.** Anything the fabric cannot back
must be readable as *unsupported*, never as `0`. A counter block that reads zero
because nothing drives it is indistinguishable from a healthy idle one, and that
ambiguity is escapes 2 and 3. Publish a capability mask instead.

**R6 — Hardware claims require a hardware run.** RTL green is not silicon fixed:
the change does not exist on a board until a rebuild and a reflash. Flashed
artifacts rot independently of the design, so diff a flashed device tree's
windows against the build's register listing before trusting a board (escape 6).

**R7 — Same version on both boards before any comparative test**, and read the
version register to prove it rather than assuming.

## 4. What a lane owes

Before a lane reports done:

1. **Every check it adds names its level and its oracle** (Section 2), and cites the
   clause it derives from (R3).
2. **Coverage at L0 that matches the property's shape** (R4) — nominal, boundary
   and negative cases, with the negative case demonstrated to fail (R2).
3. **An L1 assertion for anything it binds.** A lane that adds a pad, a
   parameter, or a wrapper connection owes a check that the binding exists —
   otherwise it can reproduce the exact tie-off class it was fixing.
4. **Growth in the compliance tests, not only the unit tests.** Running them is
   the floor. The compliance layer is what catches the class of defect module
   tests structurally cannot see: [`hive_compliance.py`](../../tb/tools/hive_compliance.py)
   (add checks derived from the standard), the behave suite under
   [`tests/`](../../tests) (add scenarios with their clause tags), and a
   clause → behaviour → test row under [`traceability/`](../traceability).
5. **A runnable hardware acceptance procedure** — exact commands, exact registers
   and counters, exact expected values before *and* after. Builds and bench
   access are serial and shared, so a lane hands the procedure back rather than
   running its own build.

## 5. When a bug is found — open a lane, do not detour

A lane that discovers a defect outside its own subject **records it and hands it
to a new lane with a fresh context**. It does not fix it in passing.

Two reasons, both learned here. A defect found while doing something else arrives
with the finder's context attached, and that context is usually the wrong one for
the fix — the finder knows the symptom, not the subject. And a lane that detours
stops being reviewable: its diff acquires changes nobody asked it for, in files
another lane may own.

What to record: the symptom, the evidence that it is real, the level it was found
at, and the clause if one applies. What *not* to do: widen the current lane's
scope, or leave the finding in a report where it will be read once and lost.

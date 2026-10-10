# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""census_selftest.py - the census's --selftest: each planted defect refused by its own words, then each rule removed.

THE ARMS. Two controls, every plant of census_plants.PLANTS and two plants of
the census table:

  positive control   the tracked sources: no finding
  negative control   a copy whose only change is a comment naming a class-D
                     wire: no finding
  each plant         a planted copy, elaborated in the shapes the plant names
                     (the recipe's unless it needs a branch only another
                     shape builds), refused by a finding carrying its words
  the table plants   a row naming a field the block does not define, and a
                     row no read matches

THE MUTATION CHECK (#665, comment 6100024293). Each arm names the rule of
census_rules.RULES whose removal must let it through (the positive control
names ``keep-names``; a plant refused by sv2v or Yosys themselves, and the
negative control, name none). After judging an arm with every rule, the arm
is judged again with its rule removed, from the same netlists unless the rule
shapes the elaboration itself, and it must then be accepted. A rule fails
when no arm names it or when one that does is still refused without it, and
so does a name census_rules.py holds that no ``live()`` in census_elab.py or
publication_census.py tests, or the reverse. A rule added without a plant
therefore fails CI.
"""

from __future__ import annotations

import multiprocessing
import os
import re
import time
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any

import census_rules
import publication_census as pc
from census_elab import RECIPE, WORK, CensusError, Shape, shapes, toolchain
from census_plants import PLANTS, apply
from census_rules import RULES

HERE = Path(__file__).resolve().parent
#: The rules whose removal changes the elaboration: an arm judged without one is elaborated again.
ELABORATION = frozenset({"shapes", "shape-params", "shape-header", "opener-guard", "keep-names"})
#: The modules whose live() tests are the census's rules.
ENFORCERS = ("census_elab.py", "publication_census.py")
LIVE = re.compile(r'\blive\("([^"]+)"\)')


@dataclass(frozen=True)
class Arm:
    """One self-test arm."""

    what: str
    src: Any                                # the planted Sources, or why they cannot be planted
    table: dict
    word: str | tuple[str, ...] | None      # None: a control, which must give no finding
    rule: str | None                        # the rule whose removal must let it through
    at: tuple[Any, ...] = ("recipe",)       # census_plants.Plant.at
    tool: tuple[str, ...] = ()              # a toolchain plant's tool, and the version line it prints


def arms(src: pc.Sources) -> list[Arm]:
    """The controls, every plant, and the two table plants."""
    note = replace(src, datapath=src.datapath.replace(
        "  wire crft_class_a_w =", "  // pp_cd_srp_over_limit_w is not read here\n  wire crft_class_a_w =", 1))
    out = [Arm("positive control, the tracked sources", src, pc.CENSUS, None, "keep-names"),
           Arm("negative control, a class-D wire named in a comment", note, pc.CENSUS, None, None)]
    out += [Arm(p.what, apply(src, p), pc.CENSUS, p.word, p.rule, p.at,
                p.edits[0] if p.where == "toolchain" else ()) for p in PLANTS]
    key = ("pp_cd_srp_tk_decl_state_w", "crft_class_a_w")
    out.append(Arm("a field the contract lacks", src, {**pc.CENSUS, key: pc.Row("field", "TALKER_DECL.DECLARE", "")},
                   "which the publication block does not define", "unknown-field"))
    out.append(Arm("a stale row", src, {**pc.CENSUS, ("pp_cd_srp_granted_slope_bps_w", "lwsrp_idle_slope"):
                                        pc.Row("status", "", "planted")},
                   "stale row: the datapath no longer reads pp_cd_srp_granted_slope_bps_w", "stale-row"))
    return out


def pick(at: tuple[Any, ...]) -> tuple[Shape, ...]:
    """The shapes an arm is elaborated in: the recipe's, or the first shape the builder
    builds that binds a parameter to at least a value."""
    every, out = shapes(), []
    for want in at:
        hit = RECIPE if want == "recipe" else next((s for s in every if s.binds(*want)), None)
        if hit is None:
            raise CensusError(f"no shape the builder builds binds {want[0]} to {want[1]} or more")
        out.append(hit)
    return tuple(out)


def pinned(name: str, line: str) -> list[str]:
    """toolchain()'s refusal of a stand-in for tool name that prints line as its version, or no finding."""
    stub = WORK.path() / f"stub-{name}-{os.getpid()}"
    stub.write_text(f"#!/bin/sh\necho '{line}'\n", encoding="utf-8")
    stub.chmod(0o755)
    saved = os.environ.get(name.upper())
    os.environ[name.upper()] = str(stub)
    try:
        toolchain()
        return []
    except CensusError as exc:
        return [str(exc)]
    finally:
        if saved is None:
            os.environ.pop(name.upper(), None)
        else:
            os.environ[name.upper()] = saved


def outcome(arm: Arm, known: set[str], nets: dict) -> list[str]:
    """Every finding the census makes on one arm; a refusal, or a failure, as one finding."""
    try:
        if arm.tool:
            return pinned(*arm.tool)
        got, _ = pc.census(arm.src, arm.table, known, pick(arm.at), 1, nets)
        return got
    except CensusError as exc:
        return [f"the census cannot read it: {exc}"]
    except Exception as exc:                # a rule removed can break the census, which refuses nothing
        return [f"the census failed: {type(exc).__name__}: {exc}"]


def refused(arm: Arm, got: list[str]) -> tuple[bool, str]:
    """(the arm's verdict, why): a control holds no finding, a plant one carrying all its words."""
    if arm.word is None:
        return not got, f"{len(got)} finding(s)" + "".join(f"\n    {f}" for f in got[:3])
    words = (arm.word,) if isinstance(arm.word, str) else arm.word
    hit = [f for f in got if all(w in f for w in words)]
    return bool(hit), f"refused ({hit[0]})" if hit else f"accepted ({got[:1] or 'no finding'})"


def run_arm(job: tuple[Arm, set[str]]) -> tuple[bool, str, bool | None]:
    """One arm with every rule, then without its own: (its verdict, its line, whether
    that removal let it through; None when it names no rule)."""
    arm, known = job
    if isinstance(arm.src, str):
        return False, f"[BAD] planted {arm.what}: {arm.src}", None
    nets: dict = {}
    ok, why = refused(arm, outcome(arm, known, nets))
    line = f"[{'ok' if ok else 'BAD'}] {'' if arm.word is None else 'planted '}{arm.what}: {why}"
    if arm.rule is None:
        return ok, line, None
    census_rules.OFF.add(arm.rule)
    try:
        held, _ = refused(arm, outcome(arm, known, {} if arm.rule in ELABORATION else nets))
    finally:
        census_rules.OFF.discard(arm.rule)
    return ok, line, not held


def enforced() -> set[str]:
    """Every rule name a live() in the census's code tests."""
    return {n for f in ENFORCERS for n in LIVE.findall((HERE / f).read_text(encoding="utf-8"))}


def mutations(every: list[Arm], through: list[bool | None]) -> int:
    """Print each rule's removal and the arms planted against it; the number of rules no arm proves."""
    lines = [f"rule {n}: census_rules.RULES names it and no live() tests it" for n in sorted(set(RULES) - enforced())]
    lines += [f"rule {n}: a live() tests it and census_rules.RULES does not name it"
              for n in sorted(enforced() - set(RULES))]
    for line in lines:
        print(f"[BAD] {line}")
    failed = len(lines)
    for name in RULES:
        mine = [(a.what, t) for a, t in zip(every, through) if a.rule == name]
        held = [what for what, t in mine if not t]
        ok = bool(mine) and not held
        print(f"[{'ok' if ok else 'BAD'}] rule {name}: " + (
            "no arm is planted against it" if not mine else
            f"removed, it lets through every one of its {len(mine)} arm(s), e.g. {mine[0][0]}" if ok else
            f"removed, {len(held)} of its {len(mine)} arm(s) are still refused, e.g. {held[0]}"))
        failed += not ok
    print(f"mutations: {failed} of {len(RULES)} rule(s) no arm proves")
    return failed


def selftest(src: pc.Sources, known: set[str], jobs: int) -> int:
    """Every arm, the shaped ones first, jobs at a time, then every rule removed; the number of failures."""
    began, every = time.monotonic(), arms(src)
    every.sort(key=lambda a: -sum(w != "recipe" for w in a.at))       # stable: the larger shapes first
    WORK.roms()                        # once, here: the workers share this process's scratch directory
    failed, through = 0, []
    with ProcessPoolExecutor(max_workers=jobs, mp_context=multiprocessing.get_context("fork")) as pool:
        for ok, line, held in pool.map(run_arm, [(a, known) for a in every]):
            print(line, flush=True)
            failed += not ok
            through.append(held)
    print(f"selftest: {failed} of {len(every)} arm(s) failed; {len(every)} arm(s) and their rules' removals "
          f"in {time.monotonic() - began:.0f} s at --jobs {jobs}")
    return failed + mutations(every, through)

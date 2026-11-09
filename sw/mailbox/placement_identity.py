#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""placement_identity.py - the all-fabric datapath, elaborated in every shape, digested so two trees compare.

THE QUESTION. milan_datapath.sv gains the control placement switch, CTRL_SPLIT_P
(#665). Off, the default, the datapath must elaborate to the
netlist it elaborated to before the switch, in every shape the builder builds.
This tool states that netlist as one digest per shape, so a tree before the
switch and a tree after it compare shape by shape.

THE ELABORATION is the census's (census_elab.py): CI's recipe, the pinned sv2v
and Yosys, every module but the datapath a blackbox, each shape's header and
the builder's parameters, and the processes as cells with every connection a
buffer. Each tree is elaborated with its own census_elab.py and its own
sources, so the base needs no copy of this tool.

THE CANONICAL FORM is the datapath module of Yosys's JSON with only what
cannot mean a different circuit taken out:

  src         every ``src`` attribute: a source position moves when a line
              is added
  made names  every name Yosys made (one holding ``$``), which carries a
              source position and a counter that follows the order Yosys
              made things in; a generate scope changes that order. Each is
              replaced by a label of the structure it names (``canonical``):
              a cell by its type, parameters, attributes, the kind of name,
              and the labels of the bits its inputs read, refined round by
              round until no round adds a label; a bit by the source's name
              for it, or else by the cell output that drives it
  the scope   the all-fabric placement's generate scopes, ``g_af_*.``, as the
              census reads them (census_elab.unscoped)
  split ports the switch's own ports, ``i_ctl_*`` and ``o_ctl_*``, and the
              buffers that drive an ``o_ctl_*`` bit from a constant; the
              switch's two parameters, at their defaults 0 and 16

and nothing else. Every source-named cell, net and port, every made cell as
a multiset of its labelled records, every memory and parameter default is
compared, with its type, parameters, port directions and connections, and so
is the port list of each blackbox module a cell is.

IT REFUSES a split port that any remaining cell reads, an ``o_ctl_*`` bit not
driven from a constant, and a parameter of the switch off its default.

    python3 sw/mailbox/placement_identity.py --dump OUT.json [--tree DIR] [--jobs N]
    python3 sw/mailbox/placement_identity.py --compare BASE.json HEAD.json
    python3 sw/mailbox/placement_identity.py --selftest [--jobs N]

``--dump`` elaborates every shape of the tree (this checkout by default) and
writes each shape's digest; ``--keep DIR`` also writes each canonical form,
for a diff. ``--compare`` fails on a shape either lacks or whose digests
differ. ``--selftest`` plants defects into this checkout's datapath and
requires each to change the recipe shape's digest or be refused by its words,
beside a control that changes a comment and must not.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import multiprocessing
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPLIT_PORT = re.compile(r"^[io]_ctl_")
SPLIT_PARAMS = {"CTRL_SPLIT_P": 0, "CTRL_ENTRIES_P": 16}
FABRIC_SCOPE = re.compile(r"(^|\\)g_af_[a-z0-9]+\.")
TOP = "milan_datapath"


class IdentityError(Exception):
    """The netlist breaks a rule of the canonical form; the message says which."""


def _ce(tree: Path):
    """The tree's own census_elab, imported from its sw/mailbox."""
    sys.path[:0] = [str(tree / "sw/mailbox")]
    return importlib.import_module("census_elab")


def _h(*parts) -> str:
    """A short stable label for a structure: the sha256 of its JSON."""
    return hashlib.sha256(json.dumps(parts, sort_keys=True, separators=(",", ":")).encode()).hexdigest()[:32]


def _clean(d: dict) -> dict:
    """d without its source position, at the top and inside its attributes."""
    return {k: (_clean(v) if k == "attributes" else v) for k, v in sorted(d.items()) if k != "src"}


#: a source position inside a name Yosys made (a path, a line, a column range), and its counters
POSITION = re.compile(r"[^\s$\\\[\]]*\.(?:v|sv|svh|vh):\d+(?:\.\d+-\d+\.\d+)?")
COUNTER = re.compile(r"\$\d+")
#: refinement stops once a round adds no label, and fails past this many rounds
ROUNDS = 64


def template(name: str) -> str:
    """A name Yosys made, without its source position and counters: what kind of object it is."""
    return COUNTER.sub("$#", POSITION.sub("@", name))


def _unscope(name: str) -> str:
    """A name without the all-fabric generate scope."""
    return FABRIC_SCOPE.sub(r"\1", name)


def _fabric_cells(top: dict) -> dict:
    """The datapath's cells by unscoped name, without those that only tie a split output.

    A split output must come from a constant, and no other cell may read a split port.
    """
    split_bits = {b for p, v in top["ports"].items() if SPLIT_PORT.match(p)
                  for b in v["bits"] if isinstance(b, int)}
    cells = {}
    for name, c in top["cells"].items():
        dirs = c.get("port_directions", {})
        outs = [b for p, bits in c["connections"].items() if dirs.get(p) == "output"
                for b in bits if isinstance(b, int)]
        ins = [b for p, bits in c["connections"].items() if dirs.get(p) != "output" for b in bits]
        if outs and set(outs) <= split_bits:
            if any(isinstance(b, int) for b in ins):
                raise IdentityError(f"the split port bit(s) cell {name} drives come from a net, not a constant")
            continue
        read = split_bits & {b for b in ins if isinstance(b, int)}
        if read:
            hit = sorted(p for p, v in top["ports"].items() if SPLIT_PORT.match(p) and read & set(v["bits"]))
            raise IdentityError(f"cell {name} reads the split port {', '.join(hit)}: the all-fabric build reads it")
        key = _unscope(name)
        if key in cells:
            raise IdentityError(f"cells {name} and another read as {key}")
        cells[key] = c
    return cells


def _bit_names(nets: dict) -> tuple[dict, dict]:
    """(each bit's first source name, each other bit's first made name's template)."""
    fixed, made_name = {}, {}
    for n, v in nets.items():
        for i, b in enumerate(v["bits"]):
            if isinstance(b, int):
                if "$" not in n:
                    fixed.setdefault(b, f"{n}[{i}]")
                else:
                    made_name.setdefault(b, template(n))
    return fixed, made_name


def _memory_labels(memories: dict, cells: dict) -> dict:
    """Each memory's label: its source name, else a digest of it and its initialisers."""
    inits: dict[str, list] = {}
    for c in cells.values():
        if c["type"].startswith("$meminit"):
            inits.setdefault(_unscope(str(c["parameters"].get("MEMID", ""))), []).append(json.dumps(
                [c["type"], {k: v for k, v in _clean(c.get("parameters", {})).items() if k != "MEMID"},
                 c["connections"]], sort_keys=True))
    return {m: (m if "$" not in m else "mem:" + _h(_clean(v), sorted(inits.get(m, []))))
            for m, v in memories.items()}


def canonical(doc: dict) -> dict:
    """The canonical form of the datapath module in Yosys's JSON doc.

    A name the source gave (no ``$``) is kept, without the all-fabric scope.
    A name Yosys made is replaced by a label of the structure it names, found
    by refinement: every such cell starts from its type, its parameters, its
    attributes and its name's template, and each round adds the labels of
    the bits its inputs read; a bit with no name from the source takes the
    label of the cell output that drives it. Rounds run until one adds no new
    label. So no label depends on the order Yosys made things in, and two
    cells share one only when no round tells them apart."""
    top = doc["modules"][TOP]
    params = dict(top.get("parameter_default_values", {}))
    for p, want in SPLIT_PARAMS.items():
        if p in params and int(str(params.pop(p)), 2) != want:
            raise IdentityError(f"the switch's parameter {p} is not at its default {want}")
    cells = _fabric_cells(top)
    nets = {_unscope(n): v for n, v in top["netnames"].items() if not SPLIT_PORT.match(n)}
    fixed, made_name = _bit_names(nets)
    memories = {_unscope(n): v for n, v in top.get("memories", {}).items()}
    mem_label = _memory_labels(memories, cells)

    def params_of(c: dict) -> dict:
        """A cell's parameters, a memory it names by its label."""
        p = _clean(c.get("parameters", {}))
        if "MEMID" in p:
            m = _unscope(str(p["MEMID"]))
            p["MEMID"] = mem_label.get(m, m)
        return p

    ports_in, ports_out, drv = {}, {}, {}
    for n, c in cells.items():
        dirs = c.get("port_directions", {})
        ports_in[n] = [(p, c["connections"][p]) for p in sorted(c["connections"]) if dirs.get(p) != "output"]
        ports_out[n] = [(p, c["connections"][p]) for p in sorted(c["connections"]) if dirs.get(p) == "output"]
        for p, bits in ports_out[n]:
            for i, b in enumerate(bits):
                if isinstance(b, int):
                    drv[b] = (n, p, i)
    made = [n for n in cells if "$" in n]
    seed = {n: _h(c["type"], params_of(c), _clean(c.get("attributes", {})), template(n)) for n, c in cells.items()
            if "$" in n}
    cell_lab = {n: (seed[n] if n in seed else n) for n in cells}
    every = {b for bits in [*(v["bits"] for v in nets.values())] for b in bits if isinstance(b, int)}
    every |= {b for n in cells for _p, bits in ports_in[n] + ports_out[n] for b in bits if isinstance(b, int)}

    def bit_labels() -> dict:
        """Each bit's label: its source name, else the cell output that drives it."""
        out = {}
        for b in every:
            if b in fixed:
                out[b] = fixed[b]
            elif b in drv:
                n, p, i = drv[b]
                out[b] = f"{cell_lab[n]}.{p}[{i}]"
            else:
                out[b] = "undriven:" + made_name.get(b, "?")
        return out

    bit_lab = bit_labels()
    count = len(set(cell_lab.values()))
    for _ in range(ROUNDS):
        cell_lab = {n: (cell_lab[n] if n not in seed else _h(cell_lab[n], [
            (p, [bit_lab[b] if isinstance(b, int) else b for b in bits]) for p, bits in ports_in[n]]))
                    for n in cells}
        bit_lab = bit_labels()
        now = len(set(cell_lab.values()))
        if now == count:
            break
        count = now
    else:
        raise IdentityError(f"refinement did not settle in {ROUNDS} rounds")
    ref = lambda bits: [bit_lab[b] if isinstance(b, int) else b for b in bits]  # noqa: E731
    named, made_recs = {}, []
    for n, c in cells.items():
        rec = {"label": cell_lab[n], "type": c["type"], "parameters": params_of(c),
               "attributes": _clean(c.get("attributes", {})),
               "dirs": dict(sorted(c.get("port_directions", {}).items())),
               "conns": {p: ref(bits) for p, bits in sorted(c["connections"].items())}}
        if n in seed:
            made_recs.append(json.dumps(rec, sort_keys=True))
        else:
            named[n] = rec
    used = {c["type"] for c in cells.values() if not c["type"].startswith("$")}
    return {
        "parameters": dict(sorted(params.items())),
        "attributes": _clean(top.get("attributes", {})),
        "ports": {p: {"direction": v["direction"], "bits": ref(v["bits"])}
                  for p, v in sorted(top["ports"].items()) if not SPLIT_PORT.match(p)},
        "nets": {n: {"hide": v.get("hide_name", 0), "width": len(v["bits"]),
                     "attributes": _clean(v.get("attributes", {}))}
                 for n, v in sorted(nets.items()) if "$" not in n},
        "named_cells": dict(sorted(named.items())),
        "made_cells": sorted(made_recs),
        "memories": dict(sorted((mem_label[m], _clean(v)) for m, v in memories.items())),
        "blackboxes": {m: {p: v["direction"] for p, v in sorted(doc["modules"][m].get("ports", {}).items())}
                       for m in sorted(used) if m in doc["modules"]},
    }


def digest(form: dict) -> str:
    """The sha256 of a canonical form, its keys in order."""
    return hashlib.sha256(json.dumps(form, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _one(job: tuple[str, int, dict, str | None]) -> tuple[str, str, int, int]:
    """Elaborate one shape of the tree: (shape, digest, cells, nets); writes the form when keep is set."""
    tree, index, overlay, keep = job
    ce = _ce(Path(tree))
    shape = ce.shapes()[index]
    docs: list[dict] = []
    orig = ce.netlist
    ce.netlist = lambda doc: (docs.append(doc), orig(doc))[1]
    try:
        ce.elaborate(overlay, shape)
    finally:
        ce.netlist = orig
    form = canonical(docs[0])
    if keep:
        Path(keep, f"{shape.name}.json").write_text(json.dumps(form, sort_keys=True, indent=0) + "\n")
    return shape.name, digest(form), len(form["named_cells"]) + len(form["made_cells"]), len(form["nets"])


def dump(tree: Path, jobs: int, keep: Path | None, overlay: dict | None = None, only: int | None = None) -> dict:
    """Every shape's digest of the tree, after the pinned tools are confirmed."""
    ce = _ce(tree)
    toolchain = ce.toolchain()
    n = len(ce.shapes())
    picks = range(n) if only is None else [only]
    work = [(str(tree), i, overlay or {}, str(keep) if keep else None) for i in picks]
    if keep:
        keep.mkdir(parents=True, exist_ok=True)
    with multiprocessing.get_context("fork").Pool(max(1, min(jobs, len(work)))) as pool:
        rows = pool.map(_one, work)
    return {"tree_head": _head(tree), "toolchain": toolchain,
            "shapes": {s: {"digest": d, "cells": c, "nets": k} for s, d, c, k in rows}}


def _head(tree: Path) -> str:
    import subprocess
    out = subprocess.run(["git", "-C", str(tree), "rev-parse", "HEAD"], capture_output=True, text=True)
    return out.stdout.strip()


def compare(base: dict, head: dict) -> list[str]:
    """Each shape's verdict; a finding for a shape missing on either side or whose digests differ."""
    out = []
    for s in sorted(set(base["shapes"]) | set(head["shapes"])):
        b, h = base["shapes"].get(s), head["shapes"].get(s)
        if b is None or h is None:
            out.append(f"FINDING shape {s}: only the {'head' if b is None else 'base'} elaborates it")
        elif b["digest"] != h["digest"]:
            out.append(f"FINDING shape {s}: base {b['digest']} head {h['digest']} "
                       f"({b['cells']} and {h['cells']} cells)")
    return out


#: (name, the datapath's line, its planted replacement, the digest changes or the refusal's words)
PLANTS = (
    ("control: a comment changes", "  assign lwsrp_slope_en    = |pp_cd_srp_sr_admitted_w;",
     "  assign lwsrp_slope_en    = |pp_cd_srp_sr_admitted_w;  // planted comment", None),
    ("an operator of the all-fabric path", "  assign lwsrp_slope_en    = |pp_cd_srp_sr_admitted_w;",
     "  assign lwsrp_slope_en    = &pp_cd_srp_sr_admitted_w;", "digest"),
    ("a wrapper port connected to another net", "      .srp_over_limit_o        (pp_cd_srp_over_limit_w),",
     "      .srp_over_limit_o        (pp_cd_srp_domain_change_w),", "digest"),
    ("the all-fabric build reads a split port", "  assign lwsrp_over_limit  = pp_cd_srp_over_limit_w;",
     "  assign lwsrp_over_limit  = pp_cd_srp_over_limit_w | i_ctl_pub_dom_adopted;",
     "reads the split port i_ctl_pub_dom_adopted"),
    ("a split output driven from a net", "  assign o_ctl_link_up       = 1'b0;",
     "  assign o_ctl_link_up       = eff_link_w;", "come from a net, not a constant"),
    ("the switch's default flipped", "  parameter int CTRL_SPLIT_P = 0,", "  parameter int CTRL_SPLIT_P = 2,",
     "not at its default 0"),
)


def selftest(jobs: int) -> int:
    """Each plant changes the recipe shape's digest or is refused by its words; the control changes nothing."""
    ce = _ce(HERE.parent.parent)
    dp = ce.REPO / "hdl/milan/milan_datapath.sv"
    text = dp.read_text()
    clean = dump(ce.REPO, 1, None, only=0)["shapes"]["recipe"]["digest"]
    print(f"clean recipe digest {clean}")
    bad = 0
    for label, old, new, want in PLANTS:
        if text.count(old) != 1:
            print(f"FAIL {label}: its anchor is not in the datapath once")
            bad += 1
            continue
        try:
            got = dump(ce.REPO, 1, None, {dp: text.replace(old, new)}, only=0)["shapes"]["recipe"]["digest"]
            words = ""
        except Exception as exc:  # noqa: BLE001 - a worker's refusal arrives re-raised
            got, words = None, str(exc)
        if want is None:
            ok = got == clean
        elif want == "digest":
            ok = got is not None and got != clean
        else:
            ok = got is None and want in words
        print(f"{'ok  ' if ok else 'FAIL'} {label}: {'digest ' + got if got else 'refused: ' + words}")
        bad += not ok
    print(f"placement identity self-test: {len(PLANTS) - bad} of {len(PLANTS)} arms as required")
    return 1 if bad else 0


def main() -> int:
    """Dump a tree's digests, compare two dumps, or run the self-test; the exit status is the verdict."""
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("--dump", type=Path, help="write every shape's digest of the tree to this file")
    ap.add_argument("--tree", type=Path, default=HERE.parent.parent, help="the checkout to elaborate")
    ap.add_argument("--keep", type=Path, help="also write each canonical form into this directory")
    ap.add_argument("--compare", nargs=2, type=Path, metavar=("BASE", "HEAD"))
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--jobs", type=int, default=1)
    args = ap.parse_args()
    if args.selftest:
        return selftest(args.jobs)
    if args.compare:
        base, head = (json.loads(p.read_text()) for p in args.compare)
        findings = compare(base, head)
        for s in sorted(head["shapes"]):
            print(f"shape {s}: base {base['shapes'].get(s, {}).get('digest')} head {head['shapes'][s]['digest']}")
        print("\n".join(findings) or f"placement identity: {len(head['shapes'])} shape(s), every digest equal")
        return 1 if findings else 0
    if args.dump:
        out = dump(args.tree.resolve(), args.jobs, args.keep)
        args.dump.write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
        for s, v in out["shapes"].items():
            print(f"shape {s}: {v['digest']} ({v['cells']} cells, {v['nets']} nets)")
        return 0
    ap.error("give --dump, --compare or --selftest")
    return 2


if __name__ == "__main__":
    sys.exit(main())

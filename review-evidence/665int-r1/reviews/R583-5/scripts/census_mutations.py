#!/usr/bin/env python3
"""Reviewer probe (R583-5): which of the publication census's stated rules
does its own self-test kill when the rule is removed?

usage: census_mutations.py REPO [JOBS]

Each worker elaborates one self-test arm (the two controls, every
census_plants.PLANTS copy, the two table plants) once through the census's
own census_elab.elaborate, then re-runs the self-test's verdict logic
(publication_census.arm) on that netlist under the unmutated census and
under each mutation below, one census rule removed in memory.
A mutation is KILLED when any arm or control changes from ok to BAD. The
census's files are never edited.
"""
import multiprocessing
import sys
from concurrent.futures import ProcessPoolExecutor
from dataclasses import replace
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
jobs = int(sys.argv[2]) if len(sys.argv) > 2 else 4
sys.path.insert(0, str(repo / "sw/mailbox"))
import census_elab as ce  # noqa: E402
import publication_census as pc  # noqa: E402
from census_plants import PLANTS, apply  # noqa: E402

ORIG_ELAB = pc.elaborate


# ---- the mutations: each removes one stated rule, in memory ----------------------------------------
O = {n: getattr(pc, n) for n in ("terminal", "step", "flow", "findings", "multiple", "population", "cone",
                                  "edge_of", "first_hop")}


def m_terminal_by_port_name(net, end):
    if end[0] == "out":
        return "wire", f"the datapath output {end[1]}"
    cell, port = end[1], end[2]
    if port in pc.CSR_READBACK:
        return "csr", port
    if port in pc.PROCESSOR_FACE:
        return "processor", port
    return O["terminal"](net, end)


def m_terminal_any_wrapper_input(net, end):
    if end[0] != "out" and end[1] == pc.WRAPPER_CELL:
        return "processor", end[2]
    return O["terminal"](net, end)


def m_terminal_outputs_not_wire(net, end):
    if end[0] == "out":
        return "csr", end[1]
    return O["terminal"](net, end)


def _step_nomem(fl, bit):
    out = []
    for e in fl.fanout.get(bit, ()):
        if e[0] == "cell":
            out += [("bit", o) for o in fl.outs[e[1]]]
        elif e[0] == "mem":
            continue
        else:
            out.append(e)
    return out


def m_edge_no_output_cell_silent(name, c, dirs):
    e = O["edge_of"](name, c, dirs)
    if e is None and c.kind.startswith("$"):
        return "cell", name          # a cell with no output: the path ends with no end recorded
    return e


def m_flow_select_and_clock_dropped(net):
    fl = O["flow"](net)
    # drop the bits entering any cell's S (mux select) or CLK port
    drop = {b for c in net.cells.values() if c.kind.startswith("$") for p in ("S", "CLK")
            for b in c.conns.get(p, ()) if isinstance(b, int)}
    for b in drop:
        fl.fanout[b] = [e for e in fl.fanout[b] if e[0] != "cell"]
    return fl


def m_findings_no_status_processor(src, table, known):
    out, sv = O["findings"](src, table, known)
    return [f for f in out if "counted as status, but it reaches the processor wrapper" not in f], sv


def m_findings_no_field_without_wire(src, table, known):
    out, sv = O["findings"](src, table, known)
    return [f for f in out if "as read on the wire, but it reaches no wire" not in f], sv


def m_multiple_off(fl, skip):
    return []


def m_population_no_second_driver(fl, wrapper):
    pop, out = O["population"](fl, wrapper)
    return pop, [f for f in out if "a second driver" not in f]


def m_cone_first_end_only(fl, start):
    ends = O["cone"](fl, start)
    return frozenset(e for e in ends if e[0] != "wire" or not e[1].startswith("the datapath output"))


MUTATIONS = {
    "terminal by port name, not by cell": ("terminal", m_terminal_by_port_name),
    "any wrapper input is the answer face": ("terminal", m_terminal_any_wrapper_input),
    "a datapath output is not the wire": ("terminal", m_terminal_outputs_not_wire),
    "a memory's write does not lead to its reads": ("step", _step_nomem),
    "a cell with no output ends the path silently": ("edge_of", m_edge_no_output_cell_silent),
    "a mux select and a flop clock lead nowhere": ("flow", m_flow_select_and_clock_dropped),
    "a status read reaching the wrapper is not refused": ("findings", m_findings_no_status_processor),
    "a field read reaching no wire is not refused": ("findings", m_findings_no_field_without_wire),
    "no check for a bit with two drivers": ("multiple", m_multiple_off),
    "no check for a second driver of a population net": ("population", m_population_no_second_driver),
    "the cone drops datapath outputs": ("cone", m_cone_first_end_only),
}

def arms(src):
    """(label, Sources-or-reason, table, words) of every self-test arm, as publication_census.selftest builds them,
    the two controls first (words None: the arm is ok when there is no finding)."""
    note = replace(src, datapath=src.datapath.replace(
        "  wire crft_class_a_w =", "  // pp_cd_srp_over_limit_w is not read here\n  wire crft_class_a_w =", 1))
    out = [("positive control", src, pc.CENSUS, None), ("negative control", note, pc.CENSUS, None)]
    out += [(p.what, apply(src, p), pc.CENSUS, p.word) for p in PLANTS]
    k = ("pp_cd_srp_tk_decl_state_w", "crft_class_a_w")
    out.append(("a field the contract lacks", src, {**pc.CENSUS, k: pc.Row("field", "TALKER_DECL.DECLARE", "")},
                "which the publication block does not define"))
    out.append(("a stale row", src, {**pc.CENSUS, ("pp_cd_srp_granted_slope_bps_w", "lwsrp_idle_slope"):
                                     pc.Row("status", "", "planted")},
                "stale row: the datapath no longer reads pp_cd_srp_granted_slope_bps_w"))
    return out


def verdict(what, planted, table, word, known):
    if word is None:
        try:
            got, _ = pc.findings(planted, table, known)
        except ce.CensusError:
            return False
        return not got
    return pc.arm((what, planted, table, word, known))[0]


def worker(job):
    """Elaborate one arm once; its verdict under the unmutated census and under each mutation."""
    what, planted, table, word, known = job
    if isinstance(planted, str):
        return what, {m: False for m in ("", *MUTATIONS)}
    try:
        net = ORIG_ELAB(pc.overlay(planted))
    except ce.CensusError as exc:
        net = ce.CensusError(str(exc))

    def cached(_ov):
        if isinstance(net, ce.CensusError):
            raise net
        return net
    pc.elaborate = cached
    res = {"": verdict(what, planted, table, word, known)}
    for name, (fn, impl) in MUTATIONS.items():
        setattr(pc, fn, impl)
        try:
            res[name] = verdict(what, planted, table, word, known)
        finally:
            setattr(pc, fn, O[fn])
    return what, res


if __name__ == "__main__":
    src = pc.load(pc.DATAPATH, pc.WRAPPER_SV)
    known = pc.fields(pc.mailbox_model.load())
    ce.recipe(); ce.tracked_openers()
    jobs_ = [(w, p, t, wd, known) for w, p, t, wd in arms(src)]
    with ProcessPoolExecutor(max_workers=jobs, mp_context=multiprocessing.get_context("fork")) as pool:
        rows = list(pool.map(worker, jobs_))
    base = {w: r[""] for w, r in rows}
    bad = [w for w, v in base.items() if not v]
    print(f"unmutated census: {len(base)} arm(s) incl. 2 controls, {len(bad)} BAD {bad}")
    survived = 0
    for name in MUTATIONS:
        flipped = [w for w, r in rows if base[w] and not r[name]]
        print(f"[{'KILLED' if flipped else 'SURVIVED'}] {name}: "
              f"{len(flipped)} arm(s) turn BAD{(' - ' + '; '.join(flipped[:4])) if flipped else ''}")
        survived += not flipped
    print(f"census_mutations: {survived} of {len(MUTATIONS)} mutation(s) survived the self-test's arms")

#!/usr/bin/env python3
"""R363-3: classify the survivors of probe_mutants.py at a checkout.

Usage: witness_r3.py <repo> <scratch-dir>
Builds each surviving mutant as a module copy under <scratch-dir> and compares
its verdict and evidence metadata with the head on a witness input, or on a grid
where equivalence is claimed. Prints one line per survivor.
"""
from __future__ import annotations

import importlib.util
import itertools
import sys
from pathlib import Path

sys.dont_write_bytecode = True
repo, scratch = Path(sys.argv[1]), Path(sys.argv[2])
src = (repo / "tb/tools/torture_campaign.py").read_text(encoding="utf-8")


def load(text: str, name: str):
    path = scratch / f"{name}.py"
    path.write_text(text, encoding="utf-8")
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def mutate(old: str, new: str, name: str):
    assert src.count(old) == 1, (name, src.count(old))
    return load(src.replace(old, new), name)


head = load(src, "w_head")
M = {
    "L3645 history zero-length guard <= -> <": mutate(
        "if clear_s <= start_s or (intervals and start_s <= intervals[-1][1]):",
        "if clear_s < start_s or (intervals and start_s <= intervals[-1][1]):", "w_l3645"),
    "L3686 PDU timestamp order < -> <=": mutate(
        'or current["timestamp_s"] < previous["timestamp_s"]):',
        'or current["timestamp_s"] <= previous["timestamp_s"]):', "w_l3686"),
    "L3793 capture window start >= end -> >": mutate(
        "if (capture_start_s >= capture_end_s or capture_start_s > required_start_s",
        "if (capture_start_s > capture_end_s or capture_start_s > required_start_s", "w_l3793"),
    "T18 pdu index floor -1": mutate(' or pdu["pdu_index"] < 0\n', ' or pdu["pdu_index"] < -1\n', "w_t18"),
    "T22 uncorrelated FAIL omits metadata": mutate(
        'return "FAIL", {"why": "uncorrelated tu fails", **detail}',
        'return "FAIL", {"why": "uncorrelated tu fails"}', "w_t22"),
    "T23 mr capture-window NOT RUN omits metadata": mutate(
        '        return "NOT RUN", dict(detail, why="recorded capture window required")',
        '        return "NOT RUN", {"why": "recorded capture window required"}', "w_t23"),
    "T24 mr invalid-record NOT RUN omits metadata": mutate(
        '        return "NOT RUN", dict(detail, why="invalid recorded evidence")',
        '        return "NOT RUN", {"why": "invalid recorded evidence"}', "w_t24"),
}


def trace(n=20, shift=0, ts=None):
    out = [{"stream_id": "s", "timestamp_s": i / 100, "pdu_index": i + shift, "mr": int(i >= 1)}
           for i in range(n)]
    if ts:
        for i, t in ts.items():
            out[i] = dict(out[i], timestamp_s=t)
    return out


def mr_args(**over):
    base = dict(stream_id="s", pdus=trace(),
                causes=[{"stream_id": "s", "timestamp_s": 0.01, "kind": "CRF disruption"}],
                media_reset_reads=[{"stream_id": "s", "timestamp_s": 0, "value": 0},
                                   {"stream_id": "s", "timestamp_s": 0.19, "value": 1}],
                observation_resolution_s=0.001, capture_complete=head.ReleaseCapture((-2, 2)))
    base.update(over)
    return base


def meta(detail: dict) -> tuple:
    return ("resolution_limit_s" in detail, "observation_resolution_s" in detail)


def for_module(mod, kwargs):
    # Each module copy defines its own ReleaseCapture class; rebuild per module.
    cap = kwargs.get("capture_complete")
    if isinstance(cap, head.ReleaseCapture):
        kwargs = dict(kwargs, capture_complete=mod.ReleaseCapture(cap.window_s, cap.complete))
    return kwargs


def show(label, fn_name, kwargs, key=lambda r: r[0]):
    h = getattr(head, fn_name)(**for_module(head, kwargs))
    m = getattr(M[label], fn_name)(**for_module(M[label], kwargs))
    print(f"{label}: head={key(h)} mutant={key(m)} -> {'DIFFERS' if key(h) != key(m) else 'same'}")


# L3645: claimed verdict-equivalent; grid over zero-length and ordinary intervals.
diff = n = 0
for a, b, r in itertools.product((0, 0.1, 0.3), (0, 0.1, 0.3, 0.6), (0, 0.001, 0.1)):
    for gm in ([], [0], [0.1]):
        kw = dict(intervals_s=[(a, b)], discontinuities_s=[0], gm_changes_s=gm,
                  observation_resolution_s=r, capture_complete=True)
        n += 1
        diff += head.check_release_tu_history(**kw)[0] != M["L3645 history zero-length guard <= -> <"].check_release_tu_history(**kw)[0]
print(f"L3645 history zero-length guard <= -> <: verdict differences {diff}/{n} (equivalent if 0)")

# L3686: equal consecutive timestamps on non-toggle PDUs.
show("L3686 PDU timestamp order < -> <=", "check_release_mr", mr_args(pdus=trace(ts={6: 0.05})))

# L3793: zero-length capture window with unordered reads (only way to satisfy the other span terms).
kw = mr_args(pdus=[], capture_complete=head.ReleaseCapture((0.0, 0.0)),
             media_reset_reads=[{"stream_id": "s", "timestamp_s": 5, "value": 0},
                                {"stream_id": "s", "timestamp_s": 0, "value": 0}])
show("L3793 capture window start >= end -> >", "check_release_mr", kw)
kw["pdus"] = [{"stream_id": "s", "timestamp_s": 0.0, "pdu_index": i, "mr": int(i == 1)} for i in range(3)]
show("L3793 capture window start >= end -> >", "check_release_mr", kw)

# T18: a trace whose indices start at exactly -1.
show("T18 pdu index floor -1", "check_release_mr", mr_args(pdus=trace(shift=-1)))

# T22-T24: verdict unchanged, metadata lost.
show("T22 uncorrelated FAIL omits metadata", "check_release_tu",
     dict(interval_s=(1, 1.1), discontinuities_s=[], gm_changes_s=[], holdover_bound_s=0.5,
          observation_resolution_s=0.001, capture_complete=True), key=lambda r: (r[0], meta(r[1])))
show("T23 mr capture-window NOT RUN omits metadata", "check_release_mr",
     mr_args(pdus=[], capture_complete=True), key=lambda r: (r[0], meta(r[1])))
show("T24 mr invalid-record NOT RUN omits metadata", "check_release_mr",
     mr_args(pdus=[dict(trace()[0], mr=2)] + trace()[1:]), key=lambda r: (r[0], meta(r[1])))

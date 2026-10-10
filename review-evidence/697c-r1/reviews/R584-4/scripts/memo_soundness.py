#!/usr/bin/env python3
"""Judge every boundary control in full (no early stop), with or without the run's preprocessing reuse.

Usage: python3 -I memo_soundness.py <checkout-root> <memo|nomemo> <jobs> <out.json>

Each control's complete finding list is recorded, so a run with reuse and one without compare finding by
finding. Only ctrl_boundary.controls is driven (no stack gate, no pin controls).
"""
import json
import sys
import tempfile
from pathlib import Path

root = Path(sys.argv[1]).resolve()
mode, jobs, out = sys.argv[2], int(sys.argv[3]), Path(sys.argv[4])
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
import ctrl_boundary as cb  # noqa: E402
import fw_rv32  # noqa: E402


class NeverStop:
    def set(self):
        pass

    def is_set(self):
        return False


orig_init = cb.Judgement.__init__


def init(self, memo, listing):
    orig_init(self, memo, listing)
    self.stop = NeverStop()


cb.Judgement.__init__ = init
if mode == "nomemo":
    cb.Judgement.lookup = lambda self, argv, unit: None
cb.JOBS = jobs
results = {}
orig_judge = cb.judge


def judge(trees, rv32, work, universe=None, computed=None, control=None):
    try:
        found = orig_judge(trees, rv32, work, universe, computed, control)
    except cb.Refusal as exc:
        results[control.name] = [f"REFUSED: {exc}"]
        raise
    results[control.name] = sorted(found)
    return found


cb.judge = judge
rv32 = fw_rv32.compiler()
with tempfile.TemporaryDirectory(prefix="ctrl-boundary-") as tmp:
    bad = cb.controls(rv32, Path(tmp) / "controls")
print(f"{mode}: {bad} misbehaved; {cb.MEMO.total('ran')} run, {cb.MEMO.total('reused')} reused")
out.write_text(json.dumps({"bad": bad, "ran": cb.MEMO.total("ran"), "reused": cb.MEMO.total("reused"),
                           "results": results}, indent=1, sort_keys=True), encoding="utf-8")

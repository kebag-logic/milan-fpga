# R608-4 reviewer probes for the round-4 echo_entries rule (disposable).
# Usage: python3 -I probe_echo.py TREE LABEL
# TREE is an exported source tree (git archive) of the processor repository.
# Each probe mutates a fresh copy (file probes) or an in-memory copy (ROM and
# record probes) and prints the gate's findings that carry the probe's words.
import copy
import json
import shutil
import sys
import tempfile
from pathlib import Path

TREE = Path(sys.argv[1]).resolve()
LABEL = sys.argv[2]
sys.path.insert(0, str(TREE / "scripts"))

from aecp_gate.gate import check  # noqa: E402
from aecp_gate.inputs import TABLE, UCODE, GateError, Inputs, load, ucode_of  # noqa: E402
from aecp_gate.rom import reachable  # noqa: E402
from aecp_gate.record import split_group  # noqa: E402

EAVL_OLD = ("    u('BUILD_FLD', ra=3, fmt=FMT_D),             # flags                  @24\n"
            "    u('BUILD_FLD', ra=2, fmt=FMT_Q),             # acquired_controller_id @28\n"
            "    u('BUILD_FLD', ra=1, fmt=FMT_Q),             # locked_controller_id   @36\n")


def table_edit(d, fn):
    t = json.loads((d / TABLE).read_text(encoding="utf-8"))
    fn(t)
    (d / TABLE).write_text(json.dumps(t, indent=2) + "\n", encoding="utf-8")


def nop_eavl(d):
    p = d / UCODE
    s = p.read_text(encoding="utf-8")
    assert s.count(EAVL_OLD) == 1
    p.write_text(s.replace(EAVL_OLD, "    u('NOP'),\n" * 3), encoding="utf-8")


def file_probe(fn):
    with tempfile.TemporaryDirectory(prefix="r608-4-probe-") as tmp:
        d = Path(tmp) / "t"
        shutil.copytree(TREE, d, ignore=shutil.ignore_patterns("obj_dir", ".git"))
        fn(d)
        try:
            return check(load(d))
        except GateError as exc:
            return [f"  (gate refused: {exc})"]


def mem_probe(base, fn):
    inp = Inputs(copy.deepcopy(base.table), dict(base.texts), copy.deepcopy(base.ucode),
                 copy.deepcopy(base.record), base.root, dict(base.swept),
                 copy.deepcopy(base.registry))
    try:
        fn(inp)
        return check(inp)
    except GateError as exc:
        return [f"  (gate refused: {exc})"]


def status_success(entry):
    """Rewrite every SET_STATUS a path from E_entry executes to SUCCESS (0)."""
    def fn(inp):
        uc = ucode_of(inp)
        code = uc.ops["SET_STATUS"]
        hit = 0
        for pc in reachable(uc, uc.entry[entry]):
            if uc.rom[pc] >> 43 == code:
                uc.rom[pc] = uc.rom[pc] & ~0xFFFFFF
                hit += 1
        assert hit, entry
    return fn


def record_success(op, prog):
    """In the decode record, AEM op's `prog` answers SUCCESS at the echo length."""
    def fn(inp):
        progs = split_group(inp.record, "AEM", op)
        assert prog in progs, (hex(op), prog, list(progs))
        progs[prog]["answers"] = {"0": "echo"}
    return fn


def report(name, got):
    print(f"== {LABEL} :: {name} :: {len(got)} finding(s)")
    for g in got[:8]:
        print(g)


def main():
    base = load(TREE)
    report("unmutated", check(base))
    report("F1 echo-hide with EAVL also in shared_entries (file)", file_probe(lambda d: (
        nop_eavl(d),
        table_edit(d, lambda t: (t["echo_entries"].append("EAVL"),
                                 t["shared_entries"].__setitem__("EAVL", "probe"))))))
    report("F2 echo-hide exactly as the self-test (file)", file_probe(lambda d: (
        nop_eavl(d), table_edit(d, lambda t: t["echo_entries"].append("EAVL")))))
    report("F3 owned single-use first entry GCLKS in echo_entries (file)", file_probe(
        lambda d: table_edit(d, lambda t: t["echo_entries"].append("GCLKS"))))
    report("F4 unowned shared TIZ4NS in echo_entries (file; ruling branch 1 allows)", file_probe(
        lambda d: table_edit(d, lambda t: t["echo_entries"].append("TIZ4NS"))))
    report("F5 private RDESCENT in echo_entries (file)", file_probe(
        lambda d: table_edit(d, lambda t: t["echo_entries"].append("RDESCENT"))))
    report("F6 echo_entries removed (file)", file_probe(
        lambda d: table_edit(d, lambda t: t.pop("echo_entries"))))
    report("F7 echo_entries a string (file)", file_probe(
        lambda d: table_edit(d, lambda t: t.__setitem__("echo_entries", "NOTIMPL"))))
    report("F8 NSUPPE dropped from shared_entries (file)", file_probe(
        lambda d: table_edit(d, lambda t: t["shared_entries"].pop("NSUPPE", None))))
    for m in ("NOTIMPL", "BADARG", "NSUPPE"):
        report(f"M0 {m} removed from echo_entries (load-bearing?)", mem_probe(
            base, lambda i, m=m: i.table["echo_entries"].remove(m)))
    report("M1 ROM: E_BADARG answers SUCCESS (shared echo, non-echo commands)",
           mem_probe(base, status_success("BADARG")))
    report("M2 ROM: E_NSUPPE answers SUCCESS", mem_probe(base, status_success("NSUPPE")))
    report("M3 ROM: E_NOTIMPL answers SUCCESS", mem_probe(base, status_success("NOTIMPL")))
    report("M4 record: GET_STREAM_INFO's BADARG answers SUCCESS at the echo length",
           mem_probe(base, record_success(0x000F, "BADARG")))
    report("M5 record: GET_AUDIO_MAP's NOTIMPL answers SUCCESS at the echo length",
           mem_probe(base, record_success(0x002B, "NOTIMPL")))


main()

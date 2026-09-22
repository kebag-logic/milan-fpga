"""P8: Robustness at HEAD, through HEAD's real checker on in-memory worlds.

Live-body cases edit docs.yml/elaborate.yml steps in a deep copy of the
pristine parsed world and run the complete check(); record cases pass a
modified copy of the recorded list as `spec` to check_carrier_steps. The
last group feeds the self-test generator a malformed pristine tree to see
whether it fails closed.
"""
from __future__ import annotations

import copy
import json
import sys
import traceback

from common import HEAD, load_module, world_at

m = load_module(HEAD, "head_p8")
W0 = world_at(m, HEAD)
D, E = m.DOCS, m.ELABORATE


def steps(w, path, jid):
    return w[path]["jobs"][jid]["steps"]


def at_name(w, path, jid, name):
    return next(i for i, s in enumerate(steps(w, path, jid)) if s.get("name") == name)


def body_case(label, path, jid, name, fn, expect):
    w = copy.deepcopy(W0)
    i = at_name(w, path, jid, name)
    fn(steps(w, path, jid)[i])
    f = m.check(w).findings
    hit = [x for x in f if expect in x]
    return {"case": label, "expect": expect, "refused": bool(f),
            "matched": bool(hit), "findings": [x[:260] for x in f[:3]],
            "ok": (bool(hit) if expect else not f)}


def record_case(label, path, jid, name, new_value, expect):
    spec = copy.deepcopy(m.CARRIER_STEP_LISTS[(path, jid)])
    i = next(n for n, e in enumerate(spec) if e.get("name") == name)
    if new_value is KeyError:
        spec[i].pop("run", None)
    else:
        spec[i]["run"] = new_value
    c = m.Contract()
    m.check_carrier_steps(c, path, W0[path], jid, spec)
    hit = [x for x in c.findings if expect in x]
    return {"case": label, "expect": expect, "findings": [x[:260] for x in c.findings[:3]],
            "ok": bool(hit)}


IDIOM = "Python idiom gate"
SOC = "SoC source-list gate (Vivado would fail 40 min in without this)"
W_IDIOM = "job `docs-check` step 34 (`Python idiom gate`) script is not the canonical form"
W_SOC = "job `docs-check` step 24 (`SoC source-list gate (Vivado would fail 40 min in without this)`) script is not the canonical form"


def setrun(v):
    return lambda s: s.__setitem__("run", v)


def main() -> int:
    idiom = W0[D]["jobs"]["docs-check"]["steps"][33]["run"]
    soc = W0[D]["jobs"]["docs-check"]["steps"][23]["run"]
    soc_lines = soc.splitlines()
    res = [
        body_case("NBSP inside a word gap", D, "docs-check", IDIOM,
                  setrun(idiom.replace("python3 scripts", "python3 scripts", 1)),
                  W_IDIOM + ": line 1 must be 'python3 scripts/check_py_idiom.py' (found '<<refused>> line 1 column 8 carries U+00A0"),
        body_case("CRLF line endings", D, "docs-check", IDIOM,
                  setrun(idiom.replace("\n", "\r\n")), W_IDIOM + ": line 1 must be"),
        body_case("U+2028 line separator", D, "docs-check", IDIOM,
                  setrun(idiom.replace("\n", " ", 1)), W_IDIOM + ": line 1 must be"),
        body_case("empty body", D, "docs-check", IDIOM, setrun(""),
                  W_IDIOM + ": line 1 must be 'python3 scripts/check_py_idiom.py' (found None)"),
        body_case("whitespace-only body", D, "docs-check", IDIOM, setrun(" \n\t\n"),
                  W_IDIOM + ": line 1 must be 'python3 scripts/check_py_idiom.py' (found None)"),
        body_case("comment line appended", D, "docs-check", IDIOM, setrun(idiom + "# note\n"),
                  W_IDIOM + ": line 3 must be None (found '# note')"),
        body_case("set +e prepended", D, "docs-check", IDIOM, setrun("set +e\n" + idiom),
                  W_IDIOM + ": line 1 must be 'python3 scripts/check_py_idiom.py' (found 'set +e')"),
        body_case("line duplicated", D, "docs-check", IDIOM,
                  setrun(idiom.splitlines()[0] + "\n" + idiom), W_IDIOM + ": line 2 must be"),
        body_case("swallowed middle command (SoC line 4)", D, "docs-check", SOC,
                  setrun("\n".join(l + (" || true" if n == 3 else "") for n, l in enumerate(soc_lines)) + "\n"),
                  W_SOC + ": line 4 must be"),
        body_case("command moved into the tclsh block", D, "docs-check", SOC,
                  setrun("\n".join([soc_lines[0], soc_lines[2], soc_lines[1]] + soc_lines[3:]) + "\n"),
                  W_SOC + ": line 2 must be"),
        body_case("non-string run (list)", D, "docs-check", IDIOM,
                  setrun(["python3 scripts/check_py_idiom.py"]),
                  "job `docs-check` step 34 must be the step named `Python idiom gate`"),
        body_case("run key removed", D, "docs-check", IDIOM, lambda s: s.pop("run"),
                  "job `docs-check` step 34 must be the step named `Python idiom gate`"),
        body_case("tabs and continuation (same script)", D, "docs-check", IDIOM,
                  setrun("python3\tscripts/check_py_idiom.py\n\npython3 \\\n   scripts/check_py_idiom.py  --selftest\n"),
                  None),
        body_case("elaborate: patch series swallowed", E, "elaborate", "Apply the toolchain patch series",
                  setrun("sw/litex/patches/apply.sh || true"),
                  "job `elaborate` step 12 (`Apply the toolchain patch series`) script is not the canonical form: line 1"),
        record_case("record: list not tuple", D, "docs-check", IDIOM,
                    ["python3 scripts/check_py_idiom.py", "python3 scripts/check_py_idiom.py --selftest"],
                    "must record a canonical normalized `run` script"),
        record_case("record: empty tuple", D, "docs-check", IDIOM, (), "must record a canonical normalized `run` script"),
        record_case("record: non-string element", D, "docs-check", IDIOM,
                    ("python3 scripts/check_py_idiom.py", None), "must record a canonical normalized `run` script"),
        record_case("record: raw string", D, "docs-check", IDIOM,
                    "python3 scripts/check_py_idiom.py", "must record a canonical normalized `run` script"),
        record_case("record: missing", D, "docs-check", IDIOM, KeyError,
                    "must record a canonical normalized `run` script"),
        record_case("record: not normalized (double space)", D, "docs-check", IDIOM,
                    ("python3  scripts/check_py_idiom.py", "python3 scripts/check_py_idiom.py --selftest"),
                    "script is not the canonical form: line 1 must be 'python3  scripts/check_py_idiom.py'"),
        record_case("record: elaborate missing", E, "elaborate", "Elaboration gates", KeyError,
                    "must record a canonical normalized `run` script"),
    ]
    # Self-test generator on a malformed pristine tree: must not report PASS.
    gen = []
    for label, fn in (("whitespace-only live body", lambda s: s.__setitem__("run", " \n")),
                      ("live run step without name", lambda s: s.pop("name"))):
        w = copy.deepcopy(W0)
        fn(steps(w, D, "docs-check")[33])
        try:
            arms = m._mutations(w)
            gen.append({"case": label, "outcome": f"built {len(arms)} arms"})
        except Exception as exc:  # noqa: BLE001
            gen.append({"case": label, "outcome": f"raised {type(exc).__name__}: {exc}",
                        "check_findings": [x[:200] for x in m.check(w).findings[:2]]})
    ok = all(r["ok"] for r in res)
    json.dump({"cases": res, "generator": gen, "all_ok": ok}, open(sys.argv[1], "w"), indent=1)
    for r in res:
        print(f"{'ok  ' if r['ok'] else 'FAIL'} {r['case']}: {r['findings'][:1]}")
    for g in gen:
        print("gen:", g)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

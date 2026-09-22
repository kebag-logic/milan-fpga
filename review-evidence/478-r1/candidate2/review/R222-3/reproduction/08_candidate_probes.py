#!/usr/bin/env python3
"""R222-3 focused controls for issue #478 on the COMBINED tree.

Runs inside scratch clones only (never the review checkout):
  CAND = <scratch>/cand  (72e16c61: PR source 1496558d merged with dev 52711029)
  DEV  = <scratch>/dev   (52711029: live dev, carries #513, lacks the issue patch)
  SRC  = <scratch>/src   (1496558d: PR source, lacks #513)

Sections
  A  pristine candidate: the three gate 36a functions and gate 32
  B  candidate gate 36a against the DEV builder (the defect the gate claims)
  C  candidate builder mutants, image path = the candidate's avdecc (#513)
  E  real shipping-YAML mutants through the candidate image path
  F  loader versus packed image, candidate builder and dev builder
  G  #513 dependency path: file-open traces of each gate 36a arm and of the
     AEM store self-test (fresh interpreters, empty bytecode cache), then
     on-disk avdecc mutants/reverts in fresh interpreters
  H  CI carrier on the combined tree: docs-check step order, and
     ci_events --check pristine and with gate 36a's carrier or the #513 step
     removed

Each graded row prints expectation, outcome and MATCH/MISMATCH. Exit status is
non-zero if any graded row mismatches or any scratch restore fails.
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
SCRATCH = Path(sys.argv[1])
CAND = SCRATCH / "cand"
DEV = SCRATCH / "dev"
SRC = SCRATCH / "src"
PY = sys.executable
PY312 = os.environ.get("R222_PY312", "")
ISSUE_PATHS = {"docs/ENDSTATION_BUILDER.md", "sw/builder/endstation_builder.py",
               "sw/builder/test_builder.py"}
PR513_PATHS = {".github/workflows/docs.yml", "avdecc/aem_maps.py",
               "avdecc/gen_aem_store.py", "docs/testing/CI_WORKFLOWS.md",
               "docs/testing/RUNNING_TESTS.md", "scripts/ci_events.py"}

sys.path.insert(0, str(CAND / "sw/builder"))
import test_builder as tb  # noqa: E402

CAND_EB = tb.eb
mismatches = 0


def rev(root: Path, spec: str = "HEAD") -> str:
    return subprocess.run(["git", "-C", str(root), "rev-parse", spec],
                          check=True, capture_output=True, text=True).stdout.strip()


def load_builder(source: str, file_path: Path, name: str):
    """Execute builder source as a fresh module whose __file__ is file_path."""
    spec = importlib.util.spec_from_loader(name, loader=None, origin=str(file_path))
    mod = importlib.util.module_from_spec(spec)
    mod.__file__ = str(file_path)
    sys.modules[name] = mod
    exec(compile(source, str(file_path), "exec"), mod.__dict__)
    return mod


def run(fn, eb=None) -> tuple[str, str]:
    saved = tb.eb
    if eb is not None:
        tb.eb = eb
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            fn()
        return "PASS", ""
    except BaseException as exc:  # noqa: BLE001 - a probe records every failure kind
        first = str(exc).splitlines()[0] if str(exc) else ""
        return "FAIL", f"{type(exc).__name__}: {first}"[:170]
    finally:
        tb.eb = saved


def grade(row: str, expect: str, got: tuple[str, str]) -> None:
    global mismatches
    ok = got[0] == expect
    if not ok:
        mismatches += 1
    print(f"{row:<62} expect {expect:<4} got {got[0]:<4} "
          f"{'MATCH' if ok else 'MISMATCH':<8} {got[1]}")


def blob_on_disk(path: Path) -> str:
    return subprocess.run(["git", "hash-object", "--no-filters", str(path)],
                          check=True, capture_output=True, text=True).stdout.strip()


@contextlib.contextmanager
def replaced(root: Path, rel: str, new_bytes: bytes):
    """Write new bytes into a scratch file; restore and blob-verify after."""
    global mismatches
    path = root / rel
    original = path.read_bytes()
    path.write_bytes(new_bytes)
    try:
        yield
    finally:
        path.write_bytes(original)
        if blob_on_disk(path) != rev(root, f"HEAD:{rel}"):
            mismatches += 1
            print(f"RESTORE FAILED for {rel}")


def text_mutant(root: Path, rel: str, old: str, new: str) -> bytes:
    text = (root / rel).read_text()
    assert text.count(old) == 1, f"{rel}: pattern count {text.count(old)}: {old!r}"
    return text.replace(old, new).encode()


def fresh_env() -> dict[str, str]:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONPYCACHEPREFIX"] = tempfile.mkdtemp(prefix="r222-r3-pyc-")
    env.pop("PYTHONPATH", None)
    return env


# A fresh interpreter that records every file opened under ROOT (audit hook
# installed before any repository import), runs one target, and prints JSON.
DRIVER = r'''
import json, os, sys, io, contextlib, runpy
root = os.path.realpath(sys.argv[1]); target = sys.argv[2]
opened = set()
def hook(event, args):
    if event == "open" and args and isinstance(args[0], (str, bytes, os.PathLike)):
        p = os.fsdecode(args[0])
        if not os.path.isabs(p):
            p = os.path.join(os.getcwd(), p)
        p = os.path.realpath(p)
        if p.startswith(root + os.sep):
            opened.add(os.path.relpath(p, root))
sys.addaudithook(hook)
status, detail = "PASS", ""
buf = io.StringIO()
try:
    with contextlib.redirect_stdout(buf):
        if target == "selftest":
            sys.path.insert(0, os.path.join(root, "avdecc"))
            sys.argv = [os.path.join(root, "avdecc/gen_aem_store.py"), "--self-test"]
            try:
                runpy.run_path(sys.argv[0], run_name="__main__")
            except SystemExit as e:
                if e.code not in (0, None):
                    status, detail = "FAIL", f"exit {e.code}"
        else:
            sys.path.insert(0, os.path.join(root, "sw/builder"))
            import test_builder as tb
            for name in target.split(","):
                getattr(tb, name)()
except BaseException as exc:
    status = "FAIL"
    detail = (type(exc).__name__ + ": " + (str(exc).splitlines() or [""])[0])[:170]
out = buf.getvalue()
print(json.dumps({"status": status, "detail": detail, "opened": sorted(opened),
                  "ok_arms": out.count("[ok  ]"), "fail_arms": out.count("[FAIL]"),
                  "tail": [l for l in out.splitlines() if l.strip()][-1:]}))
'''


def fresh(root: Path, target: str, py: str = PY) -> dict:
    proc = subprocess.run([py, "-c", DRIVER, str(root), target], cwd=str(root),
                          env=fresh_env(), capture_output=True, text=True, timeout=900)
    try:
        return json.loads(proc.stdout.strip().splitlines()[-1])
    except Exception:  # noqa: BLE001
        return {"status": "FAIL", "detail": f"driver rc {proc.returncode}: "
                f"{proc.stderr.strip()[-200:]}", "opened": [], "ok_arms": 0,
                "fail_arms": 0, "tail": []}


LOADER = "test_audio_unit_rates_loader_contract"
SHIP = "test_audio_unit_shipping_rates"
PPS = "test_pp_shadow_audio_unit_rates_match_config"
ALL36A = ",".join((LOADER, SHIP, PPS))

print(f"python {sys.version.split()[0]} ({PY})")
for name, root in (("cand", CAND), ("dev", DEV), ("src", SRC)):
    print(f"{name} root @ {rev(root)} tree {rev(root, 'HEAD^{tree}')}")
print(f"candidate MAX_AUDIO_UNIT_RATES = {CAND_EB.MAX_AUDIO_UNIT_RATES}")

print("\n== A: pristine candidate (in-process)")
grade("A1 gate 36a loader contract", "PASS", run(getattr(tb, LOADER)))
grade("A2 gate 36a shipping images", "PASS", run(getattr(tb, SHIP)))
grade("A3 gate 36a pp_shadow AU_RATES_C vs YAML", "PASS", run(getattr(tb, PPS)))
grade("A4 gate 32 builder doc key map", "PASS", run(tb.test_builder_doc_key_map))

print("\n== B: candidate gate 36a against the DEV (52711029) builder")
dev_src_path = DEV / "sw/builder/endstation_builder.py"
DEV_EB = load_builder(dev_src_path.read_text(), dev_src_path, "eb_dev")
print(f"dev builder has MAX_AUDIO_UNIT_RATES: {hasattr(DEV_EB, 'MAX_AUDIO_UNIT_RATES')}")
grade("B1 loader contract vs dev builder", "FAIL", run(getattr(tb, LOADER), DEV_EB))
grade("B2 shipping images vs dev builder", "PASS", run(getattr(tb, SHIP), DEV_EB))
grade("B3 pp_shadow comparison vs dev builder", "PASS", run(getattr(tb, PPS), DEV_EB))

print("\n== C: candidate builder mutants (loaded separately)")
cand_src_path = CAND / "sw/builder/endstation_builder.py"
CSRC = cand_src_path.read_text()
COUNT_BLOCK = (
    "    if len(rates) > MAX_AUDIO_UNIT_RATES:\n"
    "        raise ConfigError(\n"
    "            f\"clocking.audio_unit_rates_hz has {len(rates)} entries; \"\n"
    "            f\"processor walk bound is {MAX_AUDIO_UNIT_RATES} (L10, \"\n"
    "            \"protocol-processor/docs/architecture/07_memory_maps.md section 3.1)\")\n")
DUP_BLOCK = (
    "    if len(set(rates)) != len(rates):\n"
    "        raise ConfigError(\"clocking.audio_unit_rates_hz contains duplicate entries\")\n")
MEMBER_BLOCK = (
    "    if rate not in rates:\n"
    "        raise ConfigError(\"sampling_rate_hz must appear in audio_unit_rates_hz\")\n")
assert CSRC.count(COUNT_BLOCK) == 1 and CSRC.count(DUP_BLOCK) == 1
assert CSRC.count(MEMBER_BLOCK) == 1
MUTANTS = [
    ("C1 bound 8 -> 9", "MAX_AUDIO_UNIT_RATES = 8\n", "MAX_AUDIO_UNIT_RATES = 9\n", "FAIL"),
    ("C2 bound 8 -> 7", "MAX_AUDIO_UNIT_RATES = 8\n", "MAX_AUDIO_UNIT_RATES = 7\n", "FAIL"),
    ("C3 '>' -> '>=' in the count test", "if len(rates) > MAX_AUDIO_UNIT_RATES:",
     "if len(rates) >= MAX_AUDIO_UNIT_RATES:", "FAIL"),
    ("C4 duplicate refusal removed", DUP_BLOCK, "", "FAIL"),
    ("C5 duplicate test on raw (pre-int) values", "    if len(set(rates)) != len(rates):\n",
     "    _raw = list(clk.get(\"audio_unit_rates_hz\", [rate]))\n"
     "    if len(set(_raw)) != len(_raw):\n", "FAIL"),
    ("C6 rates stored sorted", "    rates = clocking[\"audio_unit_rates_hz\"]\n",
     "    clocking[\"audio_unit_rates_hz\"].sort()\n    rates = clocking[\"audio_unit_rates_hz\"]\n", "FAIL"),
    ("C7 omitted list defaults to [48000] always", "clk.get(\"audio_unit_rates_hz\", [rate])",
     "clk.get(\"audio_unit_rates_hz\", [48000])", "FAIL"),
    ("C8 duplicate test before count test (equivalent)", COUNT_BLOCK + DUP_BLOCK,
     DUP_BLOCK + COUNT_BLOCK, "PASS"),
    ("C9 current-rate membership removed", MEMBER_BLOCK, "", "FAIL"),
    ("C10 count refusal no longer names L10", "(L10, \"", "(rule, \"", "FAIL"),
    ("C11 count refusal removed", COUNT_BLOCK, "", "FAIL"),
    ("C12 count refusal truncates instead of refusing", COUNT_BLOCK,
     "    del rates[MAX_AUDIO_UNIT_RATES:]\n", "FAIL"),
]
for label, old, new, expect in MUTANTS:
    assert CSRC.count(old) >= 1, label
    mod = load_builder(CSRC.replace(old, new, 1), cand_src_path, "eb_mut_" + label.split()[0])
    got = run(getattr(tb, LOADER), mod)
    if label.startswith("C8"):
        # the equivalent mutant must also leave the image arm green
        got = got if got[0] == "FAIL" else run(getattr(tb, SHIP), mod)
    grade(label, expect, got)

print("\n== E: real shipping YAML mutants through the candidate image path")
YAML_CUR = "configs/endstation_arty_current.yaml"
YAML_4X4 = "configs/endstation_arty_4x4.yaml"
Y_OLD = "audio_unit_rates_hz: [48000, 96000, 192000]"
E_ROWS = [
    ("E1 arty_current list shortened", YAML_CUR, Y_OLD, "audio_unit_rates_hz: [48000, 96000]"),
    ("E2 arty_current list reordered", YAML_CUR, Y_OLD, "audio_unit_rates_hz: [96000, 48000, 192000]"),
    ("E3 arty_current duplicate appended", YAML_CUR, Y_OLD,
     "audio_unit_rates_hz: [48000, 96000, 192000, 192000]"),
    ("E4 arty_4x4 advertises 96000 too", YAML_4X4, "audio_unit_rates_hz: [48000]",
     "audio_unit_rates_hz: [48000, 96000]"),
]
for label, rel, old, new in E_ROWS:
    with replaced(CAND, rel, text_mutant(CAND, rel, old, new)):
        grade(f"{label} -> shipping arm", "FAIL", run(getattr(tb, SHIP)))

print("\n== F: loader versus packed image (candidate builder / dev builder)")


def outcome(eb, rates, current=48000, omit=False):
    import struct

    def mutate(c):
        c["clocking"]["sampling_rate_hz"] = current
        if omit:
            c["clocking"].pop("audio_unit_rates_hz", None)
        else:
            c["clocking"]["audio_unit_rates_hz"] = rates
    path = tb._variant(tb.CONFIGS["arty_current"], mutate)
    try:
        try:
            cfg = eb.load_config(str(path))
        except Exception as exc:  # noqa: BLE001
            return f"load_config {type(exc).__name__}: {str(exc)[:100]}"
        loaded = cfg["clocking"]["audio_unit_rates_hz"]
        try:
            ovl = eb.emit_aem_overlay(cfg)
            img = eb._entity_model_image(cfg, ovl)["aem_desc.bin"]
            desc = tb.image_descriptor(img, 0x0002)
            off, cnt = struct.unpack_from(">HH", desc, 140)
            words = list(struct.unpack_from(f">{cnt}I", desc, off))
            return f"loaded {loaded}; image offset {off} count {cnt} rates {words}"
        except Exception as exc:  # noqa: BLE001
            return f"loaded {loaded}; image {type(exc).__name__}: {str(exc)[:80]}"
    finally:
        path.unlink()


EIGHT = [192000, 96000, 44100, 88200, 176400, 32000, 24000, 48000]
F_ROWS = [
    ("F1 eight distinct (gate 36a's legal eight)", dict(rates=EIGHT)),
    ("F2 nine distinct", dict(rates=EIGHT + [22050])),
    ("F3 nine copies of 48000", dict(rates=[48000] * 9)),
    ("F4 [48000, '48000']", dict(rates=[48000, "48000"])),
    ("F5 [48000, 48000.5]", dict(rates=[48000, 48000.5])),
    ("F6 base rates reordered [192000, 48000, 96000]", dict(rates=[192000, 48000, 96000])),
    ("F7 omitted list, current 96000", dict(rates=None, current=96000, omit=True)),
    ("F8 empty list", dict(rates=[])),
    ("F11 eight copies of 48000", dict(rates=[48000] * 8)),
]
for label, kw in F_ROWS:
    print(label)
    print(f"    cand: {outcome(CAND_EB, **kw)}")
    print(f"    dev : {outcome(DEV_EB, **kw)}")

print("\n== G: #513 dependency path (fresh interpreters, empty bytecode cache)")
traces = {}
for label, target in (("G1a loader arm", LOADER), ("G1b shipping arm", SHIP),
                      ("G1c pp_shadow arm", PPS), ("G1d AEM store self-test", "selftest")):
    r = fresh(CAND, target)
    traces[label] = r
    opened = set(r["opened"])
    print(f"{label}: status {r['status']} {r['detail']} files opened {len(opened)}")
    print(f"    #513 paths opened: {sorted(opened & PR513_PATHS)}")
    print(f"    issue paths opened: {sorted(opened & ISSUE_PATHS)}")
    print(f"    avdecc files opened: {sorted(p for p in opened if p.startswith('avdecc/'))}")
    if target == "selftest":
        print(f"    arms ok {r['ok_arms']} fail {r['fail_arms']} tail {r['tail']}")
grade("G1a loader arm passes fresh", "PASS", (traces["G1a loader arm"]["status"], ""))
grade("G1b shipping arm passes fresh", "PASS", (traces["G1b shipping arm"]["status"], ""))
grade("G1c pp_shadow arm passes fresh", "PASS", (traces["G1c pp_shadow arm"]["status"], ""))
grade("G1d self-test passes fresh (20 arms)", "PASS",
      ("PASS" if traces["G1d AEM store self-test"]["status"] == "PASS"
       and traces["G1d AEM store self-test"]["ok_arms"] == 20
       and traces["G1d AEM store self-test"]["fail_arms"] == 0 else "FAIL", ""))
grade("G1e self-test opens no issue path", "PASS",
      ("PASS" if not set(traces["G1d AEM store self-test"]["opened"]) & ISSUE_PATHS else "FAIL", ""))
grade("G1f pp_shadow arm opens no #513 path", "PASS",
      ("PASS" if not set(traces["G1c pp_shadow arm"]["opened"]) & PR513_PATHS else "FAIL", ""))
if PY312:
    r = fresh(CAND, "selftest", PY312)
    grade(f"G1g self-test under {PY312.rsplit('/', 1)[-1]} (stdlib only)", "PASS",
          ("PASS" if r["status"] == "PASS" and r["ok_arms"] == 20 else "FAIL",
           f"{r['detail']} arms {r['ok_arms']}/{r['fail_arms']}"))

DESC = "avdecc/aem_descriptors.py"
G_ROWS = [
    ("G2 AUDIO_UNIT sampling_rates_offset field 144 -> 148", DESC,
     text_mutant(CAND, DESC, "b += be16(144)                      # sampling_rates_offset (fixed)",
                 "b += be16(148)                      # sampling_rates_offset (fixed)"),
     [(SHIP, "FAIL"), ("selftest", "PASS")]),
    ("G3 AUDIO_UNIT rate words emitted in reverse", DESC,
     text_mutant(CAND, DESC, "    for r in rates:\n        b += be32(r)\n",
                 "    for r in reversed(rates):\n        b += be32(r)\n"),
     [(SHIP, "FAIL")]),
    ("G4 revert avdecc/aem_maps.py to the source (pre-#513) blob", "avdecc/aem_maps.py",
     subprocess.run(["git", "-C", str(CAND), "show", "1496558d82cf35fc98dda0e781b2a1be643c301a:avdecc/aem_maps.py"],
                    check=True, capture_output=True).stdout,
     [(ALL36A, "PASS"), ("selftest", "FAIL")]),
    ("G5 revert avdecc/gen_aem_store.py to the source (pre-#513) blob", "avdecc/gen_aem_store.py",
     subprocess.run(["git", "-C", str(CAND), "show", "1496558d82cf35fc98dda0e781b2a1be643c301a:avdecc/gen_aem_store.py"],
                    check=True, capture_output=True).stdout,
     [(ALL36A, "PASS"), ("selftest", "FAIL")]),
    ("G6 KNOWN_MAP_DEVIATIONS widened by one stale entry", "avdecc/aem_maps.py",
     text_mutant(CAND, "avdecc/aem_maps.py", "    for c in range(2, 8)\n",
                 "    for c in range(2, 9)\n"),
     [(ALL36A, "PASS"), ("selftest", "FAIL")]),
]
for label, rel, new_bytes, checks in G_ROWS:
    with replaced(CAND, rel, new_bytes):
        for target, expect in checks:
            r = fresh(CAND, target)
            name = "self-test" if target == "selftest" else (
                "all gate 36a arms" if "," in target else target.replace("test_", ""))
            grade(f"{label} -> {name}", expect,
                  (r["status"], f"{r['detail']}" + (f" arms {r['ok_arms']}/{r['fail_arms']}"
                                                     if target == "selftest" else "")))

print("\n== H: CI carrier of gate 36a on the combined tree")
import yaml  # noqa: E402

wf_rel = ".github/workflows/docs.yml"
wf = yaml.safe_load((CAND / wf_rel).read_text())
steps = wf["jobs"]["docs-check"]["steps"]
names = [s.get("name", "<unnamed:" + str(s.get("uses", s.get("run", ""))[:30]) + ">") for s in steps]
print(f"docs-check steps: {len(steps)}")
for key in ("Fetch the builder source dependencies", "End-station builder gates",
            "AEM store generator self-test"):
    print(f"  step {names.index(key) + 1:>2}: {key}")
builder_run = steps[names.index("End-station builder gates")]["run"]
print(f"  builder step run: {builder_run.strip().splitlines()}")
print(f"  builder step keys: {sorted(steps[names.index('End-station builder gates')].keys())}")
grade("H1 submodule fetch precedes the builder step", "PASS",
      ("PASS" if names.index("Fetch the builder source dependencies")
       < names.index("End-station builder gates") else "FAIL", ""))
grade("H2 builder step (gate 36a) precedes the #513 self-test step", "PASS",
      ("PASS" if names.index("End-station builder gates")
       < names.index("AEM store generator self-test") else "FAIL", ""))


def ci_check(root: Path) -> tuple[str, str]:
    p = subprocess.run([PY, "scripts/ci_events.py", "--check"], cwd=str(root),
                       env=fresh_env(), capture_output=True, text=True, timeout=600)
    lines = [l for l in (p.stdout + p.stderr).splitlines() if l.strip()]
    hit = [l for l in lines if "builder" in l or "44 steps" in l or "must" in l][:1]
    return ("PASS" if p.returncode == 0 else "FAIL",
            f"rc {p.returncode}: {(hit or lines[-1:] or [''])[0][:150]}")


grade("H3 ci_events --check, pristine candidate", "PASS", ci_check(CAND))
wf_text = (CAND / wf_rel).read_text()
BUILDER_STEP = ("      - name: End-station builder gates\n"
                "        run: |\n"
                "          python3 -m pip install --quiet pyyaml\n"
                "          python3 sw/builder/test_builder.py\n")
SELFTEST_STEP = ("      - name: AEM store generator self-test\n"
                 "        run: python3 avdecc/gen_aem_store.py --self-test\n")
assert wf_text.count(BUILDER_STEP) == 1 and wf_text.count(SELFTEST_STEP) == 1
with replaced(CAND, wf_rel, wf_text.replace(BUILDER_STEP, "").encode()):
    grade("H4 builder step (gate 36a carrier) removed -> ci_events", "FAIL", ci_check(CAND))
with replaced(CAND, wf_rel, wf_text.replace(
        "          python3 sw/builder/test_builder.py\n",
        "          python3 sw/builder/test_builder.py || true\n").encode()):
    grade("H5 builder call made non-failing -> ci_events", "FAIL", ci_check(CAND))
with replaced(CAND, wf_rel, wf_text.replace(SELFTEST_STEP, "").encode()):
    grade("H6 #513 self-test step removed -> ci_events", "FAIL", ci_check(CAND))

print(f"\ngraded mismatches: {mismatches}")
for name, root in (("cand", CAND), ("dev", DEV), ("src", SRC)):
    status = subprocess.run(["git", "-C", str(root), "status", "--porcelain",
                             "--untracked-files=no"], capture_output=True, text=True).stdout
    print(f"{name} scratch tracked changes after probes: {len(status.splitlines())}")
sys.exit(1 if mismatches else 0)

#!/usr/bin/env python3
"""Remove parts of the R228-F1 fix, or plant R228-1's probes; gate 1b must answer.

No tree is copied and nothing is written into the checkout. Each entry is
applied IN MEMORY to the committed bytes of sw/builder/test_builder.py
(`git show HEAD:`), compiled as the module `test_builder` with its real
`__file__`, and gate 1b is then run by the lane's own
sw/builder/test_firmware_compiler.py, which imports that module.

  drive <checkout> <sdk-prefix> <out-dir> <verilator-bin-dir> [name ...]
      Run every selected entry as its own process (at most 8 at once) with
      the Verilator directory first on PATH; print one JSON line per entry.
  run <checkout> <name> <test_firmware_compiler arguments ...>
      The per-process worker used by `drive`.

Mutants: KILLED means a non-zero exit AND the expected failure sentence.
Plants (R228-1's plant_fp_mutant.py insertion, reproduced verbatim in
memory): PASS means exit 0 AND the "REFUSED ON THE RESOLVER PIN" line.
"""
import importlib.util
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

TABLE = ('RV32_STORE_BYTES = {"sb": 1, "sh": 2, "sw": 4,\n'
         '                    "fsh": 2, "fsw": 4, "fsd": 8, "fsq": 16}\n')
ATOMIC = ('RV32_ATOMIC_STORE_RE = re.compile(\n'
          '    r"^(?:amo(?:swap|add|xor|and|or|min|max|minu|maxu)|sc)\\.w"\n'
          '    r"(?:\\.(?:aq|rl|aqrl))?$")\n')
INTEGER_ONLY = [(TABLE, 'RV32_STORE_BYTES = {"sb": 1, "sh": 2, "sw": 4}\n'),
                (ATOMIC, 'RV32_ATOMIC_STORE_RE = re.compile(r"(?!)")\n')]
DEFAULT = ('    if rv32_memory_operand(args) and not rv32_is_load(mnem):\n'
           '        _rv32_forget_symbols(state)\n'
           '        return ("store", (Rv32Where("unclassified", f"{mnem} {ops}"), None))\n')
NO_DEFAULT = [(DEFAULT, "")]
OVERLAP = ('    for key in [key for key in mem if key[:-1] == prefix and\n'
           '                key[-1] <= start + width - 1 and key[-1] + 3 >= start]:\n'
           '        mem[key] = None\n')
FOOTPRINT = ('    further = range((address & ~3) + 4, ((address + width - 1) & ~3) + 4, 4)\n')
AMO_RD = ('            #: ordinary spelling.\n            state.set(args[0], None)\n')
UNIT_CONTROL = [
    ("    for label, base, insn, words in class_probes:\n",
     "    for label, base, insn, words in ():\n"),
    ('                    for insn in ("c.sw a5,0(a4)", "amocas.w a3,a5,0(a4)")]\n',
     "                    for insn in ()]\n"),
    ("    for label, body in stale_probes:\n", "    for label, body in ():\n"),
]
MEASUREMENT = [(
    '    if baseline_census_verdict["ran"]:\n'
    '        for label, mutation, mnemonic, extension in store_class_mutations:\n',
    '    if False:\n'
    '        for label, mutation, mnemonic, extension in store_class_mutations:\n')]
MUTANTS = {
    "FP and atomic classes dropped from the tables": (
        INTEGER_ONLY, "the fsh store class must be judged by address"),
    "unclassified-memory default removed": (
        NO_DEFAULT, "neither a recognised load nor a recognised store"),
    "pre-fix classification restored": (
        INTEGER_ONLY + NO_DEFAULT, "the fsh store class must be judged by address"),
    "overlap forgetting removed": (
        [(OVERLAP, "    return\n")], "after an fsd over a frame slot"),
    "footprint reduced to the first byte's word": (
        [(FOOTPRINT, "    further = ()\n")], "the fsd store class must be judged"),
    "AMO destination left holding its old value": (
        [(AMO_RD, "            #: ordinary spelling.\n            pass\n")],
        "after an AMO writing its base register"),
    "pre-fix classification and literal-assembly control removed": (
        INTEGER_ONLY + NO_DEFAULT + UNIT_CONTROL,
        "the resolver accepted the float struct-overlay store"),
    "pre-fix classification, literal control and compiled measurement removed": (
        INTEGER_ONLY + NO_DEFAULT + UNIT_CONTROL + MEASUREMENT,
        "float struct-overlay store through a paged base mutation passed the "
        "boot-contract gate"),
}
PLANT_ANCHOR = "    for mutation in mutations:\n        assert_rejected(*mutation)\n"


def plant(kind: str) -> str:
    """R228-1's plant_fp_mutant.py insertion for `kind`, character for character."""
    member, value = {"float": ("volatile float", "1.0000001f"),
                     "double": ("volatile double", "1.0000000000000002"),
                     "uint32": ("volatile uint32_t", "1u")}[kind]
    return (
        "    r228_probe = replace_once(\n"
        "        stored_before_aem(\n"
        "            f\"((milan_adp_r228)((csr_page << 16) | {adp_name}))->ctrl = " + value + ";\",\n"
        "            \"R228 " + kind + " struct-overlay store through a paged base\"),\n"
        "        \"static int aem_loaded;\",\n"
        "        \"typedef struct { " + member + " ctrl; } *milan_adp_r228;\\n\"\n"
        "        f\"static unsigned int csr_page = 0x{csr_base >> 16:04x}u;\\n\\n\"\n"
        "        \"static int aem_loaded;\", \"R228 paged " + kind + " overlay typedef\")\n"
        "    print(\"R228 PROBE planted: " + kind + " overlay store, pinned on RESOLVER_STORE_PIN\", flush=True)\n"
        "    assert_rejected(\"R228 PROBE: entity enabled by a " + kind.upper() +
        " struct-overlay store through a paged base\", r228_probe, docs_source, csr_source,\n"
        "                    RESOLVER_STORE_PIN)\n"
        "    print(\"R228 PROBE REFUSED ON THE RESOLVER PIN: " + kind + "\", flush=True)\n")


def edits_for(name: str) -> list[tuple[str, str]]:
    """The textual edits one entry makes."""
    if name.startswith("plant-"):
        kind = name.split("-", 1)[1]
        return [(PLANT_ANCHOR, plant(kind) + PLANT_ANCHOR)]
    return MUTANTS[name][0]


def worker(checkout: Path, name: str, args: list[str]) -> None:
    """Compile the mutated module in memory and run the lane's gate 1b driver."""
    path = checkout / "sw/builder/test_builder.py"
    text = subprocess.run(["git", "-C", str(checkout), "show", "HEAD:sw/builder/test_builder.py"],
                          check=True, capture_output=True, text=True).stdout
    assert path.read_text() == text, "working tree differs from HEAD; refusing"
    for old, new in edits_for(name):
        assert text.count(old) == 1, f"{name}: anchor not unique: {old[:60]!r}"
        text = text.replace(old, new)
    print(f"IN-MEMORY MUTATION: {name}", flush=True)
    spec = importlib.util.spec_from_loader("test_builder", loader=None, origin=str(path))
    module = importlib.util.module_from_spec(spec)
    module.__file__ = str(path)
    sys.modules["test_builder"] = module
    exec(compile(text, str(path), "exec"), module.__dict__)  # noqa: S102 - the gate under test
    driver = checkout / "sw/builder/test_firmware_compiler.py"
    spec = importlib.util.spec_from_file_location("test_firmware_compiler", driver)
    tfc = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tfc)
    assert tfc.builder is module, "the driver did not import the mutated module"
    sys.argv = [str(driver), *args]
    tfc.main()


def drive(checkout: Path, prefix: Path, out: Path, vbin: Path, names: list[str]) -> None:
    """Run each entry in its own process and record exit, head and evidence."""
    head = subprocess.run(["git", "-C", str(checkout), "rev-parse", "HEAD"],
                          check=True, capture_output=True, text=True).stdout.strip()
    entries = names or [*MUTANTS, "plant-float", "plant-double", "plant-uint32"]
    out.mkdir(parents=True, exist_ok=True)
    env = {**os.environ, "PATH": f"{vbin}:{os.environ['PATH']}"}

    def one(name: str) -> dict[str, object]:
        slug = name.replace(" ", "_").replace("'", "").replace(",", "")
        log, audit = out / f"{slug}.log", out / f"{slug}-argv.jsonl"
        start = time.time()
        with log.open("w") as stream:
            done = subprocess.run(
                [sys.executable, "-u", __file__, "run", str(checkout), name,
                 "--sdk-destination", str(prefix), "--audit", str(audit)],
                stdout=stream, stderr=subprocess.STDOUT, env=env, timeout=3600)
        output = log.read_text(errors="replace")
        if name.startswith("plant-"):
            kind = name.split("-", 1)[1]
            expected = f"R228 PROBE REFUSED ON THE RESOLVER PIN: {kind}"
            found = expected in output
            verdict = "REFUSED ON PIN, GATE PASS" if done.returncode == 0 and found else "FAIL"
        else:
            expected = MUTANTS[name][1]
            found = expected in output
            verdict = "KILLED" if done.returncode and found else "NOT KILLED"
        tail = [line for line in output.splitlines()
                if "Error" in line or "GATE 1b PASS" in line][-2:]
        dirty = subprocess.run(["git", "-C", str(checkout), "status", "--porcelain"],
                               capture_output=True, text=True).stdout.count("\n")
        return {"entry": name, "head": head, "exit": done.returncode,
                "expected": expected, "found": found, "verdict": verdict,
                "elapsed_s": round(time.time() - start, 1), "checkout_dirty_lines": dirty,
                "log": log.name, "evidence": [line[:400] for line in tail]}

    with ThreadPoolExecutor(max_workers=min(8, len(entries))) as pool:
        for result in pool.map(one, entries):
            print(json.dumps(result), flush=True)


if __name__ == "__main__":
    if sys.argv[1] == "run":
        worker(Path(sys.argv[2]).resolve(), sys.argv[3], sys.argv[4:])
    elif sys.argv[1] == "drive":
        drive(*(Path(a).resolve() for a in sys.argv[2:6]), sys.argv[6:])
    else:
        raise SystemExit(__doc__)

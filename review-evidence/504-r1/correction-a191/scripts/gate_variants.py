#!/usr/bin/env python3
"""Run gate 1b on in-memory variants of the committed head (A191, #504 / PR #521).

No tree is copied and nothing is written into the checkout. A MUTANT applies
exact textual edits to the committed bytes of sw/builder/test_builder.py
(`git show HEAD:`), executes that text as the module `test_builder` with its
real `__file__`, and runs gate 1b through the lane's own
sw/builder/test_firmware_compiler.py. A PLANT keeps the builder as committed
and hands gate 1b a firmware source patched with a reviewer's published diff:
only the gate's read of sw/firmware/milan_baremetal/milan_baremetal.c is
redirected (the -H include measurement still opens the file on disk, whose
include set no plant changes).

  drive <checkout> <sdk-prefix> <out-dir> <verilator-bin-dir> <jobs> [name ...]
      Each selected entry in its own process, at most <jobs> at once, with the
      Verilator directory first on PATH; one JSON line per entry.
  run <checkout> <name> <test_firmware_compiler arguments ...>
      The per-process worker `drive` starts.

Verdicts. A mutant is KILLED when gate 1b exits non-zero AND its log carries
the expected sentence (the control that answers it); otherwise SURVIVED or
KILLED-ELSEWHERE. A plant is REFUSED or PASSED by exit status; the expected
outcome and sentence are recorded beside it.
"""
import json
import os
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIRMWARE = "sw/firmware/milan_baremetal/milan_baremetal.c"
BUILDER = "sw/builder/test_builder.py"

#: Exact edits. The first seven are the published reviewer mutants whose
#: anchors still exist at this head, kept byte for byte (R227-2
#: resolver_gate_mutant_edit.py, R228-2 mutate_resolver.py); the rest remove
#: this round's own changes.
RANGE_WIDTH = [("                                         held.hi + offset + width - 1)",
                "                                         held.hi + offset)")]
MIRROR_INTEGER_ONLY = [(
    "        if rv32_store_bytes(mnem) is not None or \\\n"
    "                (rv32_memory_operand(args) and not rv32_is_load(mnem)) or \\\n"
    "                mnem in (\"call\", \"jal\", \"jalr\", \"tail\", \"jr\", \"ret\"):",
    "        if mnem in (\"sw\", \"sh\", \"sb\") or \\\n"
    "                mnem in (\"call\", \"jal\", \"jalr\", \"tail\", \"jr\", \"ret\"):")]
SUBWORD_VALUE = [('    if mnem == "sw" or mnem.startswith("amoswap."):\n',
                  '    if mnem in ("sb", "sh", "sw") or mnem.startswith("amoswap."):\n')]
AMO_VALUE = [('    if mnem == "sw" or mnem.startswith("amoswap."):\n',
              '    if mnem == "sw" or RV32_ATOMIC_STORE_RE.match(mnem):\n')]
STACK_KEEPS_FRAME = [("            _rv32_forget_frame(state)\n"
                      "            return (\"store\", (Rv32Where(\"stack\"), value))\n",
                      "            return (\"store\", (Rv32Where(\"stack\"), value))\n")]
NO_STALE_CONTROL = [("    for label, body in stale_probes:\n",
                     "    for label, body in ():\n")]
MUTANTS = {
    "R5/RM8-range-footprint-width": (
        RANGE_WIDTH, "loop from 0x8fffffbe came back as"),
    "R6/RM1-mirror-integer-stores-only": (
        MIRROR_INTEGER_ONLY, "with an fsw over the slot between the slot's load"),
    "RM5-memory-operand-needs-displacement": (
        [('RV32_MEM_BASE_RE = re.compile(r"\\(\\s*([a-z0-9]+)\\s*\\)$")',
          'RV32_MEM_BASE_RE = re.compile(r"\\d\\(\\s*([a-z0-9]+)\\s*\\)$")')],
        "the classifier's class default must fail closed"),
    "RM11-sym-overlap-fixed-4": (
        [("            _rv32_forget_overlap(state.mem, (\"sym\", held.name), at, width)",
          "            _rv32_forget_overlap(state.mem, (\"sym\", held.name), at, 4)")],
        "after an fsd over a static's first word, reloaded at its second"),
    "RM12-frame-overlap-fixed-4": (
        [("            _rv32_forget_overlap(state.mem, (base,), offset, width)",
          "            _rv32_forget_overlap(state.mem, (base,), offset, 4)")],
        "after an fsd over a frame slot the RV32 resolver"),
    "R10-on-this-head-every-AMO-and-SC-writes-rs2": (
        AMO_VALUE, "after an amoor.w into a frame slot, handed a placed address"),
    "A191-subword-stores-carry-their-source": (
        SUBWORD_VALUE, "after a byte store at a frame slot's own offset"),
    "A191-stack-store-keeps-frame-slots": (
        STACK_KEEPS_FRAME, "after an integer store through a pointer to a frame slot"),
    "A191-subword-value-and-literal-control-removed": (
        SUBWORD_VALUE + NO_STALE_CONTROL,
        "entity enabled through a local rewritten by a union byte store at its "
        "own offset mutation passed the boot-contract gate"),
    "A191-stack-store-and-literal-control-removed": (
        STACK_KEEPS_FRAME + NO_STALE_CONTROL,
        "entity enabled through a local rewritten by an integer store through a "
        "pointer to it mutation passed the boot-contract gate"),
}
UNPLACED_IN_FABRIC = ("STORE this gate cannot PLACE and that no declared residual "
                      "accounts for: configure_fabric() through unplaced")
#: name: (diff file, expected verdict, sentence the log must carry)
PLANTS = {
    "plant-R227-2-byte-overwrite": ("R227-2-plant-byte-overwrite.diff", "REFUSED",
                                    UNPLACED_IN_FABRIC),
    "plant-R227-2-half-overwrite": ("R227-2-plant-half-overwrite.diff", "REFUSED",
                                    UNPLACED_IN_FABRIC),
    "plant-R227-2-no-overwrite": ("R227-2-plant-no-overwrite.diff", "REFUSED",
                                  "STORES into the Milan CSR window"),
    "plant-R228-2-E12-store-through-local-pointer": (
        "R228-2-E12-store-through-local-pointer.diff", "REFUSED", UNPLACED_IN_FABRIC),
    "plant-R228-2-E12f-fp-store-through-local-pointer": (
        "R228-2-E12f-fp-store-through-local-pointer.diff", "REFUSED", UNPLACED_IN_FABRIC),
    "plant-R228-2-E10b-ranged-fsd-straddle-static-base": (
        "R228-2-E10b-ranged-fsd-straddle-static-base.diff", "REFUSED",
        "STORES into the Milan CSR window"),
    "plant-R228-2-E11b-static-fsd-over-second-word-computed": (
        "R228-2-E11b-static-fsd-over-second-word-computed.diff", "REFUSED",
        "STORE this gate cannot PLACE"),
    "plant-R228-2-E8-atomic-exchange-64-libcall": (
        "R228-2-E8-atomic-exchange-64-libcall.diff", "PASSED", "GATE 1b PASS"),
    "plant-R228-2-E9b-memset-libcall-typedef": (
        "R228-2-E9b-memset-libcall-typedef.diff", "PASSED", "GATE 1b PASS"),
}


def git(checkout: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(checkout), *args], check=True,
                          capture_output=True, text=True).stdout


def worker(checkout: Path, name: str, args: list[str]) -> None:
    """Build the variant in memory and run the lane's gate 1b driver."""
    import importlib.util
    path = checkout / BUILDER
    text = git(checkout, "show", f"HEAD:{BUILDER}")
    assert path.read_text() == text, "working tree differs from HEAD; refusing"
    if name in MUTANTS:
        for old, new in MUTANTS[name][0]:
            assert text.count(old) == 1, f"{name}: anchor count {text.count(old)}: {old[:70]!r}"
            text = text.replace(old, new)
        print(f"IN-MEMORY MUTATION: {name}", flush=True)
    else:
        firmware = checkout / FIRMWARE
        pristine = git(checkout, "show", f"HEAD:{FIRMWARE}")
        assert firmware.read_text() == pristine, "firmware differs from HEAD; refusing"
        with tempfile.TemporaryDirectory() as tmp:
            copy = Path(tmp) / "fw.c"
            copy.write_text(pristine)
            subprocess.run(["patch", "-s", str(copy), str(HERE / "plants" / PLANTS[name][0])],
                           check=True)
            planted = copy.read_text()
        real_read_text = Path.read_text
        target = firmware.resolve()

        def read_text(self, *a, **k):
            if self.resolve() == target:
                return planted
            return real_read_text(self, *a, **k)

        Path.read_text = read_text
        print(f"IN-MEMORY PLANT: {name} ({len(planted) - len(pristine):+d} bytes)", flush=True)
    spec = importlib.util.spec_from_loader("test_builder", loader=None, origin=str(path))
    module = importlib.util.module_from_spec(spec)
    module.__file__ = str(path)
    sys.modules["test_builder"] = module
    exec(compile(text, str(path), "exec"), module.__dict__)  # noqa: S102 - the gate under test
    driver = checkout / "sw/builder/test_firmware_compiler.py"
    spec = importlib.util.spec_from_file_location("test_firmware_compiler", driver)
    tfc = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tfc)
    assert tfc.builder is module, "the driver did not import the variant module"
    sys.argv = [str(driver), *args]
    tfc.main()


def drive(checkout: Path, prefix: Path, out: Path, vbin: Path, jobs: int,
          names: list[str]) -> None:
    head = git(checkout, "rev-parse", "HEAD").strip()
    entries = names or [*MUTANTS, *PLANTS]
    out.mkdir(parents=True, exist_ok=True)
    env = {**os.environ, "PATH": f"{vbin}:{os.environ['PATH']}"}

    def one(name: str) -> dict[str, object]:
        slug = name.replace("/", "_")
        log, audit = out / f"{slug}.log", out / f"{slug}-argv.jsonl"
        start = time.time()
        with log.open("w") as stream:
            done = subprocess.run(
                [sys.executable, "-u", __file__, "run", str(checkout), name,
                 "--sdk-destination", str(prefix), "--audit", str(audit)],
                stdout=stream, stderr=subprocess.STDOUT, env=env, cwd=checkout)
        body = log.read_text(errors="replace")
        if name in MUTANTS:
            sentence = MUTANTS[name][1]
            verdict = ("SURVIVED" if done.returncode == 0 else
                       "KILLED" if sentence in body else "KILLED-ELSEWHERE")
            expected = "KILLED"
        else:
            expected, sentence = PLANTS[name][1], PLANTS[name][2]
            verdict = "PASSED" if done.returncode == 0 else "REFUSED"
        record = {"name": name, "head": head, "exit": done.returncode,
                  "verdict": verdict, "expected": expected,
                  "sentence": sentence, "sentence_in_log": sentence in body,
                  "as_expected": verdict == expected and sentence in body,
                  "elapsed_s": round(time.time() - start, 1), "log": log.name}
        (out / f"{slug}.json").write_text(json.dumps(record, indent=1) + "\n")
        print(json.dumps(record), flush=True)
        return record

    with ThreadPoolExecutor(max_workers=jobs) as pool:
        results = list(pool.map(one, entries))
    bad = [r["name"] for r in results if not r["as_expected"]]
    print(f"SUMMARY head={head} {len(results) - len(bad)}/{len(results)} as expected"
          + (f"; NOT as expected: {bad}" if bad else ""), flush=True)
    sys.exit(1 if bad else 0)


def main() -> None:
    if sys.argv[1] == "run":
        worker(Path(sys.argv[2]).resolve(), sys.argv[3], sys.argv[4:])
    elif sys.argv[1] == "drive":
        drive(Path(sys.argv[2]).resolve(), Path(sys.argv[3]).resolve(),
              Path(sys.argv[4]).resolve(), Path(sys.argv[5]).resolve(),
              int(sys.argv[6]), sys.argv[7:])
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main()

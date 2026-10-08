#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Issue #654: early CPU option refusals and optional real-netlist effect tests.

The builder runs the refusal bank. --netlists additionally requires the
NaxRiscv data package and its generator sources; no missing dependency skips.
Each export uses a fresh process because CPU wrappers retain class state.
"""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
SOC = ROOT / "sw/litex/milan_soc.py"

# Keep __file__ at the real recipe, including when planting source mutations.
# Only the refusal probe replaces CPU setup with a sentinel. The effect arm
# runs the real constructor, generator and Builder without software compilation.
_PROBE = r'''
import contextlib, hashlib, io, json, re, sys, types
from pathlib import Path
from unittest.mock import patch
spec = json.loads(sys.stdin.read())
source = Path(spec["soc"]).read_text()
for old, new in spec["mutations"]:
    assert source.count(old) == 1, (old, source.count(old))
    source = source.replace(old, new)
sys.path.insert(0, str(Path(spec["soc"]).parent))
mod = types.ModuleType("soc_option_probe")
mod.__file__ = spec["soc"]
sys.modules[mod.__name__] = mod
exec(compile(source, spec["soc"], "exec"), mod.__dict__)
from litex.soc.cores.cpu.naxriscv import NaxRiscv
from litex.soc.cores.cpu.vexiiriscv import VexiiRiscv
class SetupStarted(Exception):
    pass
sink = io.StringIO()
result = {}
with contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
    if spec["mode"] == "export":
        import pythondata_cpu_naxriscv
        from litex.soc.integration.builder import Builder
        if spec["data"]:
            pythondata_cpu_naxriscv.data_location = spec["data"]
        data = Path(pythondata_cpu_naxriscv.data_location)
        assert (data / "ext/NaxRiscv/build.sbt").is_file(), "NaxRiscv sources required"
        read_args = NaxRiscv.args_read
        def frozen_args(args):
            read_args(args)
            NaxRiscv.update_repo = "no"
        # Freeze source selection, leaving every hardware option untouched.
        with patch.object(NaxRiscv, "args_read", side_effect=frozen_args):
            soc = mod.MilanSoC(mod.alinx_ax7101.Platform(), 50000000,
                              cpu="naxriscv", xlen=spec["xlen"], with_milan=False,
                              **spec["options"])
            Builder(soc, output_dir=spec["output"], compile_software=False).build(run=False)
        raw = (data / (soc.cpu.netlist_name + ".v")).read_bytes()
        rtl = re.sub(rb"//[^\n]*", b"", raw).replace(soc.cpu.netlist_name.encode(), b"CPU")
        result = {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw),
                  "rtl_sha256": hashlib.sha256(rtl).hexdigest()}
    else:
        with patch.object(VexiiRiscv, "args_read", side_effect=SetupStarted), \
             patch.object(NaxRiscv, "args_read", side_effect=SetupStarted), \
             patch.object(mod.SoCCore, "__init__", side_effect=SetupStarted), \
             patch.object(mod.board_audio_routing, "assert_front_end_routed", side_effect=SetupStarted):
            try:
                if spec["mode"] == "cli":
                    sys.argv = [spec["soc"], "--sys-clk-freq", "50000000", "--no-milan",
                                "--output-dir", spec["output"], *spec["argv"]]
                    mod.main()
                else:
                    mod.MilanSoC(None, 50000000, with_milan=False, cpu=spec["cpu"],
                                 xlen=spec["xlen"], **spec["options"])
            except SetupStarted:
                result = {"kind": "setup"}
            except ValueError as exc:
                result = {"kind": "refused", "reason": str(exc)}
            except SystemExit as exc:
                result = {"kind": "exit", "rc": exc.code, "reason": sink.getvalue()}
            else:
                raise AssertionError("probe reached neither refusal nor setup")
        assert not Path(spec["output"]).exists(), "refusal probe wrote build output"
Path(spec["result"]).write_text(json.dumps(result))
'''


def _probe(directory, **case):
    spec = dict(soc=str(SOC), mode="constructor", cpu="vexiiriscv", xlen=32, options={},
                argv=[], mutations=[], data=None,
                output=str(directory / "build"), result=str(directory / "result.json"))
    spec.update(case)
    run = subprocess.run([sys.executable, "-B", "-c", _PROBE], input=json.dumps(spec),
                         text=True, capture_output=True, cwd=ROOT, timeout=900)
    if run.returncode != 0:
        raise RuntimeError(run.stdout + run.stderr)
    return json.loads((directory / "result.json").read_text())


def _refused(result, reason, cli=False):
    assert result["kind"] == ("exit" if cli else "refused"), result
    if cli:
        assert result["rc"] == 2, result
    assert reason in result["reason"], result


def _killed(check, label):
    try:
        check()
    except AssertionError:
        print(f"  killed: {label}")
    else:
        raise AssertionError(f"survived: {label}")


def _constructor_cases(directory):
    count = 0
    for xlen in (32, 64):
        for cpu in ("vexiiriscv", "naxriscv"):
            invalid = [({"l2_bytes": value}, "whole number")
                       for value in (-1, 0.5, float("nan"), float("inf"))]
            if cpu == "vexiiriscv":
                invalid += [({"with_fpu": True}, "floating-point hardware"),
                            ({"l2_bytes": 8192}, "without a data cache"),
                            ({"with_fpu": True, "l2_bytes": 8192}, "floating-point hardware")]
                valid = [{}, {"l2_bytes": 0}]
            else:
                invalid += [({"l2_bytes": 0}, "keeps its nonzero default")]
                valid = [{}, {"with_fpu": True}, {"l2_bytes": 8192},
                         {"with_fpu": True, "l2_bytes": 8192}]
            for options, reason in invalid:
                _refused(_probe(directory, cpu=cpu, xlen=xlen, options=options), reason)
                count += 1
            for options in valid:
                assert _probe(directory, cpu=cpu, xlen=xlen, options=options)["kind"] == "setup"
                count += 1
        for cpu in ("NaxRiscv", "unknown", "", None):
            for options in ({}, {"l2_bytes": 0}):
                _refused(_probe(directory, cpu=cpu, xlen=xlen, options=options), "unsupported CPU")
                count += 1
    return count


def _cli_cases(directory):
    count = 0
    for argv, reason in ((["--with-fpu"], "floating-point hardware"),
                         (["--l2-bytes", "8192"], "without a data cache"),
                         (["--l2-bytes", "-1"], "whole number"),
                         (["--l2-bytes", "0.5"], "whole number"),
                         (["--l2-bytes", "nan"], "whole number"),
                         (["--l2-bytes", "inf"], "whole number"),
                         (["--l2-bytes=1e-400"], "whole number"),
                         (["--l2-bytes=-1e-400"], "whole number"),
                         (["--l2-bytes=1.00000000000000000000000000001"], "whole number"),
                         (["--l2-bytes=invalid"], "whole number"),
                         (["--cpu", "naxriscv", "--l2-bytes", "0"], "keeps its nonzero default"),
                         (["--cpu", "naxriscv", "--with-fpu"], "requires --cpu vexiiriscv"),
                         (["--cpu", "naxriscv", "--l2-bytes", "8192"], "requires --cpu vexiiriscv")):
        _refused(_probe(directory, mode="cli", argv=argv), reason, cli=True)
        count += 1
    for argv in ([], ["--l2-bytes", "0"], ["--l2-bytes=0.0"],
                 ["--l2-bytes=-0"], ["--l2-bytes=0e-400"]):
        assert _probe(directory, mode="cli", argv=argv)["kind"] == "setup"
        count += 1
    return count


def _refusal_controls(directory):
    cases = [
        ("remove FPU refusal", "        if with_fpu:\n", "        if False:\n",
         "vexiiriscv", {"with_fpu": True}, "floating-point hardware"),
        ("remove cacheless L2 refusal", "        if l2_bytes:\n", "        if False:\n",
         "vexiiriscv", {"l2_bytes": 8192}, "without a data cache"),
        ("remove NaxRiscv zero refusal", '    if cpu == "naxriscv" and l2_bytes == 0:', '    if False:',
         "naxriscv", {"l2_bytes": 0}, "keeps its nonzero default"),
        ("remove byte-size validation",
         '        if not size.is_finite() or size < 0 or size != size.to_integral_value():',
         '        if False:',
         "naxriscv", {"l2_bytes": 0.5}, "whole number"),
        ("remove unknown CPU refusal", '    if cpu not in ("vexiiriscv", "naxriscv"):',
         '    if False:', "NaxRiscv", {"l2_bytes": 0}, "unsupported CPU"),
        ("remove constructor validation", '        _validate_cpu_options(cpu, with_fpu, l2_bytes)',
         '        pass', "vexiiriscv", {"with_fpu": True}, "floating-point hardware"),
    ]
    for label, old, new, cpu, options, reason in cases:
        # Include the raise in ambiguous anchors; NaxRiscv has forwarding ifs too.
        if label == "remove FPU refusal":
            suffix = '            raise ValueError("--with-fpu'
            old, new = old + suffix, new + suffix
        if label == "remove cacheless L2 refusal":
            suffix = '            raise ValueError("--l2-bytes'
            old, new = old + suffix, new + suffix
        _killed(lambda: _refused(_probe(directory, cpu=cpu, options=options,
                                        mutations=[(old, new)]), reason), label)
    _killed(lambda: _refused(_probe(directory, mode="cli", argv=["--with-fpu"], mutations=[
        ('        _validate_cpu_options(args.cpu, args.with_fpu, args.l2_bytes)', '        pass')]),
        "floating-point hardware", cli=True), "remove CLI validation")
    for token in ("1e-400", "-1e-400"):
        _killed(lambda: _refused(_probe(directory, mode="cli", argv=[f"--l2-bytes={token}"],
            mutations=[('default=None, type=_parse_l2_bytes,', 'default=None, type=float,')]),
            "whole number", cli=True), f"lossy byte-count parsing: {token}")
    return len(cases) + 3


def test_refusals() -> None:
    """Grade real CLI/constructor refusals, setup boundaries and planted removals."""
    with tempfile.TemporaryDirectory(prefix="soc-options-") as tmp:
        directory = Path(tmp)
        count = _constructor_cases(directory)
        cli_count = _cli_cases(directory)
        controls = _refusal_controls(directory)
    print(f"CPU option refusals: {count} constructor cases, {cli_count} CLI cases, {controls} killed controls")


def _effect(base, changed):
    assert base["sha256"] != changed["sha256"], "option left raw netlist identical"
    assert base["rtl_sha256"] != changed["rtl_sha256"], "option changed names/comments only"


def test_netlists(data: str | None) -> None:
    """Prove both NaxRiscv option effects in RV32/RV64, and kill lost forwarding."""
    cases = [
        ("fpu", {"with_fpu": True}, [('_nax_args.with_fpu = with_fpu', '_nax_args.with_fpu = False'),
         ('if with_fpu:\n                _nax_args.scala_args', 'if False:\n                _nax_args.scala_args')]),
        ("l2", {"l2_bytes": 8192}, [('_nax_args.l2_bytes = int(l2_bytes)', 'pass')]),
    ]
    with tempfile.TemporaryDirectory(prefix="soc-option-netlists-") as tmp:
        for xlen in (32, 64):
            directory = Path(tmp) / str(xlen)
            directory.mkdir()
            base = _probe(directory, mode="export", xlen=xlen, data=data)
            print(json.dumps(dict(xlen=xlen, option="omitted", **base)), flush=True)
            for label, options, mutations in cases:
                changed = _probe(directory, mode="export", xlen=xlen, options=options, data=data)
                _effect(base, changed)
                print(json.dumps(dict(xlen=xlen, option=label, **changed)), flush=True)
                planted = _probe(directory, mode="export", xlen=xlen, options=options,
                                 mutations=mutations, data=data)
                _killed(lambda: _effect(base, planted), f"RV{xlen} lost {label} forwarding")
    print("NaxRiscv netlists: 4 effects, 4 killed controls; generated names/comments excluded")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--netlists", action="store_true", help="also run the real NaxRiscv generator")
    parser.add_argument("--nax-data-dir", help="isolated NaxRiscv data directory with generator sources")
    args = parser.parse_args()
    test_refusals()
    if args.netlists:
        test_netlists(args.nax_data_dir)
    print("RESULT: PASS")

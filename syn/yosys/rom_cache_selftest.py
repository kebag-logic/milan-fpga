#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Generated-ROM cache controls through the shipping run.sh and real tools.

A private python3 wrapper changes only generator output in the gate's scratch
folder. Generator sources, sv2v, Yosys and the driver remain untouched. Each
run keeps raw output, result records, generated-image hashes and cache argv.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from contextlib import contextmanager
from collections.abc import Iterator
from pathlib import Path

import result_cache as cache

ROOT = Path(__file__).resolve().parents[2]
IMAGES = ("ltn_rom.hex", "ucode.hex", "gptp_ucode.hex")
TOPS = ("cdc_pulse", "cdc_handshake")
# This wrapper delegates every ordinary Python invocation to the real binary.
# Output injection deliberately follows a successful real generator invocation.
WRAPPER = r'''
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

args = sys.argv[1:]
real = os.environ["ROM_PROBE_PYTHON"]
script = Path(args[0]).name if args else ""
generators = ("gen_ltn_rom.py", "gen_ucode.py", "gen_gptp_ucode.py")
if script in generators and "-o" in args:
    image = Path(args[args.index("-o") + 1])
    selected = image.name == os.environ.get("ROM_PROBE_IMAGE")
    action = os.environ.get("ROM_PROBE_ACTION", "") if selected else ""
    if action == "failed":
        sys.exit(7)
    rc = subprocess.run([real, *args]).returncode
    if rc:
        sys.exit(rc)
    if action == "changed":
        image.write_bytes(b"INVALID_ROM_DATA\n")
    elif action == "empty":
        image.write_bytes(b"")
    elif action == "missing":
        image.rename(image.with_name(image.name + ".wrong-name"))
    data = image.read_bytes() if image.exists() else None
    event = {"image": image.name, "bytes": len(data) if data is not None else None,
             "sha256": hashlib.sha256(data).hexdigest() if data is not None else None}
    with Path(os.environ["ROM_PROBE_TRACE"]).open("a") as handle:
        handle.write(json.dumps(event) + "\n")
    sys.exit(0)
if script == "result_cache.py" and len(args) > 1 and args[1] in ("lookup", "store"):
    event = {"operation": args[1], "args": args[2:]}
    staged = Path(args[args.index("--sv2v-file") + 1])
    event["sv2v_sha256"] = hashlib.sha256(staged.read_bytes()).hexdigest()
    with Path(os.environ["ROM_PROBE_TRACE"]).open("a") as handle:
        handle.write(json.dumps(event) + "\n")
os.execv(real, [real, *args])
'''


class Probe:
    """Run a fixed checkout with isolated cache/output and process injection."""

    def __init__(self, work: Path, tops: tuple[str, ...] = TOPS) -> None:
        """Prepare a private wrapper without changing any source file."""
        self.work = work
        self.tops = tops
        work.mkdir(parents=True)
        shim = work / "bin"
        shim.mkdir()
        python = shim / "python3"
        python.write_text(f"#!{sys.executable}\n" + WRAPPER, encoding="utf-8")
        python.chmod(0o755)
        self.env = dict(os.environ, PATH=f"{shim}:{os.environ['PATH']}",
                        ROM_PROBE_PYTHON=sys.executable)
        self.env.pop("ROM_PROBE_IMAGE", None)
        self.env.pop("ROM_PROBE_ACTION", None)

    def run(self, name: str, flags: list[str], mutation: tuple[str, str] = ("", "")) -> dict:
        """Run real synthesis, recording commands, exits, cells and cache causes."""
        results = self.work / name
        trace = self.work / f"{name}.trace.jsonl"
        env = dict(self.env, ROM_PROBE_IMAGE=mutation[0], ROM_PROBE_ACTION=mutation[1],
                   ROM_PROBE_TRACE=str(trace))
        command = [str(ROOT / "syn/yosys/run.sh"), "--no-structural", "--results", str(results)]
        for top in self.tops:
            command.extend(["--top", top])
        command.extend(flags)
        start = time.monotonic()
        proc = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, text=True)
        output = proc.stdout + proc.stderr
        (self.work / f"{name}.log").write_text(output, encoding="utf-8")
        rows = re.findall(r"\[PASS\]\s+(\S+)\s+cells=(\d+)([^\n]*)", output)
        receipt = dict(command=command, mutation=mutation, exit=proc.returncode,
                       seconds=round(time.monotonic() - start, 3),
                       cells={top: int(cells) for top, cells, _ in rows},
                       hits=[top for top, _, suffix in rows if "(result cache)" in suffix],
                       output=output,
                       events=[json.loads(line) for line in trace.read_text().splitlines()] if trace.exists() else [])
        (self.work / f"{name}.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
        return receipt


def cache_inputs(receipt: dict, operation: str) -> dict[str, dict[str, str]]:
    """Extract the actual cache-call identities, excluding scratch/cache paths."""
    found = {}
    for event in receipt["events"]:
        if event.get("operation") != operation:
            continue
        argv = event["args"]
        fields = dict(zip(argv[::2], argv[1::2]))
        identity = {name: fields["--" + name.replace("_", "-")]
                    for name in ("top", "mode", "program", "yosys_version", "yosys_bin_sha256",
                                 "sv2v_version", "rom_sha256")}
        identity["sv2v_sha256"] = event["sv2v_sha256"]
        found[identity["top"]] = identity
    return found


def require_live(receipt: dict, baseline: dict) -> None:
    """A miss must publish the same live result for these ROM-independent tops."""
    assert receipt["exit"] == 0 and receipt["cells"] == baseline["cells"], receipt
    assert not receipt["hits"], receipt
    assert cache_inputs(receipt, "lookup") == cache_inputs(receipt, "store"), receipt


@contextmanager
def readonly_seed(source: Path, seed: Path) -> Iterator[Path]:
    """Keep a byte-checked read-only seed, restoring write bits for cleanup."""
    shutil.copytree(source, seed)
    paths = [seed, *seed.rglob("*")]
    before = {p.relative_to(seed): p.read_bytes() for p in paths if p.is_file()}
    for path in paths:
        path.chmod(path.stat().st_mode & ~0o222)
    try:
        yield seed
        after = {p.relative_to(seed): p.read_bytes() for p in seed.rglob("*") if p.is_file()}
        assert after == before, "read-only seed bytes changed"
    finally:
        for path in paths:
            path.chmod(path.stat().st_mode | 0o200)


def bundle_changes(probe: Probe, mode: str) -> tuple[Path, dict]:
    """Every image invalidates every selected top in either mode and cache tier."""
    head = probe.work / f"{mode}-head"
    if mode == "elaborate":
        # A valid full-mode PASS must miss before this mode stores anything.
        shutil.copytree(probe.work / "full-seed", head)
    flags = ["--mode", mode, "--cache", str(head)]
    cold = probe.run(f"{mode}-cold", flags)
    require_live(cold, cold)
    assert set(cold["cells"]) == set(probe.tops), cold
    warm = probe.run(f"{mode}-warm", flags)
    assert warm["exit"] == 0 and warm["cells"] == cold["cells"], warm
    assert set(warm["hits"]) == set(probe.tops), warm
    baseline = cache_inputs(cold, "lookup")
    assert baseline and cache_inputs(warm, "lookup") == baseline
    assert all(identity["mode"] == mode for identity in baseline.values()), baseline
    with readonly_seed(head, probe.work / f"{mode}-seed") as seed:
        seed_flags = ["--mode", mode, "--cache-seed", str(seed)]
        seeded = probe.run(f"{mode}-seed-only", seed_flags)
        assert seeded["exit"] == 0 and seeded["cells"] == cold["cells"], seeded
        assert set(seeded["hits"]) == set(probe.tops), seeded
        assert not cache_inputs(seeded, "store"), seeded
        for image in IMAGES:
            name = f"{mode}-{image}"
            changed_head = probe.work / f"{name}-head"
            changed_flags = ["--mode", mode, "--cache", str(changed_head), "--cache-seed", str(seed)]
            changed = probe.run(name, changed_flags, (image, "changed"))
            require_live(changed, cold)
            actual = cache_inputs(changed, "lookup")
            for top in probe.tops:
                differences = {key for key in baseline[top] if baseline[top][key] != actual[top][key]}
                assert differences == {"rom_sha256"}, (image, differences)
            again = probe.run(name + "-warm", changed_flags, (image, "changed"))
            assert again["exit"] == 0 and again["cells"] == cold["cells"], again
            assert set(again["hits"]) == set(probe.tops), again
            # The former baseline per-head entries also cannot hit changed bytes.
            per_head = probe.run(name + "-per-head", flags, (image, "changed"))
            require_live(per_head, cold)
            assert cache_inputs(per_head, "lookup") == actual
            seed_only = probe.run(name + "-seed-only", seed_flags, (image, "changed"))
            assert seed_only["exit"] == 0 and seed_only["cells"] == cold["cells"], seed_only
            assert not seed_only["hits"] and not cache_inputs(seed_only, "store"), seed_only
            assert cache_inputs(seed_only, "lookup") == actual
    return head, cold


def invalid_generation(probe: Probe, head: Path) -> None:
    """Each failed, empty or wrong-name output refuses before any cache lookup."""
    labels = {"ltn_rom.hex": "ACMP transition-ROM", "ucode.hex": "AECP microcode",
              "gptp_ucode.hex": "gPTP microcode"}
    for image in IMAGES:
        for action in ("failed", "empty", "missing"):
            for cached in (False, True):
                flags = ["--cache", str(head)] if cached else []
                result = probe.run(f"invalid-{image}-{action}-{cached}", flags, (image, action))
                expected = (f"{labels[image]} generation failed" if action == "failed"
                            else "generated ROM is empty:")
                assert result["exit"] == 2 and expected in result["output"], result
                assert not result["hits"] and not result["cells"], result
                assert not cache_inputs(result, "lookup") and not cache_inputs(result, "store"), result


def old_and_invalid_entries(probe: Probe, head: Path, baseline: dict) -> None:
    """Real gate runs live on legacy PASS/stat pairs or invalid bundle records."""
    for mutation in ("old-key", "old-schema", "missing", "malformed", "mismatch", "duplicate"):
        planted = probe.work / f"planted-{mutation}"
        shutil.copytree(head, planted)
        for entry in planted.iterdir():
            rec = entry / cache.RECORD
            original = rec.read_text()
            fields = cache.parse_record(original)
            assert fields is not None
            rom_line = f"rom_sha256={fields['rom_sha256']}\n"
            if mutation.startswith("old-"):
                rec.write_text(original.replace(cache.SCHEMA, "milan-yosys-result-cache/1").replace(rom_line, ""))
                if mutation == "old-key":
                    text = "milan-yosys-result-cache/1\n" + "".join(
                        f"{key}={fields[key]}\n" for key in cache.INPUT_FIELDS if key != "rom_sha256")
                    entry.rename(planted / hashlib.sha256(text.encode()).hexdigest())
            else:
                replacement = {"missing": "", "malformed": "rom_sha256=bad\n",
                               "mismatch": "rom_sha256=" + "f" * 64 + "\n", "duplicate": rom_line * 2}[mutation]
                rec.write_text(original.replace(rom_line, replacement))
        result = probe.run(f"entry-{mutation}", ["--cache", str(planted)])
        require_live(result, baseline)
        if mutation != "old-key":
            assert "cache entry refused, running live" in result["output"], result


def arms(work: Path) -> None:
    """Keep the original live arms and add ROM binding/refusal controls."""
    probe = Probe(work)
    head, baseline = bundle_changes(probe, "full")
    bundle_changes(probe, "elaborate")
    invalid_generation(probe, head)
    old_and_invalid_entries(probe, probe.work / "full-seed", baseline)
    print("ROM cache controls: OK (3 images, 2 modes, 2 selected tops, head/seed, generation and schema refusals)")

"""Every harness run of checks 1-14 (and the disabled-writer and boot-walk
graders) on the given shapes, run on the round-6 harness and on the harness
of a base commit. A run whose arguments the base harness cannot take (the
round-6 --read-length and --read-verdict, or a --read-fault offset counted
from the container's end) runs on the new harness only and is counted
apart. Every other run's transcript (host addresses normalised) and every
dumped file must be equal.
Usage: harness_equivalence.py REPO BASE-COMMIT WORK JOBS SHAPE..."""
import re
import shutil
import subprocess
import sys
import threading
import time
from dataclasses import replace
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
base_commit = sys.argv[2]
work = Path(sys.argv[3]).resolve()
jobs = int(sys.argv[4])
shapes = sys.argv[5:]
sys.dont_write_bytecode = True
sys.path.insert(0, str(repo / "sw/firmware/nvm_hosttest"))
import test_nvm_firmware as t  # noqa: E402
import test_boot_walk as bootwalk  # noqa: E402
import test_disabled_writer as disabled  # noqa: E402

old_dir = work / "old-harness"
old_dir.mkdir(parents=True, exist_ok=True)
old_text = subprocess.run(["git", "-C", str(repo), "show", f"{base_commit}:sw/firmware/nvm_hosttest/nvm_host.c"],
                          capture_output=True, text=True, check=True).stdout
(old_dir / "nvm_host.c").write_text(old_text)
shutil.copytree(t.STUBS, old_dir / "stubs", dirs_exist_ok=True)
DUMPS = ("--dump-ddr", "--dump-stage", "--dump-slot-a", "--dump-slot-b")
NEW_ONLY = re.compile(r"^(--read-length|--read-verdict)$")


def norm(s: str) -> str:
    """A transcript with host addresses masked."""
    return re.sub(r"0x[0-9a-f]{6,}", "ADDR", s)


def new_only(args: tuple) -> bool:
    """Whether the base harness cannot take these arguments."""
    return any(NEW_ONLY.match(a) or (a in ("--read-fault", "--read-sealed") and args[i + 1].split(":")[1].startswith("-"))
               for i, a in enumerate(args[:-1]))


old_binary = {}
orig_run = t.run
lock = threading.Lock()
stats = {"runs": 0, "mismatch": 0, "new_only": 0}


def twin_run(bench, *args):
    """The new harness's run, checked against the base harness's."""
    if new_only(args):
        with lock:
            stats["new_only"] += 1
        return orig_run(bench, *args)
    key = bench.binary
    with lock:
        ob = old_binary.get(key)
    if ob is None:
        d = Path(str(key) + ".old")
        subprocess.run(["gcc", "-std=gnu11", "-O1", "-g", "-Wall", "-Wextra", "-Werror", f"-I{bench.work}",
                        f"-I{old_dir / 'stubs'}", f"-DNVM_HOST_JOURNAL_OFFSET=0x{t.JOURNAL:x}u",
                        f"-DNVM_HOST_AEM_OFFSET=0x{t.AEM_OFFSET:x}u", f"-DNVM_HOST_IMAGE_OFF=0x{t.IMAGE_OFF:x}u",
                        "-c", str(old_dir / "nvm_host.c"), "-o", str(d) + ".o"], check=True)
        subprocess.run(["gcc", str(d) + ".o", str(key.parent / "fw.o"), "-o", str(d)], check=True)
        with lock:
            old_binary[key] = ob = d
    r = subprocess.run([str(ob), *args], capture_output=True, text=True, cwd=bench.work, timeout=600)
    outs = [Path(args[i + 1]) if Path(args[i + 1]).is_absolute() else bench.work / args[i + 1]
            for i, a in enumerate(args[:-1]) if a in DUMPS]
    old_files = [p.read_bytes() for p in outs]
    res = orig_run(bench, *args)
    new_files = [p.read_bytes() for p in outs]
    same = r.returncode == 0 and norm(r.stdout) == norm(res[0]) and old_files == new_files
    with lock:
        stats["runs"] += 1
        if not same:
            stats["mismatch"] += 1
            if stats["mismatch"] <= 5:
                print("MISMATCH", " ".join(args)[:300], flush=True)
    return res


t.run = twin_run
t0 = time.monotonic()
findings = []
for shape in shapes:
    cfg = repo / "configs" / f"{shape}.yaml"
    w = work / shape
    w.mkdir(parents=True, exist_ok=True)
    bench = replace(t.make_bench(cfg, w, t.FIRMWARE.read_text()), jobs=jobs)
    got = t.grade(bench)
    got += disabled.grade(cfg, w / "disabled", t.FIRMWARE.read_text())
    got += bootwalk.grade(cfg, w / "boot-walk", t.FIRMWARE.read_text(), bench)
    findings += got
    print(f"{shape}: {len(got)} finding(s); twin runs so far {stats['runs']}, mismatches {stats['mismatch']}, "
          f"new-harness-only runs {stats['new_only']}", flush=True)
print(f"EQUIVALENCE: {stats['runs']} twin runs, {stats['mismatch']} mismatches, {stats['new_only']} "
      f"new-harness-only runs, {len(findings)} findings, {time.monotonic() - t0:.1f} s")
sys.exit(1 if stats["mismatch"] or findings else 0)

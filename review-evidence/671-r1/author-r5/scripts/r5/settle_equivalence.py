"""Every harness run of checks 1-14 (and the disabled-writer and boot-walk
graders) on the given shapes, run twice: once on the harness with the
word-by-word settle walk (the round-4 code) and once on the memcmp fast path.
Transcripts (host addresses normalised) and every dumped file must be equal.
Usage: settle_equivalence.py REPO WORK JOBS SHAPE..."""
import re, subprocess, sys, threading, time
from dataclasses import replace
from pathlib import Path
repo = Path(sys.argv[1]).resolve()
work = Path(sys.argv[2]).resolve()
jobs = int(sys.argv[3])
shapes = sys.argv[4:]
sys.dont_write_bytecode = True
sys.path.insert(0, str(repo / "sw/firmware/nvm_hosttest"))
import test_nvm_firmware as t
import test_boot_walk as bootwalk
import test_disabled_writer as disabled
FAST = ("\tif (memcmp(csr, shadow, sizeof(csr)) != 0)\n\t\tfor (i = 0; i < CSR_WORDS; ++i)\n"
        "\t\t\tif (csr[i] != shadow[i])\n\t\t\t\ton_store(i * 4u, csr[i]);\n")
SLOW = "\tfor (i = 0; i < CSR_WORDS; ++i)\n\t\tif (csr[i] != shadow[i])\n\t\t\ton_store(i * 4u, csr[i]);\n"
new_text = t.HARNESS.read_text()
assert new_text.count(FAST) == 1
old_dir = work / "old-harness"
old_dir.mkdir(parents=True, exist_ok=True)
(old_dir / "nvm_host.c").write_text(new_text.replace(FAST, SLOW))
import shutil
shutil.copytree(t.STUBS, old_dir / "stubs", dirs_exist_ok=True)
DUMPS = ("--dump-ddr", "--dump-stage", "--dump-slot-a", "--dump-slot-b")
norm = lambda s: re.sub(r"0x[0-9a-f]{6,}", "ADDR", s)
old_binary = {}
orig_run = t.run
lock = threading.Lock()
stats = {"runs": 0, "mismatch": 0}
def twin_run(bench, *args):
    key = bench.binary
    with lock:
        ob = old_binary.get(key)
    if ob is None:
        # the old harness, linked with the same firmware object as this bench
        d = Path(str(key) + ".old")
        subprocess.run(["gcc", "-std=gnu11", "-O1", "-g", "-Wall", "-Wextra", "-Werror", f"-I{bench.work}",
                        f"-I{old_dir / 'stubs'}", f"-DNVM_HOST_JOURNAL_OFFSET=0x{t.JOURNAL:x}u",
                        f"-DNVM_HOST_AEM_OFFSET=0x{t.AEM_OFFSET:x}u", f"-DNVM_HOST_IMAGE_OFF=0x{t.IMAGE_OFF:x}u",
                        "-c", str(old_dir / "nvm_host.c"), "-o", str(d) + ".o"], check=True)
        fwo = key.parent / "fw.o"
        subprocess.run(["gcc", str(d) + ".o", str(fwo), "-o", str(d)], check=True)
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
                print("MISMATCH", " ".join(args)[:300])
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
    print(f"{shape}: {len(got)} finding(s); runs so far {stats['runs']}, mismatches {stats['mismatch']}")
print(f"EQUIVALENCE: {stats['runs']} twin runs, {stats['mismatch']} mismatches, {len(findings)} findings, "
      f"{time.monotonic() - t0:.1f} s")
sys.exit(1 if stats["mismatch"] or findings else 0)

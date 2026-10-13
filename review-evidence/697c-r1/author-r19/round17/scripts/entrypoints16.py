"""Every entry point that pins the stack, run in a full clone whose submodule holds an edit of include/adp.h
(ADP_ADVERTISE_MS 5000u -> 9000u) that local Git state makes read as pinned (a replacement tree, a replacement
commit, a clean filter) or merely sits beside (a graft), and a mode change; each must exit non-zero naming the
changed file. Round 14 adds two states in which the edit is hidden by a forged object of the submodule's store
(its loose file overwritten with another object's bytes, every object loose): the pinned include/ tree, and the
pinned commit; each must be refused naming the forged object's place. Round 15 (entrypoints15.py): the clean
filter is refused by its key, which the stack's own configuration may not hold; and two states are added: the
submodule a partial clone whose promisor remote is reached over ssh by a recorder (core.sshCommand), the pinned
include/ tree's object missing, refused naming the keys with the recorder never run; and include/adp.h's line endings
made CRLF under a text attribute, which Git would convert back into the pinned blob, refused naming the file.
Round 16 (entrypoints16.py) adds a state of the superproject's own configuration: the clone a partial clone whose
promisor remote is reached over ssh by a recorder (core.sshCommand), refused naming the keys before the gitlink is
read, the recorder never run.
usage: python3 -B entrypoints16.py <full clone> <work>"""
import os, subprocess, sys, shutil
from pathlib import Path
clone, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sub = clone / "third_party/tsn-c-stack"
work.mkdir(parents=True, exist_ok=True)
REAL = {**os.environ, "GIT_NO_REPLACE_OBJECTS": "1", "GIT_GRAFT_FILE": "/dev/null/none"}
def g(*args, stdin=None, env=REAL):
    r = subprocess.run(["git", "-C", str(sub), *args], input=stdin, capture_output=True, text=True, env=env)
    if r.returncode:
        raise SystemExit(f"setup failed: git {' '.join(args)}: {r.stderr}")
    return r.stdout
assert Path(g("rev-parse", "--show-toplevel").strip()) == sub
pin = subprocess.run(["git", "-C", str(clone), "ls-files", "--stage", "--", "third_party/tsn-c-stack"],
                     capture_output=True, text=True).stdout.split()[1]
gitdir = Path(g("rev-parse", "--absolute-git-dir").strip())
CONFIG = (gitdir / "config").read_bytes()
RECORDER = work / "recorder"
RECORDER.write_text(f'#!/bin/sh\necho "$0 $*" >> {work}/ran\nexit 1\n')
RECORDER.chmod(0o755)
UNLISTED = "outside the pin proof's allowlist: "
SUPER = "has Git start a program or fetch while the gitlink is read: "
SUPERCONFIG = (clone / ".git/config").read_bytes()
OLD, NEW = b"#define ADP_ADVERTISE_MS 5000u", b"#define ADP_ADVERTISE_MS 9000u"

def edit():
    h = sub / "include/adp.h"
    data = h.read_bytes(); assert data.count(OLD) == 1
    h.write_bytes(data.replace(OLD, NEW))

def remade(tree, name, oid):
    out = []
    for e in filter(None, g("ls-tree", "-z", tree).split("\0")):
        meta, n = e.split("\t", 1); mode, kind, _ = meta.split()
        out.append(f"{mode} {kind} {oid}\t{n}" if n == name else e)
    return g("mktree", "-z", stdin="\0".join(out) + "\0").strip()

def subs():
    edit()
    blob = g("hash-object", "-w", "--no-filters", "include/adp.h").strip()
    inc = g("rev-parse", f"{pin}:include").strip()
    new_inc = remade(inc, "adp.h", blob)
    return inc, new_inc, remade(g("rev-parse", f"{pin}^{{tree}}").strip(), "include", new_inc)

def replacement_tree():
    inc, new_inc, _ = subs(); g("replace", inc, new_inc)

def replacement_commit():
    _, _, root = subs()
    old = g("rev-parse", f"{pin}^{{tree}}").strip()
    c = g("hash-object", "-t", "commit", "-w", "--stdin", stdin=g("cat-file", "commit", pin).replace(old, root, 1)).strip()
    g("replace", pin, c)

def graft():
    edit(); (gitdir / "info").mkdir(exist_ok=True); (gitdir / "info/grafts").write_text(f"{pin}\n")

def clean_filter():
    edit()
    g("config", "filter.pc.clean", "sed 's/ADP_ADVERTISE_MS 9000u/ADP_ADVERTISE_MS 5000u/'")
    (gitdir / "info").mkdir(exist_ok=True); (gitdir / "info/attributes").write_text("include/adp.h filter=pc\n")
    assert g("hash-object", "include/adp.h").strip() == g("rev-parse", f"{pin}:include/adp.h").strip()

LOOSE = {}


def loosen():
    """Every object of the submodule's store loose: each pack unpacked, then removed (once)."""
    for pack in sorted((gitdir / "objects/pack").glob("*.pack")):
        moved = work / pack.name
        shutil.move(pack, moved)
        for other in pack.parent.glob(pack.stem + ".*"):
            other.unlink()
        subprocess.run(["git", "-C", str(sub), "unpack-objects", "-q"], input=moved.read_bytes(), env=REAL, check=True)
        moved.unlink()


def loose(oid):
    return gitdir / "objects" / oid[:2] / oid[2:]


def replaced(path, data):
    """`path` replaced by a new file holding `data`: a loose file a hard link shares with another store (a local
    clone's) is never written."""
    new = path.with_name(path.name + ".new")
    new.write_bytes(data)
    new.chmod(0o444)
    new.replace(path)


def forge(victim, source):
    path = loose(victim)
    LOOSE.setdefault(victim, path.read_bytes())
    replaced(path, loose(source).read_bytes())


def forged_tree():
    inc, new_inc, _ = subs(); forge(inc, new_inc)


def forged_commit():
    _, _, root = subs()
    old = g("rev-parse", f"{pin}^{{tree}}").strip()
    forge(pin, g("hash-object", "-t", "commit", "-w", "--stdin", stdin=g("cat-file", "commit", pin).replace(old, root, 1)).strip())


def lazy_transport():
    inc = g("rev-parse", f"{pin}:include").strip()
    path = loose(inc)
    LOOSE.setdefault(inc, path.read_bytes())
    path.unlink()
    for key, value in (("core.repositoryformatversion", "1"), ("extensions.partialClone", "probe"),
                       ("remote.probe.url", "ssh://probe.invalid/stack"), ("remote.probe.promisor", "true"),
                       ("core.sshCommand", str(RECORDER))):
        g("config", key, value)


def converted():
    h = sub / "include/adp.h"
    data = h.read_bytes(); assert b"\r" not in data
    h.write_bytes(data.replace(b"\n", b"\r\n"))
    (gitdir / "info").mkdir(exist_ok=True); (gitdir / "info/attributes").write_text("include/adp.h text\n")
    assert g("hash-object", "include/adp.h").strip() == g("rev-parse", f"{pin}:include/adp.h").strip()


def super_lazy():
    for key, value in (("core.repositoryformatversion", "1"), ("extensions.partialClone", "probe"),
                       ("remote.probe.url", "ssh://probe.invalid/superproject"), ("remote.probe.promisor", "true"),
                       ("core.sshCommand", str(RECORDER))):
        subprocess.run(["git", "-C", str(clone), "config", key, value], check=True, env=REAL)


def mode_change():
    s = sub / "scripts/check_boundary.py"; s.chmod(s.stat().st_mode | 0o100)

def restore():
    for victim, data in LOOSE.items():
        replaced(loose(victim), data)
    LOOSE.clear()
    for ref in g("for-each-ref", "--format=%(refname)", "refs/replace").split():
        g("update-ref", "-d", ref)
    for f in ("info/grafts", "info/attributes"):
        (gitdir / f).unlink(missing_ok=True)
    new = gitdir / "config.restored"
    new.write_bytes(CONFIG)
    new.replace(gitdir / "config")
    new = clone / ".git/config.restored"
    new.write_bytes(SUPERCONFIG)
    new.replace(clone / ".git/config")
    (sub / "scripts/check_boundary.py").chmod(0o644)
    g("checkout", "-f", "--quiet", pin, "--", ".")
    r = subprocess.run([sys.executable, "-B", str(clone / "sw/firmware/ctrl/test/ctrl_build.py"), "--stack-pin"],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stdout

nosim = work / "no_simulator.py"
nosim.write_text('import sys\nfrom pathlib import Path\nargs = sys.argv[1:]\nif "--Mdir" in args and "-o" in args:\n'
                 '    exe = Path(args[args.index("--Mdir") + 1]) / args[args.index("-o") + 1]\n'
                 '    exe.parent.mkdir(parents=True, exist_ok=True)\n'
                 '    exe.write_text("#!/bin/sh\\nexit 0\\n")\n    exe.chmod(0o755)\n')
T = clone / "sw/firmware/ctrl/test"
py = [sys.executable, "-B"]
cfg = clone / "configs/endstation_ax7101_1x1_tdm8.yaml"
rt = Path("$VALIDATION_STORAGE/697c-a583/runtime")
entries = [
    ("ctrl_build.py --stack-pin (the Makefile's pin check)", py + [str(T / "ctrl_build.py"), "--stack-pin"]),
    ("test_ctrl_firmware.py --build-only", py + [str(T / "test_ctrl_firmware.py"), "--require-rv32", "--build-only", "--jobs", "4"]),
    ("test_ctrl_firmware.py --self-test", py + [str(T / "test_ctrl_firmware.py"), "--require-rv32", "--self-test", "--jobs", "4"]),
    ("fw_coverage.py --check", py + [str(clone / "sw/firmware/gtest/fw_coverage.py"), "--check", "--jobs", "4"]),
    ("ctrl_image.py", py + [str(T / "ctrl_image.py"), "--shape", "endstation_ax7101_1x1_tdm8", "--out", str(work / "img")]),
    ("ctrl_srp_image.py", py + [str(T / "ctrl_srp_image.py"), "--config", str(cfg), "--interfaces", "1", "--output",
                                str(work / "srp"), "--libc", str(rt / "libc.a"), "--compiler-runtime", str(rt / "libcompiler_rt.a")]),
    ("ctrl_boundary.py --without verilator", py + [str(T / "ctrl_boundary.py"), "--require-rv32", "--without", "verilator"]),
    ("maap_differential.py", py + [str(T / "maap_differential.py")]),
    ("maap_differential.py --self-test", py + [str(T / "maap_differential.py"), "--self-test"]),
    ("aecp_arms.py --app", py + [str(T / "aecp_arms.py"), "--app", "--output", str(work / "aecp")]),
    ("aecp_mutants.py --shard 0 1000", py + [str(T / "aecp_mutants.py"), "--shard", "0", "1000", "--output", str(work / "aecp")]),
    ("aecp_wire.py", py + [str(T / "aecp_wire.py"), "--reference", str(clone / "protocol-processor"), "--verilator", "false",
                           "--output", str(work / "aecp")]),
] + [(f"make -C tb/verilator/mbx {t}".strip(), ["make", "--no-print-directory", "-C", str(clone / "tb/verilator/mbx"),
      f"VERILATOR={sys.executable} -I {nosim}", *([t] if t else [])])
     for t in ("stack-pin", "obj_fw/libctrlfw.a", "run-cosim", "run-if2", "")]
states = [("a replacement tree", replacement_tree, "include/adp.h"),
          ("a replacement commit for the pin", replacement_commit, "include/adp.h"),
          ("a graft file", graft, "include/adp.h"),
          ("a clean filter through attributes", clean_filter, UNLISTED + "filter.pc.clean (local)"),
          ("a line-ending conversion through attributes (round 15)", converted, "include/adp.h"),
          ("a mode change", mode_change, "scripts/check_boundary.py"),
          ("a forged include/ tree object (round 14)", forged_tree, "forged or corrupt object: the pinned include/ tree"),
          ("a forged pinned commit object (round 14)", forged_commit, "forged or corrupt object: the pinned commit"),
          ("a partial clone over an ssh program, the include/ tree missing (round 15)", lazy_transport,
           UNLISTED + "core.sshcommand (local), extensions.partialclone (local), remote.probe.promisor (local)"),
          ("the superproject a partial clone over an ssh program (round 16)", super_lazy,
           SUPER + "core.sshcommand (local), extensions.partialclone (local), remote.probe.promisor (local)")]
loosen()
print(f"submodule store: {len(list((gitdir / 'objects/pack').glob('*.pack')))} packs after unpacking", flush=True)
env = {**os.environ, "VERILATOR": "false"}
bad = 0
for state, plant, needle in states:
    restore(); plant()
    print(f"== {state} (HEAD {g('rev-parse', 'HEAD').strip()[:8]}, replace refs: "
          f"{len(g('for-each-ref', 'refs/replace').split())//3})", flush=True)
    for what, argv in entries:
        try:
            r = subprocess.run(argv, cwd=clone, capture_output=True, text=True, env=env, timeout=600)
            out, rc = r.stdout + r.stderr, r.returncode
        except subprocess.TimeoutExpired:
            out, rc = "timed out", 124
        said = [ln.strip() for ln in out.splitlines() if "differs from the pinned" in ln or "forged or corrupt object" in ln
                or UNLISTED in ln or SUPER in ln]
        ran = (work / "ran").read_text().splitlines() if (work / "ran").exists() else []
        (work / "ran").unlink(missing_ok=True)
        ok = rc != 0 and any(needle in ln for ln in said) and not ran
        if ran:
            said.append(f"a program the configuration names ran {len(ran)} times: {ran[0]}")
        bad += not ok
        print(f"  [{'REFUSED' if ok else 'NOT REFUSED'}] {what}: exit {rc}: {(said[-1] if said else out.strip().splitlines()[-1] if out.strip() else '')[:160]}", flush=True)
restore()
print(f"entry points: {len(entries)} x {len(states)} states, {bad} not refused")
sys.exit(1 if bad else 0)

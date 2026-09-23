#!/usr/bin/env python3
"""Reviewer probe: literal Git filename and patch bytes under real locales.

Independent of the self-test's own fixtures.  Every environment runs in a
fresh Python process whose filesystem codec is verified, builds its fixture
repositories with raw plumbing (bytes argv, mktree -z), and drives the
checker CLI in a further fresh process through a real stdout pipe (no
PYTHONIOENCODING).  Non-injective codecs: big5, big5hkscs, johab, cp932.

    probe_codec.py --driver <label> <checker-src-dir> <locale-dir> <out.json>
    probe_codec.py --child <checker-src-dir> <expected-codec> <workdir>

Exit status of the driver is 0 when it ran; the verdict table is the result.
"""
import codecs
import json
import os
import subprocess
import sys
from pathlib import Path

#! (name, alias): alias is what a lossy transport would address instead.
PAIRS = (
    (b"\xa1\xfe.txt", b"\xa2\x41.txt"),   # big5 / big5hkscs: a1fe -> a241
    (b"\x84\x41.txt", b"\xd9\x31.txt"),   # johab: 8441 -> d931
    (b"\x87\x90.txt", b"\x81\xe0.txt"),   # cp932: 8790 -> 81e0
    (b"\xc3\xa9.txt", b"\xe9.txt"),       # utf-8 read as latin-1: c3a9 -> e9
    (b"raw-\xff.txt", None),              # undecodable in utf-8
)
ALIASES = [alias for _, alias in PAIRS if alias]
OLD = b"".join(b"line %02d\n" % i for i in range(1, 41))
CHANGED = OLD.replace(b"line 05\n", b"source 05\n")
CTL_C = OLD.replace(b"line 10\n", b"C edit 10\n")
CTL_LATER = CTL_C.replace(b"line 35\n", b"later 35\n")
BLOCK = b"a\nb\nc\nold\nd\ne\nf\n"
SEP = b"".join(b"separator-%d\n" % i for i in range(10))
REP = BLOCK + SEP + BLOCK
REP_FIRST = REP.replace(b"old", b"new", 1)
REP_SECOND = BLOCK + SEP + BLOCK.replace(b"old", b"new")


def raw(*args, data=None):
    p = subprocess.run(("git", "--no-replace-objects", *args), input=data,
                       capture_output=True)
    if p.returncode:
        raise RuntimeError(f"fixture git {args!r}: {p.stderr!r}")
    return p.stdout


def blob(data):
    return raw("hash-object", "-w", "--stdin", data=data).strip()


def tree(entries):
    recs = b"".join(b"100644 blob " + blob(data) + b"\t" + name + b"\0"
                    for name, data in sorted(entries.items()))
    return raw("mktree", "-z", data=recs).strip().decode("ascii")


def commit(tree_oid, parents, msg):
    args = ["commit-tree", tree_oid, "-m", msg]
    for p in parents:
        args += ["-p", p]
    return raw(*args).strip().decode("ascii")


def ref(name, oid):
    raw("update-ref", "refs/heads/" + name, oid)


def label(name):
    return repr(name)[1:]


def cli(checker, env, *refs):
    p = subprocess.run((sys.executable, "-B", str(checker), "--no-fetch",
                        "--base", "main", *refs), env=env, capture_output=True)
    return p.returncode, p.stdout, p.stderr


def first_word(out):
    lines = [ln for ln in out.splitlines() if ln.strip()]
    return lines[0].split()[0].decode("ascii", "replace") if lines else "none"


def child(src, expected, workdir):
    rows = []

    def row(name, got, want):
        rows.append([name, got, want, got == want])

    fs = codecs.lookup(sys.getfilesystemencoding()).name
    row("fs-encoding", fs, expected)
    if fs != expected:
        return rows
    env = {k: v for k, v in os.environ.items() if k != "PYTHONIOENCODING"}
    stream = subprocess.run((sys.executable, "-c", "import sys,codecs;print("
                             "codecs.lookup(sys.stdout.encoding).name,"
                             "sys.stdout.errors)"), env=env,
                            capture_output=True).stdout.decode().split()
    rows.append(["stdout-stream", stream, None, True])
    checker = Path(src) / "check_merge_containment.py"
    os.chdir(workdir)
    raw("init", "-q", "-b", "main")
    raw("config", "user.name", "Probe")
    raw("config", "user.email", "probe@example.invalid")
    raw("config", "commit.gpgsign", "false")
    sys.path.insert(0, str(src))
    import check_merge_containment as mc

    for name, _alias in PAIRS:
        tag = name.hex()
        base_entries = {alias: b"unchanged alias\n" for alias in ALIASES}

        def t(content, ctl, extra=None):
            return tree({**base_entries, name: content, b"ctl": ctl,
                         **(extra or {})})
        o = commit(t(OLD, OLD), [], "O")
        # 1/2: linear branch, never-landed versus landed edit of `name`
        lin = commit(t(CHANGED, OLD), [o], "L edits name")
        ref("pr", lin)
        ref("main", commit(t(OLD, CTL_LATER), [o], "unrelated"))
        rc, out, err = cli(checker, env, "pr")
        row(tag + "-linear-missing", [rc, first_word(out)], [1, "STRANDED"])
        ref("main", commit(t(CHANGED, CTL_LATER), [o], "landed"))
        rc, out, err = cli(checker, env, "pr")
        row(tag + "-linear-retained", [rc, first_word(out)], [0, "contained"])
        # 3/4: redundant merge, exact replay, tip reverts / retains `name`
        a = commit(t(CHANGED, OLD), [o], "A")
        m = commit(t(CHANGED, OLD), [o, a], "M redundant")
        c = commit(t(CHANGED, CTL_C), [m], "C")
        ra = commit(t(CHANGED, OLD), [o], "A'")
        rcm = commit(t(CHANGED, CTL_C), [ra], "C'")
        ref("pr", c)
        ref("main", commit(t(OLD, CTL_LATER), [rcm], "revert name + far edit"))
        rc, out, err = cli(checker, env, "pr")
        row(tag + "-merge-reverted", [rc, first_word(out)], [1, "UNKNOWN"])
        row(tag + "-merge-reverted-label", label(name).encode() in out, True)
        ref("main", commit(t(CHANGED, CTL_LATER), [rcm], "far edit"))
        rc, out, err = cli(checker, env, "pr")
        row(tag + "-merge-retained", [rc, first_word(out)], [0, "contained"])
        row(tag + "-merge-retained-proof", b"raw no-op retention" in out, True)
        # 5: same verbatim patch at another repeated block: postimage differs
        o2 = commit(t(REP, OLD), [], "O2")
        ref("pr", commit(t(REP_FIRST, OLD), [o2], "first block"))
        rep = commit(t(REP_SECOND, OLD), [o2], "second block")
        ref("main", commit(t(REP_SECOND, CTL_LATER), [rep], "far edit"))
        rc, out, err = cli(checker, env, "pr")
        row(tag + "-repeated-block", [rc, first_word(out)], [1, "STRANDED"])
        row(tag + "-repeated-block-label", label(name).encode() in out, True)

    # 6: patch transport: content differing only by a lossy pair must keep
    # distinct verbatim patch IDs, equal to an independent raw computation.
    o3 = commit(tree({b"content": OLD}), [], "O3")
    for name, alias in PAIRS:
        if not alias:
            continue
        stem = name.rsplit(b".", 1)[0]
        alt = alias.rsplit(b".", 1)[0]
        p1 = commit(tree({b"content": OLD.replace(b"line 07", stem)}), [o3], "p1")
        p2 = commit(tree({b"content": OLD.replace(b"line 07", alt)}), [o3], "p2")
        ids = []
        for cm in (p1, p2):
            got, err = mc._verbatim_patch_id(cm)
            patch = raw("show", *mc.RAW_DIFF_FLAGS, "--format=medium",
                        "--binary", "--full-index", "--no-renames",
                        cm).rstrip(b"\n")
            want = raw("patch-id", "--verbatim", data=patch).split()[0].decode()
            row(stem.hex() + "-patch-id-" + cm[:8], [got, err], [want, None])
            ids.append(got)
        row(stem.hex() + "-patch-ids-distinct", ids[0] != ids[1], True)

    # 7: three targets through a real stdout; stranded note names every file
    names = [n for n, _ in PAIRS]
    o4 = commit(tree({**{n: OLD for n in names}, b"ctl": OLD}), [], "O4")
    ref("aa-ok", o4)
    ref("zz-ok", o4)
    ref("pr", commit(tree({**{n: CHANGED for n in names}, b"ctl": OLD}), [o4], "s"))
    ref("main", commit(tree({**{n: OLD for n in names}, b"ctl": CTL_LATER}),
                       [o4], "unrelated"))
    rc, out, err = cli(checker, env, "aa-ok", "pr", "zz-ok")
    lines = [ln for ln in out.splitlines() if ln.strip()]
    row("report-verdicts", [rc, [ln.split()[0].decode("ascii", "replace")
                                 for ln in lines[:3]], err.decode("ascii", "replace")],
        [1, ["contained", "STRANDED", "contained"], ""])
    row("report-ascii", out.isascii(), True)
    row("report-labels", [label(n).encode() in out for n in names],
        [True] * len(names))
    return rows


ENVS = (
    # label, expected fs codec, env overrides (LOCPATH added when needed)
    ("utf-8-locale", "utf-8", {"LC_ALL": "en_US.UTF-8", "PYTHONUTF8": "0"}, False),
    ("utf-8-mode", "utf-8", {"LC_ALL": "C", "PYTHONUTF8": "1"}, False),
    ("ascii", "ascii", {"LC_ALL": "C", "PYTHONUTF8": "0"}, False),
    ("latin-1", "iso8859-1", {"LC_ALL": "en_US.ISO-8859-1", "PYTHONUTF8": "0"}, True),
    ("big5", "big5", {"LC_ALL": "zh_TW.BIG5", "PYTHONUTF8": "0"}, True),
    ("big5hkscs", "big5hkscs", {"LC_ALL": "zh_HK.BIG5-HKSCS", "PYTHONUTF8": "0"}, True),
    ("johab", "johab", {"LC_ALL": "ko_KR.JOHAB", "PYTHONUTF8": "0"}, True),
    ("cp932", "cp932", {"LC_ALL": "ja_JP.WINDOWS-31J", "PYTHONUTF8": "0"}, True),
)


def driver(label_, src, locales, out_json):
    results = {}
    #! Fixture repositories are disposable; keep them out of the receipts.
    scratch = Path(os.environ.get("PROBE_SCRATCH", Path(out_json).parent)) / (
        Path(out_json).stem + ".work")
    scratch.mkdir(parents=True, exist_ok=True)
    for env_label, expected, overrides, needs_locpath in ENVS:
        env = {k: v for k, v in os.environ.items()
               if not k.startswith(("LC_", "PYTHON")) and k not in ("LANG", "LOCPATH")}
        env.update(overrides, PYTHONCOERCECLOCALE="0", PYTHONDONTWRITEBYTECODE="1",
                   GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
        if needs_locpath:
            env["LOCPATH"] = str(locales)
        work = scratch / env_label
        work.mkdir()
        p = subprocess.run((sys.executable, "-B", str(Path(__file__).resolve()),
                            "--child", str(src), expected, str(work)),
                           env=env, capture_output=True)
        try:
            rows = json.loads(p.stdout.decode("ascii"))
        except ValueError:
            rows = [["child-crash", p.returncode, 0, False,
                     p.stderr.decode("ascii", "backslashreplace")[-2000:]]]
        results[env_label] = rows
    json.dump({"source": label_, "results": results}, open(out_json, "w"),
              indent=1, ensure_ascii=True)
    for env_label, rows in results.items():
        bad = [r for r in rows if not r[3]]
        print(f"{label_:10} {env_label:13} rows={len(rows):3} mismatches={len(bad)}")
        for r in bad:
            print(f"    MISMATCH {r[0]}: got={r[1]!r} want={r[2]!r}")


if __name__ == "__main__":
    if sys.argv[1] == "--child":
        print(json.dumps(child(Path(sys.argv[2]), sys.argv[3], sys.argv[4]),
                         ensure_ascii=True))
    elif sys.argv[1] == "--driver":
        driver(sys.argv[2], Path(sys.argv[3]).resolve(), Path(sys.argv[4]).resolve(),
               sys.argv[5])
    else:
        raise SystemExit(__doc__)

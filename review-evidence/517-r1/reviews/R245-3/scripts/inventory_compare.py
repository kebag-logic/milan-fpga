#!/usr/bin/env python3
"""Compare the milan_dp default `run` executions: base sequential vs head pooled.

usage: inventory_compare.py BASE_TREE HEAD_TREE
Uses `make -n run` in each tree (clean environment, pinned wrapper not needed
for a dry run). Every executed command line is classified; ordinary legs of the
head are read from the sim_pool argv. The script prints both ordered lists and
fails unless the executed set, order, argv and banners match exactly, every
non-ordinary command is identical, and no ordinary executable runs twice.
"""
import os, re, shlex, subprocess, sys

def dry(tree, *extra):
    env = {k: v for k, v in os.environ.items() if k not in ("MAKEFLAGS", "MFLAGS", "MAKELEVEL", "MILAN_COUNTER_FRAME_OUT")}
    r = subprocess.run(["make", "-n", "-C", f"{tree}/tb/verilator/milan_dp", "run", *extra],
                       capture_output=True, text=True, env=env)
    assert r.returncode == 0, r.stderr
    return r.stdout.replace(os.path.realpath(tree), "<TREE>").replace("\\\n", " ").splitlines()

# ordinary legs; the gPTP prerequisite runs (obj_gptp, obj_gptplat, obj_gmstep)
# stay direct recipe lines by the issue's settled scope and are compared as
# ordinary non-pool commands
LEG = re.compile(r"^\./(?!obj_gptp/|obj_gptplat/|obj_gmstep/)[A-Za-z0-9_]+/Vmilan_dp_[a-z0-9]+(\s.*)?$")

def base_view(lines):
    ordinary, other, banner = [], [], None
    for line in lines:
        m = re.match(r"^echo \"(---- .* ----)\"$", line)
        if m:
            banner = m.group(1); other.append(line); continue
        if LEG.match(line):
            ordinary.append((banner, line)); banner = None; continue
        other.append(line)
    return ordinary, other

def head_view(lines):
    ordinary, other = [], []
    runner = [l for l in lines if "sim_pool.py" in l]
    assert len(runner) == 1, runner
    for line in lines:
        if "sim_pool.py" in line:
            words = shlex.split(line)
            assert words[:3] == ["exec", "python3", "sim_pool.py"], words
            banner, excl = None, False
            for w in words[4:] if words[3].startswith("--jobs=") else words[3:]:
                pass
            it = iter(words[3:])
            for w in it:
                if w.startswith("--jobs="): continue
                if w == "--banner": banner = next(it); continue
                if w == "--exclusive": excl = True; continue
                ordinary.append((banner, w, excl)); banner, excl = None, False
            other.append("<sim_pool>")
            continue
        if LEG.match(line):
            ordinary.append((None, line, None)); other.append(line); continue
        other.append(line)
    return ordinary, other

def main():
    base, head = sys.argv[1], sys.argv[2]
    ok = True
    for extra in ([], ["SIM_JOBS=1"], ["NOTIFY_MDIR=obj_notify_x", "CRFLIC_MDIR=obj_crflic_x"]):
        b_ord, b_other = base_view(dry(base, *extra))
        h_ord, h_other = head_view(dry(head, *extra))
        print(f"== variant {extra or ['default']}")
        print(f"base sequential ordinary legs: {len(b_ord)}")
        for i, (bn, exe) in enumerate(b_ord, 1): print(f"  B{i:02d} {exe}   banner={bn!r}")
        print(f"head ordinary legs (pool argv + any stray direct leg): {len(h_ord)}")
        for i, (bn, exe, ex) in enumerate(h_ord, 1): print(f"  H{i:02d} {exe}   exclusive={ex} banner={bn!r}")
        pooled = [(bn, exe) for bn, exe, ex in h_ord if ex is not None]
        stray = [exe for bn, exe, ex in h_ord if ex is None]
        # base banners: an echo immediately before a leg; head: --banner
        same = [exe for _, exe in b_ord] == [exe for _, exe in pooled]
        same_banners = [bn for bn, _ in b_ord] == [bn for bn, _ in pooled]
        dup = len({exe for _, exe, _ in h_ord}) != len(h_ord)
        excl = sorted(exe for bn, exe, ex in h_ord if ex)
        # non-ordinary: the base's leg banner echo lines are the only lines replaced
        b_rest = [l for l in b_other if not re.match(r'^echo "---- .* ----"$', l) or l not in [f'echo "{bn}"' for bn, _ in b_ord]]
        h_rest = h_other
        bi = b_rest.index(next(l for l in b_rest if "#386 render law" in l))
        hi = h_rest.index("<sim_pool>")
        pre_same = b_rest[:bi] == [l for l in h_rest[:hi]]
        post_same = b_rest[bi:] == h_rest[hi + 1:]
        print(f"same executables in same order: {same}; same banners: {same_banners}; "
              f"stray direct ordinary legs in head: {stray}; duplicate: {dup}")
        print(f"exclusive members: {excl}")
        print(f"non-ordinary commands before pool identical: {pre_same} ({len(b_rest[:bi])} lines); "
              f"after pool identical: {post_same} ({len(b_rest[bi:])} lines)")
        if not pre_same:
            import difflib
            print("\n".join(l[:200] for l in difflib.unified_diff(b_rest[:bi], h_rest[:hi], lineterm="", n=0)))
        ok &= same and same_banners and not stray and not dup and pre_same and post_same
    print("INVENTORY", "MATCH" if ok else "MISMATCH")
    return 0 if ok else 1

sys.exit(main())

import pathlib, re, shutil, subprocess, sys
src = pathlib.Path("scripts/check_baremetal_only.py").read_text()
T_OLD = '    "scripts/act_ci.py": ACT_SLOT_TERM_MASK,\n'
R_OLD = ("    \"scripts/act_ci.py\": re.compile(\n"
         "        r'(?<=Path\\(\")/proc(?=\"\\))'\n"
         "        r'|(?<=^CGROUP_ROOT = pathlib\\.Path\\(\")/sys(?=/fs/cgroup\"\\)$)'),\n")
assert src.count(T_OLD) == 1 and src.count(R_OLD) == 1
mutants = {
    "T-removed": (T_OLD, ""),
    "T-context-free": (T_OLD, '    "scripts/act_ci.py": re.compile(r"systemd-run|native\\.cgroupdriver=systemd"),\n'),
    "T-whole-line": (T_OLD, '    "scripts/act_ci.py": re.compile(r"^.*(?:systemd-run|cgroupdriver=systemd).*$"),\n'),
    "T-no-end-guard": (T_OLD, '    "scripts/act_ci.py": re.compile(ACT_SLOT_TERM_MASK.pattern.replace("$", "")),\n'),
    "T-no-start-guard": (T_OLD, '    "scripts/act_ci.py": re.compile(ACT_SLOT_TERM_MASK.pattern.replace("(?<=^", "(?<=")),\n'),
    "R-no-dollar": (R_OLD, R_OLD.replace('cgroup"\\)$)', 'cgroup"\\))')),
    "R-no-caret": (R_OLD, R_OLD.replace("(?<=^CGROUP", "(?<=CGROUP")),
    "T-unpinned": ("        term_mask = TERM_MASKS.get(path)\n",
                   "        term_mask = TERM_MASKS.get(path, ACT_SLOT_TERM_MASK)\n"),
    "R-removed": (R_OLD, "    \"scripts/act_ci.py\": re.compile(r'(?<=Path\\(\")/proc(?=\"\\))'),\n"),
    "R-context-free": (R_OLD, "    \"scripts/act_ci.py\": re.compile(r'(?<=Path\\(\")/proc(?=\"\\))|/sys(?=/fs/cgroup)'),\n"),
    "R-no-end-guard": (R_OLD, "    \"scripts/act_ci.py\": re.compile(r'(?<=Path\\(\")/proc(?=\"\\))|(?<=^CGROUP_ROOT = pathlib\\.Path\\(\")/sys(?=/fs/cgroup)'),\n"),
    "R-unpinned": ("        runtime_mask = HOST_RUNTIME_MASKS.get(path)\n",
                   "        runtime_mask = HOST_RUNTIME_MASKS.get(path, HOST_RUNTIME_MASKS['scripts/act_ci.py'])\n"),
}
for name, (old, new) in mutants.items():
    assert src.count(old) == 1 and old != new, name
    d = pathlib.Path("/tmp/a208-mut") / name / "scripts"
    d.mkdir(parents=True, exist_ok=True)
    (d / "check_baremetal_only.py").write_text(src.replace(old, new))
    out = subprocess.run([sys.executable, str(d / "check_baremetal_only.py"), "--selftest"],
                         capture_output=True, text=True)
    failed = sorted(set(re.findall(r"\[(act-slot-[^\]]+)\]", out.stdout + out.stderr)))
    others = sorted(set(re.findall(r"^\s*-?\s*\[([^\]]+)\]", out.stdout + out.stderr, re.M)) - set(failed))
    print(f"{name}: rc={out.returncode} act-slot arms failed={len(failed)}")
    for f in failed:
        print("   ", f)
    if others:
        print("    other failing arms:", others[:8])

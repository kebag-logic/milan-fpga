#!/usr/bin/env python3
"""Reviewer probe: the real mutation driver under caller Git environment variables.

Usage: probe_gitenv.py SOURCE_CLONE WORKDIR RECEIPT.json
A disposable copy of SOURCE_CLONE gets a committed Makefile whose `run` recipe
returns at once with a named failing tally (so every control is graded in
seconds); every campaign input is still verified and copied by the real
driver. Each arm sets caller variables and records ACCEPTED (the campaign
graded all nine controls), or REFUSED with the named reason. Caller tracked
state is compared before/after every arm.
"""
import json, os, shutil, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from probe_campaign import integrity  # noqa: E402

SOURCE = Path(sys.argv[1]).resolve()
WORK = Path(sys.argv[2]).resolve()
RECEIPT = Path(sys.argv[3]).resolve()


def main():
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    repo = WORK / "repo"
    shutil.copytree(SOURCE, repo, symlinks=True)
    mk = repo / "tb/verilator/gptp_shadow/Makefile"
    text = mk.read_text()
    old = "run: gptp_ucode.hex\n\t$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vgptp_shadow_sim\n\t./obj_dir/Vgptp_shadow_sim\n"
    assert old in text
    mk.write_text(text.replace(old, "run:\n\t@echo 'FAIL stand-in got 0 exp 1'\n\t@echo '1 checks: 0 PASS, 1 FAIL'\n\t@exit 1\n"))
    clean = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    subprocess.run(["git", "-C", str(repo), "-c", "user.name=Reviewer probe", "-c", "user.email=probe@example.invalid",
                    "commit", "-qam", "reviewer disposable fast run"], env=clean, check=True)
    exec_path = subprocess.run(["git", "--exec-path"], capture_output=True, text=True, env=clean).stdout.strip()
    gitdir = str(repo / ".git")
    arms = {
        "none": {},
        "bisect-run-like": dict(GIT_EXEC_PATH=exec_path, GIT_PREFIX="", GIT_EDITOR=":"),
        "rebase-x-like": dict(GIT_EXEC_PATH=exec_path, GIT_PREFIX="", GIT_EDITOR=":", GIT_SEQUENCE_EDITOR=":"),
        "author-identity": dict(GIT_AUTHOR_NAME="A", GIT_AUTHOR_EMAIL="a@e.invalid", GIT_AUTHOR_DATE="@0 +0000",
                                GIT_COMMITTER_NAME="C", GIT_COMMITTER_EMAIL="c@e.invalid"),
        "trace-to-stderr": dict(GIT_TRACE="1", GIT_TRACE_SETUP="1", GIT_TRACE_PERFORMANCE="1"),
        "trace2-file": dict(GIT_TRACE2_EVENT=str(WORK / "trace2.json")),
        "ceiling-above-repo": dict(GIT_CEILING_DIRECTORIES=str(repo.parent)),
        "no-cross-fs": dict(GIT_DISCOVERY_ACROSS_FILESYSTEM="0"),
        "pathspec-glob": dict(GIT_GLOB_PATHSPECS="1"),
        "pathspec-icase": dict(GIT_ICASE_PATHSPECS="1"),
        "pathspec-noglob": dict(GIT_NOGLOB_PATHSPECS="1"),
        "optional-locks-off": dict(GIT_OPTIONAL_LOCKS="0"),
        "no-replace-objects": dict(GIT_NO_REPLACE_OBJECTS="1"),
        "config-nosystem": dict(GIT_CONFIG_NOSYSTEM="1"),
        "pager-editor-ssh": dict(GIT_PAGER="cat", GIT_EDITOR="true", GIT_SSH_COMMAND="ssh -oBatchMode=yes",
                                 GIT_TERMINAL_PROMPT="0", GIT_ASKPASS="true"),
        "shallow-file": dict(GIT_SHALLOW_FILE=str(WORK / "nonexistent-shallow")),
        "config-key-without-count": dict(GIT_CONFIG_KEY_0="core.bare", GIT_CONFIG_VALUE_0="true"),
        # redirect/injection class (documented as refused by name)
        "GIT_DIR-same-repo": dict(GIT_DIR=gitdir),
        "GIT_INDEX_FILE-same-index": dict(GIT_INDEX_FILE=gitdir + "/index"),
        "GIT_WORK_TREE-same-tree": dict(GIT_WORK_TREE=str(repo)),
        "GIT_CONFIG_PARAMETERS-harmless": dict(GIT_CONFIG_PARAMETERS="'color.ui'='false'"),
        "GIT_CONFIG_GLOBAL-devnull": dict(GIT_CONFIG_GLOBAL="/dev/null"),
    }
    results = []
    for label, extra in arms.items():
        before = integrity(repo, WORK / "before.json")
        env = dict(clean)
        env.update(extra, TMPDIR=str(WORK / "tmp"), PYTHONDONTWRITEBYTECODE="1")
        (WORK / "tmp").mkdir(exist_ok=True)
        done = subprocess.run([sys.executable, str(repo / "tb/verilator/gptp_shadow/mutants.py")], cwd=repo, env=env,
                              capture_output=True, text=True, timeout=300)
        after = integrity(repo, WORK / "after.json")
        out = done.stdout + done.stderr
        refused = [l for l in out.splitlines() if l.startswith("REFUSED")]
        graded = out.count("[ ok ]") + out.count("[FAIL]")
        rec = dict(arm=label, env=sorted(extra), exit=done.returncode,
                   outcome="REFUSED" if refused else ("ACCEPTED" if "controls: 9" in out else "OTHER"),
                   refusal=refused[:1], controls_graded=graded, result_line=[l for l in out.splitlines() if l.startswith("RESULT")],
                   traceback="Traceback" in out, caller_unchanged=before == after,
                   tmp_left=sorted(x.name for x in (WORK / "tmp").iterdir()))
        results.append(rec)
        print(f"{label:32s} exit={rec['exit']} {rec['outcome']:8s} graded={graded} {rec['refusal']} "
              f"caller_unchanged={rec['caller_unchanged']} tmp_left={rec['tmp_left']} tb={rec['traceback']}", flush=True)
    RECEIPT.write_text(json.dumps(results, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())

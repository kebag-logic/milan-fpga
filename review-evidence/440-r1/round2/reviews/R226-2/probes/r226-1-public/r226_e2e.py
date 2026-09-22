"""R226 end-to-end: real `gen_toc.py --write/--check` and `check_em_dash.py --base`
CLIs, base and head engines, on real Git repositories, against GitHub's renderer.

Usage: python3 -B r226_e2e.py SCRIPTS_DIR LABEL OUTDIR [--render]

For every case the BASE commit carries `## Old — heading` after the tested
prefix; the HEAD commit removes the prefix, runs the engine's own
`gen_toc.py --write` to insert the Contents block (descriptions then filled
in), and commits. The shipped em-dash CLI then judges HEAD against BASE. The
renderer oracle is GitHub's rendering of the exact BASE page: the copied label
is legitimately exempt only when that page renders the heading.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from r226_sweep import render_one  # noqa: E402

EM = "—"
HEADING = f"## Old {EM} heading"
TAIL = "\n\nBody.\n\n## Alpha\n\nBody.\n\n## Beta\n\nBody.\n\n## Gamma\n\nBody.\n"
CASES = [
    ("E01-inner-space-script", "<script>\n</script >\n"),
    ("E02-inner-tab-textarea", "<textarea>\n</textarea\t>\n"),
    ("E03-cross-textarea-PRE", "<textarea>\n</PRE>\n"),
    ("E04-cross-opening-style-Script", "<style>x</Script>\n"),
    ("E05-fence-longer-tab", "~~~~\n~~~~~\t\n"),
    ("E06-fence-space-x", "```\n``` x\n"),
    ("E07-fence-zwsp-unrefused", "```\n```​\n"),
    ("E08-fence-vt-refused", "```\n```\v\n"),
    ("E09-inner-zwsp-unrefused", "<pre>\n</pre​>\n"),
    ("E10-crlf-cross", "CRLF:<pre>\n</style>\n"),
    ("E11-lone-cr-cross", "<pre>\r</style>\r"),
    ("E12-ascii-mixed-same", "<SCRIPT>\n</sCrIpT>\n"),
    ("E13-unicode-long-s-style", "<style>\n</ſtyle>\n"),
    ("E14-non-type1-name-div", "<pre>\n</div>\n"),
    ("E15-non-type1-name-title", "<pre>\n</title>\n"),
    ("E16-inner-opening-line", "<pre></pre >\n"),
    ("E17-fence-not-ended-by-type1", "```\n</pre>\n"),
    ("E18-eof-closer-then-heading-nolf", "NOLF:<pre>\n</textarea>\n"),
]


def env() -> dict:
    e = {k: v for k, v in os.environ.items() if not k.startswith(("GIT_", "XDG_CONFIG_HOME"))}
    e.update({"GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1",
              "GIT_AUTHOR_NAME": "r226", "GIT_AUTHOR_EMAIL": "r226@localhost",
              "GIT_COMMITTER_NAME": "r226", "GIT_COMMITTER_EMAIL": "r226@localhost"})
    return e


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), "-c", "commit.gpgsign=false",
                           "-c", "core.hooksPath=/", "-c", "core.autocrlf=false", *args],
                          capture_output=True, text=True, check=True, env=env()).stdout


def page(prefix: str, nolf: bool = False) -> bytes:
    crlf = prefix.startswith("CRLF:")
    nolf = prefix.startswith("NOLF:")
    prefix = prefix.split(":", 1)[1] if (crlf or nolf) else prefix
    text = "# Page\n\nIntro.\n\n" + prefix + HEADING + TAIL
    if nolf:
        text = text.rstrip("\n")
    data = text.encode("utf-8")
    return data.replace(b"\n", b"\r\n") if crlf else data


def main() -> None:
    scripts, label, out = Path(sys.argv[1]).resolve(), sys.argv[2], Path(sys.argv[3])
    do_render = "--render" in sys.argv
    out.mkdir(parents=True, exist_ok=True)
    results = {}
    with tempfile.TemporaryDirectory(prefix="r226.e2e.") as tmp:
        repo = Path(tmp)
        shutil.copytree(scripts, repo / "scripts", ignore=shutil.ignore_patterns("__pycache__"))
        git(repo, "init", "-q", "--initial-branch=main")
        (repo / "docs").mkdir()
        for cid, prefix in CASES:
            (repo / "docs" / f"{cid}.md").write_bytes(page(prefix))
        git(repo, "add", "-A")
        git(repo, "commit", "-q", "-m", "base")
        base = git(repo, "rev-parse", "HEAD").strip()
        # base-state generator check (real CLI): which pages it reads/refuses
        chk = subprocess.run([sys.executable, "-B", "scripts/gen_toc.py", "--check"], cwd=repo,
                             capture_output=True, text=True)
        (out / f"{label}-gen_toc-check-on-base-pages.log").write_text(chk.stdout + chk.stderr + f"\nexit={chk.returncode}\n")
        # HEAD: the heading becomes real; the engine writes its own Contents block
        for cid, prefix in CASES:
            p = repo / "docs" / f"{cid}.md"
            crlf = prefix.startswith("CRLF:")
            text = "# Page\n\nIntro.\n\n" + HEADING + TAIL
            p.write_text(text)
            w = subprocess.run([sys.executable, "-B", "scripts/gen_toc.py", "--write", str(p)],
                               cwd=repo, capture_output=True, text=True)
            written = p.read_text()
            assert "## Contents" in written, (cid, w.stdout, w.stderr)
            written = written.replace("TODO describe this section", "Described.")
            p.write_bytes(written.encode().replace(b"\n", b"\r\n") if crlf else written.encode())
        git(repo, "add", "-A")
        git(repo, "commit", "-q", "-m", "head")
        chk2 = subprocess.run([sys.executable, "-B", "scripts/gen_toc.py", "--check"], cwd=repo,
                              capture_output=True, text=True)
        (out / f"{label}-gen_toc-check-on-head-pages.log").write_text(chk2.stdout + chk2.stderr + f"\nexit={chk2.returncode}\n")
        gate = subprocess.run([sys.executable, "-B", "scripts/check_em_dash.py", "--base", base],
                              cwd=repo, capture_output=True, text=True)
        (out / f"{label}-check_em_dash-cli.log").write_text(gate.stdout + gate.stderr + f"\nexit={gate.returncode}\n")
        diff = git(repo, "diff", "--stat", base, "HEAD")
        (out / f"{label}-diffstat.txt").write_text(diff)
        for cid, prefix in CASES:
            lines = [l for l in gate.stdout.splitlines() if l.startswith(f"docs/{cid}.md:")]
            results[cid] = {
                "label_finding": any("mirrors no heading" in l for l in lines),
                "heading_finding": any("in an added heading" in l for l in lines),
                "refusal_named": any("neither a space nor a tab" in l for l in lines),
                "findings": len(lines), "lines": lines}
        results["_cli"] = {"exit": gate.returncode, "summary": gate.stdout.splitlines()[-1:] or gate.stderr.splitlines()[-1:]}
        results["_head_toc_check_exit"] = chk2.returncode
        if do_render:
            oracle = {}
            for cid, prefix in CASES:
                src = page(prefix).decode("utf-8")
                row = {"id": f"R226-E-{cid}", "source": src}
                for mode in ("markdown", "gfm"):
                    r = render_one(out / "e2e-render", row, mode)
                    html = (out / "e2e-render" / "renderer" / mode / row["id"] / "response.html").read_text()
                    oracle.setdefault(cid, {})[mode] = {"h2": r["h2"], "old_heading_rendered":
                                                        bool(re.search(r"<h2[^>]*>.*?Old " + EM + " heading", html, re.S))}
            (out / "e2e-oracle.json").write_text(json.dumps(oracle, indent=1, ensure_ascii=False) + "\n")
    (out / f"{label}-e2e.json").write_text(json.dumps(results, indent=1, ensure_ascii=False) + "\n")
    for cid, _ in CASES:
        r = results[cid]
        print(label, cid, "label_finding=%s heading_finding=%s refusal=%s n=%d" % (
            r["label_finding"], r["heading_finding"], r["refusal_named"], r["findings"]))
    print(label, "CLI", results["_cli"], "head toc --check exit", results["_head_toc_check_exit"])


if __name__ == "__main__":
    main()

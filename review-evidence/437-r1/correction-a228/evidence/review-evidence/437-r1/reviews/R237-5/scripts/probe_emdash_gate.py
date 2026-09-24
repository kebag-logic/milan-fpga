#!/usr/bin/env python3
"""Run a base/head page pair through the SHIPPED em-dash gate CLI on real
Git commits, in a disposable repository built from an extracted tree.

Usage: probe_emdash_gate.py <tree> <workdir> <python> [case...]

<tree> is an extracted source tree at the reviewed head (copied whole, so
the gate's own selftest runs before its verdict, as it does in CI). For
each case the page's BASE text is committed as docs/PROBE.md, then the HEAD
text (the same page plus the Contents block gen_toc itself renders for it,
descriptions filled in), and `scripts/check_em_dash.py --base <base>` is
run inside that repository with <python>. The rc and the gate's last lines
are printed, with what gen_toc lists at the base.
"""
import shutil
import subprocess
import sys
from pathlib import Path

EM = "—"
SECTIONS = "## Alpha\n\nBody.\n\n## Beta\n\nBody.\n\n## Gamma\n\nBody.\n\n"


def pages(render) -> dict[str, str]:
    """Base pages. Every one carries three plain sections BEFORE the #516
    region, since an open raw comment swallows everything after it."""
    hidden = f"<span>\n<!--\n\n## Old {EM} heading\n</span>\n"
    control = f"# Page\n\n{SECTIONS}{hidden}"

    def forged(attr: str) -> str:
        # Positions are read off an upper-case draft: the renderer reads no
        # page that spells the attribute in lower case (its own guard).
        draft = (f'# Page\n\n{SECTIONS}<h2 X-POS="0:0-0:0">Harmless</h2>\n\n'
                 f"{hidden}")
        lines = draft.split("\n")
        pos = next(n.position for n in render(draft).nodes
                   if n.kind == "heading" and "Old" in lines[n.first - 1])
        return draft.replace("0:0-0:0", pos).replace("X-POS", attr)

    return {"control-no-forgery": control,
            "forged-DATA-SOURCEPOS": forged("DATA-SOURCEPOS"),
            "forged-Data-SourcePos": forged("Data-SourcePos"),
            "guarded-lowercase-data-sourcepos": forged("data-sourcepos")}


def main() -> int:
    tree, work, py = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
    sys.path.insert(0, str(tree / "scripts"))
    import gen_toc as g
    import gen_toc_renderer as r
    cases = pages(r.render)
    env = {"GIT_AUTHOR_NAME": "probe", "GIT_AUTHOR_EMAIL": "p@example.invalid",
           "GIT_COMMITTER_NAME": "probe", "GIT_COMMITTER_EMAIL": "p@example.invalid",
           "PATH": "/usr/bin:/bin", "HOME": str(work),
           "PYTHONDONTWRITEBYTECODE": "1", "TMPDIR": str(work),
           "GIT_CONFIG_NOSYSTEM": "1"}
    for name in sys.argv[4:] or list(cases):
        base = cases[name]
        head = g.apply(Path("PROBE.md"), base) or base
        head = head.replace(g.TODO, "Described.")
        if "Harmless" in head and name.startswith("forged"):
            # The Contents block moved the swallowed heading down: aim the
            # head page's forged attribute at its new position too, as the
            # author of such a page would.
            attr = head.split("<h2 ")[1].split("=")[0]
            old = head.split(f'{attr}="')[1].split('"')[0]
            probe = head.replace(attr, "X-POS")
            lines = probe.split("\n")
            new = next(n.position for n in r.render(probe).nodes
                       if n.kind == "heading" and "Old" in lines[n.first - 1])
            head = head.replace(f'{attr}="{old}"', f'{attr}="{new}"')
        print(f"  [{name}] generated_block(head) present: "
              f"{g.generated_block(head, 'docs/PROBE.md') is not None}")
        repo = work / name
        if repo.exists():
            shutil.rmtree(repo)
        shutil.copytree(tree, repo, symlinks=True)

        def run(*argv: str) -> subprocess.CompletedProcess:
            return subprocess.run(argv, cwd=repo, env=env, capture_output=True,
                                  text=True, check=False)

        run("git", "init", "-q", "--initial-branch=main")
        (repo / "docs/PROBE.md").write_text(base, encoding="utf-8")
        run("git", "add", "-A")
        run("git", "commit", "-q", "-m", "base")
        base_sha = run("git", "rev-parse", "HEAD").stdout.strip()
        (repo / "docs/PROBE.md").write_text(head, encoding="utf-8")
        run("git", "commit", "-q", "-am", "head")
        res = run(py, "scripts/check_em_dash.py", "--base", base_sha)
        print(f"=== {name}")
        print(f"  base page: {base!r}")
        print(f"  base headings (gen_toc): {g.headings(base)}")
        print(f"  head Contents lines: "
              f"{[l for l in head.split(chr(10)) if l.startswith('- **[')]}")
        print(f"  check_em_dash rc={res.returncode}")
        for line in (res.stdout + res.stderr).strip().splitlines()[-4:]:
            print(f"    {line}")
        shutil.rmtree(repo)
    return 0


if __name__ == "__main__":
    sys.exit(main())

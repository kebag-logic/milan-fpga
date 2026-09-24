"""End-to-end through the SHIPPED em-dash gate on real Git commits, R238-4's
method (scripts/emdash_spoof_e2e.sh) widened to every forged spelling: the
base page hides `## Old <em dash> heading` behind a raw comment left open;
the head adds a Contents block copying that label; both carry a raw element
aimed at the hidden heading's position. Usage:
emdash_e2e_spellings.py <python-with-lock> <source-repo> <workdir> [rev, default HEAD]"""
import shutil, subprocess, sys
from pathlib import Path

py, src, work = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3])
EM = "—"
SPELL = {
    "control": None,
    "upper case": lambda p: [f'<h2 DATA-SOURCEPOS="{p}">x</h2>'],
    "mixed case": lambda p: [f'<h2 Data-SourcePos="{p}">x</h2>'],
    "character reference": lambda p: ["<h2 title='", "", f"z' &#100;ata-sourcepos={p} y"],
    "backslash escape": lambda p: ["<h2 title='", "", f"z' data\\-sourcepos={p} y"],
}


def page(spell, contents):
    head = ["# Page", ""]
    toc = ["## Contents", "", "- **[Alpha](#alpha)** -- What alpha holds.",
           f"- **[Old {EM} heading](#old--heading)** -- Copied.",
           "- **[Beta](#beta)** -- What beta holds.",
           "- **[Gamma](#gamma)** -- What gamma holds.", ""] if contents else []
    forged = spell("0:0-0:0") if spell else []
    body = ["## Alpha", "", "Body.", ""] + forged + ([""] if forged else []) + [
        "<span>", "<!--", "", f"## Old {EM} heading", "", "<!-- -->", "",
        "## Beta", "", "Body.", "", "## Gamma", "", "Body.", ""]
    lines = head + toc + body
    if spell:
        at = lines.index(f"## Old {EM} heading") + 1
        pos = f"{at}:1-{at}:{len(lines[at - 1].encode())}"
        lines = head + toc + body[:4] + spell(pos) + body[4 + len(forged):]
    return "\n".join(lines)


env = {"PATH": "/usr/bin:/bin", "HOME": str(work), "GIT_CONFIG_NOSYSTEM": "1",
       "PYTHONDONTWRITEBYTECODE": "1"}
REV = sys.argv[4] if len(sys.argv) > 4 else "HEAD"
tar = subprocess.run(["git", "-C", str(src), "archive", REV, "scripts", "tools/markdown"],
                     capture_output=True, check=True).stdout
print("source head:", subprocess.run(["git", "-C", str(src), "rev-parse", REV],
                                     capture_output=True, text=True).stdout.strip())
for name, spell in SPELL.items():
    repo = work / name.replace(" ", "-")
    shutil.rmtree(repo, ignore_errors=True)
    repo.mkdir(parents=True)
    subprocess.run(["tar", "-x", "-C", str(repo)], input=tar, check=True)

    def git(*a):
        return subprocess.run(["git", "-c", "user.name=probe", "-c", "user.email=probe@example.invalid", *a],
                              cwd=repo, env=env, capture_output=True, text=True, check=True).stdout
    git("init", "-q", "--initial-branch=main"); git("add", "-A"); git("commit", "-qm", "scripts")
    (repo / "P.md").write_text(page(spell, False)); git("add", "P.md"); git("commit", "-qm", "base")
    base = git("rev-parse", "HEAD").strip()
    (repo / "P.md").write_text(page(spell, True)); git("commit", "-qam", "head")
    sys.path.insert(0, str(repo / "scripts"))
    listed = subprocess.run([py, "-c", "import sys; sys.path.insert(0, 'scripts'); import gen_toc as g; "
                             "print([h[1] for h in g.headings(open('P.md').read())])"],
                            cwd=repo, env=env, capture_output=True, text=True).stdout.strip()
    res = subprocess.run([py, "scripts/check_em_dash.py", "--base", base], cwd=repo, env=env,
                         capture_output=True, text=True)
    print(f"===== {name}: headings() at head {listed}")
    print("".join(f"    {l}\n" for l in (res.stdout + res.stderr).strip().splitlines()), end="")
    print(f"    rc={res.returncode}")
    shutil.rmtree(repo)

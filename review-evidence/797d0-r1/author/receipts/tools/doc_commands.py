"""Check commands printed on pages: the script exists and every --flag it is given appears in that script."""
import re, sys, shlex
from pathlib import Path
root = Path(sys.argv[1])
CMD = re.compile(r"(?:^|[`\s(])((?:python3?(?: -I)?|bash|sh|make(?: -C)?|\./)\s*[^`|]*)")
for page in sys.argv[2:]:
    text = (root / page).read_text()
    for n, line in enumerate(text.split("\n"), 1):
        spans = re.findall(r"`([^`]+)`", line)
        candidates = spans if spans else [line.strip()]
        for span in candidates:
            span = span.strip()
            m = re.match(r"(?:\$ )?(?:python3?(?:\s+-I)?|bash|sh)\s+(\S+)(.*)", span)
            if m:
                script, rest = m.group(1), m.group(2)
                if script.startswith("-") or "/" not in script or "<" in script or "$" in script:
                    continue
                path = root / script
                if not path.is_file():
                    print(f"{page}:{n}: MISSING SCRIPT {script} :: {span[:120]}")
                    continue
                src = path.read_text(errors="replace")
                for flag in re.findall(r"(?<![\w-])(--[a-z][\w-]*)", rest):
                    if flag not in src:
                        print(f"{page}:{n}: FLAG {flag} not in {script} :: {span[:140]}")
                continue
            m = re.match(r"make\s+-C\s+(\S+)(.*)", span)
            if m:
                d = root / m.group(1)
                if not d.is_dir() and "<" not in m.group(1) and "$" not in m.group(1):
                    print(f"{page}:{n}: MISSING MAKE DIR {m.group(1)} :: {span[:120]}")
                    continue
                mk = d / "Makefile"
                if mk.is_file():
                    for target in re.findall(r"(?<![\w=-])([a-z][\w-]*)(?![\w=])", m.group(2)):
                        if not re.search(r"(?m)^" + re.escape(target) + r"\s*:", mk.read_text()) and target not in ("j", "n"):
                            if not re.search(r"(?m)^[^#\n]*\b" + re.escape(target) + r"\b[^\n]*:", mk.read_text()):
                                print(f"{page}:{n}: MAKE TARGET {target} not in {m.group(1)}/Makefile :: {span[:120]}")

#!/usr/bin/env python3
"""Apply single-site mutants to a scratch copy of the exact-head check-ids.py and
report whether `--selftest` turns red (rc 1). Usage: mutate_ids_selftest.py <clone> <scratchdir>"""
import concurrent.futures as cf, subprocess, sys
from pathlib import Path
clone, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
src = (clone / "scripts/check-ids.py").read_text()
OLD_LOOP = '''        broken = LINE_BREAK.match(text, end)
        while broken:
            token, end = f"{token}-{broken.group(1)}", broken.end()
            broken = LINE_BREAK.match(text, end)
'''
MUTANTS = {
    "M0-identity": [],
    "M1-any-minus-one": [('token in rows or (token.endswith("-1") and token[:-2] in rows)',
                          'token in rows or token.endswith("-1")')],
    "M2-continuation-after-suffix (round-2 parser)": [
        (OLD_LOOP, ""),
        ('            yield line, token, "id"\n            sibling',
         '            broken = LINE_BREAK.match(text, end)\n'
         '            yield line, f"{token}-{broken.group(1)}" if broken else token, "id"\n            sibling')],
    "M3-single-continuation (while->if)": [("        while broken:\n", "        if broken:\n"),
                                            ("            broken = LINE_BREAK.match(text, end)\n        if text", "            pass\n        if text")],
    "M4-optional-no-linebreak": [('OPTIONAL = re.compile(r"\\(-(?:" + NEXT_LINE + r")?(', 'OPTIONAL = re.compile(r"\\(-(')],
    "M5-no-continuation": [(OLD_LOOP, "")],
    "M6-optional-not-yielded": [('            if optional:\n                yield line, f"{token}-{optional.group(1)}", "id"',
                                 '            if optional:\n                pass')],
    "M7-sibling-not-yielded": [("            if sibling:\n                yield", "            if False:\n                yield")],
    "M8-rc-always-0": [("    return 1 if problems else 0", "    return 0")],
    "M9-family-any": [('return token in rows or any(r.startswith(token + "-") for r in rows)', 'return True')],
    "M10-braces-skip-bad-list": [('                yield line, f"{token}-{{...}}", "list"', '                pass')],
    "M12-skip-optional-only-if-linebroken": [('            if optional:\n                yield line, f"{token}-{optional.group(1)}", "id"',
                                              '            if optional:\n                if "\\n" not in optional.group(0):\n                    yield line, f"{token}-{optional.group(1)}", "id"')],
    "M11-minus-one-strip-any-digit":[('token.endswith("-1") and token[:-2] in rows', 'token[-2:-1] == "-" and token[-1].isdigit() and token[:-2] in rows')],
}
def run(name, edits):
    text = src
    for old, new in edits:
        n = text.count(old)
        if n != 1:
            return name, f"MUTANT NOT APPLIED (site count {n})", ""
        text = text.replace(old, new)
    d = scratch / name.split()[0]; d.mkdir(parents=True, exist_ok=True)
    f = d / "check-ids.py"; f.write_text(text)
    p = subprocess.run([sys.executable, str(f), "--selftest"], capture_output=True, text=True)
    fails = [l.split(":")[1].strip() for l in p.stdout.splitlines() if l.startswith("SELFTEST FAIL")]
    return name, f"selftest rc={p.returncode}", " ".join(fails) + " | " + p.stdout.strip().splitlines()[-1]
with cf.ThreadPoolExecutor(12) as ex:
    for name, verdict, detail in ex.map(lambda kv: run(*kv), MUTANTS.items()):
        print(f"{name:48s} {verdict:22s} {detail}")

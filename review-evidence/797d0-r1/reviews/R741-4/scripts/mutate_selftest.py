#!/usr/bin/env python3
"""Run the inventory self-test against mutated copies of the script; every mutant must make it fail."""
import subprocess, sys, pathlib
src = pathlib.Path(sys.argv[1]).read_text(); out = pathlib.Path(sys.argv[2])
M = {
 "no-underscore-strip": ('INLINE_MARKUP_RE = re.compile(r"[`*]|(?<!\\w)_+(?=\\S)|(?<=\\S)_+(?!\\w)")', 'INLINE_MARKUP_RE = re.compile(r"[`*]")'),
 "all-underscores-stripped": ('INLINE_MARKUP_RE = re.compile(r"[`*]|(?<!\\w)_+(?=\\S)|(?<=\\S)_+(?!\\w)")', 'INLINE_MARKUP_RE = re.compile(r"[`*_]")'),
 "no-left-underscore": ('|(?<!\\w)_+(?=\\S)', ''),
 "no-right-underscore": ('|(?<=\\S)_+(?!\\w)', ''),
 "no-reference-link": ('(?:\\([^)\\n]*\\)|\\[[^\\]\\n]*\\])', '(?:\\([^)\\n]*\\))'),
 "no-inline-link": ('(?:\\([^)\\n]*\\)|\\[[^\\]\\n]*\\])', '(?:\\[[^\\]\\n]*\\])'),
 "flatten-without-link": ('for line in LINK_RE.sub(r"\\1", text).split("\\n"):', 'for line in text.split("\\n"):'),
 "normal-form-without-link": ('plain = LINK_RE.sub(r"\\1", unicodedata.normalize("NFKC", text))', 'plain = unicodedata.normalize("NFKC", text)'),
 "needle-keeps-punctuation": ('return normal_form(statement).rstrip(".,;:")', 'return normal_form(statement)'),
 "needle-strips-dot-only": ('.rstrip(".,;:")', '.rstrip(".")'),
 "also-accepts-markup-only": ('isinstance(value, str) and needle_of(value) for value in also', 'isinstance(value, str) and value.strip() for value in also'),
 "also-searched-not": ('for statement in (finding.quote, *finding.also):', 'for statement in (finding.quote,):'),
 "carried-needle-is-normal-form": ('needle = needle_of(statement)\n    if needle not in flat[0]:', 'needle = normal_form(statement)\n    if needle not in flat[0]:'),
 "held-is-normal-form": ('append(needle_of(finding.quote))', 'append(normal_form(finding.quote))'),
}
rc = 0
for name, (a, b) in M.items():
    if src.count(a) < 1:
        print(name, "NOT-APPLIED"); rc = 1; continue
    p = out / f"{name}.py"; p.write_text(src.replace(a, b))
    r = subprocess.run([sys.executable, "-I", str(p), "--selftest"], capture_output=True, text=True, cwd=sys.argv[3])
    tail = (r.stdout + r.stderr).strip().splitlines()
    fails = [l for l in tail if "FAIL" in l.upper()]
    print(f"{name}\trc={r.returncode}\t{'KILLED' if r.returncode else 'SURVIVED'}\t{(fails[0] if fails else tail[-1] if tail else '')[:170]}")

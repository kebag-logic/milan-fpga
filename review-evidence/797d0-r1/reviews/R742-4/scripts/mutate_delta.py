#!/usr/bin/env python3
"""Grade the inventory self-test against mutants of the round 4 delta, one at a time, on a copy of the generator.

Usage: mutate_delta.py <clone at the head>. The clone's generator is rewritten and restored around each mutant.
"""
import subprocess
import sys
from pathlib import Path

MARKUP = 'INLINE_MARKUP_RE = re.compile(r"[`*]|(?<!\\w)_+(?=\\S)|(?<=\\S)_+(?!\\w)")'
LINK_TAIL = '(?:\\([^)\\n]*\\)|\\[[^\\]\\n]*\\])")'
MUTANTS = {
    "underscore-not-stripped": (MARKUP, 'INLINE_MARKUP_RE = re.compile(r"[`*]")'),
    "every-underscore-stripped": (MARKUP, 'INLINE_MARKUP_RE = re.compile(r"[`*_]")'),
    "closing-underscore-kept": ('|(?<=\\S)_+(?!\\w)")', '")'),
    "opening-underscore-kept": ('r"[`*]|(?<!\\w)_+(?=\\S)|', 'r"[`*]|'),
    "reference-link-dropped": (LINK_TAIL, '(?:\\([^)\\n]*\\))")'),
    "inline-link-dropped": (LINK_TAIL, '(?:\\[[^\\]\\n]*\\])")'),
    "page-link-not-flattened": ('for line in LINK_RE.sub(r"\\1", text).split("\\n"):',
                                'for line in text.split("\\n"):'),
    "statement-link-kept": ('plain = LINK_RE.sub(r"\\1", unicodedata.normalize("NFKC", text))',
                            'plain = unicodedata.normalize("NFKC", text)'),
    "closing-punctuation-kept": ('return normal_form(statement).rstrip(".,;:")', 'return normal_form(statement)'),
    "comma-not-stripped": ('.rstrip(".,;:")', '.rstrip(".;:")'),
    "held-keeps-punctuation": ('held.setdefault(finding.page, []).append(needle_of(finding.quote))',
                               'held.setdefault(finding.page, []).append(normal_form(finding.quote))'),
    "also-empty-accepted": ('isinstance(value, str) and needle_of(value) for value in also',
                            'isinstance(value, str) and value.strip() for value in also'),
    "also-not-searched": ('for statement in (finding.quote, *finding.also):', 'for statement in (finding.quote,):'),
}

clone = Path(sys.argv[1]).resolve()
target = clone / "scripts/docs_inventory.py"
original = target.read_text(encoding="utf-8")
killed = survived = 0
try:
    for name, (old, new) in MUTANTS.items():
        if original.count(old) != 1:
            print(f"{name}\tNOT APPLIED", flush=True)
            continue
        target.write_text(original.replace(old, new), encoding="utf-8")
        run = subprocess.run(["python3", "-I", "scripts/docs_inventory.py", "--selftest"], cwd=clone,
                             text=True, capture_output=True)
        verdict = "KILLED" if run.returncode else "SURVIVED"
        killed += bool(run.returncode)
        survived += not run.returncode
        first = next((line for line in run.stdout.splitlines() if "FAIL" in line.upper()), "")
        print(f"{name}\trc={run.returncode}\t{verdict}\t{first[:110]}", flush=True)
finally:
    target.write_text(original, encoding="utf-8")
print(f"mutants {killed + survived}, killed {killed}, survived {survived}")

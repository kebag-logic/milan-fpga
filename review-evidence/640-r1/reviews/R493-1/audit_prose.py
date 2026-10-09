#!/usr/bin/env python3
"""Expose prose checks outside the built-in style gate's fixed population."""
import importlib.util
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location('style', root / 'scripts/check_doc_style.py')
style = importlib.util.module_from_spec(spec)
sys.modules['style'] = style
spec.loader.exec_module(style)
result = {}
for name in ['docs/design/MARK_II_AREA_PLAN.md', 'docs/design/AREA_BUDGET.md']:
    path = root / name
    text = path.read_text()
    sentences = [vars(f) for f in style.analyze(text) if f.reason.startswith('sentence')]
    references = []
    fenced = False
    for n, line in enumerate(text.splitlines(), 1):
        if line.startswith('```'):
            fenced = not fenced
        if fenced:
            continue
        without_links = re.sub(r'\[[^\]]*\]\([^)]*\)', '', line)
        for match in re.finditer(r'(?<![\w/#])#\d+\b', without_links):
            references.append({'line':n, 'reference':match.group(), 'text':line})
    result[name] = {'in_builtin_gate_population':path in style.DOCUMENTS,
                    'long_sentence_observations':sentences,
                    'unlinked_issue_reference_observations':references}
print(json.dumps(result, indent=2))

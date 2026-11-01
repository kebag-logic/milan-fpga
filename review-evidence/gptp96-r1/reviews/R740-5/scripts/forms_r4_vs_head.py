#!/usr/bin/env python3
"""Run named forms through copy_findings of one checker; print copy found or passed.

usage: python3 -I forms_r4_vs_head.py <check_docs.py> <repo>
"""
import importlib.util, sys, types
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location("check_docs", sys.argv[1])
m = importlib.util.module_from_spec(spec)
sys.path.insert(0, sys.argv[2])
spec.loader.exec_module(m)
fixture = types.SimpleNamespace(SYNC_RTO_MS_C=375)
table = f"{m.CONSTANTS_HEADING}\n\n| Constant | Value | Meaning |\n|---|---:|---|\n| `SYNC_RTO_MS_C` | 375 | syncReceiptTimeout, ms |\n"
FORMS = {
 "S1a marker plus five spaces then indented fence": "-     x\n  ```\n  y\nA 375 ms watch.\n",
 "S1b empty item with a trailing tab": "-\t\n   ```\n\nA 375 ms watch.\n",
 "S1c empty item with two trailing spaces": "-  \n  ```\n\nA 375 ms watch.\n",
 "S1d ordered marker not 1 cannot interrupt a paragraph": "Text\n2. ```\n\n   A 375 ms watch.\n",
 "S1e paragraph under an empty item ended by a blank": "*\n\n  Text\n    ~~~\n\n   A 375 ms watch.\n",
 "S1f form feed only line ends a list item": "- ```\n  x\n\x0c\n  A 375 ms watch.\n",
 "lazy (recorded arm)": "- Item.\nlazy\n  ```\nA 375 ms watch.\n",
}
for label, text in FORMS.items():
    print(("finding" if m.copy_findings({"docs/GUIDE.md": text}, table, fixture) else "PASSES ") + " | " + label + " | " + repr(text))

#!/usr/bin/env python3
"""R273-8 S-check: the readers vs the pinned GCC on an empty block comment
`/**/`, intact and under the closer-from-i+3 mutation (delta_probe.py's
disposable copies under <work>). usage: empty_comment_check.py <work> <gcc>"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.argv, work, gcc = sys.argv[:1] + ["x"] * 5, Path(sys.argv[1]), sys.argv[2]
import importlib.util
spec = importlib.util.spec_from_file_location("d", Path(__file__).with_name("delta_probe.py"))
src = spec.loader.get_source("d").replace("\nsys.exit(main())\n", "\n")
d = {"__file__": str(Path(__file__).with_name("delta_probe.py")), "__name__": "d"}
exec(compile(src, "delta_probe.py", "exec"), d)
text = "int a;\n/**/\n#define FOO\n/* */\n#ifdef FOO\nint b;\n#endif\nint z;\n"
print("gcc:", d["gcc_keeps"](gcc, text)["kept"])
for name in ("head-intact", "head-closer-from-i+3"):
    ns = d["load"](work / name)
    print(name, "readers keep", ns["lexer_readers"]["keeps"](text))

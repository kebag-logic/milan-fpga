"""R226 extra mutants (same harness as r226_mutants.py, separate result file)."""
import sys, runpy
from pathlib import Path
here = Path(__file__).resolve().parent
mod = runpy.run_path(str(here / "r226_mutants.py"), run_name="r226_mutants_lib")
CLOSE = mod["CLOSE"]; LEN = mod["LEN"]; T = mod["T"]
mod["MUTANTS"][:] = [
    ("X01-raw-html-tags-plus-title-both-sites",
     [(T, 'RAW_HTML_TAGS = ("pre", "script", "style", "textarea")',
          'RAW_HTML_TAGS = ("pre", "script", "style", "textarea", "title")')]),
    ("X02-closer-any-ascii-tag-name", [(T, CLOSE, 'return bool(re.search(r"</[a-z]+>", line, ASCII_FOLD))')]),
    ("X03-length-strictly-longer", [(T, LEN, "len(m.group(1)) > len(delim)")]),
    ("X04-closer-add-xmp", [(T, CLOSE, CLOSE.replace('"|".join(RAW_HTML_TAGS)', '"|".join(RAW_HTML_TAGS + ("xmp",))'))]),
]
mod["main"]()

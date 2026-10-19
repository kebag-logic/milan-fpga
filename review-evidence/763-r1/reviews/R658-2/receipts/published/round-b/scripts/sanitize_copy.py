"""Copy a text receipt, replacing host paths with neutral placeholders: sanitize_copy.py SRC DST OLD=NEW..."""
import sys
from pathlib import Path
text = Path(sys.argv[1]).read_text(errors="replace")
for pair in sys.argv[3:]:
    old, new = pair.split("=", 1)
    text = text.replace(old, new)
Path(sys.argv[2]).parent.mkdir(parents=True, exist_ok=True)
Path(sys.argv[2]).write_text(text)

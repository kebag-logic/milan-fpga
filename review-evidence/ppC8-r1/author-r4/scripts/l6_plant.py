"""Plant one stricter-L6 defect in a scratch copy's model_rules.py."""
import sys
from pathlib import Path

PLANTS = {
    "aaf-single-beside-crf": (
        "        if aaf_in and not crf_in:\n",
        "        if crf_in and sum(at_input[k] for k in aaf_in) > 1:\n"
        "            ctx.bad(\"aaf-input-source\", (cfg, D.CLOCK_SOURCE, None), \"PLANT\")\n"
        "        if aaf_in and not crf_in:\n"),
    "aaf-refused-beside-crf": (
        "        if aaf_in and not crf_in:\n",
        "        if crf_in and any(at_input[k] for k in aaf_in):\n"
        "            ctx.bad(\"aaf-input-source\", (cfg, D.CLOCK_SOURCE, None), \"PLANT\")\n"
        "        if aaf_in and not crf_in:\n"),
    "count-cap-8": (
        "            if count == 0:\n                ctx.bad(\"domain-source-count\"",
        "            if count > 8:\n"
        "                ctx.bad(\"domain-source-count\", where, \"PLANT\")\n"
        "            if count == 0:\n                ctx.bad(\"domain-source-count\""),
    "count-cap-9": (
        "            if count == 0:\n                ctx.bad(\"domain-source-count\"",
        "            if count > 9:\n"
        "                ctx.bad(\"domain-source-count\", where, \"PLANT\")\n"
        "            if count == 0:\n                ctx.bad(\"domain-source-count\""),
    "one-source-per-input-overall": (
        "        for stream in crf_in:\n",
        "        if sum(at_input.values()) > 2:\n"
        "            ctx.bad(\"crf-input-source\", (cfg, D.CLOCK_SOURCE, None), \"PLANT\")\n"
        "        for stream in crf_in:\n"),
}

root, name = Path(sys.argv[1]), sys.argv[2]
path = root / "hdl/aecp/desc/model_rules.py"
text = path.read_text()
old, new = PLANTS[name]
assert text.count(old) == 1, (name, text.count(old))
path.write_text(text.replace(old, new))

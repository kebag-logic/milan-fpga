"""Parser headings vs recorded GitHub headings for every rendered shape."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(sys.argv[1]) / "scripts"))
import gen_toc, gen_toc_renderer as r
rows = json.loads(Path(sys.argv[2]).read_text())
bad = 0
for s in rows:
    github = r.headings_of(s["response_bytes"])
    rendered = r.render(s["page"])
    heads = {n.position for n in rendered.nodes if n.kind == "heading"}
    ours = gen_toc.rendered_headings(s["page"])
    listed = [(lvl, raw) for lvl, raw, _ in gen_toc.headings(s["page"])]
    if ours != github:
        bad += 1
        print("DISAGREE", s["set"], "|", s["name"], "|", repr(s["page"]), "\n   github", github, "\n   parser", ours, "\n   resp", repr(s["response_bytes"])[:300])
print(len(rows), "shapes,", bad, "disagree")

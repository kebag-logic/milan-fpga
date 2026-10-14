"""List each layer's top-level entries and any build-only path (mount stubs, work dirs, caches, histories)."""
import json, re, sys
sys.path.insert(0, __import__("os").path.dirname(__file__))
from oci_layers import open_image, members
_, _, _, layers = open_image(sys.argv[1])
suspect = re.compile(r"^(debs|debs\.sha256|recipe|inputs|build|work/.+|root/.+|tmp/.+|home/(?!ubuntu(/\.bash_logout|/\.bashrc|/\.profile)?$).+)$|"
                     r"(^|/)(\.git|\.netrc|\.git-credentials|\.docker|\.pypirc|\.npmrc|\.bash_history|\.python_history|\.wget-hsts|\.cache)(/|$)|"
                     r"direct_url\.json$|CMakeConfigureLog\.yaml$|CMakeCache\.txt$")
for l in layers:
    tops, hits = set(), []
    for m, c in members(l["data"]()):
        tops.add(m.name.split("/")[0])
        if suspect.search(m.name):
            hits.append(m.name)
    print(json.dumps({"layer": l["index"], "by": l["created_by"][:50], "top": sorted(tops),
                      "suspect_count": len(hits), "suspect_examples": hits[:15]}))

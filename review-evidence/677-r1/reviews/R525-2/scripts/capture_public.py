#!/usr/bin/env python3
"""Read-only public artifact capture; no review reports fetched by this script."""
import json, pathlib, subprocess, sys
out = pathlib.Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=True)
repo = "repos/kebag-logic/milan-fpga"
def fetch(endpoint, name, keys):
    obj = json.loads(subprocess.check_output(["gh", "api", repo + endpoint]))
    obj = {key:obj[key] for key in keys}
    for key in ("head", "base"):
        if key in obj:
            obj[key] = {field:obj[key][field] for field in ("sha", "ref")}
    (out / name).write_text(json.dumps(obj, indent=2) + "\n")
fetch("/issues/677", "issue-677.json", ["number", "title", "body", "html_url", "updated_at"])
fetch("/issues/678", "issue-678.json", ["number", "title", "body", "html_url", "updated_at"])
fetch("/pulls/684", "pr-684.json", ["number", "title", "body", "html_url", "head", "base", "updated_at"])
for comment_id in (6021510152,6021539044,6024328677,6024757146,6024758957):
    fetch("/issues/comments/" + str(comment_id), "comment-" + str(comment_id) + ".json", ["id", "body", "html_url", "created_at", "updated_at"])
print("PASS: issue bodies, PR body, scope, takeover, correction and start captured read-only")

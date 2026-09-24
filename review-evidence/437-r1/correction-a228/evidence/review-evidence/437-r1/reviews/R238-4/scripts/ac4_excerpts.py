#!/usr/bin/env python3
"""Print GitHub's file-view rendering around each AC4 line-label difference.

Usage: ac4_excerpts.py <ac4-github-judgement.json> <repo> <base-rev>
Reads the recorded file-view responses kept by judge_ac4_lines.py and, for a
distinctive token of each differing region, prints the rendered HTML around
it (the enclosing element decides code / table row / prose / heading). Then
compares every family-two page's complete id list with gen_toc.headings().
"""
import json, re, subprocess, sys
d = json.load(open(sys.argv[1])); repo, rev = sys.argv[2], sys.argv[3]
sys.path.insert(0, f"{repo}/scripts")
import gen_toc
probes = {
 "CONTRIBUTING.md": ["A hosted pass does not replace", "syn/yosys/run.sh</pre>"],
 "QUICKSTART.md": ["git clone https://github.com/alexforencich/verilog-axis"],
 "docs/MILAN_V12_ROADMAP.md": ["GET_MILAN_INFO</code> | 5.4.4.1"],
 "docs/design/SAVED_STATE_FASTCONNECT.md": ["whole-image A/B promotion", "<th>round 3</th>"],
 "docs/design/SAVED_STATE_MATERIALIZATION.md": ["They are prerequisites of stage 1"],
 "docs/history/v1/design/TIME_SYNC.md": ["0.5 with CRF selected"],
 "docs/limitations/TROUBLESHOOTING.md": ["select listener entry 0", "sustained 5 s"],
 "docs/reference/REGISTER_MAP.md": ["<code>SCRATCH</code> | RW", "<code>IRQ_RAW</code> | RO"],
 "docs/testing/CI_WORKFLOWS.md": ["publishes the same shape", "retain their recorded", "SHA-pin script is also pinned", "Their maintenance remedy is recorded"],
 "docs/testing/TESTING.md": ["| Verible v0.0-4084", "capability boundary this page"],
}
for p in d["pages"]:
    resp = p["response_bytes"]
    for tok in probes.get(p["page"], []):
        i = resp.find(tok)
        seg = resp[max(0, i - 200): i + 90].replace("\n", "\\n") if i >= 0 else "TOKEN NOT FOUND"
        pre = i >= 0 and resp.rfind("<pre", 0, i) > resp.rfind("</pre>", 0, i)
        print(f"## {p['page']} | {tok!r} | inside <pre>: {pre}\n   {seg}\n")
for page in ["docs/history/v1/SPEC_TRACEABILITY.md", "docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md",
             "docs/history/v1/testing/MILAN_COMPLIANCE_MATRIX.md", "docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md",
             "docs/history/v1/testing/PROTOCOL_SWEEP_PLAN.md", "docs/testing/TESTING.md"]:
    resp = next(x["response_bytes"] for x in d["pages"] if x["page"] == page)
    ids = re.findall(r'<a id="user-content-([^"]*)" class="anchor"', resp)
    text = subprocess.run(["git", "-C", repo, "show", f"{rev}:{page}"], capture_output=True, check=True).stdout.decode()
    local = [a for _, _, a in gen_toc.headings(text)]
    print(f"family two: {page}: file-view ids == headings() anchors: {ids == local} ({len(ids)} headings)")

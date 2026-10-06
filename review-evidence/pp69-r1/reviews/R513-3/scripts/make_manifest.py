#!/usr/bin/env python3
"""Publish only the explicit review packet inventory, excluding scratch and API caches."""
import hashlib,pathlib,sys
p=pathlib.Path(sys.argv[1]).resolve()
files=[p/"REPORT.md"]+sorted((p/"scripts").glob("*.py"))+[p/"scripts/README.md"]
names="""adp.log adp.rc if-guards.log if-guards.rc notify.log notify.rc focused-results.json
simulator-identity.txt delta-check.json readme-merge.json campaign-summary.json
counter-shape-1-1.log counter-shape-1-2.log counter-shape-8-1.log counter-shape-8-2.log
docs.log docs.rc docs-archive-attempt.log docs-archive-attempt.rc docs-env-attempt.log docs-env-attempt.rc
docs-before-metadata-restore.log docs-before-metadata-restore.rc documentation-setup.json
resource-use.json tree-integrity.json tracked-blobs.txt independent-verdict.md independence-freeze.json
reconstruction.json full-diff.patch round3-diff.patch history.txt prior-findings.json scope-comments.json
public-comment-inventory.json issue-69.json issue-42.json issue-167.json pr-165.json reviews.json inline-comments.json
public-MANIFEST.json public-HANDOFF.md public-PR-BODY.md public-parent-adoption-148-6c22d3ca.patch public-evidence-integrity.json
evidence-tree.json hosted-summary.json hosted-final-37540577805.json hosted-final-37540570371.json""".split()
files += [p/"receipts"/name for name in names]
files += sorted((p/"receipts/notify").glob("*.log"))+[p/"receipts/notify/results.json"]
assert len(files)==len(set(files))
rows=[]
for f in sorted(files):
 assert f.is_file() and not f.is_symlink(),f
 rel=f.relative_to(p).as_posix();assert not rel.startswith("scratch/")
 rows.append(hashlib.sha256(f.read_bytes()).hexdigest()+"  "+rel)
(p/"MANIFEST.sha256").write_text("\n".join(rows)+"\n")
print(f"{len(rows)} publishable files; scratch excluded")

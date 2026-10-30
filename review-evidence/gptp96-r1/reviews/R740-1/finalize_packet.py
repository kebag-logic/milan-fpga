#!/usr/bin/env python3
"""Finalize public reconciliation and hash the explicitly selected receipts."""
import datetime,hashlib,json,pathlib
out=pathlib.Path(__file__).resolve().parent
scratch=out/"scratch"
records=[]
manifest=json.loads((scratch/"published-manifest.json").read_text())
for item in manifest:
 local={"author/HANDOFF.md":"published-handoff.md","author/PR-BODY.md":"published-body.md"}[item["file"]]
 digest=hashlib.sha256((scratch/local).read_bytes()).hexdigest()
 assert digest==item["published_sha256"]
 records.append({"file":item["file"],"sha256":digest,"matches_published_manifest":True})
comments={}
for filename in ["issue-comments.json","pr-comments.json","pr-reviews.json","pr-review-comments.json"]:
 rows=json.loads((scratch/filename).read_text())
 comments[filename]=[{"id":r["id"],"url":r.get("html_url"),"created_at":r.get("created_at",r.get("submitted_at"))} for r in rows]
evidence={"source_head":"8607347675743fe8d1ccaa370c63905c5ca1ccd5","published_evidence_commit":"54920832e24d0e69855dbbc76953fd1e27805656","published_files":records,"public_comment_inventory":comments,"exact_head_check_runs":json.loads((scratch/"check-runs.json").read_text())["total_count"],"independent_seal_sha256":hashlib.sha256((out/"INDEPENDENT.md").read_bytes()).hexdigest(),"reconciliation_utc":datetime.datetime.now(datetime.timezone.utc).isoformat()}
(out/"public-evidence-audit.json").write_text(json.dumps(evidence,indent=2)+"\n")
p=out/"REPORT.md";report=(out/"INDEPENDENT.md").read_text()
report=report.replace("Public-evidence and prior-finding reconciliation follows this sealed independent pass.","The independent snapshot is preserved as INDEPENDENT.md; post-seal public reconciliation appears below.")
report=report.replace("Receipts: probe-formatted-stale-constant.log/.rc,", "The complete make -j16 docs target also passes with the bold stale cell (probe-full-formatted-stale.log/.rc). Receipts: probe-formatted-stale-constant.log/.rc,")
report=report.replace("Remaining edition checks must retain this limitation, including Figures 11-6/11-8 and Milan Annex B.1.1;", "Remaining edition checks must retain this limitation, especially the complete corrected Figure 11-8 and Milan Annex B.1.1;")
report=report.replace("Public acceptance comments, exact published gate receipts and prior public FINDINGS have not yet been read at this independent seal. Their reconciliation will be appended after the seal; the independent findings above already establish NEGATIVE.","Public acceptance comments, published gate evidence and prior public FINDINGS were deferred until the independent verdict and ledger were written. The following reconciliation is complete; the independent findings remain unchanged.")
report=report.removesuffix("R740-1 FINISHED\n")
report+="""Post-seal public reconciliation

The issue #96 comments contain only assignment/readiness notices. PR #97 has two independent-review start notices; its review and inline-comment endpoints are empty. There are no earlier public review FINDINGS on this PR to resolve or retain at the time inspected. The start notice confirms two independent positive reviews and the full completion bar remain necessary. No manager evidence comment or manager source bank was present. This is recorded in public-evidence-audit.json, including comment URLs and the exact evidence hashes.

Parent #797 body and its public scope decisions were checked after the seal. The parent-specific Ethernet/register-map addition is separate from this donor delta. Its sweep-start decision delegates this repository pass and explicitly retains the issue rules; it does not waive the single-source rule. See [parent sweep decision](https://github.com/kebag-logic/milan-fpga/issues/797#issuecomment-6518880512) and [donor acceptance](https://github.com/Mister-M-alt/FPGA-gPTP/issues/96). The public handoff explicitly acknowledges approximately 25 remaining inline value restatements. This corroborates F3; treating a later gate as optional does not satisfy the current no-copy rule.

The linked [step-policy owner decision](https://github.com/Mister-M-alt/FPGA-gPTP/issues/68#issuecomment-5794731372) and [link-up interpretation](https://github.com/Mister-M-alt/FPGA-gPTP/issues/68#issuecomment-5798089412) confirm the checked thresholds and rearm rule. The [receive-write ruling](https://github.com/Mister-M-alt/FPGA-gPTP/issues/35#issuecomment-6105869522) permits writes up to the error edge and forbids later writes; the current guide matches that narrowed contract. No new review finding is based on superseded issue-body requirements.

The [published evidence directory](https://github.com/kebag-logic/milan-fpga/tree/54920832e24d0e69855dbbc76953fd1e27805656/review-evidence/gptp96-r1) contains MANIFEST.json and two author documents, HANDOFF.md and PR-BODY.md. Both documents match the manifest SHA-256 values. This directory contains narrative gate tables and mutation summaries, not underlying per-command raw logs. Their source-head execution claims are attributed to the author, not to the manager or this review.

| Published source validation | Base and head claim | Independent treatment |
|---|---|---|
| Docs, diagrams, contract, lint | rc 0 at both | Head reproduced locally; base not rerun |
| Arithmetic suite | 768 checks, rc 0 | Author-reported execution |
| Parser and mutations | 378 and 16 checks, rc 0 | Author-reported execution |
| Engine run | 2,048 checks in each of three runs, plus 60 | Author-reported execution |
| Gasket and mutations | 81 and 5 checks, rc 0 | Author-reported execution |
| Independent decode and mutations | 288 and 4 checks, rc 0 | Author reports dependency present and execution; not counted as a local run |
| Bench timestamp-tag suite | rc 0 | Author-reported execution |
| Engine mutation bank, synthesis | NOT RUN | No coverage credited |
| Parent quality/hygiene ratchets | rc 0 on a scratch consumer comparison | Author-reported; not current-dev acceptance |
| Parent docs with unadjusted gitlink pins | rc 1 at both base/head | Outstanding adoption work, not represented as passing |
| Parent gPTP docs after pin rewrite | rc 0 at both | Author-reported; remaining parent reconciliation still required |

The exact source head has zero hosted check runs in the check-runs response. This supplies no executed hosted job and no skipped job that can be credited as a pass. Hosted/act acceptance remains the manager responsibility.

The public handoff source-comment observations were independently checked against the unchanged generator/header: old historical loss-count, Sync-ageing and cease notes, plus repeated header wording. These are existing source-comment follow-ups outside the documentation delta, not new defects introduced here. Its dated synthesis-measurement limitation remains valid; no current resource remeasurement is claimed. No other reviewer report was read.

Additional clause cross-check after the seal: the indexed 2011 primary text maps 11.2.16 to the responder state machine and Figure 11-6 to matching Sync/Follow_Up sequence IDs and timeout handling. [IEEE maintenance request 0077](https://www.ieee802.org/1/files/public/maint/requests/maint_0077.pdf) independently locates that figure in 11.2.13.3 and records its interval-unit correction. These confirm the edition mapping; they do not eliminate the complete-primary-document access limits above.

Reproduction and publication

Run `python3 run_review_checks.py /path/to/exact/checkout` for focused gates and probes, and `python3 audit_source.py /path/to/exact/checkout` for generated-image and full tracked-byte/mode/index checks. Probe copies, temporary generator outputs and fetched supporting material stay under scratch and are excluded from publication. The gate runner uses the scoped installed lint executable; REVIEW_LINT_DIR may supply an equivalent installation directory on another machine. Individual command logs and return-code files are retained. The independent-seal digest names a relative packet path.

Final integrity: 113 tracked blobs and executable modes match the exact head, index matches HEAD, no submodule gitlinks exist, and working-tree status is clean. Every publishable receipt is listed in MANIFEST.sha256. No GitHub write, source edit, commit, push, merge, hardware access or parent build was performed. The four MINOR findings leave the five lenses unclean and the verdict NEGATIVE.

R740-1 FINISHED
"""
p.write_text(report)
(out/"independent-seal.sha256").write_text(hashlib.sha256((out/"INDEPENDENT.md").read_bytes()).hexdigest()+"  INDEPENDENT.md\n")
files=["REPORT.md","INDEPENDENT.md","independent-seal.sha256","run_review_checks.py","audit_source.py","finalize_packet.py","source-audit.log","probe-results.json","public-evidence-audit.json"]
files += [p.name for p in out.glob("*.log") if p.name not in files]
files += [p.name for p in out.glob("*.rc")]
(out/"MANIFEST.sha256").write_text("".join(hashlib.sha256((out/name).read_bytes()).hexdigest()+"  "+name+"\n" for name in sorted(set(files))))
print("Final report and",len(set(files)),"publishable files hashed.")

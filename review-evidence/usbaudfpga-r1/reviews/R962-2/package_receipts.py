#!/usr/bin/env python3
"""Select publishable review receipts and replace only private execution-root prefixes."""
import hashlib,json,pathlib
OUT=pathlib.Path(__file__).resolve().parent
ROOT=pathlib.Path.cwd()
def sha(data):return hashlib.sha256(data).hexdigest()
names=["audit_packet.py","verify_checkout.py","run_probes.py","run_gate_followups.py","package_receipts.py",
       "packet-audit.json","supporting-audit.json","checkout-initial.json","checkout-final.json",
       "probe-results.json","gate-followup-results.json","epoch-controls-results.json","grid-controls-results.json",
       "execution-notes.txt","simulator-identity.json"]
for stem in ["epoch-controls","grid-controls","gate_11","gate_32","gate_35","docs-inventory-workflow","tap-clock-docs","scheduling-controls"]:
    names += [stem+".log",stem+".rc"]
names += [str(p.relative_to(OUT)) for p in (OUT/"probe-runtime").rglob("*.log")]
provenance=[]
for name in names:
    p=OUT/name
    raw=p.read_bytes()
    data=raw
    if p.suffix in (".json",".log"):
        data=data.replace(str(ROOT).encode(),b"<review-checkout>").replace(str(OUT).encode(),b"<review-packet>")
        if data!=raw:
            dest=OUT/"scratch/unredacted"/name
            dest.parent.mkdir(parents=True,exist_ok=True)
            dest.write_bytes(raw)
            p.write_bytes(data)
    provenance.append({"path":name,"original_sha256":sha(raw),"published_sha256":sha(data),"path_redacted":raw!=data})
(OUT/"receipt-provenance.json").write_text(json.dumps(provenance,indent=2)+"\n")
names += ["receipt-provenance.json"]
(OUT/"MANIFEST.sha256").write_text("".join(sha((OUT/n).read_bytes())+"  "+n+"\n" for n in sorted(names)))
print("Publishable receipts:",len(names))

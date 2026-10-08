#!/usr/bin/env python3
"""Cross-check public receipts, immutable manifests, and the exact production scope."""
import hashlib, json, pathlib, subprocess, sys
packet=pathlib.Path(__file__).resolve().parents[1]; root=pathlib.Path(sys.argv[1]).resolve()
evidence=packet/"public/evidence"; author=evidence/"author"
def read(name): return json.loads((author/(name+".json")).read_text())
def git(*args): return subprocess.check_output(["git","-C",str(root),*args])
base="ed340b9b85258194247334b85e62cf9c23d4d051";head="f3fef22448ce4f9bed8fd249a21a5d472148bd3d"
manifest=json.loads((evidence/"MANIFEST.json").read_text())
for r in manifest: assert hashlib.sha256((evidence/r["file"]).read_bytes()).hexdigest()==r["published_sha256"]
index=read("evidence-index"); byname={r["file"]:r for r in manifest}
for r in index: assert r["sha256"]==byname["author/"+r["file"]]["original_sha256"]
receipts=read("final-receipts"); assert receipts["head"]==head and receipts["base"]==base
artifacts={r["path"]:r for r in read("run-artifacts")}
gates=[]
for family in ["processor","campaigns","parent"]:
 for ref,items in receipts[family].items():
  for name,r in items.items():
   assert r["rc"]==0,(family,ref,name)
   assert r["sha256"]==artifacts[r["log"]]["sha256"],r["log"]
   assert artifacts[r["rc_file"]]["sha256"]==hashlib.sha256(b"0\n").hexdigest()
   gates.append({"family":family,"ref":ref,"name":name,"rc":r["rc"],"log":r["log"],"log_sha256":r["sha256"]})
suite=read("suite-comparison")
assert len(suite["suites"]["head"])==33
for ref in ["base","head"]: assert sum(suite["suites"][ref].values())==suite["totals"][ref]
assert suite["differences"]=={"aecp_notify":{"base":65,"head":66}}
comparison=read("record-comparison")
assert all(not r["differences"] for r in comparison.values())
assert sum(len(r["added"]) for r in comparison.values())==2
area=read("area-comparison")
assert area["base"]["parameters"]==area["head"]["parameters"]
for k,v in area["delta"].items(): assert v==area["head"]["resources"][k]-area["base"]["resources"][k]
assert area["delta"]["LUT"]<=20 and area["delta"]["FF"]<=20
assert all(r["base"]==r["head"] for r in area["images"].values())
source="hdl/aecp/KL_aecp_notify.sv"
b=git("show",base+":"+source).decode();h=git("show",head+":"+source).decode()
# The module declaration ends at its first closing port-list line.
# Locate it without depending on whitespace in a hand-maintained inventory.
import re
def decl(s): return re.split(r"\n\s*\);",s[s.index("module KL_aecp_notify"):],maxsplit=1)[0]
assert decl(b)==decl(h)
def two(s): return s[s.index("  if (N_IF_P > 1) begin : g_ca_turns"):s.index("  end else begin : g_ca_own")]
assert two(b)==two(h).replace("    assign cx_wait_w = '0;\n","")
unchanged=["hdl/top/protocol_processor_top.sv","hdl/common/pp_pkg.sv","tb/aecp_notify/port_tuple.hpp","docs/architecture/02_interfaces.md","docs/architecture/07_memory_maps.md"]
for f in unchanged: assert git("show",base+":"+f)==git("show",head+":"+f)
area_ref="521373f6672f0058c859961e33f2cab04afb328c"
area_diff=git("diff","--name-only",area_ref,head,"--","hdl","syn").decode()
assert not area_diff
parent=read("parent-final-state")
assert parent["parent_head"]=="28f9666feab2b2ba287643c63ed3a16b1e0bb863"
assert parent["processor_head"]==head and parent["both_adoption_patches_reverse_check"]
assert parent["staged_gitlink"]==f"160000 {head} 0\tprotocol-processor"
result={"verified_published_manifest_entries":len(manifest),"published_gate_receipts":gates,"suite_totals":suite["totals"],"all_common_campaign_records_equal":True,"new_campaign_records":comparison["notify"]["added"],"area_delta":area["delta"],"area_production_inputs_unchanged_since":area_ref,"declaration_identical":True,"count_two_branch_identical_except_zero_tie":True,"unchanged_authorities":unchanged,"parent_head":parent["parent_head"],"parent_processor_gitlink":parent["staged_gitlink"],"parent_adoption_patches_verified_by_public_receipt":True,"limits":"Log hashes and gate outcomes are published receipts; unexported raw logs and synthesis reports were not read or independently recomputed."}
(packet/"receipts/public-scope-audit.json").write_text(json.dumps(result,indent=2)+"\n")
print("PASS:",len(manifest),"published manifest entries;",len(gates),"gate receipts; source scope; count-two identity; area input closure; parent provenance")

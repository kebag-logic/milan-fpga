"""P12: the single contract finding recorded by A10's act runs on scratch
66ba2106 (ac5-act/01.log docs-check, ac5-act/02.log full-ci-gate) is
byte-identical to what the 6af65a15 and ad624931 checkers report natively
on the same one-line edit (p5 scenario S6)."""
import json, pathlib, sys
root = pathlib.Path(__file__).resolve().parent.parent


def finding(text: str) -> list[str]:
    out = []
    for line in text.split("\n"):
        if "script is not the canonical form" in line and ".github/workflows/docs.yml:" in line:
            out.append(line[line.index(".github/workflows/docs.yml:"):].rstrip("\r"))
    return out


act_docs = finding((root / "receipts/public-evidence/ac5-act/01.log").read_text(encoding="utf-8"))
act_rtl = finding((root / "receipts/public-evidence/ac5-act/02.log").read_text(encoding="utf-8"))
p5 = json.loads((root / "logs/p5-maintenance-ac5.json").read_text())
native = {k: [f[f.index(".github/workflows/docs.yml:"):] for f in v["check"]["fails"]]
          for k, v in p5.items() if k.startswith("S6")}
res = {"act_docs_findings": act_docs, "act_rtl_full_findings": act_rtl, "native": native,
       "act_docs_equals_head_native": act_docs == native["S6 AC5 tamper at ad624931"],
       "act_rtl_equals_head_native": act_rtl == native["S6 AC5 tamper at ad624931"],
       "r1_native_equals_head_native": native["S6 AC5 tamper at 6af65a15"] == native["S6 AC5 tamper at ad624931"],
       "base_native_findings": native["S6 AC5 tamper at b17580b9"]}
json.dump(res, open(sys.argv[1], "w"), indent=1)
print(json.dumps(res, indent=1))
sys.exit(0 if res["act_docs_equals_head_native"] and res["act_rtl_equals_head_native"]
         and res["r1_native_equals_head_native"] and not res["base_native_findings"] else 1)

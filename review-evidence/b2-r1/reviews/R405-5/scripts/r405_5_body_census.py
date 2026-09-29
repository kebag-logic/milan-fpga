#!/usr/bin/env python3
"""R405-5: check the PR #622 body's Round 2 F2 bullet against the recorded
command census (the output of r405_4_census.py) and against the #606 page.

Checks (F7 of R405-4):
  - the bullet's derivation clause names the ACMP count as state-changing,
    with its 105 CONNECT_RX / 105 DISCONNECT_RX split, all to the peer's input;
  - no unqualified "<n> ACMP commands" remains anywhere in the body;
  - every count the bullet states equals the census receipt;
  - the bullet's census sentences agree with the page's (:264-268, :277-279).
Also reports GitHub closing keywords followed by an issue reference.

Usage: r405_5_body_census.py <pr-body.md> <census receipt> <606 page>
Exit 0 only if every check holds."""
import re, sys

body = open(sys.argv[1], encoding="utf-8").read()
census = open(sys.argv[2], encoding="utf-8").read()
page = open(sys.argv[3], encoding="utf-8").read()
fails = []

def check(cond, what):
    print(("ok   " if cond else "FAIL ") + what)
    if not cond: fails.append(what)

bullets = [l for l in body.splitlines() if l.startswith("- **F2, the saved-state layer.**")]
check(len(bullets) == 1, f"exactly one Round 2 F2 bullet ({len(bullets)})")
b = bullets[0] if bullets else ""

# census values, parsed from the receipt
def cnt(key):
    m = re.search(re.escape(key) + r" (\d+)", census)
    return int(m.group(1)) if m else None
sc = re.search(r"state-changing commands by \(command, addressed entity, index\): (\{.*\})", census).group(1)
sc = eval(sc)
dutin = eval(re.search(r"commands addressed to a DUT stream input \(descriptor type 5\): (\{[^}]*\})", census).group(1))
aecp_names = eval(re.search(r"AECP command names seen: (\[.*\])", census).group(1))
acmp_total = int(re.search(r"ACMP commands in total: (\d+)", census).group(1))
print("census: state-changing", sc, "| to DUT inputs", dutin, "| ACMP total", acmp_total)
check("RESULT: PASS" in census, "census receipt RESULT: PASS")
check(sc == {("CONNECT_RX", "PEER", 8): 105, ("DISCONNECT_RX", "PEER", 8): 105},
      "recorded state-changing = 105 CONNECT_RX + 105 DISCONNECT_RX, all PEER input 8")
check(all(n.startswith(("GET_", "READ_")) for n in aecp_names), "recorded AECP commands all GET_/READ_ (no AECP write)")

# F7 clause
clause = "210 state-changing ACMP commands (105 `CONNECT_RX`, 105 `DISCONNECT_RX`), all to the peer's input, and no AECP write"
check(clause in b, "bullet carries the state-changing clause: " + clause)
unq = re.findall(r"\b\d[\d,]* ACMP commands\b", body)
check(not unq, f"no unqualified '<n> ACMP commands' in the body ({unq})")
check("210 ACMP commands all to the peer" not in body, "old F7 text absent")
check(str(acmp_total) not in b, f"bullet does not claim the {acmp_total}-command ACMP total")

# every count in the bullet vs census / page
n_sc = sum(sc.values())
check(f"{n_sc} state-changing" in b and f"The {n_sc} `CONNECT_RX` and `DISCONNECT_RX` went to the reference peer" in b,
      f"bullet's two statements of the {n_sc} state-changing commands agree")
check("no state-changing command addressed one" in b, "bullet: no state-changing command addressed a DUT input")
check("every AECP command was a GET_ or READ_" in b, "bullet: every AECP command a GET_ or READ_")
want = f"{dutin['GET_RX_STATE']} GET_RX_STATE (the polls above), {dutin['GET_COUNTERS']} GET_COUNTERS and {dutin['READ_DESCRIPTOR']} READ_DESCRIPTOR"
check(want in b, "bullet's reads to DUT inputs equal the census: " + want)
m1 = re.search(r"\('GET_RX_STATE', 1\): (\d+)", census); m0 = re.search(r"\('GET_RX_STATE', 0\): (\d+)", census)
check(m1 and f"Stream Input 1 read unbound in {m1.group(1)} distinct polls" in b, "bullet's input-1 poll count equals census")
check(m0 and int(m0.group(1)) == 2 and "Stream Input 0 at the two censuses only" in b, "bullet's input-0 polls (2) equal census")

# page agreement
check("The lane's only state-changing commands were 105 `CONNECT_RX` and 105 `DISCONNECT_RX`." in page,
      "page :264 names the same 105 + 105 as the only state-changing commands")
check("All went to the reference peer's Stream Input 8" in page, "page :265 peer's Stream Input 8")
check(want in page, "page :279 carries the same read counts")
check("No state-changing command addressed a DUT stream input" in page, "page :277 premise")
for s in ["226 console samples", "commits (2 / 0)", "slots (229 / 230)"]:
    check(s in b, f"bullet keeps '{s}'")
check("in all 226 console samples" in page, "page :262 226 console samples")

# closing references (GitHub keywords followed by an issue reference)
kw = r"\b(close|closes|closed|fix|fixes|fixed|resolve|resolves|resolved)\b:?\s+(?:[\w.-]+/[\w.-]+)?#\d+"
closing = re.findall(kw, body, flags=re.I)
kw_url = r"\b(close|closes|closed|fix|fixes|fixed|resolve|resolves|resolved)\b:?\s+https://github\.com/[\w.-]+/[\w.-]+/issues/\d+"
closing += re.findall(kw_url, body, flags=re.I)
check(not closing, f"no closing keyword + issue reference ({closing})")
rel = re.findall(r"^Relates to (#\d+)$", body, flags=re.M)
check(rel == ["#606", "#608", "#75"], f"'Relates to' lines {rel}")

print("RESULT:", "PASS" if not fails else f"FAIL ({len(fails)})")
sys.exit(1 if fails else 0)

#!/usr/bin/env python3
"""Re-check the IEEE 802.1AS / Milan v1.2 clause claims of the #511 record.

Usage: check_clauses.py <standards-dir> <work-dir>

<standards-dir> holds the licensed PDFs (placeholder: $STANDARDS_DIR):
  802.1AS-2011.pdf, 802.1AS-2011_Cor1-2013.pdf, 802.1AS-2011_Cor_2-2015.pdf,
  802.1AS-2020.pdf, "Milan_Specification_Consolidated_v1.2_Final_Approved 20231130.pdf"
Each is converted with `pdftotext -layout` into <work-dir>. Every check prints
PASS/FAIL with the matching line number; only short fragments are echoed.
The last section maps EVERY 2011 occurrence of `delayAsymmetry` to its
enclosing numbered clause, so an unlisted arithmetic site would be visible.
Exit 0 = all checks PASS.
"""
import hashlib
import os
import re
import subprocess
import sys

DOCS = {
    "as2011": "802.1AS-2011.pdf",
    "cor1": "802.1AS-2011_Cor1-2013.pdf",
    "cor2": "802.1AS-2011_Cor_2-2015.pdf",
    "as2020": "802.1AS-2020.pdf",
    "milan": "Milan_Specification_Consolidated_v1.2_Final_Approved 20231130.pdf",
}
FAILS = []


def load(std, work, key):
    pdf = os.path.join(std, DOCS[key])
    txt = os.path.join(work, key + ".txt")
    subprocess.run(["pdftotext", "-layout", pdf, txt], check=True)
    with open(pdf, "rb") as fh:
        digest = hashlib.sha256(fh.read()).hexdigest()
    print(f"# {key}: {DOCS[key]} sha256={digest}")
    with open(txt, encoding="utf-8", errors="replace") as fh:
        return fh.read().splitlines()


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def find(lines, pat, start=0, end=None):
    rx = re.compile(pat)
    for i in range(start, len(lines) if end is None else end):
        if rx.search(lines[i]):
            return i
    return -1


def check(name, ok, detail=""):
    print(f"{'PASS' if ok else 'FAIL'} {name}{': ' + detail if detail else ''}")
    if not ok:
        FAILS.append(name)


def has(name, lines, pat, start=0, end=None):
    i = find(lines, pat, start, end)
    check(name, i >= 0, f"line {i + 1}: {norm(lines[i])[:110]}" if i >= 0 else f"/{pat}/ absent")
    return i


def span(lines, head_pat, stop_pat):
    s = find(lines, head_pat)
    e = find(lines, stop_pat, s + 1) if s >= 0 else -1
    return s, e


def main():
    std, work = sys.argv[1], sys.argv[2]
    os.makedirs(work, exist_ok=True)
    t = {k: load(std, work, k) for k in DOCS}
    a = t["as2011"]

    print("\n## IEEE 802.1AS-2011")
    has("8.3 measurement not required", a, r"does not explicitly require the measurement of delayAsymmetry")
    has("8.3 sign: positive when responder->initiator longer", a, r"delayAsymmetry is defined to be positive when the responder to initiator")
    s, e = span(a, r"^\s+10\.2\.4\.8 delayAsymmetry:", r"^\s+10\.2\.4\.9 ")
    para = " ".join(a[s:e]) if s >= 0 else ""
    check("10.2.4.8 unmodelled means zero", "not modeled, then delayAsymmetry is zero" in norm(para), f"lines {s + 1}-{e}")
    check("10.2.4.8 names no data type", s >= 0 and "data type" not in para.lower(), f"lines {s + 1}-{e}")
    has("10.2.4.5 is syncInterval (donor citation)", a, r"^\s+10\.2\.4\.5 syncInterval:")
    fig = find(a, r"Figure 10-9—ClockSlaveSync state machine\s*$")
    has("Fig 10-9 syncReceiptTime + delayAsymmetry", a, r"neighborPropDelay\*\(rcvdPSSyncPtr->rateRatio/neighborRateRatio\) \+ delayAsymmetry;", fig - 40, fig)
    has("Fig 10-9 syncReceiptLocalTime + delayAsymmetry/rateRatio", a, r"^\s+delayAsymmetry/rcvdPSSyncPtr->rateRatio;", fig - 40, fig)
    f4 = find(a, r"Figure 10-4—PortSyncSyncReceive state machine\s*$")
    has("Fig 10-4 rateRatio += (neighborRateRatio - 1)", a, r"rateRatio \+= \(neighborRateRatio", f4 - 30, f4)
    s, e = span(a, r"^\s+11\.1\.3 Transport of time-synchronization information", r"^\s+11\.1\.4 ")
    has("11.1.3 d) delayAsymmetry divided by rateRatio_i", a, r"d\)\s+The quantity delayAsymmetry \(see 10\.2\.4\.8\) divided by rateRatio", s, e)
    has("11.1.3 e) (ts,i - upstreamTxTime)(rateRatio_i) in setFollowUp", a, r"e\)\s+The quantity \(ts,i – upstreamTxTime\)\(rateRatioi\)", s, e)
    s, e = span(a, r"^\s+11\.2\.13\.2\.1 setMDSyncReceive\(\)", r"^\s+g\)\s+gmTimeBaseIndicator")
    has("11.2.13.2.1 f) minus delayAsymmetry/rateRatio", a, r"delayAsymmetry \(see 10\.2\.4\.8\) for this port divided by rateRatio \[see e\) above\]", s, e)
    has("11.2.13.2.1 NOTE 2 negligible, same for delayAsymmetry", a, r"same is true of any delayAsymmetry", s, e)
    s, e = span(a, r"^\s+11\.2\.14\.2\.3 setFollowUp\(\)", r"^\s+b\)\s+sourcePortIdentity is set equal")
    has("11.2.14.2.3 a) rateRatio x (egress - upstreamTxTime)", a, r"<syncEventEgressTimestamp>.*upstreamTxTime", s, e)
    has("10.2.11 relays only another port's PortSyncSync", a, r"rcvdPSSyncPtr->localPortNumber != thisPort")
    has("11.2.15 is the MDPdelayReq machine (donor citation)", a, r"^\s+11\.2\.15 MDPdelayReq state machine")
    s, e = span(a, r"^\s+11\.2\.15\.2\.4 computePropTime\(\)", r"^\s+11\.2\.15\.(?:2\.[5-9]|3)\b")
    check("11.2.15.2.4 computePropTime has no asymmetry term", s >= 0 and "asymmetry" not in " ".join(a[s:e]).lower(), f"lines {s + 1}-{e}")
    has("Table 11-5 Follow_Up asymmetry corrections via 11.2.13.2.1/11.2.14.2.3", a, r"the quantity delayAsymmetry is used in the")
    s, e = span(a, r"^\s+14\.6\.9 delayAsymmetry\s*$", r"^\s+14\.6\.10 ")
    body = " ".join(a[s:e]).lower()
    check("14.6.9 defines without grading", s >= 0 and not re.search(r"recommend|shall|required|optional", body), f"lines {s + 1}-{e}")
    tab = find(a, r"^\s+Table 14-6—Port Parameter Data Set Table\s*$", 11000)
    row = has("Table 14-6 row: delayAsymmetry scaledNs RW Tdot3FD 14.6.9", a, r"^\s+delayAsymmetry\s+scaledNs\s+RW\s+Tdot3FD\s+14\.6\.9", tab, tab + 40)
    check("Table 14-6 '(recommended)' sits under the data type", row >= 0 and "(recommended)" in a[row + 1], norm(a[row + 1]) if row >= 0 else "")
    has("Table 14-6 footnote Tdot3FD text", a, r"Tdot3FD = Required for time-aware IEEE 802\.3 full-duplex port", tab, tab + 45)
    has("14.6.25 is the Port Parameter Data Set Table", a, r"^\s+14\.6\.25 Port Parameter Data Set Table")
    s, e = span(a, r"^\s+14\.3\.2 offsetFromMaster\s*$", r"^\s+14\.3\.3 ")
    check("14.3.2 recommended data type scaledNs (offsetFromMaster)", s >= 0 and "It is recommended that the data type be scaledNs" in norm(" ".join(a[s:e])), f"lines {s + 1}-{e}")
    mgt = has("A.5 MGT status O", a, r"^\s+MGT\s+Is management of the timing\s+O\s+Clause 15")
    if mgt >= 0:
        print(f"INFO A.5 MGT continuation: {norm(a[mgt + 1])}")
    has("A.7 MINTA-8 asymmetry modelling optional (O, 8.3)", a, r"MINTA-8\s+If path delay asymmetry is modeled by this\s+O\s+8\.3")
    has("E.5.2.2 CSN egress ClockSlaveSync takes delayAsymmetry from CSN TLV", a, r"upstreamTxTime, neighborPropDelay, neighborRateRatio, and delayAsymmetry values from the respective")
    has("8.4.3 generation of event message timestamps", a, r"^\s+8\.4\.3 Generation of event message timestamps")

    print("\n## Every 2011 occurrence of delayAsymmetry, by enclosing numbered clause")
    head = re.compile(r"^\s{6,}(?:[0-9]{1,2}(?:\.[0-9]+)+|[A-G]\.[0-9]+(?:\.[0-9]+)*)\s+\S")
    cap = re.compile(r"(Figure|Table) [0-9A-G]+-?[0-9]*—")
    for i, ln in enumerate(a):
        if "delayasymmetry" in ln.lower() and "...." not in ln:
            h = next((norm(a[j])[:60] for j in range(i, -1, -1) if head.match(a[j])), "?")
            c = next((norm(a[j])[:50] for j in range(i, min(i + 40, len(a))) if cap.search(a[j])), "")
            pc = next((norm(a[j])[:50] for j in range(i, max(i - 15, 0), -1) if cap.search(a[j])), "")
            print(f"  line {i + 1:5d} | clause: {h} | caption above: {pc} | caption below: {c}")

    print("\n## IEEE 802.1AS-2011/Cor1-2013")
    c1 = t["cor1"]
    tab = find(c1, r"^\s*Change Table 14-6 as follows")
    has("Cor1 replacement Table 14-6 keeps the delayAsymmetry row", c1, r"^\s*delayAsymmetry\s+scaledNs\s+RW\s+Tdot3FD\s+14\.6\.9", tab, tab + 30)
    check("Cor1 does not touch Figure 10-9", find(c1, r"Figure 10-9") < 0)
    has("Cor1 changes 10.2.12.2.1 prose", c1, r"^\s*Change 10\.2\.12\.2\.1 as follows")
    has("Cor1 restates 11.2.13.2.1 f)", c1, r"delayAsymmetry \(see 10\.2\.4\.8\) for this port divided by rateRatio \[see e\) above\]")
    check("Cor1 has no MGT change", find(c1, r"\bMGT\b") < 0)

    print("\n## IEEE 802.1AS-2011/Cor2-2015")
    c2 = t["cor2"]
    check("Cor2 has no delayAsymmetry text", find(c2, r"(?i)asymmetry") < 0)
    changes = [norm(x) for x in c2 if re.match(r"^\s*Change .* as follows", x)]
    check("Cor2 only changes Figure 11-8", changes == ["Change Figure 11-8 as follows:"], str(changes))

    print("\n## IEEE 802.1AS-2020 (comparison only)")
    b = t["as2020"]
    has("2020 10.2.13 is ClockSlaveSync", b, r"^\s*10\.2\.13 ClockSlaveSync state machine")
    has("2020 10.2.13 syncReceiptTime + delayAsymmetry", b, r"meanLinkDelay\*\(rcvdPSSyncPtrCSS->rateRatio/neighborRateRatio\) \+ delayAsymmetry;")
    has("2020 11.2.14.2.1 is setMDSyncReceiveMDSR", b, r"^\s*11\.2\.14\.2\.1 setMDSyncReceiveMDSR\(\)")
    has("2020 11.2.14.2.1 f) subtracts asymmetry only for instance-specific peer delay", b, r"state machine is invoked by the instance-specific peer-to-peer delay mechanism, minus")
    has("2020 11.2.15.2.3 is setFollowUp", b, r"^\s*11\.2\.15\.2\.3 setFollowUp\(\)")
    has("2020 11.2.17.2 a) CMLDS corrects mean link delay for delayAsymmetry", b, r"CMLDS corrects the computed mean link")

    print("\n## Milan v1.2")
    m = t["milan"]
    check("Milan v1.2 never mentions asymmetry", find(m, r"(?i)asym") < 0)
    has("4.2.5 redundancy optional", m, r"A PAAD may implement seamless redundancy as defined by Section 8")
    has("4.2.6 defers to 802.1AS", m, r"defined by \[802\.1AS\], \[802\.1AS-2011/Cor1\], and \[802\.1AS-2011/Cor2\]")
    has("Table 5.19 NOT_IMPLEMENTED = 1", m, r"^\s*1\s+NOT_IMPLEMENTED\s+The PAAD-AE does not support the command type")
    has("Table 5.20 bit 31 REDUNDANCY", m, r"^\s*31\s+0x00000001\s+REDUNDANCY")
    for sec in ("5.4.4.2", "5.4.4.3", "5.4.4.4", "5.4.4.5", "7.6"):
        s = find(m, rf"^{re.escape(sec)} [A-Z]")
        has(f"{sec} carries the recommendation note", m, r"Support for this feature is a recommendation for Milan compliant PAADs", s, s + 4)
    has("8.1 redundancy not mandatory", m, r"Seamless network redundancy is not a mandatory requirement")
    has("8.3.1 at least two AVB-capable Ethernet ports", m, r"The R-PAAD shall have at least two AVB-capable Ethernet ports")

    print(f"\nRESULT: {len(FAILS)} failure(s) {FAILS}")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())

"""Scan every tracked Markdown paragraph (wrapped lines joined) for a µISA/ISA mention
together with a number of operations/ops/opcodes/instructions, digits or words.
usage: python3 -I para_scan.py <checkout>"""
import re, subprocess, sys
root = sys.argv[1]
files = subprocess.run(["git", "-C", root, "ls-files", "*.md"], capture_output=True, text=True).stdout.split()
num = r"(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|twenty|thirty|forty)[\w-]*"
pat = re.compile(r"(?<![A-Za-z])ISA\b.*?\b" + num + r"[- ](?:operations?|ops?|opcodes?|instructions?)\b|\b" + num +
                 r"[- ](?:operations?|ops?|opcodes?|instructions?)\b.*?(?<![A-Za-z])ISA\b", re.I | re.S)
for f in files:
    text = open(f"{root}/{f}", encoding="utf-8").read()
    for para in re.split(r"\n\s*\n", text):
        flat = " ".join(para.split())
        for m in pat.finditer(flat):
            if len(m.group(0)) < 200:
                print(f"{f}: …{m.group(0)[:200]}…")

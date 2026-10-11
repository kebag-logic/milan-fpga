#!/usr/bin/env python3
"""Compare moved C tokens, delta paths, gitlinks, and published image manifests."""
import argparse, hashlib, re, subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("checkout",type=Path);p.add_argument("packet",type=Path)
a=p.parse_args();root=a.checkout.resolve();packet=a.packet.resolve()
def git(*args):return subprocess.check_output(["git","--no-replace-objects","-C",str(root),*args])
# Preserve strings/chars and preprocessing tokens; remove only whitespace/comments.
token=re.compile(rb'(?P<comment>//[^\n]*|/\*[\s\S]*?\*/)|(?P<quoted>"(?:\\[\s\S]|[^"\\])*"|\'(?:\\[\s\S]|[^\'\\])*\')|(?P<space>\s+)|(?P<word>[A-Za-z_][A-Za-z_0-9]*|(?:[0-9]|\.[0-9])(?:[A-Za-z_0-9.]|[eEpP][+-])*)|(?P<operator>##|<<=|>>=|\.\.\.|->|\+\+|--|<<|>>|<=|>=|==|!=|&&|\|\||\+=|-=|\*=|/=|%=|&=|\^=|\|=)|(?P<other>.)')
def tokens(data):return [m.group() for m in token.finditer(data) if m.lastgroup not in ("comment","space")]
moved={"src/adp.c":"adp/adp.c","src/acmp.c":"acmp/acmp.c","src/maap.c":"maap/maap.c","include/adp.h":"adp/adp.h","include/acmp.h":"acmp/acmp.h","include/maap.h":"maap/maap.h","include/wire.h":"wire/wire.h"}
for new,old in moved.items():
 before=git("show",f"aef7ac66:sw/firmware/ctrl/{old}");after=(root/"third_party/tsn-c-stack"/new).read_bytes()
 b,c=tokens(before),tokens(after);assert b==c,(new,len(b),len(c));print("token-identical",new,len(b))
rel="sw/firmware/ctrl/mbx/mbx_wire.h";assert tokens(git("show",f"aef7ac66:{rel}"))==tokens((root/rel).read_bytes());print("surviving product C/H change is comment-only",rel)
changed=git("diff","--name-only","4cab445a..HEAD").decode().splitlines();print("round-9 changed paths:",*changed,sep="\n  ")
assert set(changed)=={"sw/firmware/ctrl/README.md","sw/firmware/ctrl/test/ctrl_boundary.py","sw/firmware/ctrl/test/ctrl_build.py","sw/firmware/ctrl/test/ctrl_pin.py"}
rtl=git("diff","--name-only","8b61b709..HEAD","--","hdl","syn","sw/mailbox");assert not rtl;print("no HDL, synthesis, or mailbox-contract change from source base")
for rel in ("third_party/lwSRP","protocol-processor","gptp-processor","third_party/verilog-axis"):
 assert git("ls-tree","8b61b709",rel)==git("ls-tree","HEAD",rel);print("unchanged gitlink",git("ls-tree","HEAD",rel).decode().strip())
files=[packet/"public"/n for n in ("images-dev.sha256","images-round8.sha256","images-head.sha256")]
blobs=[f.read_bytes() for f in files];assert blobs[0]==blobs[1]==blobs[2];assert len(blobs[0].splitlines())==35
for f,b in zip(files,blobs):print("image manifest",f.name,"35 rows",hashlib.sha256(b).hexdigest())
print("35/35 published ELF hashes equal at dev aef7ac66, round 8 and round 9; no images relinked in this review")

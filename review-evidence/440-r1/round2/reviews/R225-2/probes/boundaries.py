import json,sys
from pathlib import Path
out=Path(__file__).resolve().parents[1];scratch=Path((out/"scratch-path.txt").read_text().strip());sys.path.insert(0,str(scratch/"head/scripts"))
import gen_toc as g
rows=[]
def test(name,text,expected):
 kinds=g.blocks(text); actual=[k for l,k in zip(text.split("\n"),kinds) if l.startswith("## ")]
 rows.append(dict(name=name,text=text,expected=expected,actual=actual));assert actual==expected,rows[-1]
for opener in ("pre","script","style","textarea"):
 for other in ("div","title","xmp"):
  for join in ("\n","x"):
   for case in (other,other.upper()):
    for final in ("","\n"):
     test(f"other/{opener}/{case}/{join!r}/eof{not final}",f"<{opener}>{join}</{case}>\n## Hidden"+final,[g.HTML])
    test(f"recovery/{opener}/{case}/{join!r}",f"<{opener}>{join}</{case}>\n## Hidden\n</sTyLe>\n## Visible\n<script>\n## Hidden again\n",[g.HTML,g.TEXT,g.HTML])
 for close in ("pre","script","style","textarea"):
  for join in ("\n","x"):
   test(f"valid/{opener}/{close}/{join!r}",f"<{opener}>{join}</{close.upper()}>\n## Visible",[g.TEXT])
 for suffix in (" ","\t","/","lude","\u017f"):
  test(f"malformed/{opener}/{suffix!r}",f"<{opener}>\n</{opener}{suffix}>\n## Hidden",[g.HTML])
for marker in ("`","~"):
 for width in (3,4,10):
  for close_width in (width-1,width,width+2):
   for suffix in (""," ","\t"," \t ","x","\u200b","\f"):
    test(f"fence/{marker}/{width}/{close_width}/{suffix!r}",marker*width+"\n"+marker*close_width+suffix+"\n## Probe",[g.TEXT if close_width>=width and suffix in (""," ","\t"," \t ") else g.FENCE])
for other in ("div","title","xmp"):
 test("comment precedence/"+other,"<!--\n</"+other+">\n## Hidden",[g.COMMENT])
 test("type6 precedence/"+other,"<div>\n</"+other+">\n## Hidden\n\n## Visible",[g.HTML,g.TEXT])
(out/"boundaries.json").write_text(json.dumps(rows,indent=2)+"\n")
print("Independent boundary rows:",len(rows),"PASS")

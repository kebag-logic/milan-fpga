"""List newly added comment references forbidden by the source-comment rule. Argument: checkout."""
import ast,io,re,subprocess,sys,tokenize
from pathlib import Path
root=Path(sys.argv[1]); base="7398ec0aeea468d92ff642a03a06e291a0cd58d1"
diff=subprocess.check_output(["git","-C",str(root),"diff","--unified=0",base,"HEAD"],text=True)
path="";lineno=0; added={}
for s in diff.splitlines():
 if s.startswith("+++ b/"):path=s[6:]
 elif s.startswith("@@"):
  lineno=int(re.search(r"\+(\d+)",s)[1])-1
 elif s.startswith("+"):
  lineno+=1
  if "issuecomment-" in s:added.setdefault(path,[]).append((lineno,s[1:]))
 elif not s.startswith("-") and not s.startswith("\\"):lineno+=1
for path, lines in sorted(added.items()):
 if not path.endswith((".py",".c",".h",".cpp",".sv")):continue
 text=(root/path).read_text();comments=set()
 if path.endswith(".py"):
  for token in tokenize.generate_tokens(io.StringIO(text).readline):
   if token.type==tokenize.COMMENT:comments.add(token.start[0])
  for node in ast.walk(ast.parse(text)):
   if isinstance(node,ast.Expr) and isinstance(node.value,ast.Constant) and isinstance(node.value.value,str):
    comments.update(range(node.lineno,node.end_lineno+1))
 else:
  comments={n for n,s in enumerate(text.splitlines(),1) if s.lstrip().startswith(("//","/*","*"))}
 for n,s in lines:
  if n in comments:print(f"{path}:{n}: {s.strip()}")
